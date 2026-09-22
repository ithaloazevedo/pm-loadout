# Bug de performance na home do Tradicional classificado como Bug único, sem guarda-chuva de Correções

**Data**: 2026-08-04
**Tomada por**: Ithalo Mendes (com shaping do agente-spec)
**Status**: APROVADA

---

## Contexto

GTmetrix apontou grade E (Performance 40%) na home do Tradicional (tradicional.bet.br), com degradação contínua nos últimos 4 meses (Performance Score de ~50% para 40%, payload de ~2,9MB para 3,8MB). O canal de aquisição "Resultado Fácil" concentra usuários com aparelhos simples e conexões 3G — pior cenário que o próprio GTmetrix testou (profile Galaxy S6/S7 em 4G). O time já havia percebido o gap de teste antes deste pedido: configurou um device profile customizado no Chrome DevTools ("Resultado Fácil" — Galaxy A03, Android 11, 360×800) para reproduzir o pior aparelho da base.

## Opções Consideradas

1. **Bug único, com frentes de correção como Critérios de Aceite agrupados** — investigação + fixes de app/imagens/terceiros/infra dentro do mesmo item.
   - Prós: mantém coerência com a definição vigente de Bug (defeito em produção com impacto no usuário); evita fragmentar prematuramente antes de saber onde está a causa raiz dominante.
   - Contras: escopo de correção é amplo e pode ultrapassar o padrão "pequeno, urgente" de um Bug.

2. **Bug guarda-chuva com Correções como subtarefas** (uma Correção por frente: imagem lazy, terceiros, cache, etc.)
   - Prós: paraleliza o trabalho entre devs.
   - Contras: descasa com a definição vigente de Correção (achado em dev/homologação, sem impacto no usuário) — subtask de algo que já afeta produção não se encaixa por construção.

3. **Épico** — tratar como projeto de otimização de performance.
   - Prós: nenhum relevante aqui.
   - Contras: Épico é para nova entrega de valor; isto é remediar uma degradação existente, não construir algo novo.

## Decisão

Bug único (Opção 1). Critério decisivo: a definição vigente de Correção (`clickup-config-tech.md`) exige que o achado seja de dev/homologação — um Bug que já afeta produção não pode gerar subtask "Correção" sem violar essa taxonomia. Se o refinamento revelar que uma frente (ex.: scripts de terceiros, que depende de alinhamento com Marketing/CRM) precisa de trilha própria, ela vira subtask do tipo **Tarefa**, não Correção.

## Trade-offs Aceitos

O card pode crescer além do padrão usual de Bug se a investigação revelar causas muito distintas (app, imagens, terceiros, infra). Aceito conscientemente — o checkpoint de refinamento decide se alguma frente sai como item separado, mas o ponto de partida é um único Bug.

## O que mudaria a decisão

Se o refinamento com a squad concluir que a frente de terceiros (dependente de Marketing/CRM, com timeline potencialmente muito mais longa) trava o restante do trabalho, ela deve sair como Tarefa separada — não Correção, e não ficar acoplada ao Bug principal.

## Impacto

- **Produto**: home do Tradicional (squad Plataforma / Experiência do Jogador); afeta diretamente conversão do funil de entrada via canal Resultado Fácil.
- **Técnico**: bundle da aplicação Nuxt, imagens servidas via CDN, scripts de terceiros (Facebook, GTM, TikTok, Kwai, AppsFlyer), política de cache.
- **Processo**: reforça o precedente de que "Correção" nunca nasce de um Bug já em produção — sempre nasce de achado em dev/homologação.

## Links

- Card no ClickUp: [868km2d37](https://app.clickup.com/t/868km2d37) — "Corrigir lentidão e quebras na home para aparelhos/internet limitados"
- Evidência: relatório GTmetrix de tradicional.bet.br (04/08/2026, grade E)
- Thread relacionada: configuração do device profile "Resultado Fácil" no ClickUp (canal `8ccvn07-58611`)
