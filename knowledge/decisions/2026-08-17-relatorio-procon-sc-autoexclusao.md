# Relatório técnico assinado à Blow Marketplace sobre autoexclusão, respondendo ao item 4 do ofício do PROCON/SC

**Data**: 2026-08-17
**Tomada por**: Ithalo Mendes (via Orquestrador + agentes curador-de-contexto, vigilancia-regulatoria, agente-delivery)
**Status**: APROVADA

---

## Contexto

Thuane (Compliance) pediu, em 14/08/2026, um relatório técnico assinado da Vertical até segunda-feira (17/08/2026, mesmo dia da entrega) para subsidiar a resposta da Blow Marketplace LTDA (CNPJ 37.486.405/0001-91) ao Ofício nº 392/2026/SSP/PROCON/COAM (Processo SGPE SSP 00030437/2026), especificamente o item 4: procedimentos de autoexclusão de consumidores, imediatismo do bloqueio de acesso e interrupção de comunicações de marketing.

O modelo a seguir foi um relatório equivalente já enviado ao PROCON-SP (mesmo CNPJ da Blow Marketplace como destinatária), recuperado de um Artifact anterior — formato de 3 páginas, timbrado, assinado por Ithalo como PM, item por item com citação literal + resposta técnica + callout de enquadramento regulatório.

## Apuração realizada

Antes de escrever qualquer texto, rodei 3 apurações em paralelo (curador-de-contexto no claude-os, vigilancia-regulatoria em fontes primárias DOU, agente-delivery no ClickUp), porque a resposta ao item 4 tem peso legal e não podia ser escrita por suposição.

**Achados confirmados:**
- Existem duas modalidades juridicamente distintas: **autoexclusão específica** (direta com a Tradicional/Bravo) e **autoexclusão centralizada** (via SIGAP, registro nacional) — não podem ser tratadas como sinônimos na resposta.
- Autoexclusão específica: bloqueio da **capacidade de apostar** é imediato (texto literal da política pública `tradicional.bet.br/jogo-responsavel`), mas **não bloqueia login/navegação/saque** — o consumidor mantém acesso para consultar saldo e sacar.
- Retorno pós-vencimento da autoexclusão temporária **não é automático**: exige confirmação afirmativa do usuário numa tela intermediária ("Continuar" / "Talvez mais tarde") a cada login; sem essa confirmação, o bloqueio de aposta continua — confirmado por screenshot real fornecido por Ithalo durante a missão.
- Autoexclusão centralizada (SIGAP): a norma primária (IN SPA/MF nº 31/2025, art. 7º) manda impedir novas apostas imediatamente e encerrar a conta em até 3 dias, comunicar o motivo em até 1 dia e permitir saque voluntário em até 2 dias. A implementação técnica real (achado no ClickUp, cards 868k7r03e / 868ke5bhx / 868kckyfx) é um **worker periódico** — histórico de 15/15 dias, evoluído para 1x/dia — e não uma consulta síncrona a cada tentativa de login como uma memória anterior desta sessão registrava. Memória [[sigap-integracao-vertical]] corrigida para refletir essa nuance.
- Base legal exata confirmada em fonte primária (DOU): Lei 14.790/2023 art. 8º III e parágrafo único (delegação regulamentar) e art. 26 (impedimentos estruturais, categoria distinta de autoexclusão voluntária); Portaria SPA/MF nº 1.231/2024 (arts. 4º IV "d"/V, 11 VII); Portaria SPA/MF nº 2.579/2025 (cria definições de autoexclusão específica/centralizada, estende dever de abstenção publicitária às duas); IN SPA/MF nº 31/2025 (arts. 4º, 6º-9º — prazos operacionais do fluxo SIGAP). Não existe prazo numérico regulatório para a autoexclusão **específica** nem para a supressão de marketing — são deveres de abstenção contínua, não SLAs cronometrados.
- **Achado crítico durante a apuração**: card ClickUp VL-13295 (868kdn5gp), aberto 17/07/2026, documentava um incidente real (cliente bloqueado recebeu marketing, pediu indenização) sem resolução registrada até a data da missão. Levado ao Ithalo antes de escrever qualquer texto sobre o ponto.

## Decisão

1. **Sobre o incidente (VL-13295)**: Ithalo instruiu desconsiderar o card e confirmou verbalmente que a supressão de comunicações de marketing para autoexcluídos **já foi corrigida** — o relatório assume esse estado como vigente na data de emissão (17/08/2026), sem mencionar o incidente.
2. **Sobre o relatório**: gerado como Artifact reaproveitando fielmente o design/timbre/fontes do modelo anterior (mesma identidade visual da série de relatórios ao PROCON), com texto novo para o item 4, distinguindo as duas modalidades de autoexclusão e citando a base legal exata. Deixado um placeholder no Anexo I para o print real da tela de retorno pós-vencimento (a imagem foi colada diretamente no chat, sem caminho de arquivo acessível para extração automática).
3. Escopo do relatório mantido em **Tradicional apenas** (não Bravo), espelhando o precedente do relatório anterior ao PROCON-SP, já que o novo ofício do PROCON/SC não especifica marca e a Bravo não teve o conteúdo ao vivo de sua política confirmável nesta apuração (fetch bloqueado).

## Trade-offs Aceitos

- O relatório não documenta nem referencia o incidente VL-13295 — decisão do PM, que tem contexto sobre a correção que o agente não tinha acesso via ClickUp/claude-os.
- Anexo I ficou como placeholder (print não embutido) — pendente de substituição manual antes da exportação final para PDF/assinatura.
- Citação de prazos (24h, 1/2/3 dias) não teve dupla checagem jurídica formal além da leitura em fonte primária feita pelo agente `vigilancia-regulatoria` nesta sessão — registrado como nota de revisão interna (não impressa) dentro do próprio Artifact.

## O que mudaria a decisão

- Se a correção da supressão de marketing não estiver de fato completa em produção (ex.: cobre e-mail mas não WhatsApp/SMS), o texto do item 4 ficaria overclaiming e precisaria ser revisto antes do envio.
- Se o jurídico apontar erro nas citações de artigo/portaria, a Nota de Revisão do próprio Artifact já sinaliza os pontos a confirmar.

## Impacto

- **Produto**: módulo Responsible Gaming / Jogo Responsável, Tradicional.
- **Processo**: reforça o padrão de rodar apuração multi-fonte (claude-os + DOU + ClickUp) antes de redigir qualquer conteúdo com peso legal, e de tratar decisões desse tipo como bloqueantes para o PM, não para o agente decidir sozinho.

## Links

- Artifact publicado: https://claude.ai/code/artifact/708299a2-d7d4-4c20-9bff-93d5a28e6b9b
- Modelo/precedente (relatório PROCON-SP): https://claude.ai/code/artifact/46300eac-bb2f-4c28-ba24-ea72215db83a
- Ofício PROCON/SC: nº 392/2026/SSP/PROCON/COAM, Processo SGPE SSP 00030437/2026
- Incidente considerado e desconsiderado por instrução do PM: ClickUp VL-13295 / 868kdn5gp
- Memória corrigida: [[sigap-integracao-vertical]]
