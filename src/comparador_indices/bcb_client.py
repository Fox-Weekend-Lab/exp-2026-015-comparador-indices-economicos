import os
from datetime import date, datetime
from decimal import Decimal, InvalidOperation
from typing import Any

import httpx

from .models import DataError, Observation, QueryError

DEFAULT_BASE_URL = "https://api.bcb.gov.br/dados/serie/bcdata.sgs"


class BcbClient:
    def __init__(
        self,
        client: httpx.Client | None = None,
        base_url: str | None = None,
    ) -> None:
        self._client = client
        self._base_url = (
            base_url or os.getenv("BCB_SGS_BASE_URL", DEFAULT_BASE_URL)
        ).rstrip("/")

    def fetch(self, series: str, start: date, end: date) -> list[Observation]:
        url = f"{self._base_url}/{series}/dados"
        params = {
            "formato": "json",
            "dataInicial": start.strftime("%d/%m/%Y"),
            "dataFinal": end.strftime("%d/%m/%Y"),
        }
        try:
            if self._client is None:
                response = httpx.get(url, params=params, timeout=10.0)
            else:
                response = self._client.get(url, params=params, timeout=10.0)
            response.raise_for_status()
        except httpx.HTTPError as error:
            raise QueryError(
                "Não foi possível consultar o BCB. Verifique sua conexão e tente novamente."
            ) from error

        try:
            payload = response.json()
        except ValueError as error:
            raise DataError("O BCB retornou uma resposta inválida. Tente novamente.") from error

        if not isinstance(payload, list):
            raise DataError("O BCB retornou dados em formato inesperado. Tente novamente.")
        if not payload:
            raise DataError("Não há dados disponíveis para o intervalo informado.")

        return [self._parse_observation(item) for item in payload]

    @staticmethod
    def _parse_observation(item: Any) -> Observation:
        if not isinstance(item, dict):
            raise DataError("O BCB retornou uma observação inválida. Tente novamente.")
        raw_date = item.get("data")
        raw_value = item.get("valor")
        if not isinstance(raw_date, str) or not isinstance(raw_value, str):
            raise DataError("O BCB retornou uma observação inválida. Tente novamente.")

        try:
            observation_date = datetime.strptime(raw_date, "%d/%m/%Y").date()
            normalized_value = raw_value.strip()
            if "," in normalized_value:
                normalized_value = normalized_value.replace(".", "").replace(",", ".")
            value = Decimal(normalized_value)
        except (ValueError, InvalidOperation) as error:
            raise DataError("O BCB retornou uma observação inválida. Tente novamente.") from error

        return Observation(date=observation_date, value=value)
