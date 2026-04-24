from __future__ import annotations

from dataclasses import dataclass
from typing import Any, TypedDict, cast

import requests


DEFAULT_MESSAGE_API_BASE_URL = "https://training.ekos.my.id"


class MessageServiceError(Exception):
    """Raised when message API calls fail."""


class MessagePayload(TypedDict, total=False):
    nama: str
    message: str


class MessageItem(TypedDict, total=False):
    id: int | str
    nama: str
    message: str
    created_at: str


class MessageListResponse(TypedDict):
    status: str
    count: int
    data: list[MessageItem]
    raw: Any


class PostMessageResponse(TypedDict):
    status: str
    data: MessageItem | dict[str, Any]
    raw: Any


@dataclass(slots=True)
class MessageService:
    base_url: str = DEFAULT_MESSAGE_API_BASE_URL
    api_key: str | None = None
    timeout: int = 30

    def _build_headers(self) -> dict[str, str]:
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
        if self.api_key and self.api_key.strip():
            headers["x-api-key"] = self.api_key.strip()
        return headers

    def _request_json(
        self,
        method: str,
        path: str,
        params: dict[str, Any] | None = None,
        payload: dict[str, Any] | None = None,
    ) -> Any:
        url = f"{self.base_url.rstrip('/')}{path}"
        try:
            response = requests.request(
                method=method,
                url=url,
                headers=self._build_headers(),
                params=params,
                json=payload,
                timeout=self.timeout,
            )
            response.raise_for_status()
        except requests.Timeout as exc:
            raise MessageServiceError(f"Request timeout ke endpoint: {path}") from exc
        except requests.RequestException as exc:
            detail = ""
            if exc.response is not None:
                detail = f" - {exc.response.text}"
            raise MessageServiceError(f"Gagal memanggil endpoint {path}{detail}") from exc

        try:
            data = response.json()
        except ValueError as exc:
            raise MessageServiceError(f"Respons endpoint {path} bukan JSON valid.") from exc

        return data

    @staticmethod
    def _normalize_message(item: Any) -> MessageItem:
        raw = cast(dict[str, Any], item or {})
        normalized: MessageItem = {
            "nama": str(raw.get("nama") or ""),
            "message": str(raw.get("message") or ""),
        }

        if raw.get("id") is not None:
            normalized["id"] = cast(int | str, raw.get("id"))
        if raw.get("created_at") is not None:
            normalized["created_at"] = str(raw.get("created_at"))

        return normalized

    @staticmethod
    def _extract_message_list(payload: Any) -> list[MessageItem]:
        if isinstance(payload, list):
            return [MessageService._normalize_message(item) for item in payload]

        if not isinstance(payload, dict):
            return []

        candidates: list[Any] = []

        data_node = payload.get("data")
        if isinstance(data_node, list):
            candidates = data_node
        elif isinstance(data_node, dict):
            inner_list = data_node.get("items") or data_node.get("messages")
            if isinstance(inner_list, list):
                candidates = inner_list

        if not candidates:
            if isinstance(payload.get("messages"), list):
                candidates = cast(list[Any], payload.get("messages"))
            elif isinstance(payload.get("items"), list):
                candidates = cast(list[Any], payload.get("items"))

        return [MessageService._normalize_message(item) for item in candidates]

    def get_messages(self, limit: int = 20) -> MessageListResponse:
        safe_limit = max(1, min(limit, 100))
        payload = self._request_json("GET", "/api/say-hello", params={"limit": safe_limit})
        messages = self._extract_message_list(payload)
        status = str(payload.get("status") or "success") if isinstance(payload, dict) else "success"

        return {
            "status": status,
            "count": len(messages),
            "data": messages,
            "raw": payload,
        }

    def post_message(self, nama: str, message: str) -> PostMessageResponse:
        clean_nama = nama.strip()
        clean_message = message.strip()

        if not clean_nama:
            raise MessageServiceError("Nama tidak boleh kosong.")
        if not clean_message:
            raise MessageServiceError("Message tidak boleh kosong.")

        payload = self._request_json(
            "POST",
            "/api/say-hello",
            payload=MessagePayload(nama=clean_nama, message=clean_message),
        )

        if not isinstance(payload, dict):
            raise MessageServiceError("Respons POST tidak sesuai format JSON object.")

        data_node = payload.get("data")
        if isinstance(data_node, dict):
            normalized_data: MessageItem | dict[str, Any] = self._normalize_message(data_node)
        else:
            normalized_data = {}

        return {
            "status": str(payload.get("status") or "success"),
            "data": normalized_data,
            "raw": payload,
        }