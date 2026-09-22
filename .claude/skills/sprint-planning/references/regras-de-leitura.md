# Regras de leitura da sprint

Cada regra aqui existe porque a falta dela já produziu um artefato errado durante a construção do modelo,
na Sprint 2 do Time PAM (setembro de 2026). A justificativa faz parte da regra — sem ela, a próxima pessoa
desfaz a regra achando que é preciosismo.

---

## 1. Releia a sprint inteira antes de cada atualização

O PM edita o ClickUp em paralelo à conversa. Em uma única sessão apareceram cinco mudanças de status, duas
de prioridade e três cards novos, todas entre uma versão do artifact e a seguinte.

Puxe a lista completa da sprint a cada rodada, com `include_closed=true` e `subtasks=true`, e faça o diff
contra a leitura anterior. Reporte o que mudou. Nunca atualize só o pedaço que o PM mencionou.

## 2. Data de criação não é tempo de espera

**O erro:** classificar 22 itens como "parados desde antes do início da sprint, alguns desde julho" e
apresentar isso como dívida.

**Por que está errado:** um item criado em julho pode ter passado esse tempo inteiro em refinamento de
produto e design, que é a faixa de descoberta do Backlog funcionando como deveria. Idade de card não é
atraso.

**A regra:** classifique origem apenas em duas categorias, e só com o dado que sustenta cada uma:

| Categoria | Como identificar |
|---|---|
| Já em execução | status diferente de "não iniciada" — o trabalho começou antes da sprint abrir |
| Entra em execução agora | status "não iniciada" |

Se quiser falar de tempo, é preciso histórico de mudança de status. Sem isso, não afirme.

## 3. Só desenvolvedores entram na carga e no objetivo por pessoa

**O erro:** listar todo mundo com item atribuído. O topo do ranking virou o QA com 37 itens, seguido da
designer com 17 — os dois à frente de qualquer dev. A leitura ficou: "essas são as duas maiores cargas de
desenvolvimento da sprint", o que é falso.

**A regra:** quem é dev vem de `knowledge/domains/pessoas.md`. Team Lead e Tech Lead entram, porque são mão
na massa nesse time. Design, qualidade e gestão de produto ficam de fora de todas as visões.

Os **itens** deles continuam no artifact — eles são escopo da sprint e entregam valor. O que sai é a
contagem de pessoas, não o trabalho.

Item sem nenhum dev alocado recebe marca própria: ocupa lugar na sprint, mas não consome capacidade de
desenvolvimento.

## 4. A ordem da fila vem da prioridade cadastrada

**A tentação:** inventar um peso combinando frente de valor, tipo de item e status.

**Por que não:** o PM já curou a prioridade. Na Sprint 2, 54 de 58 itens tinham o campo preenchido.
Substituir isso por um algoritmo próprio joga fora a curadoria e torna a ordem impossível de explicar numa
reunião.

**A regra**, nesta ordem:

1. O que já saiu da mão do dev (em validação, indo para produção) vai para o fim, porque não depende mais
   dele.
2. Prioridade do ClickUp: urgente, alta, normal, baixa, sem prioridade.
3. Empate: em desenvolvimento antes de bloqueada, bloqueada antes de não iniciada.
4. Empate final: ordem alfabética do nome.

Desenvolvedores em ordem alfabética entre si. A ordem dentro da lista é de prioridade; a ordem das listas
não deve sugerir ranking de pessoas.

## 5. Item sem prioridade cai no fim — e isso precisa ser reportado

Aconteceu duas vezes na mesma sessão: a entrega principal de um dev entrou sem prioridade e apareceu no
rodapé da lista dele, atrás de um item marcado como baixa. Um item de compliance em desenvolvimento ficou
em último pelo mesmo motivo.

**A regra:** não abra exceção no código para um card específico — isso quebra a explicabilidade da ordem.
Reporte ao PM: "estes itens estão sem prioridade e por isso aparecem no fim; se algum deveria estar no
topo, o campo precisa ser preenchido."

## 6. Campo deduzido é marcado, listado e confirmado

Na Sprint 2, 38 de 58 itens não tinham casa preenchida e 30 não tinham frente de valor. Sem dedução não há
visão por casa nem por frente.

**A regra:** deduza o necessário, marque cada dedução visualmente no artifact (pontilhado, com tooltip
explicando), diga no rodapé quantos itens foram deduzidos, e entregue a lista ao PM para confirmação.
Campo inferido apresentado como dado é a falha mais cara desta skill.

## 7. Casa: item compartilhado aparece nas duas listas

O workspace tem três valores: Tradicional, Bravo e Vertical. **Vertical significa que afeta as duas
casas** — não é uma terceira casa e não recebe filtro próprio.

Item de plataforma ou de backoffice aparece na contagem da Tradicional e na da Bravo, marcado como
compartilhado. É a mesma entrega contada uma vez para cada operação que se beneficia dela, e o artifact
precisa dizer isso para o número não parecer inflado.

## 8. Nome de card é reescrito no artifact, nunca no ClickUp

Títulos com jargão, caixa alta, prefixo de squad ou status embutido no nome atrapalham a leitura executiva.
Reescreva no artifact, guarde o original no tooltip, e entregue a lista de sugestões ao PM.

Quando o título não diz qual é o problema — "Corrigir aba de Ajustes & Bônus" —, **não invente**. Reporte
que o nome não é autoexplicativo e peça o contexto.

## 9. Épico compartilhado: só quem tem subtarefa aberta segue na lista

Um levantamento com 32 subtarefas, 30 já fechadas, mantinha seis responsáveis no card pai. Só um tinha
subtarefa aberta. O épico aparecia em seis listas, dando impressão de carga que não existe.

**A regra:** essa é uma exceção explícita por item, não uma regra geral. Aplicada de forma ampla, ela
tiraria a designer de cards em que ela é dona do desenho e o dev de um card em que ele é dono do item.
Trate caso a caso, marque no código como exceção, e confirme com o PM.

## 10. Move do Backlog para a Sprint quebra o status

O ClickUp mapeia o status para o primeiro da lista de destino, que hoje é `bloqueada`. Itens movidos entram
na sprint parecendo impedimento.

**A regra:** depois de qualquer movimentação, releia o status e corrija para `pendente`. Na criação direta
o problema não ocorre, desde que o status seja informado explicitamente.

## 11. Épico que não fecha no ciclo não entra como item de sprint

Item grande demais para duas semanas conta como um item do ciclo no relatório de Revisão e quase
certamente não fecha, sujando a taxa de entrega com algo que nunca foi de duas semanas.

**A regra:** quando encontrar um item cujo escopo não cabe no ciclo, aponte e proponha o corte — o épico
volta ao Backlog para ser fatiado e a primeira fatia entra na sprint. A decisão é do PM.
