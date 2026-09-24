# Índice de Pesquisas

Evidência de pesquisa e voz do usuário para embasar análises específicas. Dados brutos de pesquisa
(planilhas, CSVs, respostas de formulário, exports de ferramenta como Smartico) vivem na pasta única
[Pesquisas](https://drive.google.com/drive/folders/1awv4DRLOPr4QNGNHlnRI5fOCz18aNb82), dentro de
`20. PRODUTO & PLATAFORMA` no Drive — ver decisão em
`knowledge/decisions/2026-09-24-hub-unico-pesquisas-drive.md`. Este índice não substitui essa pasta: aponta
para ela e guarda a curadoria (achado principal, status, decisão) que a pasta sozinha não tem.

Três tipos de entrada convivem aqui, cada um com uma regra própria de o que persistir:

- **Achados e análises** — sínteses já prontas (em geral um artifact do claude.ai). Indexamos **título,
  link e uma frase de achado principal** — não copiamos o conteúdo. Um artifact pode ser próprio ou
  compartilhado por terceiro, pode mudar depois de indexado, e link deletado é uma lacuna a registrar,
  não a inventar.
- **Instrumentos de pesquisa** — desenho de coleta (survey, formulário) sem link externo estável. Como
  não há onde apontar, o **arquivo completo vive aqui**, local ao PM Loadout.
- **Voz do cliente** — fonte viva (canal de chat com relatório semanal). Registramos o ponteiro para a
  fonte; snapshots analisados viram entradas datadas quando alguém (ou a automação, ver `docs/fontes-de-contexto.md`) sintetizar um relatório.

Antes de pedir uma pesquisa nova ou abrir um link, confira se já existe achado aqui. Ao usar um achado
numa análise específica, releia a fonte — este índice aponta pra evidência, não substitui a leitura dela.

---

## Achados e análises

| Atualizado | Título | Achado principal | Link | Status |
|---|---|---|---|---|
| 2026-09-04 | Diagnóstico de Churn | *a preencher* | https://claude.ai/artifact/JsSaJG94A3jzaGZ8WUAjx5 | resumo pendente |
| 2026-07-09 | Relatório de Chamados · 1º Semestre 2026 | *a preencher* | https://claude.ai/artifact/3oxYCyC71HyPHEBNccyuyw | resumo pendente |
| 2026-07-06 | Pesquisa de Satisfação · Loteria Tradicional | *a preencher* | https://claude.ai/artifact/SWfTMvzej4joQxM1J7kT67 | resumo pendente |
| 2026-06-23 | Naming — Loteria B2B · Shortlist Executivo | *a preencher* | https://claude.ai/artifact/2RcetGmUHYzQiG9kFdshtR | resumo pendente |
| não disponível (compartilhado) | Instabilidade do App, na Voz do Jogador | *a preencher* | https://claude.ai/artifact/XKAEoCTxcwzQxqjbv8kHPy | resumo pendente |

## Instrumentos de pesquisa

| Data | Título | Status | Arquivo |
|---|---|---|---|
| 2026-09-18 (rev. 1) | Onda 4 — Instrumento · Experiência de Plataforma (PAM) | **bloqueado para campo** — 5 pendências abertas (§7), só P1 é pergunta nova | [pesquisa-plataforma-onda4-instrumento.md](pesquisa-plataforma-onda4-instrumento.md) |
| 2026-09-18 (rev. 1) | Onda 4 — Formulário Ativos | bloqueado (herda §7 do instrumento) | [pesquisa-plataforma-onda4-form-ativos.md](pesquisa-plataforma-onda4-form-ativos.md) |
| 2026-09-18 (rev. 1) | Onda 4 — Formulário Inativos | bloqueado (herda §7 do instrumento) | [pesquisa-plataforma-onda4-form-inativos.md](pesquisa-plataforma-onda4-form-inativos.md) |
| 2026-09-18 (rev. 1) | Onda 4 — Formulário Ganhadores | bloqueado (herda §7 do instrumento) | [pesquisa-plataforma-onda4-form-ganhadores.md](pesquisa-plataforma-onda4-form-ganhadores.md) |

**Lacuna registrada:** o instrumento cita como fonte o instrumento combinado
`vertical/frentes/pesquisa-jogador/pesquisa-satisfacao-onda4-instrumento.md` (rev. 3), no blow-os. Esse
caminho não existe na cópia local do blow-os nesta máquina — não foi possível confirmar o conteúdo da
fonte citada. Tratar como lacuna, não como confirmação.

## Voz do cliente (fonte viva)

Fonte: [Canal ClickUp — Voz do cliente](https://app.clickup.com/9006076935/chat/r/8ccvn07-71131),
relatório semanal de análise de chamados. Sintetizada pela skill
[`voz-do-cliente`](../../.claude/skills/voz-do-cliente/SKILL.md) (agente `agente-discovery`) — ver
decisão [2026-09-24](../decisions/2026-09-24-automacao-semanal-voz-do-cliente.md). Rotina agendada ainda
**pendente de configuração** (push do repo + conector ClickUp na rotina) — até lá, rode
`/voz-do-cliente run` sob demanda ou consulte o canal diretamente.

| Período do relatório | Resumo principal | Sinal novo vs. recorrente | Arquivo | Thread original |
|---|---|---|---|---|
| *(nenhuma entrada ainda)* | | | | |
