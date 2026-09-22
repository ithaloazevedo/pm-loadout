# Suporte pode visualizar o valor do OTP (telefone e e-mail) no backoffice

**Data**: 2026-07-23
**Tomada por**: Ithalo Mendes (PM)
**Status**: APROVADA

---

## Contexto

Incidente de 22/07/2026 (origem `868kf1mq9`) expôs que a verificação de telefone no cadastro tem alto abandono: bug no `sendValidationCode` (corrigido) somado à taxa de entrega do Infobip travada em ~82%. Duas correções estruturais já estão especificadas:

- `868kf98yh` — troca de provedor de SMS (Infobip → Pushfy) com fallback automático para WhatsApp
- `868kf991c` — WhatsApp como canal alternativo de validação de telefone

Ambas levam tempo até irem ao ar (Pushfy pendente de definição de contrato; WhatsApp pendente de chave de API do Meta). Para dar autonomia ao time de suporte enquanto isso — e como capacidade permanente de atendimento — o PM propôs uma feature no backoffice para visualizar o OTP (telefone e e-mail) e comunicar manualmente ao usuário.

Antes de especificar, o Orquestrador sinalizou um risco de segurança: expor o valor de um segredo de autenticação (OTP) a um operador humano é um vetor conhecido de account takeover (operador malicioso/comprometido, ou engenharia social contra o suporte) — especialmente sensível numa plataforma de apostas regulada (Lei 14.790, SIGAP, LGPD).

## Opções Consideradas

1. **Reenviar/gerar novo código sem expor o valor** — suporte aciona reenvio (SMS/WhatsApp/e-mail); o sistema entrega direto ao usuário; o operador nunca vê o valor.
   - Prós: elimina o vetor de exposição de segredo de autenticação; menor superfície de auditoria/compliance.
   - Contras: não cobre o caso de o usuário não ter acesso a nenhum canal digital no momento (ex.: atendimento por telefone onde o suporte precisaria ditar o código).

2. **Visualizar o valor, com controles** — suporte vê o OTP na tela, mitigado por log de auditoria, permissão restrita e expiração padrão.
   - Prós: cobre qualquer canal de atendimento (inclusive voz); resolve o problema imediato de autonomia do suporte.
   - Contras: mantém a exposição do segredo a um humano; exige controles de segurança não-triviais para não virar achado de auditoria.

## Decisão

Optou-se pela **Opção 2 — suporte poderá visualizar o valor do OTP**, priorizando cobertura de todos os canais de atendimento (incluindo voz) sobre a redução de superfície de risco da Opção 1.

## Trade-offs Aceitos

- Exposição do segredo de autenticação a operadores humanos é aceita conscientemente, não é ausência de análise.
- A decisão condiciona a feature a controles mínimos não-negociáveis, definidos nesta sessão:
  - Log de auditoria por visualização (quem, quando, qual conta)
  - Permissão restrita a papel/grupo específico de suporte (não todo usuário de backoffice)
  - Sem extensão de validade do OTP só por estar sendo exibido (mesma janela de expiração do fluxo normal)
  - Sem busca livre em massa — visualização vinculada a um atendimento/ticket ativo, não lookup aberto por telefone/e-mail

## O que mudaria a decisão

- Um incidente de fraude/account takeover via suporte tornaria a Opção 1 (reenvio sem exposição) obrigatória.
- Uma auditoria de segurança ou parecer jurídico/LGPD que classifique a exposição como não-conforme.

## Impacto

- **Produto**: nova feature no Backoffice (módulo "BackOffice de Operador"), squad Operação e afiliados — superfície nova, não uma extensão de tela existente.
- **Técnico**: exige acesso do backoffice ao valor do OTP armazenado/gerado pelo PAM, mais camada de permissão e auditoria não existente hoje nesse fluxo.
- **Processo**: recomenda-se checagem de segurança/governança (`agente-governanca`) antes de ir para desenvolvimento, dado o desvio da prática padrão de mercado.

## Links

- Card no ClickUp: a criar (relacionado a `868kf98yh` e `868kf991c`)
- Tarefas relacionadas: `868kf98yh`, `868kf991c`, origem `868kf1mq9`
