# Pausar o "Indique & Ganhe" em produção por falha de integração com a Smartico (não regulatório)

**Data**: 2026-08-17
**Tomada por**: Ithalo Mendes (PM)
**Status**: APROVADA

---

## Contexto

Foram percebidas falhas na integração entre o PAM e a Smartico que estão impedindo visibilidade de dados para suporte e CRM sobre o "Indique & Ganhe", e a operação ainda não confirmou que as automações de bônus da feature estão corretas. Esta é a **terceira mudança de estado** dessa feature em menos de um mês, mas por um motivo diferente das duas anteriores:

- 30/07: desativada por vedação regulatória (Art. 42, Portaria 1.231/2024) — ver [2026-07-30-ocultar-indique-e-ganhe-vedacao-regulatoria.md](2026-07-30-ocultar-indique-e-ganhe-vedacao-regulatoria.md)
- 06/08: reativada após adequação (bônus só ao indicante) — ver [2026-08-06-reativacao-indique-e-ganhe-apos-adequacao.md](2026-08-06-reativacao-indique-e-ganhe-apos-adequacao.md)
- 17/08 (esta decisão): pausada de novo, agora por motivo **técnico/operacional**, não regulatório

## Opções Consideradas

1. **Manter ativo em produção enquanto se corrige a integração** — não interromper o fluxo do usuário.
   - Prós: nenhuma perda de canal de aquisição.
   - Contras: suporte e CRM seguem sem visibilidade de dados; risco de bônus processado incorretamente sem que ninguém perceba.

2. **Pausar apenas o botão em produção (mitigação de front), mantendo alpha 100% ativo para testes** — trocar o layout da tela, desabilitar o botão de indicação e mostrar aviso amigável, sem mexer em mecânica/backend/Smartico.
   - Prós: simples de executar (mudança só de front); permite ao time (produto + operação) validar dados e automações em alpha sem afetar produção; reversível sem novo deploy (toggle por ambiente).
   - Contras: histórico de indicações pendentes fica com sua garantia limitada (só cobre o que já foi processado/pago); links de indicação já compartilhados antes da mudança podem continuar completando indicações por trás via Smartico, mesmo com o botão desabilitado na tela — risco residual aceito conscientemente.

## Decisão

Optou-se pela **Opção 2 — pausar apenas o botão em produção**. Escopo é estritamente front-end: desabilitar o botão de ação (ícone de cadeado, texto "Disponível em breve"), exibir aviso "Estamos melhorando o Indique e Ganhe" com duas linhas ("Novas indicações estão pausadas por enquanto" / "Suas indicações anteriores continuam valendo"), e manter a seção "Amigos Indicados" (histórico) visível e funcional sem alteração. Em **alpha a feature continua 100% ativa** — é lá que o time testa em conjunto: mapeamento de dados, automações de bônus, visibilidade para suporte/CRM.

Não há data fixa de reversão — a condição de saída é a validação em alpha ser concluída com sucesso.

## Trade-offs Aceitos

- A frase "Suas indicações anteriores continuam valendo" garante apenas indicações já processadas/pagas com sucesso, não as pendentes cujo bônus ainda depende da automação em validação (confirmado explicitamente pelo PM).
- Links de indicação já compartilhados antes da mudança podem continuar completando indicações por trás via Smartico, mesmo com o botão desabilitado na tela. O PM decidiu conscientemente que mitigar só a UI é suficiente por agora, sem exigir bloqueio técnico adicional nesta rodada.
- Por decisão explícita do PM, **não foi aberto um card de Bug/Correção para a causa raiz** da falha de integração nesta rodada — ficou fora de escopo. **Achado relevante durante a execução**: já existem tickets abertos que podem ser essa causa raiz — `868kr2mtc` ("URGENTE - Problemas com Indique e Ganhe") e `868kqxt8u` ("Problema Smartico", descrição vazia) — nenhum foi vinculado ou investigado; vale o PM checar se `868kr2mtc` é de fato o problema descrito aqui antes de considerar o rastreamento da causa raiz encerrado.

## O que mudaria a decisão

- Confirmação de que `868kr2mtc` é a mesma falha e já está sendo tratada — mudaria a necessidade de abrir um card de causa raiz separado.
- Validação em alpha concluída (dados mapeados, automações de bônus corretas, visibilidade para suporte/CRM confirmada) — dispara a reversão desta pausa.
- Evidência de que o risco residual aceito (links antigos completando por trás) está gerando volume relevante — reabriria a discussão sobre bloqueio técnico adicional.

## Impacto

- **Produto**: Indique & Ganhe (Hub de Benefícios / Banca de Benefícios). Botão pausado em produção; alpha inalterado.
- **Técnico**: mudança de front-end apenas (tela "Indique e Ganhe", mobile e desktop); toggle por ambiente (mecanismo exato deixado como "❓ Aberto para refinamento técnico" — flag de sistema, env var ou config de conteúdo, a decidir pela engenharia). Sem alteração de mecânica de bônus, backend ou configuração da Smartico.
- **Processo**: card criado direto na lista Execução, pulando Backlog — mesmo padrão de fast-track usado nos dois episódios anteriores desta feature por serem mitigações urgentes.

## Links

- Card no ClickUp: [868kt2hdd](https://app.clickup.com/t/868kt2hdd) — Pausar o botão do Indique e Ganhe em produção até validar a integração com a Smartico
- Protótipo Figma: https://www.figma.com/design/YAQI935WEFUyEyDzYFX9GP/PAM---Banca-de-Beneficios?node-id=1-92
- Feature original: [868kevfgr](https://app.clickup.com/t/868kevfgr) — Indique e Ganhe
- Episódio anterior (regulatório, revogado): [868kj1d89](https://app.clickup.com/t/868kj1d89) — Ocultar o Indique & Ganhe
- Episódio anterior (reativação): [868kmj13a](https://app.clickup.com/t/868kmj13a) — Atualização da Página do Indique e Ganhe
- Iniciativa: [868k8duqn](https://app.clickup.com/t/868k8duqn) — Hub de Benefícios (Portfólio de Projetos atualizado com os 4 cards da feature)
- Possível causa raiz não confirmada/não vinculada: [868kr2mtc](https://app.clickup.com/t/868kr2mtc) — "URGENTE - Problemas com Indique e Ganhe"; [868kqxt8u](https://app.clickup.com/t/868kqxt8u) — "Problema Smartico"
