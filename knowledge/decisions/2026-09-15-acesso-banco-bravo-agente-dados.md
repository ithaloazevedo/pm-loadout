# Acesso ao banco da Bravo adicionado ao agente-dados (query-bravo)

**Data**: 2026-09-15
**Tomada por**: Ithalo (PM) via Orquestrador
**Status**: APROVADA

---

## Contexto

Ícaro enviou, via chat do ClickUp, credenciais de acesso somente-leitura ao banco de produção
da Bravo (`ar_bravo_prd`) — motivado pela investigação já concluída do furo no bloqueio SIGAP
por `PROGRAMA_SOCIAL` (`relatorio-tecnico-furo-sigap-bravo.pdf`, corrigido em 2026-09-10,
commit `5132ff98`, MR!276, ClickUp `868m4541a`). Até então, o `agente-dados`/`query-pam` só
cobria o banco da Tradicional (`trad_prd`). Com o novo acesso, ficou natural estender a
plataforma para cobrir as duas casas — inclusive a skill `auditoria-fornecedores`, recém-criada
para a Mariana.

## Opções Consideradas

1. **Só documentar o acesso, sem construir nada**
   - Prós: nenhum risco imediato.
   - Contras: acesso já validado e testado ficaria ocioso; Mariana continuaria sem cobertura
     para faturas de fornecedores da Bravo.

2. **Criar skill `query-bravo` (espelhando `query-pam`) + estender `agente-dados` e
   `auditoria-fornecedores` para as duas casas**
   - Prós: reaproveita a mesma infraestrutura de aprovação/anti-PII já validada; dá cobertura
     completa à Mariana; usa um acesso que já tinha sido concedido e testado.
   - Contras: exige tratar com cuidado uma credencial estática (não é token IAM) — mitigado
     guardando a senha só no shell local do usuário, nunca no repositório.

## Decisão

Opção 2. Criada a skill `query-bravo` (`.claude/skills/query-bravo/`, espelhada em
`.agents/skills/query-bravo/`), documentando conexão (sem a senha), schemas, tabelas grandes e
fatos técnicos confirmados da Bravo. `agente-dados.md` e `registry/agente-dados.yaml`
atualizados para operar as duas casas, com regra explícita de nunca assumir qual casa uma
pergunta ambígua se refere. `auditoria-fornecedores` (SKILL.md, `mapa-fornecedores.md`,
`aprendizados.md`) atualizada para cobrir as duas casas, com fatos confirmados separados por
casa — nunca herdados de uma para a outra. `.codex/agents/agente-dados.toml` regenerado via
`node scripts/build-runtimes.js`. Alias `bravo-prd` adicionado ao `~/.zshrc` do usuário
(mesmo padrão do `trad-prd`), com a senha só localmente, nunca no git.

**Achado técnico relevante**: a Bravo roda o mesmo formato de schema da Tradicional (mesmo
codebase `micro-api`), mas com dados/configuração próprios — confirmado que a Bravo usa **só
Legitimuz** para KYC (a Tradicional usa Serasa e Legitimuz), e que os tipos de ação em
`kyc_pending_action_types` são diferentes entre as duas casas.

## Trade-offs Aceitos

- A credencial da Bravo é usuário/senha fixo enviado por chat, não token IAM dinâmico como a
  Tradicional — risco de segurança mais alto (senha não expira automaticamente, foi
  transmitida em texto puro). Mitigado mantendo a senha fora do repositório (só no shell
  local); não é uma mitigação de infraestrutura (isso é decisão de Ícaro/infra).
- O schema `bc_orig` (6 tabelas) da Bravo não existe na Tradicional e não foi investigado —
  ficou documentado como pendência em `query-bravo/SKILL.md`, não bloqueou o resto do trabalho.
- Nenhum preço unitário de fornecedor da Bravo foi confirmado ainda — só fatos técnicos
  (estrutura, fornecedor ativo, tipos de ação). Preço entra em `aprendizados.md` só quando uma
  Mariana real confirmar.

## O que mudaria a decisão

- Se a senha da Bravo for rotacionada para um esquema IAM (como a Tradicional), atualizar
  `query-bravo/SKILL.md` e o alias `bravo-prd` para o novo método.
- Se o schema `bc_orig` se mostrar relevante para alguma investigação futura, investigar e
  documentar antes de usá-lo (não foi coberto por metadados ainda).

## Impacto

- **Produto**: nenhum módulo de produto afetado — é extensão de tooling interno de dados.
- **Técnico**: nova skill `query-bravo`; `agente-dados.md`, `registry/agente-dados.yaml`,
  `AGENTS.md`, `auditoria-fornecedores/*` atualizados; alias `bravo-prd` no shell local do
  usuário (fora do repositório).
- **Processo**: `auditoria-fornecedores` agora pode atender a Mariana também para faturas de
  fornecedores da Bravo, não só da Tradicional.

## Links

- Relatório de origem do acesso: `relatorio-tecnico-furo-sigap-bravo.pdf` (fora do repositório,
  em Downloads do usuário) — corrigido, MR!276, ClickUp `868m4541a`.
- Card no ClickUp: nenhum — decisão de tooling/plataforma, não item de produto.

## Atualização (2026-09-17) — Auditoria de governança: aprovada com ressalvas

`agente-governanca` revisou este trabalho de forma independente (ver adendo irmão em
`2026-09-10-skill-auditoria-fornecedores.md`). Veredicto: **APROVADA COM RESSALVAS**. Achados e
correções aplicadas:

- **`query-bravo/SKILL.md` não seguia o `services/skill-contract.md`** (só tinha
  `name`/`description`, igual à `query-pam` legada) — corrigido: agora tem `invocation`,
  `inputs`, `outputs`, `side_effects`, `context`, `completion`.
- **A regra de `agente-dados.md` "GGR/NGR sempre via `vw_uw_balance`" não distinguia as
  casas** — risco real de aplicar às cegas na Bravo sem confirmar que a view existe lá.
  Investigado e **confirmado com dado real**: `public.vw_uw_balance` existe na Bravo com as
  mesmas 56 colunas da Tradicional (testado com 01/09/2026 — GGR/NGR/depósitos retornaram
  valores plausíveis). Regra e `query-bravo/SKILL.md` atualizados para registrar isso
  explicitamente, em vez de deixar implícito.
- **`query-bravo/SKILL.md` estava mais raso que `query-pam`** exatamente onde custa caro
  (bancos maiores, sem exemplos de query nem views nomeadas) — adicionadas views/mat. views
  confirmadas, um exemplo de query testado contra produção, e a seção de workflow.
- **Senha da Bravo migrada do `~/.zshrc` (texto puro) para o Keychain do macOS** — o alias
  `bravo-prd` agora busca via `security find-generic-password`; testado e funcionando.
  Trade-off original ("fora do git" apenas) foi substituído por uma mitigação mais forte.
- **Pendência não resolvida nesta rodada**: schema `bc_orig` da Bravo (6 tabelas) continua não
  investigado — documentado como "não usar sem investigar" em vez de ser silenciosamente
  ignorado; e o roster de agentes em `ARCHITECTURE.md` foi checado (não lista "Agente de
  Dados", mas também não lista outros agentes especializados já existentes — julgado
  consistente com o padrão atual, não corrigido para evitar uma adição arbitrária isolada).
