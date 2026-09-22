# Serviço: Runtime Sync

**Status**: gerador manual disponível; hook automático avaliado e rebaixado por ora — ver Decision Log.

## Responsabilidade

Manter `.codex/agents/` e o subconjunto sem adaptação de runtime de `.agents/skills/` sincronizados com a
fonte única em `.claude/`, sem depender de cópia manual — que já causou drift comprovado em produção (ver
`knowledge/decisions/2026-08-11-gatilho-imediato-observabilidade-doc-desatualizada.md` e
`knowledge/decisions/2026-08-11-geracao-automatica-runtimes-codex-agents.md`).

## Fonte única vs. gerado vs. fork manual legítimo

| Caminho | Papel | Editar direto? |
|---|---|---|
| `.claude/agents/*.md` | Fonte única | Sim |
| `.claude/skills/clickup-spec/references/**` | Fonte única | Sim |
| `.codex/agents/*.toml` | **Gerado** — espelho de `.claude/agents/*.md` | **Não** — editar a fonte e rodar o comando |
| `.agents/skills/clickup-spec/references/**` | **Gerado** — espelho de `.claude/skills/clickup-spec/references/**` | **Não** — editar a fonte e rodar o comando |
| `.claude/skills/*/SKILL.md` (topo de cada skill) | Fork manual **legítimo** | Sim — cada versão pode ter adaptação de runtime intencional (ex.: banners de compatibilidade Codex, caminho de canvas, ritual de ferramenta) |
| `.agents/skills/*/SKILL.md` (topo de cada skill) | Fork manual **legítimo** | Sim — mesma lógica acima |
| Qualquer outra pasta em `.agents/skills/` (ex.: `query-trad`, `dashboard-tradicional`) | Fora do escopo do gerador | Sim — mas ver "Skills novas" abaixo antes do primeiro commit |

**Por que o escopo é restrito a agentes + `clickup-spec/references`**: varredura de termos de runtime
(`codex`, `claude code`, `.claude/canvas`, `banner`) confirmou zero ocorrências nesses dois locais — são
fatos de negócio/config puros. Já os `SKILL.md` de topo têm ocorrências legítimas de adaptação — gerar por
cima destruiria conteúdo intencional.

## Como rodar

```
node scripts/build-runtimes.js
```

Rode **sempre** depois de editar `.claude/agents/*.md` ou qualquer arquivo em
`.claude/skills/clickup-spec/references/`. O script:
- gera/atualiza `.codex/agents/*.toml` a partir do frontmatter (`name`, `description`) e do corpo de cada `.claude/agents/*.md`;
- copia verbatim `.claude/skills/clickup-spec/references/**` para `.agents/skills/clickup-spec/references/**`;
- remove arquivos órfãos nos dois destinos (um `.toml`/referência sem fonte correspondente é deletado, não deixado para trás);
- falha alto e aponta o arquivo/linha se o corpo de um agente contiver a sequência `"""` (quebraria a string TOML).

Sem dependências — só `fs`/`path` do Node.

## Por que comando manual, não hook automático (R1)

Este repositório não tem CI nem testes, e tem alta cadência de commits em conteúdo sem relação com runtime
(`knowledge/decisions/`, principalmente). Um hook de pre-commit que roda em todo commit introduziria um modo
de falha novo (bug de parsing, frontmatter em rascunho) capaz de bloquear trabalho não relacionado. A
disciplina é via protocolo documentado — mesmo padrão já usado em `services/observability.md` (R5: regra vive
uma vez, é referenciada, não duplicada por agente). Reavaliar hook automático (começando por modo
non-blocking) só se a disciplina manual falhar de novo — ver "O que mudaria a decisão" na decisão que aprovou
este serviço.

## Skills novas — triagem antes do primeiro commit versionado

Uma skill nova só deve entrar em qualquer árvore versionada (`.claude/`, `.agents/`, `.codex/`) depois de
revisada quanto a conteúdo sensível (schema de banco com colunas como `password`/`cpf`, comandos de
autenticação/token). Isso vale mesmo que a skill já exista sem commitar em mais de uma árvore — sincronizar
não substitui essa revisão.

## Relação com Agente de Evolução / Governança

Toda mudança de escopo deste serviço (o que é gerado vs. fork manual, se um hook automático volta à mesa) é
uma decisão arquitetural — segue `agente-evolucao` → `agente-governanca`, não é decidida pelo agente
operacional (`agente-delivery`, `agente-dados`) em execução normal.
