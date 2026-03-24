# Engenharia de Software 2 - Explorando Evolução de Código
## Aluno: Filipe Mauro da Terra Caldeira

# Repositório selecionado (LangChain): https://github.com/langchain-ai/langchain

# Gráfico selecionado: Production and Test Files
<img width="705" height="364" alt="image" src="https://github.com/user-attachments/assets/2cfd7730-9d5f-458d-8651-dcee2fbbf7e5" />
<br>
<img width="699" height="359" alt="image" src="https://github.com/user-attachments/assets/9bdcdcfe-2e17-4f5d-a0db-9b53775b1c00" />

# Explicação:

Transição arquitetural do framework LangChain 

Lançado em 2022, o LangChain tem o intuito de deixar os modelos de linguagem (LLMs) mais versáteis e eficientes. Para isso, as principais evoluções foram:

- Memória: Criou um fluxo inteligente para a IA lembrar do histórico da conversa, gerando respostas com muito mais contexto
- Agentes e Ferramentas: Conectou as LLMs com o mundo externo, permitindo buscas na internet, leitura de arquivos e uso de outras ferramentas
- Raciocínio: Deu à IA um roteiro "passo a passo" lógico e consistente para ela estruturar melhor suas respostas

Com o boom das IAs, o framework cresceu numa velocidade muito grande, "inchando" até bater ~570.000 linhas de código (LOC) e ~3.200 arquivos. Porém, ao olhar os dados de 2025, vemos uma queda brusca: o projeto despencou para ~318.000 LOC e ~1.900 arquivos. É uma diferença gigante. Como quase metade do código simplesmente sumiu? E por quê?

Para não ficar apenas nos achismos visuais do gráfico, fiz uma análise de dados extraindo todos os Pull Requests (PRs) do GitHub a partir de 2025 (código da análise em anexo) para descobrir o que aconteceu nos bastidores dessa mudança.
## 📊 Resultados da Análise Arquitetural (A partir de 2025)

Para entender a queda brusca no volume de código do LangChain, analisamos os Pull Requests (PRs) do repositório. Os dados comprovam um forte movimento de modularização e limpeza do monolito.

### Top 10 Tags que Mais Removeram Código

A tabela abaixo evidencia o esforço de separação de responsabilidades. Note que as maiores deleções ocorreram em dependências e integrações, enquanto o núcleo (`core`) foi a única categoria com saldo positivo.

| Tag | Total de PRs | Deleções | Adições | Saldo |
| :--- | :---: | :---: | :---: | :---: |
| `dependencies` | 358 | -100.713 | +68.621 | -32.092 |
| `integration` | 355 | -91.095 | +66.067 | -25.028 |
| `langchain` | 271 | -90.867 | +87.828 | -3.039 |
| `documentation` | 98 | -87.672 | +61.891 | -25.781 |
| `infra` | 321 | -78.029 | +47.796 | -30.233 |
| `core` | 283 | -73.008 | +73.868 | +860 |
| `github_actions` | 98 | -51.936 | +21.241 | -30.695 |
| `cli` | 18 | -47.731 | +8.419 | -39.312 |
| `standard-tests` | 81 | -45.172 | +21.827 | -23.345 |
| `text-splitters` | 65 | -44.561 | +17.918 | -26.643 |

---

### Top 5 PRs com Maior Deleção Absoluta

Estes foram os principais eventos que impulsionaram a reestruturação e "enxugaram" o repositório principal:

* **[fix(docs): redirects](https://github.com/langchain-ai/langchain/pull/33734)**
  * **Data:** 29/10/2025
  * **Impacto:** -28.819 linhas
  * **Tags:** `documentation`

* **[chore(docs): v0.3 redirects](https://github.com/langchain-ai/langchain/pull/33553)**
  * **Data:** 17/10/2025
  * **Impacto:** -27.177 linhas
  * **Tags:** `documentation`, `integration`, `core`, `langchain`, `standard-tests`, `infra`, `text-splitters`, `dependencies`, `github_actions`, `cli`

* **[feat(model-profiles): distribute data across packages](https://github.com/langchain-ai/langchain/pull/34024)**
  * **Data:** 21/11/2025
  * **Impacto:** -15.713 linhas
  * **Tags:** `documentation`, `integration`, `core`, `langchain`, `dependencies`, `feature`, `model-profiles`, `anthropic`, `deepseek`, `fireworks`

* **[chore: delete CLI](https://github.com/langchain-ai/langchain/pull/34855)**
  * **Data:** 23/01/2026
  * **Impacto:** -14.635 linhas
  * **Tags:** `infra`, `dependencies`, `github_actions`, `cli`

* **[chore: move `ToolNode` improvements back to langgraph](https://github.com/langchain-ai/langchain/pull/33634)**
  * **Data:** 29/10/2025
  * **Impacto:** -6.081 linhas
  * **Tags:** `integration`, `langchain`, `infra`, `dependencies`, `v1`

O que os dados acima revelam uma estratégia agressiva de modularização e maturidade arquitetural. O LangChain atingiu um ponto de inflexão onde o modelo de "monolito" — contendo todas as integrações possíveis no mesmo repositório — tornou-se insustentável para a manutenção e evolução da ferramenta.

Analisando as tags com maior volume de remoção, fica evidente o movimento de segregação de responsabilidades. As categorias dependencies, integration e infra acumulam os maiores saldos negativos absolutos, evidenciando que o "peso" do framework estava nas conexões diretas com ferramentas e bancos de dados de terceiros. Em contrapartida, a tag core apresenta um saldo positivo (adição de 860 linhas), o que corrobora a tese de que o núcleo essencial de raciocínio e roteamento do framework foi preservado e expandido, enquanto os elementos periféricos foram extraídos.

Os Pull Requests com as maiores deleções confirmam essa fragmentação cirúrgica na prática. O PR 34024 (feat(model-profiles): distribute data across packages), responsável por remover mais de 15.000 linhas, ilustra a extração de integrações de provedores específicos (como Anthropic, DeepSeek e Fireworks) para pacotes satélites independentes.

Da mesma forma, funcionalidades e ferramentas adjacentes que antes inchavam o repositório principal foram realocadas. Isso é evidenciado pela remoção completa da interface de linha de comando com o PR 34855 (chore: delete CLI) e pela migração de componentes especializados de agentes para projetos paralelos, como visto no PR 33634 (chore: move ToolNode improvements back to langgraph).

Por fim, uma parcela muito significativa dessa "limpeza" concentrou-se na infraestrutura de documentação. PRs massivos de redirecionamento e organização de versões anteriores (como a v0.3) removeram mais de 55.000 linhas de texto e metadados obsoletos.
A evolução do LangChain documentada a partir de 2025 reflete a transição de um repositório centralizado de hiper-crescimento para um ecossistema distribuído de alta coesão e baixo acoplamento. O código não desapareceu; ele foi reorganizado em bibliotecas menores e independentes, facilitando a governança, otimizando a esteira de testes e garantindo a escalabilidade do núcleo principal.
