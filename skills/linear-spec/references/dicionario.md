# Guia de Escrita e Dicionário Linear

Este documento estabelece o padrão para a criação de Iniciativas, Projetos e Milestones no Linear.

**Filosofia:** Estratégia centralizada no topo, autonomia técnica na base.
**Princípio guia:** *Aim for clarity* — não use jargões. Vá direto ao ponto.

---

## 1. A Regra de Ouro: Títulos Imperativos

O título de qualquer item não é um resumo vago, é uma declaração de intenção. Todo título **deve** seguir:

**Formato:** `[Verbo no Imperativo] + [Ação / Funcionalidade] + [Valor para o Negócio]`

> ❌ **Ruim:** Plataforma de competições
> ✅ **Bom:** Expandir a plataforma de competições para sustentar o engajamento em picos de acesso

---

## 2. Dicionário de Verbos por Nível

### Iniciativas (estratégico)
Verbos que comunicam apostas e direção de longo prazo:
- **Expandir:** Aumentar o alcance ou capacidade de algo existente. *(Ex: Expandir o portfólio de competições para novos segmentos)*
- **Transformar:** Mudar fundamentalmente uma experiência ou processo. *(Ex: Transformar a jornada de inscrição em competições)*
- **Consolidar:** Unificar capacidades fragmentadas. *(Ex: Consolidar a plataforma de avaliação em um único fluxo)*
- **Estabelecer:** Criar algo que ainda não existe. *(Ex: Estabelecer infraestrutura de dados para decisão em tempo real)*
- **Escalar:** Preparar para crescimento de volume ou mercado. *(Ex: Escalar o modelo de suporte para reduzir OPEX)*

### Projetos (tático)
Verbos que comunicam entregas concretas dentro de uma iniciativa:
- **Habilitar:** Destravar uma capacidade que o usuário não tinha. *(Ex: Habilitar filtros de segmento na listagem de turmas)*
- **Permitir:** Autorizar uma ação ou fluxo. *(Ex: Permitir que professores acompanhem envios das equipes)*
- **Integrar:** Conectar sistemas ou fluxos. *(Ex: Integrar notificações de status de envio)*
- **Garantir:** Blindar regras de negócio ou fluxos críticos. *(Ex: Garantir visibilidade do professor sobre envios)*
- **Otimizar:** Melhorar performance ou reduzir fricção. *(Ex: Otimizar o fluxo de inscrição para equipes escolares)*
- **Simplificar:** Remover complexidade desnecessária. *(Ex: Simplificar a navegação da home de competições)*
- **Estruturar:** Criar a base de algo novo. *(Ex: Estruturar tela de acompanhamento para professores)*
- **Automatizar:** Remover trabalho manual. *(Ex: Automatizar transição de status entre etapas)*

### Milestones (marcos intermediários)
Verbos que comunicam pontos de validação ou entrega parcial:
- **Entregar:** Disponibilizar algo para uso. *(Ex: Entregar MVP da tela de acompanhamento do professor)*
- **Validar:** Confirmar hipótese ou decisão. *(Ex: Validar novo fluxo de inscrição com escolas piloto)*
- **Concluir:** Finalizar uma etapa do projeto. *(Ex: Concluir integração com API de envio de arquivos)*
- **Lançar:** Disponibilizar para todos os usuários. *(Ex: Lançar nova home para todas as competições)*

---

## 3. Templates de Estrutura

### Para Iniciativas
Comunicam a aposta estratégica e organizam o portfólio de projetos:
- **Visão e Objetivo:** Por que essa iniciativa existe e o que queremos alcançar
- **OKRs e Metas:** Métricas com baseline e meta
- **Portfólio de Projetos:** Lista dos projetos que compõem a iniciativa
- **Milestones Centrais:** Marcos de validação ao longo do período
- **Dependências Externas:** O que precisa acontecer fora do time
- **Dono:** Quem é responsável pela iniciativa

### Para Projetos
Comunicam o que será construído e por que, dentro de uma iniciativa:
- **Alinhamento Estratégico:** A qual iniciativa responde e como contribui
- **Contexto e Problema:** O que está errado ou faltando hoje
- **Escopo:** O que faremos (dentro) e o que não faremos (fora) — ambos são obrigatórios
- **Critérios de Aceite:** Checklist binário e testável (`- [ ]`)
- **Links:** Figma, documentação, OKR relacionado
- **Milestones:** Marcos intermediários do projeto
- **Dono:** Quem é responsável pela spec e pela entrega

### Para Milestones
Comunicam um marco intermediário verificável dentro de um projeto:
- **O que representa:** O que estará pronto ou validado
- **Por que importa:** Decisão, validação de hipótese, entrega parcial
- **Data-alvo:** Quando deve ser atingido

---

## 4. Boas Práticas de Formatação

1. **Scannability primeiro:** Use tópicos, negritos para métricas e tabelas para dados estruturados. Ninguém lê parágrafos longos no Linear.
2. **Brevidade é respeito:** Specs curtas são mais lidas. O objetivo é comunicar o "porquê", "o quê" e "como" de forma eficiente — não escrever um documento exaustivo.
3. **Fora de escopo é tão importante quanto dentro:** Deixar explícito o que não será feito evita scope creep e alinha expectativas antes de começar.
4. **Critérios binários:** Cada critério de aceite deve poder ser respondido com sim ou não. "Funcionar bem" não é critério. "Carregar em menos de 2s" é.
5. **Dono nomeado:** Todo item deve ter uma pessoa responsável. Responsabilidade compartilhada é responsabilidade de ninguém.
6. **Conecte ao nível acima:** Todo Projeto deve referenciar sua Iniciativa. Todo Milestone deve referenciar seu Projeto.
