# Handoff 01 — Investigação de dados do funil de cadastro (P1–P4)

**De**: sessão Orquestrador de 02/09/2026
**Para**: nova sessão — Orquestrador + `agente-dados`
**Skills**: `query-pam`, `dashboard-tradicional`

## Antes de qualquer coisa

Leia **apenas** `knowledge/decisions/2026-09-01-funil-eventos-usa-account-created-e-data-de-ocorrencia.md`.
Ele tem o contexto completo, os números atuais e as pegadinhas do banco. Não releia conversa.

## Missão

Fechar P1 a P4 da seção "Pendências abertas" da fonte canônica. Ordem: **P2 → P1 → P3 → P4**.

P2 primeiro porque, se as flags de estado em `public.entities` descegarem os gates, o
tratamento de P1 muda de forma — e P2 é mais barato que qualquer mudança de telemetria.

## Restrições que não podem ser violadas

1. **Acesso é somente leitura.** A role em `trad_prd` tem `default_transaction_read_only=on`.
   Não tente escrever, nem "só para testar".
2. **`public.kyc_pending_actions.data` tem CPF em texto plano.** Agregado apenas. Nunca linha
   individual, nunca no dashboard, nunca no output da conversa.
3. **Não publique número não verificado no painel.** Foi exatamente esse o erro que gerou a
   retificação: uma manchete construída sobre um número que não fechava com o total.
4. **Se mexer em `tools/dashboard-tradicional/geral_app.py`**: faça backup antes (`tools/` é
   untracked no git) e bumpe a versão de **todas** as chaves de cache juntas (v5 → v6), nunca
   só algumas. Dias passados nunca expiram no cache — chave parcial serve payload velho em
   silêncio para sempre.
5. **Todo intermediário do funil é piso, não nível.** Se for publicar localização de perda,
   publique como limite (`≤` / `≥`) e diga que é limite.

## Sinal de sanidade obrigatório

Qualquer número de perda por passo tem que caber em **3.971 − 946 = 3.025** (dia 29/08).
Se não couber, o número está errado — não arredonde, investigue.

## Consultas que já foram feitas (não repita)

Há quatro sondas prontas em `tools/dashboard-tradicional/probes/` (auth IAM já resolvida,
somente leitura, replicável):

- `probe.py` / `probe2.py` — reconciliação evento × `entities`, semântica de `created`.
- `probe3.py` — quem está no denominador e quanto cada corte muda o número (gerou o
  3.971 e as 705 pessoas de P3).
- `probe4.py` — **escrito e nunca rodado**: `branch`, `owner_side` e versões do catálogo
  `dwh.registration_steps`. **Comece por aqui**: a resposta pode explicar a
  sub-instrumentação de graça — se o catálogo tem ramos, gate "cego" pode ser gate de outro
  ramo, e aí não falta evento nenhum.

## Riscos

- O `agente-dados` falhou 3x nesta investigação por erro de ambiente ("computer went to
  sleep"). Se falhar, relance — não conclua que a query está errada.
- `dwh.player_events` tem 362M linhas / 207 GB. Filtre por `player_event_type_id` (indexado),
  nunca por `detail`. Sem isso a query passa de 2s para 15s ou estoura.

## Primeira ação

Rodar `probe4.py` e responder: o catálogo de passos tem ramos (`branch`) que expliquem os 9
gates cegos, ou eles são cegos de fato?

## Critério de conclusão

- P2 respondido com evidência: as flags de estado reconciliam com os gates, sim ou não.
- Se sim: painel passa a mostrar níveis reais nos passos que reconciliaram.
- Se não: limites monótonos de P1 publicados com o número da câmera limpo, ou declarado
  explicitamente que não foi possível limpar.
- Fonte canônica atualizada com o que foi descoberto (seção "Pendências abertas").
