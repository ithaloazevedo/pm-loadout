#!/bin/bash
set -e
RUNTIME="${1:-claude}"

if [ "$RUNTIME" != "claude" ] && [ "$RUNTIME" != "codex" ] && [ "$RUNTIME" != "all" ]; then
  echo "Uso: ./install.sh [claude|codex|all]" >&2
  exit 1
fi

TMP=$(mktemp -d)
git clone --depth 1 https://github.com/ithaloazevedo/pm-loadout.git "$TMP"

if [ "$RUNTIME" = "codex" ] || [ "$RUNTIME" = "all" ]; then
  if command -v node >/dev/null 2>&1; then
    node "$TMP/scripts/build-runtimes.js"
  else
    echo "aviso: node ausente, usando .agents/ e .codex/ já commitados no repo (podem estar desatualizados)." >&2
  fi
fi

if [ "$RUNTIME" = "claude" ] || [ "$RUNTIME" = "all" ]; then
  mkdir -p ~/.claude/skills ~/.claude/agents ~/.claude/workflows
  cp -R "$TMP/.claude/skills/"* ~/.claude/skills/
  cp -R "$TMP/.claude/agents/"* ~/.claude/agents/
  cp "$TMP/.claude/workflows/banca.js" ~/.claude/workflows/
fi

if [ "$RUNTIME" = "codex" ] || [ "$RUNTIME" = "all" ]; then
  mkdir -p ~/.codex/skills ~/.codex/agents
  cp -R "$TMP/.agents/skills/"* ~/.codex/skills/
  cp -R "$TMP/.codex/agents/"* ~/.codex/agents/
fi

rm -rf "$TMP"
echo "pm-loadout instalado para $RUNTIME. Reinicie o runtime e use /orquestrador."
