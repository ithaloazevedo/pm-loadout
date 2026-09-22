# Report diário do PAM: Plataforma+Backoffice fundidos numa única página, + Novas prioridades, Em teste completo, Próxima prioridade por dev e leitura de comentários

**Data**: 2026-08-10
**Tomada por**: Ithalo Mendes (PM)
**Status**: APROVADA

---

## Contexto

Terceira rodada de ajustes no report diário do PAM no mesmo dia (ver as duas decisões relacionadas
abaixo). O Ithalo pediu, nesta ordem:

1. Dar visibilidade a **novas prioridades que entraram na esteira**, além da lista completa de **em
   teste** e da **próxima maior prioridade de cada dev**.
2. **Sempre ler comentários** para trazer contexto quando fizer sentido.
3. (Mensagem à parte, no meio da execução) **Trocar para um único report do PAM** — não fazia mais
   sentido ter uma página por squad; juntar os dois times.
4. (Mensagem à parte, com link) **Centralizar tudo como subpágina da página `8ccvn07-50171`** — o
   Ithalo já tinha renomeado/reorganizado a página "Resumo Executivo — PAM" para **"Report Status —
   PAM"** diretamente no ClickUp, em paralelo à sessão.

## Decisão

### Fusão num único report

`public/index.html`: removida a distinção `TOP_PAGE_NAMES` (por squad) + `RESUMO_TOP_PAGE_NAME` — agora
existe só `TOP_PAGE_NAME = "Report Status — PAM"`. `computeDailyPamData()` substitui
`computeDailySquadData()`: busca tarefas das duas squads, tagueia cada uma com `squadKey`/`squadLabel`,
e classifica tudo junto nos 5 baldes. A página final tem uma tabela pequena de quebra por squad (pra não
perder de onde vem cada número) mas todas as listas (Novas prioridades, Em teste, Finalizado, Bloqueado,
Próxima prioridade por dev) são únicas, com a tag de squad em cada linha.

As páginas antigas ("Report Status: Plataforma", "Report Status: Backoffice & Integrações") ficam órfãs
— a API do ClickUp não permite apagar página de Doc.

### Três recortes adicionais

Não são um 6º status — são outra lente sobre o mesmo conjunto, podendo se sobrepor aos 5 baldes:

- **Novas prioridades**: tarefas de Execução com `date_created` hoje. Não captura tarefa antiga movida de
  Backlog pra Execução hoje (ClickUp não expõe histórico de mudança de lista sem custo de N+1 chamadas) —
  limitação aceita e documentada, não escondida.
- **Em teste**: virou lista completa, igual Finalizado/Bloqueado já eram.
- **Próxima prioridade por dev**: para cada responsável com tarefa em Pendente, mostra só a de maior
  prioridade (`urgent > high > normal > low > sem prioridade`).

### Leitura de comentários

Endpoint novo `GET /api/task/:id/comments` em `server.js` (reaproveita `fetchTaskComments`, já existente
para `/api/daily-activity`, agora exposto também para tarefa avulsa — cuidado de ordem de rota: checado
antes da rota genérica `/api/task/:id`, senão nunca seria alcançado).

Aplicado só ao recorte de Novas prioridades + Bloqueado + Próxima prioridade por dev (tipicamente
15-25 tarefas, não o board inteiro). Dois caminhos de decisão sobre "quando faz sentido":
- **Botão na interface** (sem LLM): filtro mecânico por tamanho (>15 caracteres) — não julga relevância
  de verdade, só evita citar "ok"/emoji como se fosse contexto.
- **Via Claude Code** (usado nesta execução): leitura real de cada comentário, decisão editorial do que
  agrega contexto, resumo em 1 linha.

Essa leitura de comentários **encontrou um sinal que a contagem sozinha não mostraria**: a tarefa "Novas
prioridades" *"Suspeita de falha na integração PAM ↔ Smartico (evento bet-win) permitindo cumprimento
indevido de missões via compra de bônus + rollback de aposta"* tinha um comentário do Ithalo explicando
que promoções de risco já foram desativadas como mitigação, mas a correção definitiva segue sem
prioridade confirmada com o Ícaro. Isso subiu para o resumo executivo do dia como um dos 3 pontos que
pedem decisão — sem ler o comentário, o report mostraria só "6 novas prioridades", sem sinalizar que uma
delas é um risco financeiro/de fraude em aberto.

### Nome de página

Confirmado via chamada direta à API v3 (`GET .../docs/8ccvn07-68891/pages`) que a página `8ccvn07-50171`
se chama **"Report Status — PAM"** — o Ithalo já tinha renomeado a antiga "Resumo Executivo — PAM"
direto no ClickUp. `TOP_PAGE_NAME` atualizado para esse nome.

## Trade-offs Aceitos

- **"Novas prioridades" não captura reprioritização** (tarefa antiga movida de Backlog para Execução
  hoje) — só tarefa genuinamente nova. Se isso importar na prática, é extensão futura (custaria uma
  chamada de histórico por tarefa).
- **O filtro de comentário do botão (sem LLM) é mecânico, não editorial** — só evita ruído óbvio
  (comentário curto). A curadoria de verdade (como a do risco PAM↔Smartico) só acontece quando alguém
  pede pro Claude Code gerar o report.
- Página antiga fica órfã no Doc (sem meio de apagar via API) — histórico poluído, não removível.

## O que mudaria a decisão

- Se o volume de "novas prioridades"/"bloqueados"/"próxima prioridade" crescer muito, o custo de
  `/api/task/:id/comments` por tarefa (N+1) pode precisar de cache ou de um limite de quantas tarefas
  buscam comentário.
- Se o Ithalo quiser capturar reprioritização de Backlog→Execução, é uma extensão nova, não um ajuste
  deste desenho.

## Impacto

- **Produto**: nenhum módulo de produto afetado — ferramenta interna de operação do PM.
- **Técnico**: `tools/radar-produto/server.js` (`date_created` em `normalizeTask`, rota
  `GET /api/task/:id/comments`) e `tools/radar-produto/public/index.html` (fusão + 3 recortes +
  comentários) alterados. `README.md` atualizado. Script headless de publicação (fora do repositório,
  scratchpad de sessão) atualizado para espelhar a mesma lógica. Testado ao vivo — página
  "Report Status — PAM" republicada com os 5 status, os 3 recortes novos e comentários curados.
- **Processo**: nenhum.

## Links

- Código: `tools/radar-produto/server.js`, `tools/radar-produto/public/index.html`
  (`computeDailyPamData`, `buildPamDailyMarkdown`, `fetchLatestComment`), `tools/radar-produto/README.md`
- Doc de destino: [ClickUp — Report Status — PAM](https://app.clickup.com/9006076935/docs/8ccvn07-68891/8ccvn07-50171)
- Decisão relacionada (correção do "Ativos" enganoso): [[2026-08-10-report-diario-pam-corrige-ativos-e-adota-rag]]
- Decisão relacionada (taxonomia de 5 status + resumo executivo): [[2026-08-10-report-diario-pam-5-status-e-resumo-executivo]]
- Decisão relacionada (criação original do report diário): [[2026-08-10-report-diario-pam-extensao-radar-produto]]
