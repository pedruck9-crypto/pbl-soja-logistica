# PBL: exportação e logística da soja brasileira
## Objetivo
Organizar um fluxo reproduzível para analisar exportações brasileiras de soja em grão, relacionando dados agrícolas, câmbio, portos, fretes e cenários logísticos. O projeto deve preservar os dados originais, documentar fontes e hipóteses e gerar bases tratadas e resultados reproduzíveis.
## Situação atual
O repositório contém a documentação inicial, dependências e um comando que prepara as pastas previstas. A importação, o tratamento, os indicadores, a comparação de cenários e a alocação por portos ainda serão implementados. O comando inicial não calcula resultados.
## Como instalar
Requisito: Python 3.11 ou superior.
```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
$env:PYTHONPATH = "src"
```
Em macOS ou Linux, crie e ative o ambiente com `python3 -m venv .venv` e `source .venv/bin/activate`. Instale as dependências com `python -m pip install -r requirements.txt` e configure `PYTHONPATH=src` antes de executar.
## Como executar
Na raiz do repositório, com o ambiente virtual ativo:
```powershell
python -m soja_pipeline
```
Em macOS ou Linux, use `PYTHONPATH=src python -m soja_pipeline`. O comando prepara as pastas de dados e informa que o pipeline analítico ainda será implementado.
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
├── tests/                  # verificações automatizadas a adicionar
├── .gitignore
├── README.md
└── requirements.txt
```
O comando inicial cria as pastas de configuração, documentação e dados na primeira execução. Dados originais ou tratados grandes e com restrição de redistribuição devem ficar fora do Git; registre a fonte, a consulta, a data de extração e como obtê-los.
## Dependências
As dependências iniciais estão em `requirements.txt`:
- `pandas`: leitura, transformação e validação de tabelas;
- `openpyxl`: leitura e escrita de arquivos Excel;
- `requests`: consultas HTTP a fontes que disponibilizem acesso automatizado.
As versões estão limitadas no arquivo. A lista deverá ser revisada quando o pipeline for implementado e acompanhada por travamento de versões para facilitar a reprodução entre máquinas.
## Fontes e regras pendentes
- Documentar a relação entre ano-safra e ano civil sem inferir datas ausentes.
- Definir a agregação mensal da PTAX, o mês-base do IPCA e a regra de deflação.
- Completar a movimentação mensal observada por porto e produto.
- Decidir se o modelo exige cotações mensais de frete por rota.
- Obter ou definir capacidade portuária, separando observações de hipóteses.
- Documentar rotas, componentes, moeda e método para custos hipotéticos.
Até essas decisões serem registradas, o código deverá sinalizar dados ou métodos pendentes, sem inventar valores.
