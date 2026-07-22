# Método ClickUp — Hierarquia, Automação de Campos e Updates

## Princípios

1. **Direção significativa**: o Objetivo lembra a todos o porquê de longo prazo. Todo Discovery/Delivery responde a um Objetivo.
2. **Specs, não user stories**: brevidade. Comunique "porquê", "o quê" e "como" com eficiência.
3. **Donos nomeados**: assignee em todo item.
4. **Decida e avance**: nem sempre há resposta perfeita; o que importa é decidir e manter momentum.
5. **O Designer/Eng cria as próprias subtasks**: o PM cria o contexto (Discovery/Delivery); o time quebra conforme descobre.
6. **O vínculo é explícito**: sem parent nativo cross-folder, todo item referencia o nível acima por linked task **e** no corpo.
7. **Sem jargão de engenharia em nomes e corpos de cards**: os itens são lidos por produto, design e operação — títulos e seções autoexplicativos (ex.: "Estrutura base e pontos de entrada", não "Shell"). Termo técnico só quando o público é engenharia, e explicado na primeira ocorrência.
8. **Fonte única é o ClickUp**: a spec vive no card — não se cria PRD paralelo no Drive (Linear method: a spec acompanha o trabalho). Conhecimento durável de domínio (glossário, sistemas, personas, métricas, decisões estruturais) vai para o context pack no claude-os via agente `curador-de-contexto`; no Drive vivem apenas artefatos não-spec (decks, planilhas de dados), sempre linkados do card.
9. **Fronteira PM ↔ Dados na medição**: o PM é dono da **intenção de medição** — qual evento existe, de qual épico vem e qual métrica ele alimenta; declara isso na área de Instrumentação dos critérios de aceite do épico. O **schema técnico** (nome final do evento, propriedades, tipos, arquivo versionado, testes) é de **Dados/Eng**. O Plano de Medição da iniciativa é **derivado** dos épicos pelo `clickup-rollup` (não é documento novo nem escrito à mão) e serve de handoff a Dados.

## Mapa da hierarquia

| Nível | ClickUp (Vertical Tech) |
|-------|--------------------------|
| Objetivo | **Marco OKR / Resultado-chave KR** (folder Roadmap, lista Objetivos) — ciclo de metas |
| Discovery | **Projeto de Discovery** (folder Discovery & Design, lista Discovery) — Pesquisa, Prototipação, Entrevista, Definição de Escopo; escopo orientado, não fechado |
| Delivery | **Projeto de Delivery** (folder Delivery do Squad correto) — escopo fechado, só execução; nasce no Backlog, migra para Execução na sprint |
| Subtarefa | **Subtask** sob o item pai (UC, edge case, build) |
| Update | **Comentário** na task (`clickup_create_task_comment`) |

## Definição dos folders (fluxo canônico)

| Folder | Propósito | O que vive aqui |
|--------|-----------|-----------------|
| **Roadmap** | Ciclo de metas (OKRs) | **Objetivos** (Marcos OKR + KRs) |
| **Discovery & Design** | **Pesquisa, Definição de Escopo e Prototipação** | Projetos de escopo **orientado, não fechado**: pesquisa, entrevistas, protótipos navegáveis |
| **Delivery: Experiência do jogador** | Escopo **fechado** — squad PAM | Épicos, bugs, tarefas de produto voltados ao jogador |
| **Delivery: Operação e afiliados** | Escopo **fechado** — squad Backoffice | Épicos, bugs, tarefas de backoffice e afiliados |
| **Delivery: Provedora de conteúdo** | Escopo **fechado** — squad Jogos | Épicos, bugs, integrações de provedoras |

**Regras decorrentes (a `clickup-spec` sempre segue):**

- **Prototipação é sempre Discovery** — nunca Delivery, mesmo com escopo bem orientado.
- **Todo protótipo é no Figma** — Discovery de prototipação produz protótipo navegável no Figma, jamais HTML/código.
- **Delivery é só execução** — se ainda há decisão de produto/UX, é Discovery.
- **O folder de Delivery correto é determinado pelo Squad responsável**: Experiência do jogador → folder PAM; Operação e afiliados → folder Backoffice; Provedora de conteúdo → folder Jogos. Sempre confirmar o Squad antes de criar o Delivery.
- **Delivery nasce no Backlog** (status `backlog`): refinado e priorizado, pronto para sprint. Migra para **Execução** ao entrar na sprint. Nunca criar listas novas nos folders.
- **Template de Discovery é adaptativo** — JTBD, Personas, Evidências e demais seções entram só quando há informação/relevância; na dúvida, perguntar (ver [template-discovery.md](template-discovery.md)).
- **Todo Projeto de Delivery segue o [template-delivery.md](template-delivery.md)** — com critérios de aceite propostos pelo PM antes do refinamento (áreas padrão de Qualidade e Instrumentação); épico não nasce sem eles.

## Vínculos entre níveis

Não há parent nativo cruzando folders. Três mecanismos, **cada um para um propósito** — não são concorrentes:

| Mecanismo | Tool | Quando usar |
|-----------|------|-------------|
| **Linked task** ("relacionado") | `clickup_add_task_link` | Vínculo de **pertencimento**, sempre presente: toda tarefa de Discovery/Delivery → seu Objetivo (quando houver); toda Delivery → seu Discovery de origem. É o vínculo-base. |
| **Dependência** (`waiting_on` / `blocking`) | `clickup_add_task_dependency` | **Apenas** quando há ordem real (uma tarefa espera ou bloqueia outra). Alimenta as views Gantt/Timeline do folder Roadmap. Nunca use no lugar do linked task de pertencimento. |
| **Subtask** (parent-child) | campo `parent` no `clickup_create_task` | Decomposição **macro** dentro da mesma lista. Usar com parcimônia — ver guardrail abaixo. |

Decisão de modelagem: **não usamos** *Tasks in Multiple Lists* nem o campo *Relationship*. O vínculo fica
simples e legível — linked task (sistema) + Portfólio no corpo (humano).

### Boa prática — espelhar sempre no Portfólio
Sempre que vincular uma tarefa de **Discovery ou Delivery** a um **Objetivo** por linked task, **atualize
também a seção 🗂️ Portfólio de Projetos do Objetivo**. O linked task dá o vínculo de sistema; o Portfólio é
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
- O escopo da `clickup-spec` é **macro**: Objetivo, Discovery e Delivery. Mantenha tarefas no nível de projeto/aposta.
- **Evite criar subtasks e tarefas micro.** A quebra fina (passos de implementação, itens de checklist) é da squad/designer, não da spec de produto.
- Se a decomposição for inevitável, limite a **poucas frentes macro** (ex: UCs principais, grandes frentes de build) — nunca um item por micro-passo.
- Sinais de que virou micro demais: cabe em < 1 dia, é um passo técnico isolado, ou não tem valor de usuário próprio. Nesse caso, use **checklist dentro da tarefa-pai**, não uma subtask.

## Priorização de itens de Delivery

### Score de Priorização

`Score = (Impacto × Votos × Alcance) / T-Shirt-Size`

O campo **Score** é calculado automaticamente pela IA do ClickUp — nunca setar manualmente. Para orientar a priorização, proponha os valores de entrada:

- **Impacto** (magnitude): 3 = muito alto · 2 = alto · 1 = médio · 0.5 = baixo · 0.25 = mínimo
- **Alcance** (guardrail: **sempre em % da base afetada**, 0–100 — nunca número absoluto de usuários; ex.: 100 = toda a base)
- **T-Shirt Sizing** (esforço): 1 = dias · 2 = 1-2 semanas · 3 = 3-4 semanas · 4 = 1-2 meses · 5 = múltiplos ciclos
- **Votos**: votação do time (estrelas) — setados ao vivo no ClickUp; não via API

Apresente assim:
> "Score estimado ≈ [(Impacto [x]) × (Alcance [y]) × (Votos estimados [z])] / (T-Shirt [w]). Impacto [x] porque [evidência]."

### Horizonte (Now / Next / Later)
- **Now**: em execução neste quarter, escopo claro.
- **Next**: próximo na fila, escopo quase fechado.
- **Later**: aposta reconhecida, sem escopo ou prazo definido.

### Outros campos
- **Empresa**: Tradicional, Bravo, Vertical — obrigatório nos Épicos/Tarefas quando aplicável.
- **Squad**: Experiência do jogador / Operação e afiliados / Provedora de conteúdo — determina o folder de Delivery.
- **KPIs** (eixo): Compliance, Conversão, Eficiência Operacional, Receita, Retenção, Satisfação, Segurança.
- **Data de Início / Conclusão Prevista**: use quando houver comprometimento de prazo.

## Completude de Campos — Política "Nenhum Campo Vazio Inferível"

Ao criar ou atualizar qualquer item, **preencha todos os campos que a informação disponível permite inferir** — nunca deixe campo em branco quando o valor pode ser derivado do contexto.

**Campos obrigatórios por nível:**

| Nível | Campos obrigatórios | Campos a inferir |
|-------|---------------------|-----------------|
| Objetivo (OKR/KR) | assignee, tipo=`Marco (OKR)` ou `Resultado-chave (KR)`, período/ciclo | — |
| Discovery | assignee, `_Projeto`, `_Classe`, tipo correto, status=`to do`, linked task com Objetivo (quando houver) | `_Risco Reg.` se houver exposição regulatória |
| Delivery | assignee, `_Projeto`, `_Classe`, tipo correto (Épico / Tarefa / Bug / Correção), status inicial correto, linked tasks com Objetivo e Discovery (quando houver) | `_Risco Reg.` se houver exposição regulatória |
| Objetivo / KR | assignee, tipo=`Marco (OKR)` ou `Resultado-chave (KR)`, período/ciclo | — |
| Ticket operacional | assignee, `_Projeto`, `_Classe` | `_Risco Reg.` se aplicável |

**Regra de operação:**
- Se um campo obrigatório não pode ser inferido → pergunte antes de criar, não crie com campo vazio.
- Se um campo enriquecedor pode ser inferido com razoável confiança → preencha e explique o raciocínio; o usuário pode corrigir.
- Após criar, liste os campos preenchidos automaticamente e os que ficaram em aberto — não deixe o usuário adivinhar o que foi ou não gravado.

## Modelos de Update (comentários narrativos)

Formato padrão: **contexto → decisão/fato → próximo passo**. Curtos e escaneáveis.

**Objetivo criado**
```
[Nome do Objetivo] — [Ciclo/Quarter]

[1 parágrafo: o que queremos alcançar e o porquê de agora]

Projetos vinculados:
- [Discovery/Delivery 1 — objetivo em uma linha]
- [...]

Próximo passo: [primeiro Discovery ou ação concreta].
```

**Discovery iniciado** (comentar no Objetivo, quando houver)
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

[Objetivo e quarter de referência]
```

**Delivery iniciado** (comentar no Objetivo, quando houver)
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

Ao postar updates, ofereça atualizar o status dos itens via `clickup_update_task`:

| Momento | Status Discovery | Status Delivery |
|---------|------------------|-----------------|
| Discovery iniciado | `to do` | — |
| Discovery em progresso | `em progresso` | — |
| Discovery concluído | `complete` | — |
| Delivery iniciado | — | `backlog` |
| Em desenvolvimento | — | `em desenvolvimento` |
| Em homologação | — | `em homologação` |
| Deploy realizado | — | `finalizado` / `concluido` |
| Descartado | `complete` | `cancelado` |
