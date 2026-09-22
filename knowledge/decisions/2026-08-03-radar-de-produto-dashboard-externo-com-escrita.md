# Radar de Produto: dashboard externo (Artifact + MCP) com escrita restrita aos times do Ithalo

**Data**: 2026-08-03
**Tomada por**: Ithalo Mendes (PM)
**Status**: APROVADA

---

## Contexto

Ithalo pediu visibilidade consolidada do que está acontecendo em Discovery/Delivery, cruzando pessoa, time e etapa — motivado por ser PM em 2 dos 3 times da Vertical Tech (Plataforma e Backoffice & Integrações) sem uma visão agregada nativa. Depois de um brainstorming, a decisão de formato final foi um dashboard HTML externo ao ClickUp, e não uma View/Dashboard nativo.

## Opções Consideradas

1. **View/Dashboard nativo do ClickUp**
   - Prós: zero manutenção, atualização em tempo real, todo mundo do time já usa.
   - Contras: preso à UI do ClickUp; agrupamento customizado (ex.: visão por pessoa cruzando múltiplos Folders) é limitado.

2. **MCP conversacional (perguntar ao Claude sob demanda, sem artefato)**
   - Prós: não exige código.
   - Contras: não é um painel persistente — exige reabrir conversa a cada consulta.

3. **Artifact HTML externo usando a capability `mcp` do runtime do claude.ai**
   - Prós: layout 100% customizado; chama os conectores MCP (inclusive ClickUp) direto do navegador do usuário, com as credenciais dele — sem API Key exposta, sem backend.
   - Contras: só funciona dentro do runtime do claude.ai (exigiu um modo de dados fictícios para iteração local fora dele); manutenção de código fica com quem mantém o artifact.

## Decisão

Optou-se pela opção 3. Foi construído `radar-produto.html`, publicado como Artifact, usando `window.claude.mcp` para ler tarefas do ClickUp em tempo real (filtros por squad/pessoa/etapa/prioridade, KPIs). O escopo foi então estendido para edição inline de status, prioridade, prazo e responsáveis — restrita às tarefas dos squads que Ithalo lidera como PM (Plataforma, Backoffice & Integrações, e a esteira Discovery, que atravessa times). Tarefas do squad Produto aparecem em modo somente leitura.

## Trade-offs Aceitos

- O relatório de atividade diária por pessoa (cruzando comentários/timestamps) foi deliberadamente **não** incorporado como seção do dashboard: a API do ClickUp não expõe feed de atividade bruto, e a síntese qualitativa exige raciocínio de um LLM, que um Artifact HTML não pode invocar por conta própria (só chama tools de conector). Fica como relatório gerado sob demanda fora do dashboard — e ainda pendente de uma passada de governança antes de ser especificado, dado o risco de virar ferramenta de vigilância de desempenho individual.
- A capacidade de escrita não foi testada ao vivo (rate limit da API do ClickUp durante o desenvolvimento). O formato de "status válidos por lista" e da resposta de `clickup_update_task` foi implementado com base no schema formal da ferramenta, não em uma resposta observada — há fallback degradado (campo de texto livre) se o formato vier diferente do esperado.
- Discovery não tem segmentação por squad no ClickUp — tratado como esteira única, sem quebra por time.

## O que mudaria a decisão

Se `window.claude.mcp` deixar de estar disponível, ou se o uso precisar acontecer fora do ambiente claude.ai (ex.: um painel sempre aberto num monitor de sala), vale reconsiderar a opção 1 (nativo) ou uma variante com API Key + backend próprio.

## Impacto

- **Produto**: cria um canal de escrita no ClickUp fora da UI nativa — cards de Plataforma/Backoffice/Discovery podem ter status/prioridade/prazo/responsável alterados a partir do dashboard.
- **Técnico**: depende da capability `mcp` do runtime de Artifacts do claude.ai e do conector ClickUp já autorizado na conta do Ithalo.
- **Processo**: nenhuma mudança na hierarquia/esteiras do ClickUp. A correção da tabela de squads desatualizada em `knowledge/domains/processo.md` foi feita como parte desta missão.

## Links

- Artifact publicado: https://claude.ai/code/artifact/926dba86-2734-4c23-9ee7-14a66f12708d
- Correção relacionada: `knowledge/domains/processo.md`
