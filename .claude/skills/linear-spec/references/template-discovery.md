# Template: Projeto de Discovery

Use quando o problema é claro, mas o escopo ainda será definido com o Designer. O objetivo é estruturar o contexto para a exploração — não uma spec completa.

Para o contexto completo sobre o fluxo de discovery e design: [discovery-e-design.md](discovery-e-design.md)

---

## Template

```markdown
## [Verbo no Imperativo] + [Nome do Projeto]

**Iniciativa:** [Nome da Iniciativa vinculada]
**Dono:** [Nome]

---

### 🎯 Objetivo
[O que precisamos descobrir e decidir neste projeto — 1-2 frases]

### 🧠 Contexto e Problema
[Bloco narrativo com o porquê real. Inclua: personas afetadas, dados ou métricas que justificam o problema, tensões e riscos que tornam a solução não trivial. Quanto mais específico, melhor o ponto de partida para o Designer.]

### 📋 Restrições conhecidas
🚫 **Fora:**
- [Restrições já conhecidas do espaço de solução — o que a solução não pode ou não deve fazer]

### 🔍 Questões em aberto
- [ ] [O que o discovery precisa responder 1]
- [ ] [O que o discovery precisa responder 2]
- [ ] [O que o discovery precisa responder 3]

### ✅ Critérios de saída
Para avançar para Delivery:
- [ ] Direção validada com [stakeholder]
- [ ] Escopo fechado (dentro e fora definidos)
- [ ] Spec de Delivery aprovada

### 🔗 Links
- Figma: [link ou "Aguardando"]
```

---

> **Próximo passo**: após os critérios de saída cumpridos, use `/linear-spec promote [PROJ-ID]` para gerar o Projeto de Delivery a partir deste Discovery.

---

## Exemplo Real: Prototipar a Biblioteca de Conteúdos do Portal Arcoplus

## Prototipar a Biblioteca de Conteúdos do Portal Arcoplus

**Iniciativa:** Elevar a encontrabilidade de recursos no Portal Arcoplus
**Dono:** Ithalo Mendes

---

### 🎯 Objetivo
Descobrir como evoluir a Biblioteca de Conteúdos para que professores encontrem recursos de forma autônoma — definindo a lógica de relevância automática, a estrutura de categorias e a direção de busca e filtros.

### 🧠 Contexto e Problema
Hoje a Biblioteca não tem hierarquia de informações eficaz. Usuários não percebem que precisam interagir com determinados elementos para visualizar categorias. Quando nenhum destaque é configurado manualmente, a home aparece vazia — recursos valiosos ficam invisíveis. O padrão aparece em múltiplas fontes: chamados de 2025 registram que *"professores têm dificuldade de localizar materiais específicos"*; a feature de busca é pouco utilizada; o NPS 2025.2 do Nave à Vela concentra críticas em encontrabilidade. O time pedagógico produz volume expressivo de recursos que chegam com baixíssima visibilidade, dependendo de comunicações externas para serem descobertos.

### 📋 Restrições conhecidas
🚫 **Fora:**
- Deve respeitar o design system atual
- Não pode depender sempre de ação manual de PMM para exibir conteúdo relevante
- Deve funcionar para todas as marcas do Portal Plus, com foco em Nave à Vela

### 🔍 Questões em aberto
- [ ] Qual critério define "conteúdo mais relevante" sem configuração manual (data, acesso, marca, série)?
- [ ] Como estruturar as categorias de forma mais acessível e intuitiva?
- [ ] Quais filtros são realmente usados vs. ignorados pelos usuários hoje?
- [ ] Como equilibrar curadoria automática (algoritmo) e curadoria intencional (PMM)?
- [ ] A busca atual tem dados suficientes para entender padrões de uso?

### ✅ Critérios de saída
Para avançar para Delivery:
- [x] Lógica de relevância automática definida e validada com stakeholders pedagógicos
- [x] Estrutura de categorias aprovada
- [ ] Direção de design validada com ao menos um perfil de usuário real
- [ ] Spec de Delivery aprovada

### 🔗 Links
- Figma: Aguardando
