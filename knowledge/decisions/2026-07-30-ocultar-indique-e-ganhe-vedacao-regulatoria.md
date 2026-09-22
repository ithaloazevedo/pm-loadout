# Ocultar/desativar o programa "Indique & Ganhe" por vedação regulatória

**Data**: 2026-07-30
**Tomada por**: Time de Compliance (Vitor Vianna, com embasamento jurídico trazido por membro do time jurídico) — validação final pendente de Isaac Ribeiro
**Status**: REVOGADA

> **Revogada em 2026-08-06.** Vitor e Isaac alinharam reativar o programa após adequação (remover a recompensa ao indicado; só o indicante recebe). Ver [2026-08-06-reativacao-indique-e-ganhe-apos-adequacao.md](2026-08-06-reativacao-indique-e-ganhe-apos-adequacao.md).

---

## Contexto

O programa Indique & Ganhe concede R$30 de bônus ao usuário indicador, condicionado a um aporte financeiro (depósito/aposta) do novo apostador indicado. Em discussão aberta no chat do ClickUp (canal `8ccvn07-67091`, post [80110053332994](https://app.clickup.com/9006076935/chat/r/8ccvn07-67091/p/80110053332994)), o time jurídico trouxe embasamento de que esse desenho viola a regulação vigente das apostas de quota fixa.

## Opções Consideradas

1. **Manter o Indique & Ganhe como está** — não alterar o programa.
   - Prós: nenhuma perda de canal de aquisição.
   - Contras: exposição regulatória direta — o desenho atual condiciona bônus a aporte financeiro, o que a norma veda explicitamente.

2. **Ocultar/desativar o Indique & Ganhe** — remover a feature da experiência do jogador.
   - Prós: elimina o risco regulatório identificado; simples de executar (ajuste, não construção).
   - Contras: perda do canal de aquisição via indicação; possível necessidade de redesenhar o programa sem a condicionante de aporte no futuro.

## Decisão

Optou-se pela **Opção 2 — ocultar/desativar o Indique & Ganhe**. O principal fator foi o enquadramento jurídico trazido na discussão:

- Art. 42 da Portaria 1.231/2024: "é vedado condicionar a entrega de bônus, recompensas ou bens a aportes financeiros realizados pelos apostadores".
- Nota Técnica SEI nº 229/2025/MF, que reforça o mesmo entendimento e caracteriza esse tipo de bonificação como "vantagem prévia" vedada quando usada para atrair novos apostadores.

O programa atual condiciona o bônus de R$30 tanto à indicação de um novo apostador quanto ao aporte desse indicado — dupla incidência da vedação, na leitura do time jurídico.

## Trade-offs Aceitos

- Perda do Indique & Ganhe como canal de aquisição enquanto não houver um redesenho compliant (ex.: bônus não condicionado a aporte financeiro).
- Decisão foi tratada como tecnicamente fechada no chat, mas a **validação final de Isaac Ribeiro ainda não está confirmada** nas mensagens registradas — por isso o status aqui é PENDENTE, não APROVADA.

## O que mudaria a decisão

- Isaac Ribeiro (ou outra instância de compliance/jurídico) discordar do enquadramento e apontar uma leitura alternativa da Portaria 1.231/2024 ou da Nota Técnica SEI nº 229/2025/MF.
- Uma versão redesenhada do programa que remova a condicionante de aporte financeiro do indicado, tornando-o compliant sem precisar desativar.

## Impacto

- **Produto**: Indique & Ganhe, parte do Hub de Benefícios (integração Smartico).
- **Técnico**: ocultação da feature na experiência do jogador (front); sem alteração de backend/integração além disso.
- **Processo**: card de execução criado no ClickUp com bloqueio explícito até a validação final de Isaac Ribeiro.

## Links

- Card no ClickUp: [868kj1d89](https://app.clickup.com/t/868kj1d89) — Ocultar o Indique & Ganhe
- Tarefa/feature original vinculada: [868kevfgr](https://app.clickup.com/t/868kevfgr) — Indique e Ganhe
- Discussão de origem: https://app.clickup.com/9006076935/chat/r/8ccvn07-67091/p/80110053332994
