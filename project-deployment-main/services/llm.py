from __future__ import annotations

from dataclasses import dataclass

import requests


DEFAULT_OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"


class OpenRouterError(Exception):
    """Raised when OpenRouter API calls fail."""


@dataclass(slots=True)
class OpenRouterService:
    api_key: str
    base_url: str = DEFAULT_OPENROUTER_BASE_URL
    timeout: int = 60
    app_name: str = "data-project-deployment"
    app_url: str = "https://localhost"
    provider: list[str] | None = None

    def _build_headers(self) -> dict[str, str]:
        if not self.api_key.strip():
            raise OpenRouterError("OpenRouter API key tidak boleh kosong.")

        return {
            "Authorization": f"Bearer {self.api_key.strip()}",
            "Content-Type": "application/json",
            "HTTP-Referer": self.app_url,
            "X-Title": self.app_name,
        }

    def chat_completion(
        self,
        prompt: str,
        model: str = "openai/gpt-4o-mini",
        temperature: float = 0.7,
        max_tokens: int = 256,
        provider: list[str] | None = ['Azure'],
    ) -> str:
        if not prompt.strip():
            raise OpenRouterError("Prompt tidak boleh kosong.")

        if not model.strip():
            raise OpenRouterError("Model OpenRouter tidak boleh kosong.")

        url = f"{self.base_url.rstrip('/')}/chat/completions"
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": temperature,
            "max_tokens": max_tokens,
            "extra_body": {
                "provider": {
                    "order": provider if provider else []
                },
            }
        }

        try:
            response = requests.post(
                url,
                headers=self._build_headers(),
                json=payload,
                timeout=self.timeout,
            )
            response.raise_for_status()
        except requests.Timeout as exc:
            raise OpenRouterError("Request ke OpenRouter timeout.") from exc
        except requests.RequestException as exc:
            detail = ""
            if exc.response is not None:
                detail = f" - {exc.response.text}"
            raise OpenRouterError(f"Gagal memanggil OpenRouter{detail}") from exc

        try:
            data = response.json()
            content = data["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError, ValueError) as exc:
            raise OpenRouterError("Respons OpenRouter tidak sesuai format yang diharapkan.") from exc

        if not isinstance(content, str) or not content.strip():
            raise OpenRouterError("OpenRouter mengembalikan respons kosong.")

        return content


def dummy_llm_response(prompt: str, mode: str = "dummy") -> str:
    if not prompt.strip():
        return "Prompt masih kosong."
    return f"[Placeholder {mode}] Respons untuk: {prompt}"


def call_openrouter_endpoint(
    prompt: str,
    api_key: str,
    model: str = "openai/gpt-4o-mini",
    timeout: int = 60,
) -> str:
    service = OpenRouterService(api_key=api_key, timeout=timeout)
    return service.chat_completion(prompt=prompt, model=model)


def call_generic_endpoint(url: str, prompt: str, api_key: str, timeout: int) -> str:
    if not url.strip():
        return "URL endpoint belum diisi."

    service = OpenRouterService(api_key=api_key, base_url=url, timeout=timeout)
    return service.chat_completion(prompt=prompt)
