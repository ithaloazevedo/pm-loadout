# Assignee de tarefas no ClickUp nunca é atribuído sem confirmação do usuário

**Data**: 2026-07-27
**Tomada por**: Ithalo Mendes
**Status**: APROVADA

---

## Contexto

Ao criar a tarefa de atualização do rodapé (Bravo/Tradicional) no folder Delivery: Experiência do jogador, o `agente-delivery` atribuiu automaticamente o assignee Railton Araujo, inferindo por histórico de tarefas semelhantes ("Corrigir link da Ouvidoria no rodapé", etc.), sem perguntar antes. O responsável estava correto neste caso, mas o usuário identificou o padrão como indesejado: a atribuição silenciosa não deveria ser o comportamento padrão do agente.

## Opções Consideradas

1. **Criar tarefas sempre sem assignee por padrão** — dono definido depois, em triagem manual, mesmo contrariando o anti-pattern "Sem dono" hoje documentado em `anti-pattern.md`.
   - Prós: elimina qualquer risco de atribuição errada.
   - Contras: contradiz a meta de "todo item tem dono" e gera mais um passo manual sempre.

2. **Sempre perguntar antes de atribuir** — o agente pode sugerir um responsável (por histórico) e explicar o porquê, mas só aplica o assignee mediante confirmação explícita do usuário ou pedido nomeado.
   - Prós: preserva a meta de todo item ter dono, remove a decisão silenciosa do agente.
   - Contras: exige uma interação a mais quando o dono não é óbvio (mitigado: a ausência de confirmação não bloqueia a criação da tarefa).

## Decisão

Opção 2. O `agente-delivery` (e a skill `clickup-spec` de forma geral) nunca decide e aplica um assignee por conta própria — pode sugerir com base em histórico, mas só grava o campo quando o usuário confirma ou nomeia explicitamente alguém. Sem confirmação, o item nasce sem assignee e o "dono pendente" é sinalizado no handoff, em vez de travar a criação da tarefa.

## Trade-offs Aceitos

Itens podem nascer sem dono nomeado até refinamento — abre mão da garantia forte de "todo item sempre tem assignee no momento da criação" em troca de nunca atribuir errado por conta própria.

## O que mudaria a decisão

Se o time perceber que "dono pendente" está causando itens esquecidos sem triagem, pode valer a pena reintroduzir sugestão automática — mas sempre como sugestão explícita a confirmar, nunca aplicada em silêncio.

## Impacto

- **Produto**: nenhum.
- **Técnico**: nenhum.
- **Processo**: `agente-delivery.md` (regras + completude de campos) e `clickup-spec/SKILL.md` (filosofia "Dono definido" + referência de tools) atualizados para refletir a nova regra.

## Links

- Card no ClickUp: https://app.clickup.com/t/868kgg2gj (tarefa principal — Atualizar texto do rodapé — Bravo e Tradicional)
- `.claude/agents/agente-delivery.md`
- `.claude/skills/clickup-spec/SKILL.md`
