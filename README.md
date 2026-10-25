# PBL: exportação e logística da soja brasileira
## Objetivo
Organizar um fluxo reproduzível para analisar exportações brasileiras de soja em grão, relacionando dados agrícolas, câmbio, portos, fretes e cenários logísticos. O projeto deve preservar os dados originais, documentar fontes e hipóteses e gerar bases tratadas e resultados reproduzíveis.
## Situação atual
O repositório inclui leitura inicial de CSV do Comex Stat e agregação mensal de peso líquido e valor FOB. Câmbio/deflator, agricultura, lucro, comparação de cenários e alocação por portos continuam pendentes até que as fontes e convenções correspondentes sejam definidas.
## Como instalar
Requisito: Python 3.11 ou superior.
```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e .
```
Em macOS ou Linux, crie e ative o ambiente com `python3 -m venv .venv` e `source .venv/bin/activate`, depois instale o projeto com `python -m pip install -e .`.
## Como executar
Na raiz do repositório, com o ambiente virtual ativo, o comando sem subcomando prepara as pastas:
```powershell
python -m soja_pipeline
```
Para tratar um CSV do Comex Stat e gerar a base mensal por NCM e país de destino quando essa informação existir na origem:

```powershell
python -m soja_pipeline exportacoes --arquivo data/originais/exportacoes.csv --ncm 12019000
```

O resultado é salvo em `data/tratados/exportacoes_mensais.csv`. O arquivo original não é alterado. Se não houver coluna de país de destino, o programa avisa que o resultado não permite calcular concentração por destino. O código NCM informado é filtrado, mas sua vigência histórica precisa ser conferida separadamente.
## Estrutura das pastas
```text
.
├── config/                 # parâmetros de execução e caminhos
├── data/
│   ├── originais/           # arquivos de fontes preservados sem alteração
│   ├── hipoteses/           # custos, capacidades e cenários hipotéticos
│   ├── tratados/            # bases limpas e harmonizadas
│   └── resultados/          # indicadores, comparações e alocações
├── docs/                   # decisões metodológicas e dicionário de dados
├── src/
│   └── soja_pipeline/       # código do projeto
├── pyproject.toml           # configuração para instalar o pacote
├── tests/                  # verificações automatizadas a adicionar
├── .gitignore
├── README.md
└── requirements.txt
```
O comando inicial cria as pastas de configuração, documentação e dados na primeira execução. Dados originais ou tratados grandes e com restrição de redistribuição devem ficar fora do Git; registre a fonte, a consulta, a data de extração e como obtê-los.
## Dependências
As dependências estão declaradas em `pyproject.toml` e espelhadas em `requirements.txt`:
- `pandas`: leitura, transformação e validação de tabelas;
- `openpyxl`: leitura e escrita de arquivos Excel;
- `requests`: consultas HTTP a fontes que disponibilizem acesso automatizado.
As versões estão limitadas no arquivo. A lista deverá ser revisada quando o pipeline for implementado e acompanhada por travamento de versões para facilitar a reprodução entre máquinas.

## Leitura e cálculo de exportações

O módulo `soja_pipeline.dados` carrega CSV como texto, preservando códigos com zeros à esquerda e os arquivos originais. `soja_pipeline.calculos` agrega FOB e peso líquido por ano, mês e NCM, incluindo destino quando disponível, converte quilogramas em toneladas e calcula o preço FOB implícito como FOB dividido pelas toneladas.

O código ainda não calcula produtividade, câmbio/deflator, lucro, cenários ou alocação por portos. Essas etapas dependem das fontes, convenções e hipóteses pendentes abaixo. A tabela mensal é descritiva e não valida uma estratégia comercial.
## Fontes e regras pendentes
- Documentar a relação entre ano-safra e ano civil sem inferir datas ausentes.
- Definir a agregação mensal da PTAX, o mês-base do IPCA e a regra de deflação.
- Completar a movimentação mensal observada por porto e produto.
- Decidir se o modelo exige cotações mensais de frete por rota.
- Obter ou definir capacidade portuária, separando observações de hipóteses.
- Documentar rotas, componentes, moeda e método para custos hipotéticos.
Até essas decisões serem registradas, o código deverá sinalizar dados ou métodos pendentes, sem inventar valores.
