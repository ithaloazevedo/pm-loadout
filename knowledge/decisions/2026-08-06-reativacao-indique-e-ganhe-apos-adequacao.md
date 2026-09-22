# Reativar o "Indique & Ganhe" após adequação regulatória — só o indicante recebe

**Data**: 2026-08-06
**Tomada por**: Vitor Vianna (Compliance/Solicitante), alinhado com Isaac Ribeiro
**Status**: APROVADA

---

## Contexto

Em 30/07 o Indique & Ganhe foi ocultado/desativado por vedação regulatória: o desenho condicionava a entrega de bônus a aporte financeiro do apostador indicado (Art. 42 da Portaria 1.231/2024), caracterizando uso de bônus para aquisição de novos usuários — ver [2026-07-30-ocultar-indique-e-ganhe-vedacao-regulatoria.md](2026-07-30-ocultar-indique-e-ganhe-vedacao-regulatoria.md).

O Vitor reabriu o tema no chat do ClickUp: alinhou com o Isaac que o programa **pode ser reativado**, desde que revisado para caber nas normativas. A revisão combinada: **remover a recompensa entregue ao amigo indicado** (os "20 giros de bônus no Fortune Tiger") — assim apenas o indicante recebe bônus de saldo real, o que, na leitura deles, deixa de caracterizar bônus de aquisição do novo apostador.

## Opções Consideradas

1. **Manter desativado** — seguir com o programa oculto por precaução regulatória.
   - Prós: risco zero sob a leitura de 30/07.
   - Contras: perda contínua do canal de aquisição por indicação.

2. **Reativar removendo apenas a recompensa ao indicado** — republicar o programa dando bônus só ao indicante.
   - Prós: recupera o canal de aquisição; mudança pequena (ajuste, não reconstrução); endereça o ponto que o jurídico levantou (bônus ao novo apostador).
   - Contras: o bônus do indicante segue condicionado ao aporte do indicado — a condicionante de aporte não some por completo.

## Decisão

Optou-se pela **Opção 2 — reativar removendo a recompensa ao indicado**. Alinhamento de compliance feito por Vitor + Isaac. Escopo operacional:

- **CRM/Smartico**: remove a entrega dos 20 giros ao indicado na mecânica (fora do card de front).
- **Produto/Plataforma** (card [868kmj13a]): remove da página a linha "Seu amigo ganha: 20 giros no Fortune Tiger", troca o headline "Indique um amigo e ganhem juntos!" pelo aprovado **"Convide amigos e ganhe recompensas"**, e republica a página no site.

O novo headline foi validado pelo PM (Ithalo) porque o antigo sugeria que ambos ganhavam — incompatível com a versão só-indicante.

## Trade-offs Aceitos

- O bônus do indicante permanece condicionado ao aporte do amigo indicado. A leitura que sustenta a reativação é que a vedação do Art. 42 mira o bônus de **aquisição do novo apostador** (o indicado), não a recompensa ao usuário já existente que indica.

## O que mudaria a decisão

- Confirmação explícita do Isaac/jurídico de que a condicionante de aporte remanescente (bônus ao indicante quando o indicado aporta) também está fora do Art. 42 — hoje é uma leitura assumida, não um parecer registrado.
- Nova interpretação da Portaria 1.231/2024 ou nota técnica que volte a enquadrar o desenho como vedado.

## Impacto

- **Produto**: Indique & Ganhe (Hub de Benefícios). Página reativada; recompensa exclusiva ao indicante.
- **Técnico**: front da página (remoção de linha + headline + republicação); mecânica na Smartico ajustada pelo CRM.
- **Processo**: reverte a decisão de 30/07; validação de todos os comportamentos do fluxo e documentação da feature/regras de negócio entram como critérios de aceite do card.

## Links

- Card no ClickUp: [868kmj13a](https://app.clickup.com/t/868kmj13a) — Atualização da Página do Indique e Ganhe (reativação)
- Feature original: [868kevfgr](https://app.clickup.com/t/868kevfgr) — Indique e Ganhe
- Card da desativação revertida: [868kj1d89](https://app.clickup.com/t/868kj1d89) — Ocultar o Indique & Ganhe
- Decisão revertida: [2026-07-30-ocultar-indique-e-ganhe-vedacao-regulatoria.md](2026-07-30-ocultar-indique-e-ganhe-vedacao-regulatoria.md)
- Origem no chat: alinhamento Vitor/Isaac no canal do ClickUp (thread "Indique e ganhe")
