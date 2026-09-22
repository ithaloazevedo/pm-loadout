# Reativar o Check-in Diário em produção sem esperar a reformulação que motivou o desligamento

**Data**: 2026-09-02
**Tomada por**: Ithalo Mendes (PM)
**Status**: APROVADA

---

## Contexto

Em 01/09/2026 o Check-in Diário (Hub de Benefícios, Tradicional) foi desativado em produção. O
desligamento não foi um simples ocultar-botão: o Railton implementou um **kill-switch real**
(`868kzep99`, finalizado em 02/09 às 11:57) porque a primeira tentativa — `CHECKIN_DIARIO_ENABLED`
via `runtimeConfig` do Nuxt — só escondia o botão na tela, deixando `POST /cadastro/checkin`
disparável por fora via Postman/curl. A versão final expõe e valida `FLAGS_WEB.isEnableCheckinDiario`
nos controllers do `ws-plataforma`, bloqueando de fato no servidor.

O motivo declarado no card era explícito: *"o Check-in Diário vai ser desativado temporariamente para
passar por uma reformulação"*. Poucas horas depois de o kill-switch entrar em produção, o PM
determinou que a feature já pode voltar ao ar.

**Não existe card de reformulação aberto no workspace** — busca por "reformulação Check-in" em
02/09/2026 não retornou nenhum item. Ou seja: o gatilho declarado do desligamento não foi executado
e a feature volta no estado em que saiu.

## Opções Consideradas

1. **Reativar já, sem a reformulação** — virar `FLAGS_WEB.isEnableCheckinDiario` para `true` em produção.
   - Prós: devolve a mecânica de retenção diária aos jogadores imediatamente; o kill-switch fica
     provado em produção e disponível para o próximo desligamento.
   - Contras: os problemas que já existiam antes do desligamento voltam a ficar visíveis — em
     particular `868kt5akq` (VL-14487, "CHECK-IN DIÁRIO NÃO ZERA VISUALMENTE", aberto, **sem
     responsável**) e o volume recorrente de chamados "CHECK-IN DIÁRIO - Não creditado" no chat
     🟦 03. Tradicional - CRM.

2. **Manter desligado até a reformulação existir como item** — usar a janela de indisponibilidade para
   corrigir a contagem visual e a falha de crédito antes de reexpor.
   - Prós: a feature volta sem reabrir o volume operacional no suporte.
   - Contras: prolonga a indisponibilidade de uma mecânica de retenção sem data definida, já que a
     reformulação não tem card, escopo nem responsável.

## Decisão

Optou-se pela **Opção 1 — reativar já**. Card criado em fast-track direto na lista Execução do folder
Delivery: Experiência do jogador, prioridade **urgente**, due date 02/09/2026, com **Railton Araujo
confirmado explicitamente pelo PM** como responsável (a atribuição não foi inferida pelo agente — ver
[2026-07-27-assignee-nunca-atribuido-sem-confirmacao.md](2026-07-27-assignee-nunca-atribuido-sem-confirmacao.md)).

O escopo é religar a flag em produção e validar que o botão, a tela e `POST /cadastro/checkin` voltam
a funcionar — sem tocar em mecânica, backend de bônus ou configuração da Smartico.

## Trade-offs Aceitos

- **O bug visual da contagem volta ao ar junto com a feature.** `868kt5akq` (VL-14487) segue aberto e
  sem responsável. Por instrução do PM, o ticket não foi vinculado ao card novo nem alterado.
- **A reformulação fica sem card, sem escopo e sem data.** A decisão de reativar não a cancela — apenas
  a desacopla do estado da feature em produção. Se ela não virar item, o desligamento de 01/09 terá
  sido custo sem contrapartida.
- **A validação de integridade da contagem durante o período desativado ficou como refinamento
  técnico**, não como pré-requisito da reativação. Se a contagem de dias de algum jogador foi corrompida
  pelo bloqueio de servidor, isso aparece depois de religar, não antes.
- **Urgência convivendo com refinamento em aberto**: o card nasceu urgente com due date hoje, mas com
  duas perguntas técnicas na seção de refinamento (ver Impacto). Pela regra do template ele não entra
  em sprint antes do refinamento — na prática, depende do Railton responder rápido.

## O que mudaria a decisão

- Confirmação de que a falha de crédito ("não creditado", recorrente no chat do CRM) tem causa raiz
  ativa em produção — nesse caso reativar reabre um problema financeiro, não só cosmético, e o
  desligamento deveria ser mantido.
- A reformulação ganhar card e data próxima — nesse caso pode valer manter desligado e emendar as duas
  coisas, em vez de religar e desligar de novo (o Indique & Ganhe já teve três mudanças de estado em
  menos de um mês; ver
  [2026-08-17-pausar-indique-e-ganhe-producao-falha-integracao-smartico.md](2026-08-17-pausar-indique-e-ganhe-producao-falha-integracao-smartico.md)).
- Evidência de que a flag exige novo deploy para religar — muda a estimativa e o caminho de execução.

## Impacto

- **Produto**: Check-in Diário, dentro do Hub de Benefícios / Banca de Benefícios (existe **apenas na
  Tradicional**, não na Bravo).
- **Técnico**: `FLAGS_WEB.isEnableCheckinDiario` (default `true`). Backend `ws-plataforma` —
  `RegionController.ts` e `CadastroController.ts` expõem e validam a flag. Frontend `plataforma-nuxt` —
  getter `getIsEnableCheckinDiario` em `login.js`, consumido por `pages/beneficios/index.vue`; a antiga
  `CHECKIN_DIARIO_ENABLED` foi removida por redundância. Duas perguntas ficaram como **"❓ Aberto para
  refinamento técnico"**: (a) a flag é configurável em runtime ou religar exige novo deploy/mudança de
  env; (b) a conferência da contagem de dias do período desativado é verificável pelo dev sozinho ou
  precisa de apoio de dados/backoffice.
- **Processo**: fast-track direto para Execução, pulando Backlog — mesmo padrão usado nos episódios de
  mitigação urgente do Hub de Benefícios. O card **não** foi vinculado ao Épico "Hub de Benefícios"
  (`868k9ccce`, já finalizado) — a rastreabilidade fica no vínculo com o kill-switch de origem.

## Achados não confirmados pelo PM

- **Evento Smartico do check-in ainda não está em produção.** `868kpwaer` ("Enviar à Smartico o evento
  de cada dia do Check-in diário, dias 1 a 7") está em **teste em alpha**. O critério de instrumentação
  do card fala em contabilizar o registro do check-in, sem prometer o envio à Smartico. Não vinculado.
- **Campo KPIs ficou vazio** no card. "Retenção" seria o candidato, mas não foi gravado por ser
  inferência do agente.

## Links

- Card da reativação: https://app.clickup.com/t/868m09nra
- Kill-switch de origem: https://app.clickup.com/t/868kzep99
- MR backend: https://git.verticalloto.com/gitlab-instance-22b28535/ws-plataforma/-/merge_requests/190
- MR frontend: https://git.verticalloto.com/kennedy/plataforma-nuxt/-/merge_requests/691
- Bug aberto sem responsável: https://app.clickup.com/t/868kt5akq (VL-14487)
- Evento Smartico em alpha: https://app.clickup.com/t/868kpwaer
