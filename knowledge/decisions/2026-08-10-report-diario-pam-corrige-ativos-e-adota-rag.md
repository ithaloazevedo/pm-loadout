# Report diário do PAM: "Ativos" (55/56, enganoso) substituído por "Em andamento" real + Atrasados + farol RAG

**Data**: 2026-08-10
**Tomada por**: Ithalo Mendes (PM)
**Status**: APROVADA

---

## Contexto

No mesmo dia em que o report diário do PAM foi publicado pela primeira vez no ClickUp Doc
(`8ccvn07-68891`), o Ithalo notou que os números de "Ativos" (55 em Plataforma, 56 em Backoffice &
Integrações) pareciam altos demais e pediu para checar se estavam certos — e, junto disso, para refinar
o report usando dois artigos sobre modelo prático de status report como referência.

Investigação: `computeDailySquadData` (então em `public/index.html`) definia "Ativos" como **toda
tarefa não fechada** das listas de Backlog + Execução de cada squad — sem distinguir Backlog nunca
tocado, Pendente, Bloqueada, Despriorizada ou efetivamente em desenvolvimento/teste. Contagem real
verificada via `/api/tasks/plataforma`: de 54 tarefas "ativas", só ~18 estavam em status de
desenvolvimento/design/teste; o resto era Backlog (11), Pendente (11), Pronto p/ design (7),
Despriorizado (2) e Bloqueada (5, já contada à parte). O número estava **tecnicamente correto para a
definição implementada**, mas a definição em si era ruim para um status report — confundia "nada foi
feito ainda" com "está sendo trabalhado agora".

Dos dois artigos linkados, só um foi possível ler
(["Status Report: A Practical Model and Example"](https://medium.com/ilegra/status-report-a-practical-model-and-example-623037e00830)
— o outro, da Euax, só devolveu menu/navegação via fetch, conteúdo renderizado por JS não capturado).
Elementos aproveitados do que foi lido: status executivo em farol RAG (Red-Amber-Green) definido por
regra objetiva, itens não-verdes exigindo explicação numérica (não just um emoji), e o princípio geral
de "usar números para definir o status, não presumir".

## Decisão

Reescrito `computeDailySquadData`/`buildSquadDailyMarkdown`/`buildResumoExecutivoMarkdown` em
`tools/radar-produto/public/index.html` (e replicado no script headless que efetivamente publica, já
que não há automação de navegador nesta sessão para clicar no botão real):

- **"Em andamento"** substitui "Ativos": só tarefas não fechadas, não canceladas/despriorizadas, com
  status em `ST_ANDAMENTO` (desenvolvimento, teste dev/em dev/homolog/alpha, deploy p/ alpha/prd) —
  **reaproveita a mesma lista já aprovada pela liderança no report semanal**
  (`scripts/weekly_report.py`, claude-os), para os dois reports não divergirem sobre o que conta como
  trabalho em curso.
- **"Atrasados"** é novo: não fechada, não cancelada, `due_date` já vencido, status não é de conclusão —
  o sinal de risco que "toda tarefa não fechada" escondia dentro de si.
- **Farol 🔴/🟡/🟢 por squad** no Resumo Executivo: 🔴 se há bloqueado, 🟡 se não há bloqueado mas há
  atrasado, 🟢 caso contrário — e a linha de "Sinais de atenção" virou frase objetiva com as contagens,
  não só o emoji.

Republicado no Doc real depois da correção: Plataforma caiu de "56 ativos" para **12 em andamento** (+ 1
atrasado); Backoffice & Integrações caiu de "55 ativos" para **19 em andamento** (+ 2 atrasados).

## Trade-offs Aceitos

- O artigo da Euax não pôde ser lido (conteúdo renderizado por JS, `WebFetch` só devolveu a navegação do
  site) — a refinada usa só o que foi extraído do artigo da ilegra. Se o Ithalo tiver o texto completo
  daquele artigo, vale revisitar esta decisão.
- "Concluídos hoje" continua sem correção — permanece o mesmo tipo de proxy (`date_closed` no dia) que
  já tinha sido sinalizado como potencialmente inflado por fechamentos em lote (ver apuração anterior
  nesta mesma sessão, sobre `date_closed` cravado no mesmo minuto em 06/08). Não foi tratado agora
  porque exigiria excluir fechamentos em lote sem um critério objetivo à mão — fica como suspeita
  aberta, não como bug corrigido.
- A aba interativa de "Gerar Report" (período configurável, exportável em PDF) tem sua própria função
  `computeReportData` com a mesma conflação antiga ("ativo" = não fechado) — **não foi tocada**, porque
  o pedido era especificamente sobre o report publicado no Doc. Fica como problema conhecido, não
  resolvido.

## O que mudaria a decisão

- Se a liderança quiser um critério diferente para "em andamento" (ex.: incluir `revisão técnica`, que o
  report semanal deliberadamente exclui), ajustar `ST_ANDAMENTO` nos dois lugares (aqui e em
  `weekly_report.py`) para não voltarem a divergir.
- Se o artigo da Euax puder ser lido por outro meio, revisitar para incorporar o que ficou de fora.

## Impacto

- **Produto**: nenhum módulo de produto afetado — ferramenta interna de operação do PM.
- **Técnico**: `tools/radar-produto/public/index.html` e `README.md` alterados. Testado ao vivo — 3
  páginas republicadas no Doc real com os números corrigidos.
- **Processo**: nenhum.

## Links

- Código: `tools/radar-produto/public/index.html` (`computeDailySquadData`, `buildSquadDailyMarkdown`,
  `buildResumoExecutivoMarkdown`), `tools/radar-produto/README.md`
- Referência de modelo: https://medium.com/ilegra/status-report-a-practical-model-and-example-623037e00830
- Doc de destino: [ClickUp — Report Status](https://app.clickup.com/9006076935/docs/8ccvn07-68891)
- Decisão relacionada (criação original do report diário): [[2026-08-10-report-diario-pam-extensao-radar-produto]]
