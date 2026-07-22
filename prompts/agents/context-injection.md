# Prompt: Context Injection

Padrão para agentes injetarem contexto do Knowledge Graph antes de responder.

---

## Padrão de Injeção

Antes de executar qualquer missão, o agente deve:

1. **Identificar os domínios relevantes** para a missão
2. **Ler os arquivos de domínio** correspondentes em `knowledge/domains/`
3. **Verificar relações** relevantes em `knowledge/relations.md`
4. **Consultar decisões recentes** em `knowledge/decisions/INDEX.md`

## Por Tipo de Missão

| Missão | Domínios a ler |
|---|---|
| Spec de feature | `produto.md`, `processo.md` |
| Priorização | `negocio.md`, `pessoas.md` |
| Discovery de usuário | `produto.md`, `pessoas.md` |
| Integração técnica | `engenharia.md`, `operacao.md` |
| Compliance | `operacao.md` |
| Métricas | `negocio.md`, `produto.md` |
| Mudança arquitetural | `registry/` (todos os YAMLs) |

## Instrução de Contexto

"Antes de responder, leia os arquivos relevantes do `knowledge/` para garantir que sua resposta está alinhada com o estado atual do domínio."
