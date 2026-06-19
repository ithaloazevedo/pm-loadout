# Template: Projeto de Delivery

Vive no folder **Product Delivery**. Use quando o Discovery foi concluído — direção validada, escopo
fechado, engenharia pode iniciar o planejamento. **Nasce na lista `Backlog de Delivery`** (refinado e
priorizado, pronto para sprint); migra para `Execução` ao entrar na sprint, ou é criado direto em `Execução`
se for tarefa prioritária. **Nunca** crie listas novas no folder (a lista legada "Delivery" está vazia e não
deve ser usada). IDs e status em [clickup-config.md](clickup-config.md).

---

## Template

> **Sem bloco de cabeçalho.** Não repita Roadmap Item / Discovery / Dono no topo: o **Dono** é o assignee da
> task e os **vínculos** vão na seção 🔗 Links. **Espaçamento:** linha em branco só **entre** seções `###` —
> dentro de uma seção, sub-cabeçalhos colam nos bullets (sem linha em branco).

```markdown
### 🎯 Objetivo
[1-2 frases: o que este projeto entrega e qual KPI move]

### 🧠 Contexto
[Problema validado no discovery, dados que justificam, o que já sabemos sobre a direção]

### 📋 Escopo
✅ **Dentro:**
- Usuário consegue [capacidade 1]
- Usuário consegue [capacidade 2]
🚫 **Fora:**
- [o que explicitamente não será feito — evita scope creep]

### ✅ Critérios de Aceite
**[Área funcional 1]**
- [ ] [comportamento específico e testável]
**[Área funcional 2]**
- [ ] [comportamento específico e testável]

### 🔗 Links
- Roadmap Item: [Nome — link VL-XXXXX]
- Discovery: [Nome — link VL-XXXXX, se houver]
- Figma: [link]
- Pré-requisito: [link se houver]
```

**Vínculo:** linked task com o Roadmap Item **e** com o Discovery de origem.

---

## Exemplo Real: Reposicionar o KYC facial antes do FTD com processamento em background

### 🎯 Objetivo
Entregar o novo fluxo de onboarding em que a captura facial do KYC ocorre **antes do FTD** e a verificação
roda em background (30–60s, compatível com o tempo do PIX), reduzindo o drop de 48% entre cadastro e primeiro
depósito sem violar a Portaria 722/2024.

### 🧠 Contexto
O discovery validou que desacoplar o KYC do funil foi negativo: 95,22% abandonam ao chegar despreparados à
tela de captura. A direção fechada é fluxo linear obrigatório com comunicação de rota antes da câmera e
processamento assíncrono enquanto o usuário segue para o depósito.

### 📋 Escopo
✅ **Dentro:**
- Usuário passa pelo KYC facial como etapa obrigatória do onboarding, antes do depósito
- Usuário é avisado da rota antes da câmera ("tenha RG/CNH em mãos" ou "selfie em < 10s")
- Usuário segue para o depósito enquanto a verificação roda em background
- Usuário reprovado/pendente é direcionado ao fluxo de re-engajamento
🚫 **Fora:**
- Eliminar ou flexibilizar a obrigatoriedade do KYC (regulatório)
- Incentivos promocionais para concluir o KYC
- Banner de reativação (projeto separado — VL-11394)

### ✅ Critérios de Aceite
**Fluxo de onboarding**
- [ ] KYC posicionado após Email e antes do Depósito, de forma obrigatória e linear
- [ ] Tela de comunicação de rota exibida antes de abrir qualquer câmera
- [ ] Usuário avança para o depósito sem aguardar o resultado da verificação
**Processamento em background**
- [ ] Verificação (Legitimuz/Serasa) dispara de forma assíncrona ao capturar a selfie
- [ ] Resultado aprovado/reprovado/pendente atualiza o status da conta sem bloquear o depósito
- [ ] Comportamento parametrizável no backoffice quando a API reprova antes de o depósito concluir
**Conformidade**
- [ ] 100% dos fluxos garantem KYC pré-FTD (Portaria 722/2024, Art. 10c/d)
- [ ] Tratamento de dados biométricos conforme LGPD (Art. 11 §1º)

### 🔗 Links
- Roadmap Item: Otimizar o onboarding com KYC para elevar a conversão Cadastro → FTD — VL-11852
- Discovery: Investigar o gargalo de KYC no onboarding e definir direção de solução — VL-11235
- Figma: [Aguardando]
