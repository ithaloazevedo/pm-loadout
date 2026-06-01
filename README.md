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
| Especificacao | `linear-spec`, `linear-issues` |
| Qualidade | `service-check`, `usability-check`, `launch-tier` |
| Aprendizado | `metrics-detect`, `retrospective` |

## Agentes do Juninho

- `Scout`: discovery, necessidades, entrevistas, suposicoes e oportunidades.
- `Strategist`: priorizacao, estrategia, sequenciamento e trade-offs.
- `Scribe`: specs, Linear e artefatos claros.
- `Judge`: critica, qualidade, riscos e vieses.
- `Analyst`: metricas, lancamento, aprendizado e retrospectiva.

## Instalar

Clone o repositorio:

```powershell
git clone https://github.com/ithaloazevedo/pm-loadout.git
cd pm-loadout
```

No Windows:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\install.ps1
```

No macOS/Linux:

```bash
bash scripts/install.sh
```

Os instaladores copiam `skills/*` para `~/.codex/skills` ou para `$CODEX_HOME/skills`.

## Como usar

Comece pelo Juninho:

```text
$juninho
Tenho uma ideia de produto e quero transformar isso em uma iniciativa no Linear.
```

Ou chame uma skill diretamente quando ja souber o que precisa:

```text
$linear-spec
Crie uma iniciativa para...
```

## Nota sobre modo standalone

Algumas skills vieram de fluxos Mycelium/Superpowers e podem mencionar canvas, `.claude`, `/mycelium` ou conectores especificos. No `pm-loadout`, trate essas persistencias como opcionais: se o ambiente nao tiver esses recursos, a skill deve entregar o artefato no chat e declarar o que ficaria registrado.

Veja [docs/standalone-mode.md](docs/standalone-mode.md).

## Fontes e licenca

Este repo combina material original com skills selecionadas/adaptadas de projetos MIT:

- [obra/superpowers](https://github.com/obra/superpowers)
- [haabe/mycelium](https://github.com/haabe/mycelium)

Veja [NOTICE.md](NOTICE.md).
