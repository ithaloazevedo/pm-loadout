# Report diário do PAM: corrige truncamento de paginação e define método para gerar report de dia anterior

**Data**: 2026-08-18
**Tomada por**: Ithalo Mendes (PM), executado por Claude Code
**Status**: APROVADA

---

## Contexto

Pedido: gerar e publicar o "Resumo do dia dos times PAM" de **17/08/2026** (ontem), não do dia corrente —
primeira vez que o report roda em modo retroativo (D+1), não no mesmo dia. O app `tools/radar-produto` foi
desenhado assumindo publicação no mesmo dia (ver decisões de 10-11/08/2026).

## Investigação

Ao coletar os dados de 17/08 via `/api/tasks/:squad?include_closed=true` (necessário para o balde
"Finalizado", que exige tarefas fechadas), os números batiam com uma segunda coleta feita direto na API
do ClickUp (via `curl` com token pessoal) **só quando não havia paginação envolvida**. Comparando as duas
fontes achei uma divergência: a chamada do app trazia exatamente 100 tarefas para a lista Execução de
cada squad — número redondo demais para ser coincidência.

Confirmado com paginação manual (`page=0,1,2...` direto na API do ClickUp): a lista Execução de
**Plataforma tem 291 tarefas reais** (100+100+91) e a de **Backoffice & Integração tem 149** (100+49)
quando `include_closed=true` — `fetchSquadTasks` em `server.js` não paginava, então descartava
silenciosamente tudo além da primeira página. Sem closed (uso normal do dashboard, dezenas de tarefas
abertas) isso nunca estourava 100 e passou despercebido; com closed=true (usado só pelo botão de publicar
report e por `/api/daily-activity`) o corte era real — cerca de 2/3 das tarefas fechadas históricas
ficavam de fora da resposta.

Isso também significa que **execuções anteriores do report diário (10 e 11/08/2026) podem ter usado dados
truncados** sempre que o balde "Finalizado" dependeu dessa chamada — não foi possível confirmar
retroativamente o tamanho do impacto (não há como saber quantas tarefas a página 2/3 continha naqueles
dias sem refazer a chamada, que hoje já reflete outro estado do board).

## Decisão

1. **Corrigido `fetchSquadTasks` em `tools/radar-produto/server.js`**: nova função
   `fetchListTasksAllPages(listId, includeClosed)` pagina (`page=0,1,2...`) até `last_page: true` ou lista
   vazia, com teto de segurança de 50 páginas. `fetchSquadTasks` passou a usar essa função por lista em vez
   da chamada única sem `page`. Servidor reiniciado e testado: Plataforma Execução agora retorna 291
   tarefas (antes 100).
2. **Método para "report de um dia anterior"** (não documentado antes, porque o app nunca tinha rodado
   assim): os baldes Finalizado/Novas prioridades foram recalculados com corte de data (`date_closed`/
   `date_created` dentro da janela 00:00–23:59 de 17/08, fuso America/Sao_Paulo) sobre o snapshot completo
   e paginado. Os baldes Em teste/Em desenvolvimento/Pendente/Bloqueado **não têm como ser reconstruídos
   com exatidão histórica** — a API do ClickUp não expõe snapshot de status por data sem custo alto
   (histórico por tarefa via `time_in_status`, N chamadas); usar o status **atual** (no momento da geração,
   18/08) é a mesma aproximação que o app já assume para todo report (ele é, por design, uma foto do
   status vigente, não um histórico). Diferença prática nesse caso: como a geração ocorreu 1 dia depois,
   qualquer tarefa que mudou de balde entre 17 e 18/08 aparece no balde de hoje, não no de ontem — risco
   pequeno (poucas tarefas mudam de status de um dia pro outro), mas real.
3. Report publicado na subpágina `17/08/2026` do Doc "Report Status — PAM"
   ([link](https://app.clickup.com/9006076935/docs/8ccvn07-68891/8ccvn07-50331)).

## Trade-offs Aceitos

- Não foi feita nenhuma tentativa de corrigir retroativamente os reports de 10/11-08/2026 — os números
  publicados naqueles dias ficam como estão; o bug só foi corrigido daqui para frente.
- A aproximação "status atual" para os 4 baldes que não são de fechamento continua valendo mesmo em modo
  retroativo — não há orçamento de chamadas (nem endpoint pronto) para reconstruir status histórico exato
  por tarefa via `time_in_status` a cada geração.

## O que mudaria a decisão

- Se o Ithalo quiser reports retroativos exatos (baldes fiéis ao estado real do dia, não ao estado atual),
  seria necessário um novo endpoint que reconstrói status por `time_in_status` por tarefa para a data-alvo
  — custo de N chamadas por tarefa do board inteiro (não só o recorte do dia), provavelmente inviável para
  boards com centenas de tarefas sem cache.
- Se `include_closed=true` continuar sendo usado só para recortes pequenos (como hoje), o teto de 50
  páginas nunca deve ser atingido — se algum dia for, é sinal de crescimento do board que merece revisar o
  teto.

## Impacto

- **Produto**: nenhum módulo de produto afetado — ferramenta interna de operação do PM.
- **Técnico**: `tools/radar-produto/server.js` (`fetchListTasksAllPages`, `fetchSquadTasks`) alterado;
  servidor local reiniciado. Nenhuma mudança em `public/index.html` — o front-end consome o mesmo formato
  de resposta, só que agora completo.
- **Processo**: primeira vez que o report roda em modo retroativo (D+1) — método registrado acima para
  reutilizar se acontecer de novo (ex.: esquecer de publicar num dia).

## Links

- Código: `tools/radar-produto/server.js`
- Doc publicado: [ClickUp — Report Status — PAM, 17/08/2026](https://app.clickup.com/9006076935/docs/8ccvn07-68891/8ccvn07-50331)
- Decisões relacionadas: [[2026-08-11-report-diario-pam-template-final-e-formato-aprendido]],
  [[2026-08-10-report-diario-pam-extensao-radar-produto]]
