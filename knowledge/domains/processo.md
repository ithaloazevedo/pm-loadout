# Domínio: Processo

Descreve como o trabalho de produto flui — o modelo de sprints, os tipos de item e as convenções do processo.

> **Mudança estrutural em 2026-09-10** (ver `knowledge/decisions/2026-09-10-migracao-esteira-continua-para-sprints-remocao-okr-e-discovery.md`):
> o time passou de esteira contínua para **sprints**, o nível **Objetivo (OKR/KR) foi removido** (a empresa
> decidiu não ter OKRs formais por ora — os KRs/Objetivos saíram do ClickUp e não vivem em lugar nenhum hoje) e
> o folder **Discovery & Design deixou de existir** — descoberta agora é uma faixa de status **dentro do
> próprio Backlog** de cada squad, não mais um item/folder separado. Esta página já reflete o modelo novo.

---

## Modelo de Trabalho: Sprints

Cada squad tem seu próprio **Sprint Folder nativo do ClickUp**, com uma lista por sprint (ex. "Sprint 1
(7/9 - 20/9)"). Um Projeto de Delivery nasce no **Backlog** do squad, passa pela faixa de descoberta embutida
no próprio Backlog, e só migra para dentro da **Sprint ativa** quando entra em execução — nunca antes.

**Cadência (até 2026-09-18)**: sprints de 2 semanas, com início intercalado em uma semana de diferença entre
PAM e Backoffice — de propósito, para que pessoas compartilhadas entre os dois squads não acumulassem todos os
ritos (Planejamento, Daily, Revisão, Retrospectiva) na mesma semana.

> **Mudança 2026-09-18**: Backoffice & Integrações e Plataforma se fundiram num **Time PAM** único (ver
> `knowledge/domains/pessoas.md` e [[2026-09-18-fusao-backoffice-plataforma-em-time-pam]]) — a razão de ser da
> cadência intercalada (pessoas compartilhadas entre dois times evitando sobrepor ritos) deixou de existir.
> Os ritos da semana de 2026-09-18 já rodam **unificados, um único conjunto para todo o Time PAM**, conforme
> definido por Ithalo. **O que ainda não mudou**: a estrutura técnica no ClickUp — os folders de Delivery
> ("Delivery: Experiência do jogador" e "Delivery: Operação e afiliações") e os dois Sprint Folders (Sprints —
> PAM `90118303225` e Sprints — Backoffice `90118303239`) seguem fisicamente separados, com cadências de
> sprint próprias. Fundir isso é decisão técnica/operacional em aberto — não assumir feita até confirmação
> explícita do PM (ver `clickup-config.md`).

**Ritos por sprint**: Planejamento (entrada de itens do Backlog na Sprint) · Daily · Revisão (o que foi
entregue vs. planejado) · Retrospectiva (aprendizado do ciclo, itens não concluídos migram para a próxima
sprint via automação nativa do ClickUp). **Desde 2026-09-18, um único conjunto de ritos para todo o Time PAM**
— não mais um por squad.

**Migração por squad** (situação em 2026-09-10):

| Squad | Status da migração |
|---|---|
| **PAM (Experiência do Jogador)** | Já migrado — sprint ativa em curso |
| **Backoffice** | Migra a partir de 2026-09-14 |
| **Produto (Provedora de conteúdo / Jogos)** | Ainda **não** migrado — segue no fluxo antigo Backlog → Execução até segunda ordem |

**Board de Execução legado** (`901114029785` PAM, `901114029783` Backoffice): segue ativo só com itens que já
estavam lá antes da migração. Não é alimentado com itens novos. A saída desses itens é gradual, tratada no rito
de Planejamento de cada squad — devolvidos ao Backlog (se ainda não iniciados) ou encaixados diretamente na
Sprint ativa (se já em andamento). Nunca em massa nem sem confirmação do PM. IDs e detalhe em
`clickup-config.md`.

---

## Descoberta (embutida no Backlog, não é mais um item separado)

Não existe mais um "Projeto de Discovery" com folder e tipo de tarefa próprios (Pesquisa/Protótipo/Entrevista).
Um item de Delivery nasce **já com seu tipo final** (`Epic`/`Tarefa`/`Bug`/`Correção`) direto no Backlog do
squad responsável, e a descoberta acontece como uma faixa de status **dentro do próprio Backlog**, antes de o
item estar pronto para entrar em sprint:

`backlog` → **`em refinamento`** → **`pronto p/ design`** → **`em design`** → `pronto p/ execução` → `priorizado`

> A ordem e a presença de cada status **diverge por squad** — ver `clickup-config.md` → "Status por lista"
> para o fluxo exato de cada Backlog. Não assuma paridade entre squads.

**Critério de saída da faixa de descoberta**: problema validado, escopo definido, decisões de UX fechadas — só
então o item está pronto para entrar numa sprint. Prototipação continua sempre em Figma, nunca em código,
durante essa faixa.

---

## Tipos de item no ClickUp (Delivery)

| Tipo | Quando usar | Escopo típico |
|---|---|---|
| **Épico** | Entrega grande de valor, nova funcionalidade, grande implementação | Múltiplas sprints |
| **Tarefa** | Ajuste simples, pequena entrega de valor, escopo reduzido | Uma sprint ou menos |
| **Bug** | Problema em produção afetando o sistema ou o usuário final | Urgente — prioridade alta |
| **Correção** | Subtarefa de Épico ou Tarefa criada após homologação (bug pós-entrega, inconformidade com protótipo, critério de aceite não cumprido) | Pequena — integrada ao item pai |
| **Spike** | Investigação com timebox cujo entregável é uma **resposta, não código** — quando a causa, a viabilidade ou o caminho técnico são desconhecidos | Timebox curto, dentro de uma sprint |
| **Débito técnico** | "Atalhos feitos que dificultam a evolução, gera bugs, aumenta custo e reduz a velocidade" (descrição do próprio tipo no workspace) | Varia |
| **Incidente** | Episódio de produção que precisa de remediação e post-mortem com dono e data | Varia |

> **Verificado na API em 2026-09-20** (`GET /team/9006076935/custom_item`). O workspace tem mais tipos
> cadastrados do que os usados no processo — `Pesquisa`, `Protótipo`, `Entrevista`, `Iniciativa`,
> `Resultado-chave`, `Item`, `Task`, `Person`, `Hora do Sorteio`. Os cinco primeiros são resíduo do modelo
> anterior (Discovery com folder próprio, OKR/KR, Iniciativa) e **não** devem ser usados — ver nota de
> mudança estrutural no topo desta página. **Tipo existir no workspace não significa tipo em uso.**
> `Spike` foi confirmado em uso pelo PM em 2026-09-20; `Débito técnico` e `Incidente` existem e são
> adequados ao processo atual, mas o uso corrente **não foi confirmado** — checar com o PM antes de tratar
> como padrão.
>
> ⚠️ **"Tarefa" é o tipo padrão e vem como `null` na API** — não é setável por nome, e `Item` não é
> substituto (ver memória `clickup-tarefa-task-type-padrao`).

**Status (Backlog)**: faixa de descoberta → `pronto p/ execução` → `priorizado` → `complete` / `cancelado` —
diverge por squad, ver `clickup-config.md`.

**Status (Sprint ativa — execução)**: hoje **quase idêntico entre PAM e Backoffice** (diferente da era
Backlog→Execução, em que cada squad tinha um fluxo bem distinto): `pendente` → `em desenvolvimento` →
`bloqueada` → `revisão técnica` → `em homologação` (PAM: `em homologação (alpha)`) → `deploy p/ prod` →
`cancelado` / `pronto` / `fechado`. Confirme via `clickup_get_list` antes de mover um card — não assuma que
duas sprints de squads diferentes têm status idênticos sem checar. Detalhe por lista em `clickup-config.md`.

---

## Hierarquia do Processo

```
Projeto de Delivery (Épico / Tarefa / Bug)
  nasce no Backlog do squad → faixa de descoberta (em refinamento → pronto p/ design → em design)
    → pronto p/ execução → priorizado
  → entra na Sprint ativa do squad (Planejamento)
    → execução (pendente → em desenvolvimento → ... → pronto/fechado)
  └→ Correção (subtarefa de Épico ou Tarefa, criada após homologação)
```

**Não existe nível Objetivo (OKR/KR) nem Iniciativa.** Nenhum vínculo formal a um objetivo de ciclo — a
hierarquia é achatada, o Projeto de Delivery é o nível mais alto do processo de produto.

---

## Fluxo de Status das Iniciativas (Roadmap — depreciado)

> A lista "Iniciativas" no Roadmap do ClickUp foi mantida apenas como referência histórica. O processo atual
> não usa mais este nível. **O próprio folder Roadmap/Strategy foi removido em 2026-09-10** — junto com ele,
> saiu também a lista Objetivos (OKR/KR). Ver seção "Modelo de Trabalho: Sprints" acima.

---

## Squads

> Atualizado 2026-09-10 a partir da hierarquia real do workspace ClickUp (Vertical Tech). Ver
> `knowledge/domains/pessoas.md` para papéis por time.
>
> ⚠️ **Desde 2026-09-18, "Plataforma" e "Backoffice & Integrações" são um único Time PAM organizacionalmente**
> (ver seção "Modelo de Trabalho: Sprints" acima e `knowledge/domains/pessoas.md`) — mas a estrutura técnica
> abaixo (folders/sprints separados no ClickUp) ainda não foi fundida. Trate as duas linhas abaixo como as duas
> frentes técnicas do Time PAM, não mais como dois times distintos com PMs/ritos próprios.

| Squad (frente técnica no ClickUp) | Folder de Delivery no ClickUp | Sprint Folder | Responsabilidade |
|---|---|---|---|
| **Plataforma (Experiência do Jogador / PAM)** | Delivery: Plataforma | Sprints (`90118303225`) | Time PAM — front do usuário final |
| **Backoffice & Integrações** | Delivery:Backoffice & Integração | Pasta do sprint (`90118303239`) | Time PAM — operações internas e integrações |
| **Produto (Jogos)** | Delivery: Produto | — (não migrado ainda) | Ver `knowledge/domains/pessoas.md` |

Discovery não tem mais folder próprio — cada squad trata sua faixa de descoberta dentro do seu próprio
Backlog (ver seção acima). Não há mais lista única compartilhada entre squads para isso.

---

## Convenções

- **Nomes de cards**: em linguagem do usuário, não técnica. "Estrutura base" e não "Shell". "Limite de apostas" e não "bet_limit_config".
- **Prototipação**: sempre em Figma, nunca em código, durante a faixa de descoberta do Backlog.
- **Critérios de aceite**: propostos pelo PM, refinados com engineering e QA.
- **Fonte única de spec**: o card no ClickUp. Não criar PRD paralelo no Drive.
