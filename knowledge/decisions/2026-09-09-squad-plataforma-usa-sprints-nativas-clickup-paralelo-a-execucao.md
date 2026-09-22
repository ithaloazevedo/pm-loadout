# Squad Plataforma usa Sprints nativas do ClickUp ("Sprint 1", 7–20/9) em paralelo ao fluxo documentado Backlog→Execução

**Data**: 2026-09-09
**Tomada por**: Ithalo Mendes (via Orquestrador + agente-delivery)
**Status**: APROVADA

---

## Contexto

Ao abrir um Bug para o Rayan (Tech Lead da squad Plataforma) e pedir para colocá-lo na "Sprint 1 do time Plataforma", a referência local (`clickup-config.md`) só documentava duas listas no folder "Delivery: Plataforma": **Backlog** (`901114029784`) e **Execução** (`901114029785`, descrita como "WIP sprint ativa"). Não havia lista chamada "Sprint 1" nessa estrutura. O agente-delivery inicialmente assumiu "Execução" como equivalente funcional, mas o PM apontou uma lista específica por URL, revelando uma estrutura paralela não documentada.

## Opções Consideradas

1. **Tratar "Execução" como a sprint ativa real** — manter o fluxo Backlog→Execução como única fonte de verdade.
   - Prós: consistente com toda a documentação existente (`clickup-config.md`, `processo.md`).
   - Contras: ignora que o PM apontou explicitamente uma lista diferente, já em uso real.

2. **Usar a lista "Sprint 1 (7/9-20/9)" do folder nativo "Sprints"** (`90118303225`, Space Vertical Tech) — confirmada com janela de datas cobrindo o momento atual e pipeline de status próprio de engenharia (`pendente` → `em desenvolvimento` → `em homologação (alpha)` → `em revisão técnica` → `deploy p/ prod` → `pronto`/`cancelado`/`fechado`).
   - Prós: é a sprint ativa de fato, confirmada por datas e por indicação direta do PM; distinta de duas outras listas "Sprint 1" descartadas por estarem em folders soltos sem relação com o processo (ex.: ao lado de uma lista "teste backlog").
   - Contras: não documentada em `clickup-config.md` — introduz uma segunda estrutura de sprint não reconciliada com Backlog→Execução.

## Decisão

Opção 2. O card foi movido (via `clickup_move_task`, não Tasks in Multiple Lists) para a lista "Sprint 1 (7/9-20/9)" no folder "Sprints". O move preservou status, assignee, prioridade, tipo e os três custom fields compartilhados no nível do Space (Empresa, KPIs, Módulo do PAM) — nenhum campo foi perdido.

## Trade-offs Aceitos

Ficamos com duas estruturas de sprint coexistindo sem reconciliação documentada: o fluxo Backlog→Execução (documentado, usado por outras squads/casos) e o folder nativo "Sprints" (usado ao menos pela squad Plataforma, com pipeline de status próprio). Isso pode causar confusão em specs futuras até que alguém decida se Sprints substitui, complementa ou convive com Execução para essa squad.

## O que mudaria a decisão

Se `agente-evolucao`/`agente-governanca` investigar e concluir que o folder "Sprints" é o padrão real para todas as squads (ou só Plataforma) e Execução está sendo depreciada na prática, `clickup-config.md` e `processo.md` devem ser atualizados para refletir isso como fonte única — hoje é só um achado pontual, não uma reconciliação completa.

## Impacto

- **Produto**: nenhum diretamente — é uma questão de operação de ClickUp, não de escopo de feature.
- **Técnico**: nenhum.
- **Processo**: `clickup-config.md` está desatualizado para a squad Plataforma — não referencia o folder "Sprints" nem seu pipeline de status próprio. Specs futuras dessa squad devem confirmar ao vivo (via `clickup_get_workspace_hierarchy`) se o destino é Execução ou uma lista do folder Sprints, em vez de assumir a partir da doc.

## Links

- Card no ClickUp: [Dados para análise do Aviator divergem dos dados reais do jogo](https://app.clickup.com/t/868m38kmt) (868m38kmt)
- Lista "Sprint 1": https://app.clickup.com/9006076935/v/li/901114417832
- Referência desatualizada: `.claude/skills/clickup-spec/references/clickup-config.md` (linhas 24-45, listas conhecidas por folder)
