# Soja em Fluxo

Projeto acadêmico de dados e logística para analisar exportações brasileiras de soja em grão, organizar fontes heterogêneas e preparar comparações de cenários, rentabilidade e alocação portuária.

[Acessar o site publicado](https://pbl-soja-logistica-frontend.vercel.app/) · [Ver resultados e metodologia](https://pbl-soja-logistica-frontend.vercel.app/resultados-metodologia.html) · [Abrir o relatório para portfólio](frontend/assets/documentos/Relatorio_Portfolio_Soja_em_Fluxo.pdf) · [Ler o resumo do PBL](docs/RESUMO_PBL.md)

## Visão rápida

| Aspecto | Descrição |
|---|---|
| Problema | Organizar dados de exportação, agricultura, câmbio e logística para estudar diversificação de destinos e portos |
| Minha atuação | Sistema reproduzível em Python, dashboard, integração do site, documentação e publicação web |
| Tecnologias | Python, Pandas, HTML, CSS, JavaScript, GitHub e Vercel |
| Entrega atual | Site navegável, pacote Python instalável, leitura de CSV e agregação mensal inicial do Comex Stat |
| Estado | Protótipo acadêmico em evolução; resultados finais ainda dependem da validação de fontes e modelos |

## O que este projeto demonstra

- organização de um pipeline de dados com separação entre originais, hipóteses, bases tratadas e resultados;
- tratamento de tabelas com Pandas, preservando códigos e unidades;
- conversão de peso líquido para toneladas e cálculo do preço FOB implícito;
- documentação de fontes, premissas, limitações e campos de ligação;
- construção de uma interface responsiva para comunicar metodologia e resultados;
- trabalho em equipe com Jira, branches, commits e pull requests;
- publicação contínua do front-end pela Vercel.

## Minha contribuição — Pedro Lucas Rolim

Conforme a divisão de trabalho registrada no Jira, assumi duas frentes principais.

### Sistema reproduzível em código — EBDPDDDMPN-7

- organização do repositório e preparação do ambiente Python;
- estrutura do pacote `soja_pipeline`;
- leitura das bases tabulares e transformações iniciais;
- integração progressiva entre dados, cálculos e saídas;
- documentação para reprodução do projeto.

As etapas de organização e ambiente constam como concluídas. Qualidade de dados, integração completa e verificação integral da reprodução continuam em desenvolvimento.

### Dashboard de resultados — EBDPDDDMPN-12

- planejamento da visualização e arquitetura das páginas;
- desenvolvimento do front-end responsivo;
- integração das áreas de metodologia, resultados, documentos e créditos;
- diferenciação visual entre resultados preliminares, hipóteses e pendências;
- publicação do site e organização da versão para portfólio.

A conexão com os resultados finais depende da validação dos modelos e das bases produzidas pelas demais frentes da equipe.

## Arquitetura

```text
Fontes públicas
      ↓
data/originais
      ↓  leitura e validação
src/soja_pipeline
      ↓  transformações e cálculos
data/tratados → data/resultados
      ↓
frontend → publicação na Vercel
```

O fluxo preserva os arquivos originais e mantém hipóteses separadas dos dados observados. Essa decisão reduz o risco de apresentar capacidade, custos ou cenários fictícios como informação oficial.

## Situação das entregas

| Entrega | Situação |
|---|---|
| Estrutura do repositório e ambiente Python | Disponível |
| Leitura de CSV do Comex Stat | Disponível |
| Agregação mensal de peso líquido e FOB | Disponível |
| Site, metodologia e catálogo de documentos | Disponível |
| Agricultura e relação ano-safra/ano civil | Pendente de convenção final |
| Câmbio, deflator e valores constantes | Pendente de implementação |
| Cenários, lucro e HHI validados | Pendente de modelos finais |
| Capacidade, custos e alocação por portos | Pendente de dados e validação |

As tabelas e demonstrações preliminares não constituem recomendação comercial nem representam uma cooperativa real.

## Como executar

### Requisitos

- Python 3.11 ou superior;
- Git, caso o projeto seja clonado pelo repositório.

### Instalação no Windows

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e .
```

Em macOS ou Linux, use `python3 -m venv .venv`, ative com `source .venv/bin/activate` e execute `python -m pip install -e .`.

### Preparar a estrutura de dados

```powershell
python -m soja_pipeline
```

### Tratar exportações

```powershell
python -m soja_pipeline exportacoes --arquivo data/originais/exportacoes.csv --ncm 12019000
```

O comando gera `data/tratados/exportacoes_mensais.csv` sem modificar o arquivo original. Quando o país de destino não existe na fonte, o programa sinaliza que a base não permite calcular concentração por destino.

## Estrutura principal

```text
.
├── config/                  # parâmetros e caminhos
├── data/
│   ├── originais/          # arquivos preservados
│   ├── hipoteses/          # custos, capacidades e cenários
│   ├── tratados/           # bases limpas e harmonizadas
│   └── resultados/         # indicadores e comparações
├── docs/                    # metodologia e decisões
├── frontend/                # site e materiais autorizados
├── src/soja_pipeline/       # pipeline Python
├── CONTRIBUTING.md          # regras para colaboração
├── LICENSE                  # licença do código
├── pyproject.toml           # pacote e dependências
└── requirements.txt
```

## Tecnologias e dependências

- **Python e Pandas:** leitura, transformação e agregação de tabelas;
- **OpenPyXL:** leitura e escrita de planilhas Excel;
- **Requests:** acesso a fontes que ofereçam consulta automatizada;
- **HTML, CSS e JavaScript:** interface e visualização do projeto;
- **GitHub:** versionamento, revisão e colaboração;
- **Vercel:** hospedagem do front-end.

As dependências Python estão declaradas em `pyproject.toml` e `requirements.txt`.

## Decisões ainda pendentes

- documentar a relação definitiva entre ano-safra e ano civil;
- definir a agregação mensal da PTAX, o mês-base do IPCA e a regra de deflação;
- completar a movimentação mensal observada por porto e produto;
- definir a granularidade dos fretes e a composição dos custos por rota;
- separar capacidade portuária observada de capacidade hipotética;
- executar e verificar os cenários, o lucro, o HHI e a alocação portuária.

Até essas decisões serem registradas, o projeto deve sinalizar informações pendentes sem inventar valores.

## Equipe

- **Pedro Lucas Rolim:** sistema reproduzível, dashboard e integração do site;
- **Caio Rafael Tavares da Silva:** indicadores de produtividade e documentação metodológica;
- **José Guilherme Paes Rodrigues:** modelos matemáticos de oferta e demanda;
- **João Guilherme:** distribuição logística e alocação portuária;
- **Luís Felipe:** pitch de dez minutos;
- **Caio Henrique:** apoio transversal como coringa da equipe.

O [catálogo de documentos](frontend/assets/documentos/README.md) identifica as fontes e as frentes técnicas responsáveis pelos materiais incluídos.

## Contribuições

Correções e melhorias futuras são bem-vindas. Consulte o [guia de contribuição](CONTRIBUTING.md) antes de enviar código, dados ou documentos.

## Licença e materiais

O código-fonte original está disponível sob a [Licença MIT](LICENSE), mediante concordância dos respectivos autores.

A licença não abrange automaticamente marcas, logotipos, o enunciado original do PBL, documentos acadêmicos, dados ou contribuições de terceiros. Esses materiais permanecem sujeitos aos direitos e termos de suas fontes.

Consulte o [aviso de autoria, licença e materiais](NOTICE.md) para conhecer as condições aplicáveis ao código, aos textos do site, aos documentos acadêmicos, aos dados públicos e às marcas citadas no projeto.
