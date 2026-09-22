# Reorganização de vínculos com Épico e datas Início/Término para o report semanal

**Data**: 2026-08-10
**Tomada por**: Ithalo Mendes (PM)
**Status**: APROVADA (parcial — Produto ainda não iniciado; 3 conflitos e clusters órfãos seguem pendentes)

---

## Contexto

O report semanal do time (artifact interno) agrupa atividades por "Frente" (= Épico pai da tarefa) e usa `Início`/`Término` como referência temporal. A auditoria do board Vertical Tech mostrou que Plataforma e Backoffice tinham a maioria das tarefas abertas sem Épico vinculado ("Sem frente") e praticamente 100% sem `Início`/`Término`, distorcendo o report.

## Opções Consideradas

1. **Preencher datas manualmente com os leads** — mais preciso, mas lento e bloqueia o report por semanas.
2. **Inventar datas plausíveis (ex.: sprint atual)** — rápido, mas corrompe dados reais de planejamento.
3. **Derivar `Início`/`Término` do histórico real de mudança de status de cada tarefa** (quando ela entrou em execução / quando entrou em status terminal) — só preenche o que é factual; deixa em branco o que ainda não existe.

## Decisão

Optamos pela opção 3. `Início` = timestamp da primeira transição para fora da fila/backlog no histórico de status da tarefa. `Término` = timestamp da transição para um status realmente terminal (`finalizado`/`fechado`/`concluído`), nunca status de fila como "pronto p/ design" ou "pronto p/ execução". Quando o histórico não permite derivar (tarefa nunca saiu do backlog, ou ainda está ativa), o campo fica em branco — não é preenchido com valor fictício.

Escopo desta rodada: apenas squads **Plataforma** e **Backoffice & Integração**. Produto ficou de fora (poucos problemas, menor urgência).

Além disso, pseudo-épicos (tarefas comuns com ≥2 subtarefas reais funcionando como guarda-chuva) foram promovidas ao tipo Épico, e órfãs com cluster claro por nome/contexto foram vinculadas ao Épico correspondente — nunca por adivinhação.

## Trade-offs Aceitos

- Tarefas que nunca saíram do backlog continuam sem `Início` real — esperado, não é erro.
- Tarefas ativas que ainda não chegaram a um status terminal continuam sem `Término` — esperado, o report já tem fallback para isso.
- Clusters órfãos sem um Épico existente compatível (ex.: "saque" em Plataforma, tickets de acesso AWS) não foram vinculados — ficam para decisão humana (criar Épico novo ou não).
- 3 conflitos onde o `Início` derivado ficou depois do `Término` já cadastrado manualmente não foram aplicados — indicam inconsistência pré-existente que precisa de revisão humana.

## O que mudaria a decisão

Se o time decidir que quer datas de planejamento (não históricas) no board — ex. `Término` como compromisso futuro real — essa lógica de derivação não serve mais para tarefas ativas; nesse caso vira responsabilidade dos squads preencherem a data real de compromisso.

## Impacto

- **Produto**: nenhum módulo de produto afetado; é reorganização de metadados de processo.
- **Técnico**: nenhum.
- **Processo**: report semanal agora consegue agrupar corretamente por Frente e usar datas reais para Plataforma/Backoffice. Squad Produto ainda tem 7 tarefas "Sem frente" e a maioria dos Épicos sem data própria — pendente de rodada futura.

## Links

- Auditoria (dados brutos): `scratchpad/audit/payload.json`, `scratchpad/audit/report.json`
- Changelog da execução: `scratchpad/audit/changelog.json`
- Cards promovidos a Épico: `868kfcbrw`, `868k9dqjg`, `868km1cj3` (Backoffice); `868kch8vq`, `868km1uhp` (Plataforma)
