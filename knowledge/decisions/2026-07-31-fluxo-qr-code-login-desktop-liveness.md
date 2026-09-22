# Fluxo de revalidação facial no login desktop via handoff por QR Code, com vínculo de sessão obrigatório

**Data**: 2026-07-31
**Tomada por**: Ithalo Mendes (PM)
**Status**: APROVADA

---

## Contexto

O Épico [868kj1d2h](https://app.clickup.com/t/868kj1d2h) — revalidação facial (liveness) obrigatória no login após 7 dias sem acesso (ver [[2026-07-30-liveness-pos-login-7-dias-classificado-epico]]) — foi especificado sem detalhar como a captura facial aconteceria no **desktop**, onde o fluxo web não tem câmera integrada. O protótipo em Figma (https://www.figma.com/design/hDhnEAFPFYSnsoJQhgzzda/PAM---Login?node-id=5947-1060) finalizou essa lacuna: CPF → Senha → tela informativa sobre a revalidação → QR Code para validação via celular.

Login por QR Code é um padrão com risco de segurança conhecido (sequestro de sessão via QR — ex.: um atacante captura o QR legítimo e o exibe para a vítima escanear, assumindo a sessão dela). Era preciso decidir se o card assumia esse padrão sem mitigação adicional ou se acrescentava critérios de segurança específicos antes de ir para refinamento com a squad.

## Opções Consideradas

1. **Especificar o handoff via QR Code sem critérios de segurança adicionais**, tratando desktop e mobile só como uma diferença de responsividade.
   - Prós: menor escopo, mais rápido de especificar dado o prazo apertado.
   - Contras: deixa uma lacuna de segurança conhecida (sequestro de sessão/phishing via QR) sem tratamento em um fluxo de compliance regulatório — risco alto para um gate que existe justamente por exigência de Compliance.

2. **Especificar o handoff com critérios de segurança explícitos** — QR vinculado univocamente à sessão de desktop, expiração curta, uso único, e um código curto de confirmação cruzada exibido no desktop e conferido no celular antes da captura.
   - Prós: fecha a lacuna de segurança conhecida; escopo desktop passa a ser tratado como fluxo distinto do mobile, não uma variação responsiva.
   - Contras: adiciona complexidade técnica (estado de sessão servidor-a-servidor entre desktop e celular) não trivial, tensionando ainda mais o prazo de 31/07 já apertado (ver decisão anterior).

## Decisão

Optou-se pela **Opção 2**. Um gate de compliance não deveria introduzir uma superfície de ataque nova (login por QR sem vínculo de sessão é um padrão de phishing/sequestro conhecido); a segurança do mecanismo de revalidação é parte do escopo, não um adicional opcional. O Épico foi atualizado com: distinção explícita de fluxo mobile (captura nativa) vs. desktop (handoff por QR Code), novo grupo de Critérios de Aceite "Handoff via QR Code (desktop)", e correção do critério de qualidade que tratava isso como responsividade.

## Trade-offs Aceitos

- A complexidade técnica do vínculo de sessão desktop↔celular não estava contemplada quando o prazo de 31/07 foi fixado — o card ficou com uma seção **❓ Aberto para refinamento** sinalizando a necessidade de validar com Isaac Ribeiro (Compliance) se cabe entrega faseada dentro do prazo.
- O mecanismo de fallback para usuário sem celular disponível não foi definido nesta rodada — ficou como item aberto, não pode travar o acesso indefinidamente por regra geral do card.
- Não foi confirmado se o fluxo mobile é de fato captura nativa direta (inferência do PM) — a confirmar contra o protótipo finalizado.

## O que mudaria a decisão

- Confirmação de que o fornecedor (Serasa/Legitimuz) já entrega um mecanismo de vínculo de sessão pronto para reuso, o que reduziria o esforço de construir isso do zero e aliviaria a tensão de prazo.
- Isaac Ribeiro (Compliance) aceitar uma entrega faseada (ex.: mobile primeiro, desktop com QR Code em onda seguinte) — mudaria o que precisa estar pronto até 31/07 vs. depois.

## Impacto

- **Produto**: fluxo de login/acesso (Cadastro e acesso), especificamente o caminho desktop.
- **Técnico**: novo estado de sessão vinculando desktop↔celular durante o handoff; expiração e uso único do QR Code.
- **Processo**: card ganhou seções 📜 Log de Decisões e ❓ Aberto para refinamento (antes ausentes); regra do template impede entrar em sprint com refinamento pendente.

## Links

- Card no ClickUp: [868kj1d2h](https://app.clickup.com/t/868kj1d2h) — Exigir revalidação facial (liveness) no login após 7 dias sem acesso
- Protótipo: https://www.figma.com/design/hDhnEAFPFYSnsoJQhgzzda/PAM---Login?node-id=5947-1060&t=dyitKuPzqXMcpH0m-11
- Decisão anterior sobre o mesmo card: [[2026-07-30-liveness-pos-login-7-dias-classificado-epico]]
