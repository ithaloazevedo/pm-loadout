# Contrato de Skill

O contrato se aplica a toda skill criada ou alterada a partir de 2026-08-10. Skills legadas permanecem válidas até serem tocadas; devem ser migradas no respectivo PR. O maintainer da plataforma revisa a cobertura ao fim de cada ciclo trimestral. O objetivo é tornar o comportamento verificável sem transformar a skill em um documento longo.

## Campos mínimos

| Campo | Decisão que fixa |
|---|---|
| `name` e `description` | Como a skill é encontrada e em que situação deve disparar. |
| `invocation` | `user` para fluxos que exigem intenção humana; `model` para disciplinas que o agente pode equipar automaticamente. |
| `inputs` | Informação, referências ou conectores necessários. |
| `outputs` | Artefato e forma de entrega esperados. |
| `side_effects` | `none`, `propose` ou `write-confirmed`; nunca esconda escrita externa. |
| `context` | Fontes canônicas a consultar e condição para consultá-las. |
| `completion` | Condição objetiva que diferencia trabalho concluído de rascunho. |

## Regras de desenho

- Um roteador de usuário pode equipar disciplinas `model`; uma disciplina nunca chama outro roteador.
- Descrições devem listar gatilhos distintos, não sinônimos em sequência.
- Mantenha passos universais no `SKILL.md`; mova referências condicionais para `references/` com um gatilho explícito.
- Declare o efeito externo antes de executá-lo. `propose` exige confirmação antes de criar, alterar ou publicar.
- Critérios de conclusão devem ser observáveis e exaustivos para o escopo da skill.

## Modelo mínimo

```yaml
---
name: exemplo
description: Use quando [gatilho distinto] para [resultado].
invocation: user | model
inputs: [contexto necessário]
outputs: [artefato produzido]
side_effects: none | propose | write-confirmed
context: [fontes canônicas]
completion: [condição verificável]
---
```

Compatibilidade: runtimes que ignoram campos adicionais de frontmatter devem respeitar as mesmas declarações na seção `## Contrato`.
