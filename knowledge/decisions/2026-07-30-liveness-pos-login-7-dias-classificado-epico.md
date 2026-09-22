# Revalidação facial (liveness) obrigatória no login após 7 dias sem acesso, classificada como Épico apesar do prazo regulatório de 1 dia

**Data**: 2026-07-30
**Tomada por**: Ithalo Mendes (PM), a pedido de Isaac Ribeiro (Compliance)
**Status**: APROVADA

---

## Contexto

Isaac Ribeiro (Compliance) solicitou, no chat do ClickUp (canal `8ccvn07-58431`, thread [80110053393390](https://app.clickup.com/9006076935/chat/r/8ccvn07-58431/t/80110053393390)), a criação da tarefa de liveness (revalidação facial) no login para usuários com mais de 7 dias sem login, classificando-a como **regulatória** e pedindo para "matar até amanhã" (31/07/2026).

Ao especificar o item, era preciso decidir se o escopo cabe como Tarefa (uma sprint ou menos) ou Épico (múltiplas sprints), já que o prazo pedido (1 dia) é incompatível com o escopo real do que a regra exige.

## Opções Consideradas

1. **Classificar como Tarefa**, para se alinhar ao prazo pedido por Compliance.
   - Prós: sinaliza urgência de forma consistente com o pedido.
   - Contras: sub-representa o escopo real — o item exige um gate novo no fluxo de acesso (cálculo da janela de 7 dias, novos estados de resultado do liveness, tratamento de reprovado/pendente, fallback de falha de API), o que não cabe em uma sprint.

2. **Classificar como Épico**, refletindo o escopo técnico real, e tratar o prazo de 1 dia como um ponto de tensão a validar com Compliance (ex.: via uma versão mínima faseada).
   - Prós: escopo do card reflete a realidade técnica; evita compromisso de prazo que o time não consegue cumprir.
   - Contras: o prazo "até amanhã" citado por Isaac fica sem resposta imediata dentro do card — precisa de alinhamento explícito sobre o que é viável nesse prazo (ex.: liberar um recorte mínimo).

## Decisão

Optou-se pela **Opção 2 — classificar como Épico**, priorizando um escopo tecnicamente honesto sobre a aparência de velocidade. O card foi marcado com prioridade urgente e due date 31/07/2026 (o prazo pedido), mas com uma nota explícita para validar com Isaac se cabe uma versão mínima faseada dentro desse prazo.

## Trade-offs Aceitos

- Risco de o prazo regulatório de 1 dia não ser cumprido integralmente, já que o escopo completo (Épico) dificilmente fecha em 24h.
- A decisão não resolve sozinha a tensão prazo × escopo — fica como próxima conversa com Isaac Ribeiro definir o que é aceitável como entrega mínima nesse prazo.

## O que mudaria a decisão

- Compliance aceitar uma entrega faseada (ex.: liveness aplicado só a um subconjunto de usuários ou de forma mais simples inicialmente), o que poderia justificar destacar uma Tarefa/Correção menor dentro do Épico para cumprir o prazo de 31/07.
- Confirmação de que o fornecedor de liveness já integrado (Serasa, usado no onboarding/KYC) suporta reuso direto no fluxo de login sem trabalho adicional relevante — o que reduziria o escopo e poderia rebaixar a classificação.

## Impacto

- **Produto**: fluxo de login/acesso (Cadastro e acesso), módulo KYC.
- **Técnico**: integração com Serasa (liveness/KYC); novos estados de sessão/acesso condicionados ao resultado da revalidação.
- **Processo**: card criado sem assignee e sem Objetivo/OKR vinculado (nenhum OKR de compliance existente cobre requisitos regulatórios pontuais como este) — pendências a resolver no refinamento.

## Links

- Card no ClickUp: [868kj1d2h](https://app.clickup.com/t/868kj1d2h) — Revalidação facial (liveness) pós-login após 7 dias sem login
- Discussão de origem: https://app.clickup.com/9006076935/chat/r/8ccvn07-58431/t/80110053393390
