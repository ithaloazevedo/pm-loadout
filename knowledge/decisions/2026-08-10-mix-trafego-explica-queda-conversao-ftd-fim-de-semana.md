# Mix de origem de tráfego, não fricção de UX no cadastro, identificado como causa raiz dominante da queda de conversão a FTD no fim de semana — WhatsApp OTP rebaixado de prioridade até investigação de growth

**Data**: 2026-08-10
**Tomada por**: Ithalo Mendes (PM), com análise do agente-dados e agente-insights
**Status**: APROVADA (decisão de priorização; investigação de causa raiz do pico de tráfego segue aberta)

---

## Contexto

Um dashboard de análise do funil de cadastro → depósito (FTD) da Tradicional.bet.br, construído sobre `trad_prd` (skill `query-pam`), mostrou que entre sexta (07/08) e domingo (09/08/2026) o volume de pré-cadastros triplicou (589 → 1.339), mas a conversão a FTD por coorte (mesma etapa de maturação, dia 0) caiu de 29,5% para 12,5%. Hipóteses iniciais levantadas: fricção de SMS sob carga (retentativa de código disparou 41→227→303), gargalo de KYC, capacidade de API sob pico, e mix de tráfego.

Ao decompor o FTD por origem — cruzando `affiliates.clients` (afiliado) com `dwh.tbl_utm_events_processed` (UTM real, tem `entity_id` direto) — descobriu-se que o tráfego **sem nenhuma tag de marketing** ("sem UTM", não é erro de atribuição, confirmado que não há linha em `tbl_utm_events_processed` para essas entidades) saltou de 12,6% para 56,3% do volume diário, com conversão caindo de 63,9% (sábado) para 6,0% (domingo). O tráfego de afiliado, rastreável, caiu de forma bem mais suave (34,2% → 22,4%).

Nota técnica: uma primeira leitura via `affiliates.vw_clients_ftd` sugeriu erroneamente que tráfego direto convertia a 0% — essa view só cobre clientes de afiliado por construção (`JOIN` interno com `affiliates.clients`), o que é um artefato de escopo, não um dado real. Corrigido usando a flag `entities.json_statistics->>'ftdEntryId'`.

Também identificado, via Knowledge Graph e log de decisões: já existe uma tarefa pendente (`868kf991c`, bloqueada por chave de API da Meta) para habilitar WhatsApp como canal alternativo de validação de telefone — candidata a ganhar prioridade caso a hipótese de fricção de SMS se confirmasse como causa principal.

## Opções Consideradas

1. **Seguir direto para mudança de produto** — priorizar desbloqueio do WhatsApp OTP e/ou redesenho do fluxo de KYC/telefone, assumindo que a queda é fricção de UX.
   - Prós: ação mais rápida, já existe tarefa pronta no backlog.
   - Contras: os dados mostram que o mix de tráfego explica a maior parte da queda — investir em UX sem entender a origem do tráfego arrisca resolver o problema errado.

2. **Investigar a causa raiz do pico de tráfego sem tag antes de qualquer mudança de produto**, rebaixando a prioridade das ações de UX/infra até esse achado ser entendido com o time de growth/marketing.
   - Prós: evita investimento de produto/engenharia numa causa que provavelmente não é a dominante; direciona o esforço certo (mídia) para o problema certo.
   - Contras: atrasa qualquer ação imediata; a causa do pico de tráfego sem tag ainda não é conhecida (pode ser evento orgânico, compartilhamento, resultado de sorteio, notificação, ou tráfego de baixo valor) e depende de investigação fora do escopo do banco de dados do PAM.

## Decisão

Optou-se pela **Opção 2**. A tarefa `868kf991c` (WhatsApp OTP) e qualquer investimento em redesenho de KYC/telefone ficam **rebaixados de prioridade**, não cancelados — continuam válidos como frentes secundárias (a retentativa de SMS é real e tem custo). A ação imediata é levar o achado de mix de tráfego ao time de growth/marketing/CRM para entender a origem do pico de tráfego sem tag no domingo.

## Trade-offs Aceitos

- Isso adia uma ação de produto que já estava com tarefa pronta no backlog, em troca de evitar investir esforço de engenharia numa causa que os dados sugerem não ser a dominante.
- A causa raiz do próprio pico de tráfego sem tag continua desconhecida — esta decisão resolve a priorização, não o problema de origem em si.

## O que mudaria a decisão

- Se a investigação com growth/marketing concluir que o tráfego sem tag é, na verdade, tráfego pago mal instrumentado (falha de tracking, não falta de campanha) — nesse caso a ação deve ser técnica (corrigir instrumentação), não de mídia.
- Se o cruzamento de retentativa de SMS com o log de entrega do provedor mostrar uma falha técnica clara e independente do mix de tráfego, o desbloqueio do WhatsApp OTP volta a subir de prioridade.

## Impacto

- **Produto**: módulo Onboarding (Cadastro e acesso) — North Star "Conversão cadastro → 1º depósito" (KR já declarado no Knowledge Graph) não deve ser otimizada só pelo lado de UX enquanto a causa dominante for mix de tráfego.
- **Processo**: tarefa `868kf991c` mantém-se no backlog, mas sem urgência adicional motivada por este achado. Recomendado abrir uma frente de investigação com growth/marketing (fora do escopo do PM Loadout/ClickUp Vertical Tech) para entender a origem do tráfego sem tag.
- **Guardrails recomendados** (agente-insights): mix de motivo de rejeição KYC, retenção D+7/D+30 pós-FTD, custo de reenvio de SMS — a acompanhar junto da North Star antes de declarar qualquer ganho de conversão como real.

## Links

- Artifact do dashboard: funil de cadastro → FTD, visão macro/micro, origem de tráfego (sessão Claude Code, não versionado no repositório).
- Tarefa relacionada: `868kf991c` — WhatsApp como canal alternativo de validação de telefone.
- Decisão relacionada: [2026-07-23-whatsapp-numero-compartilhado-otp-boas-vindas.md](2026-07-23-whatsapp-numero-compartilhado-otp-boas-vindas.md)
- Schema: `.claude/skills/query-pam/SKILL.md` (atualizada com a pegadinha de `affiliates.vw_clients_ftd` e o uso de `dwh.tbl_utm_events_processed`)
