# Migração das páginas de promoção hard-coded da Bravo para o Page Builder

**Data**: 2026-07-23
**Tomada por**: Ithalo Mendes
**Status**: APROVADA

---

## Contexto

O ticket VL-13478 ("Alteração nas Thumbs e exclusão da página Jogo X na aba de Promoções") era um pedido pontual de suporte da Bravo — trocar thumbnails e excluir a página de promoção de um jogo específico. O pedido em si é sintoma de um problema maior: nem todas as páginas de promoção da Bravo foram migradas para o Page Builder, então mudanças de conteúdo ainda dependem de dev.

Já existia um Épico-guarda-chuva no workspace Vertical Tech — "Evoluir o Backoffice com features para eliminar OPEX" (`868kf0w78`) — cujo objetivo é dar autonomia self-service às operadoras (Bravo e Tradicional) e eliminar chamados operacionais à Tech, vinculado ao OKR "Eficiência operacional" (`868keardx`). Esse guarda-chuva já lista Page Builder no escopo, mas hoje só cobre layout de home — não o ciclo de vida completo de páginas de promoção (editar, trocar thumb, excluir).

Já houve migrações incrementais anteriores de páginas de promoção da Bravo para o Page Builder (`868ka1f29` e VL-12831, ambos finalizados) — mas claramente incompletas, já que o VL-13478 mostra pelo menos uma página (Jogo X) ainda hard-coded.

**Gatilho que mudou o curso da execução**: ao investigar o VL-13478 para reformulá-lo, descobrimos que ele havia sido triado nas últimas horas — saiu de "aberto" sem responsável para "em desenvolvimento", com Allison Macedo e Railton Araujo como assignees, prioridade alta. Ou seja, alguém já tinha começado a codar o fix pontual do Jogo X enquanto o card era investigado para virar uma iniciativa maior.

## Opções Consideradas

1. **Converter o próprio VL-13478** no Épico de migração — mover para a hierarquia de Delivery, retipar, reescrever escopo.
   - Prós: mantém um único card, sem duplicidade.
   - Contras: como o card já estava em desenvolvimento ativo (dois devs, prioridade alta), reescrever/mover o card no meio do trabalho gera risco de confusão ou de parecer que o trabalho foi descartado.

2. **Manter VL-13478 intocado e criar um novo Épico** de migração, linkado como evidência.
   - Prós: não interfere no trabalho já em andamento de Allison/Railton; separa claramente "o pedido pontual (Jogo X)" de "a iniciativa estrutural (migrar tudo)".
   - Contras: dois cards para rastrear a mesma dor; precisa de vínculo explícito para não parecer desconexo.

## Decisão

Opção 2. Criado o Épico **"Habilitar a Bravo a gerenciar páginas de promoção pelo Page Builder, sem depender de dev"** (`868kfn58n`), no folder Delivery:Backoffice & Integração, lista Backlog, vinculado ao Épico-guarda-chuva (`868kf0w78`), ao OKR (`868keardx`) e ao VL-13478 (`868kf7rej`) como evidência do problema. VL-13478 segue exatamente como estava — sem alteração de status, assignee ou descrição — para não interromper o trabalho de Allison/Railton.

Fator decisivo: o card já estar em execução ativa quando a reformulação seria aplicada. Redesenhar escopo de um card no meio do desenvolvimento é mais arriscado do que criar um novo item e linkar a evidência.

## Trade-offs Aceitos

- Duas frentes de trabalho aparentemente sobrepostas (o fix pontual do Jogo X e o Épico de migração) — mitigado pelo vínculo explícito e pela nota no Épico de que o card do Jogo X "segue sendo resolvido separadamente, não migra para este Épico".
- Escopo do Épico nasce com lacunas abertas (quantas páginas ainda são hard-coded, se o Page Builder suporta exclusão de página inteira) — fica registrado em "Aberto para refinamento", bloqueando entrada em sprint até ser fechado.
- Escopo Tradicional ficou de fora da v1 — só há evidência confirmada do problema na Bravo.

## O que mudaria a decisão

- Se o levantamento mostrar que restam poucas páginas hard-coded (≤2-3) e o Page Builder já suporta exclusão nativamente, o item deveria ser reclassificado de Épico para Tarefa.
- Se Allison/Railton confirmarem que o fix do Jogo X já implementou a capacidade de exclusão no Page Builder (não só um patch pontual de código), isso já resolve parte do escopo do Épico e deveria atualizar os critérios de aceite.

## Impacto

- **Produto**: páginas de promoção da Bravo (Hub de Promoções, web e mobile).
- **Técnico**: Page Builder (Backoffice) — possível necessidade de nova capacidade (exclusão de página inteira), a validar com engenharia.
- **Processo**: nenhuma mudança de processo; reforça o padrão de "vínculo espelhado" entre itens correlatos em vez de hierarquia formal entre Épicos (a hierarquia atual não modela Épico-pai/Épico-filho estrutural).

## Links

- Épico criado: [868kfn58n](https://app.clickup.com/t/868kfn58n) — "Habilitar a Bravo a gerenciar páginas de promoção pelo Page Builder, sem depender de dev"
- Épico-guarda-chuva: [868kf0w78](https://app.clickup.com/t/868kf0w78) — "Evoluir o Backoffice com features para eliminar OPEX"
- OKR: [868keardx](https://app.clickup.com/t/868keardx) — Eficiência operacional
- Evidência do problema (intocado): [VL-13478](https://app.clickup.com/t/868kf7rej)
- Histórico de migração anterior: [868ka1f29](https://app.clickup.com/t/868ka1f29), VL-12831 ([868k8fqnk](https://app.clickup.com/t/868k8fqnk))
