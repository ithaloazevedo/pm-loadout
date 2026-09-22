---
name: auditoria-fornecedores
description: >
  Use quando for preciso validar se o VALOR de uma fatura de fornecedor (KYC,
  CPF Check, provedor de jogos, agregador) está correto, comparado ao volume
  real registrado no banco — Tradicional (trad_prd) ou Bravo (ar_bravo_prd).
  Aciona quando o pedido descrever uma fatura em linguagem natural — "recebi
  do Serasa a fatura de validação facial, 500 consultas, fatura de X reais",
  "bate a fatura do provedor Y na Bravo", "quantas transações rodaram no
  agregador Z" — mesmo sem formato fixo, já que cada fornecedor fatura de um
  jeito diferente e cada item da fatura é tratado como um item isolado (nunca
  somado com outro serviço do mesmo fornecedor). As duas casas têm
  fornecedores/configuração próprios — nunca assumir que um fato da
  Tradicional vale para a Bravo (ex.: a Bravo só usa Legitimuz para KYC, não
  Serasa).
invocation: user
inputs:
  - de qual casa é a fatura (Tradicional ou Bravo) — **sempre perguntar se
    não estiver claro**, já que os fornecedores/fatos confirmados são
    diferentes por casa
  - descrição livre da fatura: fornecedor, serviço/item específico (tratado
    isoladamente — ex. "validação facial" é um item, "revalidação de login"
    é outro item, mesmo que sejam do mesmo fornecedor), período, valor
    cobrado
  - quantidade de uso informada na fatura (ex. "500 consultas") — **sempre
    perguntar explicitamente se a Mariana não informou**, é o que permite
    traduzir a divergência de quantidade em divergência de R$
outputs:
  - se houve ou não divergência entre o valor da fatura e o valor esperado
    segundo o banco
  - se houve, a direção (banco indica mais ou menos uso que a fatura) e a
    magnitude (em quantidade e em R$, absoluto e percentual)
  - um relatório do que foi contabilizado do nosso lado (o que foi contado,
    período, ressalvas — sempre em linguagem simples, nunca em SQL/jargão)
side_effects: write-confirmed
context:
  - .claude/skills/auditoria-fornecedores/references/mapa-fornecedores.md
  - .claude/skills/auditoria-fornecedores/references/aprendizados.md
  - .claude/skills/auditoria-fornecedores/references/questionario-mariana.md
  - .claude/skills/query-trad/SKILL.md
  - .claude/skills/query-bravo/SKILL.md
completion: >
  A resposta cobre exatamente os três itens do output em linguagem simples,
  a skill perguntou por feedback ao final, e qualquer fato durável que a
  Mariana confirmou foi registrado em `references/aprendizados.md` — nunca
  uma suposição do agente registrada como se fosse confirmada.
---

# Auditoria de Faturas de Fornecedores

## Para quem

A Mariana (Head Financeira) — **não é uma pessoa técnica.** Toda a interação com ela precisa
ser em linguagem natural e didática (ver "Como falar com a Mariana" abaixo). Não é uma skill de
produto: o público é financeiro.

## Não é para

- Lançamento contábil, DRE ou conciliação de caixa com PSP/banco — isso é escopo de
  `claude-os/blow/frentes/financeiro-tesouraria.md`, não desta skill.
- Perguntas operacionais genéricas do PAM (GGR, depósitos, funil) — isso é `query-trad` puro.

Esta skill é especificamente sobre **validar se o valor cobrado por um fornecedor externo faz
sentido** dado o volume real de uso — "o fornecedor X cobrou R$ Y, o banco sustenta esse
número?". Não integra com lançamento contábil (`organizze`) — isso foi avaliado e descartado
(ver Regras): o objetivo é validar direto a partir do que a Mariana informa da fatura, sem
depender de a fatura já estar lançada em nenhum sistema.

## Como falar com a Mariana

- **Nunca usar jargão técnico com ela** — sem "SQL", "schema", "tabela", "query", nome de
  coluna. Traduzir tudo para linguagem de negócio ("vou contar quantas validações faciais da
  Serasa aconteceram em agosto no nosso sistema").
- **Antes de rodar qualquer consulta, explicar em uma frase simples o que vai ser verificado e
  pedir o aceite dela nesses termos** — não é preciso (nem recomendado) mostrar o SQL cru para
  ela aprovar. A query em si continua sendo mostrada/registrada tecnicamente (é a regra de
  produção do `agente-dados` — nunca executar sem esse registro), só não é isso que se explica
  para a Mariana.
- **Usar números redondos e comparações simples** ao explicar divergência (ex.: "a fatura cobra
  500 validações, mas o banco só tem 480 registradas — 20 a menos, uns 4%").
- **Fechar sempre convidando feedback em linguagem simples** (ver "Aprendizado contínuo").

## Formato de entrada — cada fornecedor fatura de um jeito, e está tudo bem

Não existe um formato único de fatura — cada fornecedor descreve o que cobra à sua maneira, e
cada fatura trata os serviços que cobra como **itens separados** (ex.: Serasa/Legitimuz cobram
"validação facial" e "revalidação de login" como linhas distintas, mesmo sendo o mesmo
fornecedor). A Mariana descreve em linguagem natural o que precisa — fornecedor + item/serviço
+ período + valor cobrado — e a skill traduz isso para a tabela/filtro certos, tratando cada
item isoladamente. Exemplo real do tipo de pedido que essa skill resolve:

> "Recebi do Serasa a fatura de validação facial (onboarding) desse mês. Fatura de X reais."

**Se a Mariana não mencionar a quantidade de uso, a skill SEMPRE pergunta antes de seguir**:
"Você tem a quantidade de uso que a fatura menciona (ex.: 500 consultas)?" — sem isso, não dá
para traduzir a contagem do banco em divergência de R$, só reportar a contagem crua.

## Formato de output — exatamente três coisas, nada além

1. **Houve ou não divergência** entre o valor da fatura e o valor esperado segundo o banco.
2. **Se houve divergência**: direção (o banco sustenta mais ou menos uso que a fatura cobra) e
   magnitude — em quantidade e em R$ (absoluto e percentual). Ver "Como validar o valor" em
   `mapa-fornecedores.md` para a conta (preço unitário implícito × diferença de quantidade).
3. **Relatório do que foi contabilizado do nosso lado**: o que exatamente foi contado, em
   linguagem simples (não tabela/coluna crua), o período usado, e ressalvas relevantes (ex.:
   fuso do corte, se a quantidade da fatura não foi informada, ou — numa divergência grande —
   se a contagem pode incluir tentativas/etapas além do que o fornecedor efetivamente cobra;
   ver `mapa-fornecedores.md`).

Não adicionar causa-raiz especulativa, recomendação de ação ou qualquer outra seção além
dessas três, a menos que a Mariana peça explicitamente.

## Fluxo

1. **Checar `references/aprendizados.md`** por um fato **específico** já confirmado sobre esse
   fornecedor/item exato (preço unitário, exclusão, particularidade). Só mencionar isso à
   Mariana quando existir um fato específico sendo reaproveitado (ex.: "da última vez você
   confirmou que o preço é R$X, vou usar de novo") — regras gerais de processo deste arquivo
   (como "sempre perguntar quantidade") são orientação interna da skill, não algo para
   anunciar a ela toda vez.
2. **Identificar a casa (Tradicional ou Bravo) e o fornecedor + item/serviço específico** a
   partir da descrição da fatura, usando `references/mapa-fornecedores.md` — qual banco/tabela/
   filtro representa esse item exato (ex.: "validação facial da Serasa" ≠ "CPF Check da
   Legitimuz" ≠ "revalidação de login da Serasa" — itens diferentes, mesmo que do mesmo
   fornecedor). **Se a casa não estiver clara, perguntar antes de seguir** — os fornecedores
   confirmados são diferentes por casa (ex.: a Bravo hoje só usa Legitimuz para KYC). **Nunca
   assumir o código/tipo exato só pela documentação** — se o banco tiver uma tabela de
   referência (ex.: `public.kyc_pending_action_types`), consultá-la antes de assumir — e
   lembrar que os códigos podem ser diferentes entre as duas casas. Se a descrição da Mariana já
   for específica o suficiente (ela disse "onboarding" e qual casa, por exemplo), não é preciso
   transformar a confirmação numa pergunta separada — basta embutir o item e a casa entendidos,
   em linguagem simples, na frase que descreve o que vai ser verificado (passo 6).
3. **Se a quantidade de uso não foi informada, perguntar antes de seguir.** Sem quantidade (ou
   preço unitário), não dá para validar o valor — só reportar a contagem crua do banco.
4. **Confirmar período.** Se o corte de fuso horário do fornecedor não estiver claro, declarar
   a suposição usada.
5. **Montar a consulta** a partir dos templates em `references/mapa-fornecedores.md`, sempre
   filtrando pelo fornecedor e item certos (nunca somar itens ou fornecedores diferentes sem
   que a Mariana peça explicitamente). Explicar para ela, em uma frase simples, o que vai ser
   verificado (ver "Como falar com a Mariana") antes de pedir o aceite.
6. **Delegar a execução ao `agente-dados`** — mesmas regras de sempre: registrar o SQL, esperar
   aceite (em linguagem de negócio, não aprovação de SQL cru), nunca escrever, sempre filtro de
   data/`LIMIT`, nunca expor CPF/dado pessoal (de jogador ou de fornecedor pessoa física).
7. **Responder só com os três itens do "Formato de output"**, em linguagem simples.
8. **Fechar pedindo feedback** (ver "Aprendizado contínuo") e, se a Mariana confirmar algo
   durável, registrar em `references/aprendizados.md`.

## Aprendizado contínuo

Esta skill acumula contexto ao longo do tempo em `references/aprendizados.md`, para não
repetir a mesma pergunta a cada conciliação:

- **Ao final de cada resposta, perguntar em linguagem simples**: "Isso faz sentido pra você?
  Tem alguma explicação pra divergência (ou algo sobre esse fornecedor) que eu deveria guardar
  pra próxima vez — tipo preço que mudou, uma cobrança extra, uma promoção?"
- **Só registrar em `aprendizados.md` o que a Mariana confirmar explicitamente** — nunca uma
  suposição do agente, mesmo que pareça óbvia.
- **Se um novo relato contradiz um aprendizado anterior**, perguntar a ela qual vale agora antes
  de atualizar — nunca sobrescrever silenciosamente.
- Isso é o "auto-aprimoramento" da skill: cada conciliação real deixa a próxima mais rápida e
  mais precisa, sem exigir que a Mariana reexplique o mesmo contexto todo mês.

## Regras

- **Nunca comparar sem declarar a janela de tempo e o fuso usados.** Pequena diferença de
  corte já gera divergência que não é erro real — declare isso antes de apontar "fatura errada".
- **Nunca expor CPF/CNPJ ou dado pessoal identificável** — nem de jogador, nem de fornecedor
  pessoa física.
- **Nunca misturar fornecedores ou itens/serviços na mesma contagem sem confirmar.**
  `public.kyc_pending_actions` guarda os fornecedores de KYC na mesma tabela
  (`data->>'kycProvider'`), e cada tipo de ação (`kyc_pending_action_type_id`) é um item
  faturado separadamente — sempre filtrar pelo fornecedor e item certos, nunca agrupar achando
  que é "KYC total" a menos que seja explicitamente pedido.
- **Nunca misturar Tradicional e Bravo na mesma contagem, nem herdar um fato de uma casa para a
  outra.** São bancos separados — ex.: Tradicional usa Serasa e Legitimuz para KYC; a Bravo,
  confirmado tecnicamente, usa só Legitimuz. Se a casa não estiver clara no pedido, perguntar.
- **Sem correspondência clara no mapa, pare e pergunte — nunca force o encaixe na tabela mais
  parecida.** Em especial: qualquer fornecedor/item que aponte para o schema `bc_orig` da Bravo
  (ainda não investigado) não deve ser encaixado em `integration.transactions` ou qualquer
  outra tabela só porque "parece" a mesma coisa. Dizer à Mariana "essa parte eu ainda não sei
  mapear, deixa eu confirmar antes" é sempre melhor que uma conciliação errada.
- **Sem quantidade de uso informada (ou preço unitário), não valide o valor** — pergunte
  primeiro. Reportar só a contagem do banco sem comparar com R$ é aceitável quando a Mariana
  confirma que não tem a quantidade; assumir um preço unitário é não.
- **Não integrar com `organizze` no fluxo padrão** — avaliado e descartado: o objetivo é
  validar o valor direto a partir do que a Mariana informa, não depender de a fatura já estar
  lançada em outro sistema. O schema `organizze` fica documentado em `mapa-fornecedores.md`
  só como contexto de fundo, não como parte do fluxo.
- **Nunca falar em jargão técnico com a Mariana** (ver "Como falar com a Mariana") — a query
  real continua sendo registrada tecnicamente (regra do `agente-dados`), só não é assim que se
  explica para ela.
- **Nunca gravar em `aprendizados.md` sem confirmação explícita** dela — é a mesma regra de
  "propor antes de escrever" que vale para todo o resto da plataforma.

## Referências

- `references/mapa-fornecedores.md` — onde cada categoria de fornecedor mora no banco, e a
  conta de como traduzir quantidade em R$.
- `references/aprendizados.md` — fatos confirmados pela Mariana ao longo do tempo (preços,
  exclusões, particularidades) — checar antes de cada conciliação.
- `references/questionario-mariana.md` — o que ainda falta confirmar (a maior parte já foi
  respondida diretamente pelo PM).
