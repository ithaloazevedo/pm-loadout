# Automação semanal do canal Voz do Cliente vira skill e rotina agendada

**Data**: 2026-09-24
**Tomada por**: Ithalo Mendes (via Orquestrador)
**Status**: APROVADA (com pendência de configuração — ver "O que falta")

---

## Contexto

O PM Loadout ganhou um novo espaço de conhecimento local, `knowledge/pesquisas/`, para indexar evidência
de pesquisa e voz do usuário. O canal de Chat do ClickUp "Voz do cliente"
(https://app.clickup.com/9006076935/chat/r/8ccvn07-71131) publica um relatório semanal de análise de
chamados — uma fonte viva, diferente de um achado pontual. O Ithalo propôs uma automação que busca o
relatório mais recente toda semana, sintetiza e traz o conhecimento necessário, em vez de depender de
alguém abrir o canal manualmente.

## Opções Consideradas

1. **Só a estrutura, sem skill** — a pasta/índice recebe entradas manuais quando alguém sintetizar.
   - Prós: zero risco, zero automação para manter.
   - Contras: na prática, ninguém sintetiza toda semana; a fonte vira letra morta.

2. **Skill criada, rodada sob demanda** — sem agendamento; alguém dispara `/voz-do-cliente run`.
   - Prós: mantém uma pessoa no loop antes de qualquer gravação.
   - Contras: ainda depende de lembrete humano semanal — o problema original.

3. **Skill criada + rotina agendada semanal, autônoma** — escolhida.
   - Prós: resolve o problema real (ninguém precisa lembrar); a leitura e a síntese acontecem sozinhas.
   - Contras: é uma automação recorrente e não supervisionada por padrão a cada disparo — exige guardrails
     explícitos (não inventar achado, nunca escrever de volta no ClickUp) e uma decisão separada sobre como
     o resultado chega ao repositório principal (ver "O que falta").

## Decisão

Criar a skill `voz-do-cliente` (agente `agente-discovery`) e agendar uma rotina semanal para rodá-la. A
autonomia concedida é **estritamente local**: a execução agendada pode gravar a síntese em
`knowledge/pesquisas/voz-do-cliente/` sem confirmação a cada disparo. Essa autonomia **não** se estende a
nenhuma escrita no ClickUp (comentário, mensagem) — isso continua exigindo confirmação explícita, mesmo em
modo agendado, como qualquer outra skill do PM Loadout.

## Trade-offs Aceitos

- A síntese da semana entra no conhecimento local sem uma pessoa revisar o conteúdo antes de gravar
  (dentro do escopo local). O risco é mitigado por guardrails na skill (não fabricar tema/número, marcar
  lacuna em vez de inferir, nunca incluir dado pessoal identificável), não por revisão humana prévia.
- Dados de reclamação de cliente passam a ser lidos por uma rotina rodando em ambiente de nuvem da
  Anthropic (mecanismo descoberto ao configurar o agendamento — ver "O que falta"), não apenas em sessão
  interativa local.

## O que mudaria a decisão

Se a síntese semanal produzir achado fabricado, tendência sem base ou dado pessoal vazado alguma vez, a
autonomia da gravação local deve ser revista para `write-confirmed` (revisão humana antes de gravar), como
o padrão das demais skills do PM Loadout.

## Impacto

- **Produto**: novo espaço de conhecimento (`knowledge/pesquisas/`) ganha uma fonte viva além dos achados
  pontuais e dos instrumentos de pesquisa.
- **Técnico**: primeira rotina agendada do PM Loadout que roda em ambiente de nuvem (CCR), não como cron
  local — implica checkout próprio via GitHub e conector MCP do ClickUp anexado à rotina.
- **Processo**: nenhuma pessoa precisa mais lembrar de abrir o canal toda semana.

## O que falta (pendente de configuração, fora desta conversa)

A rotina ainda não foi criada. Descobertas ao configurar via a skill `schedule`:

1. A rotina roda num ambiente de nuvem isolado, com checkout próprio do repositório via GitHub
   (`https://github.com/ithaloazevedo/pm-loadout`) — exige que a skill e os arquivos de `knowledge/pesquisas/`
   estejam commitados **e enviados ao remoto** antes do primeiro disparo.
2. Falta decidir como o resultado semanal chega de volta ao repositório: a rotina abre um PR por semana
   (checkpoint de revisão antes de virar fonte oficial) ou commita direto na branch principal (sem
   checkpoint). Nenhuma das duas foi escolhida ainda.
3. A rotina precisa do conector MCP do ClickUp anexado (disponível na conta) para ler o canal.

## Links

- Skill: `.claude/skills/voz-do-cliente/SKILL.md`
- Índice: `knowledge/pesquisas/INDEX.md`
