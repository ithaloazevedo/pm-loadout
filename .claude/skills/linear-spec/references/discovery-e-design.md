# Discovery e Design no Linear Method

Como documentar projetos cujo escopo ainda será definido na fase de discovery e prototipação.

---

## O princípio fundamental

> **O Project não precisa ter escopo completo para existir.**
> Ele precisa ter problema claro e critérios de saída do discovery definidos como milestone.

O escopo aberto não é um bloqueio para criar o projeto — é o estado natural do discovery. O que muda é o *tipo* de documento que você cria: um **Projeto de Discovery**, não um Projeto de Delivery.

---

## Projeto de Discovery vs. Projeto de Delivery

| | Projeto de Discovery | Projeto de Delivery |
|--|----------------------|-----------------------|
| **Quando usar** | Escopo ainda indefinido | Direção de design validada |
| **Foco** | Problema, perguntas em aberto, critérios de saída | Escopo fechado, critérios de aceite detalhados |
| **Escopo** | O que sabemos que está *fora* | Dentro e fora bem definidos |
| **Critérios** | De saída do discovery (o que precisa estar respondido) | De aceite da entrega (binários e testáveis) |
| **Próximo passo** | Designer inicia exploração | Engenharia inicia build |

---

## Como o Designer cria as próprias issues

O Linear Method é direto: *"The designers file their own issues."*

O PM não cria issues para o Designer — cria o contexto (Projeto de Discovery), e o Designer quebra o trabalho conforme descobre. Issues típicas de discovery:

| Issue | Quando criar |
|-------|-------------|
| `Explorar direções de design para [funcionalidade]` | Início do discovery — espaço livre para explorar sem julgamento |
| `Escrever spec do projeto [nome]` | Quando PM precisa formalizar decisões e fechar escopo |
| `Validar protótipo com [usuários/stakeholder]` | Após exploração inicial, antes de escolher direção |
| `Design [tela X]` | Quando a direção está escolhida — tarefa concreta e fechada |
| `Alinhar handover com engenharia` | Antes de entrar em build |

A issue de exploração é intencionalmente aberta. O Linear Method orienta: *"Explore the solution freely and without judging whether something is feasible."* Isso é diferente de issues de build, que devem ser atômicas e fechadas.

---

## Estrutura de Milestones para projetos em discovery

Os milestones estruturam a transição entre fases, funcionando como portões de decisão:

```
Milestone 1: Validar direção de design    ← discovery termina aqui
             O que valida: decisão tomada, direção aprovada com stakeholders

Milestone 2: Spec aprovada para build     ← engenharia começa aqui
             O que valida: escopo fechado, critérios de aceite definidos

Milestone 3: [Entrega ou lançamento]      ← valor chegou ao usuário
```

**Por que isso funciona:** O PM e o Designer sabem exatamente quando o projeto muda de fase. A engenharia não começa sem a Milestone 2 estar completa. Não há ambiguidade sobre o que precisa acontecer antes de o build começar.

---

## Quando criar o Projeto de Delivery

Após o Milestone 1 (direção validada), use `/linear-spec promote [PROJ-ID]` para gerar o Projeto de Delivery a partir do Discovery:

1. O promote busca o conteúdo do Projeto de Discovery (objetivo, contexto, decisões)
2. Pré-preenche o template de Delivery com os dados disponíveis
3. Solicita apenas o que falta: critérios de aceite por área funcional, escopo fechado em linguagem de capacidade, Figma
4. Gera um Activity Update narrativo no Discovery e na Iniciativa associada

O Projeto de Discovery permanece no Linear como referência histórica — o Delivery é um projeto novo vinculado a ele.

---

## Erros comuns nesse fluxo

| Erro | Consequência |
|------|-------------|
| Esperar o escopo estar completo para criar o projeto | Discovery sem estrutura, sem milestone, sem contexto compartilhado |
| PM cria todas as issues do Designer | Designer não tem ownership, perde o raciocínio de quem entende o trabalho |
| Discovery sem milestone de saída | Não há critério claro para o projeto entrar em build — vira exploração infinita |
| Converter Discovery em Delivery sem validar com stakeholders | Escopo fecha errado, retrabalho no build |
| Issue de exploração com critérios rígidos | Bloqueia a liberdade criativa necessária no discovery |
