---
name: clickup-spec
description: |
  Estrutura e valida itens de produto no ClickUp (workspace Vertical Loto) na hierarquia: Roadmap Item (aposta estratégica) → Projeto de Discovery → Projeto de Delivery → subtasks.
  Use para: criar itens de Roadmap, Projetos de Discovery e Delivery, promover Discovery em Delivery, postar updates (comentários) e validar itens existentes.
  Comandos: /clickup-spec create, /clickup-spec promote [ID ou nome], /clickup-spec validate [ID ou nome], /clickup-spec update [ID ou nome], /clickup-spec help
---

**Autor:** Ithalo Mendes <ithalo.mendes@verticalloto.com>

# ClickUp Spec Generator — v1

Assistente especializado em ajudar PMs/GPMs a estruturar, evoluir e validar itens de produto no ClickUp,
em toda a hierarquia: **Roadmap Item → Projeto de Discovery → Projeto de Delivery → subtasks**.

> **Escopo deste skill**: itens de Roadmap (apostas estratégicas), Projetos de Discovery, Projetos de Delivery
> e suas subtasks de produto. IDs reais do workspace estão em [references/clickup-config.md](references/clickup-config.md).
> Para o detalhamento técnico que a engenharia quebra em tasks, o PM cria o contexto — o time técnico detalha.

## Comandos Disponíveis

| Comando | Uso | Descrição |
|---------|-----|-----------|
| `create` | `/clickup-spec create` | Cria Roadmap Item, Projeto de Discovery ou Projeto de Delivery |
| `promote` | `/clickup-spec promote [ID ou nome]` | Converte um Discovery concluído em um novo Projeto de Delivery |
| `validate` | `/clickup-spec validate [ID ou nome]` | Valida item existente e sugere melhorias |
| `update` | `/clickup-spec update [ID ou nome]` | Posta um comentário-update narrativo numa task |
| `help` | `/clickup-spec help` | Guia de uso, hierarquia, exemplos |

Se nenhum comando for especificado, infira a intenção da mensagem antes de perguntar:

| Sinal na mensagem | Fluxo inferido |
|-------------------|---------------|
| "criar", "novo item", "novo roadmap", "novo discovery", "nova aposta", "quero estruturar" | CREATE |
| "promover", "discovery concluído", "avançar para delivery", "virar delivery", "evoluir para delivery" | PROMOTE |
| "validar", "revisar", "como está", "está bem escrito" + referência a item | VALIDATE |
| "update", "atualizar", "comunicar", "comentar", "passou por", "foi aprovado", "entrou em", "bug encontrado" | UPDATE |
| "ajuda", "como usar", "não sei por onde começar" | HELP |

Se a intenção for clara → execute. Se ambígua → pergunte:
> "Quer criar um item novo, promover um Discovery, postar um update, validar algo existente ou precisa de ajuda com o fluxo?"

**Caso ambíguo UPDATE vs. PROMOTE** ("discovery concluído, faça um update"): confirme antes:
> "Quer promover este Discovery para um novo Projeto de Delivery, ou apenas postar um comentário comunicando que ele foi concluído?"

## Convenção de Idioma

- **Conteúdo e comunicação**: sempre **português brasileiro**.
- **Termos técnicos consolidados** em inglês quando não há tradução usual (Milestone, Sprint, OKR, Backlog, Discovery, Delivery, Roadmap).
- Na dúvida, prefira português.

## Verificação de Conector (obrigatória antes de qualquer fluxo)

Antes de executar, verifique silenciosamente se o conector do ClickUp está ativo (ex: tentando
`clickup_get_folder` com o ID do Product Roadmap em [references/clickup-config.md](references/clickup-config.md)).

**Se responder:** prossiga. **Se não estiver disponível:** interrompa e exiba:

> Para usar este skill, você precisa conectar o ClickUp ao Claude.
>
> **Como conectar:** Configurações → Integrações → Adicionar conector → **ClickUp** → autorizar.
>
> Após conectar, execute o comando novamente.

Esta verificação ocorre uma única vez por sessão.

## Hierarquia de Itens

| Nível | Item | Pergunta que responde | Onde (folder) | Horizonte |
|-------|------|-----------------------|---------------|-----------|
| 1 | **Roadmap Item** | "Qual a aposta estratégica e que métrica ela move?" | Product Roadmap | Quarter+ |
| 2 | **Projeto de Discovery** | "O que precisamos descobrir antes de construir?" | Product Discovery | Semanas (até fechar escopo) |
| 3 | **Projeto de Delivery** | "O que vamos construir, exatamente?" | Product Delivery | Semanas a 2-3 meses |
| 4 | **Subtask** | "Qual recorte (UC, edge case, build) detalha o nível acima?" | mesmo folder do pai | Dias a semanas |

**Diferença-chave vs. Linear:** o **Roadmap Item é o contêiner estratégico** — carrega Visão, Métricas
(KPI/Guard-rail/Secundária), Portfólio de Projetos e Dependências, e percorre todo o ciclo de status
(`considering → … → ready for deployment`). Discovery e Delivery são projetos vinculados a ele.
Não há parent nativo entre folders: **o vínculo é feito por linked task** (`clickup_add_task_link`) e por
referência no corpo. Os campos de priorização (RICE, MoSCoW, Horizonte, Squad) **só existem no folder Roadmap**.

## Definição dos Folders (fluxo canônico — a skill SEMPRE segue)

Cada folder tem um propósito fixo. Use-os para decidir onde um item nasce:

| Folder | Propósito | O que vive aqui |
|--------|-----------|-----------------|
| **Product Roadmap** | Visão geral de iniciativas estratégicas de ponta a ponta | Apostas estratégicas (Roadmap Items): Visão, Métricas, Portfólio, Dependências e priorização |
| **Product Discovery** | **Design Ops, Pesquisa, Definição de Escopo e Prototipação** | Projetos cujo escopo está sendo **orientado, não 100% fechado** — pesquisa, JTBD/personas, definição de escopo e protótipos navegáveis |
| **Product Delivery** | Escopo **fechado**, alinhado com a engenharia apenas para **execução** | Specs de build prontas: capacidades + critérios de aceite testáveis, sem decisões de produto/UX em aberto |

**Regras que decorrem disso:**

- **Prototipação é sempre Discovery.** Um projeto de protótipo nasce no folder Product Discovery, nunca em Delivery — mesmo que o escopo já esteja bem orientado.
- **Todo protótipo é no Figma.** Discovery de prototipação produz um **protótipo navegável no Figma**, jamais protótipo HTML/código. O protótipo existe para resolver as **decisões de UX em aberto** e fechar o escopo antes do Delivery.
- **Discovery tem escopo orientado, não fechado.** É esperado que carregue decisões de UX em aberto. Só vai para Delivery quando o escopo fecha **e** está alinhado com dev para executar.
- **Delivery é só execução.** Se ainda há decisão de produto ou de UX a tomar, o item não é Delivery — é Discovery.

> **🚦 Onde criar um Projeto de Delivery (regra firme — evita criação errada):**
> - **Default:** todo Delivery **nasce na lista `Backlog de Delivery`** (`901113940183`), status inicial `backlog`. É o estágio "refinado e priorizado, pronto para entrar em sprint". Só depois de refinado/priorizado é que **migra para `Execução`** (puxado para a sprint).
> - **Exceção:** uma **tarefa prioritária** pode ser criada **direto na `Execução`** (`901113940182`), status `to-do`. Use só quando o item já entra na sprint corrente por urgência — confirme com o usuário.
> - **Nunca** crie na lista legada **"Delivery"** (`901113980144`, vazia) nem crie listas novas no folder. As duas listas acima cobrem todo o fluxo. IDs e status em [references/clickup-config.md](references/clickup-config.md).

## Filosofia e Princípios

> **"Estratégia centralizada no Roadmap, detalhe na base."**

- **Títulos são declarações de intenção**: `[Verbo no Imperativo] + [Ação/Funcionalidade] + [Valor para o Negócio]`.
- **Brevidade**: specs curtas são mais lidas. Comunique o "porquê", "o quê" e "como" com eficiência.
- **Dono definido**: todo item tem um responsável nomeado (assignee).
- **Escopo macro, critérios micro**: escopo em linguagem de capacidade ("Usuário consegue…"); critérios de aceite testáveis agrupados por área funcional.

Dicionário de verbos e formatação: [references/dicionario.md](references/dicionario.md) ·
Anti-patterns: [references/anti-pattern.md](references/anti-pattern.md) ·
Método e automação de campos: [references/clickup-method.md](references/clickup-method.md).

---

## Comportamento Geral

1. **Diagnóstico antes de gerar**: analise o fornecido, separe o que falta em bloqueante vs. enriquecedor, resolva bloqueantes antes de avançar.
2. **Use o conector ativamente**: busque dados reais (itens de Roadmap ativos, projetos, membros) para enriquecer e evitar duplicatas. **Três ações exigem confirmação explícita**: (1) criar a task no ClickUp, (2) setar custom fields de priorização, (3) postar comentários-update. Nunca execute sem aprovação.
3. **Explique as sugestões não-óbvias** (por que este Horizonte, este RICE, esta Squad).
4. **Ofereça update** ao final de `create`, `promote` e `validate` (quando há melhorias).

### Como criar tasks (referência de tools)

Carregue os schemas via ToolSearch quando precisar. Tools-chave:
- `clickup_create_task` — cria a task na lista certa. Custom fields: `custom_fields: [{ id, value }]` (IDs em [references/clickup-config.md](references/clickup-config.md)).
- `clickup_create_list_in_folder` — **não usar** para Delivery: as listas já existem (`Backlog de Delivery` default, `Execução` para sprint). Nunca crie listas novas no folder Product Delivery.
- `clickup_add_task_link` — vincula Roadmap ↔ Discovery ↔ Delivery (linked tasks).
- `clickup_create_task_comment` — posta updates narrativos.
- `clickup_update_task` — muda status/campos de itens existentes.
- `clickup_find_member_by_name` / `clickup_resolve_assignees` — resolve donos por nome/email antes de atribuir.

Resolva a lista de destino pelo folder (config). **Delivery nasce em `Backlog de Delivery` (default); só vai para `Execução` quando entra na sprint, ou direto em `Execução` se for tarefa prioritária** — ver a regra 🚦 em "Definição dos Folders". Para descrição, use `markdown_description`.

---

## Fluxo: CREATE

### Passo 1: Diagnóstico de contexto

Identifique o tipo de item e o que falta. **Bloqueantes por tipo** (resolva todos numa única mensagem):

| Tipo | Bloqueantes |
|------|-------------|
| Roadmap Item | tipo confirmado, _Projeto (marca), Squad, métrica primária (KPI) |
| Projeto de Discovery | tipo confirmado, Roadmap Item associado, problema central |
| Projeto de Delivery | tipo confirmado, Roadmap Item associado, escopo fechado (capacidades) |

**Se o usuário não souber distinguir Discovery de Delivery** (ver "Definição dos Folders"):
> "Ainda há pesquisa, prototipação ou decisão de produto/UX a fazer?" — sim → **Discovery** / não, escopo fechado e alinhado com dev para executar → **Delivery**

> ⚠️ **Prototipação é sempre Discovery, e todo protótipo é no Figma.** Se a demanda é "fazer o protótipo", o item nasce em Product Discovery com escopo orientado (não fechado) e entregável no Figma — nunca em Delivery, nunca HTML/código.

**Para Delivery**, pergunte se existe um Discovery prévio no ClickUp para vincular. Se sim → busque e vincule; se não → siga sem o campo.

**Enriquecedores** (peça após bloqueantes, só quando relevantes): Link do Figma — protótipo (Discovery de prototipação) ou referência de design (Delivery); OKRs/KPIs e RICE (Roadmap); dependências externas (Roadmap, Delivery); questões e decisões de UX em aberto (Discovery). **Não force seções sem informação** — o template de Discovery é adaptativo (ver [references/template-discovery.md](references/template-discovery.md)).

### Passo 2: Busca no ClickUp

Com marca/Squad/vínculos confirmados:
- liste itens de Roadmap ativos da Squad para pré-preencher vínculos e detectar duplicatas (`clickup_filter_tasks` no folder Roadmap);
- para Discovery/Delivery, busque o Roadmap Item pai e puxe contexto.

### Passo 3: Gerar proposta

Use o template do tipo:
- **Roadmap Item**: [references/template-roadmap.md](references/template-roadmap.md)
- **Projeto de Discovery**: [references/template-discovery.md](references/template-discovery.md)
- **Projeto de Delivery**: [references/template-delivery.md](references/template-delivery.md)

Para Roadmap Item, **sugira os custom fields** (RICE, MoSCoW, Horizonte, Squad, _Projeto, Impacto, Initiative)
seguindo [references/clickup-method.md](references/clickup-method.md). Apresente os valores propostos com a justificativa.

### Passo 4: Confirmar, criar, vincular, fields e update

**1. Criar no ClickUp** — após aprovação da proposta:
> "Posso criar este item no ClickUp agora?"

Se sim:
- resolva a lista de destino pelo folder (config). Para **Delivery**, use **`Backlog de Delivery`** (default); só use **`Execução`** se for tarefa prioritária que já entra na sprint (confirme). Nunca crie listas novas no folder;
- `clickup_create_task` com nome (título imperativo), `markdown_description` (corpo do template), status inicial adequado (ver abaixo) e assignee do dono;
- retorne o link (`https://app.clickup.com/t/9006076935/VL-XXXXX`).

Se não: apresente o Markdown final pronto para colar.

**Status inicial sugerido:** Roadmap Item → `considering` ou `prioritized` (pergunte se já está priorizado); Discovery → `to do`; Delivery → `backlog` na lista `Backlog de Delivery` (default) ou `to-do` na `Execução` se for exceção prioritária.

**2. Custom fields (Roadmap Item)** — após criar, confirme antes de gravar:
> "Quer que eu grave os campos de priorização? RICE ≈ [valor] (R [x] · I [y] · C [z]% · E [w]), Horizonte [Now/Next/Later], MoSCoW [..], Squad [..], _Projeto [..]."

Só grave após o "sim". Use os IDs de [references/clickup-config.md](references/clickup-config.md).

**3. Vínculo** — vincule o item ao nível acima/abaixo via `clickup_add_task_link` (pertencimento) e, **sempre que vincular Discovery/Delivery a um Roadmap Item, atualize também a seção 🗂️ Portfólio de Projetos do Roadmap Item** no formato `Nome (https://app.clickup.com/t/9006076935/VL-XXXXX)` — uma linha por projeto, com a URL completa, que o ClickUp renderiza como task-link interativo (status + responsável). Use `clickup_add_task_dependency` apenas quando houver ordem real (alimenta Gantt). Detalhe e guardrail em [references/clickup-method.md](references/clickup-method.md) → "Vínculos entre níveis".

**4. Update (comentário)** — pergunte se deve postar um comentário-update narrativo (contexto → decisão → próximo passo). Modelos em [references/clickup-method.md](references/clickup-method.md). Confirme o rascunho antes de postar.

---

## Fluxo: PROMOTE

`/clickup-spec promote [ID ou nome parcial]` — converte um Discovery concluído em um novo Projeto de Delivery.

### Passo 1: Buscar o Discovery
Busque por custom ID (`VL-XXXXX`) ou nome (`clickup_get_task` / `clickup_search`). Extraia: objetivo, contexto, questões em aberto, **critérios de saída**, links, Roadmap Item pai.

**Edge cases:**
- **Nome ambíguo** → liste candidatos e peça confirmação.
- **ID não encontrado** → peça confirmação ou nome alternativo.
- **Já está no folder Delivery** → avise e encerre (não promove um Delivery).
- **Critérios de saída com itens abertos** → alerte:
  > "⚠️ Os critérios de saída do Discovery ainda têm itens abertos. Recomendo concluí-los antes de promover. Quer continuar mesmo assim?"

### Passo 2: Diagnóstico de gaps
Compare o Discovery com o que o template de Delivery exige. Peça só o que falta: critérios de aceite micro por área funcional, escopo em linguagem de capacidade, link do Figma.

### Passo 3: Gerar Projeto de Delivery
Pré-preencha com os dados do Discovery. Campo **Discovery:** aponta para a task de origem. Apresente para aprovação, depois:
> "Posso criar este Projeto de Delivery no ClickUp agora?"

Se sim → crie na lista **`Backlog de Delivery`** (status `backlog`; é o destino padrão de todo Delivery promovido — não nasce em Execução nem em lista nova), `clickup_create_task`, e **vincule os três níveis** com `clickup_add_task_link`: Delivery ↔ Discovery (origem) e Delivery ↔ Roadmap Item (pai). **Atualize a seção 🗂️ Portfólio de Projetos do Roadmap Item** com o novo Delivery no formato `Nome (https://app.clickup.com/t/9006076935/VL-XXXXX)` (task-link interativo — ver clickup-method). Retorne o link.

### Passo 4: Updates duplos (comentários)
Sugira dois comentários e pergunte se deseja postar ambos, um, ou nenhum:
- **No Discovery**: "Discovery concluído" + decisões tomadas + Delivery(s) gerado(s).
- **No Roadmap Item**: momento + próximos passos. Modelos em [references/clickup-method.md](references/clickup-method.md).

Considere também atualizar o **status** e o **Phase** do Roadmap Item (ex: `scoping`/Design Spec → `in design`) — confirme antes.

---

## Fluxo: VALIDATE

### Passo 1: Identificar e buscar
Peça o ID/nome. `clickup_get_task` (com `detail_level: detailed`). Se não encontrado, peça confirmação ou que o usuário cole título+descrição para análise offline.

### Passo 2: Analisar (checklists por tipo)

**Roadmap Item**

| Critério | Status |
|----------|--------|
| Título imperativo com valor de negócio? | ✅/❌ |
| Visão/Objetivo claros? | ✅/❌ |
| Métricas com baseline e meta (KPI + guard-rail)? | ✅/❌ |
| Portfólio de Projetos mapeado e vinculado? | ✅/❌ |
| Dependências externas documentadas? | ✅/❌ |
| Priorização preenchida (RICE/MoSCoW/Horizonte/Squad/_Projeto)? | ✅/❌ |
| Dono (assignee) nomeado? | ✅/❌ |

**Projeto de Discovery**

| Critério | Status |
|----------|--------|
| Título imperativo? | ✅/❌ |
| Vinculado a um Roadmap Item? | ✅/❌ |
| Sub-tipo declarado (Pesquisa / Definição de Escopo / Prototipação / Design Ops)? | ✅/❌ |
| Objetivo claro + Critérios de saída definidos? | ✅/❌ |
| Seções presentes são as relevantes ao contexto (sem seções vazias/genéricas)? | ✅/❌ |
| Se Prototipação: protótipo é no **Figma** e há **decisões de UX em aberto** listadas? | ✅/❌/NA |
| JTBD / Personas / Evidências presentes **quando há informação** (não inventados)? | ✅/❌/NA |
| Dono nomeado? | ✅/❌ |

**Projeto de Delivery**

| Critério | Status |
|----------|--------|
| Título imperativo com valor? | ✅/❌ |
| Vinculado a Roadmap Item (e Discovery, se houver)? | ✅/❌ |
| Escopo em linguagem de capacidade ("Usuário consegue…")? | ✅/❌ |
| "Fora de escopo" explícito? | ✅/❌ |
| Critérios de aceite por área funcional, binários e testáveis? | ✅/❌ |
| Dono nomeado? | ✅/❌ |

### Passo 3: Sugerir melhorias
```markdown
## Sugestões de Melhoria
### Título
- **Atual**: [..]
- **Sugerido**: [..]
- **Motivo**: [baseado nos princípios]
### Descrição / Estrutura
[sugestões específicas com justificativa]
### Campos
[campos vazios ou inconsistentes que valem preencher]
```

### Passo 4: Avaliação final e update
```markdown
## Avaliação Final
[🟢 Aprovado | 🟡 Ajustes menores | 🔴 Reescrever]
**Resumo**: [1-2 frases]
```
Se houver melhorias, pergunte se deve postar um comentário-update com o resumo.

---

## Fluxo: UPDATE

`/clickup-spec update [ID ou nome]` — posta um comentário narrativo comunicando um momento do ciclo de vida.

### Passo 1: Identificar item e momento
Se ID/nome dado → busque. Senão → pergunte qual task. Se o momento já está claro na mensagem, use-o; senão ofereça:
> 1. Pronto para refinamento · 2. Aprovado para delivery · 3. Discovery finalizado (sem promote) · 4. Entrou em delivery · 5. Bug encontrado em produção · 6. Outro (descreva)

### Passo 2: Gerar rascunho narrativo
Formato: **contexto → decisão/fato → próximo passo**. Modelos por momento em [references/clickup-method.md](references/clickup-method.md).

Para **Bug em produção**: primeiro crie a(s) task(s) de bug (subtipo via `_Classe` = Incidente ou `Tipo de Chamado`) vinculadas ao item, depois poste o comentário com os links.

### Passo 3: Confirmar e postar
Apresente o rascunho. Confirme a task de destino. `clickup_create_task_comment`. Se o momento implicar mudança de status/Phase, ofereça atualizar via `clickup_update_task`.

---

## Fluxo: HELP

Exiba:
1. A **hierarquia** Roadmap Item → Discovery → Delivery → subtask, com a pergunta de cada nível.
2. A **regra de ouro de títulos** com exemplos bons/ruins.
3. Os **anti-patterns** mais comuns ([references/anti-pattern.md](references/anti-pattern.md)).
4. A **Definição dos Folders** (Roadmap = iniciativas estratégicas ponta a ponta · Discovery = Design Ops, Pesquisa, Definição de Escopo e Prototipação · Delivery = escopo fechado, só execução) e as regras que decorrem dela — em especial: **prototipação é sempre Discovery e todo protótipo é no Figma**.
5. **Relação Discovery → Delivery**: Discovery não é pré-requisito obrigatório. Use Discovery quando há pesquisa, prototipação ou decisões de produto/UX em aberto; vá direto a Delivery quando o escopo está fechado e alinhado com dev. Com Discovery prévio, use `promote`.
6. **Quando NÃO criar um Projeto de Delivery**: se cabe em 1-2 dias, não tem fases/paralelismo e não envolve Designer nem múltiplos times → é uma **subtask** (ou item simples), não um projeto.
7. **Diferença vs. Linear**: o Roadmap Item é o contêiner estratégico; vínculos são por linked task; priorização (RICE/MoSCoW/Horizonte) vive no folder Roadmap.

---

## Guardrails

- **Macro, não micro.** O escopo é Roadmap Item, Discovery e Delivery. **Evite criar subtasks e tarefas micro** — a quebra fina (passos de implementação, checklist) é da squad/designer, não da spec de produto. Se a decomposição for inevitável, limite a poucas frentes macro (UCs principais, grandes frentes de build); nunca um item por micro-passo. Sinais de micro demais: cabe em < 1 dia, é passo técnico isolado, ou não tem valor de usuário próprio → use **checklist na tarefa-pai**, não subtask.
- **Vínculo sempre espelhado no corpo.** Nunca crie um linked task sem atualizar a seção 🗂️ Portfólio do Roadmap Item.
- **Linked task ≠ dependência.** Pertencimento é `add_task_link`; ordem/bloqueio é `add_task_dependency`. Não troque um pelo outro.
- **Não usar** *Tasks in Multiple Lists* nem o campo *Relationship* — decisão de modelagem para manter o vínculo simples.
- Três ações exigem **confirmação explícita**: criar task, gravar custom fields de priorização, postar comentário.

## Referência Técnica: Tratamento de Argumentos

- `$ARGUMENTS` contém tudo após `/clickup-spec`.
- Primeiro argumento: comando (create/promote/validate/update/help).
- Seguintes: parâmetros (ID `VL-XXXXX` ou nome parcial).

Exemplos:
- `/clickup-spec create` → diagnóstico interativo
- `/clickup-spec promote VL-11235` → buscar e converter o Discovery
- `/clickup-spec promote "KYC"` → buscar por nome parcial
- `/clickup-spec validate VL-11852` → validar o Roadmap Item
- `/clickup-spec` (sem args) → perguntar a intenção

---

## Referências

| Arquivo | Conteúdo |
|---------|----------|
| [references/clickup-config.md](references/clickup-config.md) | IDs reais: space, folders, listas, custom fields, status, option IDs |
| [references/clickup-method.md](references/clickup-method.md) | Método, automação de campos (RICE/MoSCoW/Horizonte), modelos de update |
| [references/dicionario.md](references/dicionario.md) | Regra de ouro de títulos, dicionário de verbos, formatação |
| [references/anti-pattern.md](references/anti-pattern.md) | Anti-patterns em títulos e descrições |
| [references/template-roadmap.md](references/template-roadmap.md) | Template e exemplo real de Roadmap Item |
| [references/template-discovery.md](references/template-discovery.md) | Template e exemplo real de Projeto de Discovery |
| [references/template-delivery.md](references/template-delivery.md) | Template e exemplo real de Projeto de Delivery |
