# Aprendizados confirmados — Auditoria de Faturas de Fornecedores

Log vivo de fatos confirmados durante conciliações reais. **Só entra aqui o que foi confirmado
explicitamente** — nunca uma suposição do agente, mesmo que pareça óbvia. Antes de iniciar uma
nova conciliação, consultar este arquivo por fornecedor/item — se já existir um preço unitário,
uma exclusão ou uma particularidade confirmada, reaproveitar e avisar a Mariana em linguagem
simples que está reaproveitando algo já confirmado (ela pode corrigir se mudou).

**Três categorias de confirmação, nunca misturadas sob o mesmo selo**:
1. **Decisão de produto (PM)** — como a skill deve se comportar (ex.: o que investigar, o que
   perguntar). Não exige validação da Mariana, é escopo do PM.
2. **Fato técnico (exploração direta do banco)** — verificado por query real, independente de
   qualquer pessoa confirmar. Sólido por natureza.
3. **Repasse do PM sobre o negócio/fornecedor, pendente de confirmação direta da Mariana** —
   afirmações sobre como um fornecedor real fatura, relatadas pelo PM mas **ainda não
   validadas na prática com a Mariana**. Tratar como forte indício, não como fato definitivo,
   até a primeira conciliação real com ela confirmar ou corrigir.

Formato de cada entrada: data, fornecedor/item, o que foi aprendido, categoria, quem confirmou.

---

## 2026-09-10/11 — Fundação (antes do primeiro uso real com a Mariana)

- **Não integrar com o financeiro interno (`organizze`)**: o objetivo é validar o valor da
  fatura direto a partir do que a Mariana informa, sem depender de a fatura já estar lançada em
  outro sistema. *(Categoria 1 — decisão de produto. Confirmado por: Ithalo, PM)*
- **Sempre perguntar pela quantidade de uso** (ex.: "500 consultas") quando ela não vier
  mencionada — sem isso não dá para traduzir a contagem do banco em R$, só reportar a
  contagem crua. *(Categoria 1 — decisão de produto. Confirmado por: Ithalo, PM)*
- **Cada item da fatura é um item isolado**: Serasa e Legitimuz cobrariam cada serviço (ex.:
  "validação facial" vs. "revalidação de login") como uma linha separada, mesmo sendo o mesmo
  fornecedor — nunca somar itens diferentes numa única contagem. *(Categoria 3 — repasse do PM
  sobre como o fornecedor fatura, **ainda não confirmado diretamente pela Mariana com uma
  fatura real na mão**. Tratar como indício forte, reconfirmar na primeira conciliação real.)*
- **Serasa e Legitimuz coexistem, não é migração**: os dois são usados hoje, simultaneamente,
  para etapas diferentes de KYC/CPF Check. *(Categoria 2 — fato técnico: tecnicamente
  distinguíveis em `public.kyc_pending_actions` via `data->>'kycProvider'`
  (`SERASAEX`/`LEGITIMUZ`), confirmado por query agregada real.)*

## 2026-09-15 — Acesso à Bravo (`ar_bravo_prd`) adicionado à plataforma

- **A auditoria de fornecedores agora cobre duas casas**: Tradicional (`trad_prd`, via
  `query-trad`) e Bravo (`ar_bravo_prd`, via `query-bravo`) — mesmo formato de schema, bancos
  separados. Sempre confirmar a casa antes de montar uma consulta se não estiver clara no
  pedido. *(Categoria 1 — decisão de produto. Confirmado por: Ithalo, PM)*
- **A Bravo usa só Legitimuz para KYC** (`data->>'kycProvider' = 'LEGITIMUZ'`, 663.230
  consultas) — praticamente nenhum registro de Serasa. Diferente da Tradicional, que usa os
  dois. *(Categoria 2 — fato técnico, exploração agregada, zero PII)*
- **Tipos de ação KYC da Bravo são diferentes dos da Tradicional**:
  `public.kyc_pending_action_types` da Bravo tem `DA`, `EA`, `KC`, `PA`, `RP`, `WD` — sem o
  `LR` (revalidação de login) que a Tradicional tem. Sempre consultar essa tabela no banco
  certo antes de assumir um código. *(Categoria 2 — fato técnico)*
- **`public.vw_uw_balance` existe na Bravo com o mesmo formato da Tradicional** (56 colunas,
  testado com dado real de 01/09/2026) — segura para GGR/NGR/depósito/saque diário nas duas
  casas. *(Categoria 2 — fato técnico, confirmado em 2026-09-17)*
- **Nenhum preço unitário de fornecedor da Bravo foi confirmado ainda** — só a estrutura/fatos
  técnicos acima. O preço entra aqui só quando uma Mariana real confirmar numa conciliação.

## Nota de auditoria (2026-09-14)

Um teste de ponta a ponta da skill (rodado pelo PM, com uma "Mariana" simulada e uma fatura
fictícia de R$ 5.000,00/500 validações) escreveu automaticamente uma entrada aqui como prova de
que o mecanismo de escrita confirmada funciona. Essa entrada foi **removida** — o preço de
R$ 10,00/validação nunca foi confirmado por uma Mariana real, era só o teste validando que a
skill sabe registrar um aprendizado quando alguém confirma algo. Fica só este registro de
auditoria para não apagar o rastro do teste sem explicação; nenhum preço real está confirmado
para Serasa/validação facial ainda.

## Como registrar um novo aprendizado

Ao final de uma conciliação real com a Mariana, se ela confirmar algo que vai se repetir
(preço unitário contratado, uma taxa fixa mensal, uma exclusão de tipo de consulta, um fuso
horário específico do fornecedor etc.), adicionar uma entrada nova aqui, com a data e "quem
confirmou: Mariana". Nunca sobrescrever uma entrada antiga silenciosamente — se um novo relato
contradiz um aprendizado anterior, perguntar à Mariana qual vale agora e registrar os dois
(o antigo como superado, com a data em que deixou de valer).
