import argparse
import sys
from collections.abc import Sequence
from decimal import Decimal
from typing import TextIO

from tabulate import tabulate

from .bcb_client import BcbClient
from .models import Comparison, ComparisonError, InputError
from .service import build_comparison, parse_date


class FriendlyArgumentParser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        self.exit(2, f"Erro de uso: {message}. Use --help para ver os argumentos.\n")


def create_parser() -> argparse.ArgumentParser:
    parser = FriendlyArgumentParser(description="Consulta uma série SGS do Banco Central do Brasil.")
    parser.add_argument("serie", help="Código numérico da série SGS")
    parser.add_argument("data_inicial", help="Data inicial no formato DD/MM/AAAA")
    parser.add_argument("data_final", help="Data final no formato DD/MM/AAAA")
    return parser


def format_decimal(value: Decimal) -> str:
    return f"{value:.2f}".replace(".", ",")


def render_comparison(comparison: Comparison) -> str:
    rows = [
        ["Série", comparison.series],
        [
            "Intervalo solicitado",
            f"{comparison.requested_start:%d/%m/%Y} a {comparison.requested_end:%d/%m/%Y}",
        ],
        ["Data do valor inicial", f"{comparison.initial.date:%d/%m/%Y}"],
        ["Valor inicial", format_decimal(comparison.initial.value)],
        ["Data do valor final", f"{comparison.final.date:%d/%m/%Y}"],
        ["Valor final", format_decimal(comparison.final.value)],
        ["Variação acumulada", f"{format_decimal(comparison.variation_percent)}%"],
    ]
    return tabulate(rows, headers=["Campo", "Resultado"], tablefmt="simple")


def run(
    argv: Sequence[str] | None = None,
    client: BcbClient | None = None,
    output: TextIO | None = None,
    error: TextIO | None = None,
) -> int:
    output = output or sys.stdout
    error = error or sys.stderr
    args = create_parser().parse_args(argv)

    try:
        if not args.serie.isdigit():
            raise InputError("Informe um código SGS composto apenas por números.")
        start = parse_date(args.data_inicial)
        end = parse_date(args.data_final)
        observations = (client or BcbClient()).fetch(args.serie, start, end)
        comparison = build_comparison(args.serie, start, end, observations)
    except ComparisonError as exception:
        print(f"Erro: {exception}", file=error)
        return 1

    print(render_comparison(comparison), file=output)
    return 0
