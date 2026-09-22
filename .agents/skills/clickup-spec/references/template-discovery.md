# Template: Discovery — hoje é uma faixa de status dentro do Backlog, não um item separado

> ⚠️ **Modelo mudou em 2026-09-10.** Não existe mais "Projeto de Discovery" como item separado com folder e
> tipo de tarefa próprios (Pesquisa / Protótipo / Entrevista). O folder Discovery & Design e a lista Discovery
> (`901114029780`) foram **removidos do ClickUp** (ver `knowledge/domains/processo.md` e
> `knowledge/decisions/2026-09-10-migracao-esteira-continua-para-sprints-remocao-okr-e-discovery.md`).
> Descoberta hoje é uma **faixa de status dentro do próprio Backlog** de cada squad de Delivery — `em
> refinamento` → `pronto p/ design` → `em design` (ordem varia por squad, ver `clickup-config.md` → "Status
> por lista") — antes de `pronto p/ execução` → `priorizado`. Um item de Delivery nasce **direto no Backlog**,
> já com seu tipo final (`Epic`/`Tarefa`/`Bug`/`Correção`) — nunca mais um tipo "de descoberta" separado.
>
> O conteúdo abaixo (JTBD, Personas, Evidências, decisões de UX em aberto, critérios de saída) continua útil,
> mas hoje entra como **seções do 🧠 Contexto do card de Delivery** enquanto ele está na faixa de descoberta do
> Backlog — não como corpo de um item próprio. Use este arquivo como inventário de seções a incorporar no
> Contexto do Delivery (ver [template-delivery.md](template-delivery.md)), não como template de item
> independente. Os exemplos reais no fim do arquivo ficam só como ilustração histórica de como essas seções
> eram escritas quando Discovery ainda era um item à parte.

Cobre quatro frentes — **Design Ops, Pesquisa, Definição de Escopo e Prototipação** — e por natureza tem
**escopo orientado, não 100% fechado**: é esperado que a faixa de descoberta carregue decisões de UX em
aberto. As subtasks (UC1–UCn, edge cases, telas) são criadas pelo Designer conforme descobre.

## Princípio: template adaptativo (montar só o que faz sentido)

**Não despeje seções vazias nem invente conteúdo.** O Discovery monta o documento conforme o contexto e a
informação disponível:

- **Tem informação ou faz sentido no contexto?** → inclua a seção.
- **Aquela frente não aconteceu?** (ex: nenhuma pesquisa feita) → **omita** a seção (Evidências, JTBD, Personas, etc.). Seção vazia é pior que seção ausente.
- **Há dúvida, ou parece faltar algo relevante?** → **pergunte** antes de gerar, em vez de inventar ou deixar placeholder.

Só são **sempre presentes**: **Objetivo** e **Critérios de saída**. Todo o resto entra por relevância.

## Protótipo = Figma, sempre

Quando o Discovery envolve prototipação, o entregável é um **protótipo navegável no Figma** — nunca protótipo
HTML/código. O protótipo serve para **resolver as decisões de UX em aberto** e fechar o escopo antes de
promover para Delivery.

## Sub-tipos de Discovery (qual ênfase usar)

Não é mais um tipo de tarefa separado — é só uma forma de identificar qual ênfase de descoberta o card de
Delivery está passando enquanto está na faixa de status do Backlog. Enfatize as seções do Contexto que
importam para essa ênfase:

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

> **Sem bloco de cabeçalho.** Não repita Dono / Tipo no topo: o **Dono** é o assignee do card de Delivery e o
> **sub-tipo** (Pesquisa / Definição de Escopo / Prototipação / Design Ops) fica subentendido no **nome da
> tarefa**. Estas seções entram dentro do 🧠 Contexto do Delivery — não há mais um corpo de item próprio nem
> um bloco de cabeçalho separado para elas. **Espaçamento:** linha em branco só **entre** seções `###` —
> dentro de uma seção, sub-cabeçalhos em negrito colam nos bullets (sem linha em branco antes do sub-cabeçalho
> nem entre sub-blocos). Ver [estilo-redacao.md](estilo-redacao.md).

```markdown
### 🎯 Objetivo            (sempre)
[O que precisamos descobrir/decidir — 1-2 frases]

### 🧠 Contexto e Problema  (quase sempre)
[Narrativa do porquê real, em Problema → Impacto: o que torna isso não trivial, tensões, riscos, e o
indicador de negócio afetado (conversão, retenção, satisfação, operação). Ver
[estilo-redacao.md](estilo-redacao.md).]

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

### 🔗 Links                  (se houver)
- Figma (protótipo): [link]
- Pesquisa / board: [link]
```

**Como isso se aplica hoje:** estas seções entram dentro do 🧠 Contexto do card de Delivery enquanto ele está
na faixa de descoberta do Backlog (`em refinamento` → `pronto p/ design` → `em design`) — não há mais um item
ou status próprio de Discovery para elas viverem.

> **Próximo passo:** cumpridos os critérios de saída, o item avança de status dentro do próprio Backlog
> (`pronto p/ execução` → `priorizado`) e entra na Sprint ativa do squad no rito de Planejamento — não existe
> mais "promoção" para um item separado.

---

> Os dois exemplos abaixo foram escritos quando Discovery ainda era um item separado, com seu próprio corpo e
> Links (inclusive o vínculo "Roadmap Item", nível também removido em 2026-09-10). Ficam como ilustração
> histórica de como redigir bem cada seção — hoje elas entrariam dentro do Contexto do Delivery correspondente.

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
