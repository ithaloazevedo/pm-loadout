# ClickUp — Configuração do Workspace (Vertical Tech)

Mapa de IDs reais do workspace para a skill `clickup-spec` e o agente `agente-delivery` agirem
sem precisar re-descobrir a estrutura. **Confirme via MCP no início de cada sessão** (IDs podem mudar
se o workspace for reconfigurado). Se um ID divergir, atualize este arquivo.

> **Mudança estrutural em 2026-09-10, precisada em 2026-09-21**: o folder Roadmap/Strategy (com a lista
> Objetivos/OKR) e o folder Discovery & Design saíram do processo. Eles **não foram excluídos do ClickUp**:
> continuam existindo no Space e estão em uso por outro time (confirmado pelo PM em 2026-09-21). Para esta
> skill são **fora de escopo** — o folder do nosso time é o do Time PAM, e só ele. O time passou a trabalhar
> por **sprints** — ver
> `knowledge/domains/processo.md` → "Modelo de Trabalho: Sprints" e
> `knowledge/decisions/2026-09-10-migracao-esteira-continua-para-sprints-remocao-okr-e-discovery.md`. Este
> arquivo já reflete a estrutura nova; onde algo ainda depende do modelo antigo, está marcado como **legado**.

> Última verificação: 2026-09-21 (via `clickup_get_workspace_hierarchy`, `clickup_get_folder`, API `/folder/{id}/list`).

## Hierarquia

| Nível | Nome (funcional) | Nome real no ClickUp | ID |
|-------|-------------------|----------------------|----|
| Workspace | Workspace | Workspace | `9006076935` |
| Space | **Vertical Tech** | Vertical Tech | `90114055709` |
| Folder | **Sprints — PAM** | Sprints | `90118303225` |
| Folder | ~~Sprints — Backoffice~~ **legado, não usar** | Pasta do sprint | `90118303239` |
| Folder | **Delivery: Experiência do jogador** | Delivery: Plataforma | `90118093878` |
| Folder | **Delivery: Operação e afiliados** | Delivery:Backoffice & Integração | `90118093917` |
| Folder | **Delivery: Provedora de conteúdo** | Delivery: Produto | `90118093918` |

> ⚠️ **Fora de escopo desta skill**: Folder Roadmap/Strategy (`90118093876`, lista Objetivos `901114034994`)
> e Folder Discovery & Design (`90118093877`, listas Discovery `901114029780` e Benchmarking `901114111104`).
> Eles **existem e estão em uso por outro time** — não foram excluídos. Para o Time PAM não são estrutura
> viva: não crie, mova nem leia itens neles. Registro antigo que os referencie é histórico.
>
> ⚠️ **Achado não resolvido, não use como estrutura oficial**: existe um terceiro folder chamado "Sprints"
> (`90118643577`, lista "Sprint 1 (31/8 - 11/9)" `901114762357`) sem squad identificado — provável resquício
> de teste. Não crie itens ali até confirmação do PM.
>
> ✅ **Resolvido em 2026-09-21**: a divergência de 2026-09-17 — Strategy (`90118093876`) e Discovery & Design
> (`90118093877`) ainda aparecerem na hierarquia viva — foi levada ao PM. Existem mesmo, pertencem a outro
> time, e a "remoção" de 2026-09-10 foi decisão de processo do Time PAM, não exclusão no ClickUp. Ficam fora
> de escopo (ver nota acima). A lição que permanece: presença na árvore não prova uso, e ausência não prova
> remoção.
> Também achei uma lista nova, "Sprints — Provedora de conteúdo" (`90118643577`, folder "Delivery: Produto"),
> com sprints numeradas de 1 a 9 (`901115367903` a `901115367915`) — pode ser o mesmo "terceiro folder
> Sprints" citado acima (mesmo ID `90118643577`), o que sugeriria que não é resquício de teste, e sim um
> Sprint Folder real da squad Jogos ainda não documentado. Não usei essa lista nesta operação — confirme com
> o PM antes de tratá-la como ativa.
>
> ⚠️ **Discrepância encontrada em 2026-09-18** (`clickup_get_workspace_hierarchy`, mesmos parâmetros acima):
> o folder **Sprints — PAM** (`90118303225`) não é um folder-irmão no nível do Space como a tabela de
> Hierarquia no topo deste arquivo descreve — ele aparece **aninhado dentro do folder "Delivery: PAM"**
> (`90118093878`, nome real retornado pela API hoje; a tabela acima chama esse mesmo ID de "Delivery:
> Experiência do jogador"). A lista **Backlog** (`901114029784`), que este arquivo documenta como filha
> direta de "Delivery: Experiência do jogador", está na prática dentro dessa subpasta "Sprints — PAM" —
> confirmado tanto por `clickup_get_workspace_hierarchy` quanto por `clickup_get_task` num card real
> (`868kf0wep`, antes de movido: `list.name = "Backlog"`, `folder.id = "90118303225"`, `folder.name =
> "Sprints PAM"`). Efeito prático já observado: o card `868kf0wep` — conteúdo 100% sobre integração de
> provedor de jogos (squad Backoffice) — estava fisicamente nesse Backlog da squad PAM, não no Backlog de
> "Delivery:Backoffice & Integração" (`901114029782`) onde deveria estar; eu o movi via `clickup_move_task`
> nessa mesma operação. Não reescrevi a tabela de Hierarquia acima (mudar o modelo documentado de
> "folders irmãos" para "Sprints aninhado dentro de Delivery" é decisão estrutural, não correção trivial) —
> confirme com o PM se isso é reorganização real do ClickUp ou representação nova de uma ferramenta antes de
> tratar esta nota como resolvida. **Consequência prática imediata**: antes de assumir que um item está no
> Backlog/folder "certo" só pelo nome da squad no título, confirme `folder.id` via `clickup_get_task` —
> nome da lista ("Backlog") sozinho não garante o folder.
>
> Na mesma varredura, o folder de Sprint da squad Backoffice ("Pasta do sprint", `90118303239`, lista ativa
> `901115365054`) **não apareceu em nenhum lugar** de `clickup_get_workspace_hierarchy` (nem como filho do
> Space, nem aninhado em "Delivery:Backoffice & Integração") — mas `clickup_get_folder` e `clickup_get_list`
> diretos por ID confirmaram que ele existe e funciona normalmente. Ou seja, a ausência na árvore retornada
> por `clickup_get_workspace_hierarchy` não prova que um folder foi removido — só a tentativa direta por ID
> prova presença ou ausência real. Mesmo padrão de cautela do achado de 2026-09-17 acima, agora também para
> folders, não só para task types.

### Listas conhecidas

| Folder | Lista | ID | Uso |
|--------|-------|----|-----|
| Sprints — PAM | **Sprint ativa** — resolver ao vivo | _sem ID fixo_ | ⚠️ **Nunca reuse um ID de sprint desta doc.** A sprint vira a cada 2 semanas — é o comportamento esperado, não drift. Liste as listas do folder `90118303225` e escolha aquela cujo intervalo de datas no nome contém a data de hoje. Histórico: Sprint 1 (7/9–20/9) `901114417832`; Sprint 2 (21/9–4/10) `901115407666` |
| Sprints — PAM | ⚠️ **Backlog do Produto** | `901114419863` | Lista com fluxo de status da squad Jogos/Provedora de conteúdo (`nao iniciada → desenvolvimento → teste → refatorar → alpha → concluido/cancelado`), mas hospedada dentro do folder de Sprints do PAM. Provável desalinhamento — **confirme com o PM antes de usar**; não assuma que é backlog do PAM. |
| ~~Sprints — Backoffice~~ | ~~sprint própria~~ | `901115365054` | ⚠️ **Legado.** Backoffice & Integrações e Plataforma viraram um **Time PAM** único em 2026-09-18 — o folder de sprint do time passa a ser o Sprints — PAM. Não planeje aqui sem confirmar com o PM |
| Delivery: Experiência do jogador | **Backlog** | `901114029784` | Descoberta + refinamento — squad PAM. Item pronto entra na Sprint ativa (Sprints — PAM) |
| Delivery: Experiência do jogador | **Execução** (legado) | `901114029785` | ⚠️ Board pré-sprints. Só contém itens que já estavam lá antes da migração — não recebe itens novos. Saída gradual: devolver ao Backlog ou encaixar na Sprint ativa, sempre com confirmação do PM |
| Delivery: Operação e afiliados | **Backlog** | `901114029782` | Descoberta + refinamento — squad Backoffice. Item pronto entra na Sprint ativa (Sprints — Backoffice) |
| Delivery: Operação e afiliados | **Execução** (legado) | `901114029783` | ⚠️ Mesmo status do board legado do PAM — sem itens novos, saída gradual |
| Delivery: Provedora de conteúdo | **Backlog** | `901114029786` | Projetos refinados aguardando sprint — squad Jogos. **Squad ainda não migrou para sprints** — segue no fluxo Backlog→Execução |
| Delivery: Provedora de conteúdo | **Execução** | `901114029876` | WIP — squad Jogos (fluxo antigo, ainda em uso; não é "legado" como os dois acima) |
| _(fora da hierarquia de produto)_ | **Operação, sustentação e infraestrutura** | `901114236869` | Tickets operacionais — acesso, infra, configuração, suporte a terceiros. Confirmado via MCP em 2026-08-25. Status: `pendente` → `em progresso` → `em validação` → `completo`. Template: [template-operacional.md](template-operacional.md) |

**Regra de Delivery:** todo Projeto de Delivery **nasce no Backlog** do folder correspondente à **Squad
responsável pela execução**, já com o tipo final (`Epic`/`Tarefa`/`Bug`/`Correção`) — não existe mais um item
de Discovery separado. Migra para a **Sprint ativa** do squad (PAM ou Backoffice) ao entrar em execução —
squad Jogos continua migrando para a lista **Execução** do próprio folder, sem Sprint Folder ainda. Nunca criar
listas novas nos folders. Squad não é um custom field em Delivery — é a **escolha do folder** (confirme com o
usuário quando não for óbvio):
- Squad Experiência do jogador → folder Delivery: Experiência do jogador → Sprints — PAM
- Squad Operação e afiliados → folder Delivery: Operação e afiliados → Sprints — Backoffice
- Squad Provedor de jogos → folder Delivery: Provedora de conteúdo → Execução (fluxo antigo)

## Status por lista

**Backlog — não é um fluxo único, diverge por squad** (confirmado via `clickup_get_list` em 2026-09-10):
- **Experiência do jogador** (`901114029784`): `backlog` → `em refinamento` → `pronto p/ design` → `em design` → `pronto p/ execução` → `priorizado` → `despriorizado` (done) / `fechado` (closed)
- **Operação e afiliados** (`901114029782`): `backlog` → `em design` → `em refinamento` → `pronto p/ execução` → `priorizado` → `complete` (closed) — **sem** `pronto p/ design` como status separado, e a ordem de `em design`/`em refinamento` é invertida em relação ao PAM
- **Provedora de conteúdo** (`901114029786`): não reverificado nesta atualização — confirmar via `clickup_get_list` antes de assumir paridade com as outras duas

**Sprint ativa — PAM** (resolva o ID ao vivo, ver tabela de Listas; fluxo confirmado via `clickup_get_list` em 2026-09-10):
`pendente` → `em desenvolvimento` → `bloqueada` → `em revisão técnica` → `em homologação (alpha)` →
`deploy p/ prod` → `cancelado` (done) / `pronto` (done) / `fechado` (closed)

**Sprint — Backoffice** (`901115365054`, **legado** após a fusão em Time PAM; fluxo confirmado em 2026-09-10):
`pendente` → `em desenvolvimento` → `bloqueada` → `em revisão técnica` → `em homologação` →
`deploy p/ prod` → `cancelado` (done) / `pronto` (done) / `fechado` (closed)

> As duas sprints têm fluxo **quase idêntico** — a única diferença hoje é `em homologação (alpha)` (PAM) vs.
> `em homologação` (Backoffice). Ainda assim, confirme via `clickup_get_list` antes de mover um card: são
> listas distintas, e a paridade pode quebrar no futuro como já aconteceu com os antigos boards de Execução.

**Execução — Experiência do jogador (legado, `901114029785`)** — mantido só para itens pré-migração:
`pendente` → `desenvolvimento` → `bloqueada` → `revisão técnica` → `teste em dev` → `deploy p/ alpha` → `teste em alpha` → `deploy p/ prd` → `cancelado` (done) / `finalizado` (closed)

**Execução — Operação e afiliados (legado, `901114029783`)** — mantido só para itens pré-migração:
`pendente` → `desenvolvimento` → `bloqueada` → `revisão técnica` → `teste dev` → `deploy p/ alpha` →
`teste homolog` → `deploy p/ prd` → `cancelado` (done) / `finalizado` (closed)

> Não crie itens novos em nenhum dos dois boards de Execução legados — eles só existem para escoar o que já
> estava lá antes da migração. Item novo vai direto para dentro da Sprint ativa do squad correspondente.

**Execução — Provedora de conteúdo** (`901114029876`, squad ainda não migrada para sprints — fluxo em uso normal):
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
`agente-governanca`, não inferência do agente operacional). **O campo Objetivo (list_relationship) está
duplamente morto desde 2026-09-10**: além de nunca ter sido herdado por Discovery/Delivery, a própria lista
Objetivos que ele apontava não existe mais:

| Campo | ID |
|-------|-----|
| Time (Squad) | `80057eda-8639-493b-a985-95c4b742c18f` |
| Horizonte | `f83d2bfd-56fb-40d8-bf0e-91cd978b3dfd` |
| Impacto | `44fc97aa-0d54-4d89-b7a1-a57e7618550b` |
| Alcance | `793e092e-1f45-4532-a1cb-080991d1f9ec` |
| T-Shirt Sizing | `2eb0e96e-8715-453b-8a82-79a184679e82` |
| Votos | `8a3388a0-cc3a-4f72-b374-38d3f8327b69` |
| Score | `554b5817-1c01-40e4-9d21-4dae33b2111e` |
| Objetivo (list_relationship) — ⚠️ lista-alvo removida | `70d76ca2-08fc-49b5-8baa-68eecb60aa32` |
| Iniciativa (campo de vínculo) | `6c59d3f8-f22d-4b7b-93f4-b3d8b84a2cc5` |
| Data de Início/Conclusão Prevista | `cf52c4b2-2e9a-4098-bccb-826ba13e1746` / `929a07f6-8d58-4d02-a0db-19f64d7d7694` |
| Progresso / Resumo | `d1b5ade4-77ba-432e-8c87-e3c26f1d30dd` / `faac86b5-8d69-45ae-820f-d89539c6abfd` — automáticos, não setar |

> Campos `BASELINE_*` são do sistema (Gantt baselines) — não setar.
> **Fórmula histórica** (só aplicável enquanto a lista Iniciativas existia): `Score = (Impacto × Votos × Alcance) / T-Shirt-Size`.

## Custom Fields — Espaço (⚠️ NÃO são herdados uniformemente por todas as listas)

> **Correção 2026-08-14**: esta seção afirmava que os campos abaixo eram herdados do Espaço por
> todas as listas de Discovery/Delivery. **Falso, confirmado via `clickup_get_custom_fields`** com
> `list_id` + `folder_id` + `space_id` + `include_workspace` na lista Backlog de "Delivery: Operação
> e afiliados" (`901114029782`): só `KPIs` e o campo vestigial `Iniciativa` existem ali — `Módulo do
> PAM`, `Empresa`, `MoSCoW` e `_Projeto` **não aparecem em nenhum escopo** (nem list, nem folder, nem
> space, nem workspace). Confirmado também em dois cards reais dessa lista (`868kapw4g`, `868kf0wep`
> via `clickup_get_task` com `include: ["custom_fields"]`) — nenhum dos dois tem esses 4 campos. Em
> contraste, o card real `868kpcu41` (lista Execução do folder "Delivery: Plataforma") **tem** os 4.
> Ou seja: **esses campos são configurados por lista/folder individualmente, não pelo Espaço** — a
> tabela abaixo generalizava a partir de uma squad só. Antes de exigir ou setar qualquer um destes 4
> campos num item novo, rode `clickup_get_custom_fields` na lista de destino e confirme que o campo
> existe ali. Ver `knowledge/observability/2026-08.md` (entrada de 2026-08-14) e não repita a
> generalização em outras referências sem essa mesma verificação.

Campos vistos em Discovery/Delivery (presença **varia por lista** — confirme antes de usar):
- **Iniciativa** (`6c59d3f8`) — `tasks` type: campo vestigial desde a remoção do nível Iniciativa — não preencher, não exigir em validações. Desde 2026-09-10 não há mais nível Objetivo para vincular: o Projeto de Delivery é o topo do processo, sem vínculo formal a um item superior.
- **KPIs** (`1217b008-0b54-4e08-a412-ec2e2d92bfc3`) — `drop_down`: confirmado presente em toda lista de Delivery verificada até agora, incluindo o Backlog PAM (`901114029784`, confirmado 2026-09-18 por `clickup_get_custom_fields` + leitura de 27 tasks reais); pode ser preenchido no próprio card quando o contexto permitir. Ver tabela de opções abaixo. **Cuidado com decodificação**: cards antigos podem trazer um índice de opção fora do range das opções hoje disponíveis (sinal de opção removida do menu no passado) — não arrisque um nome nesse caso, trate como "já preenchido, não decodificável com segurança" e sinalize para checagem visual no ClickUp.
- **Empresa** (`75d90db5-4d63-44be-8f6e-4c9981de755b`) — `drop_down` (opções: Tradicional / Bravo / Vertical): confirmado presente no folder "Delivery: Plataforma", incluindo o Backlog PAM (`901114029784`, confirmado 2026-09-18); **confirmado ausente** na lista Backlog de "Delivery: Operação e afiliados". Não assuma presença sem checar. Campo é single-select — cards que cobrem múltiplas casas ao mesmo tempo (ex.: uma funcionalidade entregue em Tradicional e Bravo) **usam `Vertical`** (option id `ea610ca6-b5ff-408a-8afc-3e53a545001f`): convenção confirmada pelo PM em 2026-09-21, primeiro uso no card `868m7nu02`. `Vertical` é o valor de item multi-marca, não apenas de trabalho da holding. Se nem essa opção couber, não force uma escolha — sinalize ao PM.
- **Módulo do PAM** (`f02314ee-a656-4006-8194-9ad5d18cea42`) — `drop_down`: taxonomia de produto por módulo do PAM. **Obrigatório quando o campo existe na lista de destino** — mas **confirmado ausente** na lista Backlog de "Delivery: Operação e afiliados" (ver correção acima); **confirmado presente** no Backlog PAM (`901114029784`, confirmado 2026-09-18). Não invente o campo onde ele não existe; se ausente, não bloqueie a criação por causa dele — sinalize a lacuna no handoff. Confirmado presente por prova de escrita na antiga lista Discovery (`901114029780`, folder "Discovery & Design", **removido em 2026-09-10** — referência histórica, não confirme mais nada por lá): `clickup_create_task` gravou o valor na task `868m1hqe7` (2026-09-04) e a releitura via `clickup_get_task` confirmou o valor persistido, mesmo o campo **não aparecendo** em `clickup_get_custom_fields` (list+folder+space+workspace) para essa lista. Reforça o padrão já visto em `_Classe`: leitura via `clickup_get_custom_fields` ou task sem o campo preenchido não prova ausência — só escrita + releitura prova de forma definitiva. **Confirme presença na Sprint ativa do PAM (resolva o ID ao vivo) na primeira operação** — ainda não verificado nela. Confirmado presente no Backlog PAM `901114029784` por escrita+releitura em 2026-09-21 (card `868m7nu02`).
- **Correção 2026-09-18**: a task `868kf0wep` teve `Empresa`/`Módulo do PAM` rejeitados por `clickup_update_task` (`"Custom field does not exist in the task location hierarchy"`) **não por anomalia de conector** — uma sessão concorrente (fora desta missão) moveu essa mesma task do Backlog PAM (`901114029784`) para o Backlog de "Delivery: Operação e afiliados" (`901114029782`) ao mesmo tempo, lista onde `Empresa` e `Módulo do PAM` genuinamente não existem (ver confirmação logo acima). O erro era o comportamento correto para a lista de destino após o move — o agente desta missão só não tinha visibilidade da mudança concorrente. Risco real de duas sessões operando na mesma task ao mesmo tempo, não falha do agente nem do campo; ver `knowledge/observability/2026-09.md`, entrada 2026-09-18.
- **MoSCoW** (`cd1b5e72-27dd-45b3-a466-9473e11755b3`) — `drop_down` (Must/Should/Could/Would Have): confirmado presente no folder "Delivery: Plataforma" (lista Execução); **confirmado ausente** na lista Backlog do mesmo folder (`901114029784`) — write-test via `clickup_update_task` rejeitado com "Custom field does not exist in the task location hierarchy" (2026-08-27, task `868kxgrc7`). Ou seja, o campo não é uniforme nem dentro do mesmo folder — confirme lista a lista antes de usar, não só folder.
- **_Projeto** (`5defab83-6de8-44cd-bf06-3e349cd750d3`) — `drop_down`: confirmado presente no folder "Delivery: Plataforma"; presença em outras listas não verificada.
- **_Classe** (`4ea80622-a909-4133-b859-f2191b071e33`) — `drop_down` (Evolução de Produto / Incidente / Infra / Item Projeto / Solicitação de Mudança, orderindex 0–4 nessa ordem — option ID de "Solicitação de Mudança" é `218ecd12-d3b8-40af-83a3-e329393f4a91`). **Correção 2026-08-17 (revoga a "terceira confirmação de ausência" do mesmo dia em `knowledge/observability/2026-08.md`)**: o campo **existe** no folder "Delivery: Plataforma" (lista Execução) — prova definitiva por escrita: `clickup_create_task` gravou o valor via `custom_fields` na task `868kt2hdd` e a releitura via `clickup_get_task` confirmou o valor persistido; o mesmo campo já aparecia com valor setado no card real `868kmj13a`. O que é real: nem `clickup_get_custom_fields` (list_id+folder_id) nem a leitura de uma task específica sem esse campo preenchido são confiáveis para provar **ausência** — só a tentativa de escrita + releitura prova de forma definitiva se um campo existe numa lista. `_Risco Reg.` não foi retestado por essa via — a dúvida sobre ele permanece em aberto.
- **Progresso** (`d1b5ade4`) — `automatic_progress`: auto, não setar
- **BASELINE_*** — sistema Gantt, não setar

**Mapa por lista confirmado (2026-09-02)** — `clickup_get_custom_fields` com list+folder+space+workspace na
lista **Execução** de "Delivery: Operação e afiliados" (`901114029783`), mais releitura do card `868m0b3ph`
após escrita bem-sucedida: nessa lista **existem** `Módulo do PAM`, `KPIs`, `_Classe`, `Solicitante` (dois
campos homônimos — um `users`, um `short_text`), `Tipo de Chamado`, `Iniciativa` (vestigial) e `Progresso`.
**Não existem** `Empresa`, `MoSCoW` nem `_Projeto`. Consequência prática: `Módulo do PAM` está **ausente no
Backlog** (`901114029782`) e **presente na Execução** (`901114029783`) do **mesmo folder** — a variação é por
lista, nunca por folder. Nunca infira a presença de um campo a partir do folder ou de uma lista irmã.

> Impacto, Alcance, T-Shirt Sizing, Score, Horizonte, Votos e Time **não existem** em Discovery/Delivery — ver seção de priorização acima. Para sinalizar urgência num item de Delivery/Discovery, use o campo **nativo** de prioridade do ClickUp (`priority`: urgent/high/normal/low via `clickup_create_task`/`clickup_update_task`) — não é custom field, existe em toda lista.

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

> ⚠️ **Removidos em 2026-09-10, não crie mais nenhum destes tipos:** `Marco (OKR)` e `Resultado-chave (KR)`
> (viviam na lista Objetivos, removida) e `Pesquisa`/`Protótipo`/`Entrevista` (viviam na lista Discovery,
> removida — descoberta hoje é status dentro do Backlog, não um tipo de tarefa próprio). Se esses task types
> ainda existirem como opção nomeável na API (não confirmado após a remoção dos folders), **não os use** —
> são resquício, não processo vigente.

| Folder / Lista | Tipo de Tarefa (task_type) | Quando usar |
|----------------|---------------------------|-------------|
| ~~Iniciativas~~ | ~~`Iniciativa`~~ | ⚠️ Depreciado — lista fora de uso, não crie itens deste tipo |
| Delivery (qualquer folder) / Sprint (PAM, Backoffice) | `Epic` | Feature completa ou capacidade de produto (nome do tipo no workspace é em inglês: `Epic`, não `Épico`) |
| Delivery (qualquer folder) / Sprint (PAM, Backoffice) | `Débito técnico` | Refatoração, modernização sem feature nova |
| Delivery (qualquer folder) / Sprint (PAM, Backoffice) | `Bug` | Defeito em produção — causa raiz a investigar |
| Delivery (qualquer folder) / Sprint (PAM, Backoffice) | `Tarefa` | Ação pontual sem classificação mais específica (tipo padrão do workspace) |
| Delivery (qualquer folder) / Sprint (PAM, Backoffice) | `Incidente` | Falha crítica com impacto de usuário / SLA em risco |
| Delivery (qualquer folder) / Sprint (PAM, Backoffice) | `Correção` | Fix cirúrgico com causa raiz já identificada — nasce como subtask do Épico/Tarefa que corrige |
| Sprint (PAM, Backoffice) — confirmado por escrita+releitura em 2026-09-17 | `Spike` | Investigação pontual e timeboxed com metodologia ainda incerta (ex.: apurar impacto de um bug em produção, decidir como calcular uma métrica a partir de um schema ainda não mapeado) — diferente de `Tarefa`, que pressupõe caminho de execução já conhecido. Não constava nesta tabela até esta correção; confirmado real via `clickup_get_task` no card `868m4541a` (task_type `Spike`) e via criação bem-sucedida do card `868m69avx` com o mesmo tipo, ambos na então-Sprint 1 do PAM (`901114417832`; a sprint ativa muda a cada 2 semanas — resolva o ID ao vivo). Presença em outras listas (Backlog, Backoffice, Jogos) não verificada — confirme antes de assumir paridade.

> O tipo é definido **uma vez, na criação, ainda no Backlog** — o item mantém o mesmo tipo ao migrar para a
> Sprint ativa (é a mesma task, só muda de lista). Não há mais um tipo de tarefa "de descoberta": a faixa
> `em refinamento` → `pronto p/ design` → `em design` é só status, o tipo já é o final.

**Regra de inferência:**
- "build", "feature", "épico" → **Epic**
- "dívida técnica", "refatorar" → **Débito técnico**
- "bug", "está quebrado" → **Bug** (ou **Correção** se causa raiz identificada)
- "incidente", "down", "SLA" → **Incidente**
- "investigar", "apurar", "metodologia ainda em aberto" → **Spike** (timeboxed; se a metodologia já é conhecida e o caminho é determinístico, prefira **Tarefa**)
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

- **Custom ID (`VL-XXXXX`): habilitado no espaço "Vertical Loto" (`90113593199`), não no espaço "Vertical
  Tech" (`90114055709`).** Correção 2026-08-14 à nota anterior (que dizia `custom_id` sempre `null` — isso só
  valia para tasks do espaço Vertical Tech, verificadas em 2026-08-04). Confirmado via `clickup_get_task` e
  `clickup_search` em tasks reais do espaço Vertical Loto (folder Clientes, lista "Tickets - Tradicional",
  `901110566596`): `custom_id` retorna valores reais (`VL-14409`, `VL-11372`, `VL-3210` etc.). Tasks do
  espaço Vertical Tech continuam retornando `custom_id: null` — **o Custom ID não acompanha a task se ela for
  movida para um espaço onde o recurso não está habilitado** (confirmado: uma task com `custom_id: "VL-14409"`
  em Vertical Loto perdeu o custom_id ao ser movida, via automação de status, para Vertical Tech — ver nota
  abaixo sobre automação entre espaços). Para tasks em Vertical Tech, **não invente `VL-XXXXX`** ao reportar
  links: use a URL real (`https://app.clickup.com/t/<task_id>`, ex. `https://app.clickup.com/t/868kmcquy`).
  Para tasks em Vertical Loto, o Custom ID é confiável e pode ser citado.
- **⚠️ Automação de status move tasks entre espaços (descoberto em 2026-08-14).** Na lista "Tickets -
  Tradicional" (`901110566596`, folder Clientes, espaço Vertical Loto `90113593199`), setar o status para
  `priorizado - pam` (e possivelmente `priorizado - backoffice` / `priorizado - produto`, não testados) dispara
  uma automação do workspace que **move a task fisicamente** para a lista Execução (`901114029785`) do folder
  "Delivery: Plataforma" no espaço **Vertical Tech** (`90114055709`) — aparentemente o mecanismo real de
  handoff de ticket operacional priorizado para o board de engenharia do PAM. A task chega lá com status
  `pendente` (primeiro status do pipeline de Execução), não com o status setado originalmente — o ClickUp
  remapeia porque `priorizado - pam` não existe no novo pipeline. Efeito colateral: a task perde o `custom_id`
  (ver nota acima) e passa a herdar os custom fields do novo folder (ex. `Empresa`, `MoSCoW`, `Progresso`,
  que não existem em Tickets - Tradicional). **Antes de tratar uma mudança de lista/folder/espaço inesperada
  como bug do agente ou corrupção de dados, verifique se não foi este tipo de automação** — confirme via
  `clickup_get_task_time_in_status` (mostra a mudança de status que precedeu o salto) e `clickup_search` pelo
  nome da task (mostra a localização atual real). Caso real confirmado: `868krh1bn` (VL-14409, "Serasa").
  **Mesma automação confirmada dentro de Vertical Tech em 2026-09-03**: setar `priorizado` numa task da
  lista **Backlog** (`901114029784`, folder "Delivery: Plataforma") move a task para **Execução**
  (`901114029785`) do mesmo folder, chegando com status `pendente` — `priorizado` não existe no pipeline
  de Execução. Ou seja, o gatilho não é exclusivo do folder Clientes: `priorizado` é um status de
  promoção, não um status de repouso no Backlog. Se a intenção é deixar o item priorizado **sem** puxá-lo
  para o board de execução, o status precisa ser outro. Caso real confirmado: `868m10vez` (OTP WhatsApp).
  >
  > 🚨 **Conflito com o modelo de sprints, correção decidida em 2026-09-10, execução pendente na UI do
  > ClickUp**: essa automação nativa ainda aponta para o board de **Execução legado** (`901114029785`), não
  > para a Sprint ativa (`901114417832`). **Decisão do PM**: a automação deve ser **desativada/excluída** — o
  > Backlog já funciona como fila da próxima sprint (item `priorizado` = pronto para entrar no próximo
  > Planejamento), não precisa de nenhuma automação puxando para lugar nenhum. Isso não dá para fazer via
  > API/MCP (sem ferramenta de automação disponível) — é ação manual do PM em List/Folder/Space Settings →
  > Automation no ClickUp. **Até a automação ser desativada de fato, trate `priorizado` com cautela**: confirme
  > com o PM se o item realmente deveria ir para o board legado, ou se o destino certo é aguardar o
  > Planejamento e mover manualmente para a Sprint ativa via `clickup_move_task`. Reporte se ela ainda estiver
  > disparando — não normalize o comportamento silenciosamente.
- **Vínculo entre níveis** — sem nível Objetivo nem Iniciativa acima do Delivery desde 2026-09-10; o Projeto
  de Delivery é o topo do processo. Os mecanismos abaixo seguem válidos para o que resta (Delivery ↔
  Correção, e qualquer vínculo pontual que o PM queira registrar):
  - **Linked task** (`clickup_add_task_link`) — vínculo de **pertencimento** entre itens quando fizer sentido pontualmente (ex.: um Bug que referencia o Épico afetado).
  - **Dependência** (`clickup_add_task_dependency`) — só quando há **ordem real** (uma tarefa espera outra). Alimenta Gantt/Timeline.
  - **Subtask** (campo `parent`) — decomposição macro na mesma lista; usar com parcimônia. Subtask carrega só título e escopo mínimo de execução — contexto de produto (objetivo, métricas, decisões, pendências) fica na tarefa pai, nunca duplicado na subtask.
- **Não usamos**: *Tasks in Multiple Lists* nem o campo *Relationship*.
- **Updates**: comentário na task via `clickup_create_task_comment` (não há Activity Update nativo).
- **Conteúdo em português**; termos técnicos consolidados em inglês (Discovery, Delivery, Backlog, Sprint). **OKR/KR deixaram de ser termos do processo em 2026-09-10** — não use mais, exceto em contexto histórico.
