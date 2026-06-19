# Método ClickUp — Hierarquia, Automação de Campos e Updates

## Princípios

1. **Direção significativa**: o Roadmap Item lembra a todos o porquê de longo prazo. Todo Discovery/Delivery responde a um Roadmap Item.
2. **Specs, não user stories**: brevidade. Comunique "porquê", "o quê" e "como" com eficiência.
3. **Donos nomeados**: assignee em todo item.
4. **Decida e avance**: nem sempre há resposta perfeita; o que importa é decidir e manter momentum.
5. **O Designer/Eng cria as próprias subtasks**: o PM cria o contexto (Discovery/Delivery); o time quebra conforme descobre.
6. **O vínculo é explícito**: sem parent nativo cross-folder, todo item referencia o nível acima por linked task **e** no corpo.

## Mapa da hierarquia (vs. Linear)

| Linear | ClickUp (Vertical Loto) |
|--------|--------------------------|
| Iniciativa | **Roadmap Item** (folder Product Roadmap) — Visão, Métricas, Portfólio, Dependências; percorre todo o ciclo de status |
| Projeto de Discovery | **Projeto de Discovery** (folder Product Discovery, lista Design) — Design Ops, Pesquisa, Definição de Escopo e Prototipação; escopo orientado, não fechado |
| Projeto de Delivery | **Projeto de Delivery** (folder Product Delivery) — escopo fechado, alinhado com dev só para execução |
| Issue / Milestone | **Subtask** sob o item pai (UC, edge case, build) |
| Activity Update | **Comentário** na task (`clickup_create_task_comment`) |

## Definição dos folders (fluxo canônico)

| Folder | Propósito | O que vive aqui |
|--------|-----------|-----------------|
| **Product Roadmap** | Visão geral de iniciativas estratégicas de ponta a ponta | Apostas estratégicas: Visão, Métricas, Portfólio, Dependências, priorização |
| **Product Discovery** | **Design Ops, Pesquisa, Definição de Escopo e Prototipação** | Projetos de escopo **orientado, não fechado**: pesquisa, JTBD/personas, definição de escopo, protótipos navegáveis |
| **Product Delivery** | Escopo **fechado**, alinhado com a engenharia só para **execução** | Specs de build: capacidades + critérios de aceite testáveis, sem decisões de produto/UX em aberto |

**Regras decorrentes (a `clickup-spec` sempre segue):**

- **Prototipação é sempre Discovery** — nunca Delivery, mesmo com escopo bem orientado.
- **Todo protótipo é no Figma** — Discovery de prototipação produz protótipo navegável no Figma, jamais HTML/código. O protótipo resolve as **decisões de UX em aberto** e fecha o escopo antes do Delivery.
- **Delivery é só execução** — se ainda há decisão de produto/UX, é Discovery.
- **Delivery nasce no `Backlog de Delivery`** (`901113940183`, status `backlog`): refinado e priorizado, pronto para sprint. Migra para **`Execução`** (`901113940182`) ao entrar na sprint; exceção = tarefa prioritária criada direto em `Execução`. **Nunca** usar a lista legada "Delivery" (`901113980144`, vazia) nem criar listas novas no folder.
- **Template de Discovery é adaptativo** — JTBD, Personas, Evidências e demais seções entram só quando há informação/relevância; na dúvida, perguntar (ver [template-discovery.md](template-discovery.md)).

## Vínculos entre níveis

Não há parent nativo cruzando folders. Três mecanismos, **cada um para um propósito** — não são concorrentes:

| Mecanismo | Tool | Quando usar |
|-----------|------|-------------|
| **Linked task** ("relacionado") | `clickup_add_task_link` | Vínculo de **pertencimento**, sempre presente: toda tarefa de Discovery/Delivery → seu Roadmap Item; toda Delivery → seu Discovery de origem. É o vínculo-base. |
| **Dependência** (`waiting_on` / `blocking`) | `clickup_add_task_dependency` | **Apenas** quando há ordem real (uma tarefa espera ou bloqueia outra). Alimenta as views Gantt/Timeline do folder Roadmap. Nunca use no lugar do linked task de pertencimento. |
| **Subtask** (parent-child) | campo `parent` no `clickup_create_task` | Decomposição **macro** dentro da mesma lista. Usar com parcimônia — ver guardrail abaixo. |

Decisão de modelagem: **não usamos** *Tasks in Multiple Lists* nem o campo *Relationship*. O vínculo fica
simples e legível — linked task (sistema) + Portfólio no corpo (humano).

### Boa prática — espelhar sempre no Portfólio
Sempre que vincular uma tarefa de **Discovery ou Delivery** a um **Roadmap Item** por linked task, **atualize
também a seção 🗂️ Portfólio de Projetos do Roadmap Item**. O linked task dá o vínculo de sistema; o Portfólio é
o índice legível e a fonte de verdade humana. **Os dois andam juntos — nunca crie o vínculo sem atualizar o
corpo** (vale para `create` e `promote`).

**Formato do Portfólio (task-link interativo):** cada projeto é **uma linha** com o **nome da tarefa seguido da
URL completa entre parênteses**. O ClickUp detecta a URL e a renderiza como **componente interativo** — mostra
**status e responsável** ao vivo e permite mudar o status dali. Use a URL completa com o workspace ID:

```
Nome da Tarefa (https://app.clickup.com/t/9006076935/VL-XXXXX)
Outro Projeto (https://app.clickup.com/t/9006076935/VL-YYYYY)
```

> **Não** use checkbox (`- [ ]`), prefixo `[Discovery]/[Delivery]` nem `VL-XXXXX` solto: sem a URL completa o
> texto fica estático e não vira componente. O card já exibe o status — não escreva status à mão. (Referência
> viva do padrão: VL-11852.)

### Guardrail — macro, não micro
- O escopo da `clickup-spec` é **macro**: Roadmap Item, Discovery e Delivery. Mantenha tarefas no nível de projeto/aposta.
- **Evite criar subtasks e tarefas micro.** A quebra fina (passos de implementação, itens de checklist) é da squad/designer, não da spec de produto.
- Se a decomposição for inevitável, limite a **poucas frentes macro** (ex: UCs principais, grandes frentes de build) — nunca um item por micro-passo.
- Sinais de que virou micro demais: cabe em < 1 dia, é um passo técnico isolado, ou não tem valor de usuário próprio. Nesse caso, use **checklist dentro da tarefa-pai**, não uma subtask.

## Automação de Custom Fields (Roadmap Item)

Política: **sugerir e preencher com confirmação**. Proponha valores derivados do contexto, mostre a
justificativa, grave só após o "sim". IDs e option IDs em [clickup-config.md](clickup-config.md).

### RICE
`RICE = (Reach × Impact × Confidence%) / Effort`

- **Reach**: nº de usuários/eventos por período (ex: cadastros/mês afetados). Use dados do funil se houver.
- **Impact (1-5)**: 5 = massivo, 3 = alto, 1 = baixo.
- **Confidence % (0-100)**: quão sustentada por evidência está a estimativa. Com dados fortes → 80-100; hipótese → 50; chute → ≤30.
- **Effort (1-5)**: 1 = trivial, 5 = vários ciclos de squad.

Apresente assim:
> "RICE ≈ **[valor]** — Reach [x] · Impact [y] · Confidence [z]% · Effort [w]. Confiança [z]% porque [evidência]."

### Horizonte (Now / Next / Later / Considering)
- **Now**: em execução neste quarter, escopo claro.
- **Next**: próximo na fila, escopo quase fechado.
- **Later**: aposta reconhecida, sem escopo.
- **Considering**: ainda em avaliação, pode não acontecer.

### MoSCoW
Must / Should / Could / Would — relativo ao objetivo do quarter. Justifique o porquê do nível.

### Outros
- **_Projeto** (marca): Tradicional, Bravo, Blow, NGX, Plug n Play, Cactus, Loteria 2.0 — obrigatório no Roadmap.
- **Squad**: PAM, Loteria, Novos produtos, Integrações.
- **Impacto** (eixo): Receita/Conversão, Retenção, UX, Eficiência Operacional, Compliance, Risco/Fraude.
- **Phase**: Research → Ideation → Design Spec → Implementation → Review → Complete (acompanha o estágio do trabalho).
- **Initiative**: confirme se o time renomeou as opções genéricas do template antes de setar.
- **_Risco Reg.** (number): use quando houver exposição regulatória (bets BR) — alinhe com o agente `regulatory-watch`.

> Em **Discovery** e **Delivery**, não tente setar RICE/MoSCoW/Horizonte/Squad — esses campos só existem no
> folder Roadmap. A priorização vive no Roadmap Item pai.

## Modelos de Update (comentários narrativos)

Formato padrão: **contexto → decisão/fato → próximo passo**. Curtos e escaneáveis.

**Roadmap Item criado**
```
[Nome do item] — [Horizonte/Quarter]

[1 parágrafo: a aposta e o porquê de agora]

Portfólio inicial:
- [Discovery/Delivery 1 — objetivo em uma linha]
- [...]

Próximo passo: [primeiro Discovery ou ação concreta].
```

**Discovery iniciado** (comentar no Roadmap Item)
```
Discovery iniciado: [Nome]

[1 parágrafo: problema central e o que o discovery precisa responder]

Questões em aberto:
- [questão 1]

Próximo passo: [primeira subtask / validação].
```

**Discovery concluído** (comentar no Discovery)
```
Discovery concluído. [O que foi validado — 1 frase].

O que foi decidido:
- [decisão 1]

Projetos de Delivery gerados:
- [nome]

[Roadmap Item e quarter de referência]
```

**Delivery iniciado** (comentar no Roadmap Item)
```
Delivery iniciado: [Nome]

[1 parágrafo: o que será construído e por quê]

Escopo do build:
- [capacidade 1 — linguagem de usuário]

Próximo passo: [refinamento com engenharia / primeira subtask].
```

**Bug em produção** (após criar as tasks de bug)
```
[N] bug(s) em produção — [descrição curta].

[1 parágrafo: impacto, quem é afetado, quando foi identificado]

Tasks criadas:
- [título] → [link VL-XXXXX]

Status: [em investigação / causa-raiz identificada / correção em andamento]
Próximo passo: [ação + prazo].
```

## Transições de status sugeridas

Ao postar updates, ofereça atualizar o status do Roadmap Item via `clickup_update_task`:

| Momento | Status Roadmap | Phase |
|---------|----------------|-------|
| Aposta aceita, sem escopo | `considering` / `prioritized` | Research / Ideation |
| Discovery em andamento | `scoping` | Design Spec |
| Delivery aprovado, em build | `in development` | Implementation |
| Em QA | `in qa review` | Review |
| Pronto para deploy | `ready for deployment` | Complete |
| Descartado | `not doing` | — |
