# Serviço: Observabilidade

**Status**: Spec definida — implementação completa em V2.

## Responsabilidade

Registrar interações da plataforma para entender padrões de uso, identificar gargalos e alimentar o Agente de Evolução.

## O que Registrar

Por interação:
- Agente ou skill utilizado
- Missão classificada pelo Orquestrador
- Duração estimada
- Resultado (artefato produzido / decisão tomada / sem conclusão)
- Falha ou retrabalho ocorrido
- Intervenção humana necessária

## Métricas Importantes

| Métrica | O que indica |
|---|---|
| Agente mais utilizado | Onde está o valor central da plataforma |
| Sequências recorrentes | Candidatos a loadout nomeado ou novo agente |
| Missões sem artefato | Falhas de orquestração |
| Skills nunca usadas | Candidatos a remoção |
| Perguntas bloqueantes recorrentes | Lacunas de contexto no KG |

## Relação com Agente de Evolução

O Agente de Evolução consome dados de observabilidade para:
1. Identificar padrões de uso
2. Detectar sobreposição entre agentes
3. Propor criação, fusão ou remoção de agentes
4. Submeter proposta ao Agente de Governança para aprovação
