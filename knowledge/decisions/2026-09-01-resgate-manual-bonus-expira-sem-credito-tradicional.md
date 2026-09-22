# Bônus com resgate manual expira sem crédito, e o escopo nasce só na Tradicional

**Data**: 2026-09-01
**Tomada por**: Ithalo Mendes (PM)
**Status**: APROVADA

---

## Contexto

O backoffice está habilitando a concessão de bônus com fluxo de resgate **manual** (subtask `868ky5cjf`,
branch `feature/add-fluxo-bonus-manual`, Alex — já em `teste dev`, dentro de `868kx9wv0` "Ajustes na view
de bônus"). Quando esse fluxo estiver em produção, o bônus concedido pela Smartico chega na tabela
`WebBonusEntities` com status `"P"`.

A plataforma hoje não exibe nem sabe creditar esse status: o bônus seria concedido e o jogador nunca o
veria. Faltava o card do lado da Plataforma. Ícaro (Tech Lead de Backoffice & Integrações) apontou que o
resgate na plataforma precisa de fila para o volume de requisições não derrubar o fluxo.

Duas decisões de produto precisavam ser fechadas antes de o card existir: até onde vai o escopo (casas) e
o que acontece com um bônus pendente que o jogador não resgata.

## Opções Consideradas

**Escopo por casa**

1. **Só Tradicional** — card único mirando `micro-api` + `plataforma-nuxt` da Tradicional.
   - Prós: escopo fechado, acompanha o ritmo do backoffice que já está em teste.
   - Contras: réplica na Bravo vira trabalho separado depois.
2. **Tradicional e Bravo** — subtask por casa, cobrindo `micro-api` e `micro-api-bravo`.
   - Prós: paridade de uma vez.
   - Contras: dobra o escopo sem que a ativação manual esteja confirmada na Bravo.

**Destino do bônus pendente não resgatado**

1. **Auto-resgate de segurança** — expira a validade, o sistema credita sozinho e avisa.
   - Prós: jogador ganha o pico emocional do resgate ativo sem que a casa crie mecanismo de perda.
   - Contras: enfraquece o incentivo de retorno; é justamente o que o resgate manual busca criar.
2. **Expira sem crédito** — não resgatou dentro da validade, perde.
   - Prós: preserva o gatilho de retorno diário, que é a tese do resgate manual.
   - Contras: risco de suporte e reputação — o próprio card de cashback (`868kt4t1j`) marca isso como
     "o principal ponto a resolver antes do build".
3. **Sem prazo** — fica pendente indefinidamente.
   - Prós: build mais simples.
   - Contras: acumula passivo de bônus não resgatado no balanço.

## Decisão

**Escopo: apenas Tradicional.** Bravo, se vier, é card próprio — mesmo padrão já usado em
[[2026-07-30-footer-restyle-exclusivo-tradicional-tarefa]].

**Bônus pendente expira sem crédito**, sem auto-resgate de segurança. O fator decisivo foi preservar o
gatilho de retorno: um benefício que o jogador precisa buscar dentro de um prazo é o mecanismo de DAU que
o resgate manual existe para criar; creditar sozinho ao fim do prazo devolve o comportamento ao crédito
automático que se quer sair.

Como consequência direta, duas mitigações entraram como **requisito obrigatório de escopo**, não como
opcional: prazo para resgatar sempre visível no card do bônus, e aviso ao jogador antes de expirar.

**Tipo: Tarefa com subtasks**, no Backlog do folder Delivery: Plataforma. Escopo cabe numa sprint e
acompanha o backoffice, que já está em teste dev.

## Trade-offs Aceitos

Aceita-se conscientemente o risco de suporte e reputação de um jogador perder benefício por não resgatar.
A decisão foi tomada com esse risco na mesa, não por omissão. As mitigações (prazo visível, aviso
pré-expiração) reduzem mas não eliminam o risco.

Aceita-se também que a Bravo fique atrás na paridade dessa funcionalidade.

## O que mudaria a decisão

- Volume de chamados de suporte com o tema "perdi meu bônus" após o lançamento.
- Percentual de bônus concedidos que expiram sem resgate: se for alto, a casa está pagando o custo da
  concessão sem comprar engajamento — mesma armadilha já diagnosticada no cashback creditado
  automaticamente.
- Parecer de compliance sobre o enquadramento de benefício com prazo de perda (não consultado até aqui —
  não foi identificado gatilho regulatório, mas não houve avaliação formal).

## Impacto

- **Produto**: Banca de Benefícios → tela "Meus Bônus" (aba Disponíveis) ganha estado de bônus pendente
  de resgate. Cria precedente de regra de expiração que conflita com o auto-resgate proposto para o
  cashback em `868kt4t1j` — precisa de regra única antes de os dois irem a produção.
- **Técnico**: `plataforma-nuxt` (front), `ws-plataforma` / `micro-api` (backend Tradicional),
  `WebBonusEntities` status `"P"`. Fila de processamento do resgate, evoluindo o advisory lock já
  aplicado em `868kuv3fa` / `868kuw24m`.
- **Processo**: nenhuma mudança.

## Links

- Card no ClickUp: https://app.clickup.com/t/868kzfp3d — Resgate manual de bônus na Banca de Benefícios
- Dependência (concessão com fluxo manual, backoffice): https://app.clickup.com/t/868ky5cjf
- Tarefa pai do backoffice: https://app.clickup.com/t/868kx9wv0
- Mesmo padrão de resgate manual, aplicado a cashback: https://app.clickup.com/t/868kt4t1j
