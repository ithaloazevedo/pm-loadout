# Exibir nacionalidade em "Meu perfil" reaproveita dado de KYC já coletado, sem desvio de finalidade LGPD — mesmo padrão do precedente do campo "sexo"

**Data**: 2026-09-08
**Tomada por**: Ithalo Mendes (via Orquestrador + agentes agente-spec, agente-delivery)
**Status**: APROVADA

---

## Contexto

Ithalo pediu para ajustar o card 868m2u5vg (criado por ele mesmo horas antes, só com título e 2 prints anexados, sem descrição) para inserir um campo "Nacionalidade" na seção "Informações pessoais" de "Meu perfil", com o retorno vindo do que Serasa ou Legitimuz entregam.

O Orquestrador buscou o card antes de especificar e encontrou uma discrepância de premissa: não existia nenhum outro card com seção "Informações pessoais" e campos por provedor já documentados para copiar — o próprio card 868m2u5vg era o alvo, mas estava vazio de texto. O padrão a replicar era só visual (prints da tela "Minha Conta": rótulo em negrito + valor abaixo). Os prints, enviados em duas rodadas (primeiro incompletos, depois completos), revelaram a ordem real dos campos existentes: Nome, Data de Nascimento, E-mail, CPF, Telefone, Data de última atualização — seguidos de uma seção separada "Endereço" com campo "País".

Verificação no Knowledge Graph encontrou um precedente direto: o campo "sexo" (card 868ktk86b, "Corrigir o campo sexo do cadastro do jogador com o CPF check da Legitimuz", fechado 20/08/2026) veio do CPF check da Legitimuz — dado da Receita Federal —, enquanto a Serasa é usada para KYC de verificação de documento/biometria (`knowledge/domains/engenharia.md`). Nacionalidade é o mesmo tipo de dado civil de identificação, plausivelmente da mesma fonte, mas isso é confirmação técnica, não decisão de produto.

## Opções Consideradas

**Editabilidade do campo:**
1. Editável pelo jogador (como E-mail/Telefone) — descartada.
2. **Não editável, mesmo padrão do CPF** (dado de verificação externa) — escolhida, confirmada por Ithalo via pergunta direta.

**Comportamento quando o provedor não retorna o dado:**
1. Exibir campo vazio ou "-" — descartada, gera "buraco" visual.
2. **Ocultar o campo até haver retorno** — escolhida.

**Necessidade de revisão regulatória:**
1. Tratar como desvio de finalidade LGPD (mesma preocupação do caso "sexo") — descartada: ali o dado ia para CRM/BI, uso diferente do KYC original; aqui é o próprio titular vendo seu dado na tela do seu próprio perfil, mesma finalidade da coleta original.
2. **Seguir sem acionar `vigilancia-regulatoria`** — escolhida, baixo risco.

## Decisão

1. Campo "Nacionalidade" inserido na seção "Informações pessoais", mesmo padrão visual dos demais campos, posicionado logo após "Data de Nascimento" e antes de "E-mail" (agrupa dados de identificação civil antes dos dados de contato/documento editáveis) — recomendação de UX, ajustável pelo squad Plataforma conforme Figma.
2. Valor exibido por extenso em português (nunca código bruto do provedor).
3. Campo não editável pelo jogador.
4. Campo oculto (não vazio, não "-") quando o provedor não retorna o dado.
5. Módulo do PAM: **Conta do jogador** (mesmo módulo do precedente 868ktk86b).
6. Sem assignee — deixado em aberto a pedido do PM.
7. Qual provedor exatamente (Serasa ou Legitimuz) retorna o campo, formato bruto do payload, e necessidade de backfill/reconsulta para contas já verificadas ficaram como **"Aberto para refinamento técnico"** no próprio card — não bloqueiam a especificação.

## Trade-offs Aceitos

- A fonte exata do dado (Serasa vs. Legitimuz) não foi confirmada antes de especificar — é aposta fundamentada no precedente do campo "sexo", não certeza. Se a engenharia confirmar fonte diferente da esperada, os critérios de aceite sobre formato/mapeamento podem precisar de ajuste.
- Card vive no folder "Sprints" (lista "Sprint 1 (7/9-20/9)"), estrutura ainda não mapeada em `clickup-config.md` — gap de documentação sinalizado, não resolvido nesta missão.
- Campo "Empresa" (Tradicional/Bravo/Vertical) ficou vazio por falta de sinal de que o item é específico de uma casa — mesmo padrão do precedente.

## O que mudaria a decisão

- Se a engenharia confirmar que nenhum dos dois provedores (Serasa/Legitimuz) retorna nacionalidade estruturada, seria necessária nova integração — fora do escopo assumido aqui de "reuso, sem integração nova".
- Se o design (Figma) da tela "Meu perfil" já tiver uma posição definida para o campo diferente da recomendada, a posição no critério de aceite deve ser atualizada.

## Impacto

- **Produto**: Conta do jogador (PAM) — tela "Meu perfil"/"Minha Conta", seção "Informações pessoais", app e site.
- **Técnico**: reúso de integração de KYC já existente (Serasa ou Legitimuz); nenhuma integração nova.
- **Processo**: reforça o precedente de separar pendência de produto (resolvida na conversa: editabilidade, comportamento de dado ausente, formato de exibição) de pendência técnica (fica "Aberto para refinamento técnico" no card), seguindo o mesmo padrão do card do campo "sexo".

## Links

- Card ajustado: [868m2u5vg](https://app.clickup.com/t/868m2u5vg) — "Exibir nacionalidade em 'Meu perfil'"
- Precedente direto: [868ktk86b](https://app.clickup.com/t/868ktk86b) — "Corrigir o campo sexo do cadastro do jogador com o CPF check da Legitimuz"
- Decisão relacionada (precedente de fonte e padrão de triagem produto/técnico): [2026-08-18-correcao-campo-sexo-cpf-check-legitimuz-nao-e-genero-autodeclarado](2026-08-18-correcao-campo-sexo-cpf-check-legitimuz-nao-e-genero-autodeclarado.md)
