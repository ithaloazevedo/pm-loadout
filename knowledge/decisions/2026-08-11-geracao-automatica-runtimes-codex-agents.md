# Geração automática de .codex/ e .agents/ a partir de .claude/, com sincronização manual em vez de hook automático

**Data**: 2026-08-11
**Tomada por**: Ithalo Mendes (via Agente de Governança, proposta do Agente de Evolução)
**Status**: APROVADA (com ressalvas)

---

## Contexto

O addendum da decisão [2026-08-11-gatilho-imediato-observabilidade-doc-desatualizada.md](2026-08-11-gatilho-imediato-observabilidade-doc-desatualizada.md) já tinha diagnosticado a causa raiz do incidente de `task_type "Épico"`: a plataforma mantém **3 árvores de runtime** (`.claude/`, `.agents/skills/`, `.codex/agents/`) com o mesmo conteúdo mantidas por cópia manual, e propôs investigação formal de `agente-evolucao` → `agente-governanca` sobre se `.agents/`/`.codex/` deveriam virar artefato gerado.

O `agente-evolucao` investigou e retornou uma Proposta de Mudança Arquitetural (Tipo: CRIAR): script `scripts/build-runtimes.js` que gera `.codex/agents/*.toml` a partir de `.claude/agents/*.md` e copia verbatim `.claude/skills/clickup-spec/references/**`, um pre-commit hook versionado (`scripts/hooks/pre-commit`, ativado via `git config core.hooksPath`), remoção de `.codex/` do `.gitignore`, primeiro commit de `.agents/`/`.codex/`, um novo `services/runtime-sync.md`, e regeneração defensiva no `install.sh`.

**Verificação independente feita antes de aceitar o diagnóstico** (não só a palavra do agente-evolucao):

- `.gitignore` confirmado: `.codex/` foi ignorado desde o commit `f8cceeb` (31/mai). `git ls-tree -r origin/main -- .agents .codex` retorna **zero arquivos** nas duas árvores — nunca foram commitadas. `install.sh` faz `git clone` do GitHub e depois `cp -R "$TMP/.agents/skills/"*` / `cp -R "$TMP/.codex/agents/"*`, que não existem no clone — **instalação Codex confirmadamente quebrada em qualquer máquina além desta**.
- Diff direto entre `.claude/skills/clickup-spec/references/clickup-config.md` (editado às 14:32 de hoje, corrigido pela decisão-irmã [2026-08-11-remocao-drift-iniciativa-checklist-clickup.md](2026-08-11-remocao-drift-iniciativa-checklist-clickup.md)) e sua cópia em `.agents/` (parada às 13:46, ainda pré-correção) mostra a cópia **inteira uma rodada atrás** — não só ~12 linhas: falta toda a seção "Módulo do PAM" (28 linhas), a tabela de custom fields ainda trata Iniciativa como ativa, a regra de folder de Delivery ainda é "pelo campo Time da Iniciativa" em vez de Squad. Confirma, com evidência fresca e independente, que **mesmo o próprio dia da correção não foi suficiente para propagar manualmente**.
- `.codex/agents/agente-delivery.toml`: confirmado via grep que **não tem nenhuma menção a "Módulo do PAM"**, enquanto `.claude/agents/agente-delivery.md` tem a seção completa e a torna campo obrigatório. Terceira confirmação do mesmo padrão de drift.
- Varredura de termos de runtime (`codex`, `claude code`, `.claude/canvas`, `banner`) confirma **zero ocorrências** em `.claude/skills/clickup-spec/references/*` e em `.claude/agents/*.md` — mas **ocorrências legítimas** em `orquestrador/SKILL.md` (linha 103, integrações opcionais por ferramenta) e `jtbd/SKILL.md` (linhas 10–16, regra específica do Read-before-Write do Claude Code). Isso confirma que o escopo restrito da proposta (gerar só agentes + clickup-spec/references, nunca SKILL.md de topo) está correto e não é arbitrário.
- Varredura de segredos em `.agents/`/`.codex/` não encontrou chave, senha ou token hardcoded — só menções a nomes de variável de ambiente e mecanismos de autenticação (token IAM da AWS, `PGPASSWORD`), no mesmo padrão descritivo já usado em outras skills. Porém `.agents/skills/query-pam/` e `.agents/skills/dashboard-tradicional/` são cópias de skills que **também estão `??` (nunca commitadas) do lado `.claude/`** — ou seja, o primeiro commit de `.agents/`/`.codex/`, se feito sem triagem, arrastaria para o git conteúdo (schema de banco com colunas `password`/`cpf`, comando de geração de token) que ainda não passou pelo crivo de revisão que qualquer skill nova deveria ter.
- `.claude/skills/clickup-config.md` (fonte) e o corpo de `.claude/agents/*.md` seguem o mesmo formato estrutural (frontmatter `name`/`description` + corpo Markdown) que o `.toml` do Codex (`name`/`description`/`developer_instructions = """..."""`) — geração determinística é tecnicamente viável, com um cuidado: corpo Markdown pode conter a sequência `"""` dentro de blocos de código, o que quebraria a string TOML se não for escapado.

## Opções Consideradas

1. **Manter status quo (cópia manual entre as 3 árvores)** — Prós: nenhuma mudança. Contras: o mesmo incidente já se repetiu duas vezes na mesma sessão (task_type e drift de Iniciativa) pela mesma causa raiz; verificação independente mostrou que a cópia manual falha mesmo no mesmo dia da correção.

2. **Proposta original do agente-evolucao — gerador + pre-commit hook automático + commit único imediato de `.agents/`/`.codex/`** — Prós: resolve o drift de conteúdo e o `install.sh` quebrado de uma vez. Contras: introduz o primeiro mecanismo de enforcement automático (hook que pode bloquear commit) num repositório que hoje não tem CI, não tem testes, e é operado por 1 PM com altíssima cadência de commits em conteúdo não relacionado a runtime (dezenas de arquivos em `knowledge/decisions/` por dia); risco de um bug de geração travar commits que nada têm a ver com `.claude/agents` ou `clickup-spec/references`. Além disso, comprometeria o commit único de `.agents/`/`.codex/` a incluir conteúdo de skills novas (`query-pam`, `dashboard-tradicional`) ainda não triadas do lado `.claude/`.

3. **Gerador com escopo idêntico ao proposto, mas hook rebaixado para comando manual documentado, sequenciamento explícito e triagem do primeiro commit — escolhida.**
   - Prós: resolve a mesma causa raiz (fonte única + geração determinística) sem adicionar um novo modo de falha que bloqueia trabalho não relacionado; mantém a plataforma consistente com seu padrão já estabelecido de disciplina via protocolo documentado (Decision Log Protocol, fast-track R4/R5, Governance Checklist) em vez de enforcement por ferramenta.
   - Contras: depende de disciplina do PM/agente para lembrar de rodar o comando após editar `.claude/agents/*.md` ou `clickup-spec/references/*` — mesmo trade-off que R2 da decisão do `task_type` já aceitou para "fonte única dentro de `.claude/`".

## Decisão

Aprovada a Opção 3. O gerador (`scripts/build-runtimes.js`), a remoção de `.codex/` do `.gitignore`, o novo `services/runtime-sync.md` e a regeneração defensiva no `install.sh` são aprovados como propostos, com quatro ressalvas como mudança mínima necessária:

**R1 — Hook automático rebaixado para comando manual documentado nesta rodada.** Em vez de `scripts/hooks/pre-commit` ativável via `git config core.hooksPath`, o gerador é invocado por comando explícito (`node scripts/build-runtimes.js`, documentado em `services/runtime-sync.md` e referenciado como passo obrigatório após editar `.claude/agents/*.md` ou `clickup-spec/references/*` — mesmo padrão de "regra vive uma vez, referenciada" já usado em R5 da decisão do `task_type`). Motivo: este repositório não tem CI nem testes, e um hook que roda em todo commit — incluindo os muitos commits diários em `knowledge/decisions/` que nada têm a ver com runtime — introduz um modo de falha novo (bug de parsing, frontmatter malformado num agente em rascunho) capaz de bloquear trabalho não relacionado. Reavaliar hook automático (começando por non-blocking/warn, não bloqueante) só se a disciplina manual falhar de novo — mesmo critério de "automação mínima após evidência de uso" já usado em [2026-08-10-evolucao-operacional-pm-loadout.md](2026-08-10-evolucao-operacional-pm-loadout.md).

**R2 — Sequenciamento: gerador roda só depois de commitadas as correções de conteúdo já em andamento no `.claude/`.** No momento desta decisão, `.claude/skills/clickup-spec/references/clickup-config.md` e arquivos irmãos (correção de Iniciativa) aparecem modificados no working tree, ainda não commitados. Rodar o gerador antes disso produziria uma primeira geração de `.agents/`/`.codex/` já desatualizada no mesmo commit em que se declara `.claude/` como fonte única, exigindo uma segunda rodada de regeneração imediatamente depois. Ordem: (1) finalizar e commitar as correções de conteúdo em andamento; (2) só então escrever/rodar o gerador contra esse estado estável; (3) commitar script + config + doc + saída gerada como commit de arquitetura separado (item 4 da proposta original já previa "separado de qualquer trabalho de conteúdo em andamento" — esta ressalva só torna a ordem explícita, não só a separação).

**R3 — Triagem explícita do primeiro commit de `.agents/`/`.codex/`, não "tudo que está no disco hoje".** `.agents/skills/query-pam/` e `.agents/skills/dashboard-tradicional/` são skills novas que **também nunca foram commitadas do lado `.claude/`** (confirmado via `git status`). O primeiro commit da árvore não deve arrastar essas skills para o git implicitamente via sync — elas passam pelo mesmo crivo de revisão de conteúdo que qualquer skill nova teria (schema de banco, colunas sensíveis, comandos de autenticação), decidido pelo PM, antes de entrar em qualquer árvore versionada.

**R4 — Parser deve escapar/validar a sequência `"""` dentro do corpo Markdown antes de gerar TOML**, e falhar de forma clara e localizável (não silenciosa) se encontrar colisão — relevante mesmo sem hook bloqueante, porque uma geração corrompida seria descoberta tarde.

Os demais itens da proposta (escopo do gerador restrito a agentes + `clickup-spec/references`, cópia verbatim sem tocar SKILL.md de topo, `services/runtime-sync.md`, regeneração defensiva com fallback no `install.sh`) são aprovados sem ressalva — a varredura de termos de runtime confirmou que o escopo restrito é a linha de corte certa, não arbitrária.

## Trade-offs Aceitos

- Sem hook automático, a sincronização ainda depende de alguém lembrar de rodar o comando — mesmo trade-off que a plataforma já aceitou para "fonte única dentro de `.claude/`" (R2 da decisão do `task_type`), agora estendido para as 3 árvores. Mitigado por estar documentado como passo obrigatório, não por enforcement de ferramenta.
- `install.sh` em máquinas novas só funciona corretamente depois que o primeiro commit de `.agents/`/`.codex/` acontecer — até lá, a instalação Codex remota continua quebrada (mas já estava, então não é uma regressão).
- Skills `query-pam` e `dashboard-tradicional` ficam de fora do primeiro commit gerado até serem revisadas independentemente — atrasa a paridade completa de conteúdo entre árvores, mas evita comprometer conteúdo sensível sem revisão.

## O que mudaria a decisão

Se a disciplina manual (R1) falhar — isto é, se um novo incidente de drift acontecer mesmo com o comando documentado disponível — reavaliar hook automático, começando por modo non-blocking (roda e avisa, não bloqueia) antes de ir para bloqueante. Se o parser (R4) se mostrar frágil na prática (corpo de agente real colide com `"""`), considerar formato de saída alternativo (ex.: TOML com string delimitada por marcador único gerado, ou JSON) em vez de tentar reforçar o escaping indefinidamente.

## Impacto

- **Produto**: nenhum impacto direto a features.
- **Técnico**: primeiro script de build/geração do repositório (`scripts/build-runtimes.js`); `.codex/` sai do `.gitignore`; `install.sh` ganha passo de regeneração defensiva com fallback se `node` não existir.
- **Processo**: `.claude/agents/*.md` e `.claude/skills/clickup-spec/references/**` passam a ser a fonte única versionada; `.agents/`/`.codex/` viram artefato gerado nesse subconjunto (o resto de `.agents/skills/*` continua fork manual legítimo); novo passo manual documentado em `services/runtime-sync.md` após editar as fontes.

## Links

- Precedente e causa raiz original: [2026-08-11-gatilho-imediato-observabilidade-doc-desatualizada.md](2026-08-11-gatilho-imediato-observabilidade-doc-desatualizada.md) (addendum já propunha esta investigação)
- Decisão irmã (mesma causa raiz, conteúdo): [2026-08-11-remocao-drift-iniciativa-checklist-clickup.md](2026-08-11-remocao-drift-iniciativa-checklist-clickup.md)
- Precedente de automação mínima após evidência: [2026-08-10-evolucao-operacional-pm-loadout.md](2026-08-10-evolucao-operacional-pm-loadout.md)
- Arquivos afetados: `scripts/build-runtimes.js` (novo), `scripts/hooks/pre-commit` (não criado nesta rodada — ver R1), `.gitignore`, `install.sh`, `services/runtime-sync.md` (novo), `.agents/`, `.codex/`
