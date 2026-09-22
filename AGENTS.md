# Catálogo de Agentes — PM Agentic Platform

Para Claude Code, os perfis vivem em `.claude/agents/`. Para Codex, os perfis equivalentes vivem em `.codex/agents/` e as skills em `.agents/skills/`. O registro completo com schema YAML está em `registry/`.

## Orquestrador

| Campo | Valor |
|---|---|
| **Skill** | `/orquestrador` |
| **Skill Claude** | `.claude/skills/orquestrador/SKILL.md` |
| **Skill Codex** | `.agents/skills/orquestrador/SKILL.md` |
| **Missão** | Ponto de entrada único. Identifica estágio da missão, equipa skills, coordena especialistas. |
| **Inputs** | Qualquer pedido de produto |
| **Outputs** | Missão nomeada, loadout equipado, síntese, artefato, próxima ação |
| **Não é agente** | É uma skill — instrui o agente principal (Claude ou Codex), que atua como orquestrador |

---

## Agentes Especialistas

### Agente Estratégico
| Campo | Valor |
|---|---|
| **Arquivo** | Claude: `.claude/agents/agente-estrategico.md` · Codex: `.codex/agents/agente-estrategico.toml` |
| **Missão** | Priorização, sequenciamento e rationale estratégico |
| **Inputs** | Métricas, contexto de negócio, opções em disputa |
| **Outputs** | Aposta recomendada, sequenciamento, confiança, trade-offs, evidência que mudaria a decisão |
| **Skills** | `ice`, `gist`, `wardley`, `cynefin`, `advogado-do-diabo` |
| **Handoff →** | `agente-discovery` (evidências), `agente-spec` (spec), `vigilancia-regulatoria` (risco regulatório) |

### Agente de Discovery
| Campo | Valor |
|---|---|
| **Arquivo** | Claude: `.claude/agents/agente-discovery.md` · Codex: `.codex/agents/agente-discovery.toml` |
| **Missão** | Investigação de usuários, necessidades, jobs, evidências e suposições |
| **Inputs** | Espaço de problema vago, entrevistas, notas de pesquisa, sinais de suporte |
| **Outputs** | Evidência, necessidade do usuário, oportunidade, risco de suposição, próxima ação de pesquisa |
| **Skills** | `entrevista`, `entrevista-usuario`, `jtbd`, `mapa-necessidades`, `suposicoes`, `ost`, `vieses` |
| **Handoff →** | `agente-estrategico` (priorização), `agente-spec` (spec após validação) |

### Agente de Spec
| Campo | Valor |
|---|---|
| **Arquivo** | Claude: `.claude/agents/agente-spec.md` · Codex: `.codex/agents/agente-spec.toml` |
| **Missão** | Transformar pensamento de produto em artefatos precisos no ClickUp |
| **Inputs** | Decisão de produto, ideia, oportunidade validada |
| **Outputs** | Projeto de Discovery ou Delivery estruturado, critérios de aceite, escopo |
| **Skills** | `clickup-spec`, `brainstorming`, `checar-servico`, `checar-usabilidade` |
| **Handoff →** | `agente-delivery` (execução no ClickUp) |

### Agente de Delivery
| Campo | Valor |
|---|---|
| **Arquivo** | Claude: `.claude/agents/agente-delivery.md` · Codex: `.codex/agents/agente-delivery.toml` |
| **Missão** | Operar o processo no ClickUp — criar, estruturar, vincular e auditar Discovery/Delivery |
| **Inputs** | Spec pronta, pedido de criação/update no ClickUp |
| **Outputs** | Items criados/alterados (VL-XXXXX), campos gravados, pendências, próximo passo |
| **Skills** | `clickup-spec`, `clickup-revisa-sprint`, `gist`, `ice` |
| **Handoff →** | `vigilancia-regulatoria` (risco regulatório), `agente-governanca` (decisão arquitetural) |

### Agente de Insights
| Campo | Valor |
|---|---|
| **Arquivo** | Claude: `.claude/agents/agente-insights.md` · Codex: `.codex/agents/agente-insights.toml` |
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
| **Arquivo** | Claude: `.claude/agents/agente-governanca.md` · Codex: `.codex/agents/agente-governanca.toml` |
| **Missão** | Desafiar raciocínio fraco, riscos de qualidade, e avaliar mudanças arquiteturais |
| **Inputs** | Spec, decisão, artefato, proposta de mudança arquitetural |
| **Outputs** | Objeções, riscos, mitigações, veredicto (APROVAR / COM RESSALVAS / BLOQUEAR) |
| **Skills** | `advogado-do-diabo`, `checar-servico`, `checar-usabilidade`, `vieses`, `nivel-lancamento` |

### Agente de Evolução
| Campo | Valor |
|---|---|
| **Arquivo** | Claude: `.claude/agents/agente-evolucao.md` · Codex: `.codex/agents/agente-evolucao.toml` |
| **Missão** | Observar o sistema, identificar gargalos, sobreposições e sugerir mudanças arquiteturais |
| **Inputs** | Histórico de uso, padrões recorrentes, observações do Orquestrador |
| **Outputs** | Diagnóstico do sistema, sugestão de mudança arquitetural (novo agente, fusão, remoção) |
| **Handoff →** | `agente-governanca` (validação da sugestão) |

---

## Agentes Especializados

### Curador de Contexto
| Campo | Valor |
|---|---|
| **Arquivo** | Claude: `.claude/agents/curador-de-contexto.md` · Codex: `.codex/agents/curador-de-contexto.toml` |
| **Missão** | Buscar context pack no claude-os no início de missão; propor MR com conhecimento durável ao fim |

### Vigilância Regulatória
| Campo | Valor |
|---|---|
| **Arquivo** | Claude: `.claude/agents/vigilancia-regulatoria.md` · Codex: `.codex/agents/vigilancia-regulatoria.toml` |
| **Missão** | Monitoramento legal/regulatório para bets BR, SIGAP, KYC/AML, Portarias SPA/MF |

### Prontidão IA
| Campo | Valor |
|---|---|
| **Arquivo** | Claude: `.claude/agents/prontidao-ia.md` · Codex: `.codex/agents/prontidao-ia.toml` |
| **Missão** | Avaliar readiness de features com ML/LLM/automação em 8 dimensões |

### Agente de Dados
| Campo | Valor |
|---|---|
| **Arquivo** | Claude: `.claude/agents/agente-dados.md` · Codex: `.codex/agents/agente-dados.toml` |
| **Missão** | Traduzir pergunta de negócio em SQL somente-leitura contra os bancos `trad_prd` (Tradicional) e `ar_bravo_prd` (Bravo), com aprovação explícita antes de executar |
| **Inputs** | Pergunta de negócio em linguagem natural; de qual casa (Tradicional/Bravo); fatura de fornecedor a conciliar |
| **Outputs** | SQL proposto, casa consultada, resultado interpretado em termos de negócio, ressalvas de período/PII |
| **Skills** | `query-trad` (banco Tradicional), `query-bravo` (banco Bravo), `auditoria-fornecedores` (conciliação de fatura de fornecedor — KYC, CPF Check, provedor de jogos, agregador — nas duas casas) |

---

## Painel Banca (3 Lentes)

No Claude, é invocado via `Workflow({name:"banca"})`. No Codex, o orquestrador delega em paralelo às três lentes e consolida os veredictos.

| Agente | Perspectiva |
|---|---|
| Produto | Claude: `.claude/agents/lente-produto.md` · Codex: `.codex/agents/lente-produto.toml` — estratégia, evidência, custo de oportunidade |
| Design | Claude: `.claude/agents/lente-design.md` · Codex: `.codex/agents/lente-design.toml` — UX, coerência, acessibilidade |
| Tech | Claude: `.claude/agents/lente-tech.md` · Codex: `.codex/agents/lente-tech.toml` — viabilidade, arquitetura, segurança |
