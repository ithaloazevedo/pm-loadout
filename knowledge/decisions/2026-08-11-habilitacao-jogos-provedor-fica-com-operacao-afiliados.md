# Habilitação de jogos de provedor (Banana Games) fica com squad Operação e afiliados, não com Provedora de conteúdo

**Data**: 2026-08-11
**Tomada por**: agente-delivery (execução), a pedido de Ithalo via Orquestrador
**Status**: APROVADA

---

## Contexto

Banana Games (provedora de jogos terceira) sinalizou +20 jogos ainda não ativos na Bravo e na Tradicional. Era preciso decidir em que folder/squad do ClickUp o trabalho de verificação e habilitação nasce, e se cabe um Épico guarda-chuva ou tarefas separadas por casa.

## Opções Consideradas

1. **Squad "Provedora de conteúdo"** — nome sugere ser o dono natural de integrações com provedores de jogos.
   - Prós: alinhamento nominal com o assunto.
   - Contras: ao inspecionar as tarefas reais desse folder, ele concentra o produto próprio de Loteria (motor de jogo da Vertical), não a gestão de catálogo de provedores terceiros de slot.

2. **Squad "Operação e afiliados"** (nome real no ClickUp: *Delivery:Backoffice & Integração*) — onde já vivem correções anteriores da Banana Games e a configuração de região por casa no banco de jogos (SLOT).
   - Prós: precedente direto e recente com o mesmo provedor; é quem já opera esse tipo de configuração de catálogo por casa.
   - Contras: nome do folder no ClickUp ("Backoffice & Integração") diverge do nome amigável usado no processo ("Operação e afiliados") — pode confundir quem busca pelo nome errado.

3. **Um Épico guarda-chuva com duas Tarefas filhas** vs. **duas Tarefas irmãs vinculadas, sem Épico**.
   - Épico: prós — narrativa única; contras — verificar+habilitar conteúdo já integrado é ação operacional de catálogo, não "grande entrega de valor / múltiplas sprints", fora da barra de Épico definida em `processo.md`.
   - Duas Tarefas irmãs: alinhado ao precedente real encontrado ("Configurar REGIÃO BRAVO..." / "Configurar Região Tradicional..." como tarefas irmãs na mesma squad).

## Decisão

Duas Tarefas separadas (uma por casa: Bravo e Tradicional), vinculadas entre si como itens irmãos, criadas na squad **Operação e afiliados** (folder real: Delivery:Backoffice & Integração). Fator decisivo: precedente real de trabalho no workspace — tanto correções anteriores da Banana Games quanto configuração de catálogo por casa já vivem nessa squad, e o folder "Provedora de conteúdo" na prática trata do motor de jogo próprio da Vertical, não de provedores terceiros.

## Trade-offs Aceitos

- Sem vínculo a nenhum Objetivo (OKR) — não havia Objetivo relevante cadastrado no workspace sobre portfólio/catálogo de jogos no momento da criação.
- Sem Discovery de origem — tratado como ação direta de Delivery, por ser operação sobre conteúdo já integrado.

## O que mudaria a decisão

Se surgir um padrão recorrente de habilitação de múltiplos provedores em paralelo (não só Banana Games), pode valer a pena reavaliar se isso merece um Épico "Expansão de portfólio de jogos" para agrupar essas tarefas por período, em vez de tarefas isoladas por provedor/casa.

## Impacto

- **Produto**: Módulo Jogos (catálogo/lobby) da Bravo e da Tradicional.
- **Técnico**: integração com provedor Banana Games; configuração de catálogo por casa no banco de jogos (SLOT).
- **Processo**: confirma que a squad Operação e afiliados (não Provedora de conteúdo) é quem responde por habilitação/configuração de catálogo de provedores terceiros — útil para rotear tickets futuros do mesmo tipo.

## Divergência encontrada (não é decisão, é achado a corrigir)

Campos de priorização citados na documentação de método (`Empresa`, `Impacto`, `Alcance`, `T-Shirt`, `Horizonte`, `_Projeto`, `_Classe`, `_Risco Reg.`) **não existem como custom field real** nesta lista/folder/space/workspace — confirmado via `clickup_get_custom_fields`. Só `KPIs` está de fato provisionado. Vale revisar `clickup-config.md` / `clickup-config-tech.md` contra o workspace real.

## Links

- Card no ClickUp (Bravo): https://app.clickup.com/t/868kpwagq
- Card no ClickUp (Tradicional): https://app.clickup.com/t/868kpwaj3
