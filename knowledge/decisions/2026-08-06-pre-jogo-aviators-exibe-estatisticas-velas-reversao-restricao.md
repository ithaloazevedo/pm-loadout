# Tela pré-jogo dos Aviators pode exibir estatísticas de velas/multiplicadores — reversão da restrição regulatória da task

**Data**: 2026-08-06
**Tomada por**: Ithalo Mendes (PM), com aprovação de compliance/regulatório afirmada
**Status**: APROVADA

---

## Contexto

A task [868kkyva6](https://app.clickup.com/t/868kkyva6) — "[PAM] Telas pré-jogo Aviator", com discovery finalizado — foi criada em 02/08/2026 com uma **linha vermelha regulatória** explícita no critério de aceite obrigatório:

> "A tela não pode exibir nenhum tipo de estatística, histórico de multiplicadores, indicador de 'quente/frio', probabilidade, tendência ou qualquer dado que sugira ao jogador previsibilidade ou maior chance de ganho. [...] é uma linha vermelha regulatória/responsible gaming."
> "Qualquer dado histórico, estatístico ou de tendência — fora por definição, não é lacuna a preencher."

Em 04/08/2026 o time de design anexou à task o Figma ("PAM – Pré-Jogo") e o HTML de especificação de interface (`pre-jogo-especificacao-interface.html`), que contêm **exatamente** esses dados: velas por cor dos últimos 30 min, histórico de ciclo de multiplicadores e a seção "Dados p/ análise" com cards `3x+ … 50x+`. A semântica dos cards (ex.: "30x+ 54/40" = 54 rodadas sem sair uma 30x, média a cada 40) comunica ao jogador que um multiplicador "está atrasado" — o padrão-livro de indutor de aposta (falácia do apostador).

Ou seja: o design entregue contradiz diretamente o critério de aceite regulatório do próprio discovery. O gatilho da decisão foi resolver essa contradição antes de especificar o Delivery.

## Opções Consideradas

1. **Validar com regulatório antes de especificar** — acionar vigilância regulatória p/ confirmar permissão sob a regulação de apostas de quota fixa (Lei 14.790/2023) e diretrizes de jogo responsável, mantendo a parte neutra do escopo em paralelo.
   - Prós: rota segura; carimbo de compliance documentado antes de construir a camada sensível.
   - Contras: adiciona um gate antes do fechamento da seção de dados.

2. **Compliance já aprovou — seguir completo** — o jurídico/regulatório já liberou exibir os dados; a restrição da task ficou obsoleta.
   - Prós: destrava a spec completa (com dados dinâmicos); alinhado ao design já entregue e à priorização pedida por Isaac Ribeiro.
   - Contras: a aprovação de compliance precisa estar documentada; a task ainda carrega o critério de aceite oposto, que induz a erro quem a ler.

3. **Reescopar sem os trackers** — manter a linha vermelha e especificar só dados neutros do jogo.
   - Prós: risco regulatório zero.
   - Contras: contraria o design entregue e a intenção de produto atual.

## Decisão

Escolhida a **Opção 2 — compliance já aprovou**. O PM confirmou que o jurídico/regulatório liberou exibir velas, histórico de ciclo e a seção "Dados p/ análise". A restrição registrada na task 868kkyva6 é considerada **obsoleta** e deve ser atualizada para refletir a aprovação, evitando que quem leia o card conclua o contrário.

A tela pré-jogo dos três Aviators (Aviator, Aviator 2, Aviãozinho) segue para Delivery **com** a camada de dados dinâmicos.

## Trade-offs Aceitos

- Exibir dados que sugerem frequência/atraso de multiplicadores tem risco de jogo responsável inerente; assume-se esse risco com base na aprovação de compliance.
- **A aprovação de compliance foi afirmada verbalmente pelo PM, não há evidência documental anexada nesta data.** Recomenda-se anexar ao card a evidência (quem aprovou, quando, com que embasamento) para blindar a decisão em auditoria futura.

## O que mudaria a decisão

- Surgir uma leitura regulatória (SPA/MF, GLI, jurídico interno) de que exibir frequência/atraso de multiplicadores caracteriza indução de aposta vedada.
- A evidência da aprovação de compliance não se confirmar quando solicitada.

## Impacto

- **Produto**: tela pré-jogo (pre-launch) dos jogos crash Aviator, Aviator 2 e Aviãozinho — Módulo Hubs de Jogos / Plataforma (PAM), empresa Tradicional.
- **Técnico**: exige fonte de dados em tempo real por jogo (velas por cor/30 min, histórico de ciclo, cards de frequência, pagamentos hoje) — dependência de integração a definir com engenharia. Rota pública acessível deslogado.
- **Processo**: o critério de aceite regulatório da task 868kkyva6 precisa ser atualizado (via agente-delivery, sem reescrever o Contexto — a mudança vai para o Log de Decisões do card, conforme [[2026-07-28-log-de-decisoes-separado-do-contexto]]).

## Links

- Card no ClickUp: [868kkyva6](https://app.clickup.com/t/868kkyva6) — [PAM] Telas pré-jogo Aviator
- Figma: https://www.figma.com/design/7JTyTkLWqr9WY1UVItI246/PAM---Pr%C3%A9-Jogo?node-id=1-92
- Especificação de interface (anexo do card): `pre-jogo-especificacao-interface.html`
- Precedente de tema regulatório: [[2026-07-30-ocultar-indique-e-ganhe-vedacao-regulatoria]]
