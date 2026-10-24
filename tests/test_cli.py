from datetime import date
from decimal import Decimal
from io import StringIO

from comparador_indices.cli import run
from comparador_indices.models import Observation


class FakeClient:
    def fetch(self, series: str, start: date, end: date) -> list[Observation]:
        assert series == "433"
        return [
            Observation(date(2024, 1, 1), Decimal("100")),
            Observation(date(2024, 1, 31), Decimal("105")),
        ]


def test_cli_prints_table_without_network_access() -> None:
    output = StringIO()
    error = StringIO()

    exit_code = run(["433", "01/01/2024", "31/01/2024"], FakeClient(), output, error)

    assert exit_code == 0
    assert "Variação acumulada" in output.getvalue()
    assert "5,00%" in output.getvalue()
    assert error.getvalue() == ""


def test_cli_reports_invalid_date_before_querying() -> None:
    output = StringIO()
    error = StringIO()

    exit_code = run(["433", "2024-01-01", "31/01/2024"], FakeClient(), output, error)

    assert exit_code == 1
    assert "formato DD/MM/AAAA" in error.getvalue()
