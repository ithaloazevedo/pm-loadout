# Header e bottom bar da reestilização Tradicional classificados como Épico, apesar do precedente do footer

**Data**: 2026-08-03
**Tomada por**: Ithalo Mendes
**Status**: APROVADA

---

## Contexto

Sequência da iniciativa de reestilização visual da Loteria Tradicional (mesma iniciativa do footer,
já em desenvolvimento — ver [[2026-07-30-footer-restyle-exclusivo-tradicional-tarefa]]). O PM pediu
diretamente a criação de dois novos itens de Delivery — header e bottom bar — como **Épicos**. A
pesquisa prévia no ClickUp levantou dois pontos que exigiam decisão antes de criar: (a) um ticket
legado aberto no espaço antigo Vertical Loto com o mesmo escopo do header (VL-4054, "Header Desktop
da Tradicional"), e (b) uma assimetria de classificação em relação ao footer, que foi decidido como
Tarefa pelo mesmo tipo de racional (restyle de componente existente, sem mudança de regra de
negócio).

## Opções Consideradas

1. **Tratar VL-4054 como base/dependência do novo Épico de header**
   - Prós: aproveitaria contexto de uma tentativa anterior.
   - Contras: ticket estava sem assignee há ~9 meses, sem confirmação de status real.

2. **Rebaixar Header para Tarefa, espelhando o footer** (mesmo perfil: restyle visual, sem lógica de
   negócio nova, sem elemento funcional novo)
   - Prós: consistência com o precedente e com o critério documentado em `processo.md`.
   - Contras: diverge da instrução explícita do PM, que já pediu "dois Épicos".

3. **Manter os dois como Épico, conforme pedido, sinalizando a assimetria** — escolhida.

## Decisão

O ticket legado VL-4054 foi confirmado pelo PM como **abandonado** — não é ponto de partida nem
referência de escopo para o novo Épico de header.

Header e bottom bar foram criados como **Épico** (`task_type: Epic`), por instrução explícita do PM:

- **Header** (`868kkacuy`) — pelo escopo hoje conhecido (restyle visual puro, sem elemento funcional
  novo, só preservar entradas de menu existentes), o perfil técnico é equivalente ao do footer, que
  foi classificado como Tarefa. A classificação como Épico não decorre de uma diferença objetiva de
  escopo, e sim da instrução direta do PM — fica sinalizado para reavaliação quando o Figma puder
  ser conferido (se confirmado restyle 1:1, considerar rebaixar para Tarefa).
- **Bottom bar** (`868kkad8x`) — tem diferença real de escopo que justifica Épico por critério
  próprio: introduz um item de navegação novo (Busca, sem destino funcional ainda) e uma regra de
  UI condicional (cor de fundo branca/azul variando por rota, cobrindo 6 páginas).

## Trade-offs Aceitos

- Header pode estar super-classificado frente ao precedente do footer — aceito conscientemente a
  pedido do PM; custo baixo de reverter (mudar `task_type` não tem efeito estrutural).
- Segue sem existir uma Iniciativa/Roadmap Item guarda-chuva formal para "reestilização visual da
  plataforma" — footer, header e bottom bar nascem como itens irmãos, conectados só por linked task
  (mesma lacuna já registrada na decisão do footer).

## O que mudaria a decisão

- Se o Figma do header (node `3341-52672`), quando aberto, confirmar que é restyle 1:1 sem nenhum
  elemento novo — revisitar e considerar rebaixar para Tarefa, alinhado ao footer.
- Se o volume de mudança technical do header se mostrar maior que uma sprint — mantém Épico e essa
  decisão fica só como registro histórico do racional.

## Impacto

- **Produto**: Header e Bottom bar (componentes de UI transversais) do produto Loteria Tradicional.
- **Técnico**: nenhum sistema novo — restyle de componentes existentes; bottom bar adiciona lógica
  de UI condicional (cor por rota) e um item de navegação sem destino funcional ainda.
- **Processo**: nenhuma mudança de processo; ambos seguem `template-delivery.md` padrão, no Backlog
  do folder Delivery: Plataforma.

## Links

- Header: https://app.clickup.com/t/868kkacuy
- Bottom bar: https://app.clickup.com/t/868kkad8x
- Footer (item irmão): https://app.clickup.com/t/868kj72ng
- Figma header: https://www.figma.com/design/V3snQyVaPq0iVFURUz5U2a/PAM---Homes?node-id=3341-52672
- Figma bottom bar: https://www.figma.com/design/V3snQyVaPq0iVFURUz5U2a/PAM---Homes?node-id=3341-52667
