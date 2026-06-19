# ClickUp — Configuração do Workspace (Vertical Loto)

Mapa de IDs reais do workspace para a skill `clickup-spec` e o agente `gerenciador-do-clickup` agirem
sem precisar re-descobrir a estrutura. **Confirme via MCP no início de cada sessão** (IDs podem mudar
se o workspace for reconfigurado). Se um ID divergir, atualize este arquivo.

> Última verificação: 2026-06-19.

## Hierarquia

| Nível | Nome | ID |
|-------|------|----|
| Workspace | Workspace | `9006076935` |
| Space | Vertical Loto | `90113593199` |
| Folder | **Product Roadmap** | `90118030606` |
| Folder | **Product Discovery** | `90118027675` |
| Folder | **Product Delivery** | `90118047591` |

### Listas conhecidas

| Folder | Lista | ID | Uso |
|--------|-------|----|-----|
| Product Roadmap | Product Roadmap | `901113906048` | Itens de Roadmap (apostas estratégicas) |
| Product Discovery | Design | `901113898193` | Projetos de Discovery + subtasks (UCs, edge cases) |
| Product Delivery | Execução | `901113940182` | Specs de Delivery (escopo fechado, execução). Use esta lista; só crie outra se ela for removida. |

## Status por lista

**Product Roadmap** (`901113906048`) — ciclo completo:
`Open` → `considering` → `prioritized` → `scoping` → `in design` → `in development` → `in qa review` → `ready for deployment` → `not doing` / `Closed`

**Product Discovery / Design** (`901113898193`):
`to do` → `in progress` → `em aprovação` → `fechado`

**Product Delivery / Execução** (`901113940182`): `to-do` → `stand-by` → `dev` → `qa` → `done` (confirme variações em runtime).

## Custom Fields — Folder Product Roadmap (conjunto rico)

Use estes IDs ao setar campos via `custom_fields: [{ id, value }]` no create/update de task.

| Campo | ID | Tipo | Valores / Observação |
|-------|----|------|----------------------|
| Reach | `8ccda77a-706e-461c-9747-4ddb999322c3` | number | RICE — alcance estimado |
| Impact (1-5) | `ecccb2c7-b0f1-49bc-9079-30dd230cefd4` | number | RICE — 1 a 5 |
| Confidence % | `88d02b71-c7e5-4084-8371-50d8bb72754b` | number | RICE — 0 a 100 |
| Effort (1-5) | `c58a1122-7f91-4611-aa15-66dde792c593` | number | RICE — 1 a 5 (esforço) |
| MoSCoW | `e4831715-fab6-4d12-b017-89601e257f68` | drop_down | Must Have `0eb88c1b-cf34-4d8f-a48d-4b8e06f4a104` · Should Have `b29d13fd-1dfb-46c3-9550-9e1325ed1e6b` · Could Have `2ecb5655-fdd1-4681-8606-a0182b190063` · Would Have `6433b0f3-bee7-433f-acca-3c07aff5902e` |
| Horizonte | `f55ec4a4-e0d8-45e0-bc2d-9de48884644f` | drop_down | Considering `2a15294d-2dd9-49b6-9992-72e1ac8d1653` · Now `569c551b-35a7-4d68-8214-4eb8107b929c` · Next `a9d5d058-80ac-4959-a924-7514e6a8ea89` · Later `91466793-baee-4503-a807-c6118ddc4ee8` |
| Squad | `d82385d0-dc8c-47ed-b5c8-46bd1b20e665` | drop_down | Squad PAM `baf8baa0-b844-447b-aea7-8171e9aaae15` · Squad Loteria `2ce90140-ba81-4138-af70-7c610cdbc0c3` · Squad Novos produtos `2ed8c4a5-2fa5-406c-8ee6-4fb012ecdd8b` · Squad Integrações `bf9b3ae5-d159-4a32-8eb2-093954195ec3` |
| _Projeto | `5defab83-6de8-44cd-bf06-3e349cd750d3` | drop_down | Tradicional `fb810e66-4fc4-4c5f-bad0-30bdb2cc44a2` · Bravo `2c202d8d-e37c-48a6-974a-479e16b29514` · Blow `fb51bfa2-d1bb-4c27-ae28-92210afcddd9` · NGX `e14d0fce-49d2-491d-b101-891d4e3a7e2d` · Plug n Play `05b89c3f-8826-4004-9e49-55f414e2e99f` · Cactus `d69617a0-0de7-44fa-9c42-fbcda704a0e1` · Loteria 2.0 `76bf99f0-f0a9-4b49-be5c-0010876568fd` |
| Impacto | `1217b008-0b54-4e08-a412-ec2e2d92bfc3` | drop_down | Receita/Conversão `d303b8f7-3341-4d9c-8c1a-4d1734c9f51d` · Retenção `4b35c313-285b-4d99-be1c-029504d43260` · UX `a43bdf3c-6a99-4758-84ab-33cc357a0388` · Eficiência Operacional `62b4952f-f0f9-4afd-953c-98acd084dd74` · Compliance `b839fbd5-edee-4a96-be88-5a49a7c43818` · Risco/Fraude `13634640-5a57-4afb-8b88-da85804b6484` |
| Phase | `29a31021-bf71-40c1-b352-0ec1a30e027e` | drop_down | Research `487c74a5-2753-4a43-83c1-9b7fb39e6c45` · Ideation `f0fb6ad4-7732-42f5-b1a7-13f323dc3db4` · Design Spec `4c317891-a68a-476f-8fef-ad3be1900850` · Implementation `e88d5ecc-c73e-45bb-b847-00919e2ae2fa` · Review `aed1951c-8e2d-4c84-a681-5efe60744c3e` · Complete `9e399a6d-7954-44c4-a564-d4ff72ffcc68` |
| Initiative | `cd583a2a-7355-46bb-8ca1-97bc23e74945` | drop_down | Reduce system outages · Increase CSAT · Improve usability · Improve speed & performance · Improve quality *(opções genéricas do template — confirmar se o time renomeou)* |
| Release Status | `b0838de4-5ee8-4f52-8adc-6e64aa2d121b` | drop_down | On Track · Needs Attention · At Risk · Blocked · Complete · Deferred |
| _Classe | `4ea80622-a909-4133-b859-f2191b071e33` | drop_down | Evolução de Produto `28079ca9-fdcc-4e10-bbb5-860c8eae1357` · Incidente `a394043c-...` · Infra · Item Projeto `c6a603a3-...` · Solicitação de Mudança |
| Tipo de Chamado | `ce57cd01-1842-4b79-ab89-d17b2fa97a72` | drop_down | Incidente · Solicitação de Serviço · Dúvida |
| Product Feature | `34a00a1a-f389-417c-8090-3fb562ee9591` | labels | Core Product, Inbox, Dashboards, Administration, Integrations, Filters, Performance, Payment Processing, Login, Search |
| T-Shirt Sizing | `2eb0e96e-8715-453b-8a82-79a184679e82` | emoji | 1–5 |
| On Roadmap | `5e9ed755-41bd-487d-867f-8cce17f20d39` | checkbox | — |
| Leadership Request | `c992cc15-62df-4935-b6cb-d59f81dbc579` | checkbox | — |
| QA | `3b91bc1e-c297-481e-a30a-eafac7588e6e` | users | — |
| Requester | `48aa57d3-7edc-4e64-9ada-f5d1884cee4f` | users | dono solicitante (single) |
| Solicitante | `79a15f9c-4dfa-4ab2-87c6-fef6cc4b1adc` | users | (single) |
| _Urgência | `0536092c-8553-470e-b5cd-57c78bb38a74` | number | campo legado (ITSM) |
| _Valor | `50eca712-5f99-4351-b53f-c402daa9481d` | number | campo legado |
| _Risco Reg. | `e973c619-4895-4ecf-9d3c-f53eb1e36cde` | number | risco regulatório |
| CPF | `a1af3692-8ac4-487e-9a8e-38538635acbb` | short_text | campo legado (ITSM) |

> Campos `BASELINE_*` são do sistema (Gantt baselines) — não setar.

## Custom Fields — Folders Discovery e Delivery (conjunto enxuto)

Herdados do space, sem os campos de priorização do Roadmap:
`_Urgência`, `Impacto`, `QA`, `_Classe`, `_Valor`, `_Projeto`, `Solicitante`, `CPF`, `Tipo de Chamado`, `_Risco Reg.` (mesmos IDs da tabela acima).

> Os campos RICE / MoSCoW / Horizonte / Squad / Initiative **só existem no folder Roadmap**. Em Discovery e
> Delivery, a priorização vive no item de Roadmap pai — não tente setar esses campos lá.

## Convenções

- **Custom ID** das tasks: `VL-XXXXX` (gerado automaticamente). Use em links: `https://app.clickup.com/t/9006076935/VL-XXXXX`.
- **Vínculo entre níveis**: não há parent nativo cross-folder. Três mecanismos, cada um para um propósito
  (detalhe e guardrail em [clickup-method.md](clickup-method.md) → "Vínculos entre níveis"):
  - **Linked task** (`clickup_add_task_link`) — vínculo de **pertencimento**, sempre presente (Discovery/Delivery → Roadmap Item; Delivery → Discovery de origem).
  - **Dependência** (`clickup_add_task_dependency`, `waiting_on`/`blocking`) — só quando há **ordem real**; alimenta Gantt/Timeline.
  - **Subtask** (campo `parent` no create) — decomposição **macro** na mesma lista; usar com parcimônia (ver guardrail).
- **Sempre espelhar no corpo**: ao criar um linked task, atualize a seção 🗂️ Portfólio de Projetos do Roadmap Item.
- **Não usamos**: *Tasks in Multiple Lists* nem o campo *Relationship* (decisão de modelagem — manter o vínculo simples).
- **Updates**: ClickUp não tem "Activity Update" como o Linear. O equivalente é um **comentário** na task
  (`clickup_create_task_comment`).
