# Agent Flow

## Juninho

Juninho e o orquestrador. Ele escolhe o menor conjunto de skills necessario para a missao.

```mermaid
flowchart TD
  A["Pedido do PM"] --> B["Juninho classifica a missao"]
  B --> C{"Precisa de especialista?"}
  C -->|Discovery| D["Scout"]
  C -->|Estrategia| E["Strategist"]
  C -->|Spec| F["Scribe"]
  C -->|Qualidade| G["Judge"]
  C -->|Metricas| H["Analyst"]
  C -->|Nao| I["Skill direta"]
  D --> J["Handoff"]
  E --> J
  F --> J
  G --> J
  H --> J
  I --> J
  J --> K["Resposta consolidada"]
```

## Regra de ouro

Juninho nao deve transformar toda conversa em um processo pesado. A pergunta e sempre:

> Qual e o menor loadout que melhora a decisao agora?

## Handoff padrao

```json
{
  "agent": "specialist name",
  "mission": "what the agent evaluated",
  "skills_to_use": ["skill names"],
  "evidence": ["facts or sources used"],
  "analysis": ["main reasoning points"],
  "risks": ["uncertainties or trade-offs"],
  "recommendation": "clear recommendation",
  "next_action": "next concrete step"
}
```
