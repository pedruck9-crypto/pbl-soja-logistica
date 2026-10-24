# PBL: exportação e logística da soja brasileira

## Objetivo

Organizar um fluxo reproduzível para analisar exportações brasileiras de soja em grão, relacionando dados agrícolas, câmbio, portos, fretes e cenários logísticos. O projeto deve preservar os dados originais, documentar fontes e hipóteses e gerar bases tratadas e resultados que outra pessoa consiga reproduzir.

## Situação atual

Este repositório contém a estrutura inicial e um comando de verificação. A importação, o tratamento, os cálculos dos indicadores, a comparação de cenários e a alocação por portos ainda serão implementados. Nenhum resultado é calculado por este esqueleto.

## Como instalar

Requisito: Python 3.11 ou superior.

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Em macOS ou Linux, ative o ambiente com `source .venv/bin/activate`.

## Como executar

Na raiz do repositório:

```powershell
python -m soja_pipeline
```

Por enquanto, o comando verifica a estrutura de pastas e informa que o pipeline analítico ainda precisa ser implementado. As etapas de importação e cálculo serão adicionadas depois que as regras e fontes pendentes forem definidas.

## Estrutura das pastas

```text
.
├── config/                 # parâmetros de execução e caminhos
├── data/
│   ├── originais/           # arquivos baixados das fontes, preservados sem alteração
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

Os dados originais e tratados não devem ser sobrescritos pelo pipeline. Arquivos grandes ou com restrições de redistribuição devem permanecer fora do Git; registrar no projeto a fonte, a consulta, a data de extração e as instruções para obtê-los.

## Dependências

As dependências iniciais estão em `requirements.txt`:

- `pandas`: leitura, transformação e validação de tabelas;
- `openpyxl`: leitura e escrita de arquivos Excel;
- `requests`: consultas HTTP a fontes que disponibilizem acesso automatizado.

As versões estão limitadas no arquivo de dependências. A lista deverá ser revisada quando o pipeline for implementado e acompanhada por um arquivo de travamento de versões para reprodução entre máquinas.

## Fontes e regras pendentes

- Documentar a ponte entre ano-safra e ano civil sem inferir datas ausentes.
- Definir agregação mensal da PTAX, mês-base do IPCA e regra de deflação.
- Completar movimentação mensal observada por porto e produto.
- Decidir se o modelo exige cotações mensais de frete por rota.
- Obter ou definir capacidade portuária, separando valores observados de hipóteses.
- Documentar rotas, componentes, moeda e método para custos hipotéticos.

Até essas decisões serem registradas, o código deverá sinalizar os dados ou métodos pendentes em vez de inventar valores.
