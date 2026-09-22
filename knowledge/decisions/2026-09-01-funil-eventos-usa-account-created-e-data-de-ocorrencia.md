# Funil de cadastro por eventos passa a usar `account_created` e data de ocorrência

**Data**: 2026-09-01 (implementada em 2026-09-02)
**Tomada por**: Ithalo Mendes (PM), via Orquestrador + agente-dados
**Status**: APROVADA — implementada

> **Governança**: em 02/09/2026 o PM assumiu a manutenção do dashboard junto com o
> Orquestrador (era mantido só pelo Jonatas Souza, que o originou). A correção foi aplicada
> direto no código. Avisar o Jonatas, que continua usando o app.

---

## Contexto

O dashboard local Geral/Turnover tem duas leituras do cadastro que não fecham. Em 01/09/2026 o Funil de Cadastro (flags em `public.entities`) mostrava 336 pré-cadastros e 237 cadastrados no dia, enquanto o Funil de Aquisição (eventos em `dwh.player_events`) mostrava 1.700 contas criadas e 1.397 cadastros concluídos. Diferença de 4x na mesma métrica, no mesmo dia.

A reconciliação contra o banco identificou três causas somadas, em ordem de peso:

1. **Evento errado no passo final (~2,3x).** `registration_completed` (`RGC`) não sinaliza conclusão de cadastro. O fluxo de revalidação de liveness no login reaproveita a instrumentação do cadastro, então dispara `signup_started`, `kyc_*` e `registration_completed` para conta antiga que está só entrando. 96% dos disparos do dia vieram de conta preexistente, com mediana de 195 dias de idade; 888 entidades passaram por revalidação de liveness no dia, nenhuma delas nova.
2. **Filtro por data de ingestão (~1,7x sobre o item anterior).** `dwh.player_events.created` é quando o evento chegou, não quando ocorreu. Dos 1.443 `RGC` ingeridos no dia, só 857 ocorreram no dia — 41% era backlog de até 7 dias.
3. **Dia parcial na comparação.** Um dia em curso comparado contra um número que carrega backlog de dias fechados.

Hipóteses descartadas com evidência: `registrationId` duplicado por tentativa (é 1:1 — 97% das entidades têm exatamente um id, e o que se multiplica é o `sessionId`); `entity_type_id = 6` estreito demais (é o único tipo criado no dia); evento apontando para entidade inexistente (zero órfãos).

O funil por eventos é também high-water-mark (`pessoas` na etapa N = quem alcançou N ou depois), o que faz etapas intermediárias parecerem 100% de conversão: só 33 pessoas emitiram "Endereço concluído" e 104 emitiram "Handoff do KYC concluído", mas 2.182 e 1.706 são contadas nelas.

## Opções Consideradas

1. **Trocar o passo final para `account_created` e o filtro para data de ocorrência**
   - Prós: `account_created` (`ACC`) fecha 98–99% com `public.entities` em todos os dias medidos (29/08 a 01/09). Correção de duas linhas.
   - Contras: exige conversão de fuso (`created` em horário local, `occurredAt` em UTC).

2. **Manter `registration_completed` e aplicar fator de correção**
   - Prós: nenhuma mudança de código.
   - Contras: o evento erra nas duas direções ao mesmo tempo — conta ~2x pessoas demais e captura só 12–19% das contas que realmente nasceram no dia. Não serve nem como valor absoluto nem como proxy de tendência.

3. **Separar o fluxo de revalidação de liveness da instrumentação do cadastro (na origem)**
   - Prós: resolve a causa raiz para qualquer consumidor futuro, não só o dashboard.
   - Contras: mudança em produção, depende de engenharia e de prazo; não desbloqueia o número agora.

## Decisão

Opção 1 no dashboard, com a Opção 3 como encaminhamento à parte para engenharia. O funil por eventos passa a usar `account_created` como marco de cadastro concluído e a filtrar por `(json_data->>'occurredAt')::timestamptz AT TIME ZONE 'America/Sao_Paulo'` em vez de `created::date`. Fator decisivo: `account_created` já existe, já está correto e reconcilia com a `entities` sem nenhuma outra mudança.

As pegadinhas foram registradas na skill `query-pam` para não se repetirem em análise ad-hoc.

## Trade-offs Aceitos

- O dashboard corrige o sintoma; o fluxo de revalidação continua poluindo o stream de eventos de cadastro para qualquer outro consumidor até a Opção 3 acontecer.
- Números de dias recentes continuam subindo por ingestão tardia (p90 de 3,4 dias) — comparação dia-a-dia só é estável depois de ~4 dias.
- A conversão de fuso é inferência a partir do offset consistente de −3h, não foi confirmada no schema.

## O que mudaria a decisão

Se `account_created` deixar de fechar com a `entities` (por exemplo, se passar a ser emitido também na revalidação), o marco precisa voltar a ser derivado direto de `public.entities`. Se a Opção 3 for priorizada e o fluxo de revalidação ganhar eventos próprios, o `registration_completed` volta a ser utilizável.

## Impacto

- **Produto**: toda leitura de conversão de cadastro feita pela aba Funil de Aquisição estava inflada em ~4x. Nenhuma decisão tomada com base nela deve ser mantida sem refazer a conta.
- **Técnico**: `dwh.player_events` (semântica de `created` e de `RGC`), `tools/dashboard-tradicional/geral_app.py` (rotas `/api/funil_jornada*`), fluxo de revalidação de liveness no login.
- **Processo**: `deleted` em `public.entities` usa sentinela `1970-01-01` para "não deletado" — `deleted IS NULL` retorna zero em silêncio. Corrigido nos exemplos da skill `query-pam`, vale conferir no resto do BI.

## Achado paralelo

`public.kyc_pending_actions` (tipo `KC`) guarda o retorno bruto do SERASAEX com **motivo de reprovação**, que o dashboard hoje não expõe — ele só distingue verificado/não verificado. Em 01/09 (dia parcial): 198 entidades "SEM RISCO APARENTE" (reconcilia com os 178–192 "verificado" do dashboard), 12 "NÃO PASSÍVEL DE ANÁLISE", 4 "COM RISCO", 1 "ALERTA DE RISCO", 37 travadas em `LINK_ABERTO` e 23 em `BIOMETRIA`. São ~77 pessoas/dia com causa identificável de perda no passo mais caro do funil. ⚠️ O payload traz CPF em texto plano — não pode subir para o dashboard.

## O que foi implementado (02/09/2026)

Em `tools/dashboard-tradicional/geral_app.py` e `dashboard.html`:

1. **`account_created` (ACC) é o marco de conclusão**; `registration_completed` saiu do
   funil. Resultado: a aba fecha com `public.entities` em 97,5% / 97,5% / 99,0% / 98,4% /
   98,2% nos dias 27 a 31/08 (antes: 4x de diferença).
2. **Recorte por data de ocorrência** (`OCC_DATE_SQL`), com o prefiltro por `created`
   esticando **para frente** (+8d) e não para trás — o evento chega depois de ocorrer. A
   expressão usa `AT TIME ZONE 'America/Sao_Paulo'`: sem isso, 16–19% dos eventos caem no
   dia errado, porque `created` está em horário de Brasília e `occurredAt` em UTC.
3. **Filtro de coorte** (`JORNADA_COORTE_SQL`) que exclui a revalidação de login por idade
   da entidade, mantendo o tráfego anônimo do topo. Remove 91,5% dos disparos de RGC.
4. **`_jornada_base_sql` unificado** nas quatro rotas — elas divergiam entre si por
   repetirem o mesmo CTE.
5. **Filtro por `player_event_type_id`** em vez de `detail`: 14,7s → 2,3s, porque só o
   primeiro é indexado (a tabela tem 362M linhas / 207 GB).
6. **Tempo entre passos passou a usar o instante de ocorrência.** Antes usava
   `min(pe.created)`, misturando o tempo do usuário com o atraso da esteira de dados.
7. **Chaves de cache versionadas** (hoje em v5 — ver Retificação): dias passados nunca
   expiram no cache, então sem bumpar a chave a correção não aparece no histórico. Bumpar
   **todas** as rotas juntas, nunca só algumas.

### Achado que a correção expôs: o meio do funil é sub-instrumentado

Trocar o high-water-mark (`maior >= n`) por contagem real de emissores revelou que o funil
**não é monotônico**. Em 29/08: 946 contas criadas, mas só 509 `email.submitted`, 267
`consent.submitted` e 219 `kyc.provider_handoff_completed`. Não se cria conta sem passar
por esses gates — logo eles não emitem evento para todo mundo. A leitura antiga forçava a
descida e escondia isso (exibia 2.182 pessoas em "Endereço concluído" quando 33 emitiram).

Tratamento: cada etapa carrega `cobertura_pct` e `instrumentacao_parcial`; a conversão só é
calculada entre marcos confiáveis consecutivos e vem `null` nos demais, em vez de um número
inventado. Gate sub-instrumentado fica fora do ranking de perdas, para o time não caçar
fricção onde só falta evento. O frontend exibe as ressalvas (`avisos[]`) acima do funil.

## Retificação (02/09/2026) — o número do telefone era impossível

Uma versão intermediária desta correção publicou **"3.072 pessoas perdidas no passo do
telefone"**. O número não podia existir: a perda total do funil é 3.971 − 946 = **3.025**.
O excesso de 47 é exatamente 946 − 899, ou seja, o próprio sub-registro do evento de
telefone. A causa foi uma tolerância de cobertura de 10% que eu havia criado: `phone.submitted`
passou com 95%, foi promovido a "marco confiável" e a manchete foi construída sobre a exceção.

Correções aplicadas:

- **`COBERTURA_MIN_GATE = 1.0`** (exato, sem tolerância). O telefone virou o 9º gate cego.
  Dos 10 gates obrigatórios, **9 são cegos** (cobertura de 8,4% a 95,0%).
- **O painel afirma apenas dois níveis**: 3.971 (`signup_started`) → 946 (`account_created`).
  Todo número intermediário é piso, não nível. O painel diz explicitamente que **não se sabe
  em que passo a perda acontece**.
- **Manchetes assinadas como limite**, porque `account_created` está em 99,0% e não em 100%:
  conversão **≥ 23,8%** (piso; 24,1% pela `entities`) e **≤ 3.025** não concluíram
  (teto; 3.015 pela `entities`). Rótulo trocado de "perda" para **"não concluíram no mesmo
  dia"** — a coorte é do mesmo dia, então quem concluiu em D+1 era contado como abandono.
- **Selo de validação fabricado, removido.** O bloco 1 exibia "✓ o marco final confere com a
  tabela de entidades (fonte independente)" sem que a rota **jamais** consultasse
  `public.entities` — renderizava sempre que `referencia.pessoas` fosse truthy. Agora há
  query real e a divergência é publicada (946 vs 956 = 1,0%, limite 3,0%).
- **Denominador limpo**: 4.721 → 3.971. Havia 750 pessoas que nunca iniciaram cadastro, das
  quais 705 entraram na coorte só por `kyc.camera_granted`. Conversão 20,0% → 23,8%.
- **Chaves de cache em v5** (`reg_steps_catalog_v5`, `jornada6|`, `jornada_dia5|`, `atrito5|`,
  `tempo_passos5|`). Dias passados nunca expiram: bumpar só algumas chaves serve payload
  antigo em silêncio para sempre.

O diagnóstico original do PM (a etapa "01 Entrada no site" estaria inflando as porcentagens)
tinha impacto medido de 20,0% → 20,1% (4 pessoas). A causa era o denominador, não a etapa.

**Conclusão que fica**: o meio do funil é **sub-instrumentado, não de alta fricção**. Não há
evidência de onde a perda acontece. Antes desta retificação havia uma manchete afirmando o
contrário.

## Pendências abertas (referenciadas pelos handoffs)

- **P1 — Limpar o número da câmera e publicar limites monótonos.** `kyc.camera_granted`
  marca 1.104 > 946 (impossível). Restringir à coorte, deduplicar por pessoa e excluir
  revalidação/retentativa. Com o número limpo, dá para afirmar "≤ 2.867 se perderam antes da
  câmera, ≥ 158 em ou depois dela" — localização fraca, mas verdadeira.
- **P2 — Reconciliar gates cegos contra as flags de estado** que a aba Geral já usa
  (`public.entities`). Se funcionar, descega vários gates sem tocar no pipeline. É o item de
  maior retorno da lista e mais barato que qualquer mudança de telemetria.
- **P3 — Quem são as 705 pessoas** que entram por `kyc.camera_granted` sem `signup_started`,
  e o filtro de coorte deve migrar de nível de evento para nível de pessoa?
- **P4 — Publicar a sobreposição de identidades `946 ∩ 3.971`.** Hoje os dois números são
  tratados como pontas da mesma coorte sem que a interseção tenha sido medida.
- **P5 — Trocar o critério "cobertura = 100%" por "informatividade"** (só entra passo com
  volume acima do marco final e com cross-check independente). Muda regra estrutural do
  painel — depende de decisão do PM.
- **P6 — Engenharia, na origem**: separar a telemetria de revalidação de liveness da de
  cadastro; e adicionar 4 eventos de checkpoint em fronteira de segmento, em vez de
  consertar os 9 gates. Cards não abertos — aguardando decisão do PM e o teste de provedor
  de SMS de custo zero.

**Não usar este painel como baseline de KR ainda.** Há 7 dias de histórico e 4 liquidados.
Se 23,8% virar meta agora, vai se mover vários pontos por conserto de medição e ninguém vai
separar isso de melhoria real. Aguardar ~14 dias liquidados.

## Correção paralela: vazamento no cache

`get_entity_ids_for_frentes` usa chave com bucket de hora, então `INSERT OR REPLACE` nunca
colidia e nascia uma linha nova por hora, com até 3,8 MB de lista de entity_ids. `cache_get`
expirava a leitura mas nunca apagava a linha. O `cache.db` tinha **1.266 linhas órfãs /
1.489 MB**. Adicionado `cache_purge()` + purga na escrita; arquivo foi de **1,4 GB para
7,6 MB**.

## Links

- Card no ClickUp: 868kv6jk6 (migração da telemetria do cadastro para eventos) — decisão a anexar
- Rotas afetadas: `/api/funil_jornada`, `/api/funil_jornada_diario`, `/api/funil_atrito`, `/api/funil_tempo_passos`
- Invariantes para quem mexer depois: bloco `# ── FUNIL DE AQUISIÇÃO` em `geral_app.py` e a seção "Governança e como mexer no código" da skill `dashboard-tradicional`
- **Pendência de engenharia**: separar a instrumentação da revalidação de liveness da do cadastro (resolve na origem, para qualquer consumidor) e completar a telemetria dos gates de e-mail/consentimento/KYC
