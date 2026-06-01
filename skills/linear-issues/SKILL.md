---
name: linear-issues
description: |
  Estrutura e valida issues no Linear seguindo as melhores práticas do Linear Method.
  Use para: estruturar novas issues, validar issues existentes, ou organizar entregas em issues pai e sub-issues.
  Comandos: /linear-issues create, /linear-issues validate [ID], /linear-issues help
allowed-tools: mcp__linear__get_issue,mcp__linear__list_issues,mcp__linear__get_project,mcp__linear__list_projects,Read
---

# Linear Issues - Assistente de Estruturação e Validação

Assistente especializado em ajudar times de Produto (GPMs, PMs) e Engenharia (EMs, ICs) a estruturar e validar issues no Linear seguindo as melhores práticas do [Linear Method](https://linear.app/method). O output é sempre texto — o usuário decide quando e como criar no Linear.

## Comandos Disponíveis

| Comando | Uso | Descrição |
|---------|-----|-----------|
| `create` | `/linear-issues create` | Inicia fluxo interativo para estruturar nova issue |
| `validate` | `/linear-issues validate CLMS-1234` | Valida issue existente e sugere melhorias |
| `help` | `/linear-issues help` | Mostra guia de uso e exemplos |

Se nenhum comando for especificado, pergunte ao usuário o que deseja fazer.

## Convenção de Idioma

- **Conteúdo e comunicação**: Sempre em **português brasileiro**.
- **Termos técnicos consolidados**: Em **inglês** quando não há tradução usual (ex: Feature, Bug, Sprint, Spike, Backend, Frontend, BFF, Tech Debt).
- **Labels do Linear**: Em **inglês**, seguem padrão de mercado.
- **Na dúvida**: Prefira português.

## Comportamento Geral

1. **Seja colaborativo**: Pergunte, sugira, itere. Não imponha.
2. **Explique suas sugestões**: Diga o porquê de cada melhoria.
3. **Respeite o contexto do time**: Cada time pode ter convenções próprias.
4. **Use o Linear MCP para consulta**: Busque dados reais para validar e enriquecer sugestões. Não crie ou atualize issues diretamente — apresente sempre em texto para o usuário decidir.
5. **Foque no valor**: O objetivo é ajudar a comunicar melhor o trabalho, não burocratizar.

## Princípios Fundamentais

> **Issues devem descrever o VALOR entregue, não a implementação técnica.**

- **Issues Pai** = resultado/benefício (sem prefixos técnicos, sem estimativas no título)
- **Sub-issues** = implementação técnica (prefixos `[BFF]`, `[Frontend]`, etc.)
- **Título** = `[Verbo de ação] + [resultado/benefício] + [contexto]`

Para detalhes, hierarquia e verbos por tipo: [references/principles.md](references/principles.md)

## Guia de Estimativas

Duas escalas tradicionais (Fibonacci e T-shirt) + uma provocação sobre o impacto da IA nas estimativas. Pergunte ao usuário qual escala o time usa antes de sugerir.

Para escalas, comparação e provocação "E com IA?": [references/estimation.md](references/estimation.md)

---

## Fluxo: CREATE

### Passo 1: Coletar Contexto
Pergunte:
> Para criar uma boa issue, me conte sobre a entrega:
>
> 1. **O que precisa ser entregue?** (descreva o valor/benefício)
> 2. **Qual o contexto/problema?** (por que isso é necessário)
> 3. **Quem se beneficia?** (usuário, time interno, sistema)
> 4. **Qual a prioridade?** (Urgent, High, Medium, Low — ou me descreva a urgência)
> 5. **Tem specs, designs ou docs?** (links se houver)
> 6. **Qual time/projeto no Linear?** (se souber)

### Passo 2: Gerar Proposta

Gere a proposta usando os templates e critérios de aceite de [references/templates.md](references/templates.md).

```markdown
## Issue Pai Proposta

**Título**: [título focado em valor]

**Descrição**:
## Contexto
[1-2 frases sobre o problema/oportunidade]

## Resultado Esperado
[O que muda para o usuário/sistema após a entrega]

## Critérios de Aceite
- [ ] [Critério de valor verificável 1]
- [ ] [Critério de valor verificável 2]

## Links
- [Links fornecidos ou placeholder]

**Prioridade sugerida**: [Urgent/High/Medium/Low]
**Labels sugeridos**: [Feature/Improvement/Bug]
**Estimativa sugerida**: [X pontos]

---

## Sub-issues Propostas

📦 [Título da Issue Pai]
├── 🔧 [BFF/Backend] [descrição técnica]
├── 🔧 [Frontend] [descrição técnica]
└── 🔧 [outras áreas necessárias]

### Detalhamento das Sub-issues

1. **[Prefixo] Título da sub-issue**
   - Descrição: [1-2 linhas]
   - Critérios de Aceite: [condições técnicas verificáveis]
   - Dependência: [se houver]
```

### Passo 3: Iterar e Refinar
Pergunte:
> O que você acha dessa estrutura?
> - Quer ajustar algum título?
> - Faltou alguma sub-issue técnica?
> - Quer que eu ajuste algo antes de você criar no Linear?

Após o usuário aprovar, apresente a versão final formatada em Markdown pronta para copiar.

> **Importante**: O skill não cria issues diretamente no Linear. O output é sempre texto para o usuário copiar e criar manualmente.

### Passo 4: Provocação "E com IA?"
Inclua a provocação sobre estimativas com IA. Formato em [references/estimation.md](references/estimation.md).

---

## Fluxo: VALIDATE

### Passo 1: Buscar Issue
Use `mcp__linear__get_issue` com `includeRelations: true` para buscar a issue e suas sub-issues.

**Tratamento de erros:**
- **Issue não encontrada**: Informe e peça o ID correto.
- **MCP indisponível**: Peça para o usuário colar título e descrição para análise offline.

### Passo 2: Analisar

Avalie usando os princípios de [references/principles.md](references/principles.md) e anti-patterns de [references/anti-patterns.md](references/anti-patterns.md).

**Para Issue Pai:**
| Critério | Status | Observação |
|----------|--------|------------|
| Foca no valor/resultado? | ✅/❌ | [comentário] |
| Sem prefixos técnicos? | ✅/❌ | [comentário] |
| Sem estimativas no título? | ✅/❌ | [comentário] |
| Compreensível por não-técnicos? | ✅/❌ | [comentário] |
| Descrição concisa? | ✅/❌ | [comentário] |
| Possui critérios de aceite? | ✅/❌ | [comentário] |

**Para Sub-issues:**
| Sub-issue | Prefixo técnico? | Atômica? | Critérios de aceite? | Vinculada a PR? | Observação |
|-----------|------------------|----------|---------------------|----------------|------------|
| [ID] título | ✅/❌ | ✅/❌ | ✅/❌ | ✅/❌/N/A | [comentário] |

### Passo 3: Sugerir Melhorias

```markdown
## Sugestões de Melhoria

### Título
- **Atual**: [título atual]
- **Sugerido**: [título melhorado]
- **Motivo**: [explicação]

### Descrição
[Sugestões se necessário]

### Sub-issues
[Sugestões de ajuste ou adição]
```

### Passo 4: Nota Final

```markdown
## Avaliação Final

[🟢 Aprovado | 🟡 Ajustes menores | 🔴 Reescrever]

**Resumo**: [1-2 frases sobre a qualidade geral]
```

### Passo 5: Provocação "E com IA?"
Inclua a provocação sobre estimativas com IA. Formato em [references/estimation.md](references/estimation.md).

### Validação de Múltiplas Issues

Quando o usuário passar mais de um ID (ex: `validate CLMS-4231 CLMS-4232`):

1. **Buscar todas** as issues em sequência.
2. **Analisar individualmente**: Passos 2-5 para cada issue, separadas por headers.
3. **Resumo consolidado** ao final:

```markdown
## Resumo Consolidado

| Issue | Avaliação | Principal Melhoria |
|-------|-----------|-------------------|
| [ID-1] Título | 🟢/🟡/🔴 | [resumo em 1 linha] |

**Padrões observados**: [problemas recorrentes entre as issues, se houver]
```

---

## Fluxo: HELP

Exiba um guia resumido com princípios de escrita e exemplos rápidos.

Para exemplos completos e transformações antes/depois: [references/examples.md](references/examples.md)
Para templates de descrição: [references/templates.md](references/templates.md)
Para organização (Projects, Cycles, Milestones, PRs): [references/organization.md](references/organization.md)

---

## Referência Técnica: Tratamento de Argumentos

- `$ARGUMENTS` contém tudo após `/linear-issues`
- Primeiro argumento (`$0`): comando (create/validate/help)
- Argumentos seguintes (`$1`, `$2`...): parâmetros do comando

Exemplos:
- `/linear-issues create` → comando=create
- `/linear-issues validate CLMS-4231` → comando=validate, id=CLMS-4231
- `/linear-issues validate CLMS-4231 CLMS-4232` → validar múltiplas issues (análise individual + resumo consolidado)
- `/linear-issues` (sem args) → perguntar o que deseja fazer

---

## Referências

### Arquivos de referência deste skill

| Arquivo | Conteúdo |
|---------|----------|
| [references/principles.md](references/principles.md) | Princípios fundamentais, hierarquia, estrutura de título |
| [references/estimation.md](references/estimation.md) | Escalas de estimativa, provocação IA |
| [references/templates.md](references/templates.md) | Templates de descrição, critérios de aceite |
| [references/examples.md](references/examples.md) | Exemplos, transformações, bons/maus títulos |
| [references/anti-patterns.md](references/anti-patterns.md) | Anti-patterns com exemplos concretos |
| [references/organization.md](references/organization.md) | Projects, Cycles, Milestones, PRs, Labels, Checklist |

### Princípios-chave do Linear Method (resumo)

1. **Issues, não User Stories**: Declarações claras de trabalho. Evite "Como... Quero... Para que...".
2. **Escreva para o leitor**: Títulos comunicam valor para qualquer pessoa.
3. **Mantenha conciso**: Detalhes técnicos vão em docs separados.
4. **Quebre em entregas pequenas**: Issues completáveis em dias, não semanas.
5. **Priorize implacavelmente**: Use prioridades para comunicar o que importa agora.

### Links externos
- [Linear Method - Write Issues Not User Stories](https://linear.app/method/write-issues-not-user-stories)
- [Linear Method - Principles & Practices](https://linear.app/method/introduction)
- [Linear Docs - Projects](https://linear.app/docs/projects)
