import numpy as np
import pandas as pd


# =====================================================================
# 1. PROCESSAMENTO DO COMEX STAT (CÁLCULO DO PREÇO IMPLÍCITO P)
# =====================================================================
def processar_comexstat(caminho_csv: str) -> pd.DataFrame:
  """Lê o CSV do Comex Stat, padroniza as colunas, converte a quantidade em KG

  para Toneladas (Q) e calcula o Preço Implícito (P = Valor FOB / Q_ton) em
  US$/t.
  """
  df = pd.read_csv(caminho_csv, sep=';')

  # Padronização de colunas
  df = df.rename(
      columns={
          'Ano': 'ano',
          'Mês': 'mes',
          'Valor FOB (US$)': 'valor_fob_usd',
          'Quilograma Líquido': 'kg_liquido',
      }
  )

  # Conversão de KG para Toneladas (Q)
  df['Q_ton'] = df['kg_liquido'] / 1000.0

  # CÁLCULO DO PREÇO IMPLÍCITO (P = Valor FOB / Q_ton)
  df['P_fob_usd_ton'] = df['valor_fob_usd'] / df['Q_ton']

  # Ordenação temporal
  df['data'] = pd.to_datetime(
      df['ano'].astype(str) + '-' + df['mes'].astype(str) + '-01'
  )
  df = df.sort_values('data').reset_index(drop=True)

  return df


# =====================================================================
# 2. DECISÃO MICROECONÔMICA VIA DERIVAÇÃO (C(q) = 5M + 180q + 0,0006q²)
# =====================================================================
def calcular_decisao_cooperativa(
    preco_fob: float, area_hectares: float = 50000.0
) -> pd.Series:
  """Otimização analítica via Derivação:

  - Receita: R(q) = P * q
  - Custo Total: C(q) = 5.000.000 + 180q + 0,0006q²
  - Custo Marginal: C'(q) = dC/dq = 180 + 0,0012q
  - Maximização do Lucro (1ª Derivada): R'(q) = C'(q) => P = 180 + 0,0012q
    => q* = (P - 180) / 0,0012
  - Condição de 2ª Ordem: L''(q) = -C''(q) = -0,0012 < 0 (Garante Ponto de Máximo)
  - Shutdown Point: min(CVMe) = US$ 180,00/t
  """
  p_shutdown = 180.0  # Preço limite (min CVMe)

  if preco_fob < p_shutdown:
    return pd.Series({
        'Status': 'PARAR PRODUÇÃO',
        'Preço de Equilíbrio FOB (US$/t)': preco_fob,
        'Quantidade Ótima q* (T)': 0.0,
        'Receita Total (US$)': 0.0,
        'Custo Total (US$)': 5000000.0,
        'Lucro Ótimo L* (US$)': -5000000.0,
        'Custo Médio (US$/t)': np.nan,
        'Produtividade (t/ha)': 0.0,
    })

  # Derivação da Quantidade Ótima q* (CPO: P = C'(q))
  q_opt = (preco_fob - 180.0) / 0.0012

  # Indicadores Financeiros no Ponto de Lucro Ótimo
  receita = preco_fob * q_opt
  custo = 5000000.0 + (180.0 * q_opt) + (0.0006 * (q_opt**2))
  lucro_otimo = receita - custo
  cme = custo / q_opt if q_opt > 0 else np.nan
  produtividade_ha = q_opt / area_hectares

  return pd.Series({
      'Status': 'OPERANDO',
      'Preço de Equilíbrio FOB (US$/t)': preco_fob,
      'Quantidade Ótima q* (T)': q_opt,
      'Receita Total (US$)': receita,
      'Custo Total (US$)': custo,
      'Lucro Ótimo L* (US$)': lucro_otimo,
      'Custo Médio (US$/t)': cme,
      'Produtividade (t/ha)': produtividade_ha,
  })


# =====================================================================
# 3. PIPELINE E GERAÇÃO DA TABELA FINAL (2015 A 2025)
# =====================================================================
def executar_pipeline_completo(
    caminho_csv_comexstat: str = None, area_hectares: float = 50000.0
) -> pd.DataFrame:
  if caminho_csv_comexstat:
    # Leitura dos dados reais se informado o CSV
    df_mensal = processar_comexstat(caminho_csv_comexstat)
    df_anual = (
        df_mensal.groupby('ano')
        .agg({'valor_fob_usd': 'sum', 'Q_ton': 'sum'})
        .reset_index()
    )
    df_anual['Preço de Equilíbrio FOB (US$/t)'] = (
        df_anual['valor_fob_usd'] / df_anual['Q_ton']
    )
  else:
    # Série temporal de Preços Históricos Implícitos (2015-2025)
    df_anual = pd.DataFrame({
        'ano': list(range(2015, 2026)),
        'Preço de Equilíbrio FOB (US$/t)': [
            395.0,
            375.0,
            380.0,
            390.0,
            350.0,
            355.0,
            460.0,
            580.0,
            520.0,
            425.0,
            400.0,
        ],
    })

  # Aplicação da otimização por derivação linha a linha
  df_decisoes = df_anual['Preço de Equilíbrio FOB (US$/t)'].apply(
      lambda p: calcular_decisao_cooperativa(p, area_hectares=area_hectares)
  )

  # Consolidação mantendo a coluna 'ano'
  df_final = pd.concat([df_anual[['ano']], df_decisoes], axis=1)
  return df_final


# Executar e exibir o DataFrame formatado na tela
df_resultado = executar_pipeline_completo(area_hectares=50000.0)
pd.options.display.float_format = '{:,.2f}'.format
print(df_resultado.to_string(index=False))