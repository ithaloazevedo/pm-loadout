# Report diário do PAM (visão por Frente + publicação no ClickUp Doc) construído como extensão do radar-produto, não como ferramenta nova

**Data**: 2026-08-10
**Tomada por**: Ithalo Mendes (PM)
**Status**: APROVADA

---

## Contexto

Ithalo pediu uma ferramenta local de "report e visualização diária" inspirada num artifact de report semanal (agrupado por Frente/Épico, com bucket "Sem frente"), com edição/reorganização manual e publicação de um relatório para a diretoria. O plano inicial cogitava PDF; depois mudou para publicar diretamente em páginas de um ClickUp Doc já criado por ele (`8ccvn07-68891`).

Antes de especificar a construção, foi feita uma checagem de duplicidade: `tools/radar-produto/` já existe — painel local de Discovery/Delivery do ClickUp, com edição inline (status/prioridade/prazo/responsável) restrita aos squads que Ithalo lidera (Plataforma, Backoffice & Integração, Discovery) e um mecanismo de status report (period-based, exportado via `window.print()`).

## Opções Consideradas

1. **Construir uma ferramenta nova e separada** para o report por Frente + publicação no Doc.
   - Contras: duplicaria autenticação, config de squad/lista e a base de edição já existentes e funcionando no `radar-produto` — dois apps locais fazendo tarefas sobrepostas contra o mesmo workspace.
2. **Estender o `radar-produto`** com: (a) um modo de visão "por Frente" com reatribuição de Épico, e (b) um botão de publicação diária no ClickUp Doc.
   - Prós: reaproveita toda a infraestrutura existente (servidor, auth, squads, drawer de edição); menor superfície de manutenção.
   - Contras: acopla mais responsabilidades num único app local.

## Decisão

Optou-se pela **Opção 2**. Implementado em `tools/radar-produto/`:

- **Visão "por Frente"** (`server.js`: `normalizeTask` agora expõe `parent`; `updateTask` aceita `patch.parent`. `public/index.html`: novo `groupBy: "frente"`, agrupamento por tarefa-pai com bucket "Sem frente", seletor inline de reatribuição de Épico restrito a candidatos da mesma lista — ClickUp não permite parent fora da lista da subtarefa).
- **Publicação diária no ClickUp Doc**, escopo **PAM apenas** (Plataforma + Backoffice & Integração — Produto explicitamente fora, por decisão do Ithalo). Botão gera/atualiza (idempotente por data) uma subpágina do dia em cada página de squad, mais uma subpágina agregada em "Resumo Executivo — PAM" (criada automaticamente na primeira vez), via API v3 de Docs do ClickUp.

Testado ao vivo (leitura e escrita) contra o Doc real — ver "Achados técnicos" abaixo.

## Achados técnicos (documentados em `tools/radar-produto/README.md` e `query-pam` onde aplicável)

- A API v3 de Docs do ClickUp retorna **500 quando `max_page_depth=-1`** é passado (o valor que a própria documentação recomenda para "sem limite") — confirmado tanto via chamada direta quanto via MCP. Omitir o parâmetro já retorna a árvore completa. O servidor local não passa mais esse parâmetro.
- Houve um **500 intermitente isolado** numa chamada de edição de página, não reproduzido de novo com o mesmo payload — o servidor agora tenta novamente uma vez após falha 5xx antes de desistir.
- **Opex×Capex (Bug vs. não-Bug) não foi implementado no report diário** — o tipo de tarefa customizado (`custom_item_id`) não é resolvido pela API de lista sem uma chamada adicional por tarefa; ficou de fora para não estimar/adivinhar.

## Trade-offs Aceitos

- Reatribuição de Épico (escrita real na hierarquia do board, visível ao time todo) não foi testada ao vivo pelo Claude Code — só leitura e simulação com dados reais. Primeiro teste real é do próprio Ithalo, no painel.
- Nomes de página do Doc estão hardcoded em `public/index.html` (`TOP_PAGE_NAMES`, `RESUMO_TOP_PAGE_NAME`) — renomear uma página no ClickUp exige atualizar o código também.
- Report diário não tem Opex×Capex nem quebra por Frente (esse nível de detalhe fica só na visão interativa do app, não no que é publicado no Doc) — decisão consciente de manter o report da diretoria curto.

## O que mudaria a decisão

- Se o uso deixar de ser só do Ithalo (outros PMs precisarem publicar reports de outros squads), a lista de squads/nomes de página hardcoded precisa virar configuração, não código.
- Se a ClickUp API v3 continuar instável em produção, considerar aumentar para mais de uma retentativa ou logar falhas persistentes para investigação.

## Impacto

- **Produto**: nenhum módulo de produto afetado — ferramenta interna de operação do PM.
- **Técnico**: `tools/radar-produto/server.js` e `public/index.html` alterados (não um novo diretório). Testes de leitura e escrita real feitos contra o workspace Vertical Tech e o Doc `8ccvn07-68891`; páginas de teste criadas durante a verificação foram marcadas "[pode apagar]" no próprio Doc (sem capacidade de deletar via API/MCP disponível).
- **Processo**: nenhum.

## Links

- Código: `tools/radar-produto/` (`server.js`, `public/index.html`, `README.md`)
- Doc de destino: [ClickUp — Report Status](https://app.clickup.com/9006076935/docs/8ccvn07-68891)
- Skill de schema relacionada (não usada aqui, mas mesma sessão): `.claude/skills/query-pam/SKILL.md`
