# PM Agentic Platform — Arquitetura

## Visão

Plataforma de Product Management orientada por agentes. Transforma conhecimento organizacional em ação estruturada, com rastreabilidade, governança e capacidade de auto-evolução.

## Camadas

```
                        Usuário
                           │
                           ▼
                    Orquestrador          ← único ponto de entrada
                           │
      ┌────────────┬────────────┬────────────┬────────────┐
      ▼            ▼            ▼            ▼            ▼
  Estratégico  Discovery     Spec        Delivery    Insights

──────────────────────────────────────────────────────────────
                  Serviços Compartilhados
──────────────────────────────────────────────────────────────
  Knowledge Graph · Memory · Decision Log · Prompt Library
  Templates · Agent Registry · Observabilidade

──────────────────────────────────────────────────────────────
                   Meta Intelligence
──────────────────────────────────────────────────────────────
          Agente de Evolução · Agente de Governança
```

## Princípios

### 1. Responsabilidade única
Cada agente resolve apenas um domínio. Nunca criar agentes genéricos. Evitar sobreposição.

### 2. Contexto compartilhado
Nenhum agente possui conhecimento próprio. Todo contexto vem de:
- Knowledge Graph (`knowledge/`)
- Memory (Claude built-in)
- Decision Log (`knowledge/decisions/`)

### 3. Orquestrador como único ponto de entrada
O usuário nunca conversa diretamente com agentes especialistas. Toda comunicação passa pelo Orquestrador (`/orquestrador`).

### 4. Serviços ≠ Agentes
Tudo que não toma decisão não é agente. Memory, Registry, Templates, Prompt Library e Knowledge Graph são serviços.

### 5. Evolução incremental
Criar novos agentes só com evidência clara de necessidade. Governança avalia cada mudança arquitetural.

## Agentes

Ver [AGENTS.md](AGENTS.md) para o catálogo completo com inputs, outputs e handoff rules.

## Serviços

Ver [SERVICES.md](SERVICES.md) para a especificação de cada serviço compartilhado.

## Knowledge Graph

Ver [knowledge/README.md](knowledge/README.md) para estrutura de domínios e relações.

## Registry

Ver [registry/](registry/) para o registro YAML de cada agente.

## Fluxo Geral

```
Usuário
  ↓
Orquestrador
  ↓
Consulta Knowledge Graph
  ↓
Consulta Memory
  ↓
Seleciona Agente Especialista
  ↓
Agente produz resposta
  ↓
Resposta validada
  ↓
Atualiza Decision Log
  ↓
Atualiza Knowledge Graph (se necessário)
  ↓
Observabilidade registra tudo
```

## Roadmap de Evolução

### V1 — Fundação (atual)
- Orquestrador
- Knowledge Graph
- Memory
- Agente Estratégico, Agente de Discovery, Agente de Spec, Agente de Delivery, Agente de Insights

### V2 — Rastreabilidade
- Decision Log operacional
- Observabilidade completa
- Templates centralizados
- Agent Registry automatizado
- Prompt Library

### V3 — Auto-evolução
- Agente de Evolução observando padrões de uso
- Agente de Governança avaliando mudanças
- Sugestão automática de novos agentes
- Autoavaliação da arquitetura

## Critérios de Sucesso

A plataforma será bem-sucedida quando:

- Todo conhecimento do produto estiver conectado ao Knowledge Graph.
- Os agentes utilizarem contexto compartilhado, sem duplicação de memória.
- O Orquestrador conseguir selecionar automaticamente o especialista correto.
- O sistema registrar decisões e histórico de forma rastreável.
- A plataforma conseguir evoluir novos agentes com base em evidências de uso.
- A manutenção da arquitetura permanecer simples, modular e escalável.
