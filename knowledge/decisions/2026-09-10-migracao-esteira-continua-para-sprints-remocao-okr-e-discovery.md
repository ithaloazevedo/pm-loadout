# Migração de esteira contínua para sprints, remoção do nível Objetivo (OKR/KR) e do folder Discovery & Design

**Data**: 2026-09-10
**Tomada por**: Ithalo Mendes (via Orquestrador)
**Status**: APROVADA

> **Adendo (mesma sessão)**: `clickup-rollup` foi renomeada para **`clickup-revisa-sprint`** e o comando
> `/clickup-spec sprint` foi renomeado para **`/clickup-spec plan`**, para os nomes casarem com os ritos
> (Revisão e Planejamento). O corpo abaixo já usa os nomes novos.

---

## Contexto

O Ithalo alterou o space **Vertical Tech** no ClickUp: o time passa a trabalhar por **sprints**, em vez de
esteira contínua (Backlog → Execução sem corte de tempo). A escolha foi para controlar melhor as entregas e
dar aos devs um escopo mais focado por ciclo. As sprints de squads diferentes ficam **intercaladas** (uma
semana de diferença no início) de propósito, para que pessoas compartilhadas entre squads não acumulem todos
os ritos (Planejamento, Daily, Revisão, Retrospectiva) na mesma semana.

Junto com essa mudança, duas remoções estruturais que não tinham sido anunciadas de antemão e só foram
descobertas ao inspecionar a hierarquia real do ClickUp via MCP:

- O **folder Roadmap/Strategy** (`90118093876`, continha a lista Objetivos/OKR-KR, `901114034994`) foi
  removido. Confirmado com o usuário: **a empresa decidiu não ter OKRs formais por ora** ("a empresa não tem
  maturidade suficiente para OKRs") — os Objetivos/KRs saíram do ClickUp e não vivem em lugar nenhum hoje, nem
  dentro nem fora da ferramenta.
- O **folder Discovery & Design** (`90118093877`, continha a lista Discovery, `901114029780`) também foi
  removido. Confirmado com o usuário: descoberta ficava "muito burocrática para o time" como item separado —
  hoje é uma **faixa de status dentro do próprio Backlog** de cada squad (`em refinamento` → `pronto p/
  design` → `em design`), e um item de Delivery nasce já com o tipo final, sem passar por um item de Discovery
  à parte.

O pedido original também trouxe um follow-up explícito: investigar como a feature nativa de Sprints do
ClickUp funciona e propor o que automatizar com os agentes para "gerar dados e principalmente valor para os
stakeholders" — não só documentar a estrutura nova, mas redesenhar o que os agentes fazem com ela.

## Descoberta técnica (via MCP, antes de qualquer edição)

- **Sprints — PAM**: folder nativo "Sprints" (`90118303225`), sprint ativa "Sprint 1 (7/9-20/9)"
  (`901114417832`). PAM já migrado.
- **Sprints — Backoffice**: folder nativo "Pasta do sprint" (`90118303239`), sprint "Sprint 1 (14/9-27/9)"
  (`901115365054`). Backoffice migra em 2026-09-14.
- **Squad Jogos (Provedora de conteúdo) não migrou** — segue no fluxo antigo Backlog → Execução até segunda
  ordem. Não estava no pedido original do usuário; inferido pela ausência de Sprint Folder para essa squad.
- Os dois boards de **Execução legados** (`901114029785` PAM, `901114029783` Backoffice) seguem ativos só com
  itens pré-migração — não recebem itens novos, esvaziam gradualmente via Planejamento.
- **Sprint Points (ClickApp de estimativa) não está ativo** em nenhuma Sprint Folder — sem ele, só dá para
  medir throughput por contagem de itens, não velocity.
- ClickUp nativo já resolve a cascata de itens não concluídos entre sprints (Sprint Automations) — não
  precisa de automação própria dos agentes para isso.
- 🚨 **Achado crítico não resolvido**: a automação nativa do workspace que move uma task para "Execução" ao
  setar status `priorizado` (documentada desde 2026-08-14 em `clickup-config.md`) **ainda aponta para o board
  de Execução legado**, não para a Sprint ativa. Ou seja, hoje, setar `priorizado` num item do Backlog do PAM
  puxa o item para o lugar errado. Fica documentado como alerta em `clickup-config.md` e `clickup-method.md`;
  não foi corrigido (está fora do alcance da API/MCP — é configuração de automação do workspace).
- Dois achados de estrutura real não resolvidos, deixados como pendência para o usuário, não assumidos como
  estrutura oficial: (1) um terceiro folder "Sprints" (`90118643577`, "Sprint 1 31/8-11/9") sem squad
  identificado, provável resquício de teste; (2) uma lista "Backlog do Produto" (`901114419863`) hospedada
  dentro do folder de Sprints do PAM, com fluxo de status idêntico ao antigo board da squad Jogos — parece
  estar no lugar errado.

## Decisão

Reescrever a fonte de verdade da plataforma (Knowledge Graph, skill `clickup-spec`, skill `clickup-revisa-sprint`,
agentes `agente-delivery`/`agente-spec`/`lente-produto`, orquestrador, docs de topo, ferramenta
`radar-produto`) para refletir:

1. **Hierarquia achatada**: Projeto de Delivery (Epic/Tarefa/Bug/Correção) → Subtask. Sem Objetivo (OKR/KR),
   sem Discovery separado, sem Iniciativa (já removida antes).
2. **Descoberta embutida no Backlog**: um Delivery nasce direto no Backlog do squad, já com o tipo final, e
   passa por uma faixa de status de descoberta antes de estar pronto para sprint.
3. **Modelo de sprints para PAM e Backoffice**: o comando `/clickup-spec promote` (Discovery→Delivery) foi
   **substituído** por `/clickup-spec plan` (Backlog→Sprint ativa, via `clickup_move_task`, rito de
   Planejamento). Squad Jogos continua no fluxo antigo até migrar.
4. **`clickup-revisa-sprint` redesenhada**: de "roll-up de updates no card de Objetivo" para "relatório de sprint"
   (Revisão/Retrospectiva) — entregue vs. planejado, motivo de não-conclusão, itens travados. Sem card de
   Objetivo para ancorar, o destino do relatório (comentário nos itens / Chat do ClickUp / só na conversa)
   passou a ser **escolhido com o usuário a cada execução**, não fixo.
5. **Automações propostas** (para o rito de cada sprint): Planejamento (mover Backlog→Sprint com
   confirmação, auditar board de Execução legado), Daily (sinalizar itens travados via
   `clickup_get_bulk_tasks_time_in_status`), Revisão (relatório entregue vs. planejado), Retrospectiva (tempo
   em status como insumo objetivo de gargalos; confirmar Sprint Automations ativa).

## Trade-offs Aceitos

- **Plano de Medição (handoff PM→Dados sobre eventos de instrumentação) foi descontinuado, não substituído.**
  Vivia como seção derivada no card de Objetivo — sem Objetivo, não há onde reconstruí-lo sem inventar uma
  nova estrutura. Fica como pendência explícita para o usuário decidir (por épico? num Doc?), não resolvida
  nesta sessão.
- **Reconciliação do Portfólio de Projetos também descontinuada** pelo mesmo motivo (dependia da seção 🗂️ no
  card de Objetivo).
- **`template-objetivo.md` não foi excluído**, só marcado como legado/histórico — mais conservador do que
  apagar um artefato que pode ser retomado se a empresa amadurecer para OKRs formais no futuro.
- **A automação nativa de `priorizado` não foi corrigida nesta sessão** — decisão tomada (desativá-la: o
  Backlog já funciona como fila da próxima sprint, sem necessidade de nenhum destino automático), mas a
  execução exige acesso à configuração de automações do workspace, fora do alcance do MCP disponível — ação
  manual do PM na UI do ClickUp.
- **O terceiro folder "Sprints" órfão e a lista "Backlog do Produto" mal posicionada não foram integrados à
  documentação como estrutura oficial** — ficam como pendência de limpeza manual do usuário no ClickUp.
- **A apresentação já compartilhada com o time** (`apresentacoes/novo-processo-produto-tech.html`, que mostra
  a estrutura antiga de 3 folders incluindo Roadmap e Discovery & Design) **não foi editada nesta sessão** —
  é uma peça de comunicação já distribuída; reeditá-la é decisão do usuário, não inferência automática.
- **Tensão não resolvida com a memória de sessão sobre um "OKRs Q3 2026 deck" para a diretoria** — não está
  claro se isso foi abandonado junto com a decisão de não ter OKRs formais de produto, ou se OKR de diretoria
  continua existindo fora do ClickUp/produto. Sinalizado ao usuário, não resolvido aqui.

## O que mudaria a decisão

- Se a squad Jogos migrar para sprints, `clickup-config.md`, `clickup-method.md`, `processo.md` e a
  `clickup-spec` precisam de mais uma rodada de atualização (hoje ela é tratada como exceção documentada).
  - Se a automação nativa de `priorizado` for reconfigurada para apontar para a Sprint ativa em vez do board
  legado, o alerta 🚨 em `clickup-config.md`/`clickup-method.md`/`agente-delivery.md` deixa de ser necessário.
- Se o usuário decidir reintroduzir OKRs formais no futuro, esta remoção precisa ser revertida — os arquivos
  tocados aqui (e `template-objetivo.md`, hoje legado) voltam a precisar de um "onde vive" ativo.
- Se o usuário quiser reviver o Plano de Medição ou a reconciliação de Portfólio, é uma decisão de design nova
  (que lar elas ganham sem o card de Objetivo), não uma reversão simples.

## Impacto

- **Produto**: nenhum diretamente — mudança de processo/ferramenta, não de escopo de feature.
- **Técnico**: `tools/radar-produto/server.js` tinha uma dependência hardcoded na lista Discovery
  (`901114029780`, já inexistente) — corrigida como parte desta sessão, senão o dashboard quebraria.
- **Processo**: reescrita de ~25 arquivos entre skill `clickup-spec` (config, método, templates, dicionário,
  anti-patterns), skill `clickup-revisa-sprint` (redesenho completo), agentes (`agente-delivery`, `agente-spec`,
  `lente-produto`), skill `orquestrador` (+ referências), Knowledge Graph (`processo.md`, `negocio.md`,
  `pessoas.md`, `relations.md`/`.yaml`, `README.md`), registry (`agente-estrategico.yaml`,
  `agente-dados.yaml`), docs de topo (`AGENTS.md`, `README.md`, `SERVICES.md`) e a ferramenta
  `radar-produto`. `.codex/agents/*.toml` e `.agents/skills/clickup-spec/references/**` propagados via
  `node scripts/build-runtimes.js`. Os dois `SKILL.md` de topo (`clickup-spec`, `clickup-revisa-sprint`) e o
  `SKILL.md`/referências do `orquestrador` são forks manuais — editados nas duas cópias (`.claude/` e
  `.agents/`) separadamente, já que o script de geração não os cobre.

## Links

- Sprint ativa PAM: https://app.clickup.com/9006076935/v/li/901114417832
- Sprint ativa Backoffice: https://app.clickup.com/9006076935/v/li/901115365054
- Decisão anterior que já sinalizava a estrutura de sprints como achado pontual não reconciliado:
  [2026-09-09-squad-plataforma-usa-sprints-nativas-clickup-paralelo-a-execucao.md](2026-09-09-squad-plataforma-usa-sprints-nativas-clickup-paralelo-a-execucao.md)
  — esta decisão é a reconciliação completa que aquela previa como próximo passo.
- Precedente de mesmo padrão (remoção de nível hierárquico, propagação em cascata):
  [2026-08-11-remocao-drift-iniciativa-checklist-clickup.md](2026-08-11-remocao-drift-iniciativa-checklist-clickup.md)
- Fonte de verdade reescrita: `knowledge/domains/processo.md`, `.claude/skills/clickup-spec/references/clickup-config.md`, `.claude/skills/clickup-spec/references/clickup-method.md`
