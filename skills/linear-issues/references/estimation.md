# Guia de Estimativas

## Conteúdo
- Escala Fibonacci
- T-shirt Sizing
- Quando usar cada escala
- Equivalência aproximada
- Provocação: Estimativas na Era da IA

---

Estimativas refletem **complexidade, incerteza e esforço** — não horas exatas. Existem duas escalas comuns:

## Escala Fibonacci (Pontos de Complexidade)

Melhor para times que querem **granularidade** e usam velocity para planejamento de sprints.

| Pontos | Complexidade | Referência |
|--------|-------------|------------|
| 1 | Trivial | Ajuste de texto, config simples |
| 2 | Pequena | Alteração isolada em 1 componente/endpoint |
| 3 | Moderada | Alteração em 2-3 arquivos, lógica conhecida |
| 5 | Significativa | Feature nova com frontend + backend |
| 8 | Complexa | Feature cross-team, integrações, incerteza moderada |
| 13 | Muito complexa | Múltiplas dependências, alta incerteza |

## T-shirt Sizing

Melhor para times que preferem **simplicidade** e estimativas rápidas, sem debates prolongados sobre números.

| Tamanho | Complexidade | Referência |
|---------|-------------|------------|
| XS | Trivial | Ajuste de texto, config, typo |
| S | Pequena | Alteração isolada, lógica simples e conhecida |
| M | Moderada | Feature pequena, 2-3 componentes envolvidos |
| L | Grande | Feature completa com frontend + backend |
| XL | Muito grande | Épico, múltiplas integrações, alta incerteza |

## Quando usar cada escala

| Critério | Fibonacci | T-shirt |
|----------|-----------|---------|
| **Planejamento de sprint** | Melhor — permite calcular velocity | Funciona, mas menos preciso |
| **Estimativas rápidas** | Pode gerar debate sobre 3 vs 5 | Melhor — decisão mais rápida |
| **Times novos em estimativas** | Curva de aprendizado maior | Mais intuitivo para começar |
| **Relatórios e métricas** | Melhor — dados numéricos para gráficos | Precisa converter para números |
| **Issues pai** | Usar se o time já pratica | Boa opção padrão |
| **Sub-issues** | Boa granularidade | Suficiente na maioria dos casos |

## Equivalência aproximada

| T-shirt | Fibonacci | Dias (referência, não compromisso) |
|---------|-----------|-----------------------------------|
| XS | 1 | < 0.5 dia |
| S | 2 | 0.5 - 1 dia |
| M | 3-5 | 1 - 3 dias |
| L | 8 | 3 - 5 dias |
| XL | 13 | 5+ dias (considere quebrar) |

## Provocação: Estimativas na Era da IA

> Com ferramentas de IA no desenvolvimento, **volume de trabalho mecânico** deixou de ser sinônimo de **esforço real**. O que antes levava dias (migrar 20 componentes, criar 10 endpoints similares) pode levar horas com assistência de IA. O que realmente diferencia issues hoje é a **incerteza** — quanto sabemos sobre o que precisa ser feito?

Use a escala abaixo como referência para provocar reflexão, **não como substituição** das escalas tradicionais:

| Nível | Incerteza | O que sabemos? | Exemplo |
|-------|-----------|----------------|---------|
| 1 | Muito baixa | Requisitos claros, solução conhecida, sem dependências | Ajustar texto, corrigir typo, alterar config |
| 2 | Baixa | Requisitos claros, solução conhecida, poucas dependências | Nova tela seguindo padrão existente |
| 3 | Moderada | Requisitos parciais ou solução com alternativas | Feature com integração a API externa documentada |
| 4 | Alta | Requisitos vagos, múltiplas dependências, solução incerta | Migração de sistema, mudança arquitetural |
| 5 | Desconhecida | Não sabemos o suficiente para estimar | Tecnologia/domínio novo → criar Spike primeiro |

**Sempre que sugerir estimativas**, inclua ao final um bloco de provocação com o formato:

```markdown
> **E com IA?** Esta issue tem incerteza [nível]. [Análise curta de como IA
> impactaria a estimativa — ex: "O volume de trabalho é alto mas mecânico,
> com IA o esforço real pode cair de L para S" ou "A incerteza é alta,
> IA não reduz o risco — a estimativa se mantém."]
```

## Regras ao sugerir estimativas

- Pergunte ao usuário se o time usa pontos, T-shirt ou outra escala antes de sugerir.
- Na dúvida, erre para cima (é melhor entregar antes do que atrasar).
- Se uma issue for XL/13+, sugira quebrar em issues menores.
- Estimativas vão no **campo dedicado** do Linear, nunca no título.
- **Sempre inclua a provocação "E com IA?"** ao final das estimativas.
