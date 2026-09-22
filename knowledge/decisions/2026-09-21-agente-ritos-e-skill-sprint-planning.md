# Agente de Ritos e skill sprint-planning

**Data:** 2026-09-21
**Decisor:** Ithalo (PM)
**Status:** decidido, primeira versão entregue

## Contexto

Durante o planejamento da Sprint 2 do Time PAM, a conversa produziu um artifact de planning que passou por
doze iterações até chegar num formato que o PM aprovou. O formato não estava registrado em lugar nenhum —
se a próxima planning fosse gerada do zero, o aprendizado se perderia.

## Decisão

Criar um agente especialista em ritos de Scrum e transformar o formato validado em skill.

**`agente-ritos`** conduz as cerimônias. Começa com o Planejamento. Revisão continua atendida pela
`clickup-revisa-sprint` até ser migrada; Daily e Retrospectiva ainda não foram implementados.

**`sprint-planning`** define método e formato da planning. O artifact tem três abas:

| Aba | Obrigatória | Conteúdo |
|---|---|---|
| Visão executiva | sim | objetivo da sprint, números, dois gráficos enxutos (frente de valor e casa), objetivo por desenvolvedor, pontos de atenção |
| Por desenvolvedor | sim | devs em ordem alfabética, itens em ordem de prioridade |
| Em discussão | não | só quando há trabalho considerado e não comprometido |

As abas "Por frente de valor" e "Por casa", que eram listas completas, viraram dois gráficos dentro da
visão executiva. A lista inteira repetida em três recortes cansava sem acrescentar.

## Por que assim

As duas seções mais elogiadas pelo PM foram **Visão executiva** e **Por desenvolvedor** — as duas que
respondem "que valor a sprint entrega" e "o que cada pessoa faz primeiro". As demais eram recorte da mesma
informação.

A aba "Em discussão" nasceu de uma situação atípica (a dívida de um incidente sendo considerada para a
sprint). Vira opcional, mas o agente pergunta uma vez se há algo a considerar — decisão pendente, dívida de
incidente, pedido de stakeholder que ainda não virou card.

## Regras que viraram parte da skill

Registradas em `.claude/skills/sprint-planning/references/regras-de-leitura.md`, cada uma com a
justificativa. As que mais custaram para descobrir:

- **Só desenvolvedores contam na carga.** Sem esse corte, o QA aparecia como a maior carga de
  desenvolvimento da sprint, com 37 itens contra 29 do primeiro dev.
- **Data de criação não é tempo de espera.** Item antigo costuma ter passado o tempo em refinamento de
  produto e design. Apresentar idade de card como atraso foi um erro corrigido pelo PM.
- **A ordem da fila vem da prioridade cadastrada no ClickUp**, não de peso inventado — 54 de 58 itens
  tinham o campo preenchido, e substituir isso tornaria a ordem inexplicável numa reunião.
- **Campo deduzido é marcado visualmente e confirmado com o PM.** 38 de 58 itens estavam sem casa e 30 sem
  frente de valor.
- **Mover do Backlog para a Sprint quebra o status** — o ClickUp mapeia para `bloqueada`.

## Tom de voz

Na mesma decisão, o guia de tom de voz do Ithalo virou arquivo canônico do repositório em
`knowledge/tom-de-voz.md`. O caminho anterior era um arquivo em `~/Downloads` que não existe mais. O
`orquestrador` agora lista o guia como fonte de contexto obrigatória, e o
`clickup-spec/references/estilo-redacao.md` passou a apontar para ele como fonte.

## Próximos passos

Refinar os demais ritos: Daily, Revisão (migrando a `clickup-revisa-sprint` para o agente) e
Retrospectiva.
