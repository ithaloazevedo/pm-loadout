# Report diário do PAM: taxonomia fechada de 5 status (só Execução, sem subtarefa) + resumo executivo em texto

**Data**: 2026-08-10
**Tomada por**: Ithalo Mendes (PM)
**Status**: APROVADA

---

## Contexto

Depois da correção do "Ativos" enganoso (ver decisão relacionada), o Ithalo pediu duas mudanças
adicionais no report diário do PAM publicado no ClickUp Doc:

1. Fechar a taxonomia de status em exatamente 5 categorias: **finalizado, em teste, em desenvolvimento,
   pendente e bloqueado** — e ignorar subtarefas.
2. Incluir, no "Resumo do dia" de cada página, um texto executivo escrito no tom de voz dele.

## Decisão

### Taxonomia de 5 status

Reescrito `computeDailySquadData`/`classifyStatus5` em `tools/radar-produto/public/index.html`:

- Escopo restrito à **lista de Execução** de cada squad (Backlog fica de fora) — mesma regra já usada
  pelo `report-semanal` do claude-os ("Abas 1 e 2 olham SÓ Execução"). Resolve de forma limpa o problema
  de status que só existem em Backlog/Discovery (Pronto p/ Design, Em Design, Em Refinamento) não
  caberem em nenhum dos 5 baldes.
- **Subtarefas excluídas** (`task.parent` preenchido) — pedido explícito do Ithalo, para não inflar
  contagem com o detalhamento interno de uma tarefa-pai.
- Cada tarefa cai em **exatamente um** dos 5 baldes (mutuamente exclusivos, ao contrário do desenho
  anterior que tinha "Em andamento"/"Bloqueados"/"Atrasados" como cortes independentes que podiam se
  sobrepor). "Finalizado" é o único balde com recorte de dia (`date_closed` hoje); os outros 4 são foto
  do status atual.
- Tarefas Canceladas/Despriorizadas continuam excluídas de tudo (`ST_CANCEL`, sem mudança).
- Status fora dos 5 esperados (não deveria sobrar nenhum depois do filtro de Execução) geram aviso no
  console em vez de sumir silenciosamente.
- **"Atrasados" foi removido** da estrutura — não é um dos 5 status pedidos, é um atributo de prazo
  ortogonal ao status. Trade-off aceito conscientemente (ver abaixo).

### Resumo executivo em texto

Adicionado parâmetro `textoExecutivo` em `buildSquadDailyMarkdown`/`buildResumoExecutivoMarkdown`. Não
há geração automática dentro do app local — decisão consciente de manter `server.js`/`public/index.html`
sem dependência de LLM. Dois caminhos: (a) pedir ao Claude Code pra escrever com base nos números do dia
e publicar direto via `/api/report-doc/page`; (b) `window.prompt()` no botão da interface, pra colar um
texto já pronto. Sem preenchimento, cai no placeholder `_(resumo executivo não informado)_`.

Nesta execução (10/08/2026), os 3 textos (Plataforma, Backoffice, PAM) foram escritos pelo Claude com
base nos números reais do dia, em três rodadas:

1. **1ª versão**, escrita a partir do resumo de tom de voz já guardado na memória `tom-de-voz-ithalo`
   (arquivo original `~/Downloads/Guia_Tom_de_Voz_Ithalo_Azevedo.md` não encontrado — busca por nome,
   por conteúdo via Spotlight e checagem de sessões antigas do Claude Desktop não achou o texto real).
   Publicada, mas com frases mais telegráficas do que o guia pedia.
2. **2ª versão**, revisada contra o resumo da memória (estrutura contextualizar→desenvolver→
   implicações→síntese, "Na prática...", frases de ritmo variado) e republicada.
3. **3ª e versão final**: o Ithalo colou, na mesma conversa, uma descrição completa do próprio tom de voz
   (análise externa via ChatGPT, validada por ele como fiel) — bem mais rica que o resumo que estava na
   memória. Essa descrição virou a **fonte primária** de tom de voz (substituindo o resumo antigo,
   registrada na memória `tom-de-voz-ithalo`). A regra mais relevante para este report especificamente:
   *"em mensagens para diretoria, reduza contexto e aumente conclusão"* — as versões 1 e 2 estavam
   reexplicando cada bloqueio por extenso dentro do texto (redundante com a lista já linkada logo
   abaixo) e terminando em números neutros em vez de terminar no próximo passo. Os 3 textos foram
   reescritos mais curtos, terminando em decisão/próximo passo explícito, e republicados.

Republicado no Doc real depois da versão final: Plataforma (5 finalizado, 4 em teste, 2 em
desenvolvimento, 4 pendente, 4 bloqueado) e Backoffice & Integrações (4 finalizado, 3 em teste, 12 em
desenvolvimento, 9 pendente, 3 bloqueado) — incluindo o bloqueio do reenvio dos arquivos do SIGAP (prazo
14/08, já conhecido de apuração anterior) destacado nos 3 textos executivos como o item que precisa de
decisão, não só acompanhamento.

## Trade-offs Aceitos

- **"Atrasados" saiu do report.** Um item pode estar "em desenvolvimento" e com `due_date` vencido sem
  que isso apareça em lugar nenhum agora. Se a liderança sentir falta desse sinal de risco, é reintroduzi-
  lo como um recorte adicional (não um 6º status — continua sendo um atributo de prazo, não um estado).
- **O arquivo original do guia de tom de voz não foi encontrado** — a fonte usada na versão final é a
  descrição que o próprio Ithalo colou na conversa (validada por ele), não o arquivo original em
  `~/Downloads`. A memória `tom-de-voz-ithalo` foi atualizada com essa descrição como fonte primária e
  com um aviso sobre o arquivo ausente, para a próxima sessão não repetir a busca.
- **Geração do texto executivo depende de uma sessão do Claude Code** (ou de alguém colar um texto
  pronto no prompt do botão) — não é automático. Se a rotina precisar rodar sem intervenção humana num
  dia, a página vai sair com o placeholder.
- A aba interativa "Gerar Report" (período configurável, exportável em PDF) continua com sua própria
  lógica antiga de status/"ativo" — não foi tocada, mesmo trade-off já registrado na decisão anterior.

## O que mudaria a decisão

- Se o guia de tom de voz for localizado, revisar os textos já publicados e, se fizer sentido, escrever
  um "estilo de referência" reutilizável (poucas regras, não um resumo do guia inteiro) para acelerar a
  próxima geração.
- Se "Atrasados" fizer falta na prática, decidir se ele volta como recorte adicional ao lado dos 5
  status, ou embutido no texto executivo (ex.: mencionar prazo vencido só quando relevante).

## Impacto

- **Produto**: nenhum módulo de produto afetado — ferramenta interna de operação do PM.
- **Técnico**: `tools/radar-produto/public/index.html` e `README.md` alterados. Script headless de
  publicação (fora do repositório, em scratchpad de sessão) atualizado para espelhar a mesma lógica.
  Testado ao vivo — 3 páginas republicadas no Doc real com os 5 status e os textos executivos.
- **Processo**: nenhum.

## Links

- Código: `tools/radar-produto/public/index.html` (`classifyStatus5`, `computeDailySquadData`,
  `buildSquadDailyMarkdown`, `buildResumoExecutivoMarkdown`), `tools/radar-produto/README.md`
- Doc de destino: [ClickUp — Report Status](https://app.clickup.com/9006076935/docs/8ccvn07-68891)
- Decisão relacionada (correção do "Ativos" enganoso, mesmo dia): [[2026-08-10-report-diario-pam-corrige-ativos-e-adota-rag]]
- Decisão relacionada (criação original do report diário): [[2026-08-10-report-diario-pam-extensao-radar-produto]]
