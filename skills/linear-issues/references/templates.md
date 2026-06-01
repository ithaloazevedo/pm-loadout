# Templates de Descrição e Critérios de Aceite

## Conteúdo
- Templates: Feature, Bug Fix, Improvement, Tech Debt, Spike
- Critérios de aceite: princípios, exemplos por tipo, dicas

---

## Templates de Descrição

### Feature

```markdown
## Contexto
[1-2 frases sobre a necessidade ou oportunidade]

## Resultado Esperado
[O que muda para o usuário/sistema após a entrega]

## Critérios de Aceite
[ver seção "Critérios de Aceite" abaixo para exemplos por tipo]

## Links
- [Spec/RFC](link)
- [Design no Figma](link)
```

### Bug Fix

```markdown
## Problema
[Descrição do comportamento incorreto]

## Comportamento Esperado
[Como deveria funcionar]

## Como Reproduzir
1. [Passo 1]
2. [Passo 2]

## Critérios de Aceite
[ver seção "Critérios de Aceite" abaixo para exemplos por tipo]

## Links
- [Log de erro](link)
- [Ticket de suporte](link)
```

### Improvement

```markdown
## Situação Atual
[Como está hoje e por que precisa melhorar]

## Melhoria Proposta
[O que será diferente após a entrega]

## Critérios de Aceite
[ver seção "Critérios de Aceite" abaixo para exemplos por tipo]

## Métricas de Sucesso
- [Métrica 1]
- [Métrica 2]
```

### Tech Debt

```markdown
## Débito Técnico
[Descrição do problema técnico]

## Impacto se Não Resolver
- [Risco 1]
- [Risco 2]

## Solução Proposta
[Abordagem técnica resumida]

## Critérios de Aceite
[ver seção "Critérios de Aceite" abaixo para exemplos por tipo]
```

### Spike (Investigação Técnica)

```markdown
## Objetivo da Investigação
[Pergunta ou hipótese a ser validada]

## Contexto
[Por que essa investigação é necessária agora]

## Perguntas a Responder
1. [Pergunta 1]
2. [Pergunta 2]
3. [Pergunta 3]

## Timebox
[Duração máxima: ex. 2 dias, 1 sprint]

## Entregável Esperado
[O que será produzido: RFC, POC, documento de decisão, etc.]

## Próximos Passos (pós-spike)
- Se viável: [ação]
- Se inviável: [ação alternativa]
```

---

## Critérios de Aceite

Critérios de aceite definem **quando uma issue está "done"**. Devem ser escritos como condições verificáveis — algo que qualquer pessoa do time consiga testar e confirmar.

### Princípios

- **Verificáveis**: Cada critério deve poder ser respondido com "sim" ou "não".
- **Focados no comportamento**: Descreva o que o sistema faz, não como foi implementado.
- **Independentes**: Cada critério deve ser testável isoladamente.
- **Presentes em todos os tipos**: Issues pai, sub-issues, features, bugs — todas se beneficiam de critérios claros.

### Para Issues Pai (foco no valor)

Critérios de alto nível que validam o resultado entregue ao usuário:

```markdown
## Critérios de Aceite
- [ ] Usuário consegue filtrar turmas por segmento na listagem
- [ ] Filtro selecionado persiste ao navegar entre páginas
- [ ] Tela carrega em menos de 2s com filtro aplicado
```

### Para Sub-issues (foco técnico)

Critérios específicos da implementação técnica:

```markdown
## Critérios de Aceite
- [ ] Endpoint GET /api/turmas aceita query param `segmento`
- [ ] Resposta filtrada retorna apenas turmas do segmento informado
- [ ] Retorna 400 se segmento inválido
- [ ] Testes unitários cobrindo cenários de filtro
```

### Para Bug Fixes

Critérios que confirmam a correção e ausência de regressão:

```markdown
## Critérios de Aceite
- [ ] Notificação é entregue ao perfil administrativo em até 30s
- [ ] Notificações para outros perfis continuam funcionando normalmente
- [ ] Log de erro não aparece mais no Datadog após deploy
```

### Para Spikes

Critérios que validam o entregável da investigação:

```markdown
## Critérios de Aceite
- [ ] Documento de decisão publicado com prós/contras das alternativas
- [ ] POC funcional demonstrando viabilidade (ou documento explicando inviabilidade)
- [ ] Próximos passos definidos e issues de follow-up criadas
```

### Dicas de Escrita

| Bom | Ruim |
|-----|------|
| "Usuário vê mensagem de erro ao digitar código inválido" | "Tratar erros" |
| "Tempo de resposta < 2s para 1000+ registros" | "Melhorar performance" |
| "Email de confirmação enviado em até 1 minuto" | "Enviar email" |
| "Componente renderiza sem erros no console" | "Funcionar corretamente" |
