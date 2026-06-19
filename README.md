# PM Loadout

Biblioteca gamificada de skills para Product Managers.

O ponto de entrada recomendado e o `$juninho`: um orquestrador que identifica a missao de produto, equipa as skills certas e aciona especialistas quando precisa de uma segunda lente.

## Loadout inicial

| Area | Skills |
|---|---|
| Orquestracao | `juninho` |
| Ideacao | `brainstorming`, `bias-check`, `devils-advocate` |
| Discovery | `interview`, `user-interview`, `jtbd-map`, `user-needs-map`, `assumption-test`, `ost-builder` |
| Estrategia | `gist-plan`, `ice-score`, `wardley-map`, `cynefin-classify` |
| Especificacao | `clickup-spec`, `linear-spec`, `linear-issues` |
| Qualidade | `service-check`, `usability-check`, `launch-tier` |
| Aprendizado | `metrics-detect`, `retrospective` |

## Agentes do Juninho

- `Scout`: discovery, necessidades, entrevistas, suposicoes e oportunidades.
- `Strategist`: priorizacao, estrategia, sequenciamento e trade-offs.
- `Scribe`: specs e artefatos claros.
- `Gerenciador do ClickUp`: opera o processo no ClickUp (Roadmap, Discovery, Delivery), executa a `clickup-spec`.
- `Judge`: critica, qualidade, riscos e vieses.
- `Analyst`: metricas, lancamento, aprendizado e retrospectiva.
- `Regulatory Watch`: atualizacoes legais/regulatorias de bets BR e checklist de compliance.

## Instalar

A fonte canonica das skills e agentes e a pasta `.claude/` na raiz do repo. Clone o repositorio:

```powershell
git clone https://github.com/ithaloazevedo/pm-loadout.git
cd pm-loadout
```

Para usar fora do repo, copie as skills e agentes para a pasta global do Claude Code (`~/.claude`).

No macOS/Linux:

```bash
mkdir -p ~/.claude/skills ~/.claude/agents
cp -R .claude/skills/* ~/.claude/skills/
cp -R .claude/agents/* ~/.claude/agents/
```

No Windows (PowerShell):

```powershell
New-Item -ItemType Directory -Force $HOME\.claude\skills, $HOME\.claude\agents | Out-Null
Copy-Item -Recurse -Force .\.claude\skills\* $HOME\.claude\skills\
Copy-Item -Recurse -Force .\.claude\agents\* $HOME\.claude\agents\
```

> Para propagar exclusoes (skill ou agente removido), apague o item de destino antes de copiar.

Alternativamente, ao trabalhar dentro do proprio repo, as skills e agentes em `.claude/` ja sao reconhecidos pelo Claude Code sem instalar nada.

## Como usar

Comece pelo Juninho:

```text
/juninho
Tenho uma ideia de produto e quero transformar isso em um item de roadmap no ClickUp.
```

Ou chame uma skill diretamente quando ja souber o que precisa:

```text
/clickup-spec create
Crie um item de roadmap para...
```

## Nota sobre modo standalone

Algumas skills vieram de fluxos Mycelium/Superpowers e podem mencionar canvas, `.claude`, `/mycelium` ou conectores especificos. No `pm-loadout`, trate essas persistencias como opcionais: se o ambiente nao tiver esses recursos, a skill deve entregar o artefato no chat e declarar o que ficaria registrado.

Veja [docs/standalone-mode.md](docs/standalone-mode.md).

## Fontes e licenca

Este repo combina material original com skills selecionadas/adaptadas de projetos MIT:

- [obra/superpowers](https://github.com/obra/superpowers)
- [haabe/mycelium](https://github.com/haabe/mycelium)

Veja [NOTICE.md](NOTICE.md).
