# Eliminação do drift do nível Iniciativa nos docs operantes da skill clickup-spec

**Data**: 2026-08-11
**Tomada por**: Ithalo Mendes (via Orquestrador)
**Status**: APROVADA

---

## Contexto

Ao validar a tarefa de Delivery `868kpcu41` (teste A/B do fluxo de cadastro), o `agente-delivery` reportou como
gap de qualidade "campo Iniciativa vazio, sem vínculo a Roadmap Item/Iniciativa". Isso está errado: o nível
Iniciativa **já tinha sido removido do processo** — `knowledge/domains/processo.md` já registrava "Não existe
nível Iniciativa. Projetos de Discovery e Delivery são vinculados diretamente aos Objetivos" e a lista
"Iniciativas" no ClickUp como "mantida apenas como referência histórica".

O PM identificou o erro e pediu a correção do checklist para isso não se repetir.

**Causa raiz**: a decisão de remover o nível Iniciativa nunca se propagou aos docs operantes que o
`agente-delivery`/`clickup-spec` realmente consultam. `knowledge/domains/processo.md` (fonte de verdade do
Knowledge Graph) e `agente-delivery.md:43` já estavam corretos; mas `clickup-config.md` (a fonte de IDs/regras
que `SKILL.md` manda carregar) ainda tratava a lista Iniciativas como ativa, com custom fields, regra de
status, regra de vínculo e uma instrução explícita de que "os campos Empresa, Time, KPIs, Horizonte, Impacto,
Score vivem na Iniciativa. Não tente setá-los em Discovery/Delivery" — o que faz o agente continuar
verificando/exigindo esse vínculo. O mesmo padrão apareceu em `template-delivery.md` (3 ocorrências),
`agente-delivery.md:90` (contradizendo a própria linha 43 do mesmo arquivo) e `clickup-method.md` (instruindo
propor Impacto/Alcance/Score/Horizonte/Votos como se existissem em itens de Delivery).

**Achado adicional, verificado via dado real (não suposição)**: consultei `868kpcu41` via `clickup_get_task`
e confirmei que os campos Impacto, Alcance, T-Shirt Sizing, Score, Horizonte, Votos e Time **nunca estiveram
disponíveis em Discovery/Delivery** — só existiam na lista Iniciativas. `clickup-method.md` instruía o agente
a propor esses valores em itens de Delivery, o que teria causado uma falha de gravação (mesma classe de erro
do incidente de `task_type "Épico"` registrado em
[2026-08-11-gatilho-imediato-observabilidade-doc-desatualizada.md](2026-08-11-gatilho-imediato-observabilidade-doc-desatualizada.md)).

Havia ainda um arquivo órfão, `clickup-config-tech.md` — versão anterior (2026-07-03) de `clickup-config.md`,
não referenciada por `SKILL.md` nem por `agente-delivery.md`, mas com o mesmo conteúdo desatualizado sobre
Iniciativa, mantendo viva uma segunda cópia divergente.

## Decisão

Aplicado como **fast-track de correção factual** (`services/observability.md` → R4): o fato já estava
decidido e registrado no Knowledge Graph (`processo.md`); o que faltava era propagação, não uma nova decisão
estrutural. Corrigido nesta mesma rodada:

- `clickup-config.md`: lista Iniciativas marcada depreciada na Hierarquia, Status e Tipos de Tarefa; regra de
  Delivery reescrita para depender da Squad (folder), não do campo Time da Iniciativa; seção de custom fields
  de priorização reescrita para declarar que Impacto/Alcance/T-Shirt/Score/Horizonte/Votos/Time **não têm
  moradia ativa em Discovery/Delivery** (com a evidência de `868kpcu41`); campo Iniciativa marcado vestigial;
  vínculo entre níveis reescrito para linked task direto ao Objetivo.
- `clickup-config-tech.md`: banner de depreciação apontando para `clickup-config.md` como fonte real.
- `template-delivery.md`: removidas 3 referências a Iniciativa (folder por Time da Iniciativa, bloco de
  cabeçalho, vínculo da seção Links).
- `agente-delivery.md:90`: corrigida a contradição com a própria linha 43 do arquivo.
- `clickup-method.md`: seção "Priorização de itens de Delivery" reescrita — não instrui mais gravar campos
  inexistentes; Squad explicitado como escolha de folder, não custom field.

## Trade-offs Aceitos

- **Onde os campos de priorização (Impacto/Alcance/Score/Horizonte/Votos/Time) devem viver agora que a
  Iniciativa não existe mais é uma pergunta aberta, não respondida aqui.** Decidi não inventar uma resposta —
  os IDs ficam documentados como referência histórica em `clickup-config.md`, e o agente é instruído a usar
  `ice`/`gist` na conversa em vez de tentar gravar esses campos. Redefinir a moradia é candidato a proposta de
  `agente-evolucao` → `agente-governanca` se o time sentir falta de um score formal no nível Delivery.
- `clickup-config-tech.md` foi marcado como legado em vez de removido — mais conservador, evita decidir
  unilateralmente uma exclusão de arquivo sem pedido explícito.

## O que mudaria a decisão

Se o time decidir reintroduzir um nível de aposta estratégica acima de Discovery/Delivery (revertendo a
remoção da Iniciativa), esta correção precisa ser revertida junto — os arquivos tocados aqui voltariam a
precisar de um "onde vive" ativo.

## Impacto

- **Produto**: nenhum — correção de documentação/config, não de comportamento de produto.
- **Técnico**: nenhuma integração nova; edições em `clickup-config.md`, `clickup-config-tech.md`,
  `template-delivery.md`, `agente-delivery.md`, `clickup-method.md`.
- **Processo**: `agente-delivery` para de exigir vínculo a Iniciativa e para de tentar gravar campos de
  priorização inexistentes em Discovery/Delivery — elimina a classe de falso-positivo que gerou este
  incidente.

## Links

- Tarefa que revelou o drift: `868kpcu41` ("[PAM] Estruturação de teste A/B cadastro")
- Fonte de verdade já correta: `knowledge/domains/processo.md` → "Hierarquia do Processo"
- Precedente de mesmo padrão (fast-track de doc desatualizada, task_type): [2026-08-11-gatilho-imediato-observabilidade-doc-desatualizada.md](2026-08-11-gatilho-imediato-observabilidade-doc-desatualizada.md)
- Decisão irmã (mesma sessão): [2026-08-11-aberto-para-refinamento-tecnico-restricao-de-uso.md](2026-08-11-aberto-para-refinamento-tecnico-restricao-de-uso.md)
