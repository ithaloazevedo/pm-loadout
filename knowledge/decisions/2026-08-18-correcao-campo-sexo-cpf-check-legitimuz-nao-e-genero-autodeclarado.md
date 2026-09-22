# Correção do campo "sexo" via CPF check da Legitimuz é uso interno de CRM/BI — distinto do "gênero autodeclarado" da Portaria SPA/MF 2.579/2025

**Data**: 2026-08-18
**Tomada por**: Ithalo Mendes (via Orquestrador + agentes vigilancia-regulatoria, agente-governanca, agente-spec, agente-delivery)
**Status**: APROVADA

---

## Contexto

Ithalo trouxe a missão já com solução definida: "fazer varredura na base no login, para atualizar sexo no banco de dados pois temos uma base de usuários 100% masculina" — aproveitando que o CPF check da Legitimuz (fornecedor já integrado em produção para KYC/AML, épico [868kckzxv](https://app.clickup.com/t/868kckzxv)) retorna esse dado.

O Orquestrador não tratou o pedido como spec pronta — acionou `vigilancia-regulatoria` e `agente-governanca` antes de qualquer card, por dois sinais de alta criticidade: mudança em massa em banco de produção de dado pessoal, e uma suposição não verificada ("sexo" == "gênero").

## Achados

1. **Achado regulatório central**: a Portaria SPA/MF nº 2.579/2025 (altera a 1.231/2024) exige coletar "identificação do gênero do apostador" no cadastro, para fins de autoexclusão/módulo de impedidos — mas esse campo é **autodeclarado pelo próprio usuário**. É uma fonte e um propósito diferentes do "sexo" registral que vem da Receita Federal via CPF check. Confundir os dois cria não-conformidade dupla (fonte errada para o requisito regulatório, e uso fora de finalidade para o dado de KYC).
2. **Risco de desvio de finalidade (LGPD art. 6º, I)**: o CPF check foi consultado sob base legal de cumprimento de obrigação regulatória (KYC/AML). Reaproveitar o "sexo" retornado para popular um campo usado em BI/CRM/segmentação é finalidade nova, não coberta automaticamente pela integração existente — exige base legal própria e possível atualização de política de privacidade antes de rodar a varredura em produção.
3. **Causa raiz do "100% masculino" não estava confirmada** — pode ser ausência histórica de coleta ou bug ativo de captura no cadastro. Ficou como pendência técnica explícita no card (não bloqueia a criação, mas bloqueia o rollout em sprint).
4. **Estrutura de squads mudou desde 30/07/2026** e o `agente-spec` inicialmente usou nomenclatura antiga ("Operação e afiliados" / "Experiência do jogador" como termos soltos) — a estrutura vigente é Backoffice & Integrações / Plataforma (Experiência do Jogador) / Produto. Ithalo é PM em ambos os squads candidatos (Backoffice & Integrações e Plataforma).
5. **Dois gaps de campo confirmados pelo `agente-delivery`**: `_Classe` não existe na lista Backlog do folder Delivery: Experiência do Jogador (existe só na lista Execução da mesma folder, e no folder Backoffice & Integração); `_Risco Reg.` não existe em nenhum escopo do workspace, apesar de citado no método. Nenhum dos dois foi criado — reportados como gap estrutural para `agente-governanca`/`agente-evolucao`, não resolvidos nesta missão.

## Opções Consideradas

**Propósito de negócio do campo "sexo":**
1. Atender à exigência regulatória de gênero da Portaria 2.579/2025 — descartada, porque esse campo precisa ser autodeclarado, o CPF check não serve para essa finalidade.
2. Uso interno de segmentação/CRM/BI — **escolhida**.

**Squad dono:**
1. Plataforma (Experiência do Jogador) — dona da base de usuários, cadastro, login e perfil.
2. Backoffice & Integrações — dona da relação com o fornecedor Legitimuz.

**Vínculo com Iniciativa/OKR:**
1. Linkar direto a um OKR sem Iniciativa intermediária, seguindo o precedente do próprio 868kckzxv — **escolhida**.
2. Criar/vincular a uma Iniciativa de qualidade de dado — descartada, nenhuma existe hoje e criar uma só para este item foi considerado overhead desnecessário.

## Decisão

1. O campo "sexo" corrigido por este item é de **uso interno de CRM/BI**, não o campo de gênero autodeclarado da Portaria 2.579/2025 (esse é outro requisito, outro épico, fora de escopo aqui).
2. Squad dono: **Plataforma (Experiência do Jogador)**.
3. OKR pai: **"Aumentar engajamento e retenção melhorando a percepção de valor do usuário"** ([868k6mdf6](https://app.clickup.com/t/868k6mdf6)), linkado direto, sem Iniciativa.
4. Módulo do PAM: **Conta do jogador** (é tecnicamente um campo de cadastro/perfil, independente do uso posterior).
5. Épico criado: [868ktk86b](https://app.clickup.com/t/868ktk86b) — Backlog, Delivery: Experiência do Jogador, sem assignee.
6. Os dois riscos de compliance (base legal/finalidade LGPD; confirmação de que o campo não é consumido em nada user-facing hoje) entraram como **critérios de aceite testáveis**, não como pendência aberta — o épico não deve entrar em sprint com eles em aberto.

## Trade-offs Aceitos

- O card nasce sem sign-off jurídico/DPO — decisão consciente de não bloquear a criação do item por isso, mas o rollout em produção fica travado até o sign-off existir.
- Três pendências técnicas legítimas ficaram em "Aberto para refinamento técnico": causa raiz do 100% masculino, se o payload do CPF check já está armazenado (custo do backfill) ou exige reconsulta à Legitimuz, e o ponto exato do fluxo (cadastro/KYC, não literalmente "login") onde a atualização prospectiva dispara.
- Gaps de `_Classe` e `_Risco Reg.` não resolvidos — o card foi criado sem eles.
- A seção visual "Portfólio de Projetos" do OKR 868k6mdf6 ainda não reflete este vínculo (o linked task já está gravado); recomendado rodar `clickup-rollup` para consolidar.

## O que mudaria a decisão

- Se a verificação de consumo do campo "sexo" encontrar uso user-facing (comunicação personalizada, saudação, formulário de perfil exibido), o risco de misgendering em massa volta à mesa e pode justificar reabrir a decisão de produto (ex.: separar "sexo registral" de um campo de autodeclaração opcional).
- Se jurídico/DPO reprovar a base legal proposta, a varredura não roda até haver alternativa (ex.: consentimento explícito em vez de uso automático do dado de KYC).
- Se a causa raiz do "100% masculino" for um bug ativo de captura, o escopo do item precisa crescer para incluir a correção do fluxo de cadastro, não só o backfill.

## Impacto

- **Produto**: Conta do jogador (PAM), potencial alimentação futura de CRM/Marketing e Hub de Benefícios/percepção de valor.
- **Técnico**: reúso da integração Legitimuz já existente (CPF check); nenhuma integração nova.
- **Processo**: reforça o padrão de não aceitar solução pré-definida sem separar pendência de produto/compliance (resolvida na conversa) de pendência técnica (fica "Aberto para refinamento" no card); reforça também checar a estrutura de squads vigente antes de nomear folders/donos, já que a nomenclatura muda com frequência.

## Links

- Card criado: [868ktk86b](https://app.clickup.com/t/868ktk86b)
- OKR vinculado: [868k6mdf6](https://app.clickup.com/t/868k6mdf6) — "Aumentar engajamento e retenção melhorando a percepção de valor do usuário"
- Épico base (integração Legitimuz já existente): [868kckzxv](https://app.clickup.com/t/868kckzxv) — "Integrar Legitimuz (AML)"
- Decisão relacionada (estrutura de squads vigente): [2026-07-30-estrutura-times-e-papeis](2026-07-30-estrutura-times-e-papeis.md)
- Decisão relacionada (assignee nunca automático): [2026-07-27-assignee-nunca-atribuido-sem-confirmacao](2026-07-27-assignee-nunca-atribuido-sem-confirmacao.md)
