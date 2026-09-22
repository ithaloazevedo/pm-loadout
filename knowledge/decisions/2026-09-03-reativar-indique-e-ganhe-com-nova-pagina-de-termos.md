# Reativar o "Indique & Ganhe" em produção com nova página de Termos e Condições dedicada

**Data**: 2026-09-03
**Tomada por**: Ithalo Mendes (PM)
**Status**: APROVADA

---

## Contexto

Esta é a quarta mudança de estado do Indique & Ganhe em pouco mais de um mês:

1. 30/07 — oculto por vedação regulatória (Art. 42 Portaria 1.231/2024). Revogado em seguida. Ver [2026-07-30-ocultar-indique-e-ganhe-vedacao-regulatoria.md](2026-07-30-ocultar-indique-e-ganhe-vedacao-regulatoria.md).
2. 06/08 — reativado após ajuste: recompensa só ao indicante. Ver [2026-08-06-reativacao-indique-e-ganhe-apos-adequacao.md](2026-08-06-reativacao-indique-e-ganhe-apos-adequacao.md).
3. 17/08 — pausado de novo, agora por falha técnica na integração PAM↔Smartico (bônus não pago, status travado em "pendente", suporte/CRM sem visibilidade). Condição de saída definida: validar em alpha que dados e automações de bônus estão corretos. Ver [2026-08-17-pausar-indique-e-ganhe-producao-falha-integracao-smartico.md](2026-08-17-pausar-indique-e-ganhe-producao-falha-integracao-smartico.md).
4. 03/09 (esta decisão) — reativação, com uma peça nova: uma página de Termos e Condições dedicada ao Indique & Ganhe (antes as regras apareciam só num link/modal "Veja as regras" sem página própria).

O Orquestrador levantou duas pendências antes de aceitar a reativação como pronta para virar card, dado o histórico de idas e vindas: (a) a condição de saída técnica de 17/08 tinha sido cumprida de fato, já que o card de causa raiz (868kr2mtc) foi fechado no mesmo deploy que só pausou o botão, sem evidência registrada de correção; (b) o novo texto de T&C (que mantém a condicionante de aporte de R$30 do indicado para liberar a recompensa do indicador) já era a versão final aprovada por compliance, já que a decisão de 06/08 registrava essa condicionante remanescente como "leitura assumida, não parecer registrado".

## Opções Consideradas

1. **Reativar direto, como pedido** — sem confirmar as duas pendências.
   - Prós: mais rápido.
   - Contras: risco de reproduzir o incidente de 17/08 (prejuízo financeiro, retrabalho manual de suporte) e/ou publicar T&C sem aval jurídico final.

2. **Confirmar as duas pendências com o PM antes de estruturar o card** — pausar a spec até resposta explícita.
   - Prós: evita repetir o padrão de 3 reversões em um mês por decisão apressada.
   - Contras: pequeno atrito adicional na conversa.

## Decisão

Optou-se pela **Opção 2**. O PM confirmou explicitamente, nesta conversa: (1) a validação em alpha da integração Smartico já foi concluída com sucesso (dados mapeados, automações de bônus corretas, visibilidade de suporte/CRM confirmada); (2) o texto do Google Doc de T&C já é a versão final aprovada por compliance/jurídico (Vitor Vianna/Isaac Ribeiro). Com as duas pendências resolvidas, a spec seguiu para o `agente-delivery`.

Escopo do card criado ([868m11wy2](https://app.clickup.com/t/868m11wy2)):
- Nova página de T&C do Indique & Ganhe, no padrão da página de T&C já existente no site, com o conteúdo do Google Doc.
- Botão "Veja as regras" passa a redirecionar para essa nova página.
- Reversão da flag `INDIQUE_GANHE_BUTTON_ENABLED` em produção — Melk (dev responsável) não tem acesso a produção e deve solicitar a mudança a Rayan Teixeira Aguiar (Tech Lead Plataforma).

## Trade-offs Aceitos

- A confirmação das duas pendências (validação Smartico e aprovação do T&C) veio da palavra do PM nesta conversa, não de um artefato auditável (ex.: link do teste em alpha, parecer jurídico assinado) — se a informação estiver desatualizada ou imprecisa, o risco do incidente de 17/08 se repete.
- A condicionante de aporte financeiro do indicado (R$30 em apostas) permanece no desenho, carregando o mesmo risco de leitura regulatória que a decisão de 06/08 já havia sinalizado como não totalmente pacificado.

## O que mudaria a decisão

- Evidência de que a validação em alpha da integração Smartico não foi de fato concluída (ex.: bônus continuando a falhar após reativação).
- Nova manifestação de compliance/jurídico revisando a leitura sobre a condicionante de aporte de R$30 do indicado.

## Impacto

- **Produto**: Indique & Ganhe (Hub de Benefícios / Banca de Benefícios). Nova página de T&C dedicada; botão de indicação reabilitado em produção.
- **Técnico**: front (nova página + redirect do botão) e reversão de env var em produção (sem alteração de mecânica/backend/Smartico nesta rodada).
- **Processo**: card criado direto em Execução, mesmo padrão de fast-track dos 3 episódios anteriores desta feature. Vinculado à feature original (868kevfgr) e ao card da pausa técnica (868kt2hdd) para preservar o histórico.

## Links

- Card no ClickUp: [868m11wy2](https://app.clickup.com/t/868m11wy2) — Reativar o Indique e Ganhe em produção após validação da integração com a Smartico
- Feature original: [868kevfgr](https://app.clickup.com/t/868kevfgr) — Indique e Ganhe
- Card da pausa técnica (revertido por esta decisão): [868kt2hdd](https://app.clickup.com/t/868kt2hdd)
- Causa raiz reportada (fechada junto com o deploy da pausa, sem confirmação registrada de correção): [868kr2mtc](https://app.clickup.com/t/868kr2mtc)
- Documento de T&C (fonte do conteúdo da nova página): https://docs.google.com/document/d/1NFuJihv8xhG-7xHLsJ3nUAN-txcPA7Kb/edit#heading=h.gco319ubcayw
- Episódios anteriores desta feature: [2026-07-30-ocultar-indique-e-ganhe-vedacao-regulatoria.md](2026-07-30-ocultar-indique-e-ganhe-vedacao-regulatoria.md), [2026-08-06-reativacao-indique-e-ganhe-apos-adequacao.md](2026-08-06-reativacao-indique-e-ganhe-apos-adequacao.md), [2026-08-17-pausar-indique-e-ganhe-producao-falha-integracao-smartico.md](2026-08-17-pausar-indique-e-ganhe-producao-falha-integracao-smartico.md)
