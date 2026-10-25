"""Leitura conservadora de arquivos CSV para as etapas do pipeline."""

from pathlib import Path

import pandas as pd


def ler_csv(
    caminho: str | Path,
    *,
    separador: str | None = None,
    encoding: str = "utf-8-sig",
    colunas_obrigatorias: tuple[str, ...] = (),
) -> pd.DataFrame:
    """Carrega um CSV como texto, sem alterar o arquivo de origem.

    Se ``separador`` não for informado, o Pandas tenta inferi-lo. Os valores
    ficam como texto nesta etapa para preservar códigos, zeros à esquerda e
    a representação original dos números; conversões e validações de domínio
    devem ocorrer em etapas posteriores do pipeline.
    """
    arquivo = Path(caminho)
    if not arquivo.is_file():
        raise FileNotFoundError(f"Arquivo CSV não encontrado: {arquivo}")

    opcoes: dict[str, object] = {
        "encoding": encoding,
        "dtype": "string",
        "keep_default_na": False,
        "on_bad_lines": "error",
    }
    if separador is None:
        opcoes.update(sep=None, engine="python")
    else:
        opcoes["sep"] = separador

    try:
        tabela = pd.read_csv(arquivo, **opcoes)
    except pd.errors.EmptyDataError as erro:
        raise ValueError(f"O arquivo CSV está vazio: {arquivo}") from erro

    if tabela.empty and len(tabela.columns) == 0:
        raise ValueError(f"O arquivo CSV não contém cabeçalho nem registros: {arquivo}")

    repetidas = tabela.columns[tabela.columns.duplicated()].tolist()
    if repetidas:
        raise ValueError(f"O CSV contém nomes de coluna repetidos: {repetidas}")

    ausentes = sorted(set(colunas_obrigatorias) - set(tabela.columns))
    if ausentes:
        raise ValueError(f"Colunas obrigatórias ausentes em {arquivo.name}: {ausentes}")

    return tabela
