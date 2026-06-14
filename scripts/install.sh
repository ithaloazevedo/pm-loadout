#!/usr/bin/env bash
set -euo pipefail

# PM Loadout — instalador.
# A fonte canônica das skills e agentes é a pasta .claude/ na raiz do repo.
# Por padrão instala para o Claude Code (~/.claude). Use --codex para instalar também no Codex.

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_root="$(cd "$script_dir/.." && pwd)"

skills_source="$repo_root/.claude/skills"
agents_source="$repo_root/.claude/agents"

install_codex=false
for arg in "$@"; do
  case "$arg" in
    --codex) install_codex=true ;;
  esac
done

copy_tree() {
  local src="$1"; local dest="$2"
  [ -d "$src" ] || return 0
  mkdir -p "$dest"
  for item in "$src"/*; do
    [ -e "$item" ] || continue
    local name; name="$(basename "$item")"
    local target="$dest/$name"
    rm -rf "$target"
    cp -R "$item" "$target"
  done
}

# Claude Code (skills + agentes)
claude_home="${CLAUDE_HOME:-"$HOME/.claude"}"
copy_tree "$skills_source" "$claude_home/skills"
copy_tree "$agents_source" "$claude_home/agents"
echo "PM Loadout instalado no Claude Code: $claude_home/{skills,agents}"

# Codex (apenas skills) — opcional
if [ "$install_codex" = true ]; then
  codex_home="${CODEX_HOME:-"$HOME/.codex"}"
  copy_tree "$skills_source" "$codex_home/skills"
  echo "PM Loadout instalado no Codex: $codex_home/skills"
fi

echo 'Use /juninho (Claude Code) ou $juninho (Codex) para comecar.'
