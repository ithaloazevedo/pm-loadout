# Serviço: Decision Log

## Responsabilidade

Registrar decisões importantes com justificativa, trade-offs e contexto. Torna o raciocínio rastreável e reduz retrabalho.

## Implementação

Arquivos markdown em `knowledge/decisions/`, indexados em `knowledge/decisions/INDEX.md`.

## Responsabilidade por Tipo de Decisão

| Tipo de decisão | Agente responsável por registrar |
|---|---|
| Priorização estratégica, aposta, sequenciamento | `agente-estrategico` — após confirmação do usuário |
| Mudança arquitetural na plataforma de agentes | `agente-governanca` — após veredicto APROVADA |
| Decisão de produto com trade-off de escopo relevante | `agente-spec` — ao finalizar spec que exigiu escolha de escopo |

**Nenhum agente registra sem confirmação do usuário.** O log captura decisões aceitas, não recomendações.

## Quando Registrar

Registre uma decisão quando:
- A escolha afeta múltiplos times ou sistemas
- Há trade-offs explícitos sendo feitos
- A decisão vai ser questionada no futuro
- Um caminho foi descartado e o porquê importa
- Uma mudança arquitetural na plataforma de agentes é aprovada

**Não registre** decisões triviais ou reversíveis. Não registre decisões bloqueadas.

## Protocolo

1. Copie `knowledge/decisions/TEMPLATE.md`
2. Nomeie: `YYYY-MM-DD-titulo-curto.md`
3. Preencha todos os campos
4. Adicione uma linha em `knowledge/decisions/INDEX.md`
5. Se houver card no ClickUp, adicione o link VL-XXXXX
6. Se a decisão introduzir nova entidade ou alterar relação no KG, atualizar `knowledge/relations.yaml`

## Relação com Memory e Knowledge Graph

- **Memory**: lembra que a decisão foi tomada e quem tomou (contexto pessoal)
- **Decision Log**: armazena o raciocínio completo (contexto de domínio)
- **Knowledge Graph**: atualizado quando a decisão introduz nova entidade ou muda relação existente
