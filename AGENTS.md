# Catálogo de Agentes — PM Agentic Platform

Todos os agentes vivem em `.claude/agents/`. O registro completo com schema YAML está em `registry/`.

## Orquestrador

| Campo | Valor |
|---|---|
| **Skill** | `/orquestrador` |
| **Arquivo** | `.claude/skills/orquestrador/SKILL.md` |
| **Missão** | Ponto de entrada único. Identifica estágio da missão, equipa skills, coordena especialistas. |
| **Inputs** | Qualquer pedido de produto |
| **Outputs** | Missão nomeada, loadout equipado, síntese, artefato, próxima ação |
| **Não é agente** | É uma skill — instrui o Claude principal, que atua como orchestrator |

---

## Agentes Especialistas

### Agente Estratégico
| Campo | Valor |
|---|---|
| **Arquivo** | `.claude/agents/agente-estrategico.md` |
| **Missão** | Priorização, sequenciamento e rationale estratégico |
| **Inputs** | Objetivos, métricas, opções em disputa |
| **Outputs** | Aposta recomendada, sequenciamento, confiança, trade-offs, evidência que mudaria a decisão |
| **Skills** | `ice`, `gist`, `wardley`, `cynefin`, `advogado-do-diabo` |
| **Handoff →** | `agente-discovery` (evidências), `agente-spec` (spec), `vigilancia-regulatoria` (risco regulatório) |

### Agente de Discovery
| Campo | Valor |
|---|---|
| **Arquivo** | `.claude/agents/agente-discovery.md` |
| **Missão** | Investigação de usuários, necessidades, jobs, evidências e suposições |
| **Inputs** | Espaço de problema vago, entrevistas, notas de pesquisa, sinais de suporte |
| **Outputs** | Evidência, necessidade do usuário, oportunidade, risco de suposição, próxima ação de pesquisa |
| **Skills** | `entrevista`, `entrevista-usuario`, `jtbd`, `mapa-necessidades`, `suposicoes`, `ost`, `vieses` |
| **Handoff →** | `agente-estrategico` (priorização), `agente-spec` (spec após validação) |

### Agente de Spec
| Campo | Valor |
|---|---|
| **Arquivo** | `.claude/agents/agente-spec.md` |
| **Missão** | Transformar pensamento de produto em artefatos precisos no ClickUp |
| **Inputs** | Decisão de produto, ideia, oportunidade validada |
| **Outputs** | Projeto de Discovery ou Delivery estruturado, critérios de aceite, escopo |
| **Skills** | `clickup-spec`, `brainstorming`, `checar-servico`, `checar-usabilidade` |
| **Handoff →** | `agente-delivery` (execução no ClickUp) |

### Agente de Delivery
| Campo | Valor |
|---|---|
| **Arquivo** | `.claude/agents/agente-delivery.md` |
| **Missão** | Operar o processo no ClickUp — criar, estruturar, vincular e auditar Discovery/Delivery |
| **Inputs** | Spec pronta, pedido de criação/update no ClickUp |
| **Outputs** | Items criados/alterados (VL-XXXXX), campos gravados, pendências, próximo passo |
| **Skills** | `clickup-spec`, `clickup-rollup`, `gist`, `ice` |
| **Handoff →** | `vigilancia-regulatoria` (risco regulatório), `agente-governanca` (decisão arquitetural) |

### Agente de Insights
| Campo | Valor |
|---|---|
| **Arquivo** | `.claude/agents/agente-insights.md` |
| **Missão** | Sinais de sucesso, loops de aprendizado, métricas e retrospectivas |
| **Inputs** | Lançamento a monitorar, ciclo encerrado, pergunta de mensuração |
| **Outputs** | Métrica principal, guardrails, lacunas de instrumentação, cadência de aprendizado |
| **Skills** | `metricas`, `nivel-lancamento`, `retrospectiva`, `ice`, `suposicoes` |
| **Handoff →** | `agente-estrategico` (re-priorização pós-aprendizado) |

---

## Agentes de Governança e Evolução

### Agente de Governança
| Campo | Valor |
|---|---|
| **Arquivo** | `.claude/agents/agente-governanca.md` |
| **Missão** | Desafiar raciocínio fraco, riscos de qualidade, e avaliar mudanças arquiteturais |
| **Inputs** | Spec, decisão, artefato, proposta de mudança arquitetural |
| **Outputs** | Objeções, riscos, mitigações, veredicto (APROVAR / COM RESSALVAS / BLOQUEAR) |
| **Skills** | `advogado-do-diabo`, `checar-servico`, `checar-usabilidade`, `vieses`, `nivel-lancamento` |

### Agente de Evolução
| Campo | Valor |
|---|---|
| **Arquivo** | `.claude/agents/agente-evolucao.md` |
| **Missão** | Observar o sistema, identificar gargalos, sobreposições e sugerir mudanças arquiteturais |
| **Inputs** | Histórico de uso, padrões recorrentes, observações do Orquestrador |
| **Outputs** | Diagnóstico do sistema, sugestão de mudança arquitetural (novo agente, fusão, remoção) |
| **Handoff →** | `agente-governanca` (validação da sugestão) |

---

## Agentes Especializados

### Curador de Contexto
| Campo | Valor |
|---|---|
| **Arquivo** | `.claude/agents/curador-de-contexto.md` |
| **Missão** | Buscar context pack no claude-os no início de missão; propor MR com conhecimento durável ao fim |

### Vigilância Regulatória
| Campo | Valor |
|---|---|
| **Arquivo** | `.claude/agents/vigilancia-regulatoria.md` |
| **Missão** | Monitoramento legal/regulatório para bets BR, SIGAP, KYC/AML, Portarias SPA/MF |

### Prontidão IA
| Campo | Valor |
|---|---|
| **Arquivo** | `.claude/agents/prontidao-ia.md` |
| **Missão** | Avaliar readiness de features com ML/LLM/automação em 8 dimensões |

---

## Painel Banca (3 Lentes)

Invocado via `Workflow({name:"banca"})`. Roda em paralelo e retorna veredicto consolidado.

| Agente | Perspectiva |
|---|---|
| `.claude/agents/lente-produto.md` | Head de Produto — estratégia, evidência, custo de oportunidade |
| `.claude/agents/lente-design.md` | Head de Design — UX, coerência, acessibilidade |
| `.claude/agents/lente-tech.md` | Head de Tecnologia — viabilidade, arquitetura, segurança |
