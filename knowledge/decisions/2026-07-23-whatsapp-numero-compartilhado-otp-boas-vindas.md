# Mesmo número/BM do WhatsApp Business API será compartilhado entre autenticação (OTP) e boas-vindas

**Data**: 2026-07-23
**Tomada por**: Ithalo Mendes (PM)
**Status**: APROVADA

---

## Contexto

O PM recebeu credenciais de uma BM do WhatsApp Business API — "Tradicional Contigência", número "Tradicional Autenticação" — e pediu a criação de uma nova entrega: mensagem automatizada de boas-vindas via WhatsApp após a finalização do cadastro.

O nome do número ("Autenticação") indica que essa credencial foi originalmente provisionada para a tarefa `868kf991c` — "WhatsApp como canal alternativo de validação de telefone" —, já registrada como pendente de chave de API do Meta na decisão [2026-07-23-visualizacao-otp-backoffice.md](2026-07-23-visualizacao-otp-backoffice.md).

Antes de especificar a nova entrega, o Orquestrador sinalizou que a Meta recomenda segregar números por categoria de mensagem (autenticação vs. marketing/notificação/utilidade), porque o uso misto pode afetar o *quality rating* do número — crítico no caso de um número também usado para OTP de login/cadastro.

## Opções Consideradas

1. **Manter o número exclusivo para autenticação** — a mensagem de boas-vindas usaria uma BM/número novo e dedicado.
   - Prós: segue a prática recomendada pela Meta; isola o risco de rating do canal crítico de autenticação.
   - Contras: exige provisionar e aprovar uma segunda BM/número; mais lento para colocar a entrega no ar.

2. **Reaproveitar o mesmo número/BM para os dois casos de uso** — OTP de validação de telefone e mensagem de boas-vindas compartilham a mesma integração/credenciais.
   - Prós: reaproveita infraestrutura e credenciais já obtidas; entrega mais rápida.
   - Contras: mistura categorias de mensagem no mesmo número, com risco de afetar o quality rating do canal usado para autenticação.

## Decisão

Optou-se pela **Opção 2 — reaproveitar o mesmo número/BM para os dois casos de uso**, priorizando velocidade de entrega e reaproveitamento de infraestrutura já provisionada sobre a redução de risco de rating recomendada pela Meta.

## Trade-offs Aceitos

- Risco de o quality rating do número cair por causa do volume/comportamento das mensagens de boas-vindas, podendo impactar a confiabilidade do canal de autenticação (OTP) que depende do mesmo número.
- Nenhum controle adicional de monitoramento de rating foi definido nesta decisão — fica como item de acompanhamento técnico, não como bloqueio.

## O que mudaria a decisão

- Queda mensurável no quality rating do número ou aumento de falhas/atrasos na entrega de OTP após o início do envio de boas-vindas.
- Orientação da Meta ou incidente que exija segregação de números por categoria.

## Impacto

- **Produto**: módulo Onboarding (Cadastro e acesso) — duas entregas (`868kf991c` e a nova tarefa de boas-vindas) passam a compartilhar a mesma integração/BM do WhatsApp Business API.
- **Técnico**: uma única integração de WhatsApp Business Cloud API atende dois casos de uso; sem segregação de números por categoria de mensagem.
- **Processo**: as duas tarefas foram vinculadas (linked task) no ClickUp, e um comentário de decisão foi postado em ambas para que qualquer squad que assuma uma delas veja o contexto compartilhado.

## Links

- Card no ClickUp: [868kfh183](https://app.clickup.com/t/868kfh183) — Habilitar o envio de boas-vindas via WhatsApp após a conclusão do cadastro
- Tarefa relacionada: `868kf991c` — Habilitar a validação de telefone via WhatsApp
- Decisão relacionada: [2026-07-23-visualizacao-otp-backoffice.md](2026-07-23-visualizacao-otp-backoffice.md)
