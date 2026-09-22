# Checagem de geolocalização (Portaria 722/2024, Arts. 27-34) implementada via SDK Legitimuz, com enforcement diferenciado por tipo de sinal

**Data**: 2026-08-14
**Tomada por**: Ithalo Mendes (via Orquestrador + agentes vigilancia-regulatoria, agente-spec, agente-delivery)
**Status**: APROVADA

---

## Contexto

Ithalo trouxe um print de uma norma regulatória com uma seção "Dos requisitos de geolocalização — Prevenção de fraudes de localização" (Arts. 27-34) e um link de um ClickUp Doc externo (workspace de outra organização, inacessível via integração — retornou `not_found_or_authorized`) contendo a documentação técnica de um "SDK" a ser avaliado para atender ao requisito. O usuário citou a norma internamente como "portaria 722".

Como o link do doc não pôde ser lido automaticamente, o Orquestrador perguntou ao usuário qual era o fornecedor — a resposta foi **Legitimuz**, que o usuário confirmou colando o conteúdo técnico completo da documentação do SDK diretamente no chat.

## Achados

1. **"Portaria 722" é real e específica**: confirmado pelo agente `vigilancia-regulatoria` (DOU + espelhos oficiais) que se trata da **Portaria SPA/MF nº 722, de 2 de maio de 2024**, em vigor desde a publicação, aplicável igualmente a app mobile e web/desktop (a norma não diferencia canal).
2. **Achado colateral de higiene regulatória**: uma citação diferente, corrente no canal interno de Compliance da empresa ("Portaria 2.579/2025, Art. 31, XVI", sobre limites prudenciais de aposta), está com a norma-base errada — esse artigo pertence à **Portaria 1.231/2024**; a 2.579/2025 apenas altera dispositivos de autoexclusão da mesma portaria-base. Não corrigido nesta missão (fora do escopo do card criado) — só sinalizado ao usuário para correção manual no canal de Compliance.
3. **O SDK da Legitimuz é client-side (browser, script tag) e assíncrono via webhook** — não há confirmação de SDK nativo equivalente para app mobile puro na documentação recebida. A própria Legitimuz já modelou uma ação dedicada `check`, documentada como "must be sent every 30 minutes" — ou seja, o fornecedor desenhou o método pensando exatamente no Art. 33.
4. **Lacuna de cobertura**: a documentação recebida não evidencia cobertura para os Arts. 27 (rootkit/virtualização/RDP), 29 (root/jailbreak) e 30 (anti-MITM/anti-tampering) — só cobre geolocalização e reputação de IP (VPN/proxy/Tor/botnet) e "impossible travel".
5. **Art. 34 (certificação) não é sobre homologar o fornecedor de geolocalização** — é sobre certificar o sistema de apostas como um todo por uma entidade certificadora habilitada pela SPA (ex. Trisgma, Quinel, Gaming Associates Europe), com prazo de 90 dias contado do ato de autorização de funcionamento de cada operador (Art. 8º da própria 722/2024) — data do ato de autorização da Tradicional/Bravo não confirmada nesta missão; risco de o prazo já ter vencido, dado que a operação já está no ar.
6. **A Legitimuz já está integrada em produção** — achado do `agente-delivery` ao checar duplicidade: existe um épico já finalizado, [868kckzxv "Integrar Legitimuz (AML)"](https://app.clickup.com/t/868kckzxv), usando o mesmo fornecedor para score de renda presumida. Este novo épico é extensão de uso de uma integração existente, não uma integração do zero.
7. **Épico irmão na mesma Portaria**: [868khhfn0 "Autenticação persistente para o app"](https://app.clickup.com/t/868khhfn0) já tratou dos Arts. 14/16 da mesma Portaria 722/2024 (reautenticação após 30 min de inatividade + MFA a cada 7 dias) — ver decisão [2026-08-11-requisitos-regulatorios-sessao-login-biometria-device](2026-08-11-requisitos-regulatorios-sessao-login-biometria-device.md). Há duas mecânicas de "30 minutos" na mesma jornada (reautenticação de sessão vs. checagem de geolocalização) que precisam ser coordenadas na arquitetura — registrado como pendência de "Aberto para refinamento técnico" no novo card, não decidido nesta missão.

## Opções Consideradas

**Enforcement para sinais de fraude de localização:**

1. **Bloquear a aposta para todo sinal (VPN/proxy/Tor/botnet E impossible travel) com o mesmo rigor** — mais conservador do ponto de vista de compliance, mas "impossible travel" é um sinal mais fraco e sujeito a falso positivo (ex.: troca de wifi para 4G), gerando fricção indevida em usuários legítimos.
2. **Bloquear direto quando VPN/proxy/Tor/botnet é detectado (mandado pelos Arts. 27/28/32, não é opcional) e degradar para verificação adicional (ex.: solicitar GPS) antes de bloquear quando só "impossible travel" for sinalizado.**

**Empresa (Tradicional vs. Bravo):**

1. Dois épicos irmãos, um por casa.
2. Item único cobrindo as duas casas, com campo `Empresa = Vertical` como guarda-chuva (mesmo padrão já registrado em [2026-07-30-bloqueio-campanhas-smartico-cadastro-login](2026-07-30-bloqueio-campanhas-smartico-cadastro-login.md)).

## Decisão

1. Optou-se pela **Opção 2** de enforcement: bloqueio direto para reputação de IP (VPN/proxy/Tor/botnet), verificação adicional antes de bloquear para "impossible travel". Decisão do PM, não do Orquestrador — a norma mandata bloqueio para o primeiro caso, mas dá margem de produto para o segundo por ser sinal mais fraco.
2. Optou-se por **item único cobrindo Tradicional + Bravo**, seguindo o precedente já registrado — a implementação é uma única integração client-side no PAM compartilhado, sem motivo técnico confirmado para desmembrar por casa.
3. Módulo do PAM = **Compliance** (não AML nem Cadastro e acesso, as duas opções originalmente propostas pelo `agente-spec` — o usuário escolheu a terceira opção já existente no dropdown do workspace).
4. Épico criado reaproveitando um placeholder vazio ("Geoloc") que o próprio Ithalo já havia criado no Backlog da squad Experiência do jogador, em vez de abrir um item novo do zero.

## Trade-offs Aceitos

- **Risco residual assumido conscientemente**: Arts. 27/29/30 (rootkit, root/jailbreak, anti-MITM) ficam fora do escopo deste épico até confirmação com a Legitimuz sobre se e como eles cobrem esses pontos. Ação de confirmação com o fornecedor roda em paralelo, fora do card.
- **Dependência externa não resolvida**: certificação do sistema por entidade habilitada pela SPA (Art. 34) e o prazo de 90 dias (Art. 8º) são frente de compliance/jurídico, não de engenharia — o épico técnico pode ficar pronto e a operação ainda estar formalmente não conforme até essa auditoria acontecer.
- Campo `_Projeto` (Tradicional/Bravo exclusivo) ficou vazio, só `Empresa = Vertical` preenchido — mesmo trade-off já aceito no precedente Smartico.
- Card criado sem assignee — dono pendente de confirmação do PM.
- Achado de doc drift não corrigido nesta missão: `agente-delivery.md` e `clickup-method.md` citam campos `_Classe` e `_Risco Reg.` como obrigatórios em Delivery, mas eles não existem de fato no folder usado (confirmado via `clickup_get_custom_fields`) — sinalizado para um passe futuro de `agente-governanca`, não bloqueou a criação do card.

## O que mudaria a decisão

- Confirmação da Legitimuz sobre cobertura (ou não) dos Arts. 27/29/30 — se não cobrirem, é preciso avaliar fornecedor complementar antes de declarar compliance total.
- Confirmação se o app mobile da Tradicional/Bravo é WebView (script funciona direto) ou nativo puro (precisaria de SDK mobile equivalente, não evidenciado na documentação recebida) — registrado como "Aberto para refinamento técnico" no card.
- Confirmação da data do ato de autorização de funcionamento de cada casa, para calcular se o prazo de 90 dias de certificação (Art. 8º) já venceu.
- Se Plataforma/Tech Lead confirmarem que a implementação por casa precisa ser separada (ex. datas de rollout diferentes por licença SPA), o item deve ser desmembrado em dois épicos irmãos.

## Impacto

- **Produto**: módulo Compliance; jornadas de login, cadastro, depósito, saque e aposta (onde o SDK dispara `sendAnalisys`), Tradicional e Bravo.
- **Técnico**: extensão da integração já existente com a Legitimuz (client-side, via script); necessidade de definir arquitetura de espera do webhook assíncrono antes de liberar a conclusão da aposta; coordenação com o timer/heartbeat de sessão do épico 868khhfn0.
- **Processo**: reforça o padrão de rodar `vigilancia-regulatoria` antes de fechar spec com pendência regulatória, e de checar duplicidade/placeholders existentes antes de criar itens novos no ClickUp.

## Links

- Card criado: [868kr6b33](https://app.clickup.com/t/868kr6b33) — "Garantir a checagem de localização do jogador antes da aposta e a cada 30 minutos para atender à exigência regulatória de geolocalização"
- Objetivo vinculado: [868kcdz64](https://app.clickup.com/t/868kcdz64) — "Escalar a operação multimarcas com autonomia e conformidade" (vazio, sem KRs — linkado mesmo assim para rastreabilidade)
- Épico irmão (mesma Portaria, Arts. 14/16): [868khhfn0](https://app.clickup.com/t/868khhfn0) — "Autenticação persistente para o app"
- Épico base (integração Legitimuz já existente): [868kckzxv](https://app.clickup.com/t/868kckzxv) — "Integrar Legitimuz (AML)"
- Decisão relacionada: [2026-08-11-requisitos-regulatorios-sessao-login-biometria-device](2026-08-11-requisitos-regulatorios-sessao-login-biometria-device.md)
- Decisão relacionada (precedente Empresa dupla): [2026-07-30-bloqueio-campanhas-smartico-cadastro-login](2026-07-30-bloqueio-campanhas-smartico-cadastro-login.md)
- Fonte primária da norma: Portaria SPA/MF nº 722/2024 — [BNLData (texto integral Arts. 27-34)](https://bnldata.com.br/legislacao/portaria-spa-mf-no-722-de-2-de-maio-de-2024-sistema-de-apostas/), [LegisWeb](https://www.legisweb.com.br/legislacao/?id=458565)
