# Discovery de encontrabilidade de jogos ganha escopo ampliado: entrada + funcionamento da busca

**Data**: 2026-09-04
**Tomada por**: Ithalo Mendes (via Orquestrador)
**Status**: APROVADA

---

## Contexto

A pesquisa de churn da Tradicional.bet.br (126 respostas, +30 dias sem login, coleta
27/08–03/09/2026) apontou "encontrar jogos e apostas" como o ponto de dificuldade de
navegação mais citado (20/126, mais que o dobro de qualquer outro). O PM propôs abrir um
Discovery no time Plataforma para "estudar a possibilidade de redundância no botão
Buscar" nas homes e na banca, com a hipótese de que os respondentes da pesquisa ainda não
tinham visto a nova bottom bar com esse botão.

Antes de abrir o card, o Orquestrador cruzou a hipótese contra o ClickUp.

## Opções Consideradas

1. **Abrir o Discovery só com o escopo original** (redundância de entrada do botão
   Buscar nas homes e na banca)
   - Prós: fiel ao pedido literal do PM, escopo menor.
   - Contras: o botão "Buscar" (Épico 868kkad8x, squad Plataforma, no ar desde
     06/08/2026) foi lançado **sem destino funcional** — não existe hoje nenhuma tela ou
     lógica de busca implementada, nem Discovery/Delivery aberto tratando disso. Ampliar
     a presença de um botão que não leva a lugar nenhum não fecha o problema relatado.

2. **Ampliar o escopo para cobrir também "o que a busca faz quando acionada"** — escolhida
   - Prós: fecha o loop do problema real; evita retrabalho de reabrir o Discovery em
     poucas semanas quando alguém perceber que "achar o botão" não resolve nada sem uma
     busca funcional atrás dele.
   - Contras: escopo maior, mais uma frente para negociar prioridade com o time.

## Decisão

O card de Discovery (https://app.clickup.com/t/868m1hqe7) foi aberto cobrindo as duas
frentes: (a) onde as entradas de acesso à busca deveriam existir (a pergunta original do
PM — homes, banca, bottom bar) e (b) o que a experiência de busca deve de fato entregar
quando acionada, já que essa funcionalidade nunca foi especificada.

A hipótese original do PM (usuários da pesquisa não viram o botão novo) foi confirmada
por cruzamento de datas: o épico foi ao ar em 06/08/2026, e todo respondente da pesquisa
já estava há 30+ dias sem logar antes de ~28/07/2026 — nenhum chegou a ver a mudança.

## Trade-offs Aceitos

- O Discovery nasce mais amplo do que o pedido original — o kickoff com o time de
  Plataforma precisa validar essa leitura antes de prosseguir (marcado como questão em
  aberto no card, não decidido unilateralmente).

## Atualização (2026-09-04, mesmo dia)

O PM confirmou diretamente, antes mesmo do kickoff, que "banca" = **Banca de Benefícios**
(Épico 868k9ccce): o hub de gamificação/promoções da Tradicional — missões, check-in
diário, roleta diária, Indique e Ganhe, bônus, promoções, mensagens, torneios, acesso via
bottom bar/banner/menu só para logados. O card foi atualizado: a pendência saiu de
"Questões em aberto" e virou fato assentado em Evidências, e o Épico do Hub de Benefícios
foi linkado. Ficou registrada como leitura a explorar (não decidida) a hipótese de que a
Banca de Benefícios é uma superfície de retorno diário recorrente, o que pode reforçar o
racional de colocar uma entrada de busca ali.

## O que mudaria a decisão

- Se o time de Plataforma já tiver, fora do ClickUp, uma definição de escopo/tela para a
  busca que o Orquestrador não encontrou — revisar e possivelmente desmembrar em dois
  Discoveries menores.

## Impacto

- **Produto**: navegação da Tradicional (bottom bar, homes, banca — a mapear).
- **Técnico**: nenhum sistema novo definido ainda; Bravo já tem um `SearchDropdown` em 8
  páginas (sem página de resultados) citado como referência a avaliar, não como padrão a
  copiar.
- **Processo**: nenhuma mudança de processo.

## Links

- Card no ClickUp: https://app.clickup.com/t/868m1hqe7
- Épico bottom bar (introduz o botão Buscar sem destino funcional): https://app.clickup.com/t/868kkad8x
- Relatório da pesquisa de churn: https://claude.ai/code/artifact/90b64e6a-c7a4-4a65-a02f-bf5cc5506c5a
- Decisão relacionada (classificação dos épicos irmãos): [[2026-08-03-header-bottom-bar-epicos-reestilizacao-tradicional]]
