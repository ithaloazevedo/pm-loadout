# Anti-patterns a Evitar — ClickUp

Erros comuns em Roadmap Items, Projetos de Discovery/Delivery e subtasks — e como corrigir.

---

## Roadmap Item

| Anti-pattern | Exemplo | Problema |
|--------------|---------|----------|
| Título genérico sem direção | `Melhorar o onboarding` | Não comunica aposta. Qualquer coisa se encaixa. |
| Substantivo no lugar de verbo | `Onboarding 2026` | Parece nome de produto, não intenção |
| Sem métricas | item sem KPI/baseline | Impossível avaliar sucesso |
| Sem portfólio vinculado | item sem Discovery/Delivery ligados | Estratégia sem execução mapeada |
| Priorização vazia | sem RICE/Horizonte/Squad | Não dá para sequenciar no roadmap |
| Sem dono | sem assignee | Ninguém é accountable |

> ❌ `KYC no cadastro` → ✅ `Otimizar o onboarding com KYC para elevar a conversão Cadastro → FTD`

---

## Projeto de Discovery

| Anti-pattern | Exemplo | Problema |
|--------------|---------|----------|
| Discovery órfão | sem Roadmap Item vinculado | Investigação desconectada da estratégia |
| Sem critérios de saída | discovery sem gate | Nunca se sabe quando avançar para Delivery |
| Problema sem dados | "usuários reclamam" | Sem baseline, não há como medir melhora |
| Questões em aberto ausentes | discovery que já "sabe a resposta" | Então não é discovery — é delivery |

> ❌ `Pesquisar KYC` → ✅ `Investigar o gargalo de KYC no onboarding e definir a direção de solução`

---

## Projeto de Delivery

| Anti-pattern | Exemplo | Problema |
|--------------|---------|----------|
| Delivery órfão | sem Roadmap Item / Discovery | Build desconectado da decisão |
| Título nominal | `Tela de KYC` | Não declara intenção nem valor |
| Sem "Fora de Escopo" | só o que vai fazer | Sem limite, qualquer coisa entra no meio |
| Critérios em prosa | `A verificação deve funcionar bem` | Não é verificável |
| Escopo > 2-3 meses | projeto gigante | Quebre em projetos menores independentes |
| Sem dono | sem PM/EM | Ninguém escreve a spec nem responde pela entrega |

> ❌ `Reposicionar KYC` → ✅ `Reposicionar o KYC facial antes do FTD com processamento em background`

---

## No Título (geral)

| Anti-pattern | Exemplo | Problema |
|--------------|---------|----------|
| Estimativas no título | `[25h] Criar fluxo de KYC` | Polui — use o campo de estimativa |
| Siglas sem contexto | `[UC2] Ajuste RN1` | Incompreensível fora do time imediato (ok em subtask interna, não no projeto) |
| Só implementação, sem valor | `Refatorar AuthService` | Não explica o benefício |
| Genérico demais | `Ajustes na API` | Não comunica o que muda nem para quem |
