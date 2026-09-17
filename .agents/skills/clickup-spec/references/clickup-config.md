# ClickUp — Configuração do Workspace (Vertical Tech)

Mapa de IDs reais do workspace para a skill `clickup-spec` e o agente `agente-delivery` agirem
sem precisar re-descobrir a estrutura. **Confirme via MCP no início de cada sessão** (IDs podem mudar
se o workspace for reconfigurado). Se um ID divergir, atualize este arquivo.

> Última verificação: 2026-09-17 (folders reconfirmados um a um via `clickup_get_folder`;
> mapa de nomes reais inalterado desde 2026-08-04). Os **IDs** abaixo seguem
> corretos, mas o **nome de exibição** de vários folders mudou no ClickUp desde 2026-07-21 — a coluna
> "Nome" usa o nome **funcional** (papel no processo, usado neste doc e nos templates); o nome real
> atual no ClickUp vai entre parênteses. Confirme por ID, não por nome, ao chamar `clickup_get_folder`.

## Hierarquia

| Nível | Nome (funcional) | Nome real no ClickUp | ID |
|-------|-------------------|----------------------|----|
| Workspace | Workspace | Workspace | `9006076935` |
| Space | **Vertical Tech** | Vertical Tech | `90114055709` |
| Folder | **Roadmap** | Strategy | `90118093876` |
| Folder | **Discovery & Design** | Discovery & Design | `90118093877` |
| Folder | **Delivery: Experiência do jogador** | Delivery: Plataforma | `90118093878` |
| Folder | **Delivery: Operação e afiliados** | Delivery:Backoffice & Integração | `90118093917` |
| Folder | **Delivery: Provedora de conteúdo** | Delivery: Produto | `90118093918` |

### Listas conhecidas

| Folder | Lista | ID | Uso |
|--------|-------|----|-----|
| Roadmap | **Objetivos** | `901114034994` | Marcos OKR e Resultados-chave (KRs) do ciclo |
| Roadmap | ~~Iniciativas~~ | `901114029779` | ⚠️ **Depreciada — não usar.** O nível Iniciativa foi removido do processo (ver `knowledge/domains/processo.md` → "Hierarquia do Processo"). Mantida no ClickUp só como referência histórica: não crie nem edite itens aqui, e não exija vínculo a ela em validações de Discovery/Delivery. |
| Discovery & Design | **Discovery** | `901114029780` | Pesquisa, protótipos, entrevistas, definição de escopo |
| Delivery: Experiência do jogador | **Backlog** | `901114029784` | Projetos refinados aguardando sprint — squad PAM |
| Delivery: Experiência do jogador | **Execução** | `901114029785` | WIP sprint ativa — squad PAM |
| Delivery: Operação e afiliados | **Backlog** | `901114029782` | Projetos refinados aguardando sprint — squad Backoffice |
| Delivery: Operação e afiliados | **Execução** | `901114029783` | WIP sprint ativa — squad Backoffice |
| Delivery: Provedora de conteúdo | **Backlog** | `901114029786` | Projetos refinados aguardando sprint — squad Jogos |
| Delivery: Provedora de conteúdo | **Execução** | `901114029876` | WIP sprint ativa — squad Jogos |

**Regra de Delivery:** todo Projeto de Delivery **nasce no Backlog** do folder correspondente à **Squad responsável
pela execução**. Migra para **Execução** ao entrar na sprint. Nunca criar listas novas nos folders. Squad não é
um custom field em Discovery/Delivery — é a **escolha do folder** (confirme com o usuário quando não for óbvio):
- Squad Experiência do jogador → folder Delivery: Experiência do jogador
- Squad Operação e afiliados → folder Delivery: Operação e afiliados
- Squad Provedor de jogos → folder Delivery: Provedora de conteúdo

## Status por lista

**Objetivos** (`901114034994`):
`not started` → `in progress` → `on track` → `at risk` → `off track` → `cancelled` / `complete`

**Discovery** (`901114029780`):
`to do` → `em progresso` → `em validação` → `pronto` → `complete`

**Backlog (todos os folders de Delivery):**
`backlog` → `em refinamento` → `pronto p/ execução` → `priorizado` → `complete` / `cancelado`

**Execução — Experiência do jogador** (`901114029785`) **e Operação e afiliados** (`901114029783`):
`to do` → `em desenvolvimento` → `bloqueada` → `em revisão técnica` → `em homologação` → `aguardando deploy` → `cancelado` / `pronto` / `finalizado`

**Execução — Provedora de conteúdo** (`901114029876`):
`nao iniciada` → `desenvolvimento` → `teste` → `refatorar` → `alpha` → `concluido` / `cancelado`

## Custom Fields — priorização (Impacto/Alcance/T-Shirt/Score/Horizonte/Votos/Time): sem moradia ativa

Antes da remoção do nível Iniciativa, estes campos viviam só na lista Iniciativas (depreciada acima) — **nunca
foram herdados por Discovery ou Delivery**. Confirmado via `clickup_get_task` em item real de Delivery
(`868kpcu41`, verificado em 2026-08-11): o card não tem esses campos disponíveis, só `Empresa`, `KPIs`,
`MoSCoW`, `Módulo do PAM`, `_Projeto` (estes sim herdados pelo Espaço — ver tabela abaixo).

**Não tente gravar Impacto, Alcance, T-Shirt Sizing, Score, Horizonte ou Votos em Discovery/Delivery** — os IDs
abaixo só existem na lista Iniciativas; a chamada falha ou é ignorada pela API. **Squad não é um campo**: é a
escolha do folder de Delivery (ver "Regra de Delivery" acima). Se o usuário pedir para priorizar um item de
Delivery hoje, use `ice` ou `gist` na conversa — não tente gravar RICE/Score como custom field.

IDs preservados como referência histórica (redefinir a moradia é decisão estrutural — `agente-evolucao` →
`agente-governanca`, não inferência do agente operacional):

| Campo | ID |
|-------|-----|
| Time (Squad) | `80057eda-8639-493b-a985-95c4b742c18f` |
| Horizonte | `f83d2bfd-56fb-40d8-bf0e-91cd978b3dfd` |
| Impacto | `44fc97aa-0d54-4d89-b7a1-a57e7618550b` |
| Alcance | `793e092e-1f45-4532-a1cb-080991d1f9ec` |
| T-Shirt Sizing | `2eb0e96e-8715-453b-8a82-79a184679e82` |
| Votos | `8a3388a0-cc3a-4f72-b374-38d3f8327b69` |
| Score | `554b5817-1c01-40e4-9d21-4dae33b2111e` |
| Objetivo (list_relationship) | `70d76ca2-08fc-49b5-8baa-68eecb60aa32` |
| Iniciativa (campo de vínculo) | `6c59d3f8-f22d-4b7b-93f4-b3d8b84a2cc5` |
| Data de Início/Conclusão Prevista | `cf52c4b2-2e9a-4098-bccb-826ba13e1746` / `929a07f6-8d58-4d02-a0db-19f64d7d7694` |
| Progresso / Resumo | `d1b5ade4-77ba-432e-8c87-e3c26f1d30dd` / `faac86b5-8d69-45ae-820f-d89539c6abfd` — automáticos, não setar |

> Campos `BASELINE_*` são do sistema (Gantt baselines) — não setar.
> **Fórmula histórica** (só aplicável enquanto a lista Iniciativas existia): `Score = (Impacto × Votos × Alcance) / T-Shirt-Size`.

## Custom Fields — Espaço (herdados por todas as listas)

Campos herdados automaticamente por Discovery e Delivery:
- **Iniciativa** (`6c59d3f8`) — `tasks` type: campo ainda existe no card (herdado do Espaço), mas é **vestigial desde a remoção do nível Iniciativa** — não preencher, não exigir em validações. Vínculo de pertencimento hoje é via **linked task direto ao Objetivo** (quando houver), não este campo.
- **Empresa** e **KPIs** — `drop_down`: confirmados presentes em Discovery/Delivery reais (ver nota na seção de priorização acima); podem ser preenchidos no próprio card quando o contexto permitir.
- **Módulo do PAM** (`f02314ee-a656-4006-8194-9ad5d18cea42`) — `drop_down`: taxonomia de produto por módulo do PAM. **Obrigatório em todo card de produto (Discovery/Delivery) — nunca deixar vazio** (ver regra abaixo).
- **Progresso** (`d1b5ade4`) — `automatic_progress`: auto, não setar
- **BASELINE_*** — sistema Gantt, não setar

> Impacto, Alcance, T-Shirt Sizing, Score, Horizonte, Votos e Time **não existem** em Discovery/Delivery — ver seção de priorização acima. **Exceção: o `Módulo do PAM` vive no próprio card** e deve ser sempre preenchido nele.

### Módulo do PAM — opções (option IDs)

Campo `f02314ee-a656-4006-8194-9ad5d18cea42`. Setar via `custom_fields: [{ id, value }]` com o option ID:

| Opção | Option ID |
|-------|-----------|
| Financeiro | `6f96a196-b8a5-426f-bceb-b62dbc34d7d7` |
| Banca de benefícios / SMARTICO | `b7148ba9-24d9-4311-a851-0a0d214dd997` |
| Conta do jogador | `0f31e583-e427-40dc-95d7-d26e41ef5054` |
| Melhorias gerais | `cdda94e1-f394-489d-b0fc-62b084391fc8` |
| Loteria Tradicional | `cdfe5dd3-9327-4975-ae1a-dcd9990cce46` |
| Homes e busca de jogos | `e0d74df6-e7fb-4385-88bb-358f5c55c44b` |
| CRM & Marketing | `2bf1d9a0-a966-4f5a-8104-9fe2437be0e3` |
| Backoffice do operador | `521b2946-9aa6-4691-b9fb-914533e40c45` |
| Afiliados | `203ab8dd-cf46-4e78-bc80-ac6c8e9f390c` |
| Relatórios & Dados | `77524e31-017a-47f7-84b1-c4c5b9754557` |
| Infraestrutura & arquitetura | `03d4d971-5b51-4b27-a420-228510117405` |
| Cadastro e acesso | `6903c361-2398-4c3d-98fe-0c82977ca19f` |
| Validação facial | `5ea5ea17-a4da-4847-aeb4-ea395f28b939` |
| Hub de Esportes / FIRST | `a40eb45c-bcf8-4981-891e-a584fe0e3d24` |
| Integrações com provedor | `c378f6aa-652e-4526-b1e7-8da5f3cd268c` |
| Integrações com agregador | `f66abca9-51bb-4aab-ac8f-edd8424a4d0a` |
| AML - Prevenção a fraudes | `f0294b0a-83f5-4005-99fd-5cb5486b534c` |
| Performance | `2a4ba4bf-8e4c-4c92-a7ed-a291186585b0` |
| Compliance | `dbb97076-1305-4a5f-820c-a811c9f5fa24` |

> **Regra:** todo card de produto (Delivery ou Discovery) nasce com `Módulo do PAM` preenchido — infira do contexto/família (épico pai, feature, módulo afetado). Se não for inferível com segurança, **pergunte antes de criar**; não crie o card com o campo vazio.

## Tipos de Tarefa por Lista

Ao criar uma task via `clickup_create_task`, **sempre selecione o tipo correto**. O tipo muda a view e os campos disponíveis.

| Folder / Lista | Tipo de Tarefa (task_type) | Quando usar |
|----------------|---------------------------|-------------|
| Objetivos | `Marco (OKR)` | Objetivo estratégico do ciclo — meta qualitativa |
| Objetivos | `Resultado-chave (KR)` | Métrica mensurável que comprova o avanço do OKR |
| ~~Iniciativas~~ | ~~`Iniciativa`~~ | ⚠️ Depreciado — lista fora de uso, não crie itens deste tipo |
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
- "build", "feature", "épico" → **Epic**
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

- **Custom ID (`VL-XXXXX`): não confirmado em produção.** Verificado via `clickup_get_task` em 2026-08-04
  em tasks novas e antigas (incluindo uma de 2026-07) — `custom_id` retorna `null` em todas. O recurso de
  Custom ID pode não estar habilitado neste workspace. **Não invente `VL-XXXXX`** ao reportar links: use a
  URL real retornada por `clickup_create_task`/`clickup_get_task` (formato `https://app.clickup.com/t/<task_id>`,
  ex. `https://app.clickup.com/t/868kmcquy`). Se o Custom ID for habilitado depois, atualize esta nota.
- **Vínculo entre níveis** — mecanismos, sem nível Iniciativa no meio:
  - **Linked task** (`clickup_add_task_link`) — vínculo de **pertencimento**, o mecanismo principal: toda Discovery/Delivery → seu Objetivo (quando houver); toda Delivery → seu Discovery de origem (quando promovido).
  - **Dependência** (`clickup_add_task_dependency`) — só quando há **ordem real** (uma tarefa espera outra). Alimenta Gantt/Timeline.
  - **Subtask** (campo `parent`) — decomposição macro na mesma lista; usar com parcimônia. Subtask carrega só título e escopo mínimo de execução — contexto de produto (objetivo, métricas, decisões, pendências) fica na tarefa pai, nunca duplicado na subtask.
- **Portfólio no Objetivo**: ao vincular Discovery ou Delivery a um Objetivo, atualize a seção 🗂️ Portfólio de Projetos do Objetivo no formato `Nome (https://app.clickup.com/t/9006076935/VL-XXXXX)` — o ClickUp renderiza como task-link interativo com status e responsável ao vivo.
- **Não usamos**: *Tasks in Multiple Lists* nem o campo *Relationship*.
- **Updates**: comentário na task via `clickup_create_task_comment` (não há Activity Update nativo).
- **Conteúdo em português**; termos técnicos consolidados em inglês (Discovery, Delivery, Backlog, Sprint, OKR, KR).
