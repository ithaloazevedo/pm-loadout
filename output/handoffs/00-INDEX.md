# Handoffs — Funil de Cadastro / dashboard Geral-Turnover

Distribuição da sessão de 02/09/2026 em sessões independentes. Cada handoff é autocontido:
aponta para a fonte canônica e não repete o corpo dela.

**Fonte canônica única**: `knowledge/decisions/2026-09-01-funil-eventos-usa-account-created-e-data-de-ocorrencia.md`
Leia **só** esse arquivo antes de começar. Não é necessário reler nenhuma conversa anterior.

## Como abrir cada sessão

Abra uma sessão nova do Claude Code em `~/Projetos/pm-loadout` e cole o prompt da linha.
Uma sessão por handoff — é isso que reduz o consumo de tokens.

| # | Handoff | Prompt de abertura | Depende de |
|---|---|---|---|
| 01 | Investigação de dados (P1–P4) | `/orquestrador execute output/handoffs/01-dados-funil.md` | nada — pode ir agora |
| 02 | Documentação e skill (D1–D2) | `/orquestrador execute output/handoffs/02-doc-skill.md` | nada — pode ir agora |
| 03 | Cards de engenharia (P6) | `/orquestrador execute output/handoffs/03-cards-engenharia.md` | decisão do PM |

## O que NÃO delegar

Estes itens não vão para sessão nenhuma — são decisão ou conversa do PM:

- **P5** — trocar o critério de "cobertura = 100%" por "informatividade". Muda regra
  estrutural do painel. Decida antes de alguém implementar.
- **Baseline de KR** — não usar 23,8% como meta antes de ~14 dias liquidados (hoje: 7 dias,
  4 liquidados).
- **Reabrir decisões tomadas sobre o "3.072 no telefone"** — se houve projeto, prioridade de
  squad ou compromisso de trimestre em cima daquele número, revisar. Aparecer sozinho depois
  custa mais confiança que o erro original.
- **Falar com o Jonatas antes** de o painel mudar debaixo dele. Ele originou o app. Enquadrar
  como design de evento e pipeline a montante — 4 dos 5 defeitos não são erro de quem montou
  a tela.

## Ordem recomendada

02 pode rodar em paralelo com qualquer coisa (não toca em código do app).
Dentro do 01, **P2 antes de P1**: se as flags de estado descegarem os gates, P1 muda de forma.
03 só depois do teste de provedor de SMS de custo zero — senão compromete escopo às cegas.
