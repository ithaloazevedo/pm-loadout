# ClickUp — Configuração do Workspace (Vertical Tech)

> ⚠️ **Arquivo legado, não referenciado por nenhuma skill/agente ativo.** A fonte real usada por `SKILL.md` e
> `agente-delivery.md` é [clickup-config.md](clickup-config.md) — mais recente (verificado 2026-08-04) e já
> corrigido para refletir a remoção do nível Iniciativa (ver `knowledge/domains/processo.md`). Este arquivo
> ficou desatualizado (ex.: ainda trata a lista Iniciativas como ativa, ainda afirma Custom ID `VL-XXXXX`
> confirmado quando `clickup-config.md` já corrigiu isso para `null`). Mantido só como histórico — não edite
> nem consulte para decisões operacionais; se notar necessidade real de conteúdo daqui, migre para
> `clickup-config.md` em vez de manter as duas cópias vivas.

Mapa de IDs reais do workspace para o agente `agente-delivery` operar no espaço Vertical Tech.
**Confirme via MCP no início de cada sessão** (IDs podem mudar se o workspace for reconfigurado).

> Última verificação: 2026-07-03 (folders de Delivery renomeados: Experiência do jogador · Operação e afiliados · Provedora de conteúdo — mesmos IDs).

## Hierarquia

| Nível | Nome | ID |
|-------|------|----|
| Workspace | Workspace | `9006076935` |
| Space | Vertical Tech | `90114055709` |
| Folder | **Roadmap** | `90118093876` |
| Folder | **Discovery & Design** | `90118093877` |
| Folder | **Delivery: Experiência do jogador (ex-PAM)** | `90118093878` |
| Folder | **Delivery: Operação e afiliados (ex-Backoffice)** | `90118093917` |
| Folder | **Delivery: Provedora de conteúdo (ex-Jogos)** | `90118093918` |

> Cada squad tem seu próprio folder de Delivery — o folder já implica o time. Não é necessário prefixar o nome das listas. A visão cross-squad (diretoria) deve ser criada como **View no nível do Space**, não de folder.

### Listas

| Folder | Lista | ID | Uso |
|--------|-------|----|-----|
| Roadmap | **Objetivos** | `901114034994` | OKRs do ciclo — objetivos e key results |
| Roadmap | **Iniciativas** | `901114029779` | Apostas estratégicas vinculadas a um Objetivo |
| Discovery & Design | **Discovery** | `901114029780` | Pesquisa, benchmark, prototipação, definição de escopo |
| Delivery: Experiência do jogador (ex-PAM) | **Backlog** | `901114029784` | Projetos PAM refinados, aguardando sprint |
| Delivery: Experiência do jogador (ex-PAM) | **Execução** | `901114029785` | WIP da squad PAM |
| Delivery: Operação e afiliados (ex-Backoffice) | **Backlog** | `901114029782` | Projetos Backoffice refinados, aguardando sprint |
| Delivery: Operação e afiliados (ex-Backoffice) | **Execução** | `901114029783` | WIP da squad Backoffice |
| Delivery: Provedora de conteúdo (ex-Jogos) | **Backlog** | `901114029786` | Projetos Jogos refinados, aguardando sprint |
| Delivery: Provedora de conteúdo (ex-Jogos) | **Execução** | `901114029876` | WIP da squad Jogos |

## Status por lista

> Roadmap verificado via MCP em 2026-07-03; demais listas a confirmar na primeira operação.

**Objetivos** (`901114034994`):
`not started` → `in progress` → `on track ` → `at risk` → `off track` → `cancelled` (done) · `complete` (closed)
(⚠️ `on track ` tem espaço no fim — usar exatamente assim até corrigirem na UI)

**Iniciativas** (`901114029779`) — funil da aposta:
`em consideração` → `priorizado` → `em discovery` → `em delivery` → `descartado` (done) · `finalizado` (closed)

**Discovery** (`901114029780`):
`To do` → `In progress` → `Em aprovação` → `Fechado`

**Backlog** (listas `901114029784`, `901114029782`, `901114029786`):
`Backlog` → `Priorizado` → `Em refinamento`

**Execução** (listas `901114029785`, `901114029783`, `901114029876`):
`To do` → `Stand-by` → `Dev` → `QA` → `Aprovado` → `Em correção` → `Deploy` → `Concluído`

## Custom Fields — lista Iniciativas (verificados via MCP em 2026-07-03)

| Campo | ID | Tipo | Opções / Observação |
|-------|----|------|---------------------|
| Time | `80057eda-8639-493b-a985-95c4b742c18f` | drop_down | Experiência do jogador `021d9d26-06eb-4af7-a943-3dec4142cfd6` · Operação e afiliados `5c92d689-a38f-4778-95dc-a387efcdbfe6` · Provedor de jogos `cd1e0cae-9d3c-4fb5-8799-fd68b134fcda` |
| Empresa | `75d90db5-4d63-44be-8f6e-4c9981de755b` | drop_down | Tradicional `2c64c8c0-a3b2-42e4-9599-bf9a6d9839c1` · Bravo `72d1d85b-5f88-48a6-88a6-ac820ff7f8a9` · Vertical `ea610ca6-b5ff-408a-8afc-3e53a545001f` |
| Horizonte | `f83d2bfd-56fb-40d8-bf0e-91cd978b3dfd` | drop_down | Now `53a9a548-…626c72` · `Next ` (⚠️ espaço no fim) `2d251cc0-…9fbf34` · Later `fee7aa18-…c91f7` |
| KPIs | `1217b008-0b54-4e08-a412-ec2e2d92bfc3` | drop_down | Compliance · Conversão · Eficiência Operacional · Receita · Retenção · Satisfação · Segurança |
| Impacto | `44fc97aa-0d54-4d89-b7a1-a57e7618550b` | drop_down | Escala RICE: 3 · 2 · 1 · 0.5 · 0.25 (option IDs no ClickUp) |
| Alcance | `793e092e-1f45-4532-a1cb-080991d1f9ec` | number | **% da base estimada afetada pela iniciativa (0–100)** — não é número absoluto de usuários |
| Votos | `8a3388a0-cc3a-4f72-b374-38d3f8327b69` | votes | Votação do time (proxy de confiança) — **não setável via API**, cada membro vota na UI |
| T-Shirt Sizing | `2eb0e96e-8715-453b-8a82-79a184679e82` | emoji (1–5) | Esforço |
| Score | `554b5817-1c01-40e4-9d21-4dae33b2111e` | text (AI) | **Score = (Impacto × Votos × Alcance) / T-Shirt Sizing** — calculado por AI field a partir dos 4 fatores |
| Objetivo | `70d76ca2-08fc-49b5-8baa-68eecb60aa32` | list_relationship | Relação com a lista Objetivos (`901114034994`) |
| Data de Início Prevista | `cf52c4b2-2e9a-4098-bccb-826ba13e1746` | date | — |
| Data de Conclusão Prevista | `929a07f6-8d58-4d02-a0db-19f64d7d7694` | date | — |
| RICE | `e4fd28cb-a099-4514-9544-dc9fc5ab25f2` | formula | Fórmula nativa (complementar ao Score) |

> **Ritual do Score (definido pelo Ithalo em 2026-07-03):** ao criar uma Iniciativa, **sempre propor os valores de Impacto, Alcance e T-Shirt Sizing e validar com o usuário antes de gravar**. Votos vem da votação do time na UI; o Score é recalculado pelo AI field.
> **MoSCoW não se aplica a Iniciativas** — se usado, é no nível dos épicos (Delivery).
> Campos `BASELINE_*`, `Progresso` e `Resumo` (AI) são do sistema — não setar.

## Tipos de Tarefa

Tipos customizados nomeáveis via API (verificados em 2026-07-03, reconfirmados em 2026-07-23 via erro da API): `milestone`, `form_response`, `meeting_note`, `ai_skill`, `Epic`, `Pesquisa`, `Resultado-chave`, `Incidente`, `Bug`, `Débito técnico`, `Entrevista`, `Hora do Sorteio`, `Person`, `Protótipo`, `Correção`, `Iniciativa`, `Item` (não existe `Projeto` nem `Tarefa` como tipo nomeável).

> **⚠️ Armadilha confirmada em 2026-07-23:** "Tarefa" **não é um `task_type` setável por nome** — tentar `task_type: "Tarefa"` retorna erro da API. O tipo **padrão do sistema** (quando nenhum `task_type` customizado é setado, ou seja `task_type: none`/`null`) é o que a UI do ClickUp exibe como **"Tarefa"** em português. **Para criar uma subtask de Delivery ("Tarefa" da hierarquia de processo), NÃO setar `task_type`** (omitir o parâmetro, ou passar `"none"` num update) — nunca usar `Item` como substituto, isso aparece diferente na UI.

> **🚦 Bug vs. Correção (regra firme, definida pelo Ithalo em 2026-07-03):**
> - **Bug** = defeito identificado **em produção**, com impacto real ou potencial no usuário final.
> - **Correção** = problema encontrado **durante o desenvolvimento**, sem impacto no usuário final — ex.: inconformidade com o protótipo, critério de aceite não cumprido, defeito achado na homologação.
> Na dúvida, pergunte "onde isso foi identificado?": produção → Bug; dev/homologação → Correção.

## Regras de vínculo

| Vínculo | Mecanismo | Regra |
|---------|-----------|-------|
| Iniciativa → Objetivo | `clickup_add_task_link` | Toda Iniciativa criada recebe link para o Objetivo correspondente |
| Discovery/Delivery → Iniciativa | `clickup_add_task_link` | Todo Discovery ou Delivery criado recebe link para a Iniciativa pai |
| Delivery → Discovery de origem | `clickup_add_task_link` | Quando promovido de um Discovery, vincula também ao Discovery de origem |

**Nunca usar** Tasks in Multiple Lists. Exceção à regra anti-Relationship: o campo **Objetivo** (list_relationship) na lista Iniciativas foi adotado pelo time — preenchê-lo **além** do linked task Iniciativa → Objetivo.

## Portão Backlog → Execução

Um Projeto de Delivery só migra do Backlog para Execução quando tem:
- (a) Iniciativa vinculada
- (b) Spec macro escrita
- (c) Viabilidade validada (checkbox marcado)
- (d) Dono definido (assignee)

## Squads

| Squad | Responsabilidade |
|-------|-----------------|
| Backoffice | Backoffice, dashboards e painel de afiliados |
| PAM | Experiência do jogador — cadastro, login, onboarding, acesso a jogos. Sustenta Tradicional.bet.br e Bravo.bet.br |
| Jogos | Vertical como provedora de jogos — Loteria Tradicional, futuro Bingo e integrações com agregadores |

## Convenções

- **Custom ID** das tasks: `VL-XXXXX` (gerado automaticamente). Links: `https://app.clickup.com/t/9006076935/VL-XXXXX`.
- **Backlog default**: todo Delivery **nasce no Backlog do time correspondente**. Só vai para Execução após o portão.
- **Conteúdo em português**; termos técnicos consolidados em inglês (Discovery, Delivery, Backlog, OKR).
- **Macro, não micro**: o agente opera no nível Objetivo / Iniciativa / Discovery / Delivery. Subtasks são da squad.

## Pendências de configuração manual

- [x] Configurar status das listas do Roadmap (Objetivos + Iniciativas) — feito em 2026-07-03; ⚠️ corrigir espaço em `on track ` e `Next `
- [ ] Confirmar/configurar status das listas Discovery, Backlog e Execução
- [x] Custom fields da lista Iniciativas criados (ver tabela acima, com IDs)
- [x] T-Shirt Sizing ativo (campo emoji na lista Iniciativas)
- [x] Task types verificados (`Epic` no lugar de `Projeto`; "Tarefa" = tipo padrão do sistema, não setar `task_type`)
- [ ] Criar View "Todos os times" **no nível do Space** (não de folder) — board ou tabela agrupado por squad, agregando os 3 folders de Delivery
- [ ] Deletar folders de template antigos: `Product Roadmap` (×2), `Product Discovery`, `Product Delivery` — **antes, migrar as tasks legadas** (ex.: VL-12231, VL-11984 no Product Discovery antigo)
