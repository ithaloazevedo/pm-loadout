# Domínio: Negócio

Entidades que descrevem objetivos, métricas e aprendizados — o "porquê" por trás do trabalho de produto.

> **Objetivo e KR deixaram de ser rastreados formalmente em 2026-09-10** (ver
> `knowledge/decisions/2026-09-10-migracao-esteira-continua-para-sprints-remocao-okr-e-discovery.md`): a
> empresa decidiu não ter OKRs formais por ora (falta de maturidade para o ciclo hoje). As duas seções abaixo
> (Objetivo, KR) ficam mantidas como referência — podem ser retomadas no futuro — mas **hoje não há instância
> viva** desses conceitos no processo de produto. Métrica, Hipótese e Experimento (seções seguintes) não são
> afetados: continuam existindo normalmente como conceitos de negócio.

---

## Objetivo *(descontinuado em 2026-09-10 — sem instância viva hoje)*

**Definição**: Resultado qualitativo ambicioso que a empresa quer alcançar num ciclo (quarter/semestre).

**Atributos**: enunciado, empresa, período, status (em progresso / atingido / descartado)

**Relações**:
- medido por → KR (Resultado-chave)
- impulsionado por → Iniciativa / Feature

---

## KR — Resultado-chave *(descontinuado em 2026-09-10 — sem instância viva hoje)*

**Definição**: Métrica mensurável que indica progresso em direção a um Objetivo.

**Atributos**: enunciado, baseline, target, dono, fonte de dados, frequência de atualização

**Exemplos (Q3 2026 — Tradicional)**:
- KR1: Conversão cadastro → 1º depósito ≥ X%
- KR2: Churn 30 dias ≤ Y%
- KR3: Uptime PIX ≥ 99.9%

**Relações**:
- pertence a → Objetivo
- alimentado por → Evento / Métrica

---

## Métrica

**Definição**: Medida recorrente usada para acompanhar saúde de produto ou negócio.

**Atributos**: nome, fórmula, unidade, frequência, dono, fonte, guardrail (threshold mínimo aceitável)

**Tipos**:
- **North Star**: uma métrica central que captura o valor entregue ao usuário
- **Guardrail**: métrica que não pode piorar enquanto outra avança
- **Diagnóstico**: métrica que ajuda a entender causa de variação

**Exemplos**:
- Conversão cadastro → 1º depósito (North Star — Onboarding)
- Churn 7/30/60 dias (Guardrail — Retenção)
- Taxa de aprovação KYC (Diagnóstico — Onboarding)

**Relações**:
- alimentada por → Evento
- pertence a → KR / Objetivo

---

## Hipótese

**Definição**: Crença testável sobre comportamento de usuário ou impacto de uma feature.

**Formato padrão**: "Acreditamos que [ação] para [segmento] vai resultar em [outcome] porque [razão]. Saberemos que funcionou quando [evidência]."

**Atributos**: enunciado, risco (alto/médio/baixo), status (não testada / em teste / validada / refutada)

**Relações**:
- oriunda de → Suposição / Discovery
- testada por → Experimento

---

## Experimento

**Definição**: Teste estruturado para validar ou refutar uma Hipótese.

**Atributos**: hipótese testada, design do experimento, duração, critério de sucesso, resultado

**Tipos**:
- A/B test
- Feature flag para subgrupo
- Entrevista de validação
- Smoke test (landing page, form)

**Relações**:
- testa → Hipótese
- alimenta → Decisão / Decision Log
