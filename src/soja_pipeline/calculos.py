"""Cálculos descritivos de exportações a partir da base do Comex Stat."""

from __future__ import annotations

import re
import unicodedata
from decimal import Decimal, InvalidOperation

import pandas as pd


_MESES = {
    "janeiro": 1,
    "fevereiro": 2,
    "marco": 3,
    "abril": 4,
    "maio": 5,
    "junho": 6,
    "julho": 7,
    "agosto": 8,
    "setembro": 9,
    "outubro": 10,
    "novembro": 11,
    "dezembro": 12,
}

_ALIAS_COLUNAS = {
    "ano": ("ano", "co_ano"),
    "mes": ("mes", "co_mes"),
    "codigo_ncm": ("codigo_ncm", "ncm", "co_ncm"),
    "valor_fob_usd": ("valor_us_fob", "valor_fob_us", "valor_fob_usd", "vl_fob"),
    "quilograma_liquido": ("quilograma_liquido", "kg_liquido", "peso_liquido"),
    "pais_destino": ("pais", "pais_de_destino", "pais_destino", "co_pais"),
}


def _normalizar_rotulo(valor: str) -> str:
    texto = unicodedata.normalize("NFKD", valor)
    texto = "".join(caractere for caractere in texto if not unicodedata.combining(caractere))
    texto = re.sub(r"[^a-zA-Z0-9]+", "_", texto.casefold()).strip("_")
    return texto


def _mapear_colunas(tabela: pd.DataFrame) -> dict[str, str]:
    rotulos = {_normalizar_rotulo(str(coluna)): str(coluna) for coluna in tabela.columns}
    mapeadas: dict[str, str] = {}
    obrigatorias = ("ano", "mes", "codigo_ncm", "valor_fob_usd", "quilograma_liquido")
    for nome_canonico, aliases in _ALIAS_COLUNAS.items():
        encontrada = next((rotulos[alias] for alias in aliases if alias in rotulos), None)
        if encontrada:
            mapeadas[nome_canonico] = encontrada
        elif nome_canonico in obrigatorias:
            raise ValueError(
                f"Coluna necessária não encontrada: {nome_canonico}. "
                f"Cabeçalhos recebidos: {list(tabela.columns)}"
            )
    return mapeadas


def _mes_para_numero(valor: object) -> int:
    texto = str(valor).strip().casefold()
    numero = re.match(r"^(\d{1,2})(?:\D|$)", texto)
    if numero:
        mes = int(numero.group(1))
    else:
        sem_acentos = _normalizar_rotulo(texto)
        mes = next((n for nome, n in _MESES.items() if nome in sem_acentos), 0)
    if not 1 <= mes <= 12:
        raise ValueError(f"Mês inválido no arquivo: {valor!r}")
    return mes


def _numero_para_decimal(valor: object) -> Decimal:
    texto = str(valor).strip().replace("US$", "").replace("$", "").replace(" ", "")
    if not texto:
        raise ValueError("Foi encontrado um valor numérico vazio.")
    if "," in texto and "." in texto:
        # O último separador é tratado como decimal; o outro, como milhar.
        decimal = "," if texto.rfind(",") > texto.rfind(".") else "."
        milhares = "." if decimal == "," else ","
        texto = texto.replace(milhares, "").replace(decimal, ".")
    elif "," in texto:
        texto = texto.replace(".", "").replace(",", ".")
    try:
        return Decimal(texto)
    except InvalidOperation as erro:
        raise ValueError(f"Valor numérico inválido: {valor!r}") from erro


def calcular_exportacoes_mensais(
    tabela: pd.DataFrame,
    *,
    codigo_ncm: str | None = None,
) -> pd.DataFrame:
    """Agrupa FOB e peso líquido por mês, NCM e destino quando disponível.

    O cálculo gera toneladas a partir de quilogramas líquidos e preço FOB
    implícito (FOB dividido pelas toneladas). Não atribui destino ausente nem
    valida a vigência histórica do código NCM; essas etapas exigem fonte e
    regra de classificação documentadas.
    """
    colunas = _mapear_colunas(tabela)
    dados = pd.DataFrame(index=tabela.index)
    dados["ano"] = pd.to_numeric(tabela[colunas["ano"]].str.strip(), errors="coerce")
    dados["mes"] = tabela[colunas["mes"]].map(_mes_para_numero)
    dados["codigo_ncm"] = tabela[colunas["codigo_ncm"]].astype("string").str.strip()
    dados["fob_usd"] = tabela[colunas["valor_fob_usd"]].map(_numero_para_decimal).astype(float)
    dados["quilograma_liquido"] = tabela[colunas["quilograma_liquido"]].map(_numero_para_decimal).astype(float)

    if "pais_destino" in colunas:
        dados["pais_destino"] = tabela[colunas["pais_destino"]].astype("string").str.strip()

    invalidos = dados["ano"].isna() | (dados["ano"] % 1 != 0)
    if invalidos.any():
        linhas = (invalidos.to_numpy().nonzero()[0] + 2).tolist()
        raise ValueError(f"Ano inválido nas linhas do CSV: {linhas[:10]}")
    dados["ano"] = dados["ano"].astype("int64")

    if dados["codigo_ncm"].eq("").any():
        raise ValueError("Há linhas sem código NCM.")
    if (dados["fob_usd"] < 0).any() or (dados["quilograma_liquido"] < 0).any():
        raise ValueError("FOB e peso líquido não podem ser negativos.")

    if codigo_ncm is not None:
        ncm = str(codigo_ncm).strip()
        dados = dados.loc[dados["codigo_ncm"] == ncm].copy()
        if dados.empty:
            raise ValueError(f"Nenhum registro encontrado para o NCM {ncm}.")

    dimensoes = ["ano", "mes", "codigo_ncm"]
    if "pais_destino" in dados.columns:
        dimensoes.append("pais_destino")

    resultado = (
        dados.groupby(dimensoes, as_index=False, dropna=False)
        .agg(fob_usd=("fob_usd", "sum"), quilograma_liquido=("quilograma_liquido", "sum"))
    )
    resultado["ano_mes"] = (
        resultado["ano"].astype(str) + "-" + resultado["mes"].astype(str).str.zfill(2)
    )
    resultado["quantidade_t"] = resultado["quilograma_liquido"] / 1000
    resultado["preco_implicito_usd_t"] = resultado["fob_usd"].div(
        resultado["quantidade_t"].where(resultado["quantidade_t"] > 0)
    )

    ordem = ["ano_mes", "ano", "mes", "codigo_ncm"]
    if "pais_destino" in resultado.columns:
        ordem.append("pais_destino")
    ordem.extend(["quantidade_t", "fob_usd", "preco_implicito_usd_t"])
    return resultado[ordem].sort_values(ordem[: len(dimensoes) + 1]).reset_index(drop=True)
