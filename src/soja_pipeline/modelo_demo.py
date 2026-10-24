"""Exemplo didatico de ajuste linear e maximizacao de lucro.

Todos os valores sao hipoteticos e servem apenas para demonstrar o metodo.
As duas partes sao exercicios separados e nao representam resultados do projeto.
"""

import numpy as np


# Ajuste linear ilustrativo: quantidade em funcao do preco.
precos_amostra = np.array([300.0, 400.0, 500.0])
matriz = np.column_stack((np.ones(precos_amostra.size), precos_amostra))

quantidade_demanda = np.array([121.0, 108.0, 101.0])
quantidade_oferta = np.array([91.0, 108.0, 131.0])

coef_demanda = np.linalg.lstsq(matriz, quantidade_demanda, rcond=None)[0]
coef_oferta = np.linalg.lstsq(matriz, quantidade_oferta, rcond=None)[0]

# Confere os coeficientes esperados para os dados do exemplo.
np.testing.assert_allclose(coef_demanda, [150.0, -0.1], atol=1e-8, rtol=0)
np.testing.assert_allclose(coef_oferta, [30.0, 0.2], atol=1e-8, rtol=0)


# Exercicio separado: lucro total com custo quadratico hipotetico.
preco_venda = 350.0
custo_variavel_unitario = 180.0
custo_fixo = 5_000_000.0
coef_custo_quadratico = 0.0006

# Derivada do lucro igual a zero: margem - 2*a*q = 0.
quantidade_otima = (preco_venda - custo_variavel_unitario) / (2 * coef_custo_quadratico)
lucro_maximo = (
    -custo_fixo
    + (preco_venda - custo_variavel_unitario) * quantidade_otima
    - coef_custo_quadratico * quantidade_otima**2
)

assert np.isclose(quantidade_otima, 141_666.6666666667, atol=1e-8, rtol=0)
assert np.isclose(lucro_maximo, 7_041_666.666667, atol=1e-3, rtol=0)

if __name__ == "__main__":
    print("Exemplo didatico: valores hipoteticos, sem interpretacao empirica.")
    print(f"Coeficientes da demanda (intercepto, inclinacao): {coef_demanda}")
    print(f"Coeficientes da oferta (intercepto, inclinacao): {coef_oferta}")
    print(f"Quantidade otima ilustrativa: {quantidade_otima:,.2f}")
    print(f"Lucro maximo ilustrativo: R$ {lucro_maximo:,.2f}")
