# Guia de Escrita e Dicionário — ClickUp

Padrão para criar Projetos de Discovery/Delivery e subtasks no ClickUp.

**Filosofia:** Contexto e intenção vivem no próprio card de Delivery — sem nível estratégico acima dele.
**Princípio guia:** *Aim for clarity* — sem jargão, direto ao ponto.

---

## 1. A Regra de Ouro: Títulos Imperativos

O título é uma declaração de intenção, não um resumo vago. Todo título **deve** seguir:

**Formato:** `[Verbo no Imperativo] + [Ação / Funcionalidade] + [Valor para o Negócio]`

> ❌ **Ruim:** Onboarding com KYC
> ✅ **Bom:** Otimizar o onboarding com KYC para elevar a conversão Cadastro → FTD

---

## 2. Dicionário de Verbos por Nível

### Projetos (Discovery / Delivery — tático)
Entregas concretas do processo de produto:
- **Investigar / Descobrir:** (faixa de descoberta) entender antes de construir. *(Ex: Investigar o gargalo de KYC no onboarding)*
- **Habilitar:** destravar uma capacidade nova ao usuário.
- **Permitir:** autorizar uma ação ou fluxo.
- **Reposicionar:** mudar a ordem/posição de uma etapa. *(Ex: Reposicionar o KYC facial antes do FTD)*
- **Integrar:** conectar sistemas ou fluxos.
- **Garantir:** blindar regras de negócio críticas.
- **Simplificar / Automatizar:** remover complexidade ou trabalho manual.

### Subtasks (recortes / marcos)
- **Desenhar:** (UC, fluxo) *(Ex: Desenhar fluxo de re-engajamento para quem abandonou o KYC)*
- **Entregar / Validar / Concluir / Lançar:** marcos verificáveis.

---

## 3. Estrutura por Nível

### Projeto de Discovery (faixa de descoberta dentro do Backlog do Delivery)
- **Dono** (assignee)
- **Objetivo** (o que decidir)
- **Contexto e Problema** (dados, personas, tensões)
- **Restrições conhecidas** (fora de escopo)
- **Questões em aberto** (checklist)
- **Critérios de saída** (gate p/ sprint)
- **Links** (Figma/FigJam)

### Projeto de Delivery
- **Dono** (assignee)
- **Objetivo** (o que entrega, qual indicador de negócio move)
- **Contexto** (validado na faixa de descoberta)
- **Escopo** (dentro = capacidades; fora = explícito)
- **Critérios de Aceite** por área funcional (binários)
- **Links**

---

## 4. Boas Práticas de Formatação

1. **Scannability primeiro:** tópicos, negrito em métricas, tabelas para dados. Ninguém lê parágrafos longos.
2. **Brevidade é respeito:** specs curtas são mais lidas.
3. **Fora de escopo é tão importante quanto dentro:** evita scope creep.
4. **Critérios binários:** cada critério responde sim/não. "Funcionar bem" não é critério; "verificar em < 10s" é.
5. **Dono nomeado:** responsabilidade compartilhada é de ninguém.
6. **O card carrega seu próprio porquê:** sem nível estratégico acima do Delivery, o Contexto de cada
   Projeto explica sozinho o problema, o impacto e o indicador de negócio que ele move.
