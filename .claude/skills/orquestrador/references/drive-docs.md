# Drive Docs — producing well-formatted documents in Google Drive

Load this whenever a mission produces or edits a document in Google Drive (PRD, spec, brief, one-pager). It encodes hard-won constraints of the Google Drive MCP and PRD formatting best practices so we never ship a malformed doc again.

## Hard constraints of the Google Drive MCP (learned the hard way)

- **No in-place editing.** The MCP can `read_file_content`, `get_file_metadata`, `create_file`, `copy_file` — but **cannot edit the body of an existing Google Doc** and has **no delete/trash tool**. So:
  - Never claim you "overwrote" or "updated" a Doc. You can only **create a new file**.
  - When replacing a doc, create the new one and **tell the user exactly which old file(s) to trash manually** (give titles + IDs).
- **Conversion to a native Google Doc is limited.** `create_file` only auto-converts `text/plain → Google Doc` and `text/csv → Sheet`. **It does NOT convert `text/html` to a native Doc** — HTML is stored as a `.html` file (even if you set `mimeType` to the Doc type). Confirmed empirically.

## The formatting decision (pick before creating), best → worst

0. **Preferred — a native Google Docs MCP.** If a Google Docs server is connected (tools like `create_doc`, `insert_doc_elements`, `update_paragraph_style`, `batch_update_doc`), use it. It creates a true native Doc with heading styles, tables, and an outline, editable, **zero manual conversion**. This is the canonical method (chosen 2026-06). See `## Connecting a Google Docs MCP` below if the tools aren't present.
1. **Fallback (no Docs MCP) — upload HTML (`contentMimeType: "text/html"`).** Gives real `<h1>/<h2>/<h3>`, `<table>`, `<strong>`, `<ul>/<ol>`, `<pre>`. BUT this MCP stores it as an `.html` file (it does NOT convert HTML to a native Doc); the user must open it via **"Abrir com → Documentos Google"** to get an editable Doc. Best fidelity with zero setup, but one manual click.
2. **Last resort — `text/plain` → native Doc.** Converts immediately **but has no heading/table styles**. Write clean prose: NO markdown symbols, numbered/UPPERCASE titles, plain `-` bullets at most.

## Connecting a Google Docs MCP

The bundled `claude_ai_Google_Drive` connector has **no Docs API** (no `batchUpdate`), so it cannot create formatted native Docs. To get the preferred method, connect a server that wraps the Google Docs API — e.g. the open-source `workspace-mcp` (`github.com/taylorwilsdon/google_workspace_mcp`):
- Needs `uv`/`uvx`, a Google Cloud project with the **Docs + Drive APIs** enabled, and OAuth credentials (`GOOGLE_OAUTH_CLIENT_ID` / `GOOGLE_OAUTH_CLIENT_SECRET`).
- Register (stdio): `claude mcp add --scope user --env GOOGLE_OAUTH_CLIENT_ID=... --env GOOGLE_OAUTH_CLIENT_SECRET=... --transport stdio google-docs -- uvx workspace-mcp --tool-tier core`
- **Do not name the server `workspace`** — that name is reserved by Claude Code and skipped at load.

## Never do this

- **Never send raw markdown as `text/plain`.** Google imports it literally: you get visible `#`, `*`, `\-`, `\#`, escaped punctuation, and zero heading styles. This is exactly what produced the "mal formatado" doc.
- **Never paste raw 4-byte emoji into `text/plain`.** Encoding corrupts them (🔥 became `ð¥`). In HTML, use entities: `&#128293;` (🔥), `&#10003;` (✓). Always include `<meta charset="utf-8">`.

## Always do this

- After creating, **verify**: call `get_file_metadata` (check `fileSize` > 0 and `mimeType`) or `read_file_content`. State the result honestly.
- Land the file in the **same folder** as the source (`parentId` from the original's metadata).
- Report the artifact with its title + link, and (if it's an `.html` file) the one-line "Abrir com → Documentos Google" instruction.

## PRD structure (content best practices)

A good PRD is **user-first**, **MVP-scoped**, and a **living document**. Recommended skeleton (maps onto the ClickUp hierarchy used by `clickup-spec`):

1. **Title + metadata block** — status, version, date, owner, product, audience, north-star metric.
2. **Executive summary** — vision, the bet, strategic objective, KPIs, in one paragraph.
3. **Roadmap Item (strategic bet)** — pain, product direction, target audience, north star + secondary objectives, value hypothesis, success signal, positioning.
4. **Discovery** — assumptions to test, options/mechanics under exploration, open questions, compliance to confirm.
5. **Delivery (v1)** — scope, navigation/architecture, screen-by-screen spec, data model, tracking events, design tokens, prototype/build handoff.
6. **Subtasks** — deliverable breakdown.
7. **Cross-cutting** — phasing (v1/v2/v3), success metrics, risks & open questions, compliance, references.

Keep facts/assumptions/recommendations/open-questions separated (Juninho's operating rule). Cite sources for any external claim.
