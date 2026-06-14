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
| Projeto de Discovery | **Projeto de Discovery** (folder Product Discovery, lista Design) |
| Projeto de Delivery | **Projeto de Delivery** (folder Product Delivery) |
| Issue / Milestone | **Subtask** sob o item pai (UC, edge case, build) |
| Activity Update | **Comentário** na task (`clickup_create_task_comment`) |

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
