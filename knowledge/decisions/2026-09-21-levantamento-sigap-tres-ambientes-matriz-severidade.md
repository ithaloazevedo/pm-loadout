# Levantamento do furo SIGAP para a SPA cobre três ambientes, separa universo por corte de data e reporta matriz de severidade em vez de número único

**Data**: 2026-09-21
**Tomada por**: Ithalo Mendes (via Orquestrador + agente-delivery)
**Status**: APROVADA

---

## Contexto

Reunião com a SPA marcada para 22/09/2026 sobre o furo no bloqueio SIGAP por motivo `PROGRAMA_SOCIAL`.
O levantamento anterior ([868m4541a](https://app.clickup.com/t/868m4541a), fechado na Sprint 1 do PAM)
tinha escopo deliberadamente restrito à Bravo e produziu o número que circula hoje: **838 pessoas** com
ao menos um evento depois do momento em que já deveriam estar bloqueadas. A Nota Explicativa externa já
redigida afirma que a falha foi "restrita à plataforma Bravo".

Ithalo pediu a criação de uma tarefa para Ícaro na sprint ativa, consolidando Tradicional, Bravo atual e
Bravo legado desde 19/12/2025, com o acesso somente-leitura aos dois bancos (`trad_prd`, `ar_bravo_prd`)
já liberado para ele e para o Ícaro.

## Achados que mudaram o escopo pedido

1. **A exceção nasceu em código compartilhado, a correção não.** O commit `1b01c1f92` (19/12/2025) criou a
   exceção no `micro-api` compartilhado (`EntitiesController.ts`) — a Bravo só herdou em março/2026. A
   correção `5132ff9802b2b781648636c4886d6e65c3f0d2b1` (MR!276, 10/09/2026) foi mergeada em `prd_bravo-new`.
   Não há evidência de que a Tradicional tenha sido corrigida. Logo, o levantamento da Tradicional pode não
   ser prova negativa, e sim a descoberta de um segundo furo ativo — o que derrubaria a afirmação de
   "restrita à plataforma Bravo" da Nota Explicativa antes de ela ser sustentada perante a SPA.
2. **A correção não fechou a exceção, apenas a datou.** O `SOCIAL_PROGRAM_BLOCK_CUTOFF` limitou a exceção a
   contas criadas antes de 01/12/2025. Beneficiário de programa social com conta anterior a essa data segue
   não bloqueado hoje, por desenho. A lei não abre essa exceção — é pergunta em aberto para a SPA, não só
   uma nuance de métrica.
3. **"838" é um numerador achatado.** O próprio levantamento citado em reunião distingue 365 depositantes e
   169 pessoas com saque dentro dos mesmos 838 — exposições financeiras muito diferentes tratadas como um
   grupo único.

## Decisão

Criada a tarefa [868m7n3kv](https://app.clickup.com/t/868m7n3kv) (Spike, Sprint 2 do PAM `901115407666`,
assignee Ícaro Lopes, prioridade `urgent`, due 22/09/2026, KPI e Módulo = Compliance, `Empresa` vazio por
ser multimarca, `_Tarefa Sprint` = Não planejada (SM ou SS)), linkada a `868m4541a` e `868m69avx`, com as
seguintes definições fechadas pelo PM — nenhuma delas deixada em aberto no card:

- **Recorte do universo**: apenas o motivo `PROGRAMA_SOCIAL`. Os demais motivos do SIGAP (inclui FIES e
  Desenrola) entram só como número de controle, para demonstrar que o bloqueio funcionava neles.
- **Prejuízo por pessoa** = total depositado − total sacado − saldo atual, com o saldo atual em coluna
  separada por ser valor retido e restituível de imediato, diferente da perda consumada em aposta.
- **Segmentação obrigatória por data de cadastro no corte de 01/12/2025**: contas a partir do corte formam
  o denominador da taxa de falha; contas anteriores, cobertas pela exceção ainda vigente, vão em bloco à
  parte. Taxa de efetividade = bloqueados ÷ universo identificado; taxa de falha = movimentaram ÷ quem
  deveria ter sido bloqueado. Os dois denominadores vão declarados junto do número.
- **Matriz de severidade em degraus** no lugar do número único: identificados → bloqueados corretamente →
  acessaram → depositaram → apostaram → tiveram perda → sacaram, cada pessoa contada no degrau mais
  profundo alcançado, com contagem e valor em cada degrau, por ambiente e consolidado. Os 838/365/169 da
  Bravo entram como baseline de conferência da extração, não como número novo.
- **Verificação de código na Tradicional** vira critério de aceite: um resultado zerado naquele ambiente só
  é reportado acompanhado da conclusão sobre se a exceção existiu e se está corrigida lá.
- Ordem de execução: números macro primeiro, detalhamento individual por CPF depois.

## Trade-offs Aceitos

- **Tarefa única em vez de uma por ambiente**, apesar de o pedido original falar em dividir a extração entre
  os três ambientes — três cards para menos de 24h de trabalho seria overhead; a divisão vive nos critérios
  de aceite e quem quebra é a engenharia.
- **Fonte do Bravo legado desconhecida** — fica em "❓ Aberto para refinamento técnico" (pendência
  estritamente técnica, permitida). Se não existir log de consulta SIGAP no legado, o escopo cai para dois
  ambientes e essa parte da Nota Explicativa fica sem sustentação — decisão do PM, não da squad.
- **Prazo de 24h para consolidar três ambientes** com a lista nominal por CPF sendo o item mais caro e o
  último da fila.
- **`868m7g7u4`** ("[Tradicional] canLogin travado após desbloqueio SIGAP", em desenvolvimento com Melk
  nesta mesma sprint) **não foi linkado** por decisão do PM, embora toque o mesmo fluxo na Tradicional.

## O que mudaria a decisão

- Se a verificação de código mostrar que a Tradicional também rodou com a exceção sem correção, isso deixa
  de ser um levantamento de impacto e vira incidente ativo — a Nota Explicativa precisa ser reescrita antes
  da reunião, não depois.
- Se o Jurídico/Compliance concluir que a exceção para contas anteriores a 01/12/2025 não tem base legal, o
  bloco "pré-corte" deixa de ser contexto e vira correção com prazo.

## Impacto

- **Produto**: módulo Compliance; bloqueio de impedidos SIGAP na Tradicional e nas duas gerações da Bravo.
- **Técnico**: `cpf_impedidos_sigap_queries` como fonte do universo e T0; `entities`, `pix.transactions`,
  `integration.bets`, `integration.sport_bets`, `withdraw_requests` como fontes de evento; fonte equivalente
  no Bravo legado ainda desconhecida.
- **Processo**: reforça que a definição de métrica (denominador, fórmula de prejuízo, recorte do universo) é
  decisão de produto fechada antes do card, não pergunta deixada para quem extrai. PII e material de
  resposta a regulador não circulam em comentário aberto do ClickUp.

## Links

- Tarefa criada: [868m7n3kv](https://app.clickup.com/t/868m7n3kv)
- Levantamento anterior (Bravo, fechado): [868m4541a](https://app.clickup.com/t/868m4541a)
- Detalhamento por CPF na Bravo (precedente metodológico): [868m69avx](https://app.clickup.com/t/868m69avx)
- Nota Explicativa externa: `~/Downloads/relatorio-sigap-bravo-versao-externa.md`, `Nota Explicativa — Furo SIGAP Bravo.pdf`
- Relatório técnico do furo: `~/Downloads/relatorio-tecnico-furo-sigap-bravo.pdf`
- Decisão relacionada (acesso ao banco da Bravo): [[2026-09-15-acesso-banco-bravo-agente-dados]]
- Decisão relacionada (enforcement de impedidos, dois épicos): [[2026-08-27-enforcement-usuarios-impedidos-status-flags-dois-epicos]]
- Decisão relacionada (escopo de "Aberto para refinamento técnico"): [[2026-08-11-aberto-para-refinamento-tecnico-restricao-de-uso]]
