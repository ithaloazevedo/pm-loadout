# Fusão de Backoffice & Integrações e Plataforma em um Time PAM único, ponta a ponta

**Data**: 2026-09-18
**Tomada por**: Ithalo Mendes
**Status**: APROVADA

---

## Contexto

Os dois times sob responsabilidade de Ithalo como PM — Backoffice & Integrações e Plataforma (Experiência do
Jogador) — se fundem em um único **Time PAM**. Junto à fusão, duas saídas da empresa: Linecker Gomes (Product
Designer da Plataforma), substituído por Mateus Sperandio; e Tony (QA, antes compartilhado entre os dois
times), substituído por David.

## Decisão

- Backoffice & Integrações + Plataforma (Experiência do Jogador) → **Time PAM**, com responsabilidade ponta a
  ponta: PAM, backoffice, experiência do jogador e as integrações dele com provedor, KYC, AML, agregadores etc.
- Liderança única do Time PAM: **Rayan** assume Team Lead (antes Tech Lead da Plataforma); **Ícaro** segue
  como Tech Lead (antes Tech Lead do Backoffice & Integrações).
- Pessoas: Hugo, Alex e Allison (designer), do Backoffice & Integrações, migram para o Time PAM, junto com
  Railton, Melk e Ícaro, da Plataforma.
- Linecker Gomes saiu da empresa; **Mateus Sperandio** assume como Product Designer na frente de experiência
  do jogador do Time PAM.
- Tony (QA, antes compartilhado entre os dois times) saiu da empresa; **David** assume como QA único do Time
  PAM.
- Ritos unificados: a partir da semana de 2026-09-18, um único conjunto de ritos (Planejamento, Daily,
  Revisão, Retrospectiva) para todo o Time PAM, substituindo a cadência intercalada que existia entre os
  squads PAM e Backoffice.

## Trade-offs Aceitos

- Papel de Gabriel Moreschi (Team Lead anterior da Plataforma) no time fundido **não foi confirmado** nesta
  rodada — Knowledge Graph registra como pendência (listado como desenvolvedor por suposição), não como fato.
- A fusão organizacional (pessoas, ritos) não implica, por si só, a fusão da estrutura técnica no ClickUp — os
  dois folders de Delivery e os dois Sprint Folders (PAM e Backoffice) seguem fisicamente separados até
  decisão explícita em contrário.

## O que mudaria a decisão

Se a fusão dos ritos exigir também fundir os backlogs/sprints técnicos no ClickUp num único squad — decisão
ainda não tomada, a discutir na Planning conjunta ou depois dela.

## Impacto

- **Processo**: a cadência intercalada de sprints (uma semana de diferença entre PAM e Backoffice) perde a
  razão de ser que a motivou — pessoas não estão mais divididas em dois times evitando sobrepor ritos. Ver
  `knowledge/domains/processo.md`.
- **Produto**: nenhuma mudança de escopo de produto — reorganização de quem executa o quê.
- **Técnico**: nenhuma mudança na estrutura ClickUp (folders/squads/sprints) até decisão explícita. O roster
  hardcoded de designers usado pelo report diário do PAM (`tools/radar-produto/public/index.html`, variável
  `DESIGNERS`) foi atualizado para refletir a troca Linecker Gomes → Mateus Sperandio.

## Links

- Knowledge Graph: `knowledge/domains/pessoas.md`, `knowledge/domains/processo.md`
- Decisão anterior relacionada: [[2026-07-30-estrutura-times-e-papeis]]
- Roster de designers no radar-produto: `tools/radar-produto/public/index.html`
