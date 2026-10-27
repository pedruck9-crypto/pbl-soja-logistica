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

## Resumo do PBL

Para a versão pública de portfólio, o repositório utiliza um [resumo autoral do problema](docs/RESUMO_PBL.md). O enunciado institucional original não é redistribuído neste projeto.

## Créditos

Projeto acadêmico desenvolvido em equipe:

- Pedro Lucas Rolim — sistema reproduzível, dashboard e integração do site;
- Caio Rafael Tavares da Silva — indicadores de produtividade e documentação metodológica;
- José Guilherme Paes Rodrigues — modelos matemáticos de oferta e demanda;
- João Guilherme — distribuição logística e alocação portuária;
- Luís Felipe — pitch de dez minutos;
- Caio Henrique — apoio transversal como coringa da equipe.

### Contribuição de Pedro Lucas Rolim

Conforme a divisão de trabalho registrada no Jira, Pedro assumiu duas frentes principais:

- **EBDPDDDMPN-7 — Sistema reproduzível em código:** organização do repositório, preparação do ambiente, estrutura do pacote Python, leitura das bases e evolução do pipeline de transformações. As etapas de organização do projeto e preparação do ambiente constam como concluídas; transformações, qualidade de dados, integração progressiva e verificação integral da reprodução continuam em desenvolvimento.
- **EBDPDDDMPN-12 — Dashboard de resultados:** definição dos indicadores, planejamento das visualizações, implementação do front-end e integração das páginas de metodologia, resultados, documentos e créditos. A conexão com resultados finais depende da validação dos modelos e das bases da equipe.

Entre as entregas verificáveis no repositório estão o site estático publicado, a estrutura instalável em Python, os módulos iniciais de dados e cálculos, o catálogo de documentos e as interfaces que distinguem resultados preliminares, hipóteses e pendências.

O catálogo de documentos registra as [fontes e frentes técnicas responsáveis](frontend/assets/documentos/README.md).

## Licença e uso dos materiais

O código-fonte original deste repositório é disponibilizado sob a [Licença MIT](LICENSE), mediante concordância dos respectivos autores.

A licença MIT não abrange:

- nomes, marcas, logotipos ou identidade visual de instituições;
- o enunciado original do PBL ou materiais fornecidos pela instituição e pela professora;
- PDFs, apresentações e demais documentos acadêmicos, salvo indicação expressa;
- dados públicos ou privados, que permanecem sujeitos aos termos das fontes originais;
- contribuições de terceiros que possuam licença ou autorização própria.

O projeto é uma produção acadêmica independente e não constitui página oficial, recomendação comercial ou representação institucional. Para reutilizar materiais excluídos da MIT, consulte o respectivo titular dos direitos.
