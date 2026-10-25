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
# 2. DECISÃO MICROECONÔMICA DA COOPERATIVA (C(q) = 5M + 180q + 0,0006q²)
# =====================================================================
def calcular_decisao_cooperativa(preco_fob: float) -> pd.Series:
  """Aplica as equações microeconômicas de otimização de lucro:

  - Custo Marginal: C'(q) = 180 + 0,0012q - Condição de Ótimo: R'(q) = C'(q) =>
  P = 180 + 0,0012q => q* = (P - 180) / 0,0012 - Shutdown Point: P = min(CVMe) =
  US$ 180,00/t
  """
  p_shutdown = 180.0  # Preço limite abaixo do qual paralisa a produção

  if preco_fob < p_shutdown:
    return pd.Series({
        'Status': 'PARAR PRODUÇÃO',
        'Quantidade ótima de produção (T)': 0.0,
        'Receita (US$)': 0.0,
        'Custo (US$)': 5000000.0,
        'Lucro (US$)': -5000000.0,
        'Custo Médio (US$/t)': np.nan,
    })

  # Cálculo da Quantidade Ótima q* e Indicadores Financeiros
  q_opt = (preco_fob - 180.0) / 0.0012
  receita = preco_fob * q_opt
  custo = 5000000.0 + 180.0 * q_opt + 0.0006 * (q_opt**2)
  lucro = receita - custo
  cme = custo / q_opt

  return pd.Series({
      'Status': 'OPERANDO',
      'Quantidade ótima de produção (T)': q_opt,
      'Receita (US$)': receita,
      'Custo (US$)': custo,
      'Lucro (US$)': lucro,
      'Custo Médio (US$/t)': cme,
  })


# =====================================================================
# 3. PIPELINE AUTOMÁTICO PARA A LISTA COMPLETA DE ANOS (2015 A 2025)
# =====================================================================
def executar_pipeline_completo(caminho_csv_comexstat: str = None) -> pd.DataFrame:
  if caminho_csv_comexstat:
    # Caso tenha o CSV do Comex Stat salvo localmente
    df_mensal = processar_comexstat(caminho_csv_comexstat)
    df_anual = (
        df_mensal.groupby('ano')
        .agg({'valor_fob_usd': 'sum', 'Q_ton': 'sum'})
        .reset_index()
    )
    df_anual['P_fob_usd_ton'] = df_anual['valor_fob_usd'] / df_anual['Q_ton']
  else:
    # LISTA COMPLETA DOS ANOS (2015-2025) com Preços Históricos do Comex Stat
    df_anual = pd.DataFrame({
        'ano': list(range(2015, 2026)),
        'Preço implícito (US$/T)': [
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

  # Aplicação da decisão da cooperativa para TODOS OS ANOS da lista
  df_decisoes = df_anual['Preço implícito (US$/T)'].apply(calcular_decisao_cooperativa)

  # Consolidação dos dados
  df_final = pd.concat([df_anual, df_decisoes], axis=1)
  return df_final


# Executar e exibir o DataFrame formatado
df_resultado = executar_pipeline_completo()
pd.options.display.float_format = '{:,.2f}'.format
print(df_resultado.to_string(index=False))