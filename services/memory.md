# Serviço: Memory

## Responsabilidade

Manter histórico de sessões, decisões, preferências do usuário e contexto de projetos entre conversas.

## Implementação

Memory é fornecida pelo runtime. No Claude Code, ela pode ser persistida em arquivos do projeto; no Codex, o histórico da tarefa e as instruções do workspace oferecem o contexto de trabalho. Não dependa de um caminho privado de memória para concluir uma missão.

## Tipos de Memória

| Tipo | O que armazena | Quando salvar |
|---|---|---|
| `user` | Perfil, preferências, expertise | Quando algo novo sobre o usuário é aprendido |
| `feedback` | Regras de comportamento aprendidas com o usuário | Quando o usuário corrige ou valida uma abordagem |
| `project` | Fatos sobre o projeto — quem faz o quê, decisões, prazos | Quando algo muda no contexto do projeto |
| `reference` | Ponteiros para sistemas externos | Quando se aprende onde algo vive (ClickUp, Drive, Notion) |

## Controle de Validade (Staleness)

Memories do tipo `project` e `reference` envelhecem. Para reduzir o risco de agir sobre informação stale, o frontmatter de cada memory deve incluir:

```yaml
metadata:
  type: project
  last_verified: YYYY-MM-DD   # última vez que o fato foi confirmado como atual
  valid_until: YYYY-MM-DD     # opcional — para fatos com prazo conhecido (ex: deadline, freeze)
```

**Regra de uso**: antes de recomendar algo com base em uma memory de tipo `project` ou `reference`, verificar se o fato ainda é atual (ler o arquivo correspondente no projeto ou consultar o sistema externo). Se estiver desatualizado, atualizar a memory antes de usar.

**Quem faz a limpeza**: o `agente-evolucao` é responsável por propor remoção ou atualização de memórias desatualizadas quando identificadas durante observação do sistema.

## O que NÃO salvar

- Padrões de código ou arquitetura (derivável do código)
- Histórico git (use `git log`)
- Listas de tarefas em andamento (use o TodoWrite)
- Detalhes efêmeros da conversa atual

## Relação com Knowledge Graph

Memory armazena contexto *pessoal e processual* do usuário.
Knowledge Graph armazena *conhecimento de domínio* do produto.

Não duplicar: fatos sobre o produto vão no KG; preferências do PM vão na Memory.
