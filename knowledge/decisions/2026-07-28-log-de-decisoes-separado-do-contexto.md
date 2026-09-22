# Mudanças de escopo pós-criação vão para "Log de Decisões", não reescrevem o Contexto

**Data**: 2026-07-28
**Tomada por**: Ithalo Mendes
**Status**: APROVADA

---

## Contexto

Ao consolidar 8 Épicos de padronização de páginas legais (Bravo/Tradicional) em 1 épico guarda-chuva com 17 subtasks, o `agente-delivery` registrou o histórico da consolidação (por quê, trade-offs) misturado à seção de Contexto do épico, seguindo a regra então vigente do `template-delivery.md` ("Decisões fechadas vivem no Contexto — com data"). O usuário apontou que isso polui a leitura do card para quem só precisa entender o que construir hoje — decisões estruturais/histórico de replanejamento não deveriam viver junto com a explicação do problema/objetivo atual.

## Decisão

O `template-delivery.md` agora separa duas coisas que antes viviam juntas no Contexto:
- **Contexto**: só a decisão original de escopo — o "porquê" deste item existir do jeito que existe hoje. Estável, limpo, dev-facing.
- **📜 Log de Decisões** (nova seção, opcional, só existe se houve mudança pós-criação): uma linha objetiva por decisão — "DD/MM — o que mudou — link se houver." Sem prosa, sem justificativa — isso já está no Contexto ou foi decidido em outro lugar (comentário de decisão, por exemplo).

## Trade-offs Aceitos

Itens que nunca mudaram de escopo não têm essa seção — ela só aparece quando necessária, evitando ruído em todo card por padrão.

## O que mudaria a decisão

Se, na prática, times acharem o Log de Decisões redundante com os comentários de decisão já postados nas tasks (mesmo protocolo, dois lugares), vale reavaliar se um substitui o outro.

## Impacto

- **Processo**: `clickup-spec/references/template-delivery.md` atualizado — nova seção 📜 Log de Decisões e regra de uso revisada.
- **Produto/Técnico**: nenhum.

## Links

- `.claude/skills/clickup-spec/references/template-delivery.md`
- Épico afetado: https://app.clickup.com/t/868kh28pd
