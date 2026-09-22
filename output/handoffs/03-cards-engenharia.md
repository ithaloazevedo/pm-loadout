# Handoff 03 — Cards de engenharia da telemetria de cadastro (P6)

**De**: sessão Orquestrador de 02/09/2026
**Para**: nova sessão — Orquestrador + `agente-spec` + `agente-delivery`
**Skills**: `clickup-spec`

## ⚠️ Não execute sem confirmação do PM

Este handoff compromete escopo de engenharia. O PM ainda **não** autorizou abrir os cards, e
há uma dependência aberta: o teste de provedor de SMS de custo zero (dono e data não
definidos) deveria vir antes de financiar os eventos de checkpoint. Confirme antes.

## Antes de qualquer coisa

Leia **apenas** `knowledge/decisions/2026-09-01-funil-eventos-usa-account-created-e-data-de-ocorrencia.md`,
seção "Pendências abertas", item P6. Não releia conversa.

## Missão

Dois itens no ClickUp (workspace Vertical Tech), ambos de engenharia/plataforma — **não** são
mudança no dashboard:

1. **Separar a telemetria de revalidação de liveness da telemetria de cadastro.** O fluxo de
   revalidação no login reaproveita a instrumentação do cadastro e dispara `signup_started`,
   `kyc_*` e `registration_completed` para conta antiga que está só entrando. Resolve na
   origem, para qualquer consumidor — hoje cada consumidor precisa do próprio filtro de
   coorte. Contexto e números na fonte canônica (Contexto, item 1).
2. **Adicionar 4 eventos de checkpoint em fronteira de segmento**, em vez de consertar os 9
   gates cegos. O argumento: 9 gates cegos custam 9 correções; 4 checkpoints em fronteira
   dão localização de perda suficiente para decidir onde investir. Se o handoff 01 (P2)
   já tiver descegado gates via flags de estado, **reduza o escopo deste item** antes de
   abrir — pode virar 2 checkpoints, ou nenhum.

## Restrições do processo (não negociáveis)

- **Nunca escreva a descrição do card diretamente.** Passe contexto e intenção ao
  `agente-delivery`; ele aplica `template-delivery.md`. Descrição pronta repassada como corpo
  do card é anti-pattern.
- **Assignee só com confirmação explícita do PM.** Não infira dono por squad ou histórico.
- **Pendência técnica pode ficar em "❓ Aberto para refinamento técnico"; pendência de
  produto, compliance ou negócio não pode.** Triagem antes de criar.
- Card não leva especulação: sem nome de Team Lead/squad no Contexto, sem metadado de busca.
- Ao citar a tarefa criada na conversa, dê a **URL crua** (não link markdown).

## Link existente

Card 868kv6jk6 — migração da telemetria do cadastro para eventos. A decisão canônica ainda
precisa ser anexada a ele. Verifique se os dois itens novos são filhos dele ou pares.

## Primeira ação

Perguntar ao PM: abrir os dois agora, ou esperar o teste do SMS? E checar se o handoff 01
mudou o escopo do item 2.

## Critério de conclusão

Dois itens criados (ou um, se P2 tiver reduzido o escopo), com URL reportada, decisão
canônica anexada ao 868kv6jk6, e nenhum assignee atribuído sem confirmação.
