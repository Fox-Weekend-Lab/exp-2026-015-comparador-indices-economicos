from dataclasses import dataclass
from datetime import date
from decimal import Decimal


class ComparisonError(Exception):
    """Erro esperado que pode ser apresentado ao usuário."""


class InputError(ComparisonError):
    """Erro nos argumentos ou no intervalo informado."""


class DataError(ComparisonError):
    """Erro nos dados retornados pelo serviço."""


class QueryError(ComparisonError):
    """Erro durante a consulta ao serviço remoto."""


@dataclass(frozen=True)
class Observation:
    date: date
    value: Decimal


@dataclass(frozen=True)
class Comparison:
    series: str
    requested_start: date
    requested_end: date
    initial: Observation
    final: Observation
    variation_percent: Decimal
