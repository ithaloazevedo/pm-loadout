# Estrutura de 3 times e distinção Team Lead vs. Tech Lead

**Data**: 2026-07-30
**Tomada por**: Ithalo Mendes
**Status**: APROVADA

---

## Contexto

Na sessão anterior (mesma data), ao estruturar a página "Organização dos Times" do handbook, foi sinalizada uma divergência: o Knowledge Graph do pm-loadout registrava uma estrutura de squads (Experiência do jogador / Operação e afiliados / Provedora de conteúdo) diferente da encontrada no Notion pessoal do Ithalo (reunião de 08/07/2026: Provedor de Jogos / Experiência do Jogador / Back Office e Integrações). Ithalo trouxe agora a estrutura real e nomeada, com papéis explícitos por pessoa — uma terceira versão, mais recente e mais detalhada que as duas anteriores.

## Decisão

Estrutura vigente — 3 times, cada um com Team Lead + Tech Lead + Devs + Product Designer + PM (+ QA quando houver):

| Time | Team Lead | Tech Lead | Devs | Designer | PM | QA |
|---|---|---|---|---|---|---|
| Backoffice & Integrações | Hugo | Ícaro | Alex | Allison | Ithalo | Tony (compartilhado c/ Plataforma) |
| Plataforma (Experiência do Jogador) | Gabriel Moreschi | Rayan | Railton, Melk | Linecker | Ithalo | Tony (compartilhado c/ Backoffice & Integrações) |
| Produto | Marcelinho | Kennedy | Gabriel, Marcos | Mateus | Victor Tarelho | Primo |

Também foi definida a distinção de papel entre **Team Lead** (pessoas e entrega: 1-on-1, carreira, planning, remove impedimentos, interface com negócio) e **Tech Lead** (técnico: padrão de código, review de PR, arquitetura, mentoria técnica) — ambos hands-on, dado o time enxuto.

## Trade-offs Aceitos

- Estrutura documentada como vigente sem confirmação cruzada com os próprios Team Leads/Tech Leads — assume-se que Ithalo tem essa informação de primeira mão.
- Papéis de PM/Designer/QA reaproveitados do Knowledge Graph anterior (não vieram na mensagem original) — podem precisar de ajuste fino.

## O que mudaria a decisão

Se a estrutura mudar de novo (já mudou 3 vezes em ~3 semanas: KG antigo → reunião 08/07 → esta) ou se os Team Leads/Tech Leads discordarem da definição de papel proposta.

## Impacto

- **Processo**: primeira vez que a distinção Team Lead vs. Tech Lead fica explícita e nomeada por pessoa — antes só existia "Engineering Lead" genérico no KG.
- **Pendências levantadas por esta estrutura** (não resolvidas, só identificadas):
  - Onde entram os 2 novos contratados (1 dev + 1 arquiteto) — nenhum dos 3 times foi indicado.
  - ~~Backoffice & Integrações não tem QA dedicado.~~ Resolvido — ver Log de Decisões.
  - Ithalo é PM em 2 times — mesmo padrão de sobrecarga já apontado na decisão de 08/07/2026, ainda sem rito de sincronização definido entre os dois backlogs.
  - Não há critério de decisão definido para quando Team Lead e Tech Lead discordam (prazo vs. qualidade técnica).
  - Não há trilha de carreira/leveling definida, apesar de "career growth" já ser responsabilidade nomeada do Team Lead.

## 📜 Log de Decisões

- 03/08 — Tony não é QA exclusivo da Plataforma: é compartilhado entre Backoffice & Integrações e Plataforma (os dois times do PAM). Gap de QA do Backoffice & Integrações estava errado, não existe — corrigido na tabela acima e no handbook.

## Links

- Knowledge Graph: `knowledge/domains/pessoas.md`
- Handbook ClickUp — página "Organização dos Times 👥": https://app.clickup.com/9006076935/v/dc/8ccvn07-62251/8ccvn07-49931
- Decisão anterior relacionada: [[2026-07-30-handbook-vertical-tech-centralizado-clickup]]
