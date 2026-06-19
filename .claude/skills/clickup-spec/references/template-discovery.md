# Template: Projeto de Discovery

Vive no folder **Product Discovery** (lista `Design`). Cobre quatro frentes — **Design Ops, Pesquisa,
Definição de Escopo e Prototipação** — e por natureza tem **escopo orientado, não 100% fechado**: é esperado
que carregue decisões de UX em aberto. As subtasks (UC1–UCn, edge cases, telas) são criadas pelo Designer
conforme descobre.

## Princípio: template adaptativo (montar só o que faz sentido)

**Não despeje seções vazias nem invente conteúdo.** O Discovery monta o documento conforme o contexto e a
informação disponível:

- **Tem informação ou faz sentido no contexto?** → inclua a seção.
- **Aquela frente não aconteceu?** (ex: nenhuma pesquisa feita) → **omita** a seção (Evidências, JTBD, Personas, etc.). Seção vazia é pior que seção ausente.
- **Há dúvida, ou parece faltar algo relevante?** → **pergunte** antes de gerar, em vez de inventar ou deixar placeholder.

Só são **sempre presentes**: **Objetivo**, **Critérios de saída** e o **vínculo com o Roadmap Item** (na seção 🔗 Links). Todo o
resto entra por relevância.

## Protótipo = Figma, sempre

Quando o Discovery envolve prototipação, o entregável é um **protótipo navegável no Figma** — nunca protótipo
HTML/código. O protótipo serve para **resolver as decisões de UX em aberto** e fechar o escopo antes de
promover para Delivery.

## Sub-tipos de Discovery (qual ênfase usar)

Deixe o sub-tipo subentendido no **nome da tarefa** e enfatize as seções que importam para ele:

| Sub-tipo | Pergunta central | Seções que costumam importar |
|----------|------------------|------------------------------|
| **Pesquisa** | "O que precisamos aprender sobre o usuário/problema?" | Personas, JTBD, Evidências & Pesquisa, Questões em aberto |
| **Definição de Escopo** | "O que entra e o que fica de fora?" | Contexto, Restrições, Escopo orientado, Critérios de saída |
| **Prototipação (Figma)** | "Como validamos a solução e fechamos as decisões de UX?" | Prototipação (Figma), Decisões de UX em aberto, JTBD/Personas (se houver) |
| **Design Ops** | "Que processo/sistema de design precisamos organizar?" | Objetivo, Contexto, Critérios de saída (mais enxuto) |

> Um Discovery pode combinar frentes (ex: Pesquisa + Prototipação). Use o bom senso: inclua as seções das frentes que de fato aconteceram.

---

## Template (montagem condicional)

Seções marcadas com *(sempre)* são obrigatórias; as demais entram **apenas se** houver informação/relevância.

> **Sem bloco de cabeçalho.** Não repita Roadmap Item / Dono / Tipo no topo: o **Dono** é o assignee da task,
> o **sub-tipo** (Pesquisa / Definição de Escopo / Prototipação / Design Ops) fica subentendido no **nome da
> tarefa**, e o **vínculo com o Roadmap Item** vai na seção 🔗 Links. O corpo começa direto no `### 🎯 Objetivo`.
> **Espaçamento:** linha em branco só **entre** seções `###`.

```markdown
### 🎯 Objetivo            (sempre)
[O que precisamos descobrir/decidir — 1-2 frases]

### 🧠 Contexto e Problema  (quase sempre)
[Narrativa do porquê real: o que torna isso não trivial, tensões, riscos]

### 👤 Personas / público-alvo   (se houver recorte de persona relevante)
[Quem é afetado e a característica que muda o design. Omita se não há recorte claro.]

### 🎯 Jobs to be Done       (se ajudar a enquadrar a solução)
["Quando [situação], quero [motivação], para [resultado]" — funcional / emocional / social. Só se agrega clareza.]

### 🔬 Evidências & Pesquisa  (somente se houve pesquisa/dados)
[Dados de funil, entrevistas, suporte, analytics. **Se nada foi pesquisado, omita a seção inteira.**]

### 📋 Restrições conhecidas  (se houver)
🚫 **Fora:** [o que a solução não pode/não deve fazer]

### 🎨 Prototipação (Figma)   (obrigatória quando o sub-tipo é Prototipação)
- **Protótipo (Figma):** [link ou "a produzir"]
- **O que o protótipo precisa validar:** [hipótese/experiência a testar]

### ❓ Decisões de UX em aberto  (típico de Prototipação / Definição de Escopo)
- [ ] [decisão de UX que o protótipo/discovery precisa fechar antes do Delivery]

### 🔍 Questões em aberto      (se houver)
- [ ] [o que o discovery ainda precisa responder]

### ✅ Critérios de saída      (sempre)
Para avançar para Delivery:
- [ ] Decisões de UX em aberto resolvidas
- [ ] Escopo fechado (dentro e fora definidos)
- [ ] Direção validada com [stakeholder]
- [ ] Spec de Delivery aprovada

### 🔗 Links                  (Roadmap Item sempre; demais se houver)
- Roadmap Item: [Nome — link VL-XXXXX]
- Figma (protótipo): [link]
- Pesquisa / board: [link]
```

**Status inicial:** `to do`. **Vínculo:** linked task com o Roadmap Item pai — e **espelhe no 🗂️ Portfólio do Roadmap Item**.

> **Próximo passo:** cumpridos os critérios de saída, use `/clickup-spec promote VL-XXXXX` para gerar o Delivery.

---

## Exemplo Real 1 — Definição de Escopo + Pesquisa (sem prototipação)

> Mostra o template adaptativo: tem **Evidências** fortes (dados de funil), então a seção entra; **não** tem
> seção de Prototipação nem JTBD formal porque não agregavam ao caso.

### 🎯 Objetivo
Redesenhar o fluxo de KYC para que ocorra de forma obrigatória e linear no onboarding, reduzindo o abandono
de 51,4% na etapa de verificação e elevando a conversão Cadastrado → Verificado de 48,6% → 70%.

### 🧠 Contexto e Problema
O funil (01–03/jun/2026) mostra que de 3.356 pré-cadastros chegamos a apenas 925 depositantes (30,7%). O
gargalo está na verificação (KYC): de 3.012 cadastrados, só 1.464 ficam verificados (queda de 51,4%); as
demais etapas têm drop < 2%.

### 🔬 Evidências & Pesquisa
**Dado crítico:** 95,22% abandonam ao abrir a tela de captura de documento. **Causa raiz:** uma mudança
recente desacoplou o KYC do onboarding — sem KYC obrigatório no funil, o usuário não tem urgência e não
retorna.

### 📋 Restrições conhecidas
🚫 **Fora:**
- Eliminar o KYC — obrigação regulatória
- Incentivar com promoções
- Ignorar o fluxo Serasa

### 🔍 Questões em aberto
- [ ] Como funciona o Serasa no mobile com QR code? (80% dos usuários são mobile)

### ✅ Critérios de saída
- [ ] Fluxo linear obrigatório definido (Pré-cadastro → Telefone → Email → KYC → Depósito)
- [ ] Fluxo desenhado para UC1, UC2, UC3 (ver subtasks) + edge cases mapeados
- [ ] Comportamento do Serasa no mobile validado
- [ ] Direção validada com stakeholders (PO, Tech Lead, Compliance)
- [ ] Spec de Delivery aprovada

### 🔗 Links
- Roadmap Item: Otimizar o onboarding com KYC para elevar a conversão Cadastro → FTD — VL-11852
- FigJam: https://www.figma.com/board/4xRhTCwXpvDc6B7iweVIQl/Onboarding

---

## Exemplo Real 2 — Prototipação (Figma), escopo orientado

> Mostra um Discovery de **Prototipação**: escopo orientado mas não fechado, com **JTBD**, **Personas** e
> **Decisões de UX em aberto** que o protótipo Figma precisa resolver. Não inventa Evidências porque a
> pesquisa ainda não foi feita — a seção é omitida.

### 🎯 Objetivo
Prototipar no Figma o loop de hábito do Hub de Benefícios Gamificado (sequência diária → chances → recompensa
com regra clara) para validar a experiência com o público 34–54 e fechar as decisões de UX antes do build.

### 🧠 Contexto e Problema
A Banca de Benefícios hoje fica escondida atrás de um ícone pequeno e o valor de fidelização não é capturado.
A aposta é transformá-la num Clube de Benefícios gamificado, destacado, que dê motivo para voltar todo dia —
nascendo compliant (Lei 14.790): a pressão de streak é sobre *visitar*, nunca *apostar*.

### 👤 Personas / público-alvo
~70% da base tem 34–54 anos, mobile-first. Tom: clube/benefícios, mecânicas familiares e de alto valor
percebido — sem linguagem gamer pesada ou infantilizada.

### 🎯 Jobs to be Done
- **Funcional:** "Quando entro na plataforma, quero ver rapidamente o que ganho hoje, para sentir que vale a pena voltar."
- **Emocional:** "Quero sentir que sou reconhecido como cliente fiel, sem pressão para apostar."

### 🎨 Prototipação (Figma)
- **Protótipo (Figma):** a produzir — "Plataforma - Tradicional", node 20417-39943 (Banca de Benefícios)
- **O que o protótipo precisa validar:** se o loop streak→chances→recompensa é claro e gera retorno diário sem ser lido como "mais um jogo".

### ❓ Decisões de UX em aberto
- [ ] Streak diário rígido vs. consistência semanal (X de 7) para adultos com rotina
- [ ] "Check-in" = só abrir o hub ou ação ativa (toque)?
- [ ] Enquadramento visual de roleta/raspadinha como benefício de fidelidade (não como produto de aposta)

### ✅ Critérios de saída
- [ ] Decisões de UX em aberto resolvidas no protótipo
- [ ] Loop validado com stakeholders e amostra do público 34–54
- [ ] Escopo v1 fechado (módulos dentro/fora) e spec de Delivery aprovada

### 🔗 Links
- Roadmap Item: Hub Gamificado — VL-11857
- Figma (protótipo): a produzir
- PRD: https://docs.google.com/document/d/1XzCgxZloqCV6ukKYOimT8UUJ-vv91O83RfLwJtv851I/edit
