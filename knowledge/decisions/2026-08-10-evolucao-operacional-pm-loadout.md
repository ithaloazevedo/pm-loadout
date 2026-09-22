# PM Loadout adota contratos de skill e disciplinas operacionais incrementais

**Data**: 2026-08-10
**Tomada por**: Ithalo Mendes
**Status**: APROVADA

---

## Contexto

O PM Loadout já possuía competências de produto, Knowledge Graph, Decision Log e operação no ClickUp, mas faltavam convenções explícitas para configuração por workspace, continuidade entre sessões, pesquisa auditável e aprendizado sobre o uso da própria plataforma.

## Opções Consideradas

1. **Adicionar novos agentes para cada lacuna**
   - Prós: responsabilidades muito explícitas.
   - Contras: aumenta roteamento e manutenção sem evidência de uso recorrente.

2. **Adicionar disciplinas e contratos ao sistema atual**
   - Prós: melhora previsibilidade sem duplicar agentes ou mudar a fronteira PM → Engenharia.
   - Contras: exige migração gradual das skills legadas e rotina de observabilidade.

## Decisão

Adotar a opção 2: contrato para skills novas ou alteradas, setup local com escrita confirmada, modelagem ativa de domínio, handoff compacto, pesquisa verificável, validação de ClickUp em dois eixos e observabilidade mensal mínima.

## Trade-offs Aceitos

- As skills legadas migram quando forem alteradas, em vez de uma conversão ampla agora.
- A observabilidade começa manual e agregada; não haverá telemetria individual nem captura automática de conversas.
- O modo offline do ClickUp prioriza proposta na conversa sobre automação.

## O que mudaria a decisão

Se a migração incremental gerar inconsistência recorrente, ou se os registros mensais não fornecerem sinal suficiente, revisar a convenção e avaliar automação mínima após evidência de uso.

## Impacto

- **Produto**: melhora a rastreabilidade de decisões e a qualidade de itens antes de Delivery.
- **Técnico**: nenhuma nova integração obrigatória; conectores respeitam configuração local e confirmação.
- **Processo**: novas skills e alterações passam a declarar contrato; o Agente de Evolução consolida observabilidade mensal.

## Links

- [Contrato de skill](../../services/skill-contract.md)
- [Observabilidade](../../services/observability.md)
- [Orquestrador](../../.agents/skills/orquestrador/SKILL.md)
