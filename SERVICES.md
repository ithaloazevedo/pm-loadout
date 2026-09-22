# Serviços Compartilhados — PM Agentic Platform

Serviços são infraestrutura — não tomam decisões e não são agentes. Fornecem contexto, persistência e rastreabilidade para toda a plataforma.

Especificações detalhadas em `services/`.

---

## Memory Service

| Campo | Valor |
|---|---|
| **Localização** | Memória do runtime (Claude ou Codex); fatos duráveis no Knowledge Graph |
| **Responsabilidade** | Histórico de sessões, decisões, preferências, contexto do usuário |
| **Como consumir** | Use o contexto da tarefa; não assuma um caminho privado de memória |
| **Spec** | [services/memory.md](services/memory.md) |

---

## Knowledge Graph

| Campo | Valor |
|---|---|
| **Localização** | `knowledge/` |
| **Responsabilidade** | Fonte única de verdade sobre domínios: Produto, Negócio, Engenharia, Operação, Pessoas, Processo |
| **Como consumir** | Agentes leem os arquivos de domínio relevantes antes de responder |
| **Spec** | [knowledge/README.md](knowledge/README.md) |

---

## Decision Log

| Campo | Valor |
|---|---|
| **Localização** | `knowledge/decisions/` |
| **Responsabilidade** | Registrar decisões importantes com justificativa, trade-offs e contexto |
| **Como consumir** | Usar template `knowledge/decisions/TEMPLATE.md`; indexar em `INDEX.md` |
| **Spec** | [services/decision-log.md](services/decision-log.md) |

---

## Prompt Library

| Campo | Valor |
|---|---|
| **Localização** | `prompts/` |
| **Responsabilidade** | Centralizar prompts reutilizáveis: routing, context injection, handoff |
| **Como consumir** | Agentes referenciam arquivos de `prompts/` quando precisam de padrões estabelecidos |
| **Spec** | [services/prompt-library.md](services/prompt-library.md) |

---

## Templates

| Campo | Valor |
|---|---|
| **Localização** | Claude: `.claude/skills/clickup-spec/references/template-*.md` · Codex: `.agents/skills/clickup-spec/references/template-*.md` |
| **Responsabilidade** | Template de Delivery (Discovery hoje são seções incorporadas a esse template, não um item separado); template de Objetivo/Roadmap Item mantido só como histórico, deprecado desde a remoção de OKRs formais em 2026-09-10 |
| **Como consumir** | `agente-spec` e `agente-delivery` referenciam ao criar artefatos |

---

## Agent Registry

| Campo | Valor |
|---|---|
| **Localização** | `registry/` |
| **Responsabilidade** | Registro YAML de cada agente: missão, inputs, outputs, tools, dependências, métricas de sucesso |
| **Como consumir** | Leitura por humanos e pelo Agente de Evolução para auditar a arquitetura |
| **Spec** | [services/agent-registry.md](services/agent-registry.md) |

---

## Observabilidade

| Campo | Valor |
|---|---|
| **Localização** | `services/observability.md` (schema) |
| **Responsabilidade** | Registrar interações: agente usado, tempo, resultado, falhas, retrabalho |
| **Status** | Definido em spec; implementação completa em V2 |
| **Spec** | [services/observability.md](services/observability.md) |
