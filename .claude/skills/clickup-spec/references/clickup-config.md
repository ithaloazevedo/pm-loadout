# ClickUp — Configuração do Workspace (Vertical Tech)

Mapa de IDs reais do workspace para a skill `clickup-spec` e o agente `agente-delivery` agirem
sem precisar re-descobrir a estrutura. **Confirme via MCP no início de cada sessão** (IDs podem mudar
se o workspace for reconfigurado). Se um ID divergir, atualize este arquivo.

> Última verificação: 2026-07-21.

## Hierarquia

| Nível | Nome | ID |
|-------|------|----|
| Workspace | Workspace | `9006076935` |
| Space | **Vertical Tech** | `90114055709` |
| Folder | **Roadmap** | `90118093876` |
| Folder | **Discovery & Design** | `90118093877` |
| Folder | **Delivery: Experiência do jogador** | `90118093878` |
| Folder | **Delivery: Operação e afiliados** | `90118093917` |
| Folder | **Delivery: Provedora de conteúdo** | `90118093918` |

### Listas conhecidas

| Folder | Lista | ID | Uso |
|--------|-------|----|-----|
| Roadmap | **Objetivos** | `901114034994` | Marcos OKR e Resultados-chave (KRs) do ciclo |
| Roadmap | **Iniciativas** | `901114029779` | Apostas estratégicas vinculadas a um Objetivo |
| Discovery & Design | **Discovery** | `901114029780` | Pesquisa, protótipos, entrevistas, definição de escopo |
| Delivery: Experiência do jogador | **Backlog** | `901114029784` | Projetos refinados aguardando sprint — squad PAM |
| Delivery: Experiência do jogador | **Execução** | `901114029785` | WIP sprint ativa — squad PAM |
| Delivery: Operação e afiliados | **Backlog** | `901114029782` | Projetos refinados aguardando sprint — squad Backoffice |
| Delivery: Operação e afiliados | **Execução** | `901114029783` | WIP sprint ativa — squad Backoffice |
| Delivery: Provedora de conteúdo | **Backlog** | `901114029786` | Projetos refinados aguardando sprint — squad Jogos |
| Delivery: Provedora de conteúdo | **Execução** | `901114029876` | WIP sprint ativa — squad Jogos |

**Regra de Delivery:** todo Projeto de Delivery **nasce no Backlog** do folder correspondente ao Time da Iniciativa.
Migra para **Execução** ao entrar na sprint. Nunca criar listas novas nos folders. O folder correto é determinado
pelo campo **Time** da Iniciativa:
- Time = Experiência do jogador → folder Delivery: Experiência do jogador
- Time = Operação e afiliados → folder Delivery: Operação e afiliados
- Time = Provedor de jogos → folder Delivery: Provedora de conteúdo

## Status por lista

**Objetivos** (`901114034994`):
`not started` → `in progress` → `on track` → `at risk` → `off track` → `cancelled` / `complete`

**Iniciativas** (`901114029779`):
`em consideração` → `priorizado` → `em discovery` → `em delivery` → `descartado` / `finalizado`

**Discovery** (`901114029780`):
`to do` → `em progresso` → `em validação` → `pronto` → `complete`

**Backlog (todos os folders de Delivery):**
`backlog` → `em refinamento` → `pronto p/ execução` → `priorizado` → `complete` / `cancelado`

**Execução — Experiência do jogador** (`901114029785`) **e Operação e afiliados** (`901114029783`):
`to do` → `em desenvolvimento` → `bloqueada` → `em revisão técnica` → `em homologação` → `aguardando deploy` → `cancelado` / `pronto` / `finalizado`

**Execução — Provedora de conteúdo** (`901114029876`):
`nao iniciada` → `desenvolvimento` → `teste` → `refatorar` → `alpha` → `concluido` / `cancelado`

## Custom Fields — Lista Iniciativas (conjunto principal)

Use estes IDs ao setar campos via `custom_fields: [{ id, value }]` no create/update de task.

| Campo | ID | Tipo | Valores / Observação |
|-------|----|------|----------------------|
| Empresa | `75d90db5-4d63-44be-8f6e-4c9981de755b` | drop_down | Tradicional `2c64c8c0-a3b2-42e4-9599-bf9a6d9839c1` · Bravo `72d1d85b-5f88-48a6-88a6-ac820ff7f8a9` · Vertical `ea610ca6-b5ff-408a-8afc-3e53a545001f` |
| Time | `80057eda-8639-493b-a985-95c4b742c18f` | drop_down | Experiência do jogador `021d9d26-06eb-4af7-a943-3dec4142cfd6` · Operação e afiliados `5c92d689-a38f-4778-95dc-a387efcdbfe6` · Provedor de jogos `cd1e0cae-9d3c-4fb5-8799-fd68b134fcda` |
| KPIs | `1217b008-0b54-4e08-a412-ec2e2d92bfc3` | drop_down | Compliance `b839fbd5-edee-4a96-be88-5a49a7c43818` · Conversão `d303b8f7-3341-4d9c-8c1a-4d1734c9f51d` · Eficiência Operacional `62b4952f-f0f9-4afd-953c-98acd084dd74` · Receita `cf9586c2-9c19-4142-8971-79b6388feca4` · Retenção `4b35c313-285b-4d99-be1c-029504d43260` · Satisfação `a43bdf3c-6a99-4758-84ab-33cc357a0388` · Segurança `13634640-5a57-4afb-8b88-da85804b6484` |
| Horizonte | `f83d2bfd-56fb-40d8-bf0e-91cd978b3dfd` | drop_down | Now `53a9a548-87ef-4d68-8fa2-83419c626c72` · Next `2d251cc0-e963-4295-b856-d4ab6c9fbf34` · Later `fee7aa18-af6e-4569-b203-063f035c91f7` |
| Impacto | `44fc97aa-0d54-4d89-b7a1-a57e7618550b` | drop_down | 3 `2c34ca33-f605-4e1b-b253-bbc3d0fd0ec8` · 2 `5d9d464c-3973-435e-9c3a-b5d6c82de78a` · 1 `b811d0cc-1db4-403d-9f46-3e12d7b46cb4` · 0.5 `18fda8f5-50a3-4d87-b656-d80e7e11b296` · 0.25 `904129a2-70ae-413d-8a9c-fc8f3ea2eafa` |
| Alcance | `793e092e-1f45-4532-a1cb-080991d1f9ec` | number | Nº de usuários/eventos afetados por período |
| T-Shirt Sizing | `2eb0e96e-8715-453b-8a82-79a184679e82` | emoji | 1 (trivial) a 5 (múltiplos sprints) |
| Votos | `8a3388a0-cc3a-4f72-b374-38d3f8327b69` | votes | Estrelas — votação do time |
| Score | `554b5817-1c01-40e4-9d21-4dae33b2111e` | text (AI) | **Auto-calculado**: (Impacto × Votos × Alcance) / T-Shirt-Size — não setar manualmente |
| Objetivo | `70d76ca2-08fc-49b5-8baa-68eecb60aa32` | list_relationship | Vincula a Iniciativa ao seu Marco OKR na lista Objetivos |
| Iniciativa | `6c59d3f8-f22d-4b7b-93f4-b3d8b84a2cc5` | tasks | Vínculo de pertencimento: Discovery/Delivery → Iniciativa pai |
| Data de Início Prevista | `cf52c4b2-2e9a-4098-bccb-826ba13e1746` | date | — |
| Data de Conclusão Prevista | `929a07f6-8d58-4d02-a0db-19f64d7d7694` | date | — |
| Progresso | `d1b5ade4-77ba-432e-8c87-e3c26f1d30dd` | automatic_progress | Auto — não setar |
| Resumo | `faac86b5-8d69-45ae-820f-d89539c6abfd` | text (AI) | Auto-gerado — não setar |

> Campos `BASELINE_*` são do sistema (Gantt baselines) — não setar.

## Fórmula de Score (priorização)

`Score = (Impacto × Votos × Alcance) / T-Shirt-Size`

O campo **Score** é calculado automaticamente pela IA do ClickUp. Para orientar a priorização, proponha os valores de entrada:

- **Impacto** (magnitude do efeito): 3 = muito alto · 2 = alto · 1 = médio · 0.5 = baixo · 0.25 = mínimo
- **Alcance** (usuários afetados): estimativa numérica por período (ex: 12.000 usuários/mês)
- **T-Shirt Sizing** (esforço): 1 = dias · 2 = 1-2 semanas · 3 = 3-4 semanas · 4 = 1-2 meses · 5 = múltiplos ciclos
- **Votos**: votação do time (estrelas) — setar ao vivo no ClickUp; não via API

Apresente assim:
> "Score estimado ≈ [(Impacto [x]) × (Alcance [y]) × (Votos estimados [z])] / (T-Shirt [w]). Impacto [x] porque [evidência]. Alcance [y] com base em [dado]."

## Custom Fields — Espaço (herdados por todas as listas)

Campos herdados automaticamente por Discovery e Delivery:
- **Iniciativa** (`6c59d3f8`) — `tasks` type: vincula Discovery/Delivery à Iniciativa pai (mecanismo principal de pertencimento)
- **Progresso** (`d1b5ade4`) — `automatic_progress`: auto, não setar
- **BASELINE_*** — sistema Gantt, não setar

> Para Discovery e Delivery: os campos Empresa, Time, KPIs, Horizonte, Impacto, Score, Horizonte **vivem na Iniciativa**. Não tente setá-los em Discovery/Delivery — a priorização vive no item pai.

## Tipos de Tarefa por Lista

Ao criar uma task via `clickup_create_task`, **sempre selecione o tipo correto**. O tipo muda a view e os campos disponíveis.

| Folder / Lista | Tipo de Tarefa (task_type) | Quando usar |
|----------------|---------------------------|-------------|
| Objetivos | `Marco (OKR)` | Objetivo estratégico do ciclo — meta qualitativa |
| Objetivos | `Resultado-chave (KR)` | Métrica mensurável que comprova o avanço do OKR |
| Iniciativas | `Iniciativa` | Aposta estratégica de produto — contêiner de Discovery + Delivery |
| Discovery | `Pesquisa` | Pesquisa com usuários, análise de dados, benchmark |
| Discovery | `Protótipo` | Prototipação navegável no Figma para fechar decisões de UX |
| Discovery | `Entrevista` | Entrevistas estruturadas ou guerrilla com usuários |
| Delivery (qualquer folder) | `Epic` | Feature completa ou capacidade de produto (nome do tipo no workspace é em inglês: `Epic`, não `Épico`) |
| Delivery (qualquer folder) | `Débito técnico` | Refatoração, modernização sem feature nova |
| Delivery (qualquer folder) | `Bug` | Defeito em produção — causa raiz a investigar |
| Delivery (qualquer folder) | `Tarefa` | Ação pontual sem classificação mais específica (tipo padrão do workspace) |
| Delivery (qualquer folder) | `Incidente` | Falha crítica com impacto de usuário / SLA em risco |
| Delivery (qualquer folder) | `Correção` | Fix cirúrgico com causa raiz já identificada |

**Regra de inferência:**
- "pesquisar", "entender o usuário", "descobrir" → **Pesquisa**
- "prototipar", "design no Figma", "validar UX" → **Protótipo**
- "entrevistar" → **Entrevista**
- "build", "feature", "épico" → **Épico**
- "dívida técnica", "refatorar" → **Débito técnico**
- "bug", "está quebrado" → **Bug** (ou **Correção** se causa raiz identificada)
- "incidente", "down", "SLA" → **Incidente**
- Se ambíguo: pergunte entre as opções do folder correto.

## Guard-rails de Integridade — Nunca Excluir

**Exclusão é operação bloqueada por padrão.**

| Operação | Status |
|----------|--------|
| Excluir o space (`90114055709`) | 🚫 **Proibido** — irreversível |
| Excluir qualquer folder | 🚫 **Proibido** — irreversível |
| Excluir qualquer lista | 🚫 **Proibido** — ofereça arquivar ou fechar status |
| Excluir uma tarefa | ⚠️ Só com **confirmação explícita dupla** — avise irreversibilidade |

Quando o usuário pedir "apagar" ou "deletar": interrompa, informe o impacto, ofereça a alternativa
não-destrutiva (status `descartado`/`cancelado`, arquivar, comentário de encerramento).

## Convenções

- **Custom ID** das tasks: `VL-XXXXX` (gerado automaticamente). Links: `https://app.clickup.com/t/9006076935/VL-XXXXX`.
- **Vínculo entre níveis** — dois mecanismos complementares:
  - **Campo Iniciativa** (`6c59d3f8`, tipo `tasks`) — vínculo de **pertencimento**: preencher em Discovery/Delivery para apontar para a Iniciativa pai. É o mecanismo principal da Vertical Tech.
  - **Linked task** (`clickup_add_task_link`) — vínculo de **sistema**: complementar ao campo Iniciativa; mantém o relacionamento visível nas views de linked tasks.
  - **Dependência** (`clickup_add_task_dependency`) — só quando há **ordem real** (uma tarefa espera outra). Alimenta Gantt/Timeline.
  - **Subtask** (campo `parent`) — decomposição macro na mesma lista; usar com parcimônia.
- **Portfólio na Iniciativa**: ao vincular Discovery ou Delivery a uma Iniciativa, atualize a seção 🗂️ Portfólio da Iniciativa no formato `Nome (https://app.clickup.com/t/9006076935/VL-XXXXX)` — o ClickUp renderiza como task-link interativo com status e responsável ao vivo.
- **Não usamos**: *Tasks in Multiple Lists* nem o campo *Relationship*.
- **Updates**: comentário na task via `clickup_create_task_comment` (não há Activity Update nativo).
- **Conteúdo em português**; termos técnicos consolidados em inglês (Discovery, Delivery, Backlog, Sprint, OKR, KR).
