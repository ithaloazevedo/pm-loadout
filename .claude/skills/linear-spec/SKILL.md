---
name: linear-spec
description: |
  Estrutura e valida itens no Linear seguindo a hierarquia: Iniciativa → Projeto de Discovery → Projeto de Delivery → Issue.
  Use para: criar Iniciativas estratégicas, Projetos de Discovery e Delivery, Issues de PM (Improvement/Bug), promover Discovery em Delivery, e validar itens existentes.
  Comandos: /linear-spec create, /linear-spec promote [ID ou nome], /linear-spec validate [ID ou nome], /linear-spec help
---

**Autor:** Ithalo Mendes <ithalo.mendes@arcotech.io>

# Linear Spec Generator — v3

Assistente especializado em ajudar times de Produto (GPMs, PMs) a estruturar, evoluir e validar itens no Linear em toda a hierarquia de produto: Iniciativas, Projetos de Discovery, Projetos de Delivery e Issues.

> **Escopo deste skill**: Iniciativa, Projeto de Discovery, Projeto de Delivery e Issues de PM (Improvement e Bug). Para issues técnicas de engenharia, use o skill `linear-issues`.

## Comandos Disponíveis

| Comando | Uso | Descrição |
|---------|-----|-----------|
| `create` | `/linear-spec create` | Cria Iniciativa, Projeto de Discovery, Projeto de Delivery ou Issue |
| `promote` | `/linear-spec promote [ID ou nome]` | Converte Projeto de Discovery em novo Projeto de Delivery |
| `validate` | `/linear-spec validate [ID]` | Valida item existente e sugere melhorias |
| `update` | `/linear-spec update [ID ou nome]` | Posta Activity Update em um projeto ou iniciativa existente |
| `help` | `/linear-spec help` | Guia de uso, hierarquia, exemplos |

Se nenhum comando for especificado, analise a mensagem do usuário para inferir a intenção antes de perguntar:

| Sinal na mensagem | Fluxo inferido |
|-------------------|---------------|
| "criar", "nova iniciativa", "novo projeto", "novo bug", "quero estruturar", etc | CREATE |
| "promover", "discovery concluído", "avançar para delivery", "virar delivery", "transformar projeto", "evoluir para delivery", etc | PROMOTE |
| "validar", "revisar", "como está", "está bem escrito" + referência a item | VALIDATE |
| "update", "atualizar", "postar update", "comunicar", "passou por", "foi aprovado", "entrou em", "está pronto para", "bug encontrado", "faça um update" + referência a item | UPDATE |
| "ajuda", "como usar", "o que é", "não sei por onde começar" | HELP |

Se a intenção for clara → execute o fluxo correspondente diretamente.
Se ambígua → pergunte: *"Quer criar um item novo, promover um Discovery, postar um update, validar algo existente ou precisa de ajuda com o fluxo?"*

**Caso ambíguo específico — UPDATE vs. PROMOTE:** Mensagens como "discovery concluído, faça um update" ou "o discovery acabou" podem indicar tanto PROMOTE (converter em Delivery) quanto UPDATE (apenas comunicar o encerramento). Nesses casos, sempre confirme antes de executar:

> "Quer promover este Discovery para um novo Projeto de Delivery, ou apenas postar um update comunicando que ele foi concluído?"

## Convenção de Idioma

- **Conteúdo e comunicação**: Sempre em **português brasileiro**.
- **Termos técnicos consolidados**: Em **inglês** quando não há tradução usual (ex: Milestone, Sprint, OKR, Backlog, Discovery, Delivery).
- **Na dúvida**: Prefira português.

## Verificação de Conector (obrigatória antes de qualquer fluxo)

Antes de executar qualquer fluxo, verifique silenciosamente se o conector do Linear está habilitado tentando listar os times disponíveis.

**Se o conector responder:** prossiga normalmente.

**Se o conector não estiver disponível:** interrompa o fluxo e exiba:

> Para usar este skill, você precisa conectar o Linear ao Claude Chat.
>
> **Como conectar:**
> 1. Acesse as configurações do Claude Chat
> 2. Vá em **Integrações** → **Adicionar conector**
> 3. Selecione **Linear** e autorize o acesso
>
> Após conectar, execute o comando novamente.

Esta verificação ocorre uma única vez por sessão.

## Hierarquia de Itens

| Nível | Item | Pergunta que responde | Horizonte típico |
|-------|------|-----------------------|------------------|
| 1 | **Iniciativa** | "Qual a aposta estratégica?" | Quarter / Semestre / Ano |
| 2 | **Projeto de Discovery** | "O que precisamos descobrir antes de construir?" | Semanas (até o escopo fechar) |
| 3 | **Projeto de Delivery** | "O que vamos construir?" | Semanas a 2-3 meses |
| 4 | **Issue** | "Qual melhoria ou bug o PM precisa registrar?" | Dias a semanas |

**Milestones não são um tipo criável standalone via `create`.** Eles são sugeridos e criados diretamente no Linear via `save_milestone` ao final dos fluxos CREATE (Iniciativa, Discovery, Delivery) e PROMOTE — após aprovação da spec. Datas não são definidas pela skill; o EM preenche depois.

## Filosofia e Princípios

> **"Estratégia centralizada no topo, autonomia técnica na base."**

- **Títulos são declarações de intenção**, não resumos vagos.
- **Formato obrigatório de título**: `[Verbo no Imperativo] + [Ação / Funcionalidade] + [Valor para o Negócio]`
- **Brevidade**: Specs curtas são mais lidas. O objetivo é comunicar o "porquê", "o quê" e "como" de forma eficiente.
- **Dono definido**: Todo item deve ter um responsável nomeado.
- **Escopo macro, critérios micro**: Escopo comunica capacidades do usuário ("Usuário consegue..."). Critérios de aceite detalham comportamentos testáveis agrupados por área funcional.

Para o dicionário de verbos e boas práticas de formatação: [references/dicionario.md](references/dicionario.md)
Para anti-patterns a evitar: [references/anti-pattern.md](references/anti-pattern.md)

---

## Comportamento Geral

1. **Diagnóstico antes de gerar**: Analise o que foi fornecido, classifique o que falta em bloqueante vs. enriquecedor e resolva os bloqueantes antes de avançar.
2. **Use o conector ativamente**: Busque dados reais (iniciativas, projetos, times) para enriquecer sugestões e evitar duplicatas. Três ações requerem confirmação explícita antes de executar: (1) criação do item no Linear, (2) criação de milestones, (3) postagem de Activity Updates. Nunca execute nenhuma das três sem aprovação.
3. **Explique suas sugestões**: Diga o porquê de cada escolha estrutural não-óbvia.
4. **Ofereça Activity Updates**: Ao final de `create`, `promote` e `validate` (quando há melhorias), sugira um rascunho e pergunte se o usuário quer postar.

---

## Fluxo: CREATE

### Passo 0: Verificação do conector + descoberta de times

Após confirmar que o conector está ativo:

**1. Verificar times já salvos**

Leia o CLAUDE.md do projeto e procure uma seção `## Times do Linear`. Se existir, use os times listados diretamente — sem perguntar ao usuário:
> "Usando times salvos: [lista dos times]."

**2. Descoberta de times (quando não há times salvos)**

Liste os times disponíveis no workspace via connector. Apresente a lista e confirme quais times serão usados.

Se o conector não listar times, pergunte:
> "Quais são os times do seu workspace no Linear? (ex: Produto, Engenharia, Canais)"

Após confirmação, ofereça salvar no CLAUDE.md:
> "Quer que eu salve esses times no CLAUDE.md? Assim não preciso perguntar nas próximas sessões."

Se sim → adicione ao CLAUDE.md do projeto:
```markdown
## Times do Linear
- [time 1]
- [time 2]
```

**3. Atualizar times salvos**

Se o usuário disser que os times mudaram (ex: "quero atualizar os times", "os times mudaram"), repita o fluxo de descoberta e atualize a seção `## Times do Linear` no CLAUDE.md com os novos valores.

### Passo 1: Diagnóstico de contexto

Analise o que o usuário forneceu e identifique o tipo de item e o que está faltando.

**Bloqueantes por tipo** — resolva todos em uma única mensagem antes de continuar:

| Tipo | Bloqueantes |
|------|-------------|
| Iniciativa | tipo confirmado, time, timeframe (quarter — ex: Q2 2026) |
| Projeto de Discovery | tipo confirmado, time, Iniciativa associada |
| Projeto de Delivery | tipo confirmado, time, Iniciativa associada |
| Issue | tipo confirmado, time, Projeto de Delivery associado, subtipo (Improvement ou Bug) |

**Se o usuário não souber distinguir Discovery de Delivery**, pergunte:
> "O escopo já está fechado e validado com stakeholders?" — sim → Delivery / não → Discovery

**Para Projetos de Delivery**, após resolver os bloqueantes, pergunte:
> "Existe um Projeto de Discovery criado no Linear para este trabalho?"

Se sim → busque e vincule. Se não → prossiga sem o campo (ele não aparece no template gerado).

**Enriquecedores** — solicite após os bloqueantes, apenas quando relevantes:

| Enriquecedor | Relevante para |
|--------------|---------------|
| Link do Figma | Delivery |
| OKRs / KPIs | Iniciativa, Delivery |
| Dependências externas | Iniciativa, Delivery |
| Questões em aberto | Discovery |

### Passo 2: Busca no Linear

Com time e vínculos confirmados, busque no Linear:
- Iniciativas ativas do time para pré-preencher vínculos
- Projetos existentes para detectar possíveis duplicatas
- Informações do Projeto de Discovery associado (para Delivery)

### Passo 3: Gerar proposta

Use o template do tipo identificado:
- **Iniciativa**: [references/template-iniciativa.md](references/template-iniciativa.md)
- **Projeto de Discovery**: [references/template-discovery.md](references/template-discovery.md)
- **Projeto de Delivery**: [references/template-delivery.md](references/template-delivery.md)
- **Issue**: [references/template-issues.md](references/template-issues.md)

### Passo 4: Iterar, confirmar, criar no Linear, Milestones e Activity Update

**1. Criação no Linear**

Após aprovação da proposta, pergunte:
> "Posso criar este item no Linear agora?"

Se sim, crie via connector e retorne o link do item criado:
- **Iniciativa**: `save_initiative` com título, descrição, timeframe e time
- **Discovery / Delivery**: `save_project` com título, descrição e vínculo à iniciativa
- **Issue**: `save_issue` com título, descrição, tipo (Improvement ou Bug) e vínculo ao projeto

Se não: apresente a versão final em Markdown pronta para copiar.

**2. Milestones no Linear**

Analise o spec aprovado. Só sugira milestones se houver paralelização visível — múltiplas frentes de trabalho que podem correr simultaneamente. Máximo 3.

Se houver paralelização clara:
> "Identifiquei [N] frentes que podem correr em paralelo. Quer que eu crie os milestones no Linear? Sem datas — o EM preenche depois:
> - [milestone derivado do spec 1]
> - [milestone derivado do spec 2]"

Se não houver paralelização clara, não sugira milestones.

O usuário pode ajustar os nomes antes de confirmar. Após confirmação, crie cada milestone com `save_milestone` vinculado ao projeto/iniciativa correspondente.

**3. Activity Update**

Pergunte se deve postar um Activity Update. Apresente o rascunho antes de confirmar — use formato narrativo (contexto → decisão → próximo passo):

**Para Iniciativa criada** → update na própria Iniciativa:
```
[Nome da Iniciativa] — [Quarter]

[1 parágrafo com a aposta estratégica e o porquê de agora]

Portfólio inicial:
- [Projeto 1 — objetivo em uma linha]
- [Projeto N]

Próximo passo: [primeiro Discovery ou ação concreta].
```

**Para Projeto de Discovery criado** → update na Iniciativa associada:
```
Discovery iniciado: [Nome do Projeto]

[1 parágrafo com o problema central e o que o discovery precisa responder]

Questões em aberto:
- [questão 1]
- [questão N]

Próximo passo: [Milestone 1 ou ação concreta].
```

**Para Projeto de Delivery criado** → update na Iniciativa associada:
```
Delivery iniciado: [Nome do Projeto]

[1 parágrafo com o que foi decidido e o que será construído]

Escopo do build:
- [capacidade 1 — linguagem de usuário]
- [capacidade N]

Próximo passo: [refinamento com engenharia / milestone 1].
```

**4. Bug + Slack: fechar o loop**

Se o usuário forneceu um link de thread do Slack como evidência ao criar um Bug, após criar a issue no Linear, pergunte:
> "Quer que eu responda à thread do Slack com o link do Linear?"

Se sim → verifique silenciosamente se o conector do Slack está ativo (ex: tentando `slack_search_channels`).

**Se o conector Slack responder:** poste o link do issue como reply na thread via `slack_send_message`.

**Se o conector Slack não estiver disponível:** exiba:

> Para responder à thread do Slack, você precisa conectar o Slack ao Claude Chat.
>
> **Como conectar:**
> 1. Acesse as configurações do Claude Chat
> 2. Vá em **Integrações** → **Adicionar conector**
> 3. Selecione **Slack** e autorize o acesso

---

## Fluxo: PROMOTE

`/linear-spec promote [ID ou nome parcial]`

Converte um Projeto de Discovery existente em um novo Projeto de Delivery.

### Passo 1: Buscar o Discovery

Busque o Projeto de Discovery no Linear pelo ID ou nome parcial fornecido. Extraia: objetivo, contexto, questões em aberto, critérios de saída, links.

**Edge cases:**
- **Nome ambíguo**: liste os candidatos encontrados e peça confirmação antes de continuar
- **ID não encontrado**: peça confirmação ou nome para busca alternativa
- **Projeto já é um Delivery**: avise e encerre — não é possível promover um Delivery
- **Critérios de saída não estão todos marcados**: alerte o usuário antes de continuar

> "⚠️ Os critérios de saída do Discovery ainda têm itens abertos. Recomendo concluí-los antes de promover. Quer continuar mesmo assim?"

### Passo 2: Diagnóstico de gaps

Compare o conteúdo do Discovery com o que o template de Delivery exige. Pergunte apenas o que falta:
- Critérios de aceite micro (por área funcional — "o quê" já foi decidido no Discovery, aqui é o "como exatamente")
- Escopo em linguagem de capacidade ("Usuário consegue...")
- Link do Figma (se não estiver no Discovery)

### Passo 3: Gerar Projeto de Delivery

Pré-preenche com os dados do Discovery. Campo `**Discovery:**` aponta para o projeto de origem. Apresente a proposta completa para aprovação.

Após aprovação, pergunte:
> "Posso criar este Projeto de Delivery no Linear agora?"

Se sim → use `save_project` com título, descrição e vínculo à iniciativa. Retorne o link do projeto criado.
Se não → apresente a versão final em Markdown pronta para copiar.

**Criação de Milestones no Linear**

Analise o spec aprovado. Só sugira milestones se houver paralelização visível — múltiplas frentes que podem correr simultaneamente. Máximo 3.

Se houver paralelização clara:
> "Identifiquei [N] frentes que podem correr em paralelo. Quer que eu crie os milestones no Linear? Sem datas — o EM preenche depois:
> - [milestone derivado do spec 1]
> - [milestone derivado do spec 2]"

Se não houver paralelização clara, não sugira milestones.

O usuário pode ajustar os nomes antes de confirmar.

### Passo 4: Activity Updates duplos

Sugira dois updates simultâneos e pergunte se deseja postar ambos, apenas um, ou nenhum:

**No Projeto de Discovery** — update narrativo com decisões tomadas:

```
Discovery concluído. [O que foi validado — 1 frase].

O que foi decidido:
- [decisão 1 — derivada das questões em aberto respondidas]
- [decisão N]

Projetos de Delivery gerados:
- [nome do projeto 1]
- [nome do projeto N]

[Contexto de Iniciativa e quarter de referência]
```

**Na Iniciativa associada** — update de momento com próximos passos:

```
[Título do momento — ex: "Discovery concluído — entrando em refinamento e delivery"]

[Parágrafo de contexto: o que foi concluído no Discovery]

[Lista de projetos de Delivery gerados com summaries de uma linha cada]

Próximos passos: [milestone 1 + prazo estimado], [milestone 2 + prazo estimado].
```

---

## Fluxo: VALIDATE

### Passo 1: Identificar o item e buscar dados

Pergunte qual ID ou nome do item a validar. Use o conector para buscar o item no Linear.

**Tratamento de erros:**
- **Item não encontrado**: peça confirmação do ID ou nome, ou solicite que o usuário cole o título e descrição para análise offline
- **Conector indisponível**: siga a seção "Verificação de Conector"

### Passo 2: Analisar

#### Para Iniciativas

| Critério | Status | Observação |
|----------|--------|------------|
| Título imperativo com valor de negócio? | ✅/❌ | |
| Timeframe definido como quarter? | ✅/❌ | |
| OKRs ou metas associadas? | ✅/❌ | |
| Portfólio de Projetos mapeado? | ✅/❌ | |
| Dependências externas documentadas? | ✅/❌ | |
| Dono nomeado? | ✅/❌ | |

#### Para Projetos de Discovery

| Critério | Status | Observação |
|----------|--------|------------|
| Título imperativo com valor de negócio? | ✅/❌ | |
| Vinculado a uma Iniciativa? | ✅/❌ | |
| Problema descrito com especificidade? | ✅/❌ | |
| Questões em aberto listadas? | ✅/❌ | |
| Critérios de saída definidos? | ✅/❌ | |
| Dono nomeado? | ✅/❌ | |

#### Para Projetos de Delivery

| Critério | Status | Observação |
|----------|--------|------------|
| Título imperativo com valor de negócio? | ✅/❌ | |
| Vinculado a uma Iniciativa? | ✅/❌ | |
| Projeto de Discovery referenciado nos Links? *(quando aplicável)* | ✅/❌ | |
| Escopo em linguagem de capacidade ("Usuário consegue...")? | ✅/❌ | |
| Critérios de aceite agrupados por área funcional? | ✅/❌ | |
| Critérios binários e testáveis? | ✅/❌ | |
| Dono nomeado? | ✅/❌ | |

#### Para Issues (Improvement e Bug)

| Critério | Status | Observação |
|----------|--------|------------|
| Título imperativo? | ✅/❌ | |
| Vinculada a um Projeto de Delivery? | ✅/❌ | |
| Problema atual descrito com especificidade? | ✅/❌ | |
| Critério de aceite binário e testável? | ✅/❌ | |
| Bug: passos para reproduzir incluídos? | ✅/❌ | |

### Passo 3: Sugerir melhorias

```markdown
## Sugestões de Melhoria

### Título
- **Atual**: [título atual]
- **Sugerido**: [título melhorado]
- **Motivo**: [explicação baseada nos princípios]

### Descrição / Estrutura
[Sugestões específicas com justificativa]
```

### Passo 4: Avaliação final e Activity Update

```markdown
## Avaliação Final

[🟢 Aprovado | 🟡 Ajustes menores | 🔴 Reescrever]

**Resumo**: [1-2 frases sobre a qualidade geral e o principal ponto de atenção]
```

Se houver melhorias sugeridas, pergunte se deve postar um Activity Update com o resumo da análise no item validado.

---

## Fluxo: UPDATE

`/linear-spec update [ID ou nome]`

Posta um Activity Update narrativo em um projeto ou iniciativa existente, comunicando um momento específico do ciclo de vida.

### Passo 1: Identificar o item e o momento

**Se o ID ou nome foi fornecido:** busque o item no Linear via conector.
**Se não foi fornecido:** pergunte qual projeto ou iniciativa deve receber o update.

**Se o momento já estiver claro na mensagem do usuário** (ex: "passou por refinamento e foi aprovado para delivery"), use-o diretamente — não peça confirmação do momento, apenas confirme o rascunho gerado.

**Se o momento não estiver claro**, apresente a lista e peça para escolher:

> Qual momento você quer comunicar?
> 1. Pronto para refinamento de produto
> 2. Refinamento de produto finalizado — aprovado para delivery
> 3. Discovery finalizado (sem promote)
> 4. Entrou para delivery
> 5. Bug encontrado em produção
> 6. Outro (descreva em uma frase)

### Passo 2: Gerar rascunho narrativo

Use o formato padrão: **contexto → decisão/fato → próximo passo**.

Adapte o tom ao momento:

**Pronto para refinamento de produto**
```
[Nome do Projeto] — pronto para refinamento

[1 parágrafo: o que foi concluído que viabiliza o refinamento — discovery, validação, alinhamento com stakeholders]

Próximo passo: refinamento de produto com [time/pessoa] — [prazo estimado ou "a definir"].
```

**Refinamento de produto finalizado — aprovado para delivery**
```
Refinamento concluído. [Nome do Projeto] aprovado para delivery.

[1 parágrafo: o que foi decidido no refinamento — escopo fechado, critérios validados, dependências resolvidas]

Escopo aprovado:
- [capacidade 1]
- [capacidade N]

Próximo passo: [refinamento técnico com engenharia / início do build / milestone 1].
```

**Discovery finalizado (sem promote)**
```
Discovery concluído. [O que foi validado — 1 frase].

[1 parágrafo: direção definida, perguntas respondidas, decisões tomadas]

Próximos passos: [criar Projeto de Delivery / refinamento / outra ação concreta].
```

**Entrou para delivery**
```
[Nome do Projeto] entrou para delivery — [Quarter ou período].

[1 parágrafo: contexto do que será construído e por quê agora]

Escopo do build:
- [capacidade 1]
- [capacidade N]

Próximo passo: [milestone 1 ou ação concreta].
```

**Bug encontrado em produção**

Este momento executa duas ações em sequência — criação das issues e postagem do update:

**1. Criar Issues de Bug no Linear**

Para cada bug mencionado pelo usuário, aplique o fluxo de CREATE (subtipo Bug) usando o template de Issue. Vincule cada issue ao projeto em questão. Pergunte apenas o que for bloqueante e ainda não estiver na mensagem do usuário.

Após criar todas as issues, confirme os links gerados antes de passar para o update.

**2. Postar o update narrativo**

```
[N] bug(s) identificado(s) em produção — [descrição curta do conjunto de problemas].

[1 parágrafo: impacto observado, quem é afetado, contexto de quando foi identificado]

Issues criadas:
- [título do bug 1] → [link]
- [título do bug N] → [link]

Status atual: [em investigação / causa-raiz identificada / correção em andamento]
Próximo passo: [ação imediata + prazo estimado].
```

**Outro (livre)**
Gere um update narrativo baseado na descrição fornecida pelo usuário, seguindo o formato contexto → decisão/fato → próximo passo.

### Passo 3: Confirmar destino e postar

Apresente o rascunho e pergunte:
> "Quer postar este update no projeto, na Iniciativa associada, ou nos dois?"

Aguarde confirmação antes de executar. Use `save_status_update` vinculado ao projeto ou iniciativa correspondente.

---

## Fluxo: HELP

Exiba:

1. **A hierarquia** Iniciativa → Discovery → Delivery → Issue com a pergunta que cada nível responde.
2. **A regra de ouro de títulos** com exemplos bons e ruins.
3. **Os anti-patterns mais comuns** (baseados em [references/anti-pattern.md](references/anti-pattern.md)).
4. **Exemplos reais** de Iniciativa e Projeto de Delivery bem estruturados.
5. **Relação Discovery → Delivery**: Discovery não é pré-requisito obrigatório de Delivery. Use Discovery quando o escopo ainda não está fechado e há incertezas a resolver. Vá direto para Delivery quando o escopo já está claro e validado com stakeholders. Quando existir um Discovery prévio, use `promote` para converter — ele pré-preenche o Delivery com as decisões tomadas e vincula os dois projetos.
6. **Quando NÃO criar um Projeto de Delivery**: Se o trabalho tem os três sinais abaixo, o item certo é uma Issue — não um Projeto de Delivery:
   - Cabe em 1-2 dias de trabalho de uma pessoa
   - Não tem fases nem paralelismo
   - Não envolve Designer nem múltiplos times
   *(Esses sinais não se aplicam a Discovery — um Discovery pode ser pequeno e de uma pessoa só, e ainda assim fazer sentido como projeto.)*
7. **Quando usar `validate`**: Use quando um item foi criado fora do skill, quando alguém pediu revisão da spec, ou quando o projeto já existe e o time quer garantir que está bem estruturado antes de avançar. O validate analisa título, vínculos, escopo e critérios de aceite — e sugere melhorias com justificativa.
8. **Lembrete de escopo**: este skill não cobre issues técnicas de engenharia — para isso, use `linear-issues`.

---

## Activity Updates — Formato e Exemplos

Os updates são narrativos, não one-liners. Contextualizam o momento do projeto para toda a equipe.

### Exemplo: Update em Iniciativa (após promote)

> **Discovery concluído — entrando em refinamento e delivery**
>
> O projeto de discovery da Biblioteca de Conteúdos foi finalizado. Protótipo validado, direção definida, escopo fechado.
>
> Três projetos de delivery gerados para Q2/2026:
>
> **Redesenhar a Biblioteca de Conteúdos do Portal Plus** — nova experiência de navegação: DS atualizado, pastas em grade, busca transversal e filtros combinados
>
> **Implementar Notificação parametrizável no backoffice da Biblioteca** — substitui "Destaques" por componente configurável
>
> **Simplificar a arquitetura de conteúdos do backoffice** — migração de hierarquia (pré-requisito para o redesign)
>
> Próximos passos: refinamento com engenharia esta semana, build e staging em mai/2026, deploy em produção até Jun/30.

### Exemplo: Update em Projeto de Discovery (após promote)

> **Discovery concluído.** O protótipo foi validado e a direção de produto está definida — as perguntas em aberto foram respondidas e o escopo está fechado para build.
>
> **O que foi decidido:**
> - Pastas visíveis em grade substituem o menu dropdown como padrão de navegação
> - Busca transversal com filtros cumulativos resolve o problema de encontrabilidade documentado
> - Seção "Destaques" substituída por componente de Notificação parametrizável
>
> **Projetos de Delivery gerados:**
> - Redesenhar a Biblioteca de Conteúdos do Portal Plus
> - Implementar Notificação parametrizável no backoffice da Biblioteca
> - Simplificar a arquitetura de conteúdos do backoffice
>
> Os três projetos estão vinculados à iniciativa *Elevar a encontrabilidade de recursos no Portal Arcoplus*, com prazo-alvo em Jun/2026.

## Referência Técnica: Tratamento de Argumentos

- `$ARGUMENTS` contém tudo após `/linear-spec`
- Primeiro argumento: comando (create/promote/validate/help)
- Argumentos seguintes: parâmetros do comando

Exemplos:
- `/linear-spec create` → comando=create, iniciar diagnóstico interativo
- `/linear-spec promote PROJ-123` → comando=promote, buscar e converter o projeto PROJ-123
- `/linear-spec promote "Biblioteca"` → comando=promote, buscar projeto por nome parcial
- `/linear-spec validate INI-42` → comando=validate, buscar e analisar a Iniciativa INI-42
- `/linear-spec` (sem args) → perguntar o que o usuário deseja fazer

---

## Referências

| Arquivo | Conteúdo |
|---------|----------|
| [references/dicionario.md](references/dicionario.md) | Regra de ouro de títulos, dicionário de verbos, boas práticas de formatação |
| [references/anti-pattern.md](references/anti-pattern.md) | Anti-patterns comuns em títulos e descrições |
| [references/linear-method.md](references/linear-method.md) | Princípios do Linear Method (documentação oficial) |
| [references/template-iniciativa.md](references/template-iniciativa.md) | Template e exemplo real de Iniciativa Estratégica |
| [references/template-discovery.md](references/template-discovery.md) | Template de Projeto de Discovery |
| [references/template-delivery.md](references/template-delivery.md) | Template e exemplo real de Projeto de Delivery |
| [references/template-issues.md](references/template-issues.md) | Templates de Issue: Improvement e Bug |
| [references/discovery-e-design.md](references/discovery-e-design.md) | Fluxo Discovery → Delivery, milestones de transição, erros comuns |

### Princípios-chave do Linear Method (resumo)

1. **Direção significativa**: Iniciativas e Milestones existem para lembrar a todos o propósito de longo prazo do trabalho.
2. **Conecte o trabalho diário a metas maiores**: Todo Projeto deve responder a uma Iniciativa.
3. **Escreva specs, não user stories**: Brevidade. O objetivo é comunicar "porquê", "o quê" e "como" de forma eficiente.
4. **Nomeie donos**: Todo item deve ter um responsável claro.
5. **Decida e avance**: Nem sempre existe a resposta perfeita. O mais importante é decidir e manter o momentum.
6. **O Designer cria as próprias issues**: O PM cria o contexto (Discovery). O Designer quebra o trabalho conforme descobre.
