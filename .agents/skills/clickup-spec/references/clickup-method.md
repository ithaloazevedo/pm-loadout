# Método ClickUp — Hierarquia, Sprints, Automação de Campos e Updates

> **Mudança estrutural em 2026-09-10**: sem nível Objetivo (OKR/KR) nem Discovery separado — ver
> `knowledge/domains/processo.md` e `knowledge/decisions/2026-09-10-migracao-esteira-continua-para-sprints-remocao-okr-e-discovery.md`.
> Este documento já reflete o modelo de sprints.

## Princípios

1. **Direção significativa**: sem Objetivo formal de ciclo, o Projeto de Delivery carrega seu próprio "porquê" no Contexto do card — Problema → Impacto → Solução conectado a um indicador de negócio (ver princípio 10).
2. **Specs, não user stories**: brevidade. Comunique "porquê", "o quê" e "como" com eficiência.
3. **Donos nomeados**: assignee em todo item.
4. **Decida e avance**: nem sempre há resposta perfeita; o que importa é decidir e manter momentum.
5. **O Designer/Eng cria as próprias subtasks**: o PM cria o contexto (o Projeto de Delivery); o time quebra conforme descobre.
6. **O vínculo é explícito quando existe**: não há mais nível acima do Delivery para referenciar por padrão — use linked task só quando houver uma relação pontual real (ex.: Bug que referencia o Épico afetado).
7. **Sem jargão de engenharia em nomes e corpos de cards**: os itens são lidos por produto, design e operação — títulos e seções autoexplicativos (ex.: "Estrutura base e pontos de entrada", não "Shell"). Termo técnico só quando o público é engenharia, e explicado na primeira ocorrência.
8. **Fonte única é o ClickUp**: a spec vive no card — não se cria PRD paralelo no Drive (Linear method: a spec acompanha o trabalho). Conhecimento durável de domínio (glossário, sistemas, personas, métricas, decisões estruturais) vai para o context pack no claude-os via agente `curador-de-contexto`; no Drive vivem apenas artefatos não-spec (decks, planilhas de dados), sempre linkados do card.
9. **Fronteira PM ↔ Dados na medição**: o PM é dono da **intenção de medição** — qual evento existe, de qual épico vem e qual métrica ele alimenta; declara isso na área de Instrumentação dos critérios de aceite do épico. O **schema técnico** (nome final do evento, propriedades, tipos, arquivo versionado, testes) é de **Dados/Eng**.
10. **Negócio antes de tecnologia**: todo Contexto segue Problema → Impacto → Solução, conectado a um indicador de negócio (conversão, receita, retenção, satisfação, eficiência operacional), com dado no lugar de adjetivo. Requisitos legais/regulatórios entram pela implicação prática em linguagem simples — nunca como citação jurídica extensa ou artigos encadeados. Estrutura e exemplos em [estilo-redacao.md](estilo-redacao.md).
11. **Especulação do agente não é conteúdo do card**: assim como o assignee (regra própria — nunca atribuído sem confirmação), **Links, 📜 Log de Decisões e ❓ Aberto para refinamento técnico só recebem itens confirmados pelo PM**. **Aberto para refinamento técnico é exclusiva de decisão técnica de engenharia** — pendência de produto/compliance/negócio é resolvida com PM + Orquestrador + agente especialista antes do card, não registrada ali (detalhe em [estilo-redacao.md](estilo-redacao.md)). — vindos de uma decisão já registrada (`knowledge/decisions/`) ou de confirmação explícita na conversa. Achados da própria investigação do agente (dúvidas levantadas, links candidatos, sugestões de vínculo) são **propostos no handoff da missão**, não escritos direto no card; só entram no corpo depois que o PM confirmar. **Contexto nunca cita nomes de Team Lead/Tech Lead nem estrutura de squads como justificativa de raciocínio** — é informação interna do PM/Knowledge Graph, não conteúdo do card (se a squad responsável importa para o escopo, cite a squad, não as lideranças). **Metadado do processo de investigação do agente** (termos de busca, datas de busca, "nenhum item encontrado") **nunca vai para o card** — é conteúdo de handoff, não de produto.

## Mapa da hierarquia

| Nível | ClickUp (Vertical Tech) |
|-------|--------------------------|
| Delivery | **Projeto de Delivery** (folder Delivery do Squad correto) — nasce no Backlog já com tipo final (`Epic`/`Tarefa`/`Bug`); passa pela faixa de descoberta embutida no Backlog (`em refinamento`→`pronto p/ design`→`em design`); migra para a **Sprint ativa** do squad ao entrar em execução |
| Subtarefa | **Subtask** sob o item pai (UC, edge case, build, ou **Correção** pós-homologação) |
| Update | **Comentário** na task (`clickup_create_task_comment`) |

> Não existe mais nível Objetivo (OKR/KR) nem Discovery como item/folder separado. O Projeto de Delivery é o
> topo do processo — ver `knowledge/domains/processo.md` → "Hierarquia do Processo".

## Definição dos folders (fluxo canônico)

| Folder | Propósito | O que vive aqui |
|--------|-----------|-----------------|
| **Delivery: Experiência do jogador** | Backlog (descoberta + refinamento) — squad PAM | Épicos, bugs, tarefas de produto voltados ao jogador |
| **Sprints — PAM** | Execução — squad PAM | Sprint ativa (ex.: "Sprint 1 (7/9 - 20/9)") |
| **Delivery: Operação e afiliados** | Backlog (descoberta + refinamento) — squad Backoffice | Épicos, bugs, tarefas de backoffice e afiliados |
| **Sprints — Backoffice** ("Pasta do sprint" no ClickUp) | Execução — squad Backoffice | Sprint ativa (ex.: "Sprint 1 (14/9 - 27/9)") |
| **Delivery: Provedora de conteúdo** | Backlog + Execução — squad Jogos (**não migrado para sprints ainda**) | Épicos, bugs, integrações de provedoras |

**Regras decorrentes (a `clickup-spec` sempre segue):**

- **Descoberta é uma faixa de status dentro do Backlog, não um item separado.** Um Delivery nasce direto no Backlog do squad, já com o tipo final — passa por `em refinamento`→`pronto p/ design`→`em design` antes de estar pronto para sprint. Prototipação continua sempre em Figma, nunca em código, durante essa faixa.
- **Delivery é execução assim que entra na Sprint** — se ainda há decisão de produto/UX em aberto, o item permanece no Backlog, não entra na sprint.
- **O folder de Delivery correto é determinado pelo Squad responsável**: Experiência do jogador → folder PAM → Sprints — PAM; Operação e afiliados → folder Backoffice → Sprints — Backoffice; Provedora de conteúdo → folder Jogos → Execução (fluxo antigo, ainda sem sprint). Sempre confirmar o Squad antes de criar o Delivery.
- **Delivery nasce no Backlog** (status `backlog`). Migra para a **Sprint ativa** do squad no rito de Planejamento — nunca automaticamente, nunca antes de `pronto p/ execução`/`priorizado`. Nunca criar listas novas nos folders nem nas pastas de Sprint.
- **Todo Projeto de Delivery segue o [template-delivery.md](template-delivery.md)** — com critérios de aceite propostos pelo PM antes do refinamento (áreas padrão de Qualidade e Instrumentação); épico não nasce sem eles. As seções que antes viviam num Discovery separado (JTBD, Personas, Evidências, decisões de UX em aberto) hoje entram como parte do próprio Contexto do Delivery quando há informação relevante.

## Sprints — planejamento, execução e fechamento

Cada squad migrado (PAM, Backoffice) tem seu Sprint Folder nativo do ClickUp, com uma lista por sprint. A
squad Jogos ainda não migrou — segue no fluxo Backlog→Execução até segunda ordem.

**Cadência**: sprints de 2 semanas, com início intercalado em 1 semana de diferença entre PAM e Backoffice, para
que pessoas compartilhadas entre os dois squads não acumulem todos os ritos na mesma semana.

**Ritos**:
- **Planejamento** (início da sprint): auditar o Backlog do squad (itens em `pronto p/ execução`/`priorizado`), confirmar com o PM o que entra, mover os itens confirmados para a Sprint ativa via `clickup_move_task`. No mesmo rito, revisar o board de Execução legado (se ainda houver itens) e propor devolver ao Backlog ou encaixar na sprint — sempre com confirmação.
- **Daily**: sem automação de fluxo. Útil gerar um resumo de itens travados (parados há N dias, ou em `bloqueada`) via `clickup_get_bulk_tasks_time_in_status` antes do rito.
- **Revisão**: ao fim da sprint, relatório do que foi concluído vs. planejado, postado como comentário na lista de Sprint — é o principal artefato de dado/valor para stakeholders (ver "Modelos de Update" abaixo).
- **Retrospectiva**: tempo-em-status real por sprint (`clickup_get_bulk_tasks_time_in_status`) como insumo objetivo de gargalos. A cascata nativa do ClickUp (Sprint Automations) migra itens não concluídos para a próxima sprint automaticamente — confirmar que está ativada no workspace (config manual, fora do alcance da API).

> 🚨 **Cuidado com a automação nativa de `priorizado`**: no Backlog do PAM, setar o status `priorizado` dispara
> uma automação do workspace que move a task para o board de **Execução legado** (`901114029785`), não para a
> Sprint ativa. **Decidido em 2026-09-10: essa automação deve ser desativada** — o Backlog já funciona como
> fila da próxima sprint, não precisa de nenhum destino automático. Desativação é ação manual do PM na UI do
> ClickUp (sem ferramenta de automação no MCP); até lá, trate `priorizado` com cautela. Ver `clickup-config.md`
> → "Convenções" para o detalhe.

**Sprint Points**: o ClickApp de estimativa (esforço por task, escala tipo Fibonacci) **não está ativado** hoje em nenhuma Sprint Folder — sem ele, só dá para medir throughput por contagem de itens, não velocity. Ativar é decisão/configuração manual do usuário no workspace, não algo que a skill resolve.

## Vínculos entre níveis

Sem nível acima do Delivery, vínculo por linked task deixou de ser o padrão — use só quando pontualmente fizer
sentido:

| Mecanismo | Tool | Quando usar |
|-----------|------|-------------|
| **Linked task** ("relacionado") | `clickup_add_task_link` | Vínculo pontual entre itens quando há relação real (ex.: um Bug que referencia o Épico afetado). Não é mais obrigatório por padrão. |
| **Dependência** (`waiting_on` / `blocking`) | `clickup_add_task_dependency` | **Apenas** quando há ordem real (uma tarefa espera ou bloqueia outra). Nunca use no lugar do linked task de pertencimento. |
| **Subtask** (parent-child) | campo `parent` no `clickup_create_task` | Decomposição **macro** dentro da mesma lista, ou **Correção** pós-homologação do item pai. Usar com parcimônia — ver guardrail abaixo. |

Decisão de modelagem: **não usamos** *Tasks in Multiple Lists* nem o campo *Relationship*.

### Guardrail — macro, não micro
- O escopo da `clickup-spec` é **macro**: o Projeto de Delivery. Mantenha tarefas no nível de projeto/aposta.
- **Evite criar subtasks e tarefas micro.** A quebra fina (passos de implementação, itens de checklist) é da squad/designer, não da spec de produto.
- Se a decomposição for inevitável, limite a **poucas frentes macro** (ex: UCs principais, grandes frentes de build) — nunca um item por micro-passo.
- Sinais de que virou micro demais: cabe em < 1 dia, é um passo técnico isolado, ou não tem valor de usuário próprio. Nesse caso, use **checklist dentro da tarefa-pai**, não uma subtask.

## Priorização de itens de Delivery

**Score, Impacto, Alcance, T-Shirt Sizing, Votos, Horizonte e Time (Squad) não existem como custom field em
Delivery** — viviam só na lista Iniciativas, hoje depreciada (ver `clickup-config.md`). Não proponha
nem tente gravar esses valores num item de Delivery. Se o usuário quiser priorizar um item de Delivery hoje,
use a skill `ice` ou `gist` na conversa — a pontuação fica no diálogo/handoff, não em custom field. Redefinir
uma moradia para esses campos no nível Delivery é decisão estrutural (`agente-evolucao` → `agente-governanca`),
não algo a inferir sozinho.

### Squad
Experiência do jogador / Operação e afiliados / Provedora de conteúdo — **não é um campo**, é a escolha do
folder de Delivery (confirme com o usuário quando não for óbvio).

### Campos que de fato existem em Discovery/Delivery
- **Empresa**: Tradicional, Bravo, Vertical.
- **KPIs** (eixo): Compliance, Conversão, Eficiência Operacional, Receita, Retenção, Satisfação, Segurança.
- **Data de Início / Conclusão Prevista**: use quando houver comprometimento de prazo.

## Completude de Campos — Política "Nenhum Campo Vazio Inferível"

Ao criar ou atualizar qualquer item, **preencha todos os campos que a informação disponível permite inferir** — nunca deixe campo em branco quando o valor pode ser derivado do contexto.

**Campos obrigatórios por nível:**

| Nível | Campos obrigatórios | Campos a inferir |
|-------|---------------------|-----------------|
| Delivery | assignee, `_Projeto`, `_Classe`, tipo correto (`Epic` / Tarefa / Bug / Correção — valor exato em clickup-config.md), status inicial `backlog` | `_Risco Reg.` se houver exposição regulatória |
| Ticket operacional | assignee, `_Projeto`, `_Classe` | `_Risco Reg.` se aplicável |

**Regra de operação:**
- Se um campo obrigatório não pode ser inferido → pergunte antes de criar, não crie com campo vazio.
- Se um campo enriquecedor pode ser inferido com razoável confiança → preencha e explique o raciocínio; o usuário pode corrigir.
- Após criar, liste os campos preenchidos automaticamente e os que ficaram em aberto — não deixe o usuário adivinhar o que foi ou não gravado.

## Modelos de Update (comentários narrativos)

Formato padrão: **contexto → decisão/fato → próximo passo**. Curtos e escaneáveis.

**Delivery criado** (comentar no próprio card)
```
[Nome do Delivery]

[1 parágrafo: problema, impacto e o que será construído]

Escopo do build:
- [capacidade 1 — linguagem de usuário]

Próximo passo: [refinamento com design/engenharia].
```

**Pronto para sprint** (item saiu da faixa de descoberta do Backlog — `pronto p/ execução`/`priorizado`)
```
[Nome do Delivery] está pronto para entrar em sprint.

[1 parágrafo: o que foi decidido/fechado na faixa de descoberta — escopo, UX, critérios de aceite]

Próximo passo: entrar na Sprint [N] do squad [PAM/Backoffice] no próximo Planejamento.
```

**Entrou na sprint** (Planejamento — comentar na task ao mover para a Sprint ativa)
```
Entrou na Sprint [N] ([datas]) — squad [PAM/Backoffice].

[1 parágrafo: o que será entregue nesta sprint]

Próximo passo: acompanhar na Daily.
```

**Relatório de Revisão (Sprint Review)** — o artefato central de dados/valor para stakeholders; postar na lista
de Sprint ao final do ciclo
```
Sprint [N] ([datas]) — squad [PAM/Backoffice] — Revisão

Planejado: [N] itens · Concluído: [N] itens ([%])

Entregue:
- [nome do item] → [link]

Não concluído (migra para a próxima sprint):
- [nome do item] — [motivo em 1 frase]

Próximo passo: Planejamento da Sprint [N+1] em [data].
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

**Resposta a investigação em andamento** (comentário que responde perguntas/hipóteses já levantadas antes)
```
[Recap em 1-2 frases: o que é o caso, pra quem não leu o histórico/relatório anterior]

**[Pergunta ou hipótese 1]** — [resposta, com o número que a sustenta inline].

**[Pergunta ou hipótese 2]** — [resposta, com o número que a sustenta inline]. [O que ainda fica em
aberto, se for o caso.]

[Conclusão consolidada: o que isso muda no diagnóstico geral]

Próximo passo: [ação concreta + quem/o quê está pendente].
```
Ver [estilo-redacao.md](estilo-redacao.md#recap-antes-de-responder--quem-não-acompanhou-o-histórico-não-pode-ficar-perdido) para o racional (recap + evidência inline).

## Transições de status sugeridas

Ao postar updates, ofereça atualizar o status dos itens via `clickup_update_task`. A sequência (Backlog →
Sprint) diverge por squad — confirme o fluxo exato em `clickup-config.md` antes de aplicar:

| Momento | Status no Backlog | Status na Sprint |
|---------|-------------------|-------------------|
| Delivery criado | `backlog` | — |
| Em refinamento/design (descoberta) | `em refinamento` → `pronto p/ design` → `em design` (ordem varia por squad) | — |
| Pronto para sprint | `pronto p/ execução` → `priorizado` | — |
| Entrou na sprint (Planejamento) | — | `pendente` |
| Em desenvolvimento | — | `em desenvolvimento` |
| Bloqueado | — | `bloqueada` |
| Em homologação | — | `em homologação` (Backoffice) / `em homologação (alpha)` (PAM) |
| Deploy realizado | — | `deploy p/ prod` → `pronto` / `fechado` |
| Descartado | `despriorizado`/`fechado` | `cancelado` |

> Squad Jogos (Delivery: Provedora de conteúdo) ainda não tem Sprint Folder — use o fluxo antigo Backlog →
> Execução documentado em `clickup-config.md` até a migração acontecer.
