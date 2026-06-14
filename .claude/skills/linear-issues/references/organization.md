# Organização: Projects, Cycles, Milestones, PRs, Labels e Checklist

## Conteúdo
- Projects e Cycles
- Milestones
- Vinculação a Pull Requests
- Labels recomendados
- Checklist de revisão

---

## Projects e Cycles

### Quando vincular a um Project
- Issues que fazem parte de uma **entrega maior com escopo definido** devem ser vinculadas a um Project.
- Se o usuário não souber o projeto, pergunte: "Essa entrega faz parte de alguma iniciativa maior? (ex: migração, redesign, novo módulo)"

### Quando vincular a um Cycle
- Issues planejadas para uma **sprint/ciclo específico** devem ser vinculadas ao Cycle correspondente.
- Se o time trabalha com Cycles, pergunte: "Essa issue deve entrar no ciclo atual ou no próximo?"

### Quando usar Milestones
Milestones são **marcos de progresso dentro de um Project**. Representam entregas intermediárias com data-alvo, ajudando a quebrar projetos grandes em checkpoints verificáveis.

- Use milestones quando um Project tem **entregas faseadas** (ex: "Fase 1 — MVP", "Fase 2 — Integrações", "Fase 3 — Rollout")
- Cada milestone deve ter uma **data-alvo** e um conjunto claro de issues que precisam ser concluídas para atingi-lo
- Milestones **não substituem** Cycles — cycles são períodos de tempo (sprints), milestones são pontos de entrega

**Quando usar:**

| Cenário | Milestone? | Exemplo |
|---------|-----------|---------|
| Projeto com entregas faseadas | Sim | "MVP do novo checkout entregue até 15/03" |
| Dependência externa com prazo | Sim | "Integração com parceiro X pronta até go-live" |
| Sprint planning regular | Não (usar Cycle) | "Sprint 12 — 01/03 a 15/03" |
| Issue avulsa sem projeto | Não | Bug fix pontual |

**Pergunte ao usuário**: "Esse projeto tem marcos intermediários de entrega? (ex: MVP, beta, go-live)"

### Hierarquia no Linear

```
🏢 Project (iniciativa/entrega grande)
├── 🏁 Milestone 1 — "MVP" (data-alvo: 15/03)
│   ├── 📦 Issue Pai A
│   │   ├── 🔧 Sub-issue 1
│   │   └── 🔧 Sub-issue 2
│   └── 📦 Issue Pai B
│       └── 🔧 Sub-issue 3
├── 🏁 Milestone 2 — "Integrações" (data-alvo: 30/04)
│   └── 📦 Issue Pai C
│       └── 🔧 Sub-issue 4
└── 📦 Issues sem milestone (backlog do projeto)

🔄 Cycle (sprint/período)
├── 📦 Issue de Project A (milestone 1)
├── 📦 Issue de Project B (milestone 2)
└── 📦 Issue avulsa (sem projeto)
```

---

## Vinculação a Pull Requests

Issues e sub-issues devem ser vinculadas aos PRs que implementam suas entregas. Isso garante rastreabilidade entre o **que foi planejado** e o **que foi implementado**.

### Quando vincular

| Tipo | Vincula a PR? | Como |
|------|--------------|------|
| **Sub-issue** | Sim, sempre | Cada sub-issue deve ter pelo menos 1 PR vinculado |
| **Issue Pai** | Não diretamente | É fechada quando todas as sub-issues estão concluídas |
| **Bug Fix** (sem sub-issues) | Sim | PR vinculado diretamente à issue |
| **Spike** | Opcional | Vincular se houver POC com código |

### Convenção de Branch

Referencie o ID da issue no nome da branch:

```
feat/CLMS-4231-validar-codigo-2fa
fix/CLMS-4500-corrigir-timeout-api
chore/CLMS-4600-atualizar-dependencias
```

**Formato**: `<tipo>/<ID-issue>-<descricao-curta>`

### Referência no PR

Mencione o ID da issue no título ou corpo do PR para ativar a vinculação automática do Linear:

```markdown
# Título do PR
[CLMS-4289] Criar endpoint /login/2fa/verify

# Ou no corpo do PR
Closes CLMS-4289
```

### Fluxo de Fechamento

```
📦 Issue Pai: Validar código 2FA e liberar acesso ao Portal
│   Status: In Progress → Done (automático quando sub-issues fecham)
│
├── 🔧 [BFF] Criar endpoint /login/2fa/verify
│   └── PR #142 → merged → sub-issue fecha automaticamente
│
├── 🔧 [Frontend] Criar tela de código 2FA
│   └── PR #145 → merged → sub-issue fecha automaticamente
│
└── 🔧 [Frontend] Exibir erro quando código inválido
    └── PR #145 (mesmo PR) → merged → sub-issue fecha automaticamente
```

> **Nota**: Múltiplas sub-issues podem ser resolvidas pelo mesmo PR quando fazem parte da mesma implementação.

---

## Labels Recomendados

### Por Tipo de Entrega

| Label | Uso |
|-------|-----|
| `Feature` | Nova funcionalidade |
| `Improvement` | Melhoria em funcionalidade existente |
| `Bug` | Correção de defeito |
| `Tech Debt` | Débito técnico |
| `Spike` | Investigação/pesquisa técnica |

### Por Área Técnica (para sub-issues)

| Label | Uso |
|-------|-----|
| `Frontend` | Alterações no cliente |
| `Backend` | Alterações em APIs/serviços |
| `BFF` | Backend for Frontend |
| `Infra` | Infraestrutura e DevOps |
| `Data` | Pipelines e dados |

---

## Checklist de Revisão

### Para Issue Pai

- [ ] Título descreve valor/resultado, não implementação
- [ ] Qualquer pessoa do time entende o benefício
- [ ] Sem prefixos técnicos (`[BFF]`, `[Frontend]`, etc.)
- [ ] Sem estimativas no título (usar campo dedicado)
- [ ] Descrição tem apenas o contexto necessário
- [ ] Critérios de aceite presentes e verificáveis

### Para Sub-issues

- [ ] Prefixo técnico indica a área: `[BFF]`, `[Frontend]`, `[API]`, `[Infra]`
- [ ] Descreve uma entrega atômica e verificável
- [ ] Vinculada à issue pai correta
- [ ] Atribuída ao responsável técnico
- [ ] Critérios de aceite técnicos definidos
- [ ] Vinculada a PR (quando implementação iniciada)
