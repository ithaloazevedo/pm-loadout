# Prompt: Protocolo de Handoff

Padrão para transferir trabalho entre agentes com contexto completo.

---

## Quando Fazer Handoff

Faça handoff quando:
- O trabalho requer competência de outro agente
- A missão mudou de estágio (discovery → estratégia → spec → delivery)
- Um risco especializado foi identificado (regulatório, técnico, qualidade)

## Formato do Handoff

```json
{
  "de": "agente-origem",
  "para": "agente-destino",
  "mission": "o que o agente de destino deve fazer",
  "context": {
    "problema": "o problema original",
    "evidencias": ["lista de evidências coletadas"],
    "decisoes": ["decisões já tomadas"],
    "constraints": ["limitações conhecidas"]
  },
  "skills_recomendadas": ["skills para a missão"],
  "riscos": ["riscos a considerar"],
  "next_action": "primeira ação do agente de destino"
}
```

## Regras

- Nunca fazer handoff sem contexto suficiente para o agente de destino continuar
- Sempre incluir as evidências coletadas — não resuma, cite
- Se o handoff é para agente-delivery, a spec deve estar completa e validada
- Se o handoff é para agente-governanca, incluir a proposta e os trade-offs explicitados
