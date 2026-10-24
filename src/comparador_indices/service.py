from datetime import date, datetime
from decimal import Decimal
from collections.abc import Iterable

from .models import Comparison, DataError, InputError, Observation


def parse_date(value: str) -> date:
    try:
        return datetime.strptime(value, "%d/%m/%Y").date()
    except ValueError as error:
        raise InputError("Informe as datas no formato DD/MM/AAAA.") from error


def validate_interval(start: date, end: date) -> None:
    if start > end:
        raise InputError("A data inicial deve ser anterior ou igual à data final.")


def build_comparison(
    series: str,
    requested_start: date,
    requested_end: date,
    observations: Iterable[Observation],
) -> Comparison:
    validate_interval(requested_start, requested_end)
    ordered = sorted(observations, key=lambda observation: observation.date)
    if not ordered:
        raise DataError("Não há observações disponíveis para o intervalo informado.")

    initial = ordered[0]
    final = ordered[-1]
    if initial.value == Decimal("0"):
        raise DataError("A variação não pode ser calculada porque o valor inicial é zero.")

    variation = ((final.value / initial.value) - Decimal("1")) * Decimal("100")
    return Comparison(
        series=series,
        requested_start=requested_start,
        requested_end=requested_end,
        initial=initial,
        final=final,
        variation_percent=variation,
    )
