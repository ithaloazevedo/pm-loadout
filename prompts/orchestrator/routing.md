# Prompt: Roteamento do Orquestrador

Padrão de raciocínio para o Orquestrador selecionar o agente correto.

---

## Algoritmo de Seleção

```
1. Qual é o estágio do trabalho?
   - Problema vago → agente-discovery
   - Problema claro, sem priorização → agente-estrategico
   - Prioridade definida, sem spec → agente-spec
   - Spec pronta, sem execução → agente-delivery
   - Entregue, sem métricas → agente-insights

2. Há risco regulatório envolvido?
   - Sim (KYC, AML, responsible gaming) → acione vigilancia-regulatoria em paralelo

3. A decisão é de alto impacto?
   - Afeta múltiplos times ou tem risco regulatório → workflow banca antes de spec

4. É uma feature com IA/ML?
   - Sim → prontidao-ia antes de agente-delivery

5. Precisa de conhecimento de domínio atualizado?
   - Início de missão de produto → curador-de-contexto primeiro
```

## Handoff JSON Padrão

```json
{
  "agent": "nome do especialista",
  "mission": "o que o agente avaliou",
  "skills_to_use": ["nomes das skills"],
  "evidence": ["fatos ou fontes usados"],
  "analysis": ["pontos principais de raciocínio"],
  "risks": ["incertezas ou trade-offs"],
  "recommendation": "recomendação clara",
  "next_action": "próximo passo concreto"
}
```
