# Template: Objetivo (OKR/KR)

> ⚠️ **Legado/histórico, não usar.** O nível Objetivo (OKR/KR) saiu do processo de produto em 2026-09-10 — a
> empresa decidiu não ter mais OKRs formais. O folder Roadmap/Strategy e a lista Objetivos (`901114034994`)
> foram **removidos do ClickUp** (ver `knowledge/domains/processo.md` e
> `knowledge/decisions/2026-09-10-migracao-esteira-continua-para-sprints-remocao-okr-e-discovery.md`). Não
> crie Marco (OKR) nem Resultado-chave (KR) novos — esses task types não têm mais lista onde viver. Este
> arquivo fica só como referência para quem precisar entender specs antigas que ainda citam OKR/KR.

Vive no folder ~~Roadmap → Objetivos~~ (lista Objetivos, removida). Dois tipos de item:

- **Marco (OKR)** — objetivo qualitativo do ciclo: "o que queremos alcançar".
- **Resultado-chave (KR)** — métrica que prova o avanço do Marco OKR.

---

## Template: Marco (OKR)

```markdown
### 🎯 Objetivo do ciclo
[1-2 frases: o problema/oportunidade e por que importa agora — não a solução nem a métrica (isso vai
nos KRs). Ver [estilo-redacao.md](estilo-redacao.md).]

### 📈 Resultados-chave (KRs)
- KR1: [métrica] de [baseline] → [meta] até [prazo]
- KR2: [métrica] de [baseline] → [meta] até [prazo]

### 🗂️ Projetos vinculados
Nome do Discovery (https://app.clickup.com/t/9006076935/VL-XXXXX)
Nome do Delivery (https://app.clickup.com/t/9006076935/VL-YYYYY)

### 🔗 Dependências
- **[Área/Time/Decisão]:** [o que está pendente]
```

**Campos:** assignee (dono do OKR), tipo=`Marco (OKR)`, período/ciclo. **Status inicial:** `to do`.

---

## Template: Resultado-chave (KR)

```markdown
### 🎯 O que medimos
[A métrica, o que representa e por que foi escolhida para este Marco OKR.]

### 📏 Meta e baseline
| | Valor |
|---|---|
| **Baseline** | [valor atual] |
| **Meta** | [valor alvo] |
| **Prazo** | [data/ciclo] |
| **Fonte de dados** | [onde vive a métrica] |

### ✅ Critérios de considerado atingido
- [ ] [condição objetiva e verificável]
```

**Campos:** assignee, tipo=`Resultado-chave (KR)`, Marco OKR pai (linked task), período/ciclo.

---

> **Portfólio = task-link interativo.** Cada projeto vinculado ao Objetivo é uma linha `Nome (URL completa)` — o ClickUp renderiza como componente com status e responsável ao vivo. Detalhes em [clickup-method.md](clickup-method.md) → "Boa prática — espelhar sempre no Portfólio".

---

## Exemplo Real: Elevar a conversão Cadastro → FTD

### 🎯 Objetivo do ciclo
Destravar o maior ponto de abandono do funil — a queda entre o fim do cadastro e o primeiro depósito — com conformidade à regulação vigente (Portaria 722/2024).

### 📈 Resultados-chave
- KR1: Conversão Cadastro → FTD de 30,7% → 45% até set/2026
- KR2: 100% dos fluxos com KYC pré-FTD conforme Portaria 722/2024

### 🗂️ Projetos vinculados
Investigar o gargalo de KYC no onboarding (https://app.clickup.com/t/9006076935/VL-11235)
Reposicionar KYC facial antes do FTD (https://app.clickup.com/t/9006076935/VL-11369)
Banner de reativação para KYC reprovado/pendente (https://app.clickup.com/t/9006076935/VL-11394)

### 🔗 Dependências
- **API KYC (Legitimuz / Serasa):** decisão de provedor e SLA — _em aberto_
- **Jurídico/Compliance:** Portaria 722/2024, Lei 14.790, LGPD
