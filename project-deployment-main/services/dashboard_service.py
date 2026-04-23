from __future__ import annotations

from dataclasses import dataclass
from typing import Any, TypedDict, cast

import requests


DEFAULT_DASHBOARD_API_BASE_URL = "https://training.ekos.my.id"


class DashboardFilters(TypedDict, total=False):
	province: str
	type: str
	year: int
	month: int
	sektor: str
	status: str
	kanwil: str


class DashboardRow(TypedDict):
	row_id: int
	npwp_bendahara: str
	provinsi: str
	sektor: str
	jenis_pajak: str
	tahun_pajak: int
	bulan: int
	penerimaan_bruto_idr: float
	restitusi_idr: float
	penerimaan_neto_idr: float
	jumlah_wp: int
	status_pembayaran: str
	kode_kanwil: str


class DashboardDataResponse(TypedDict):
	status: str
	count: int
	total: int
	filters: DashboardFilters
	data: list[DashboardRow]


class DashboardOptions(TypedDict):
	province: list[str]
	type: list[str]
	year: list[int]
	month: list[int]
	sektor: list[str]
	status: list[str]
	kanwil: list[str]


class DashboardOptionsResponse(TypedDict):
	status: str
	count: int
	filters: DashboardFilters
	options: DashboardOptions


class ReferenceOptionItem(TypedDict):
	label: str
	value: str | int


class DashboardReferences(TypedDict):
	province: list[ReferenceOptionItem]
	type: list[ReferenceOptionItem]
	year: list[ReferenceOptionItem]
	month: list[ReferenceOptionItem]
	sektor: list[ReferenceOptionItem]
	status: list[ReferenceOptionItem]
	kanwil: list[ReferenceOptionItem]


class DashboardReferencesResponse(TypedDict):
	status: str
	references: DashboardReferences


class DashboardServiceError(Exception):
    """Raised when dashboard API calls fail."""


@dataclass(slots=True)
class TaxRevenueDashboardService:
	"""Service client for tax revenue dashboard endpoints."""

	base_url: str = DEFAULT_DASHBOARD_API_BASE_URL
	api_key: str | None = None
	timeout: int = 30

	def _build_headers(self) -> dict[str, str]:
		headers = {"Accept": "application/json"}
		if self.api_key and self.api_key.strip():
			headers["Authorization"] = f"Bearer {self.api_key.strip()}"
		return headers

	@staticmethod
	def _clean_params(filters: dict[str, Any] | None) -> dict[str, Any]:
		if not filters:
			return {}

		clean: dict[str, Any] = {}
		for key, value in filters.items():
			if value is None:
				continue
			if isinstance(value, str) and not value.strip():
				continue
			clean[key] = value

		return clean

	def _request_json(self, path: str, params: dict[str, Any] | None = None) -> Any:
		url = f"{self.base_url.rstrip('/')}{path}"
		query = self._clean_params(params)

		try:
			response = requests.get(
				url,
				headers=self._build_headers(),
				params=query,
				timeout=self.timeout,
			)
			response.raise_for_status()
		except requests.Timeout as exc:
			raise DashboardServiceError(f"Request timeout ke endpoint: {path}") from exc
		except requests.RequestException as exc:
			detail = ""
			if exc.response is not None:
				detail = f" - {exc.response.text}"
			raise DashboardServiceError(f"Gagal memanggil endpoint {path}{detail}") from exc

		try:
			return response.json()
		except ValueError as exc:
			raise DashboardServiceError(f"Respons endpoint {path} bukan JSON valid.") from exc

	@staticmethod
	def _to_int(value: Any) -> int:
		try:
			return int(value)
		except (TypeError, ValueError):
			return 0

	@staticmethod
	def _to_float(value: Any) -> float:
		try:
			return float(value)
		except (TypeError, ValueError):
			return 0.0

	@staticmethod
	def _normalize_filters(filters: Any) -> DashboardFilters:
		raw = cast(dict[str, Any], filters or {})
		normalized: DashboardFilters = {}

		if raw.get("province"):
			normalized["province"] = str(raw["province"])
		if raw.get("type"):
			normalized["type"] = str(raw["type"])
		if raw.get("year") is not None:
			normalized["year"] = TaxRevenueDashboardService._to_int(raw["year"])
		if raw.get("month") is not None:
			normalized["month"] = TaxRevenueDashboardService._to_int(raw["month"])
		if raw.get("sektor"):
			normalized["sektor"] = str(raw["sektor"])
		if raw.get("status"):
			normalized["status"] = str(raw["status"])
		if raw.get("kanwil"):
			normalized["kanwil"] = str(raw["kanwil"])

		return normalized

	@staticmethod
	def _normalize_row(item: Any) -> DashboardRow:
		row = cast(dict[str, Any], item or {})
		return {
			"row_id": TaxRevenueDashboardService._to_int(row.get("row_id")),
			"npwp_bendahara": str(row.get("npwp_bendahara") or ""),
			"provinsi": str(row.get("provinsi") or ""),
			"sektor": str(row.get("sektor") or ""),
			"jenis_pajak": str(row.get("jenis_pajak") or ""),
			"tahun_pajak": TaxRevenueDashboardService._to_int(row.get("tahun_pajak")),
			"bulan": TaxRevenueDashboardService._to_int(row.get("bulan")),
			"penerimaan_bruto_idr": TaxRevenueDashboardService._to_float(row.get("penerimaan_bruto_idr")),
			"restitusi_idr": TaxRevenueDashboardService._to_float(row.get("restitusi_idr")),
			"penerimaan_neto_idr": TaxRevenueDashboardService._to_float(row.get("penerimaan_neto_idr")),
			"jumlah_wp": TaxRevenueDashboardService._to_int(row.get("jumlah_wp")),
			"status_pembayaran": str(row.get("status_pembayaran") or ""),
			"kode_kanwil": str(row.get("kode_kanwil") or ""),
		}

	@staticmethod
	def _normalize_options(values: Any, as_int: bool = False) -> list[str] | list[int]:
		raw_values = values if isinstance(values, list) else []
		if as_int:
			return [TaxRevenueDashboardService._to_int(v) for v in raw_values]
		return [str(v) for v in raw_values if str(v)]

	@staticmethod
	def _normalize_reference_items(items: Any, as_int: bool = False) -> list[ReferenceOptionItem]:
		raw_items = items if isinstance(items, list) else []
		normalized: list[ReferenceOptionItem] = []

		for item in raw_items:
			if not isinstance(item, dict):
				continue

			label = str(item.get("label") or "")
			value: str | int
			if as_int:
				value = TaxRevenueDashboardService._to_int(item.get("value"))
			else:
				raw_value = item.get("value")
				value = str(raw_value) if raw_value is not None else ""

			if not label:
				label = str(value)

			normalized.append({"label": label, "value": value})

		return normalized

	def get_dashboard_data(self, filters: DashboardFilters | None = None) -> DashboardDataResponse:
		"""Get filtered main dashboard data from /api/tax-revenue-dashboard."""
		payload = cast(dict[str, Any], self._request_json("/api/tax-revenue-dashboard", params=filters))
		rows = [self._normalize_row(item) for item in cast(list[Any], payload.get("data") or [])]

		return {
			"status": str(payload.get("status") or "unknown"),
			"count": self._to_int(payload.get("count")),
			"total": self._to_int(payload.get("total")),
			"filters": self._normalize_filters(payload.get("filters")),
			"data": rows,
		}

	def get_options(self, active_filters: DashboardFilters | None = None) -> DashboardOptionsResponse:
		"""Get cascading options based on active filters from /api/tax-revenue-dashboard/options."""
		payload = cast(dict[str, Any], self._request_json("/api/tax-revenue-dashboard/options", params=active_filters))
		options = cast(dict[str, Any], payload.get("options") or {})

		return {
			"status": str(payload.get("status") or "unknown"),
			"count": self._to_int(payload.get("count")),
			"filters": self._normalize_filters(payload.get("filters")),
			"options": {
				"province": cast(list[str], self._normalize_options(options.get("province"))),
				"type": cast(list[str], self._normalize_options(options.get("type"))),
				"year": cast(list[int], self._normalize_options(options.get("year"), as_int=True)),
				"month": cast(list[int], self._normalize_options(options.get("month"), as_int=True)),
				"sektor": cast(list[str], self._normalize_options(options.get("sektor"))),
				"status": cast(list[str], self._normalize_options(options.get("status"))),
				"kanwil": cast(list[str], self._normalize_options(options.get("kanwil"))),
			},
		}

	def get_references(self) -> DashboardReferencesResponse:
		"""Get full master references from /api/tax-revenue-dashboard/references."""
		payload = cast(dict[str, Any], self._request_json("/api/tax-revenue-dashboard/references"))
		references = cast(dict[str, Any], payload.get("references") or {})

		return {
			"status": str(payload.get("status") or "unknown"),
			"references": {
				"province": self._normalize_reference_items(references.get("province")),
				"type": self._normalize_reference_items(references.get("type")),
				"year": self._normalize_reference_items(references.get("year"), as_int=True),
				"month": self._normalize_reference_items(references.get("month"), as_int=True),
				"sektor": self._normalize_reference_items(references.get("sektor")),
				"status": self._normalize_reference_items(references.get("status")),
				"kanwil": self._normalize_reference_items(references.get("kanwil")),
			},
		}
