"""Comando de linha de comando do pipeline do PBL da soja."""

import argparse
from pathlib import Path

from soja_pipeline.calculos import calcular_exportacoes_mensais
from soja_pipeline.dados import ler_csv


def _exportacoes(raiz: Path, args: argparse.Namespace) -> int:
    origem = args.arquivo if args.arquivo.is_absolute() else raiz / args.arquivo
    saida = args.saida if args.saida.is_absolute() else raiz / args.saida
    base = ler_csv(origem, separador=args.separador)
    resultado = calcular_exportacoes_mensais(base, codigo_ncm=args.ncm)

    saida.parent.mkdir(parents=True, exist_ok=True)
    resultado.to_csv(saida, sep=";", index=False, encoding="utf-8-sig", decimal=",")
    print(f"Arquivo tratado salvo em: {saida}")
    if "pais_destino" not in resultado.columns:
        print(
            "Aviso: a fonte não contém país de destino. O resultado é agregado "
            "por mês e NCM e não permite calcular concentração por destino."
        )
    print(f"Linhas agregadas: {len(resultado)}")
    return 0


def main() -> int:
    root = Path(__file__).resolve().parents[2]
    parser = argparse.ArgumentParser(
        prog="soja_pipeline",
        description="Tratamento reproduzível de dados do PBL da soja.",
    )
    subcommands = parser.add_subparsers(dest="command")
    exports = subcommands.add_parser(
        "exportacoes", help="agrega exportações mensais por NCM e destino disponível"
    )
    exports.add_argument("--arquivo", type=Path, required=True, help="CSV original de entrada")
    exports.add_argument(
        "--saida",
        type=Path,
        default=Path("data/tratados/exportacoes_mensais.csv"),
        help="CSV tratado de saída",
    )
    exports.add_argument("--ncm", help="filtra por um código NCM exato")
    exports.add_argument("--separador", help="separador do CSV; por padrão, é inferido")

    args = parser.parse_args()
    if args.command == "exportacoes":
        try:
            return _exportacoes(root, args)
        except (OSError, ValueError) as error:
            parser.error(str(error))

    folders = (
        "data/originais",
        "data/hipoteses",
        "data/tratados",
        "data/resultados",
        "config",
        "docs",
    )
    for name in folders:
        (root / name).mkdir(parents=True, exist_ok=True)
    print("Estrutura do projeto verificada e pastas preparadas.")
    print("Para tratar exportações, use: soja_pipeline exportacoes --help")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
