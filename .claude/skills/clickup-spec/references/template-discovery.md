# Template: Projeto de Discovery

Vive no folder **Product Discovery** (lista `Design`). Use quando o problema é claro mas o escopo ainda
será definido com o Designer. Estrutura o contexto para a exploração — não é uma spec completa.
As subtasks (UC1–UCn, Edge Cases) são criadas pelo Designer conforme descobre.

---

## Template

```markdown
**Roadmap Item:** [Nome — link VL-XXXXX]
**Dono:** [Nome]
**Tipo:** Projeto de Discovery

---

### 🎯 Objetivo
[O que precisamos descobrir e decidir — 1-2 frases]

### 🧠 Contexto e Problema
[Narrativa do porquê real: personas afetadas, dados/métricas que justificam, tensões e riscos que tornam a solução não trivial. Quanto mais específico, melhor o ponto de partida do Designer.]

### 📋 Restrições conhecidas
🚫 **Fora:**
- [o que a solução não pode/não deve fazer]

### 🔍 Questões em aberto
- [ ] [o que o discovery precisa responder]

### ✅ Critérios de saída
Para avançar para Delivery:
- [ ] Direção validada com [stakeholder]
- [ ] Escopo fechado (dentro e fora definidos)
- [ ] Spec de Delivery aprovada

### 🔗 Links
- Figma/FigJam: [link ou "Aguardando"]
```

**Status inicial:** `to do`. **Vínculo:** linked task com o Roadmap Item pai.

> **Próximo passo**: cumpridos os critérios de saída, use `/clickup-spec promote VL-XXXXX` para gerar o Delivery.

---

## Exemplo Real: Investigar o gargalo de KYC no onboarding e definir direção de solução

**Roadmap Item:** Otimizar o onboarding com KYC para elevar a conversão Cadastro → FTD — VL-11852
**Dono:** Ithalo Mendes
**Tipo:** Projeto de Discovery

---

### 🎯 Objetivo
Redesenhar o fluxo de KYC para que ocorra de forma obrigatória e linear no onboarding, reduzindo o abandono
de 51,4% na etapa de verificação e elevando a conversão Cadastrado → Verificado de 48,6% → 70%.

### 🧠 Contexto e Problema
O funil (01–03/jun/2026) mostra que de 3.356 pré-cadastros chegamos a apenas 925 depositantes (30,7%). O
gargalo está na verificação (KYC): de 3.012 cadastrados, só 1.464 ficam verificados (queda de 51,4%); as
demais etapas têm drop < 2%. **Dado crítico:** 95,22% abandonam ao abrir a tela de captura de documento.
**Causa raiz:** uma mudança recente desacoplou o KYC do onboarding — sem KYC obrigatório no funil, o usuário
não tem urgência e não retorna. **Fluxo desejado:** Pré-cadastro → Telefone → Email → **KYC** → Depósito.

### 📋 Restrições conhecidas
🚫 **Fora:**
- Eliminar o KYC — obrigação regulatória
- Incentivar com promoções
- Ignorar o fluxo Serasa

### 🔍 Questões em aberto
- [ ] Como funciona o Serasa no mobile com QR code? (80% dos usuários são mobile)

### ✅ Critérios de saída
Para avançar para Delivery:
- [ ] Fluxo linear obrigatório definido (Pré-cadastro → Telefone → Email → KYC → Depósito)
- [ ] Fluxo desenhado para UC1, UC2, UC3 (ver subtasks) + edge cases mapeados
- [ ] Comunicação de rota antes da câmera ("tenha seu RG/CNH em mãos" / "selfie em < 10s")
- [ ] Fluxo de re-engajamento desenhado para quem abandonou (canal, timing, limite de disparos)
- [ ] Comportamento do Serasa no mobile validado
- [ ] Direção validada com stakeholders (PO, Tech Lead, Compliance)
- [ ] Spec de Delivery aprovada

### 🔗 Links
- FigJam: https://www.figma.com/board/4xRhTCwXpvDc6B7iweVIQl/Onboarding
