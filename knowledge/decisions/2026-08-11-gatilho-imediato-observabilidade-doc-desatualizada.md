# Gatilho imediato de observabilidade para erro causado por doc/skill desatualizada, com fonte única para o enum de task_type

**Data**: 2026-08-11
**Tomada por**: Ithalo Mendes (via Agente de Governança)
**Status**: APROVADA (com ressalvas)

---

## Contexto

O `agente-delivery` tentou criar um item de Delivery no ClickUp com `task_type = "Épico"` (nome funcional em português usado internamente). O valor real aceito pela API do workspace é `"Epic"` (inglês). A chamada falhou por completo (nem `task_type` nem descrição foram gravados); o PM identificou o erro sozinho e precisou reenviar campo e descrição manualmente.

O protocolo de observabilidade (`services/observability.md`, decidido em 2026-08-10) só registra entradas "ao término de missões relevantes" e é consolidado mensalmente pelo `agente-evolucao`. O `agente-evolucao` só propõe mudança arquitetural com evidência de padrão recorrente (mínimo 5+ ocorrências) — critério pensado para "criar novo agente", não para "corrigir doc/skill com erro pontual comprovado". Não havia gatilho imediato para esse tipo de falha, e a própria decisão de 2026-08-10 já previa isso: *"se a migração incremental gerar inconsistência recorrente... revisar a convenção"* — este incidente é essa evidência.

**Causa raiz investigada (mais ampla do que a proposta original assumia):** a proposta apontava uma única linha desatualizada em `clickup-config.md:164`. A investigação encontrou o mesmo erro (task_type "Épico" tratado como valor literal, em vez de "Epic") em **8 ocorrências, em 3 arquivos**:
- `.claude/skills/clickup-spec/references/clickup-config.md:164` (regra de inferência, contradizendo a tabela correta na linha 153 do mesmo arquivo)
- `.claude/agents/agente-delivery.md:49, 52, 75, 78, 85` (a própria doc operante do agente, incluindo uma tabela "Tipos de Item — Delivery" que duplica a tabela de `clickup-config.md` e diverge dela)
- `registry/agente-delivery.yaml:40, 46`

Ou seja: o valor do enum de `task_type` não tem fonte única — está declarado de forma independente em 3 lugares, e uma correção anterior (a tabela principal de `clickup-config.md`) não se propagou às outras cópias. Essa duplicação de fonte é a causa estrutural, não apenas uma linha desatualizada.

## Opções Consideradas

1. **Manter o protocolo atual (sem gatilho imediato)** — Prós: nenhuma mudança de processo. Contras: o mesmo bug tem alta chance de recorrer (Delivery é a operação mais frequente do agente), e o próprio precedente de 2026-08-10 já sinalizava que isso deveria ser revisto diante de evidência real.

2. **Gatilho imediato objetivo e ancorado nos campos já existentes do schema de observabilidade (`blocker`, `rework`, `human_intervention`) + fast-track para correção factual trivial comprovada, reservando o pipeline formal de `agente-evolucao` → `agente-governanca` para quando a correção envolve decisão de arquitetura (ex.: definir fonte única) — escolhida.**
   - Prós: fecha o loop sem inflar ritual para erros triviais; usa infraestrutura já existente (schema de observabilidade, `failure_modes` do registry).
   - Contras: depende de autoavaliação do agente no momento da falha (ainda sem telemetria automática); exige critério objetivo bem definido para não virar ruído.

3. **Rotear toda falha operacional (mesmo sem causa em doc) pelo pipeline completo de `agente-evolucao`, imediatamente, sem distinção de gravidade** — Contras: sobrecarga de ritual para qualquer erro pontual, descaracteriza o "imediato" como sinal raro e valioso, risco de auto-justificativa ("a doc que causou" quando na verdade foi julgamento do agente).

## Decisão

Aprovada a Opção 2, com as seguintes ressalvas como mudança mínima necessária:

**R1 — Corrigir todas as 8 ocorrências identificadas, não só a linha ~164.** `clickup-config.md:164`, `agente-delivery.md:49,52,75,78,85` e `registry/agente-delivery.yaml:40,46` devem ser corrigidos na mesma rodada. Corrigir só uma linha deixa a doc operante do próprio agente (`agente-delivery.md`) ainda instruindo a usar `Épico` como valor de `task_type`.

**R2 — Eliminar a duplicação de fonte, não só o valor errado.** `clickup-config.md` → "Tipos de Tarefa por Lista" passa a ser a única fonte de valores de `task_type`. A tabela "Tipos de Item — Delivery" em `agente-delivery.md` (linhas 45–52) deve remeter a essa fonte em vez de redeclarar os valores — senão a próxima atualização do enum se repete só em um lugar e o mesmo drift acontece de novo.

**R3 — Critério objetivo e falsificável para o gatilho imediato**, evitando julgamento subjetivo do agente sobre "foi doc ou fui eu": o gatilho dispara quando `blocker=true` OU `rework=true` OU `human_intervention=true` **E** o valor incorreto é rastreável a um doc/skill referenciada (não a uma inferência livre do agente). Isso reaproveita campos que já existem no schema de `services/observability.md`, sem inventar novo mecanismo.

**R4 — Fast-track para correção factual trivial comprovada** (ID divergente, enum errado, valor rejeitado pela própria API): corrige-se direto no doc + registra-se no log de observabilidade imediatamente, sem esperar aprovação formal prévia de `agente-governanca`. Reserva-se o pipeline pesado de "Proposta de Mudança Arquitetural" (`agente-evolucao` → `agente-governanca`) para quando a correção implica decisão estrutural (ex.: qual arquivo vira fonte única — como neste caso, por isso passou por aqui). Toda correção fast-track continua auditável no log, para revisão retrospectiva por governança se o padrão se repetir.

**R5 — Não duplicar a regra do item 2 da proposta em cada agente operacional.** Regra ("erro causado por doc/skill desatualizada → sinalizar imediato + fast-track de fato comprovado") vive uma vez em `services/observability.md`; `agente-delivery.md`, `agente-dados.md` e futuros agentes operacionais apenas referenciam esse serviço, não reafirmam o texto — repetir o mesmo parágrafo em N arquivos é exatamente o padrão de duplicação que causou este incidente.

Item 3 da proposta original (adicionar `failure_mode` em `registry/agente-delivery.yaml`) é aprovado sem ressalva — já é a convenção documentada em `services/agent-registry.md` ("failure_modes são observados em uso real — adicionar quando identificados").

## Trade-offs Aceitos

- O gatilho imediato ainda depende de autoavaliação do agente (observabilidade continua manual, sem telemetria automática) — mitigado por âncora em campos objetivos do schema (R3), não eliminado.
- O fast-track (R4) permite correção sem aprovação prévia — aceito porque o custo de reverter um texto errado é baixo e o custo de não corrigir rápido (recorrência do mesmo bug em operação frequente) é maior; a auditabilidade retroativa é a rede de segurança.
- Consolidar a fonte única em `clickup-config.md` (R2) exige que quem editar tipos no futuro lembre de editar um lugar só — isso é disciplina editorial, não automação; pode voltar a divergir se não for reforçado.

## O que mudaria a decisão

Se o fast-track (R4) gerar correções malfeitas que precisem ser revertidas, eliminar o fast-track e exigir aprovação de governança mesmo para fatos triviais. Se o critério objetivo do gatilho (R3) gerar falsos negativos (erros reais de doc não capturados) ou falsos positivos (ruído), revisar os campos-âncora do schema de observabilidade.

## Impacto

- **Produto**: nenhuma mudança direta a features; reduz retrabalho manual do PM na criação de itens de Delivery.
- **Técnico**: nenhuma integração nova; edições em docs/config existentes (`clickup-config.md`, `agente-delivery.md`, `registry/agente-delivery.yaml`, `services/observability.md`).
- **Processo**: `services/observability.md` ganha gatilho imediato objetivo + fast-track; `clickup-config.md` vira fonte única do enum `task_type`; `agente-delivery.md`/registry corrigidos nas 8 ocorrências identificadas.

## Links

- Doc afetada: `.claude/skills/clickup-spec/references/clickup-config.md`
- Agente afetado: `.claude/agents/agente-delivery.md`, `registry/agente-delivery.yaml`
- Serviço afetado: `services/observability.md`
- Precedente: [PM Loadout adota contratos de skill e disciplinas operacionais incrementais](2026-08-10-evolucao-operacional-pm-loadout.md)

## Addendum (2026-08-11) — Execução via fast-track (R4) revelou escopo maior

Ao aplicar R1–R5, uma varredura de `Épico` como valor de `task_type` (fora do histórico de decisões, que é registro histórico legítimo) encontrou o mesmo erro em **mais arquivos do que os 8 apontados pela governança**, porque a plataforma mantém **3 árvores de runtime mantidas manualmente em paralelo** para o mesmo conteúdo:

- `.claude/` (Claude Code) — `skills/clickup-spec/SKILL.md` linhas 152, 157, 224, 274 também tinham o valor errado, além dos 8 já corrigidos.
- `.agents/skills/` (mirror para Codex, instalado via `install.sh` em `~/.codex/skills`) — cópia manual de `clickup-config.md` e `SKILL.md`, já divergente do original antes mesmo deste incidente (faltava a seção "Módulo do PAM"), com o mesmo bug de `task_type` nas mesmas 4 linhas.
- `.codex/agents/agente-delivery.toml` (agente para Codex, instalado via `install.sh` em `~/.codex/agents`) — terceira cópia manual do conteúdo de `agente-delivery.md`, com o mesmo bug nas mesmas 5 linhas.

Todas as ocorrências foram corrigidas nesta mesma rodada de fast-track (mesmo fato, mesma correção trivial — não é decisão estrutural nova). O que muda é o diagnóstico: **o "erro pontual" é, na raiz, um sintoma de que não existe geração/sincronização automática entre as 3 árvores** — cada uma é editada e copiada à mão. Isso é maior do que "definir `clickup-config.md` como fonte única" (R2, já decidido): mesmo com fonte única dentro de `.claude/`, as cópias em `.agents/` e `.codex/` continuam podendo divergir a cada novo edit, porque nada as sincroniza.

**Não resolvido nesta decisão** (fora do escopo de fast-track — é decisão de arquitetura de build/instalação, não correção factual): se `.agents/` e `.codex/agents/` devem virar artefato gerado a partir de `.claude/` (script de build no `install.sh`, ou symlink) em vez de fork editado à mão. Proposto como candidato de investigação para `agente-evolucao` → `agente-governanca`.
