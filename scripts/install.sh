#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_root="$(cd "$script_dir/.." && pwd)"
codex_home="${CODEX_HOME:-"$HOME/.codex"}"
skills_source="$repo_root/skills"
skills_destination="$codex_home/skills"

mkdir -p "$skills_destination"

for skill_path in "$skills_source"/*; do
  [ -d "$skill_path" ] || continue
  skill_name="$(basename "$skill_path")"
  target="$skills_destination/$skill_name"
  rm -rf "$target"
  cp -R "$skill_path" "$target"
done

echo "PM Loadout instalado em: $skills_destination"
echo 'Use $juninho para comecar.'
