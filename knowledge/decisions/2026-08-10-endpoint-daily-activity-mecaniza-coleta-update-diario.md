# Coleta do update diário por pessoa migrada de chamadas MCP do agente para endpoint mecanizado no radar-produto

**Data**: 2026-08-10
**Tomada por**: Ithalo Mendes (PM)
**Status**: APROVADA

---

## Contexto

A rotina `/orquestrador` de update diário (Feito/Pendente/Pontos de atenção/Impedimentos/Próximos
passos por pessoa dos times do Ithalo, enviado via ClickUp Chat) rodou pela primeira vez delegando a
coleta inteira a um agente (`agente-delivery`), que fez ~29 chamadas de ferramenta MCP do ClickUp
(`find_member_by_name`, `filter_tasks`, `get_task_comments`, `time_in_status`) para 10 pessoas — ~185k
tokens e ~385s, com risco de rate limit explicitamente antecipado no próprio comando.

Na sequência, o Ithalo pediu para analisar o padrão do `report-semanal` do claude-os
(`scripts/weekly_report.py`) — que resolve exatamente esse tipo de gargalo fazendo toda a coleta e o
cálculo **em disco**, via chamada direta à API REST do ClickUp, e não através de contexto de LLM — e
aplicar a mesma lógica ao update diário.

Uma checagem de duplicidade (mesmo princípio já usado na decisão de hoje sobre o report diário do PAM)
achou `tools/radar-produto/`: app local que já fala direto com a API REST do ClickUp com token pessoal,
e que ganhou hoje mais cedo um botão de publicação diária (contagens objetivas — concluídas/ativas/
bloqueadas — sem síntese narrativa nem leitura de comentário).

## Opções Consideradas

1. **Manter a coleta dentro do agente/MCP**, só reduzindo o número de chamadas.
   - Contras: não elimina o risco de rate limit nem o custo de token; o problema é estrutural (LLM
     dirigindo dezenas de chamadas exploratórias), não um ajuste fino de quantidade.
2. **Construir um script novo e separado**, à parte, replicando `weekly_report.py` para o recorte diário.
   - Contras: duplicaria a autenticação e o acesso à API que `tools/radar-produto/server.js` já tem e já
     mantém — exatamente o anti-padrão identificado na decisão de hoje sobre o report diário do PAM.
3. **Estender `tools/radar-produto/server.js`** com um endpoint de coleta mecanizada
   (`/api/daily-activity`), consumido pelo passo de síntese do `/orquestrador`.
   - Prós: reaproveita a conexão com a API do ClickUp já existente e testada; mantém uma única
     integração fazendo a coleta, em vez de duas.
   - Contras: acopla mais uma responsabilidade ao `radar-produto`.

## Decisão

Optou-se pela **Opção 3**. Implementado em `tools/radar-produto/server.js`:

- `GET /api/daily-activity?squads=<chaves>&date=YYYY-MM-DD` — busca as tarefas das squads pedidas
  (incluindo fechadas), filtra para as que tiveram `date_closed` ou `date_updated` caindo no dia-alvo
  (mesmo tipo de proxy que o `weekly_report.py` usa, já que a API do ClickUp não expõe log de atividade
  bruto por data), e só para esse recorte já reduzido busca comentários (filtrados para o dia) e
  histórico de status (`time_in_status`) — com concorrência limitada a 4 chamadas simultâneas
  (`mapLimit`) para não recriar do lado do script o mesmo risco de rate limit que essa mudança existe
  para evitar do lado do agente.
- O endpoint **não** agrupa por pessoa, não exclui liderança do recorte, e não escreve a síntese
  narrativa — isso continua sendo trabalho do passo seguinte (o `/orquestrador`), que agora recebe um
  JSON pequeno e pronto em vez de fazer a exploração ele mesmo.

Testado ao vivo contra a API real (squads `plataforma,backoffice`, data `2026-08-07`): 15 tarefas
retornadas em ~4.2s, cobrindo Linecker, Railton, Primo, kennedy Souza, Melk, Tony, Rayan, Allison e
Hugo — inclusive uma tarefa do Hugo (`868khq2hy`, reporte diário WhatsApp) que a passagem anterior via
agente não tinha capturado. Ícaro e Alex não aparecem no recorte — consistente com a cobertura parcial
que a própria execução anterior via agente já tinha reportado para essas duas pessoas.

## Trade-offs Aceitos

- O passo de síntese narrativa (Feito/Pendente/Pontos de atenção/Impedimentos/Próximos passos) continua
  exigindo uma chamada de LLM — não é possível mecanizar essa parte como as contagens do report semanal,
  porque exige leitura interpretativa de comentário, não contagem. O ganho é eliminar a exploração via
  MCP, não eliminar o LLM do processo inteiro.
- O `/orquestrador` ainda precisa ser ajustado, na próxima execução da rotina, para chamar
  `GET /api/daily-activity` (via `curl`/fetch local) em vez de instruir um agente a fazer a coleta via
  MCP — essa mudança de instrução não foi persistida em nenhum arquivo do repositório porque a rotina em
  si não está salva como skill/comando reutilizável (foi colada inline no prompt do usuário); fica como
  próximo passo caso o Ithalo queira fixá-la.
- `date_updated` como proxy de "teve atividade no dia" é mais largo que `date_closed` — pode incluir
  tarefas tocadas por motivo não relacionado ao trabalho da pessoa (ex.: reindexação, edição de campo por
  terceiro). O passo de síntese precisa continuar filtrando por relevância, não tratar toda tarefa
  retornada como atividade confirmada.

## O que mudaria a decisão

- Se a rotina de update diário virar um cron/rotina persistida (via `/schedule` ou similar), o ponto de
  chamada ao endpoint precisa estar no corpo dessa rotina, não só documentado aqui.
- Se o volume de tarefas "tocadas no dia" crescer a ponto de `mapLimit(tasks, 4, ...)` ainda esbarrar em
  rate limit, considerar reduzir a concorrência ou passar a usar webhooks do ClickUp em vez de polling.

## Impacto

- **Produto**: nenhum módulo de produto afetado — ferramenta interna de operação do PM.
- **Técnico**: `tools/radar-produto/server.js` (+ `normalizeTask` ganhou `date_updated`) e `README.md`
  alterados. Testado ao vivo (só leitura) contra o workspace Vertical Tech real.
- **Processo**: a próxima execução da rotina `/orquestrador` de update diário deve consumir
  `/api/daily-activity` em vez de instruir um agente a coletar via MCP.

## Links

- Código: `tools/radar-produto/server.js`, `tools/radar-produto/README.md`
- Referência de padrão: `report-semanal` (claude-os) — `.claude/skills/report-semanal/SKILL.md`,
  `scripts/weekly_report.py`
- Decisão relacionada (mesmo dia, mesmo princípio de não duplicar): [[2026-08-10-report-diario-pam-extensao-radar-produto]]
