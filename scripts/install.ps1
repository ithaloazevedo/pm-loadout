param(
    [string]$CodexHome = $(if ($env:CODEX_HOME) { $env:CODEX_HOME } else { Join-Path $HOME ".codex" })
)

$ErrorActionPreference = "Stop"

$RepoRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
$SkillsSource = Join-Path $RepoRoot "skills"
$SkillsDestination = Join-Path ([System.IO.Path]::GetFullPath($CodexHome)) "skills"

New-Item -ItemType Directory -Force -Path $SkillsDestination | Out-Null

Get-ChildItem -Directory -Path $SkillsSource | ForEach-Object {
    $Target = Join-Path $SkillsDestination $_.Name
    if (Test-Path -LiteralPath $Target) {
        Remove-Item -Recurse -Force -LiteralPath $Target
    }
    Copy-Item -Recurse -Force -Path $_.FullName -Destination $Target
}

Write-Host "PM Loadout instalado em: $SkillsDestination"
Write-Host "Use `$juninho para comecar."
