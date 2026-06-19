# Template: Roadmap Item (aposta estratégica)

Vive no folder **Product Roadmap** (lista `Product Roadmap`). É o contêiner estratégico: carrega visão,
métricas, portfólio de projetos e dependências, e percorre todo o ciclo de status. Equivale à Iniciativa do Linear.

---

## Template

```markdown
### 🎯 Visão e Objetivo
[2-3 frases: a aposta estratégica, o problema que destrava e o porquê de agora. Cite a métrica que move.]

### 📈 Métricas associadas
| Tipo | Métrica | Meta | Baseline |
|------|---------|------|----------|
| KPI primário | [métrica] | [meta] | [baseline] |
| Guard-rail | [o que não pode piorar] | [limite] | [atual] |
| Secundária | [métrica de apoio] | [meta] | [—] |

### 🗂️ Portfólio de Projetos
Nome do Discovery (https://app.clickup.com/t/9006076935/VL-XXXXX)
Nome do Delivery (https://app.clickup.com/t/9006076935/VL-YYYYY)

### 🔗 Dependências Externas
- **[Área/Time/Decisão]:** [o que está pendente]
```

**Campos a sugerir** (com confirmação): _Projeto (marca), Squad, Impacto (eixo), RICE (Reach/Impact/Confidence/Effort),
MoSCoW, Horizonte, Phase. Ver [clickup-method.md](clickup-method.md). **Status inicial:** `considering` ou `prioritized`.

> **Portfólio = task-link interativo.** Cada projeto é uma linha `Nome (URL completa da tarefa)` — o ClickUp
> renderiza a URL como componente com status e responsável ao vivo. Nada de checkbox, prefixo `[Discovery]` ou
> `VL-XXXXX` solto. Detalhe em [clickup-method.md](clickup-method.md) → "Boa prática — espelhar sempre no Portfólio".

---

## Exemplo Real: Otimizar o onboarding com KYC para elevar a conversão Cadastro → FTD

### 🎯 Visão e Objetivo
Destravar o maior ponto de abandono do funil — a queda de **48%** entre o fim do cadastro e o primeiro
depósito (FTD) — reposicionando o **KYC facial para antes do FTD**, em conformidade com a Portaria 722/2024
(Art. 10c/d). Após a captura da selfie o usuário segue direto ao depósito enquanto a verificação
(Legitimuz/Serasa) roda em background (30–60s, compatível com o tempo do PIX). Quem é reprovado ou fica
pendente é recuperado por re-engajamento. Mantém a operação fora do risco de penalidade de até R$ 2 bi
(Lei 14.790, Art. 59).

### 📈 Métricas associadas
| Tipo | Métrica | Meta | Baseline |
|------|---------|------|----------|
| KPI primário | Conversão Cadastro → FTD | Reduzir o drop de 48% | −48% no funil atual |
| Guard-rail | Conformidade KYC pré-FTD (Portaria 722/2024) | 100% dos fluxos | fluxo atual não conforme |
| Secundária | Reativação de usuários com KYC reprovado/pendente | A definir | — |

### 🗂️ Portfólio de Projetos
Investigar o gargalo de KYC no onboarding e definir direção de solução (https://app.clickup.com/t/9006076935/VL-11235)
Reposicionar KYC facial antes do FTD com processamento em background (https://app.clickup.com/t/9006076935/VL-11369)
Banner de reativação para KYC reprovado/pendente (https://app.clickup.com/t/9006076935/VL-11394)

### 🔗 Dependências Externas
- **API de KYC (Legitimuz / Serasa):** decisão de provedor e SLA de resposta — _em aberto_
- **Jurídico / Compliance:** Portaria 722/2024 (Art. 10c/d), Lei 14.790 (Art. 59), LGPD (Art. 11 §1º — biometria; Art. 39 — DPA)
- **Backoffice:** parametrização quando a API reprova antes de o depósito concluir

> Campos: _Projeto = (marca) · Squad = (resolver) · Impacto = Receita/Conversão + Compliance · Horizonte = Now ·
> MoSCoW = Must Have · RICE ≈ alto (Reach amplo no topo de funil, Impact 5, Confidence alta por dados de funil, Effort médio).
