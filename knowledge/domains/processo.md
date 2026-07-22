# Domínio: Processo

Descreve como o trabalho de produto flui — as esteiras, os tipos de item e as convenções do processo.

---

## Esteiras de Produto

O processo de produto da Vertical Tech tem duas esteiras principais:

### Discovery
Pesquisa, prototipação e definição de escopo. Antecede o Delivery.

**Tipos de item no ClickUp**:
- **Pesquisa**: exploração qualitativa ou quantitativa de um problema/oportunidade
- **Protótipo**: validação de solução via Figma (nunca código nesta fase)
- **Entrevista**: sessão estruturada com usuário real

**Status**: `to do` → `em progresso` → `em validação` → `pronto` → `complete`

**Critério de saída**: problema validado, escopo definido, hipóteses testadas.

### Delivery
Construção e entrega de valor. Downstream do Discovery.

**Tipos de item no ClickUp**:

| Tipo | Quando usar | Escopo típico |
|---|---|---|
| **Épico** | Entrega grande de valor, nova funcionalidade, grande implementação | Múltiplas sprints |
| **Tarefa** | Ajuste simples, pequena entrega de valor, escopo reduzido | Uma sprint ou menos |
| **Bug** | Problema em produção afetando o sistema ou o usuário final | Urgente — prioridade alta |
| **Correção** | Subtarefa de Épico ou Tarefa criada após homologação (bug pós-entrega, inconformidade com protótipo, critério de aceite não cumprido) | Pequena — integrada ao item pai |

**Status (Backlog)**: `backlog` → `em refinamento` → `pronto p/ execução` → `priorizado` → `complete` / `cancelado`

**Status (Execução)**: `to do` → `em desenvolvimento` → `bloqueada` → `em revisão técnica` → `em homologação` → `aguardando deploy` → `pronto` / `finalizado`

---

## Hierarquia do Processo

```
Objetivo (OKR/KR)
  ├→ Projeto de Discovery
  └→ Projeto de Delivery
       ├→ Épico
       ├→ Tarefa
       ├→ Bug
       └→ Correção (subtarefa de Épico ou Tarefa)
```

**Não existe nível Iniciativa.** Projetos de Discovery e Delivery são vinculados diretamente aos Objetivos quando relevante.

---

## Fluxo de Status das Iniciativas (Roadmap — depreciado)

> A lista "Iniciativas" no Roadmap do ClickUp foi mantida apenas como referência histórica. O processo atual não usa mais este nível.

---

## Squads

| Squad | Folder no ClickUp | Responsabilidade |
|---|---|---|
| **Experiência do jogador** | Delivery: Experiência do jogador | PAM — front do usuário final |
| **Operação e afiliados** | Delivery: Operação e afiliados | Backoffice — operações internas |
| **Provedora de conteúdo** | Delivery: Provedora de conteúdo | Jogos — integração com provedoras |

---

## Convenções

- **Nomes de cards**: em linguagem do usuário, não técnica. "Estrutura base" e não "Shell". "Limite de apostas" e não "bet_limit_config".
- **Prototipação**: sempre em Figma, nunca em código durante Discovery.
- **Critérios de aceite**: propostos pelo PM, refinados com engineering e QA.
- **Fonte única de spec**: o card no ClickUp. Não criar PRD paralelo no Drive.
