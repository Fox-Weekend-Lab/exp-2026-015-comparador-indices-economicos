from datetime import date
from decimal import Decimal

import pytest

from comparador_indices.models import DataError, InputError, Observation
from comparador_indices.service import build_comparison, parse_date


def test_build_comparison_orders_observations_and_calculates_positive_variation() -> None:
    comparison = build_comparison(
        "433",
        date(2024, 1, 1),
        date(2024, 3, 1),
        [
            Observation(date(2024, 3, 1), Decimal("110")),
            Observation(date(2024, 1, 1), Decimal("100")),
        ],
    )

    assert comparison.initial.value == Decimal("100")
    assert comparison.final.value == Decimal("110")
    assert comparison.variation_percent == Decimal("10.0")


def test_build_comparison_calculates_negative_and_zero_variation() -> None:
    negative = build_comparison(
        "1", date(2024, 1, 1), date(2024, 2, 1),
        [Observation(date(2024, 1, 1), Decimal("100")), Observation(date(2024, 2, 1), Decimal("90"))],
    )
    zero = build_comparison(
        "1", date(2024, 1, 1), date(2024, 1, 1),
        [Observation(date(2024, 1, 1), Decimal("100"))],
    )

    assert negative.variation_percent == Decimal("-10.0")
    assert zero.variation_percent == Decimal("0")


def test_service_rejects_inverted_interval_and_zero_initial_value() -> None:
    with pytest.raises(InputError, match="data inicial"):
        build_comparison("1", date(2024, 2, 1), date(2024, 1, 1), [])
    with pytest.raises(DataError, match="inicial é zero"):
        build_comparison(
            "1", date(2024, 1, 1), date(2024, 1, 2),
            [Observation(date(2024, 1, 1), Decimal("0"))],
        )


def test_parse_date_rejects_invalid_format() -> None:
    with pytest.raises(InputError, match="DD/MM/AAAA"):
        parse_date("2024-01-01")
