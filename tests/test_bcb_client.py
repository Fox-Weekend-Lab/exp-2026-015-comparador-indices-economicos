from datetime import date
from decimal import Decimal

import httpx
import pytest

from comparador_indices.bcb_client import BcbClient
from comparador_indices.models import DataError, QueryError


def test_fetch_builds_sgs_request_and_converts_observations() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/sgs/433/dados"
        assert dict(request.url.params) == {
            "formato": "json",
            "dataInicial": "01/01/2024",
            "dataFinal": "31/01/2024",
        }
        return httpx.Response(200, json=[{"data": "01/01/2024", "valor": "10,50"}])

    transport = httpx.MockTransport(handler)
    with httpx.Client(transport=transport) as http_client:
        client = BcbClient(http_client, base_url="https://example.invalid/sgs")
        observations = client.fetch("433", date(2024, 1, 1), date(2024, 1, 31))

    assert observations[0].date == date(2024, 1, 1)
    assert observations[0].value == Decimal("10.50")


def test_fetch_rejects_empty_response() -> None:
    transport = httpx.MockTransport(lambda request: httpx.Response(200, json=[]))
    with httpx.Client(transport=transport) as http_client:
        client = BcbClient(http_client, base_url="https://example.invalid")
        with pytest.raises(DataError, match="Não há dados"):
            client.fetch("1", date(2024, 1, 1), date(2024, 1, 2))


def test_fetch_translates_http_failure() -> None:
    transport = httpx.MockTransport(lambda request: httpx.Response(500))
    with httpx.Client(transport=transport) as http_client:
        client = BcbClient(http_client, base_url="https://example.invalid")
        with pytest.raises(QueryError, match="Não foi possível consultar"):
            client.fetch("1", date(2024, 1, 1), date(2024, 1, 2))
