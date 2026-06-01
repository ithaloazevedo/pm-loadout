# Standalone Mode

Some imported skills were originally written for broader agent frameworks. They may mention:

- `.claude/canvas`;
- `/mycelium:*` commands;
- `CLAUDE_PLUGIN_ROOT`;
- Claude-specific tools such as `Read`;
- Linear MCP tools.

In PM Loadout, these are optional integrations, not hard requirements.

## Rule

If the referenced system is unavailable, do not fail the task. Produce the artifact in the conversation and state what would have been persisted.

## Example

If a skill says:

> Update `.claude/canvas/opportunities.yml`.

In standalone mode, respond with:

```markdown
Nao encontrei um canvas Mycelium disponivel. Entrego abaixo o conteudo que seria registrado em `opportunities.yml`.
```

Then provide the structured artifact.

## Juninho responsibility

Juninho should detect these cases and keep the flow useful:

- treat persistence as best-effort;
- avoid claiming files or tools were updated when they were not;
- keep the PM-facing artifact complete enough to copy into Linear, Notion, Docs, or another system.
