# Mapa de fornecedores — onde cada fatura mora no banco

> **Objetivo confirmado com a Mariana (2026-09-10): validar se o VALOR (R$) de uma fatura de
> fornecedor está correto**, a partir do que ela informa diretamente (fornecedor, item/serviço,
> período, valor e — sempre que possível — a quantidade de uso). Não é uma integração contábil
> — o lado "lançamento no financeiro interno" (`organizze`) foi avaliado e **descartado do
> fluxo padrão** (ver seção 1). A reconciliação compara só duas coisas: o que a Mariana informa
> da fatura × o que o banco mostra de uso real.
>
> **Duas casas, mesmo formato de schema, fatos diferentes.** A plataforma tem acesso a dois
> bancos — Tradicional (`trad_prd`, via skill `query-trad`) e Bravo (`ar_bravo_prd`, via skill
> `query-bravo`) — que rodam o mesmo codebase/schema (mesmos nomes de tabela/coluna), mas são
> instâncias separadas com **fornecedores e configuração próprios**. Este documento organiza os
> fatos confirmados por casa em cada seção — **nunca aplicar um fato confirmado numa casa à
> outra sem reconfirmar** (ex.: a Tradicional usa Serasa e Legitimuz para KYC; a Bravo, confirmado
> tecnicamente em 2026-09-15, usa só Legitimuz). Se a casa não estiver clara no pedido da
> Mariana, perguntar antes de montar qualquer consulta.
>
> Nenhuma credencial ou dado de conexão vive aqui — só nomes de schema/tabela/coluna. Conexão
> real e regras de segurança estão em `.claude/skills/query-trad/SKILL.md` (Tradicional) e
> `.claude/skills/query-bravo/SKILL.md` (Bravo).

## 0. Como validar o VALOR, não só a quantidade

O banco só sabe contar **uso real** (quantidade). A fatura cobra em **R$**. Para validar o
valor sem depender de nenhuma integração contábil, a skill usa o preço unitário **implícito**
na própria fatura:

```
preço_unitário = valor_fatura ÷ quantidade_fatura   (a quantidade que a Mariana informou)
valor_esperado = preço_unitário × quantidade_banco   (contagem real do banco no período/item)
divergência_R$ = valor_esperado − valor_fatura
```

- **Se a Mariana não tiver a quantidade da fatura**, pergunte antes de seguir — sem
  quantidade (ou um preço unitário contratado à parte), não dá para traduzir a contagem do
  banco em R$. Nesse caso, reporte só a contagem do banco como referência, deixando claro que
  não foi possível validar o valor.
- **Cada item da fatura é validado isoladamente** — a Mariana confirmou que fornecedores como
  Serasa/Legitimuz cobram cada serviço (ex.: "validação facial" vs. "revalidação de login")
  como uma linha separada. Nunca some quantidade/valor de itens diferentes numa só conta.

## 1. Lado contábil — `organizze.records` (fora do fluxo padrão, contexto de fundo)

**Avaliado e descartado como parte do fluxo padrão (2026-09-10)**: a Mariana confirmou que o
objetivo é validar o valor direto a partir do que ela informa da fatura — não é necessário
integrar com o lançamento contábil interno. Fica documentado abaixo só como contexto, caso um
caso futuro precise dele (ex.: auditoria de lançamentos já feitos, não validação de fatura
nova).

Confirmado por exploração de metadados em 2026-09-10 (nenhuma linha de dado real foi lida,
só `pg_tables`/`information_schema.columns`/`COUNT(*)`): `organizze` é um schema de contas a
pagar/receber (parece ser o app "Organizze" usado internamente pelo financeiro), com 19
tabelas. As 4 potencialmente relevantes, caso um caso futuro precise:

| Tabela | Linhas (2026-09-10) | Papel |
|---|---|---|
| `organizze.records` | 22.539 | **Fato** — um lançamento por fatura/parcela: `value`, `dt_emission`, `dt_due`, `dt_paid`, `interest_value`, `fine_value`, `discount`, `amount_paid`, `pis_cofins`, `description`, `memo`, `json_data` |
| `organizze.contacts` | 975 | **Fornecedor** — `name`, `cpf_cnpj`, `person_type`. `records.contact_id → contacts.id` |
| `organizze.cost_centers` | 74 | **Centro de custo** — `records.cost_center_id → cost_centers.id` |
| `organizze.record_categories` | 1.615 | **Categoria** (hierarquia via `parent_path`) — `records.record_category_id → record_categories.id` |

⚠️ Nenhuma FK é `enforced` neste schema (mesmo padrão do resto do `trad_prd`) — os
relacionamentos acima são por convenção de nome de coluna, não checados pelo banco.

## 2. KYC / CPF Check — lado uso real

### 2.1 Tradicional (`trad_prd`, via `query-trad`)

**✅ Confirmado em 2026-09-10** (pelo PM + exploração agregada, zero PII lida): **Serasa e
Legitimuz são os dois fornecedores em uso hoje, simultaneamente** — não é migração de um para
o outro. `knowledge/domains/operacao.md` (que só cita Serasa) está desatualizado; não foi
corrigido ainda porque essa correção passa por `curador-de-contexto` (MR no claude-os), não por
este arquivo.

| Fonte | O que é | Observação |
|---|---|---|
| `public.kyc_pending_actions` | Ações de KYC por jogador. `data` (JSON) guarda `kycProvider`, `lastResult`, `lastStatus` | **Os dois fornecedores coexistem nesta mesma coluna**: `data->>'kycProvider' = 'SERASAEX'` (1.142.214 consultas) ou `'LEGITIMUZ'` (881.360 consultas), medido em 2026-09-10 sem filtro de data. Basta `WHERE data->>'kycProvider' = 'SERASAEX'` (ou `'LEGITIMUZ'`) + filtro de período — **nunca somar os dois sem que o pedido seja explicitamente "KYC total"**. `data` guarda **CPF em texto plano** — só agregar, nunca expor linha. |
| `public.cpf_queries` | Consultas de CPF (`cpf`, `response`, `json_data`, `created`) | **Não tem rótulo de fornecedor.** `json_data` é sobre notificação de cadastro (`incompleteRegistration`, `phone`, `email`), não sobre o fornecedor de KYC. `response` mistura dois formatos de payload sem chave `provider`/`vendor`: um parece bureau de dados cadastrais (`blacklist`, `gender`, `nationality`), outro parece serviço cobrado por crédito/relatório (`TotalCost`, `TotalCostInCredits`, `UniqueIdentifier`). Dá para inferir o fornecedor pela *forma* do JSON, mas não por igualdade direta — **confirmar com o time técnico se essa tabela ainda alimenta algum fluxo de faturamento antes de usá-la numa reconciliação.** |
| `dwh.player_events` | Evento de funil, tipo `KYC`/`KYCF` (falha), `FCID` (FaceIndex/biometria) | **Não é ledger de custo** — é evento operacional, útil só para checar se o volume de eventos bate na ordem de grandeza do que `kyc_pending_actions` mostra, não como fonte primária de fatura. `created` é data de **ingestão**, não de ocorrência (~41% chegam atrasados, p90 de 3,4 dias) — para corte de período real usar `(json_data->>'occurredAt')::timestamptz`, não `created`. |

**✅ Confirmado pela Mariana (2026-09-11): cada tipo de ação é faturado como item separado.**
`kyc_pending_actions` tem pelo menos os tipos `KC` (KYC/onboarding) e `LR` (revalidação de
login) em `kyc_pending_action_type_id` — a fatura trata "validação facial/onboarding" e
"revalidação de login" como linhas distintas, então a query **precisa filtrar pelo tipo exato**
do item da fatura, nunca somar `KC` + `LR` como "KYC total".

**✅ Descoberto em teste técnico (2026-09-14): existe uma tabela de referência.**
`public.kyc_pending_action_types` traduz o código (`kyc_pending_action_type_id`) para nome —
`SELECT id, name FROM public.kyc_pending_action_types;` mostra todos os tipos existentes
(confirmado ter pelo menos `KC` = "KYC" e `LR` = "LoginRevalidation"). **Sempre consultar essa
tabela antes de assumir qual código corresponde ao item que a Mariana descreveu** — pode haver
mais tipos além de `KC`/`LR` que ainda não documentamos aqui.

**⚠️ Cuidado antes de tratar uma divergência grande como erro de fatura**: o nome da tabela
(`kyc_PENDING_actions`) sugere que ela pode registrar mais de uma linha por tentativa/etapa do
fluxo de verificação, não necessariamente uma linha só por validação concluída com sucesso. Se
a contagem do banco vier muito maior que a da fatura, antes de declarar divergência real,
verificar se existe uma coluna de status/resultado (`status`, `lastStatus` no `data`) que
permita isolar só as tentativas concluídas/aprovadas, e comparar esse recorte menor contra a
fatura — o fornecedor provavelmente só cobra pela validação finalizada, não por cada tentativa.

### 2.2 Bravo (`ar_bravo_prd`, via `query-bravo`)

**✅ Confirmado tecnicamente em 2026-09-15** (consulta agregada, zero PII): a Bravo usa **só
Legitimuz** para KYC — `data->>'kycProvider' = 'LEGITIMUZ'` em `public.kyc_pending_actions`
(663.230 consultas, medido sem filtro de data). Praticamente nenhum registro de Serasa. **Não
assumir Serasa como opção para uma fatura da Bravo.**

`public.kyc_pending_action_types` da Bravo tem um conjunto **diferente** do da Tradicional:
`DA` (DeleteAccount), `EA` (EditAccount), `KC` (KYC), `PA` (PauseAccount), `RP`
(RecoveryPassword), `WD` (Withdrawal) — **não existe o tipo `LR` (revalidação de login) que a
Tradicional tem**. Sempre rodar `SELECT id, name FROM public.kyc_pending_action_types;` contra
o banco certo (Bravo ou Tradicional) antes de assumir um código — os dois bancos têm essa
mesma tabela de referência, mas com conteúdo próprio.

A mesma estrutura de `kyc_pending_actions` (coluna `data` com `kycProvider`/`lastStatus`, CPF
em texto plano) e o mesmo cuidado com divergência grande por granularidade de
tentativa/etapa (ver 2.1) se aplicam aqui — é o mesmo formato de tabela, só que noutro banco.

## 3. Transações de jogo (jogo / jogador / provedor / agregador) — lado uso real

Cadeia validada em investigação anterior (ver documento fonte anexado à criação desta skill,
`estrutura-casino.md` — rastreamento ponta a ponta com dados reais):

```
integration.provider_aggregators  (agregador — ex. Softswiss, Galaxsys)
        │
        ▼
integration.providers              (provider dentro do agregador)
        │
        ▼
integration.games                  (catálogo de jogos do provider)
        │
        ▼
integration.rounds   (1 rodada externa do provider)
        │
        ▼
integration.bets     (1+ apostas dentro da rodada; único lugar com entity_id/jogador)
        │
        ▼
integration.transactions  (débito da aposta e, se houver prêmio, crédito)
```

Pontos que importam para reconciliação de fatura:

- **`entity_id` (jogador) só existe em `bets`** — qualquer filtro por jogador precisa
  necessariamente tocar essa tabela.
- **Nenhuma FK é `enforced`** neste schema — toda relação é implícita, mantida só pela
  aplicação.
- **Uma aposta pode gerar mais de uma linha em `transactions`** (débito + crédito de prêmio) —
  se a fatura do provedor conta "transações" como uma por chamada de API, o total do banco
  pode ser maior que "uma por aposta". Confirmar com o fornecedor/Mariana o que ele está
  contando (pergunta 6 do questionário) antes de julgar uma divergência como erro.
- **`transaction_provider`** em `integration.transactions` é a chave de idempotência usada
  pela aplicação para deduplicar por id do provedor — é o candidato mais forte para bater a
  fatura linha a linha (se o fornecedor também expõe esse id), em vez de só comparar totais.
- **Performance**: `integration.rounds` não é indexada por `created` — para recortes de data,
  sempre bridgear por `bets.created`/`bets.round_id` (índice `idx_bets_entity_created`). Nunca
  filtrar `rounds.created` direto (timeout em escala).

### Template — com `entity_id` (caminho barato)

```sql
WITH game_ids AS (
    SELECT g.id
    FROM integration.games g
    JOIN integration.providers p ON p.id = g.provider_id
    JOIN integration.provider_aggregators pa ON pa.id = p.provider_aggregator_id
    WHERE (:aggregator_cod::text IS NULL OR pa.cod = :aggregator_cod)
      AND (:provider_cod::text  IS NULL OR p.cod  = :provider_cod)
      AND (:game_id::int        IS NULL OR g.id   = :game_id)
)
SELECT r.game_id, COUNT(*) AS qtd_apostas, SUM(t.value) AS valor_total
FROM integration.bets b
JOIN integration.rounds r ON r.id = b.round_id
JOIN integration.transactions t ON t.bet_id = b.id
WHERE b.entity_id = :entity_id
  AND b.created >= :date_from
  AND b.created <  :date_to
  AND r.game_id IN (SELECT id FROM game_ids)
GROUP BY r.game_id;
```

### Template — sem `entity_id`, por provedor/agregador (caminho caro — exige janela curta)

```sql
-- ATENÇÃO: rounds não tem índice em created; filtro de data vai em bets.created,
-- depois do join. Comece com 1-2 dias e rode EXPLAIN antes de EXPLAIN ANALYZE.
WITH game_ids AS (
    SELECT g.id
    FROM integration.games g
    JOIN integration.providers p ON p.id = g.provider_id
    JOIN integration.provider_aggregators pa ON pa.id = p.provider_aggregator_id
    WHERE (:aggregator_cod::text IS NULL OR pa.cod = :aggregator_cod)
      AND (:provider_cod::text  IS NULL OR p.cod  = :provider_cod)
)
SELECT r.game_id, COUNT(*) AS qtd_apostas, SUM(t.value) AS valor_total
FROM integration.rounds r
JOIN integration.bets b ON b.round_id = r.id
JOIN integration.transactions t ON t.bet_id = b.id
WHERE r.game_id IN (SELECT id FROM game_ids)
  AND b.created >= :date_from
  AND b.created <  :date_to
GROUP BY r.game_id;
```

Ambos os templates são somente leitura e ponto de partida — ajustar `GROUP BY`/colunas de
saída conforme o item exato da fatura (por jogo, por provider, por agregador, por jogador).

**Bravo (`ar_bravo_prd`, via `query-bravo`)**: mesma cadeia de tabelas e os mesmos dois
templates acima funcionam sem alteração de estrutura — confirmado que
`integration.provider_aggregators/providers/games/rounds/bets/transactions` existem lá com o
mesmo formato. **Os agregadores cadastrados são diferentes por casa** — na Bravo (levantado em
2026-09-15): Galaxsys, Everest - Sports Book, Softswiss, Vertical Loto, Banana Games, Plug N
Play, Popok, Creedroomz. Sempre confirmar `cod`/`name` no banco certo antes de assumir que um
agregador existe também na outra casa.

## 4. Ordem recomendada de trabalho numa reconciliação

1. Checar `references/aprendizados.md` por algo já confirmado sobre essa casa +
   fornecedor/item (preço unitário, exclusão, particularidade) — reaproveitar e avisar a
   Mariana em linguagem simples, dando espaço para ela corrigir se mudou.
2. **Confirmar a casa (Tradicional ou Bravo)** se não estiver clara no pedido — nunca assumir.
   Depois, identificar fornecedor + item exato a partir da descrição da fatura (ex.: "Serasa,
   validação facial/onboarding, Tradicional" → banco `trad_prd` via `query-trad`,
   `kyc_pending_actions` filtrado por `kycProvider = 'SERASAEX'` **e** o
   `kyc_pending_action_type_id` exato desse item — nunca o tipo genérico "todo KYC"; já para
   "Legitimuz, Bravo" → banco `ar_bravo_prd` via `query-bravo`).
3. Se a quantidade de uso não foi informada, perguntar antes de seguir — sem ela (ou um preço
   unitário), não dá para validar o valor, só reportar a contagem crua do banco.
4. Confirmar o período exato (e o fuso, se relevante) — declarar a suposição usada se não
   estiver explícito.
5. Montar a query de uso real na tabela certa (seção 2 ou 3 acima), sempre filtrando pelo
   fornecedor e item certos — nunca somando Serasa + Legitimuz, nem tipos diferentes de ação,
   achando que é "KYC total".
6. Explicar em uma frase simples o que vai ser verificado e pedir o aceite da Mariana nesses
   termos (não em SQL) antes de rodar via `agente-dados`.
7. Responder só com os três itens do "Formato de output" do `SKILL.md` — houve divergência?
   direção e magnitude (em quantidade e R$)? relatório do que foi contabilizado do nosso lado?
   — sempre em linguagem simples.
8. Fechar pedindo feedback (ver "Aprendizado contínuo" no `SKILL.md`) e registrar em
   `aprendizados.md` qualquer fato durável que a Mariana confirmar.
