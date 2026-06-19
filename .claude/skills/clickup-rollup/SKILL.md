---
name: clickup-rollup
description: |
  Consolida os updates das tarefas relacionadas (Discovery/Delivery) em comentários narrativos nos Roadmap Items do ClickUp (workspace Vertical Loto), para que cada iniciativa deixe de ficar isolada.
  Detecta updates relevantes nas tarefas vinculadas a cada Roadmap Item — pesquisa concluída (com resultado), protótipo finalizado (com link do Figma), mudança de status, novo Delivery promovido — e posta um roll-up na iniciativa.
  Na mesma varredura, mantém a seção Portfólio de Projetos de cada Roadmap Item fiel aos vínculos reais (reconciliação aditiva dos linked tasks).
  Ignora tarefas operacionais, bugs e qualquer tarefa não vinculada ao Roadmap. Executado pelo agente gerenciador-do-clickup. Feito para rodar sob demanda ou agendado diariamente.
  Comandos: /clickup-rollup run [ID ou nome opcional], /clickup-rollup dry-run, /clickup-rollup help
---

**Autor:** Ithalo Mendes <ithalo.mendes@verticalloto.com>

# ClickUp Roll-up — Updates de Iniciativa

Mantém cada **Roadmap Item** (iniciativa) vivo: quando uma tarefa **relacionada** (Discovery/Delivery vinculada
por linked task) tem um update relevante, esta skill **sintetiza e posta um comentário narrativo no Roadmap
Item** — "pesquisa realizada com o resultado", "protótipo finalizado com link do Figma", "Delivery entrou em
QA", etc. Assim a iniciativa concentra a história dos seus projetos, sem ninguém precisar caçar tarefa por tarefa.

Na mesma passada, a rotina também **mantém a seção 🗂️ Portfólio de Projetos da iniciativa espelhando os vínculos
reais** — fechando, de forma automática, o guardrail manual da `clickup-spec` ("nunca crie um linked task sem
atualizar o Portfólio"). Duas responsabilidades, uma varredura: **comentar** o que avançou e **reconciliar** o
Portfólio.

> **Quem executa:** o agente [gerenciador-do-clickup](../../agents/gerenciador-do-clickup.md). Esta skill é a
> rotina; o agente é o braço que lê o ClickUp e posta os comentários.
> **Relação com `clickup-spec`:** a `clickup-spec` *cria/estrutura* itens; a `clickup-rollup` *mantém a iniciativa
> atualizada* com o que acontece nos projetos vinculados. As duas compartilham config e método.

## Comandos

| Comando | Uso | Descrição |
|---------|-----|-----------|
| `run` | `/clickup-rollup run [ID/nome]` | Varre os Roadmap Items ativos e posta os roll-ups necessários (modo automático — só ClickUp). Aceita ID/nome para rodar em uma única iniciativa. |
| `run` **+ notas** | `/clickup-rollup run` + notas da reunião | Igual ao `run`, mas você fornece as **notas da reunião** (pontos coletados + próximos passos). A skill cruza o progresso do ClickUp com as suas decisões e escreve o update na sua voz. **Modo recomendado** — ver "Modo com notas". |
| `dry-run` | `/clickup-rollup dry-run` | Faz a varredura e **apresenta** os roll-ups que seriam postados, **sem postar** (aceita notas também). Use para revisar antes. |
| `help` | `/clickup-rollup help` | Explica escopo, gatilhos e formato. |

## Verificação de Conector (obrigatória)

Antes de rodar, verifique silenciosamente se o conector do ClickUp está ativo (ex: `clickup_get_folder` com o
ID do Product Roadmap em [../clickup-spec/references/clickup-config.md](../clickup-spec/references/clickup-config.md)).
Se não estiver disponível, interrompa e oriente a conectar o ClickUp (Configurações → Integrações → ClickUp).
**Em execução agendada/headless, o conector pode não estar autenticado** — ver "Agendamento diário".

## Escopo — o que entra e o que NÃO entra

**Entra:** tarefas de **Discovery** e **Delivery** vinculadas por *linked task* a um **Roadmap Item** (folder
Product Roadmap). Só essas alimentam o roll-up da iniciativa.

**NÃO entra (nunca gerar roll-up a partir destas):**
- Bugs / incidentes (`_Classe` = Incidente, `Tipo de Chamado` = Incidente).
- Tarefas operacionais e de suporte (ex: folders/listas de Tickets, CRM, sustentação).
- Qualquer tarefa **sem vínculo** com um Roadmap Item.
- Subtasks puramente técnicas (passos de implementação) — o sinal relevante é o **status/entregável do projeto**, não cada micro-passo.

> Regra de ouro: se a tarefa não está no Portfólio de uma iniciativa, ela não existe para esta skill.

## O que conta como "update relevante" (gatilhos)

Só estes momentos geram roll-up — para evitar ruído:

| Gatilho na tarefa vinculada | O que o roll-up comunica |
|------------------------------|--------------------------|
| **Mudança de status** (ex: Discovery → `em aprovação`/`fechado`; Delivery → `dev`/`qa`/`done`) | "[Projeto] avançou para [status]." |
| **Pesquisa concluída** (Discovery sub-tipo Pesquisa fechado, ou comentário com resultado) | "Pesquisa realizada: [principais achados + decisão]." |
| **Protótipo finalizado** (Discovery de Prototipação com link do Figma + status fechado) | "Protótipo finalizado: [link Figma] · [decisões de UX fechadas]." |
| **Novo Delivery promovido** a partir de um Discovery | "Escopo fechado; Delivery [VL-XXXXX] criado." |
| **Bloqueio/risco registrado** (comentário marcado como bloqueio, ou status `stand-by`) | "Bloqueio: [o quê] · próximo passo." |
| **Entrega concluída** (Delivery `done`/`ready for deployment`) | "[Projeto] entregue." |

Edição cosmética (typo na descrição, troca de assignee, mudança de data) **não** é gatilho.

## Reconciliação do Portfólio (espelho dos vínculos)

Segunda responsabilidade da mesma varredura. Como o passo 2 **já lê os linked tasks** de cada iniciativa, a
reconciliação roda no mesmo job, sem leitura extra. Objetivo: manter a seção **🗂️ Portfólio de Projetos** do
Roadmap Item fiel aos vínculos reais, fechando o guardrail manual da `clickup-spec`.

**O que faz:**
- **Adiciona** ao Portfólio todo Discovery/Delivery vinculado (linked task) que ainda não está listado, no formato `Nome (https://app.clickup.com/t/9006076935/VL-XXXXX)` — uma linha por projeto, com a URL completa, que o ClickUp renderiza como task-link interativo (status + responsável). Ver clickup-method → "Boa prática — espelhar sempre no Portfólio".
- **Sinaliza no relatório** (não remove) entradas do Portfólio que apontam para uma tarefa **sem vínculo ativo** — pode ser link removido ou item arquivado; a remoção é decisão de uma pessoa.
- **Não toca** em nada fora da seção 🗂️ Portfólio: Visão, Métricas, Dependências e qualquer anotação manual ficam intactas.

**Quando edita:** só quando há diferença real (algum vínculo faltando). Portfólio já fiel → não escreve nada
(mesma lógica de silêncio do roll-up). Mesmo escopo do roll-up: só Discovery/Delivery vinculados — bug,
operacional e tarefa solta nunca entram.

**Como:** `clickup_update_task` com `markdown_description`, reescrevendo **apenas** o bloco da seção 🗂️ Portfólio
e preservando o resto do corpo na íntegra. Edição puramente **aditiva** — nunca apaga linhas existentes. Em
`dry-run`, só apresentar o diff (o que seria adicionado / o que está órfão), sem gravar.

## Modo com notas (briefing da reunião) — recomendado

O fluxo ideal: você coleta os pontos com o time, define os próximos passos e **roda a skill passando essas notas**. O update final junta duas camadas:

- **Camada factual** (do ClickUp): o que de fato avançou nas tarefas vinculadas — a skill detecta sozinha.
- **Camada humana** (das suas notas): o que foi decidido, o contexto da conversa e, principalmente, **os próximos passos** que você definiu.

O comentário é escrito na sua voz fundindo as duas — fato + decisão.

**Como passar as notas:** rode `/clickup-rollup run` e cole as notas (livres, podendo citar várias iniciativas). Ex.:
> *"Hub: validamos o loop com 3 usuários, vamos de streak semanal. Afiliados: alinhei com o dev, começam segunda. KYC: validação fecha essa semana, subimos sexta."*

**Como a skill usa:**
1. Mapeia cada trecho da nota para a iniciativa correspondente (por nome). Não identificou com segurança → **pergunta**, não chuta.
2. Para cada iniciativa, funde o progresso do ClickUp com a sua nota e escreve o update.
3. **O próximo passo vem sempre da sua nota** — a skill nunca o inventa.

**Regra do próximo passo:**
- **Com nota** para a iniciativa → use o próximo passo que você deu.
- **Sem nota**, mas com update no ClickUp → escreva o progresso e marque o próximo passo como **"a definir"** (não invente).
- **Nota sem update no ClickUp** (você decidiu algo que ainda não virou status/comentário lá) → ainda vale roll-up: a decisão humana já é um update relevante para o stakeholder.

Sem notas, a skill roda no **modo automático** (só ClickUp) — útil para a rotina agendada, com próximos passos "a definir".

## Processo (passo a passo)

1. **Listar iniciativas ativas.** `clickup_filter_tasks` no folder Product Roadmap (`90118030606`), status diferente de `not doing`/`Closed`. Opcional: filtrar por uma iniciativa se o comando trouxe ID/nome.
2. **Para cada iniciativa**, ler os vínculos: `clickup_get_task` com `include: ["linked_tasks"]`. Resolver cada linked task (`clickup_get_task` → status, `date_updated`, descrição; `clickup_get_task_comments` p/ achados recentes). Descartar as que caem no escopo "NÃO entra".
3. **Determinar a janela** (idempotência — ver abaixo): pegar a data do **último roll-up automático** já postado na iniciativa; considerar só updates de tarefas vinculadas com `date_updated` **posterior** a essa data. Sem roll-up anterior → janela padrão de **7 dias**.
4. **Aplicar os gatilhos.** Se nenhuma tarefa vinculada teve update relevante na janela **e** não há nota da reunião para a iniciativa → **não postar nada** (silêncio é resultado válido). Uma nota relevante, sozinha, já justifica o roll-up.
5. **Sintetizar** um único comentário de roll-up por iniciativa (formato abaixo), **fundindo o progresso detectado no ClickUp com as notas da reunião** (se fornecidas — ver "Modo com notas"). O **próximo passo vem das notas**; sem nota, marque "a definir" — nunca invente.
6. **Postar** com `clickup_create_comment` (entity_type `task`, entity_id da iniciativa). Em `dry-run`, só apresentar.
7. **Reconciliar o Portfólio** (ver "Reconciliação do Portfólio"): compare os linked tasks de Discovery/Delivery com a seção 🗂️ Portfólio do Roadmap Item; se faltar algum, reescreva **só** esse bloco via `clickup_update_task` (edição aditiva) e sinalize entradas órfãs no relatório. Portfólio já fiel → não escreve. Em `dry-run`, só apresentar o diff.
8. **Reportar** ao final: quantas iniciativas varridas, quantos roll-ups postados, quantos Portfólios reconciliados (e o que foi adicionado/órfão), quais ficaram em silêncio e por quê.

## Idempotência (sem estado persistente)

ClickUp não guarda "última execução"; o estado vive nos **próprios comentários**:

- Todo roll-up começa com o marcador (linha de título) **`**Update da iniciativa**`** — humano, estável e detectável. **Sem data no texto:** o ClickUp já carimba a data do comentário.
- Antes de postar, leia os comentários da iniciativa, ache o update mais recente com esse marcador e use o `date_created` nativo dele como início da janela.
- **Nunca** poste um roll-up que repita um update já consolidado num roll-up anterior. Na dúvida sobre duplicidade, prefira **não** postar e sinalizar no relatório.

## Tom e formato do comentário (Activity Update humanizado)

O comentário **não é um relatório de status** — é o **update que o PM escreveria de próprio punho para os stakeholders**, em primeira pessoa, com lente de valor. Inspirado no Activity Update do `linear-spec`: narrativo, contextual, conecta o trabalho ao resultado.

**Tom (voz do Ithalo):**
- Fale como gente, para gente: "a gente", "seguimos" — direto e caloroso, sem jargão de processo.
- **Comece pelo valor / pelo porquê**, não pelo status. O stakeholder quer saber o que isso destrava, não em que coluna a tarefa está.
- Traduza status em significado: "entrou em validação" → "estamos a um passo de subir pra produção"; "design finalizado" → "pronto pra virar produto".
- Use o nome do projeto em linguagem natural; **evite códigos `VL-XXXXX` e termos operacionais** no corpo (o vínculo já garante a rastreabilidade).
- Transparência honesta: se algo ainda está em aberto, diga. Emojis com parcimônia (no máximo um, se couber).
- Curto: 3–6 linhas. Abertura → o que avançou e por que importa → próximo passo.
- **O próximo passo vem de você** (das notas da reunião), nunca inventado. Sem nota, escreva "a definir".

**Estrutura:**

```markdown
**Update da iniciativa**

{Abertura: 1 frase conectando ao resultado/valor da iniciativa.}

{Progresso, em prosa: o que avançou e por que importa — tecendo os projetos que tiveram update, sem listar status cru.}

{Próximo passo, em tom de parceria.}
```

> Sem data no texto — o comentário já vem datado pelo ClickUp.

### Exemplo (voz humanizada)

> **Update da iniciativa**
>
> Avançamos bem no onboarding com KYC — justamente o ponto onde a gente mais perdia usuário, com quase metade sumindo entre o cadastro e o primeiro depósito.
>
> O novo fluxo, com a validação facial antes do depósito e a verificação rodando em segundo plano (sem travar ninguém), está em validação. E o banner que recupera quem fica pendente já está em deploy.
>
> Ou seja: estamos a um passo de destravar o maior gargalo do funil, sem abrir mão da conformidade. Assim que a validação fechar, subimos pra produção. Seguimos.

## Modo de confirmação

- **Interativo** (`/clickup-rollup run` digitado por uma pessoa): em `clickup-spec`, postar comentário exige confirmação. Aqui, **apresente os roll-ups + as reconciliações de Portfólio e peça um "ok" único** para aplicar tudo (ou rode `dry-run` antes). Não pergunte item a item.
- **Agendado/autônomo** (rotina diária): **postar e reconciliar é autorizado automaticamente**, porque a skill já se protege por (a) gatilhos restritos, (b) exclusão de bugs/operacional, (c) dedup por marcador e (d) edição de Portfólio **aditiva** e restrita a uma única seção. Ainda assim, o relatório final do run lista tudo que foi postado e reconciliado para auditoria.

## Agendamento diário

Esta skill é desenhada para rodar **uma vez ao dia**. Para agendar, use a skill `schedule` (rotinas/cron do
Claude Code) — a forma de pedir e os cuidados estão na seção "Como agendar" abaixo (no chat principal).

> ⚠️ **Conector em execução headless:** rotinas agendadas rodam fora da sessão interativa e o conector ClickUp
> autenticado via claude.ai pode **não** estar presente. Se o run agendado falhar na verificação de conector,
> rode em uma sessão interativa (ou em um ambiente onde o conector esteja disponível) e trate o agendamento
> como um lembrete diário para executar `/clickup-rollup run`.

## Guardrails

- **Só iniciativas e seus vínculos.** Nunca gere roll-up a partir de bug, operacional ou tarefa solta.
- **Silêncio é válido.** Sem update relevante na janela → não poste. Nada de comentário "sem novidades".
- **Um roll-up por iniciativa por execução.** Agrupe; não pingue um comentário por tarefa.
- **Sem duplicar.** Respeite o marcador e a janela; na dúvida, não poste.
- **Português, primeira pessoa, voz do PM** — humanizado, valor antes de status, como se o próprio PM tivesse comentado (ver "Tom e formato"). Nunca soe como robô ou relatório.
- **Não muda status nem campos** das tarefas — esta skill só **lê** e **comenta**. Mudanças de status são da `clickup-spec`/`gerenciador-do-clickup` sob confirmação.
- **Exceção única de escrita no corpo:** a reconciliação pode editar **apenas** a seção 🗂️ Portfólio do Roadmap Item, de forma **aditiva** (nunca apaga, nunca toca outras seções nem outras tarefas). Qualquer remoção é só sinalizada no relatório, jamais executada.

## Referências

| Arquivo | Conteúdo |
|---------|----------|
| [../clickup-spec/references/clickup-config.md](../clickup-spec/references/clickup-config.md) | IDs de space, folders, listas, custom fields, status |
| [../clickup-spec/references/clickup-method.md](../clickup-spec/references/clickup-method.md) | Método e modelos de comentário narrativo |
| [../../agents/gerenciador-do-clickup.md](../../agents/gerenciador-do-clickup.md) | Agente executor |
