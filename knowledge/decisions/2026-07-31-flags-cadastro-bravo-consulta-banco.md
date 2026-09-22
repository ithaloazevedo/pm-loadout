# Flags de progresso no funil de cadastro/KYC/depósito da Bravo, classificadas como Épico, com pendência de arquitetura de acesso ao banco registrada sem bloquear a criação

**Data**: 2026-07-31
**Tomada por**: Ithalo Mendes
**Status**: APROVADA

---

## Contexto

A Bravo (segunda marca, cliente do PAM) pediu a implementação de flags de progresso para 11 etapas do funil de cadastro, KYC e depósito — CPF inserido, senha inserida, telefone inserido, telefone validado, email inserido, email validado, tela pré-KYC, KYC, verificação facial com sucesso, tela de depósito, depósito concluído — para consultar via SQL direto no banco e montar seus próprios dashboards de conversão.

Duas decisões precisavam ser tomadas ao especificar: (1) classificar o item como Épico ou Tarefa; (2) como tratar a pendência de arquitetura de acesso ao banco (a Bravo consultando diretamente um banco compartilhado com a Tradicional) sem travar a criação do card.

## Opções Consideradas

1. **Classificar como Tarefa** — tratar como ajuste simples de instrumentação.
   - Prós: reflete a aparência inicial do pedido ("adicionar flags").
   - Contras: descartada — 11 checkpoints cruzando dois módulos (Onboarding + Carteira), decisão de segurança/LGPD pendente (isolamento de dado entre casas no PAM compartilhado) e um entregável fora do padrão da squad (documentação técnica para consumidor externo) não cabem em uma sprint.

2. **Classificar como Épico**, refletindo o escopo técnico real.
   - Prós: mesmo raciocínio do precedente do liveness (`2026-07-30-liveness-pos-login-7-dias-classificado-epico.md`) — escopo real deve prevalecer sobre a aparência de simplicidade do pedido.
   - Contras: nenhum relevante identificado.

3. **Bloquear a criação do card até confirmar o mecanismo de acesso da Bravo ao banco** (arquitetura/segurança) vs. **criar agora e registrar a pendência como "Aberto para refinamento"**.
   - Prós de criar agora: segue o precedente do card do Smartico (`2026-07-30-bloqueio-campanhas-smartico-cadastro-login.md`), que registrou pendência de arquitetura sem bloquear a criação; mantém o card como fonte única de rastreio da pendência.
   - Contras: card pode ser priorizado por engano antes da pendência de segurança/LGPD ser resolvida — mitigado por manter o card em `backlog`/`em refinamento` até lá.

## Decisão

Optou-se pela **Opção 2 (Épico)** e pela **criação imediata do card com a pendência registrada** (Opção 3, segunda alternativa). Card criado: [Flags de progresso do funil de cadastro, KYC e depósito para consulta via SQL (Bravo)](https://app.clickup.com/t/868kjmpj6), Folder Delivery: Plataforma, Lista Backlog, `task_type: Epic`, status `backlog`.

Squad dona provisória: **Plataforma (Experiência do Jogador)** — cobre as etapas 1-9 (Onboarding) e é dona histórica das rotas de cadastro/login (mesmo precedente do Smartico). A titularidade das etapas 10-11 (depósito, módulo Carteira) **não foi confirmada** e ficou registrada como pendência no card, sem desmembrar preventivamente em subtask separada — mesmo trade-off aceito no card do Smartico.

Campos de alta confiança setados: `Empresa = Bravo`, `_Projeto = Bravo`. Campos como KPIs (sugestão: Observabilidade), Módulo do PAM (deixado em branco por cruzar Cadastro e acesso + KYC + Financeiro) e prioridade nativa (sugestão: Alta) foram propostos como suposição no corpo do card, não gravados como decisão fechada. Assignee não foi atribuído, conforme regra fixa do workspace.

## Trade-offs Aceitos

- O card pode ficar em `backlog`/`em refinamento` por mais tempo até o Tech Lead da squad Plataforma confirmar o mecanismo de acesso da Bravo ao banco — aceito conscientemente para não travar a existência do item nem forçar uma decisão de segurança apressada.
- Squad de Carteira (etapas 10-11) pode precisar de um item complementar ou subtask se, no refinamento, ficar confirmado que depósito tem dono técnico diferente de Plataforma.
- Nenhum vínculo formal a Objetivo/KR — o candidato mais próximo ("Elevar a conversão Cadastro → FTD de 37% para 70%") foi citado no corpo do card como sugestão, não linkado, por decisão de quem mede ser a Bravo e não a Vertical.
- Fonte original do pedido da Bravo (chat/e-mail/ticket) não foi localizada nesta missão — registrada como pendência no card.

## O que mudaria a decisão

- Se o Tech Lead de Plataforma confirmar que expor uma réplica/view de leitura à Bravo é tecnicamente equivalente a um mecanismo já existente (ex.: o item adjacente "Acesso ao banco de dados de produção com níveis de leitura e escrita para a squad Plataforma", achado durante a verificação de duplicidade), o escopo de arquitetura deste épico pode reduzir.
- Se ficar confirmado que Carteira/depósito é de outra squad, desmembrar em subtask ou item complementar, seguindo o mesmo critério usado no Smartico.
- Se a fonte do pedido da Bravo for localizada, adicionar aos Links do card para rastreabilidade, como nos precedentes.

## Impacto

- **Produto**: módulos Onboarding (cadastro, KYC, verificação facial) e Carteira (depósito), casa Bravo.
- **Técnico**: persistência de novas flags/estado por etapa, integração com Serasa (KYC/verificação facial), e um novo mecanismo de leitura ao banco exposto a um cliente externo — com requisito de isolamento de dado entre Bravo e Tradicional no PAM compartilhado (implicação de segurança e LGPD, dado que os dados incluem CPF e resultado de verificação facial).
- **Processo**: nenhuma mudança de processo; reforça o padrão de registrar pendência de arquitetura dentro do próprio item em vez de bloquear a criação por falta de confirmação técnica (mesmo padrão do Smartico).

## Links

- Card criado: [868kjmpj6](https://app.clickup.com/t/868kjmpj6) — "Flags de progresso do funil de cadastro, KYC e depósito para consulta via SQL (Bravo)"
- Precedente de classificação: [2026-07-30-liveness-pos-login-7-dias-classificado-epico.md](2026-07-30-liveness-pos-login-7-dias-classificado-epico.md)
- Precedente de pendência não-bloqueante: [2026-07-30-bloqueio-campanhas-smartico-cadastro-login.md](2026-07-30-bloqueio-campanhas-smartico-cadastro-login.md)
