# Radar de Produto (aplicação local)

Painel de acompanhamento de Delivery do ClickUp (workspace Vertical Tech) — filtros por squad,
pessoa, etapa e prioridade, KPIs, edição inline de status/prioridade/prazo/responsáveis (restrita aos
squads que Ithalo lidera como PM: Plataforma e Backoffice & Integração), visão por Frente
(Épico pai) com reatribuição direta de tarefas "sem frente", geração de status report editável
exportável em PDF, e publicação diária de report consolidado (PAM) em páginas do ClickUp Doc.

Roda 100% local: um pequeno servidor Node (sem dependências) chama a API do ClickUp usando seu token
pessoal, e serve a página em `http://localhost`. O token nunca chega ao navegador.

## Configurar

1. Gere um token pessoal no ClickUp: **Configurações → Apps → API Token**.
2. Copie o arquivo de exemplo e cole o token nele:
   ```
   cp .env.example .env
   ```
   Edite `.env` e preencha `CLICKUP_API_TOKEN=pk_...`. Esse arquivo já está no `.gitignore` da raiz do
   repositório — nunca será versionado.

## Rodar

```
node server.js
```

Abra `http://localhost:4173` no navegador (ou a porta que você definir em `PORT` no `.env`).

## Estrutura

- `server.js` — servidor HTTP local (Node nativo, zero dependências). Expõe `/api/tasks/:squad`,
  `/api/task/:id`, `/api/members`, `/api/daily-activity` (ver abaixo), `PUT /api/task/:id` (API REST v2
  do ClickUp, `https://api.clickup.com/api/v2`), e `POST /api/report-doc/page` (API v3 de Docs,
  `https://api.clickup.com/api/v3`) — todos com o token do `.env`.
- `public/index.html` — a página em si (mesma UI do protótipo original em Artifact, adaptada para
  consumir a API local em vez do conector MCP).

## Coleta mecanizada para o update diário por pessoa (`/api/daily-activity`)

Mesmo princípio do `report-semanal` do claude-os (`scripts/weekly_report.py`): a coleta e a filtragem
rodam **em disco**, contra a API REST do ClickUp, em vez de um agente fazer dezenas de chamadas
exploratórias via MCP (`find_member` → `filter_tasks` → `get_task_comments` → `time_in_status`, por
pessoa) — foi assim que a rotina `/orquestrador` de update diário rodou da primeira vez, com risco real
de rate limit e ~185k tokens gastos só na coleta.

```
GET /api/daily-activity?squads=plataforma,backoffice&date=2026-08-07
```

- `squads` (obrigatório): chaves de `SQUADS` separadas por vírgula (`plataforma`, `backoffice`,
  `produto`). Tarefas que aparecem em mais de uma squad são deduplicadas por `id`.
- `date` (opcional, `YYYY-MM-DD`, fuso America/Sao_Paulo): dia-alvo. Default é hoje.

Devolve `{ date, tasks: [...] }`, só com as tarefas cujo `date_closed` ou `date_updated` caiu naquele
dia — o mesmo tipo de proxy que o `weekly_report.py` usa, porque a API do ClickUp não expõe log de
atividade bruto por data. Cada tarefa do recorte já vem com `assignees`, `comments` (filtrados para o
dia; `null` significa "falha ao buscar", **não** "sem comentários") e `status_history`
(`{ current, history }`, via `time_in_status`).

Como o recorte por `date_closed`/`date_updated` normalmente já reduz para dezenas de tarefas (não
centenas), buscar comentário e histórico por tarefa vira viável — o servidor limita a 4 chamadas
concorrentes (`mapLimit`) para não recriar do lado do script o mesmo risco de rate limit que essa coleta
existe para evitar do lado do agente.

**O que este endpoint não faz — e não deveria fazer**: agrupar por pessoa, excluir liderança do recorte,
ou escrever a síntese narrativa (Feito/Pendente/Pontos de atenção/Impedimentos/Próximos passos). Isso é
trabalho de interpretação sobre um conjunto já pequeno e bem definido — cabe ao passo seguinte (o
`/orquestrador` ou quem consumir o endpoint), não ao script de coleta.

## Visão por Frente e reatribuição de Épico

O modo "Ver por frente" agrupa as tarefas do squad ativo pela tarefa-pai (Épico) — mesmo conceito de
"Frente" usado no report semanal do time. Tarefas sem `parent`, e que ninguém referencia como pai, caem
no grupo "Sem frente". Cada linha editável tem um seletor para associar/reatribuir a um Épico existente
(`PUT /task/:id` com `parent`) — candidatos são limitados a Épicos **da mesma lista** (Backlog ou
Execução) da tarefa, porque o ClickUp não permite parent fora da lista da subtarefa. Não é possível
"desassociar" uma tarefa de volta para "sem frente" só reatribuindo — a API do ClickUp não aceita
`parent: null` numa subtarefa existente (só reatribuir para outro pai válido).

## Publicação diária no ClickUp Doc (escopo PAM, um único report)

O botão "Publicar report do dia no Doc" gera/atualiza, no Doc
[`8ccvn07-68891`](https://app.clickup.com/9006076935/docs/8ccvn07-68891), **uma única** subpágina do dia
(nome = data `DD/MM/AAAA`) sob **"Report Status — PAM"** — Plataforma e Backoffice & Integração fundidos
num relatório só (decisão do Ithalo, 10/08/2026; antes eram 3 páginas: uma por squad + um resumo
consolidado à parte). Rodar de novo no mesmo dia **atualiza** a subpágina existente (não duplica) — o
servidor busca a árvore de páginas do Doc antes de decidir criar ou atualizar.

A página tem, nesta ordem (template fechado com o Ithalo em 10-11/08/2026, ver decisão relacionada):
título "Resumo do dia dos times PAM", resumo executivo em texto, os 5 números do dia (sem tabela de
quebra por squad — ele tirou isso ao editar manualmente), Novas prioridades, Finalizado hoje, Em teste,
Bloqueado, Próxima prioridade por dev e Próxima prioridade por designer. As duas últimas seções agrupam
por squad com subtítulo em negrito (`**Time Plataforma:**` / `**Time Backoffice & Integrações:**`), não
uma lista achatada misturando os dois times.

### Referência de tarefa é URL solta — "Mencionar tarefa" não é possível via API, mas o Ithalo converte à mão

Cada item de tarefa é escrito como a **URL solta** (`taskRef()` em `public/index.html` retorna só
`t.url`, sem colchetes) — decisão revertida em 18/08/2026 (ver decisão relacionada). Entre 10/08 e
17/08/2026 o formato era `[Nome da tarefa](url)` (hyperlink markdown); o Ithalo pediu para voltar a URL
solta porque **é assim que ele consegue, depois, converter a referência num chip nativo do ClickUp**:
seleciona a URL visível no doc e cola de novo no editor — esse *paste* dentro do editor visual é o que
aciona a conversão automática para "Mencionar tarefa" (chip com status ao vivo e avatar), não algo que a
API grava. Com a URL escondida atrás de um texto de link, ele precisaria "copiar link" em vez de
selecionar texto — fricção desnecessária dado que ele faz essa conversão tarefa por tarefa, todo dia, ao
revisar o report. **Sem responsável nem squad no fim da linha** continua valendo (removido em 11/08/2026);
só "Próxima prioridade por dev/designer" mostra nome de pessoa antes da URL, porque ali o nome é o rótulo
da linha, não repetição.

Um formato de URL alternativo foi testado e descartado em 11/08/2026: algumas tarefas têm um "ID
customizado" (ex.: `VL-14233`), que permite uma URL longa `.../t/{team_id}/{custom_id}` em vez da curta
`.../t/{id}`. Cheguei a suspeitar que esse formato pudesse acionar algo diferente na renderização — não
aciona. Testado via API: os dois formatos são normalizados de forma **idêntica** quando publicados como
link markdown (`[url](url)`). A diferença que apareceu numa edição manual do Ithalo era só reflexo de ele
ter copiado o link pelo botão "Copy Link" do ClickUp (que usa o ID customizado quando a tarefa tem um
configurado) — irrelevante agora que o formato publicado é a URL solta, sem link markdown nenhum.

**"Mencionar tarefa" (chip nativo — chevron, status ao vivo, avatar do responsável) continua impossível
de gerar via API**, ponto confirmado na documentação oficial
(["Docs API Limitations"](https://developer.clickup.com/docs/docsimportexportlimitations)): **"Embed a
task" está explicitamente na lista do que a API de Docs NÃO suporta** — é recurso exclusivo do editor
visual, sem representação em `text/md` nem `text/plain` (as únicas duas formas que `content_format`
aceita). Isso não muda com a URL solta: uma URL gravada via API **não** auto-converte para chip só por
estar solta — ela aparece como texto simples (às vezes nem clicável) até alguém colar de novo dentro do
editor visual. A URL solta no conteúdo publicado existe para viabilizar *essa* conversão manual
subsequente, não para contorná-la via API. Ver decisão relacionada para o histórico completo (inclusive a
tentativa anterior, de 10/08/2026, que testou URL solta esperando um resultado diferente e confirmou o
mesmo comportamento).

### Os 5 status do dia (decisão do Ithalo, 10/08/2026)

Definições (`computeDailyPamData`/`classifyStatus5` em `public/index.html`). Cada tarefa cai em
**exatamente um** dos 5 baldes — não há sobreposição nem "toda tarefa não fechada" genérico:

| Status | Regra |
|---|---|
| **Finalizado** | `date_closed` caiu hoje, calculado no fuso de São Paulo — único balde com recorte de dia |
| **Em teste** | status atual em Teste Dev/em Dev/Homolog/Alpha |
| **Em desenvolvimento** | status atual em Desenvolvimento, Revisão Técnica, Deploy p/ Alpha/PRD |
| **Pendente** | status atual é "Pendente" |
| **Bloqueado** | status atual contém "bloque" |

Duas regras de escopo, aplicadas antes de classificar:
- **Só a lista de Execução conta** — Backlog fica de fora (mesma regra do `report-semanal` do
  claude-os: "Abas 1 e 2 olham SÓ Execução"). É por isso que status só de Backlog/Discovery (Pronto p/
  Design, Em Design, Em Refinamento) nunca aparecem aqui — se aparecerem, é sinal de tarefa na lista
  errada.
- **Subtarefas são ignoradas** (`task.parent` preenchido) — pedido do Ithalo para não inflar a contagem
  com o detalhamento interno de uma tarefa-pai.
- Tarefas Canceladas/Despriorizadas são excluídas de todos os baldes (`ST_CANCEL`) — não representam
  trabalho em curso nem risco.
- Uma tarefa fechada em **outro** dia (não hoje) não conta em nenhum balde — já não é nem "hoje" nem
  trabalho em curso.
- Se sobrar uma tarefa de Execução sem subtarefa, sem cancelamento, com status fora dos 5 esperados, o
  script avisa no console (`[report diário] ... status fora dos 5 esperados`) em vez de descartar
  silenciosamente — não deveria acontecer, mas se acontecer é sinal de status novo no board.

**Antes desta revisão**, o segundo número chamava-se "Ativos" e contava toda tarefa não fechada de
Backlog + Execução — produzindo números como 55/56 num board com só ~10-20 itens realmente em execução
(o Ithalo notou o número estranho no mesmo dia em que o report foi publicado pela primeira vez;
ver decisão relacionada abaixo).

### Três recortes adicionais (pedido do Ithalo, 10/08/2026)

Não são um 6º status — são outra lente sobre o mesmo conjunto de tarefas, e por isso podem se sobrepor
com os 5 baldes acima (uma tarefa pode ser, ao mesmo tempo, "nova" e "em desenvolvimento").

- **Novas prioridades**: tarefas de Execução com `date_created` hoje. Captura tarefa **nova** que já
  nasceu priorizada. **Não captura** uma tarefa antiga que só hoje foi movida de Backlog para Execução —
  a API de listagem do ClickUp não expõe histórico de mudança de lista sem uma chamada por tarefa; se
  esse caso importar, é uma extensão futura, não o comportamento atual.
- **Em teste**: agora lista as tarefas (não só a contagem), igual já acontecia com Finalizado e
  Bloqueado.
- **Próxima prioridade por dev/designer**: para cada responsável com pelo menos uma tarefa em
  **Pendente**, mostra a de maior prioridade (`urgent` > `high` > `normal` > `low` > sem prioridade) —
  não a soma, só a próxima. Uma tarefa com mais de um responsável aparece na linha de cada um. Split
  dev/designer por roster fixo (`DESIGNERS` em `public/index.html`, hoje Allison Macedo e Mateus
  Sperandio, espelha `knowledge/domains/pessoas.md`) — quem não é designer conhecido cai em "por dev".

### Comentário como contexto — usar com parcimônia, não por padrão

Pedido original do Ithalo: trazer contexto dos comentários nas seções que precisam de explicação — Novas
prioridades, Bloqueado e Próxima prioridade por dev/designer. Endpoint: `GET /api/task/:id/comments`
(devolve os comentários da tarefa, mais recente primeiro).

**Correção de 11/08/2026**: a primeira versão anexava comentário em quase toda tarefa do recorte (~9 de
24). O Ithalo cortou quase tudo ao editar manualmente — manteve 1, e mesmo esse como texto inline
(`Nome (url): comentário`), não como citação em bloco separado. A regra passou a ser: só incluir quando
o comentário é a **única forma de explicar por que aquele item pede atenção** (ex.: o card "Suspeita de
falha PAM↔Smartico" tinha um comentário revelando que o impacto financeiro já foi estimado em R$260 mil
— sem isso, só a lista de "Novas prioridades" não mostraria a gravidade), não como anexo automático.

Duas formas de decidir "quando faz sentido", dependendo de quem publica:
- **Pelo botão na interface** (sem LLM): `fetchLatestComment()` mostra o último comentário só se tiver
  mais de 15 caracteres — filtro mecânico, existe só pra não citar um "ok"/emoji de reação como se fosse
  contexto. Não julga relevância de verdade nem aplica a parcimônia acima — é um piso, não o padrão
  desejado.
- **Via Claude Code**: lê os comentários reais do recorte, aplica a parcimônia (a maioria fica de fora),
  resume em 1 linha inline quando entra, e publica.

### Resumo executivo em texto

A página tem um parágrafo de "Resumo do dia" em texto corrido, no tom de voz do Ithalo — não é gerado
pelo app local (não há LLM embutido em `server.js`/`public/index.html`, de propósito, pra manter o app
100% local e sem dependência externa além da API do ClickUp). Dois caminhos pra preencher:
1. **Via Claude Code** (como foi feito em 10/08/2026): pede pro Claude olhar os números do dia e
   escrever o resumo, que publica direto chamando `/api/report-doc/page`.
2. **Pelo botão na interface**: `publishDailyReport()` abre um `window.prompt()` pedindo o texto (colar
   algo já escrito, ou deixar em branco). Em branco vira o placeholder
   `_(resumo executivo não informado)_` — a página nunca fica sem essa seção, só sinaliza que ninguém
   preencheu ainda.

**Guia de tom de voz**: o arquivo original (`~/Downloads/Guia_Tom_de_Voz_Ithalo_Azevedo.md`) não foi
localizado em 10/08/2026 — pode ter sido movido ou apagado. Na mesma conversa, o Ithalo colou uma
descrição completa do próprio tom de voz (análise externa, validada por ele como fiel), que virou a
fonte primária guardada na memória `tom-de-voz-ithalo`. Regra mais relevante para este report
especificamente: **para diretoria, reduza contexto e aumente conclusão** — o texto executivo não deve
reexplicar os itens que a lista logo abaixo já mostra; deve terminar em decisão ou próximo passo
explícito, não em número neutro. Se o arquivo original for localizado, vale revisar os textos contra ele.

Correções específicas aprendidas em 11/08/2026 (edição manual do Ithalo em cima de um texto que ele achou
confuso — ver memória `feedback-report-diario-pam-formato` para o histórico completo):
- Declarar o fato direto, não emoldurar com "o caso que estamos chamando de X" — ex.: "o caso aconteceu
  no jogo 'Pinata Wins'", não "o caso que chamamos de Pinata Wins" (era o nome real do jogo, não um
  apelido interno).
- "Mitigado" ≠ "corrigido" — usar o verbo certo conforme a ação foi paliativa ou definitiva.
- Sem fricção de processo interno no resumo ("fulano cobrou retorno sem resposta", "precisa alinhar com
  fulano amanhã") — relatar fato e status, não quem está pressionando quem.
- Item secundário ou não confirmado não entra no parágrafo executivo — fica só dentro da seção onde a
  tarefa aparece (ex.: Bloqueado), sem repetir como comentário na abertura.
- A frase de transição pro board vai direto pros bullets de número, sem comentário depois dela.

**Nome de página é hardcoded**: `TOP_PAGE_NAME` em `public/index.html` precisa ficar em sincronia com o
nome real da página de topo no Doc do ClickUp. Se renomear a página lá, atualize aqui também — foi
exatamente essa dessincronia que aconteceu em 10/08/2026 quando o Ithalo renomeou/reorganizou a página
"Resumo Executivo — PAM" direto no ClickUp para "Report Status — PAM": o código precisou ser atualizado
pra apontar pro novo nome.

## Limitações conhecidas

- Os IDs de squad/lista/folder estão fixos no código (`server.js`, objeto `SQUADS`) — refletem a
  estrutura atual do workspace Vertical Tech. Se a estrutura de Folders/Listas mudar no ClickUp, esses
  IDs precisam ser atualizados manualmente.
- **Mudança estrutural de 2026-09-10**: o folder Discovery & Design (e a lista compartilhada
  `901114029780`) foi removido do ClickUp — descoberta agora é uma faixa de status dentro do Backlog de
  cada squad, não mais uma esteira própria (ver `knowledge/domains/processo.md`). A categoria "Discovery"
  deste dashboard (squad, filtro de etapa, KPIs) está desatualizada e pendente de revisão — o servidor
  já não referencia mais a lista removida, mas o app ainda não foi redesenhado para mostrar a faixa de
  descoberta embutida no Backlog nem as novas Sprints (Plataforma e Backoffice já migraram para Sprint
  Folders nativos do ClickUp; Produto ainda não).
- O campo "Tipo" da tarefa mostra apenas o tipo padrão ou um ID numérico para tipos customizados — a
  API do ClickUp não resolve o nome do tipo customizado sem uma chamada adicional que não foi implementada.
  Por isso o report diário e o Opex×Capex do report semanal (Bug vs. não-Bug) **não** foram implementados
  no report diário — precisaria resolver `custom_item_id` por tarefa, custo N+1 chamadas.
- **A API v3 de Docs do ClickUp mostrou instabilidade em uso real**: o parâmetro documentado
  `max_page_depth=-1` ("sem limite") retorna 500 nesta API — o servidor omite o parâmetro (o padrão já
  retorna a árvore completa). Também houve um 500 intermitente isolado numa chamada de edição de página
  sem causa aparente (reproduzida uma vez, não reproduzida de novo com o mesmo payload) — o servidor
  tenta de novo uma vez após falha 5xx antes de desistir.
- Reatribuir Épico ("Ver por frente") nunca foi testado ao vivo pelo Claude Code de propósito — é uma
  mudança visível na hierarquia real do board, que o time inteiro vê; o primeiro teste real é ao usar o
  seletor no painel de verdade, não via automação.
- **As páginas antigas "Report Status: Plataforma" e "Report Status: Backoffice & Integrações"** (do
  desenho anterior, com uma página por squad) ficaram órfãs depois da fusão em "Report Status — PAM" —
  o histórico delas continua no Doc, só não recebem mais atualização.
- **A API do ClickUp não permite apagar página de Doc** — confirmado em 10/08/2026 (uma tentativa de
  `DELETE` não tem endpoint correspondente na v3). **Mas dá pra apagar pela interface do ClickUp**:
  confirmado em 11/08/2026, quando uma página de teste criada via API sumiu depois de o Ithalo mexer no
  Doc — uma tentativa de editá-la de novo via API voltou `403 DELETED`. Ou seja: página de teste
  descartável (`[pode apagar]`) precisa mesmo ser removida à mão pelo Ithalo; o Claude não tem esse
  poder via API, mas o Ithalo tem via UI.
- **`/api/task/:id/comments` custa uma chamada por tarefa** — só é chamado para o recorte já pequeno de
  Novas prioridades + Bloqueado + Próxima prioridade por dev (tipicamente 15-25 tarefas), nunca para o
  board inteiro. Se esse recorte crescer muito, reconsiderar concorrência/rate limit.
