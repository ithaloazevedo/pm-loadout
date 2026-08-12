# Routing Map

Use este mapa quando o Orquestrador precisa escolher skills.

## Roteamento Rápido

| Intenção do usuário | Primeira skill | Considerar depois |
|---|---|---|
| "Tenho uma ideia" | `brainstorming` | `vieses`, `suposicoes` |
| "Quem é o usuário?" | `entrevista-usuario` | `jtbd`, `mapa-necessidades` |
| "Tenho pesquisa/entrevistas" | `ost` | `jtbd` |
| "Quais oportunidades?" | `ost` | `suposicoes`, `ice` |
| "Qual prioridade?" | `ice` | `gist`, `advogado-do-diabo` |
| "Isso é complexo?" | `cynefin` | `wardley` |
| "Como vira estratégia?" | `gist` | `wardley`, `ice` |
| "Como escrever no ClickUp?" | `clickup-spec` | `checar-servico`, `checar-usabilidade` |
| "Isso está bom para o usuário?" | `checar-usabilidade` | `checar-servico` |
| "Pode lançar?" | `nivel-lancamento` | `metricas`, `checar-servico` |
| "Como medir?" | `metricas` | `retrospectiva` |
| "O que aprendemos?" | `retrospectiva` | `metricas` |

## Heurísticas de Roteamento

- Se o ClickUp é mencionado junto a uma ideia vaga, faça um check de prontidão para spec mas mantenha a missão primária como "Clarificar ideia".
- Se o usuário ainda está descrevendo a ideia, evite `clickup-spec`.
- Se o usuário tem evidências mas sem síntese, use `ost` antes de priorizar.
- Se o usuário tem opções mas sem confiança, use `suposicoes` antes de `ice`.
- Se a decisão afeta múltiplos times ou um roadmap, adicione `advogado-do-diabo`.
- Se o pedido é sobre prontidão para produção, prefira `checar-servico`, `checar-usabilidade`, `nivel-lancamento` e `metricas`.

## Condições de Parada

Pare quando uma das situações for verdadeira:

- a decisão está clara o suficiente;
- o próximo artefato está pronto para revisão;
- há uma pergunta bloqueante;
- evidência é fraca demais para a conclusão solicitada;
- o trabalho deve ir diretamente a um agente especialista.
