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
- `agente-delivery`: opera o processo no ClickUp (Projeto de Delivery — Backlog com faixa de descoberta embutida, e Sprint), executa a `clickup-spec`.
- `Judge`: critica, qualidade, riscos e vieses.
- `Analyst`: metricas, lancamento, aprendizado e retrospectiva.
- `Regulatory Watch`: atualizacoes legais/regulatorias de bets BR e checklist de compliance.

## Instalar

O loadout suporta Claude Code e Codex. As fontes de cada runtime são `.claude/` (Claude) e `.agents/skills` + `.codex/agents` (Codex). Clone o repositório:

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

### Codex

Ao abrir este repositório no Codex, as skills em `.agents/skills/` e os perfis em `.codex/agents/` são carregados pelo workspace. Para instalar globalmente no macOS/Linux:

```bash
mkdir -p ~/.codex/skills ~/.codex/agents
cp -R .agents/skills/* ~/.codex/skills/
cp -R .codex/agents/* ~/.codex/agents/
```

O suporte é dual: Canvas, Mycelium e as ferramentas `Read`/`Write` continuam válidos no Claude. No Codex, quando essas integrações não existirem, a skill entrega o artefato na conversa e só salva conhecimento durável em `knowledge/` quando solicitado ou confirmado.

## Como usar

Comece pelo Juninho:

```text
/juninho
Tenho uma ideia de produto e quero transformar isso em um Projeto de Delivery no ClickUp.
```

Ou chame uma skill diretamente quando ja souber o que precisa:

```text
/clickup-spec create
Crie um Projeto de Delivery para...
```

## Nota sobre modo standalone

Algumas skills vieram de fluxos Mycelium/Superpowers e podem mencionar canvas, `.claude`, `/mycelium` ou conectores específicos. Essas integrações continuam suportadas no Claude; no Codex, trate-as como opcionais quando o ambiente não as oferecer. A versão em `.agents/skills/` inclui essa compatibilidade para Codex.

Veja [docs/standalone-mode.md](docs/standalone-mode.md).

## Fontes e licenca

Este repo combina material original com skills selecionadas/adaptadas de projetos MIT:

- [obra/superpowers](https://github.com/obra/superpowers)
- [haabe/mycelium](https://github.com/haabe/mycelium)

Veja [NOTICE.md](NOTICE.md).
