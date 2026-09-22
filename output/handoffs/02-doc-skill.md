# Handoff 02 — Documentação e skill (D1–D2)

**De**: sessão Orquestrador de 02/09/2026
**Para**: nova sessão — Orquestrador
**Skills**: `dashboard-tradicional`

## Antes de qualquer coisa

Leia **apenas** `knowledge/decisions/2026-09-01-funil-eventos-usa-account-created-e-data-de-ocorrencia.md`.
Ele já está atualizado e é a fonte. Não releia conversa. Não toque em código do app.

## Missão

**D1 — Skill `dashboard-tradicional`.** Atualizar a seção "Governança e como mexer no código"
em `.claude/skills/dashboard-tradicional/SKILL.md` **e** o espelho em
`.agents/skills/dashboard-tradicional/SKILL.md` (os dois têm que ficar iguais) com os
invariantes que a retificação estabeleceu:

- `COBERTURA_MIN_GATE = 1.0` é exato. Tolerância de cobertura foi a causa raiz de uma manchete
  impossível — se alguém quiser afrouxar, tem que refutar isso primeiro.
- O painel afirma dois níveis (`signup_started` → `account_created`). Todo intermediário é
  piso. Manchete de nível não confirmado sai com `≥`/`≤` e com o rótulo de limite.
- Bumpar as chaves de cache de **todas** as quatro rotas juntas, sempre. Lista das chaves
  atuais na fonte canônica.
- Qualquer selo de validação exibido no frontend precisa vir de query real no payload —
  nunca renderizar por truthiness de outro campo. Já houve um selo fabricado em produção
  local.
- Sinal de sanidade: perda por passo tem que caber na perda total do funil.

**D2 — Índice de decisões.** Confirmar que a decisão está em `knowledge/decisions/INDEX.md`
com a descrição refletindo a retificação, não só a correção original.

## Restrições

- `tools/` é untracked no git. Não é o alvo deste handoff, mas se precisar tocar, backup antes.
- Não reescreva a fonte canônica: ela está correta. Aponte para ela na skill em vez de copiar
  o conteúdo.

## Primeira ação

Ler a seção "Governança e como mexer no código" da skill e comparar com a seção "Retificação"
da fonte canônica — a skill ainda não conhece nada da retificação.

## Critério de conclusão

Alguém que abra a skill sem contexto nenhum consegue mexer no funil sem repetir os cinco erros
listados na retificação. Espelho `.agents/` idêntico ao `.claude/`.
