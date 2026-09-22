# Skill de auditoria de faturas de fornecedores (KYC/CPF Check/provedores de jogos/agregadores)

**Data**: 2026-09-10
**Tomada por**: Ithalo (PM) via Orquestrador
**Status**: APROVADA

---

## Contexto

Mariana (Head Financeira, BLOW) recebe faturas de fornecedores — KYC, CPF Check, provedores
de jogos e agregadores — que às vezes vêm com divergências em relação ao uso real. Não havia
nenhuma forma de conferir rapidamente volume real (total de consultas de KYC, total de
transações por jogo/jogador/provedor) contra o banco `trad_prd` (PAM).

## Opções Consideradas

1. **Criar agente novo com conexão própria ao banco**
   - Prós: identidade dedicada para o público financeiro.
   - Contras: duplica infraestrutura de conexão, aprovação de SQL e regra anti-PII que já
     existem e funcionam em `agente-dados`/`query-pam`; contraria o princípio de governança
     da plataforma de evitar sobreposição entre agentes.

2. **Criar skill nova executada pelo `agente-dados` existente**
   - Prós: reaproveita 100% da infraestrutura de conexão/aprovação/anti-PII já validada;
     mesmo padrão já usado por `query-pam`; menor superfície para manter.
   - Contras: nenhum relevante identificado.

## Decisão

Opção 2: criar a skill `auditoria-fornecedores` (`.claude/skills/auditoria-fornecedores/`,
espelhada em `.agents/skills/auditoria-fornecedores/`), executada pelo `agente-dados`
já existente. `agente-dados.md` e `registry/agente-dados.yaml` foram atualizados para listar a
nova skill; `AGENTS.md` ganhou a entrada de catálogo do `agente-dados` (que ainda não constava
lá, apesar de já registrado em `registry/`).

Exploração de metadados no schema `organizze` (19 tabelas, antes indocumentado) confirmou que
`organizze.records`/`contacts`/`cost_centers`/`record_categories` já é o lado contábil da
fatura (fornecedor, centro de custo, categoria, valor, datas) — a skill cruza esse lado com o
lado "uso real" (`integration.bets`/`transactions` para jogo/provedor/agregador,
`public.kyc_pending_actions`/`cpf_queries` para KYC/CPF Check).

## Trade-offs Aceitos

- O mapeamento exato de qual fornecedor (Legitimuz vs. Serasa) cobre qual etapa (KYC
  documental vs. CPF Check/AML) **não foi confirmado** — ficou como pergunta em aberto no
  questionário para a Mariana, em vez de uma suposição. `knowledge/domains/operacao.md` não
  foi editado agora por causa dessa incerteza.
- Não foi lida nenhuma linha de conteúdo real de `organizze.contacts`/`records` (só
  metadados/contagem) — falta confirmar se os fornecedores já estão cadastrados lá com nome
  reconhecível, e se a quantidade da fatura (não só o valor) é lançada em algum campo.

## O que mudaria a decisão

- Se a fonte de fatura de fornecedor não estiver no `trad_prd` (ex.: sistema de ERP externo,
  planilha), a skill precisaria de uma conexão/agente própria — reavaliar então.
- Se `organizze` se mostrar irrelevante (fornecedores não cadastrados lá) após leitura de
  conteúdo aprovada, a reconciliação passa a depender só do valor/quantidade que a Mariana
  informa manualmente por fatura.

## Impacto

- **Produto**: nenhum módulo de produto afetado — é tooling interno para o financeiro.
- **Técnico**: nova skill + referências em `.claude/skills/auditoria-fornecedores/` (espelhada
  em `.agents/skills/`); `agente-dados.md`, `registry/agente-dados.yaml` e `AGENTS.md`
  atualizados; `.codex/agents/agente-dados.toml` regenerado via
  `node scripts/build-runtimes.js`.
- **Processo**: questionário entregue à Mariana (`references/questionario-mariana.md`) para
  destravar o refinamento — respostas devem alimentar uma atualização futura desta skill e,
  se confirmarem o fornecedor de KYC/CPF Check, uma atualização de
  `knowledge/domains/operacao.md` via `curador-de-contexto`.

## Links

- Documento de referência: `estrutura-casino.md` (anexado pelo usuário — mapa da cadeia de
  transação de cassino, incorporado em `references/mapa-fornecedores.md`).
- Card no ClickUp: nenhum — decisão de tooling/plataforma, não item de produto.

---

## Atualização (mesmo dia, 2026-09-10)

O primeiro trade-off acima **foi resolvido ainda nesta sessão**, antes de qualquer commit:

- O PM confirmou diretamente: **Serasa e Legitimuz são os dois fornecedores de KYC/CPF Check
  em uso hoje, simultaneamente** (não é migração de um para o outro).
- Exploração agregada (zero PII) confirmou que **os dois coexistem na mesma tabela**,
  `public.kyc_pending_actions`, distinguíveis por `data->>'kycProvider'`
  (`SERASAEX` = 1.142.214 consultas, `LEGITIMUZ` = 881.360, medido sem filtro de data).
  `public.cpf_queries` não carrega rótulo de fornecedor e provavelmente não é fonte confiável
  de fatura — sinalizado em `mapa-fornecedores.md` para confirmar com o time técnico.
- O PM também definiu o formato de output da skill: exatamente três itens (houve divergência?
  direção/magnitude? relatório do que foi contabilizado do nosso lado?) — sem causa-raiz
  especulativa a menos que pedida. `SKILL.md` foi reescrito para refletir isso.
- `knowledge/domains/operacao.md` continua não editado — a correção Serasa→Serasa+Legitimuz
  deve ir via `curador-de-contexto` num MR ao claude-os, não neste arquivo.

## Atualização (2026-09-11) — MVP fechado com PM, integração com organizze descartada

O PM validou o MVP e deu mais três respostas diretas, fechando o segundo trade-off também:

- **Integração com `organizze` (lançamento contábil) foi avaliada e descartada do fluxo
  padrão.** O objetivo é mais estreito do que o desenho original: validar se o **valor (R$)**
  da fatura está correto, direto a partir do que a Mariana informa (fornecedor, item, período,
  valor e — quando houver — quantidade), sem depender de nenhum sistema já ter a fatura
  lançada. `organizze` permanece documentado em `mapa-fornecedores.md` só como contexto de
  fundo, não como passo do fluxo.
- **A skill sempre pergunta pela quantidade de uso quando a fatura não a informa** — é o que
  permite traduzir contagem do banco em divergência de R$ (preço unitário implícito = valor da
  fatura ÷ quantidade da fatura).
- **Cada item da fatura é tratado isoladamente** — confirmado que Serasa/Legitimuz cobram cada
  tipo de ação (ex.: validação facial vs. revalidação de login) como linha separada, resolvendo
  também a dúvida técnica sobre `kyc_pending_action_type_id`.
- **Requisito de comunicação**: a Mariana não é uma pessoa técnica — a skill nunca fala em
  SQL/schema/tabela com ela, sempre traduz para linguagem de negócio, e fecha cada resposta
  convidando feedback.
- **Auto-aprimoramento**: novo arquivo `references/aprendizados.md` acumula fatos confirmados
  por ela (preço unitário, exclusões, particularidades) entre conversas — nunca uma suposição
  do agente registrada como se fosse confirmada. `SKILL.md` foi reescrito para checar esse
  arquivo no início de cada conciliação e propor um novo registro ao final.
- Espelho em `.agents/skills/auditoria-fornecedores/` ressincronizado após as mudanças.

## Atualização (2026-09-14) — validação ponta a ponta com dois testes simulados

O PM rodou dois testes reais via `agente-dados` simulando a Mariana (um sem quantidade
informada, outro com fluxo completo e divergência) para validar a skill antes do primeiro uso
real. Achados incorporados:

- **A skill seguiu o `SKILL.md` à risca** nos dois testes: checou `aprendizados.md`, nunca usou
  jargão técnico com "a Mariana", parou para perguntar quando faltava quantidade, e só
  registrou aprendizado com confirmação explícita.
- **Achado técnico real**: existe `public.kyc_pending_action_types`, uma tabela de referência
  que traduz `kyc_pending_action_type_id` para nome (`KC`="KYC", `LR`="LoginRevalidation") —
  documentado em `mapa-fornecedores.md`. A regra "nunca assumir o código, sempre consultar a
  tabela de referência" foi reforçada no `SKILL.md`.
- **Nova ressalva documentada**: `kyc_pending_actions` pode contar tentativa/etapa, não só
  validação concluída — antes de tratar uma divergência grande como erro de fatura, checar se
  há coluna de status para isolar só o que foi concluído.
- **Contaminação de teste corrigida**: o segundo teste, seguindo a instrução simulada, chegou a
  gravar em `aprendizados.md` um preço unitário (R$ 10,00/validação Serasa) que **nunca foi
  confirmado por uma Mariana real** — era só a prova de que o mecanismo de escrita confirmada
  funciona. Essa entrada fictícia foi removida e substituída por uma nota de auditoria, para não
  deixar um "fato" falso disponível para uma conciliação real futura.
- Duas clarificações de comportamento adicionadas ao `SKILL.md`: (a) só mencionar à Mariana que
  um fato foi "reaproveitado" quando é um fato específico daquele fornecedor/item — regra geral
  de processo não se anuncia; (b) confirmar o item entendido pode vir embutido na frase que
  descreve o que será verificado, sem virar uma pergunta extra quando a descrição dela já foi
  suficientemente específica.

## Atualização (2026-09-17) — Auditoria de governança: aprovada com ressalvas

`agente-governanca` revisou esta skill (junto com o acesso à Bravo, ver decisão irmã de
2026-09-15) de forma independente. Veredicto: **APROVADA COM RESSALVAS** — a arquitetura
(skill nova + `agente-dados` existente, sem agente novo) segue correta; a ressalva é sobre
status de prontidão. Achados e correções:

- **Os fatos da seção "Fundação" de `aprendizados.md` misturavam três naturezas sob o mesmo
  selo "confirmado"**: decisão de produto do PM, fato técnico verificado por query real, e
  repasse do PM sobre como fornecedores faturam — este último **nunca foi confirmado
  diretamente por uma Mariana real**. Corrigido: o arquivo agora categoriza cada entrada em 3
  tipos explícitos, e o item sobre Serasa/Legitimuz faturarem itens separados foi rebaixado
  para "indício forte, pendente de confirmação direta" em vez de fato definitivo.
- **Faltava uma regra de "sem correspondência no mapa → pare e pergunte"** — adicionada ao
  `SKILL.md`, cobrindo em especial o schema `bc_orig` da Bravo (nunca investigado) para evitar
  que um item de fatura seja encaixado à força na tabela mais parecida.
- **A skill nunca foi usada com a Mariana real** — só com duas simulações desenhadas pelo
  próprio PM. Isso valida que a skill segue o roteiro escrito, não que uma pessoa não-técnica
  de fato entende a linguagem usada. **Pendência real, não resolvida nesta rodada**: rodar (ou
  agendar) a primeira conciliação real com ela, e definir como ela efetivamente aciona a skill
  no dia a dia (acesso direto? repasse manual pelo PM?).
