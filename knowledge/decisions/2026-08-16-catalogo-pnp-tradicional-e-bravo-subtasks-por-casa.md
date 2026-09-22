# Épico de expansão do catálogo via PNP passa a cobrir Tradicional e Bravo; ondas de ativação desdobram em subtasks por casa

**Data**: 2026-08-16
**Tomada por**: agente-delivery (execução), a pedido de Ithalo via Orquestrador
**Status**: APROVADA

---

## Contexto

O épico [Expandir o catálogo de jogos da Tradicional e da Bravo com novos provedores via integração PNP](https://app.clickup.com/t/868kapw4g) (squad Operação e afiliados) nasceu com título e descrição falando só da Tradicional, com 6 subtasks: 2 bloqueadores técnicos (módulo de bônus da PNP, integração com a Smartico) e 4 ondas de ativação de provedor. O PM confirmou que o escopo real é para as duas casas (Tradicional e Bravo rodam no mesmo PAM), o que exigia decidir como representar isso na estrutura de subtasks — desdobrar cada onda em duas (uma por casa) ou manter 4 subtasks com um checklist "ativar em Tradicional" / "ativar em Bravo" dentro de cada uma.

## Opções Consideradas

1. **4 subtasks de onda com checklist por casa dentro de cada uma.**
   - Prós: menos itens no board.
   - Contras: esconde o status por casa dentro de um checklist — não dá pra ver, sem abrir a subtask, se uma onda está pronta na Tradicional mas travada na Bravo.

2. **Desdobrar cada onda em duas subtasks (uma por casa) — 8 subtasks de ativação no total.**
   - Prós: alinhado ao precedente real do workspace — a habilitação de catálogo da Banana Games já usou duas Tarefas irmãs, uma por casa (ver [decisão anterior](2026-08-11-habilitacao-jogos-provedor-fica-com-operacao-afiliados.md)), porque ativar um provedor no catálogo é uma configuração por casa (região/SLOT), não uma ação única. Dá status independente por casa direto no board.
   - Contras: dobra o número de subtasks de ativação (4 → 8).

3. **Desdobrar também os 2 bloqueadores técnicos por casa** vs. **mantê-los únicos**.
   - Únicos: confirmado que faz sentido — a integração com a Smartico (motor de CRM de missões/bônus da Banca de Benefícios) é hoje **exclusiva da Tradicional**; a Bravo não tem esse módulo (`knowledge/domains/produto.md`, seção Módulo). Não há "versão Bravo" desse bloqueador para desdobrar. O módulo de bônus da própria PNP é trabalho técnico de integração, não uma configuração por casa.

## Decisão

Escopo do épico generalizado para as duas casas. As 4 subtasks de ativação por onda foram desdobradas em 8 (uma por casa, por onda) — total de 10 subtasks no épico (2 bloqueadores + 8 de ativação). Os 2 bloqueadores técnicos permaneceram únicos, sem desdobrar por casa. A nota "Não confundir com" na seção Links do épico foi reescrita (não removida) para precisar a distinção com o épico [868k9cqm3](https://app.clickup.com/t/868k9cqm3): aquele é a Vertical distribuindo a Loteria via PNP para outros operadores (fornecedora); este é o PAM consumindo catálogo de provedores terceiros via PNP como agregador (cliente) — direções opostas do mesmo tipo de protocolo.

## Trade-offs Aceitos

- Board do épico passa de 6 para 10 subtasks — mais itens para a squad acompanhar, mas com rastreabilidade por casa nas 4 ondas.
- Assignees das 10 subtasks continuam em aberto (confirmado pelo PM) — squad decide depois.

## O que mudaria a decisão

Se surgir evidência de que a ativação de provedor num futuro passe a ser feita por um mecanismo único cross-casa (ex.: configuração central de catálogo compartilhada entre Tradicional e Bravo), o desdobramento por casa deixaria de fazer sentido e as 8 subtasks de ativação poderiam voltar a ser 4.

## Impacto

- **Produto**: Módulo Jogos (catálogo/lobby) da Tradicional e da Bravo; Banca de Benefícios/Smartico (exclusiva da Tradicional).
- **Técnico**: integração PNP (agregador de provedores); integração Smartico para bônus via PNP.
- **Processo**: reforça o precedente de que ativação/habilitação de catálogo de provedor é rastreada por casa (Tarefas/subtasks separadas), enquanto bloqueadores técnicos de integração que não variam por casa permanecem únicos.

## Links

- Épico: https://app.clickup.com/t/868kapw4g
- Precedente (Banana Games): [2026-08-11-habilitacao-jogos-provedor-fica-com-operacao-afiliados.md](2026-08-11-habilitacao-jogos-provedor-fica-com-operacao-afiliados.md)
- Épico não relacionado (distinção precisada, não confundir): https://app.clickup.com/t/868k9cqm3
