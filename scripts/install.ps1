param(
    [switch]$Codex,
    [string]$ClaudeHome = $(if ($env:CLAUDE_HOME) { $env:CLAUDE_HOME } else { Join-Path $HOME ".claude" }),
    [string]$CodexHome  = $(if ($env:CODEX_HOME)  { $env:CODEX_HOME }  else { Join-Path $HOME ".codex" })
)

# PM Loadout — instalador.
# A fonte canônica das skills e agentes é a pasta .claude/ na raiz do repo.
# Por padrao instala para o Claude Code. Use -Codex para instalar tambem no Codex.

$ErrorActionPreference = "Stop"

$RepoRoot     = Resolve-Path (Join-Path $PSScriptRoot "..")
$SkillsSource = Join-Path $RepoRoot ".claude/skills"
$AgentsSource = Join-Path $RepoRoot ".claude/agents"

function Copy-Tree {
    param([string]$Source, [string]$Destination)
    if (-not (Test-Path -LiteralPath $Source)) { return }
    New-Item -ItemType Directory -Force -Path $Destination | Out-Null
    Get-ChildItem -Path $Source | ForEach-Object {
        $Target = Join-Path $Destination $_.Name
        if (Test-Path -LiteralPath $Target) { Remove-Item -Recurse -Force -LiteralPath $Target }
        Copy-Item -Recurse -Force -Path $_.FullName -Destination $Target
    }
}

# Claude Code (skills + agentes)
$ClaudeRoot = [System.IO.Path]::GetFullPath($ClaudeHome)
Copy-Tree -Source $SkillsSource -Destination (Join-Path $ClaudeRoot "skills")
Copy-Tree -Source $AgentsSource -Destination (Join-Path $ClaudeRoot "agents")
Write-Host "PM Loadout instalado no Claude Code: $ClaudeRoot\{skills,agents}"

# Codex (apenas skills) — opcional
if ($Codex) {
    $CodexRoot = [System.IO.Path]::GetFullPath($CodexHome)
    Copy-Tree -Source $SkillsSource -Destination (Join-Path $CodexRoot "skills")
    Write-Host "PM Loadout instalado no Codex: $CodexRoot\skills"
}

Write-Host "Use /juninho (Claude Code) ou `$juninho (Codex) para comecar."
