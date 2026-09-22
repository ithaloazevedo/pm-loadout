# Bloqueio da Banca de Benefícios fica restrito ao jogador sem FTD — bônus abuser sai do escopo e critério por depósito é mantido

**Data**: 2026-09-02
**Tomada por**: Ithalo Mendes (PM)
**Status**: APROVADA

---

## Contexto

O épico [868kparmw](https://app.clickup.com/t/9006076935/868kparmw) (Delivery: Plataforma, Tradicional) nasceu unificando **duas** condições de bloqueio da Banca de Benefícios — hub de missões e recompensas via Smartico, que existe apenas na Tradicional:

1. jogador que ainda não fez o primeiro depósito (FTD);
2. jogador marcado com a flag de bônus abuser.

A justificativa declarada para tratar os dois casos num item só era que "a solução de interface é a mesma": estado bloqueado com cadeado e mensagem explicando o que falta desbloquear. O próprio card carregava um comentário de 08/2026 registrando o gatilho da indefinição: *"Aguardando decisão da diretoria sobre o que fazer com o check-in diário p/ Bônus Abusers"*.

A decisão da diretoria saiu e foi alinhada com todas as áreas envolvidas: o jogador marcado como bônus abuser **não visualizará** a Banca de Benefícios — ocultação total, não estado bloqueado. Isso derruba a premissa que unificava os dois casos: a solução de interface deixou de ser a mesma.

## Opções Consideradas

1. **Reduzir o épico à condição sem FTD e tirar o bônus abuser** (escolhida)
   - Prós: cada comportamento fica no item cuja solução de interface ele de fato usa; o épico volta a ter uma única condição de entrada, testável sem ambiguidade de mensageria; encerra a pendência que aguardava a diretoria.
   - Contras: risco de a regra de ocultação ficar órfã se ninguém a carregar adiante — triado com o PM e descartado (ver Decisão).

2. **Manter os dois casos no épico, com comportamentos diferentes**
   - Prós: um único item cobrindo todas as condições de acesso à Banca.
   - Contras: descartada — "bloqueado com cadeado" e "não visualiza" são entregas distintas de interface, com critérios de aceite e instrumentação distintos. Unificar voltaria a esconder duas coisas atrás de um título.

3. **Trocar o gatilho de "primeiro depósito" para "ao menos uma aposta registrada"** (recomendação do `vigilancia-regulatoria`, não adotada)
   - Prós: alinharia o critério ao verbo da norma ("para a realização de aposta") e fecharia a lacuna do jogador que deposita e não aposta.
   - Contras: descartada pelo PM — o critério por depósito atende à intenção de negócio e a validação jurídica já foi feita (ver Trade-offs).

## Decisão

Escolhida a **Opção 1**. O épico passa a cobrir exclusivamente o jogador sem FTD, e o tratamento do bônus abuser sai como item de "Fora" com destino explícito.

Dois pontos foram triados com o PM na mesma sessão, antes de considerar a spec fechada:

- **Destino da regra do bônus abuser**: o PM confirmou que o tratamento **já está resolvido** — nenhum card precisa ser criado e a regra não fica pendente no backlog. Por isso o bullet de "Fora" declara o destino sem apontar card.
- **Critério de bloqueio**: **mantido no primeiro depósito (FTD)**. O PM informou que o critério e a mensagem da tela bloqueada já passaram pela validação do jurídico. A recomendação de trocar o gatilho para "aposta registrada" foi apresentada, avaliada e não adotada.

Consequências de campo: KPI passa de **Segurança** (setado quando o bônus abuser estava no escopo) para **Conversão**. A seção "Aberto para refinamento técnico" foi removida, porque a única pendência ali era a fonte da flag de bônus abuser.

## Trade-offs Aceitos

- **Exposição regulatória mapeada e aceita com validação jurídica prévia.** O `vigilancia-regulatoria` levantou, com texto literal de fonte oficial verificado em 02/09/2026, que a Portaria SPA/MF 1.231/2024, art. 42, §1º, I veda "condicionar a entrega de bônus, recompensas ou bens a aportes financeiros realizados pelos apostadores", e que o FAQ oficial da SPA (Questões Técnicas, Pergunta 78) exemplifica "bônus ou rodadas grátis mediante aporte financeiro anterior". Também apontou que a Lei 14.790/2023, art. 29, I e o art. 42, §1º, II falam em vantagem prévia "para a realização de **aposta**", não de depósito — e que a Portaria Interministerial MF/SECOM/MJSP nº 73, de 10/07/2026, art. 4º, VII, "c", passou a vedar chamadas para ação "inclusive com mecânicas promocionais". O PM avaliou o conjunto e manteve o critério por FTD, informando que a validação jurídica já ocorreu. A análise fica registrada aqui para não ser refeita a cada refinamento.
- **Nenhum critério de restrição de copy nem gate de aprovação jurídica entrou no card**, por decisão do PM (copy já validada). O critério de Mensageria segue informando que falta o primeiro depósito e o que desbloqueia.
- **A lacuna do jogador que deposita e não aposta permanece aberta por escolha**: com critério binário por depósito, quem faz PIX e não aposta passa a ver a Banca completa.
- **A instrumentação deixou de segmentar por condição** — com uma condição só, o evento de visualização do estado bloqueado mede apenas quantos jogadores encontram o bloqueio por falta de FTD.

## O que mudaria a decisão

- Publicação do **regulamento específico de bônus** que a SPA promete no FAQ 33 — nenhum foi publicado até 02/09/2026. Se ele tratar de gate de acesso condicionado a aporte, o critério por FTD precisa ser reavaliado.
- Manifestação nova do jurídico sobre o art. 42, §1º, I alcançar *gate de acesso* (a letra é "condicionar a **entrega**"; o épico condiciona acesso ao hub) — ponto que o `vigilancia-regulatoria` marcou como interpretação, não texto.
- Se aparecer volume material de jogadores que depositam e não apostam, a lacuna deixa de ser teórica e o gatilho por aposta volta à mesa.
- Se a regra de ocultação para bônus abuser não estiver de fato ativa, ela precisa de card próprio — o "Fora" deste épico não a implementa.

## Impacto

- **Produto**: Banca de Benefícios / SMARTICO, Tradicional apenas (não existe equivalente na Bravo). Estado bloqueado da Banca para jogador sem primeiro depósito.
- **Técnico**: integração Smartico (renderização headless dentro do PAM) e consulta ao estado de FTD do jogador. A pendência sobre a fonte da flag de bônus abuser deixou de existir neste item.
- **Processo**: reforça duas regras já estabelecidas — mudança de escopo pós-criação vai para o Log de Decisões e não reescreve o Contexto ([2026-07-28](2026-07-28-log-de-decisoes-separado-do-contexto.md)); e incerteza de compliance é triada com o PM antes de fechar a spec, nunca deixada na seção de refinamento técnico.

## Links

- Card: [868kparmw](https://app.clickup.com/t/9006076935/868kparmw) — "Exibir a Banca de Benefícios em estado bloqueado para jogador sem FTD"
- Decisão do mesmo dia, mesma Banca de Benefícios: [2026-09-02-reativar-check-in-diario-sem-reformulacao.md](2026-09-02-reativar-check-in-diario-sem-reformulacao.md)
- Precedente de item Smartico com pendência regulatória registrada sem bloquear a criação: [2026-07-30-bloqueio-campanhas-smartico-cadastro-login.md](2026-07-30-bloqueio-campanhas-smartico-cadastro-login.md)
- Precedente de vedação regulatória revogada em feature de benefícios: [2026-07-30-ocultar-indique-e-ganhe-vedacao-regulatoria.md](2026-07-30-ocultar-indique-e-ganhe-vedacao-regulatoria.md)
