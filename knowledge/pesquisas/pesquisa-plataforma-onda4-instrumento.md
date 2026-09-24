# Instrumento — Onda 4 · Pesquisa de Experiência de Plataforma (PAM)

> **Status:** desenho inicial do programa — **não liberado para campo.** Bloqueios abertos na §7.
> **Autor:** `arquiteto-de-instrumento` · **Data:** 2026-09-18 (rev. 1)
> **Origem:** cisão do programa combinado (decisão de Mateus Sperandio, 18/09/2026). As perguntas
> migradas **não são novas** — vêm com redação literal já revisada em dupla no instrumento combinado
> (`vertical/frentes/pesquisa-jogador/pesquisa-satisfacao-onda4-instrumento.md`, rev. 3).
> **Entradas:** `LEDGER-COMPARABILIDADE.md` deste programa · ledger e instrumento do programa combinado ·
> `README.md` deste programa (regras 15–18).
> **Revisão dupla obrigatória antes do campo:** `revisor-metodologico-survey` + `pesquisador-discovery`.
> Só a **P1 é pergunta nova** e precisa de revisão de mérito; o resto é migração literal.

---

## 0. Diagnóstico da onda

| Item | Resposta |
|---|---|
| **Objetivo dominante** | **Abrir o programa.** Estabelecer o ponto zero de satisfação com a plataforma e **atribuir a instabilidade ao dono certo** — a razão de existir da cisão |
| **Métrica-mãe** | **Satisfação com a plataforma 1–5** (P1). O NPS **não entra nesta onda** — ver P-D1 no ledger §1b |
| **Decisões que dependem dela** | (a) a estabilidade é problema da Loteria ou da Plataforma; (b) depósito/saque merece frente própria na O5; (c) a satisfação com a conta está num nível que exige escalonamento antes de qualquer roadmap |
| **Séries a proteger** | **Login/instabilidade** — 1 ponto herdado por tema (O3, 55,5% em ativos). É a única série deste programa, e o que a protege é a **redação literal** |
| **Ações lançadas que exigem recall (P6)** | Correção de estabilidade → P2, **literal** |
| **Restrição estruturante** | **Teto duro de 4 itens** (README, regra 18). Este instrumento é anexado à mesma distribuição da onda de Loteria; cada item aqui custa taxa de resposta lá |

### 0.1 Limitações declaradas antes do campo

1. **P1 é ponto zero sem referência externa.** Não existe satisfação com plataforma medida antes.
   O gatilho é **piso absoluto**, não comparativo (ledger §5), e é revisado na O5.
2. **PD1 — mudança de enquadramento.** A P2 é literal, mas o formulário ao redor mudou por completo.
   A variação O3→O4 é **limite superior**, não deterioração real. Ressalva permanente do primeiro par.
3. **P3 (CPF) carrega viés de incentivo sobre a composição de inativos** — bônus por conclusão não o
   elimina. Exposição de LGPD segue tratada com o jurídico. Nenhum dos dois é resolvido por desenho de
   pesquisa: **são sinalizados e encaminhados**, como no programa combinado.
4. **Nenhuma pergunta mede cadastro em si** (o fluxo de criação de conta). Quem responde já tem conta —
   o instrumento não fala com quem desistiu no cadastro. **Lacuna declarada**, candidata a pesquisa
   própria (não de survey de base) numa onda futura.
5. **Ganhadores não tem pergunta exclusiva aqui.** O fluxo de pagamento do prêmio é medido pelo programa
   de Loteria ("problema para receber prêmio", "segurança ao jogar/receber"). Duplicar aqui reintroduziria
   a ambiguidade que a cisão removeu. Declarado, não esquecido.

---

## 1. Orçamento de perguntas

Contagem: plena = 1,0 · condicional = 0,5.

| Formulário | Teto | Plenas | Condicionais | Subtotal | Itens no arquivo |
|---|---|---|---|---|---|
| **Ativos** | **4,0** | 2 | 1 (×0,5) | **2,5** | 3 |
| **Inativos** | 4,0 | 3 (inclui CPF) | 1 (×0,5) | **3,5** | 4 |
| **Ganhadores** | 4,0 | 2 | 1 (×0,5) | **2,5** | 3 |

**Por que tão curto.** Este não é um programa menos importante — é um programa que **compartilha o
respondente** com o de Loteria (README, regra 17). O teto protege a taxa de resposta dos dois. Escopo
novo aqui só depois que a O4 mostrar onde está o problema.

---

## 2. Estrutura — ATIVOS

Legenda: 🟢 idêntica e verificável · 🔵 nova · 🔶 condicional migrada

| # | Pergunta | Tipo | Status | Comparabilidade / função |
|---|---|---|---|---|
| **1** | **Satisfação com a plataforma 1–5** | Escala linear 1–5 | 🔵 | **Métrica-âncora do programa.** Ponto zero. R1 com objeto próprio |
| **2** | **Login / instabilidade** | Única (3) | 🟢 | **Literal obrigatório.** Única série do programa (1 ponto: O3, 55,5%). Medida de efeito da correção de estabilidade. **Ressalva PD1** |
| **2b** | **Origem do problema** (cond. a 2 ≠ "raramente ou nunca") | Única (5) | 🔶 | Migrada literal. **Agora sem ambiguidade** — o instrumento inteiro é sobre a conta |

**2 plenas + 1 condicional = 2,5.**

---

## 3. A pergunta nova — os dois testes e o critério pré-registrado

Só há uma. As demais são migração literal e **não precisam dos dois testes** — já passaram no
instrumento combinado.

### 3.1 Satisfação com a plataforma 1–5 (P1 — os três formulários)

- **Teste da lacuna.** Três ondas mediram satisfação **com o jogo** e nenhuma mediu satisfação com a
  conta. A O3 produziu o achado de que 55,5% dos ativos enfrentam instabilidade, mas não há nenhuma
  métrica de atitude para dizer se isso corrói ou não a relação com a plataforma. A cisão cria um
  programa **sem métrica-mãe** se esta pergunta não existir — e um programa com uma única fechada de
  incidência não é um programa, é uma pergunta solta.
- **Teste da decisão.** O corte < 60% de notas 4–5 em ativos **escalona imediatamente para o time de
  Plataforma, antes de qualquer iniciativa de roadmap**. Acima disso, a instabilidade é tratada como
  problema técnico pontual, e não como erosão de confiança na conta. São dois caminhos de ação
  diferentes, com donos diferentes.
- **Tipo:** escala linear 1–5, **espelhando exatamente** a escala da satisfação do programa de Loteria.
  Espelhar a escala **não** torna as duas comparáveis — o objeto é outro. Espelha-se para que o
  respondente não tenha que aprender duas escalas, e porque a comparação proibida é entre programas, não
  entre formatos.
- **Redação (objeto nomeado — README regra 16):**
  *"De 1 a 5, quanto você está satisfeito com a **sua conta** na Tradicional — entrar, depositar e sacar?"*
  O objeto aparece duas vezes: nominalmente ("sua conta") e por enumeração ("entrar, depositar e sacar").
- **Cuidado de construto declarado.** A enumeração é **deliberadamente tripla** e, num teste estrito,
  seria multi-barrelada. **Aceito, com justificativa:** o teto de 4 itens não comporta três escalas
  separadas, e o que se quer aqui é a **atitude geral com a conta**, não o diagnóstico por etapa — o
  diagnóstico é justamente o trabalho da P2b. A enumeração funciona como **definição do objeto**, não
  como três perguntas. **Registrado como risco conhecido**; se a O4 mostrar que o dado não se lê, a O5
  desdobra.
- **Critério pré-registrado:** **sem gatilho de nível comparativo na O4** (ponto zero). Gatilho de piso
  absoluto: **% de notas 4–5 < 60% em ativos, base válida → escalonamento para Plataforma.** Variação
  só a partir da O5 (queda > 0,3 na média).
- **Ordem:** item **nº1**, antes de qualquer pergunta de problema. Regra de ordem herdada: nenhuma
  pergunta de problema antes da métrica de atitude, ou a nota mede o que o formulário acabou de lembrar.

---

## 4. Estrutura — INATIVOS

Mesmo tronco, **tempo verbal no passado**. Distribuição obrigatória por **CRM (e-mail/push)**.

| # | Pergunta | Tipo | Status |
|---|---|---|---|
| 1 | Satisfação com a conta 1–5 (da última vez que usou) | Escala 1–5 | 🔵 |
| 2 | Login / instabilidade (passado) | Única (3) | 🟢 |
| 2b | Origem do problema (cond.) | Única (5) | 🔶 |
| 3 | **CPF** | Resposta curta | 🟢 — **R4, última pergunta absoluta, exclusiva de inativos** |

**3 plenas (inclui CPF) + 1 condicional = 3,5.**

**Nota de recorte, obrigatória:** o recorte de última sessão precisa ser **idêntico ao da O3 e idêntico
ao do formulário de inativos da Loteria** (P-D3). Recortes diferentes entre os dois programas tornam
impossível ler os dois juntos, que é o único motivo de dispará-los na mesma janela.

---

## 5. Estrutura — GANHADORES

| # | Pergunta | Tipo | Status |
|---|---|---|---|
| 1 | Satisfação com a conta 1–5 | Escala 1–5 | 🔵 |
| 2 | Login / instabilidade | Única (3) | 🟢 |
| 2b | Origem do problema (cond.) | Única (5) | 🔶 |

**2 plenas + 1 condicional = 2,5.** Sem exclusiva — ver §0.1, item 5.

---

## 6. Redação literal — para colar no Google Forms

**P1 — Satisfação com a plataforma**
*ativos/ganhadores:* "De 1 a 5, quanto você está satisfeito com a sua conta na Tradicional — entrar,
depositar e sacar?"
*inativos:* "De 1 a 5, quanto você estava satisfeito com a sua conta na Tradicional — entrar, depositar e
sacar — na época em que jogava?"
Escala linear 1–5 · 1 = muito insatisfeito · 5 = muito satisfeito.

**P2 — Login / instabilidade** *(literal migrada, não alterar)*
*ativos/ganhadores:* "Você tem enfrentado problemas de login ou instabilidade no app/site?"
*inativos:* "Você enfrentou problemas de login ou instabilidade no app/site?"
Única, nesta ordem: Sim, com frequência · Às vezes · Raramente ou nunca.

**P2b — Origem do problema** *(condicional, literal migrada)*
*ativos/ganhadores:* "Onde o problema costuma acontecer?" · *inativos:* "Onde o problema costumava
acontecer?"
Única, nesta ordem: Fazer login / entrar na conta · Depositar ou sacar · Usar a Loteria depois de logado ·
Vários deles / mais de um · Não sei dizer.

**P3 — CPF** *(inativos, última pergunta absoluta)*
"Pra creditar seu bônus de participação, informe seu CPF."
Resposta curta.

### 6.1 Custódia do CPF — regra migrada literal (§9.1 do instrumento combinado)

| Regra | Conteúdo |
|---|---|
| **Finalidade única** | Usado **exclusivamente** para creditar o bônus. Não cruza com PAM, não alimenta segmentação, não vira chave de análise |
| **Custódia** | Arquivo sob o **CRM**, armazenamento restrito. **Nunca versionado** — não entra no repositório, em anexo de tarefa nem em pasta compartilhada |
| **Export para análise** | A coluna é removida **antes** de o arquivo sair para a análise. CSV com CPF chegando à análise é **recusa de fonte** |
| **Prazo de descarte** | **Até 30 dias corridos** após o crédito do último bônus, com registro de quem executou |
| **Rota de tratamento** | Coordenada por **Pedro** com o jurídico |
| **Bônus** | **Por conclusão**, não por elegibilidade — o CPF é a última pergunta, e só quem chega ao fim o informa |

---

## 7. O que ainda bloqueia o campo

| # | Bloqueio | Dono | Por quê |
|---|---|---|---|
| 1 | **P-D2 — qual formulário carrega o bônus dos inativos** | **Pedro** | Com o CPF aqui, o de Loteria fica sem incentivo, o que **muda a composição de inativos** e quebra o par O3→O4 daquele programa. Recomendação: submissão encadeada, CPF no fim do conjunto. Ledger §5 |
| 2 | **P-D1 — NPS entra neste programa?** | **Mateus** | Não bloqueia a O4 (o desenho já assume que não), mas precisa de resposta antes da O5 |
| 3 | **P-D3 — recorte de inativos declarado**, idêntico ao da O3 e ao do programa de Loteria | **Pedro** | Sem isso, a leitura conjunta dos dois programas nasce quebrada |
| 4 | **Revisão dupla da P1** | `revisor-metodologico-survey` + `pesquisador-discovery` | É a única pergunta nova, e carrega um risco de multi-barrelamento **aceito e declarado** (§3.1) que precisa de segunda opinião |
| 5 | **Gate de publicação rodado** (§8) contra os 3 formulários | Quem publicar | Campo extra é bloqueio, não observação |

---

## 8. Checklist do gate de publicação

Rodar **antes de abrir o campo**, comparando este instrumento com o formulário publicado. Campo extra
é **bloqueio**, não observação.

- [ ] **Contagem de itens bate:** ativos 3 · inativos 4 · ganhadores 3
- [ ] **Nenhum campo extra** no formulário publicado — nenhum
- [ ] **Redação da P2 e da P2b conferida caractere a caractere** contra a §6 (é a única série do programa)
- [ ] **Tipo de resposta conferido item a item** (I11): escala linear 1–5 · única (3) · única (5) · resposta curta
- [ ] **Ordem das opções conferida** — a ordem faz parte do contrato (§2a do ledger)
- [ ] **Condicional da P2b configurada**: exibida só para "Sim, com frequência" e "Às vezes"
- [ ] **CPF existe só no formulário de inativos e é a última pergunta** (R4)
- [ ] **CPF: custódia, export sem a coluna e prazo de descarte confirmados** (§6.1)
- [ ] **Meta de N e piso declarados** por segmento, com responsável nomeado (R2)
- [ ] **Canal correto por segmento:** ativos in-app · inativos **CRM** · ganhadores fluxo pós-prêmio
- [ ] **Recorte de inativos idêntico** ao da O3 e ao do formulário de Loteria, declarado por escrito
- [ ] **Disparo na mesma janela** da onda 4 de Loteria (README, regra 17)
- [ ] **P-D2 decidida** — sem ela o conjunto não abre

---

## 9. Log de revisão

| Rev. | Data | O que mudou |
|---|---|---|
| 1 | 2026-09-18 | **Criação do programa.** Cisão do instrumento combinado: migração literal de login/instabilidade, origem do problema e CPF; criação da P1 (satisfação com a plataforma) como métrica-âncora; recusa fundamentada de duplicar o NPS (P-D1); registro de PD1 (mudança de enquadramento) e PD2 (migração do CPF e sua consequência sobre o incentivo dos inativos da Loteria) |
