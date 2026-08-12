# Guia de Escrita e Dicionário — ClickUp

Padrão para criar Roadmap Items, Projetos de Discovery/Delivery e subtasks no ClickUp.

**Filosofia:** Estratégia centralizada no Roadmap, detalhe na base.
**Princípio guia:** *Aim for clarity* — sem jargão, direto ao ponto.

---

## 1. A Regra de Ouro: Títulos Imperativos

O título é uma declaração de intenção, não um resumo vago. Todo título **deve** seguir:

**Formato:** `[Verbo no Imperativo] + [Ação / Funcionalidade] + [Valor para o Negócio]`

> ❌ **Ruim:** Onboarding com KYC
> ✅ **Bom:** Otimizar o onboarding com KYC para elevar a conversão Cadastro → FTD

---

## 2. Dicionário de Verbos por Nível

### Roadmap Item (estratégico)
Apostas e direção de longo prazo:
- **Otimizar:** melhorar um fluxo/resultado existente. *(Ex: Otimizar o onboarding para elevar conversão)*
- **Expandir:** aumentar alcance ou capacidade. *(Ex: Expandir o hub de esportes para novos mercados)*
- **Transformar:** mudar fundamentalmente uma experiência. *(Ex: Transformar a jornada de verificação de conta)*
- **Consolidar:** unificar capacidades fragmentadas.
- **Estabelecer:** criar algo que ainda não existe.
- **Escalar:** preparar para crescimento de volume/mercado.

### Projetos (Discovery / Delivery — tático)
Entregas concretas dentro de um Roadmap Item:
- **Investigar / Descobrir:** (Discovery) entender antes de construir. *(Ex: Investigar o gargalo de KYC no onboarding)*
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

### Roadmap Item
- **Visão e Objetivo:** por que existe, o que move
- **Métricas associadas:** KPI primário, Guard-rail, Secundária (com baseline e meta)
- **Portfólio de Projetos:** Discovery/Delivery vinculados
- **Dependências Externas:** o que precisa acontecer fora do time
- **Dono + priorização** (RICE/MoSCoW/Horizonte/Squad/_Projeto)

### Projeto de Discovery
- **Roadmap Item** vinculado + Dono
- **Objetivo** (o que decidir)
- **Contexto e Problema** (dados, personas, tensões)
- **Restrições conhecidas** (fora de escopo)
- **Questões em aberto** (checklist)
- **Critérios de saída** (gate p/ Delivery)
- **Links** (Figma/FigJam)

### Projeto de Delivery
- **Roadmap Item** + **Discovery** vinculados + Dono
- **Objetivo** (o que entrega, qual KPI move)
- **Contexto** (validado no Discovery)
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
6. **Conecte ao nível acima:** todo Projeto referencia seu Roadmap Item — por linked task e no corpo.
