# Radar de Produto: migração de Artifact+MCP para aplicação local com API Token

**Data**: 2026-08-03
**Tomada por**: Ithalo Mendes (PM)
**Status**: APROVADA

---

## Contexto

Substitui parcialmente a decisão registrada em [[2026-08-03-radar-de-produto-dashboard-externo-com-escrita]]. Durante o desenvolvimento do Bloco C (edição inline), a API do ClickUp aplicou um rate limit (~23h de espera) nas chamadas MCP feitas durante testes intensivos. Ithalo pediu para trocar o transporte por uma chamada direta à API do ClickUp com um token pessoal (`CLICKUP_API_TOKEN`), para evitar depender da cota do conector MCP.

## Opções Consideradas

1. **Chamar a API do ClickUp direto do HTML do Artifact, com o token embutido**
   - Contras (eliminatório): Artifacts publicados rodam sob um CSP que bloqueia `fetch`/`XHR`/WebSocket para qualquer host externo — a chamada nunca sai do sandbox. Além disso, um token de escrita embutido no código-fonte de uma página HTML fica visível a qualquer um que abra o DevTools.

2. **Manter MCP, otimizar o consumo de chamadas** (reduzir polling, cache mais agressivo)
   - Prós: sem mudança de arquitetura.
   - Contras: não elimina o rate limit, só reduz a chance de bater nele; o rate-limit observado veio de uso intensivo de debug, não necessariamente do uso real — mas ficaria sem solução definitiva.

3. **Migrar para uma aplicação local com backend próprio guardando o token**
   - Prós: usa a API REST v2 do ClickUp diretamente (rate limit nativo da API, mais generoso que qualquer cota agregada de conector); o token nunca chega ao navegador (fica só no processo do servidor local); sem CORS (mesma origem); não depende do runtime do claude.ai.
   - Contras: sai do Artifact — Ithalo precisa rodar `node server.js` localmente sempre que quiser usar; a estrutura de squads/listas do ClickUp está hardcoded no servidor e exige atualização manual se o workspace mudar.

## Decisão

Optou-se pela opção 3. Como "só Ithalo vai usar" e não há necessidade de hospedagem, o app roda localmente: um servidor Node sem dependências (`tools/radar-produto/server.js`) expõe endpoints REST locais que chamam `https://api.clickup.com/api/v2` com o token do `.env`, e serve a página (`tools/radar-produto/public/index.html`) — a mesma UI construída no protótipo em Artifact, com a camada MCP substituída por `fetch('/api/...')`.

Testado com dados reais do workspace (leitura): listagem de tarefas por squad, detalhe de tarefa com status válidos por lista, e membros do workspace — todos funcionando de ponta a ponta. A escrita (`PUT /api/task/:id`) não foi testada ao vivo nesta sessão.

## Trade-offs Aceitos

- Perde a vantagem original do Artifact (zero instalação, roda no navegador de qualquer sessão claude.ai) — agora exige `node server.js` rodando localmente.
- Os IDs de Folder/Lista dos squads estão hardcoded no servidor (mesma limitação que já existia no protótipo em Artifact) — mudanças na estrutura do workspace exigem atualização manual do código.
- O campo "Tipo" da tarefa (Épico/Tarefa/Bug/Correção) não é resolvido pelo nome para tipos customizados — a API do ClickUp exigiria uma chamada adicional (`custom_item`) não implementada; mostra um ID numérico como fallback.

## O que mudaria a decisão

Se o uso deixar de ser só do Ithalo (outros PMs/Team Leads precisarem acessar sem rodar nada localmente), valeria reconsiderar hospedar esse mesmo backend em algum lugar acessível pela rede da empresa — a decisão de "não hospedar" foi tomada especificamente porque o uso é individual.

## Impacto

- **Produto**: nenhuma mudança de funcionalidade percebida — mesmos filtros, KPIs, edição e status report do protótipo anterior.
- **Técnico**: novo diretório `tools/radar-produto/` no repositório, com um servidor Node e um `.env` local (nunca versionado). Consome a API REST v2 do ClickUp diretamente, não mais o conector MCP.
- **Processo**: nenhuma mudança.

## Links

- Código: `tools/radar-produto/`
- Decisão anterior (arquitetura em Artifact): `knowledge/decisions/2026-08-03-radar-de-produto-dashboard-externo-com-escrita.md`
