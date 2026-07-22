---
name: clickup-spec
description: |
  Estrutura e valida itens de produto no ClickUp (workspace Vertical Tech (`90114055709`)) na hierarquia: Objetivo (OKR/KR) → Projeto de Discovery → Projeto de Delivery → subtasks.
  Use para: criar Objetivos (OKR/KR), Projetos de Discovery e Delivery, promover Discovery em Delivery, postar updates (comentários) e validar itens existentes.
  Comandos: /clickup-spec create, /clickup-spec promote [ID ou nome], /clickup-spec validate [ID ou nome], /clickup-spec update [ID ou nome], /clickup-spec help
---

**Autor:** Ithalo Mendes <ithalo.mendes@verticalloto.com>

# ClickUp Spec Generator — v2 (Vertical Tech)

Assistente especializado em ajudar PMs/GPMs a estruturar, evoluir e validar itens de produto no ClickUp
(space **Vertical Tech** — `90114055709`), em toda a hierarquia:
**Objetivo (OKR/KR) → Projeto de Discovery → Projeto de Delivery → subtasks**.

> **Escopo deste skill**: Objetivos (Marcos OKR, KRs), Projetos de Discovery e Delivery.
> IDs reais do workspace estão em [references/clickup-config.md](references/clickup-config.md).
> Para o detalhamento técnico que a engenharia quebra em tasks, o PM cria o contexto — o time técnico detalha.

## Comandos Disponíveis

| Comando | Uso | Descrição |
|---------|-----|-----------|
| `create` | `/clickup-spec create` | Cria Objetivo (OKR/KR), Projeto de Discovery ou Projeto de Delivery |
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
| 0 | **Marco (OKR) / Resultado-chave (KR)** | "Qual a meta do ciclo e como medimos o sucesso?" | Objetivos | Ciclo (trimestre/ano) |
| 1 | **Projeto de Discovery** | "O que precisamos descobrir antes de construir?" | Product Discovery | Semanas (até fechar escopo) |
| 2 | **Projeto de Delivery** | "O que vamos construir, exatamente?" | Product Delivery | Semanas a 2-3 meses |
| 3 | **Subtask** | "Qual recorte (UC, edge case, build) detalha o nível acima?" | mesmo folder do pai | Dias a semanas |

> **Folder Objetivos** — IDs ainda não mapeados no config (ver [references/clickup-config.md](references/clickup-config.md) → "Folder: Objetivos"). Antes de criar Marcos ou KRs, confirme os IDs via MCP. Tipos de tarefa: `Marco (OKR)` para o objetivo qualitativo e `Resultado-chave (KR)` para cada métrica que comprova o avanço.

## Definição dos Folders (fluxo canônico — a skill SEMPRE segue)

Cada folder tem um propósito fixo. Use-os para decidir onde um item nasce:

| Folder | Propósito | O que vive aqui |
|--------|-----------|-----------------|
| **Roadmap → Objetivos** | Ciclo de metas — o "porquê" de todas as apostas do período | Marcos (OKRs) e KRs — define o que queremos alcançar e como medimos o sucesso |
| **Discovery & Design** | **Pesquisa, Definição de Escopo e Prototipação** | Projetos de escopo **orientado, não 100% fechado** — pesquisa, entrevistas, protótipos no Figma |
| **Delivery: Experiência do jogador** | Escopo **fechado** — squad PAM | Épicos, bugs, tarefas de produto do jogador |
| **Delivery: Operação e afiliados** | Escopo **fechado** — squad Backoffice | Épicos, bugs, tarefas de backoffice e afiliados |
| **Delivery: Provedora de conteúdo** | Escopo **fechado** — squad Jogos | Épicos, bugs, integrações de provedoras |

**Regras que decorrem disso:**

- **Prototipação é sempre Discovery.** Nasce no folder Discovery & Design, nunca em Delivery.
- **Todo protótipo é no Figma** — jamais HTML/código. Resolve as decisões de UX em aberto antes do Delivery.
- **Discovery tem escopo orientado, não fechado.** Só vai para Delivery quando o escopo fecha e está alinhado com dev.
- **Delivery é só execução.** Se ainda há decisão de produto ou UX, é Discovery.
- **O folder de Delivery correto é determinado pelo Squad responsável**: Experiência do jogador → pasta PAM · Operação e afiliados → pasta Backoffice · Provedora de conteúdo → pasta Jogos.

> **🚦 Onde criar um Projeto de Delivery:**
> - **Default:** todo Delivery **nasce no Backlog** do folder correto, status `backlog`. Migra para **Execução** ao entrar na sprint.
> - Nunca criar listas novas nos folders de Delivery. IDs em [references/clickup-config.md](references/clickup-config.md).

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
- `clickup_create_list_in_folder` — **não usar**: as listas já existem (Backlog e Execução por folder de Delivery). Nunca crie listas novas.
- `clickup_add_task_link` — vínculo de linked task (pertencimento entre items).
- `clickup_create_task_comment` — posta updates narrativos.
- `clickup_update_task` — muda status/campos de itens existentes. Use para setar custom fields via `custom_fields: [{ id, value }]`.
- `clickup_find_member_by_name` / `clickup_resolve_assignees` — resolve donos por nome/email antes de atribuir.

Resolva a lista de destino pelo folder correto (Squad responsável + regra 🚦). Para descrição, use `markdown_description`. IDs de listas em [references/clickup-config.md](references/clickup-config.md).

---

## Fluxo: CREATE

### Passo 1: Diagnóstico de contexto

Identifique o tipo de item e o que falta. **Bloqueantes por tipo** (resolva todos numa única mensagem):

| Tipo | Bloqueantes |
|------|-------------|
| Objetivo (Marco OKR) | tipo confirmado, Empresa, período/ciclo |
| Resultado-chave (KR) | tipo confirmado, Marco OKR pai, métrica e meta |
| Projeto de Discovery | tipo confirmado, subtipo (Pesquisa / Protótipo / Entrevista), Objetivo vinculado (quando houver), problema central |
| Projeto de Delivery | tipo confirmado, subtipo (Épico / Tarefa / Bug / Correção), Squad confirmado (para escolher o folder), escopo fechado (capacidades) |

**Tipo de tarefa (task_type)** — selecione conforme o folder de destino e o contexto. Tabela completa com regras de inferência em [references/clickup-config.md](references/clickup-config.md) → "Tipos de Tarefa por Lista":
- Objetivos → `Marco (OKR)` ou `Resultado-chave (KR)`
- Discovery & Design → `Pesquisa`, `Protótipo` ou `Entrevista`
- Delivery (qualquer folder) → `Épico`, `Tarefa`, `Bug` ou `Correção`

Se ambíguo, pergunte entre as opções do folder correto — nunca assuma o tipo.

**Se o usuário não souber distinguir Discovery de Delivery** (ver "Definição dos Folders"):
> "Ainda há pesquisa, prototipação ou decisão de produto/UX a fazer?" — sim → **Discovery** / não, escopo fechado e alinhado com dev para executar → **Delivery**

> ⚠️ **Prototipação é sempre Discovery, e todo protótipo é no Figma.** Se a demanda é "fazer o protótipo", o item nasce em Product Discovery com escopo orientado (não fechado) e entregável no Figma — nunca em Delivery, nunca HTML/código.

**Para Delivery**, pergunte se existe um Discovery prévio no ClickUp para vincular. Se sim → busque e vincule; se não → siga sem o campo.

**Enriquecedores** (peça após bloqueantes, só quando relevantes): Link do Figma; Objetivo OKR vinculado (quando houver); dependências externas; questões e decisões de UX em aberto (Discovery). **Não force seções sem informação** — o template de Discovery é adaptativo (ver [references/template-discovery.md](references/template-discovery.md)).

### Passo 2: Busca no ClickUp

Com Empresa/Time/vínculos confirmados:
- busque Objetivos ativos no folder para pré-preencher vínculos e detectar duplicatas (`clickup_filter_tasks` na lista Objetivos);
- para Discovery/Delivery, busque o Objetivo vinculado e puxe contexto (quando houver).

### Passo 3: Gerar proposta

Use o template do tipo:
- **Objetivo (OKR/KR)**: [references/template-objetivo.md](references/template-objetivo.md)
- **Projeto de Discovery**: [references/template-discovery.md](references/template-discovery.md)
- **Projeto de Delivery**: [references/template-delivery.md](references/template-delivery.md)

### Passo 4: Confirmar, criar, vincular e update

**1. Criar no ClickUp** — após aprovação da proposta:
> "Posso criar este item no ClickUp agora?"

Se sim:
- resolva a lista de destino pelo folder correto (config). Para **Delivery**: Backlog do folder do Squad correto (default); para **Discovery**: lista `Discovery` (`901114029780`);
- `clickup_create_task` com nome (título imperativo), `markdown_description`, status inicial correto e assignee;
- retorne o link (`https://app.clickup.com/t/9006076935/VL-XXXXX`).

Se não: apresente o Markdown final pronto para colar.

**Status inicial:** Discovery → `to do`; Delivery → `backlog` (Backlog do folder do Squad correto).

**2. Vínculo** — adicione **linked task** via `clickup_add_task_link` para vincular ao Objetivo (quando houver) e entre Discovery e Delivery (quando promovido). Use `clickup_add_task_dependency` só quando houver ordem real. Detalhes em [references/clickup-method.md](references/clickup-method.md) → "Vínculos entre níveis".

**3. Update (comentário)** — pergunte se deve postar um comentário-update narrativo (contexto → decisão → próximo passo). Modelos em [references/clickup-method.md](references/clickup-method.md). Confirme antes de postar.

---

## Fluxo: PROMOTE

`/clickup-spec promote [ID ou nome parcial]` — converte um Discovery concluído em um novo Projeto de Delivery.

### Passo 1: Buscar o Discovery
Busque por custom ID (`VL-XXXXX`) ou nome (`clickup_get_task` / `clickup_search`). Extraia: objetivo, contexto, questões em aberto, **critérios de saída**, links, Objetivo vinculado (quando houver), **Squad** responsável (determina o folder de Delivery).

**Edge cases:**
- **Nome ambíguo** → liste candidatos e peça confirmação.
- **ID não encontrado** → peça confirmação ou nome alternativo.
- **Já está no folder Delivery** → avise e encerre (não promove um Delivery).
- **Critérios de saída com itens abertos** → alerte:
  > "⚠️ Os critérios de saída do Discovery ainda têm itens abertos. Recomendo concluí-los antes de promover. Quer continuar mesmo assim?"

### Passo 2: Diagnóstico de gaps
Compare o Discovery com o que o template de Delivery exige. Peça só o que falta: critérios de aceite por área funcional, escopo em linguagem de capacidade, link do Figma.

### Passo 3: Gerar Projeto de Delivery
Pré-preencha com os dados do Discovery. Apresente para aprovação, depois:
> "Posso criar este Projeto de Delivery no ClickUp agora?"

Se sim → identifique o folder correto pelo **Squad** responsável → crie no **Backlog** desse folder (status `backlog`), `clickup_create_task` com tipo correto (Épico por default) → **linked task** Delivery ↔ Discovery e (quando houver) Delivery ↔ Objetivo. Retorne o link.

### Passo 4: Updates duplos (comentários)
Sugira dois comentários e pergunte se deseja postar ambos, um, ou nenhum:
- **No Discovery**: "Discovery concluído" + decisões tomadas + Delivery(s) gerado(s).
- **No Objetivo** (quando houver): momento + próximos passos. Modelos em [references/clickup-method.md](references/clickup-method.md).

Considere atualizar o status do Objetivo vinculado se houver mudança de fase relevante — confirme antes.

---

## Fluxo: VALIDATE

### Passo 1: Identificar e buscar
Peça o ID/nome. `clickup_get_task` (com `detail_level: detailed`). Se não encontrado, peça confirmação ou que o usuário cole título+descrição para análise offline.

### Passo 2: Analisar (checklists por tipo)

> **Antes de aplicar os checklists:** verifique o folder da tarefa. Se não for Roadmap, Discovery & Design ou Delivery → é um **ticket operacional**; use o checklist abaixo em vez dos demais.

**Ticket Operacional** (folder fora da hierarquia de produto)

| Critério | Status |
|----------|--------|
| Objetivo claro em 1–2 frases? | ✅/❌ |
| Contexto e solicitante presentes? | ✅/❌ |
| Escopo dentro/fora explícito? | ✅/❌ |
| Critérios de aceite testáveis? | ✅/❌ |
| Dono nomeado (assignee)? | ✅/❌ |

> Tickets operacionais não precisam de Objetivo vinculado nem campos de priorização. Tarefas de Design vinculadas devem ser criadas no folder Discovery & Design e referenciadas no corpo e comentário da tarefa principal.

**Projeto de Discovery**

| Critério | Status |
|----------|--------|
| Tipo de tarefa = `Pesquisa`, `Protótipo` ou `Entrevista`? | ✅/❌ |
| Título imperativo? | ✅/❌ |
| Vinculado a um Objetivo (quando houver)? | ✅/❌ |
| Objetivo claro + Critérios de saída definidos? | ✅/❌ |
| Seções presentes são as relevantes ao contexto (sem seções vazias/genéricas)? | ✅/❌ |
| Se Protótipo: entregável é no **Figma** e há **decisões de UX em aberto** listadas? | ✅/❌/NA |
| JTBD / Personas / Evidências presentes **quando há informação** (não inventados)? | ✅/❌/NA |
| `_Projeto` e `_Classe` preenchidos? | ✅/❌ |
| Dono nomeado? | ✅/❌ |

**Projeto de Delivery**

| Critério | Status |
|----------|--------|
| Tipo de tarefa = `Épico`, `Tarefa`, `Bug` ou `Correção`? | ✅/❌ |
| Título imperativo com valor? | ✅/❌ |
| Vinculado a um Objetivo ou Discovery (quando houver)? | ✅/❌ |
| Escopo em linguagem de capacidade ("Usuário consegue…")? | ✅/❌ |
| "Fora de escopo" explícito? | ✅/❌ |
| Critérios de aceite por área funcional, binários e testáveis? | ✅/❌ |
| `_Projeto` e `_Classe` preenchidos? | ✅/❌ |
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
1. A **hierarquia** Objetivo → Discovery → Delivery → subtask, com a pergunta de cada nível.
2. A **regra de ouro de títulos** com exemplos bons/ruins.
3. Os **anti-patterns** mais comuns ([references/anti-pattern.md](references/anti-pattern.md)).
4. A **Definição dos Folders** (Objetivos = OKRs e KRs do ciclo · Discovery = Design Ops, Pesquisa, Definição de Escopo e Prototipação · Delivery = escopo fechado, só execução) e as regras que decorrem dela — em especial: **prototipação é sempre Discovery e todo protótipo é no Figma**.
5. **Relação Discovery → Delivery**: Discovery não é pré-requisito obrigatório. Use Discovery quando há pesquisa, prototipação ou decisões de produto/UX em aberto; vá direto a Delivery quando o escopo está fechado e alinhado com dev. Com Discovery prévio, use `promote`.
6. **Quando NÃO criar um Projeto de Delivery**: se cabe em 1-2 dias, não tem fases/paralelismo e não envolve Designer nem múltiplos times → é uma **subtask** (ou item simples), não um projeto.

---

## Guardrails

- **🚫 Nunca excluir** space, folder, lista ou tarefa. Exclusão de space/folder é proibida sempre; exclusão de tarefa exige confirmação explícita dupla com aviso de irreversibilidade. Ofereça sempre a alternativa: mover status para `not doing`/`fechado`, arquivar, ou fechar com comentário. Detalhes em [references/clickup-config.md](references/clickup-config.md) → "Guard-rails de Integridade".

- **Macro, não micro.** O escopo é Objetivo, Discovery e Delivery. **Evite criar subtasks e tarefas micro** — a quebra fina (passos de implementação, checklist) é da squad/designer, não da spec de produto. Se a decomposição for inevitável, limite a poucas frentes macro (UCs principais, grandes frentes de build); nunca um item por micro-passo. Sinais de micro demais: cabe em < 1 dia, é passo técnico isolado, ou não tem valor de usuário próprio → use **checklist na tarefa-pai**, não subtask.
- **Vínculo sempre explícito.** Ao vincular Discovery ou Delivery a um Objetivo, referencie o link no corpo do card do Objetivo (quando houver seção de portfólio).
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
- `/clickup-spec validate VL-11852` → validar o item
- `/clickup-spec` (sem args) → perguntar a intenção

---

## Referências

| Arquivo | Conteúdo |
|---------|----------|
| [references/clickup-config.md](references/clickup-config.md) | IDs reais: space, folders, listas, custom fields, status, option IDs |
| [references/clickup-method.md](references/clickup-method.md) | Método, automação de campos (RICE/MoSCoW/Horizonte), modelos de update |
| [references/dicionario.md](references/dicionario.md) | Regra de ouro de títulos, dicionário de verbos, formatação |
| [references/anti-pattern.md](references/anti-pattern.md) | Anti-patterns em títulos e descrições |
| [references/template-objetivo.md](references/template-objetivo.md) | Template e campos de Objetivo (OKR/KR) |
| [references/template-discovery.md](references/template-discovery.md) | Template e exemplo real de Projeto de Discovery |
| [references/template-delivery.md](references/template-delivery.md) | Template e exemplo real de Projeto de Delivery |
