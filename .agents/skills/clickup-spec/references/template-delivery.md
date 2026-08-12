# Template: Projeto de Delivery (Épico)

Vive no **folder de Delivery da squad que executa** (Experiência do jogador / Operação e afiliados /
Provedora de conteúdo — em regra, o folder é determinado pela squad responsável pela execução; se um épico é
executado por outra squad, ex. gestão no backoffice, ele vai para o folder dessa squad). Use quando o
Discovery foi concluído — direção validada, escopo fechado, engenharia pode iniciar o planejamento.
**Nasce na lista `Backlog`**; migra para `Execução` ao entrar na sprint. **Nunca** crie listas novas nos
folders. IDs e status em [clickup-config.md](clickup-config.md).

Os **critérios de aceite são propostos pelo PM** a partir do protótipo/discovery e validados no
refinamento com a squad — o épico não nasce sem eles.

---

## Template

> **Sem bloco de cabeçalho.** Não repita Objetivo / Discovery / Dono no topo: o **Dono** é o assignee da
> task e os **vínculos** vão na seção 🔗 Links. **Espaçamento:** linha em branco só **entre** seções `###`. Dentro de uma seção, sub-cabeçalhos em
> negrito colam nos bullets — **sem linha em branco antes do sub-cabeçalho nem entre sub-blocos**. Isso
> vale sobretudo em ✅ Critérios de Aceite (área funcional + Qualidade + Instrumentação, todos colados).

```markdown
### 🎯 Objetivo
[1-2 frases: o que este épico entrega e qual objetivo e KPI/KR ele move]

### 🧠 Contexto
[Problema → Impacto → Solução: o problema validado no discovery, o dado que sustenta (quanti ou
quali) e o indicador de negócio afetado (conversão, receita, retenção, satisfação, operação) — só
depois o que este item muda nisso. Decisões já fechadas que moldam o escopo (ex.: "estratégia
híbrida decidida em DD/MM") entram aqui. Requisito legal/regulatório entra pela implicação prática
em uma frase, citação curta entre parênteses — nunca texto de lei entre aspas ou vários artigos
encadeados (ver [estilo-redacao.md](estilo-redacao.md)).]

### 📋 Escopo
✅ **Dentro:**
- [Ator] [faz / acessa / recebe] [capacidade em linguagem simples — sem detalhe técnico]

🚫 **Fora:**
- [O que não entra neste épico — com destino: v2, outro épico ou nunca]

### ✅ Critérios de Aceite
**[Área funcional 1]**
- [ ] [comportamento específico e testável]
**Qualidade (padrão em todo épico voltado ao usuário)**
- [ ] Telas seguem o Design System — indistinguíveis do restante do portal
- [ ] Responsivo desktop e mobile conforme protótipo
**Instrumentação (padrão em todo épico)**
- [ ] Eventos [X, Y] registrados — o KPI do Objetivo é mensurável no lançamento

### ❓ Aberto para refinamento técnico
[Exclusiva para decisão técnica pendente do time de engenharia — ex.: validação de arquitetura, viabilidade
de uma abordagem, escolha entre soluções técnicas. Pendência de produto, compliance ou negócio **não entra
aqui**: é discutida e resolvida entre PM, Orquestrador e o agente especialista certo (`vigilancia-regulatoria`,
`agente-discovery`, `agente-estrategico`) antes de o card ser criado ou fechado — não fica registrada como um
"aberto" à espera de terceiros. Esvazia após o refinamento: cada item vira decisão no Contexto ou critério de
aceite.]

### 🔗 Links
- Figma: [frame específico da seção, não o arquivo inteiro]
- Discovery: [Nome — link] · OKR: [Nome — link] (se não houver não inclua)
- Pré-requisito: [link — espelha a dependência waiting_on do sistema]

### 📜 Log de Decisões
[Só existe se houve mudança de escopo/estrutura DEPOIS da criação do item. Uma linha por
decisão: "DD/MM — o que mudou, objetivamente — link se houver." Não é para justificar o
porquê (isso é Contexto) — é registro factual, curto, sem prosa. Mantém o Contexto estável
e limpo para quem só quer entender o que construir hoje.]
```

**Regras de uso:**

- **Escopo define fronteira, não comportamento** — "usuário acessa X" pertence ao Escopo; "ao clicar em Y, sistema faz Z" pertence aos Critérios de Aceite. Não repita nos CAs o que já está no Escopo como capacidade.
- **Fora de escopo tem destino** — outro épico, v2 ou nunca; evita o "e onde isso vai ser feito?".
- **A decisão original de escopo vive no Contexto**, com data — é o "porquê" deste item existir do jeito que existe hoje. **Mudanças de escopo posteriores à criação** (consolidações, replanejamentos, redirecionamentos) **não reescrevem o Contexto** — vão para 📜 Log de Decisões, objetivas e sem poluir a leitura de quem só precisa entender o que construir.
- **Qualidade e Instrumentação são áreas fixas** dos critérios. Em ferramenta interna (backoffice),
  adaptar Qualidade para o padrão da ferramenta.
- **Delivery não entra em sprint com ❓ Aberto para refinamento técnico preenchida.**
- **Vínculo:** linked task com o Objetivo (quando houver) **e** com o Discovery de origem; pré-requisito na
  seção Links espelha uma dependência `waiting_on` real.
- **Feature nova declara seu kill switch** — se a funcionalidade pode precisar ser desligada sem
  deploy (integração externa, mecânica de risco), a flag de desativação entra no escopo ou em
  épico de gestão dedicado.

---

## Exemplo Real: Reposicionar o KYC facial antes do FTD com processamento em background

_(anterior às áreas padrão de Qualidade/Instrumentação — nos novos épicos, elas sempre entram)_

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
- Eliminar ou flexibilizar a obrigatoriedade do KYC (regulatório — nunca)
- Incentivos promocionais para concluir o KYC (avaliar em iniciativa de conversão)
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
- OKR: Otimizar o onboarding com KYC para elevar a conversão Cadastro → FTD — VL-11852
- Discovery: Investigar o gargalo de KYC no onboarding e definir direção de solução — VL-11235
- Figma: [Aguardando]
