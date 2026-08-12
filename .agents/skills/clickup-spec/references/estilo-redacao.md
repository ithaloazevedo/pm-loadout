# Estilo de Redação — Contexto e Narrativa

Regras de como escrever qualquer seção narrativa de um card (Contexto, Objetivo do ciclo, comentários
de update) — em Objetivo, Discovery, Delivery e tickets operacionais. Aplica a todo agente que redige
corpo de card: `agente-delivery`, `agente-spec`.

## Por que isso existe

Quem lê um card — engenharia, design, outro PM, diretoria — precisa entender o **porquê** antes do
**o quê**. Um Contexto bem escrito reduz reunião de alinhamento: a pessoa sai sabendo por que aquilo
existe, qual dor resolve, o que sustenta a decisão e como medir se deu certo.

## Estrutura: Problema → Impacto → Solução

Toda narrativa de Contexto segue essa ordem — nunca começa pela solução:

1. **Problema** — o que acontece hoje, de forma factual.
2. **Impacto** — o que isso custa ao negócio ou ao usuário (conversão, receita, retenção,
   satisfação, tempo operacional, risco).
3. **Solução** — o que este item muda nisso (breve; o "como" detalhado fica no Escopo/Critérios).

> ❌ `Implementar integração com Serasa.`
> ✅ `Atualmente o fluxo depende de interpretações diferentes do retorno do Serasa, gerando bloqueios
> indevidos de jogadores. Esta iniciativa busca padronizar essa interpretação para reduzir falsos
> positivos e aumentar a conversão do cadastro.`

## Evidência, não adjetivo

Toda alegação de problema vem com um número ou uma fonte — nunca só um advérbio de intensidade.

> ❌ `É extremamente importante melhorar essa etapa.`
> ✅ `Hoje perdemos aproximadamente 40% dos usuários nesta etapa, impactando diretamente a conversão
> do cadastro.`

Pergunte-se: como sabemos que isso é um problema? Que dado sustenta — quantitativo (funil, evento,
analytics) ou qualitativo (entrevista, suporte, feedback)? Se não há dado ainda, diga isso
explicitamente ("hipótese não validada") em vez de forçar um número ou usar só adjetivo.

## Tecnologia é meio, não fim

Mesmo Contexto técnico se conecta a um indicador de negócio — a tecnologia aparece como o caminho,
não como o objetivo.

> ❌ `Implementar logs.`
> ✅ `Melhorar a observabilidade (capacidade de enxergar o que acontece no sistema em produção) para
> reduzir o tempo de detecção de incidentes, identificando mais rápido o impacto na jornada do
> jogador e diminuindo o MTTR (tempo médio de recuperação).`

Indicadores comuns para conectar: conversão, receita, retenção, satisfação, eficiência operacional,
tempo de atendimento, compliance, escalabilidade.

## Engenharia como parceira, não executora

Quando ainda há algo a validar, prefira verbos de descoberta a ordens de execução:

- "Precisamos validar..."
- "Precisamos descobrir..."
- "Precisamos confirmar..."
- "Existem alternativas..."

Isso vale sobretudo em Discovery. No Delivery, o escopo já está fechado — Escopo e Critérios de
Aceite são, sim, direção definida — mas o Contexto ainda explica o raciocínio que levou à decisão,
em vez de só mandar construir.

## Explique conceitos na primeira ocorrência

Assuma que quem lê pode ser novo no time ou de outra área. Termos como KYC, Observabilidade,
Conversão, Retenção, Feature Flag, Dashboard, Discovery ganham uma explicação rápida (parênteses ou
meia frase) na primeira menção do card. Depois disso, use o termo livremente.

## Linguagem executiva

- Frases objetivas, sem enrolação.
- Poucos adjetivos — troque por dado ou fato sempre que possível.
- Muito contexto (a informação por trás da frase), pouca retórica.

> ❌ `Considerando o contexto supracitado, faz-se necessária a revisão do fluxo...`
> ✅ `O fluxo acontece da seguinte forma...`

## Requisitos legais e normas: a implicação, não o texto jurídico

Regulação (Portaria, Lei, LGPD) entra pelo que ela obriga **na prática**, não pelo texto formal. Diga
o que muda para o usuário ou a operação; cite a norma como referência entre parênteses, não como
sujeito da frase.

> ❌ `Em conformidade com o disposto na Portaria SPA/MF nº 722/2024, artigo 12, faz-se necessária a
> implementação de verificação prévia ao depósito.`
> ✅ `A regulação exige que o KYC (verificação de identidade) aconteça antes do primeiro depósito —
> sem isso, a casa fica exposta a autuação (Portaria 722/2024).`

**Não cite o texto da lei entre aspas, nem encadeie vários artigos/portarias/notas técnicas em
sequência no meio do parágrafo** — isso lê como parecer jurídico, não como spec de produto. Regra
prática:

- Parafraseie o que a norma proíbe/exige, em uma frase, como faria para explicar a um colega no
  corredor.
- A citação (lei, artigo, portaria) vai **entre parênteses ao final da frase**, curta — não é o
  sujeito da frase.
- Se há mais de uma fonte legal com grau de confiança diferente (ex.: lei confirmada + portaria
  ainda sob leitura conflitante), a base **confirmada** entra no Contexto em uma frase. A parte
  **não confirmada** (artigo exato incerto, nota técnica não vista em fonte primária) **não vai para
  o card como pendência aberta** — "Aberto para refinamento técnico" é exclusiva de decisão técnica de
  engenharia, nunca de incerteza jurídica/compliance. Acione `vigilancia-regulatoria` (ou jurídico) e
  resolva a incerteza **antes** de escrever o Contexto; se não for possível resolver antes de criar o
  item, isso é motivo para segurar a criação, não para registrar a dúvida no card e seguir adiante.

> ❌ `A Lei nº 14.790/2023, art. 29, I, veda ao agente operador conceder "adiantamento, antecipação,
> bonificação ou vantagem prévia, ainda que a mero título de promoção, de divulgação ou de
> propaganda, para a realização de aposta". [...] a Portaria SPA/MF nº 1.231/2024 detalha essa
> vedação, mas o artigo exato ficou inconclusivo (art. 3º §4º II ou art. 42 §1º II)...`
> ✅ `A lei proíbe oferecer qualquer tipo de bônus ou vantagem para incentivar o cadastro antes da
> primeira aposta (Lei 14.790/2023, art. 29, I) — é por isso que campanhas de missão/recompensa não
> podem aparecer nessas rotas.` *(a existência e o artigo exato da portaria complementar foram
> confirmados com `vigilancia-regulatoria` antes de escrever esta frase — nunca deixados como dúvida
> registrada no card)*

## Contexto não é relatório do agente

Duas coisas que **nunca** entram no Contexto (nem em nenhuma outra seção do card), mesmo quando
verdadeiras e relevantes para você decidir a estrutura:

- **Nomes de Team Lead/Tech Lead ou estrutura de squads como justificativa.** "Squad X (Team Lead
  Fulano, Tech Lead Beltrano) é dona disso" é raciocínio interno do PM/Knowledge Graph — quem lê o
  card não precisa disso para entender ou executar. Se a squad importa para o escopo, cite a squad;
  não as lideranças.
- **Metadado do seu próprio processo de investigação** — termos de busca usados, datas de busca,
  "nenhum item relacionado encontrado no workspace". Isso é o registro do seu trabalho de agente, não
  informação de produto. Vai no seu texto de handoff para quem te invocou, nunca no corpo do card.

> ❌ `Rotas de cadastro e login são de propriedade da squad Plataforma (Team Lead Gabriel Moreschi,
> Tech Lead Rayan). A configuração de campanhas Smartico é de propriedade da squad Backoffice &
> Integrações (Team Lead Hugo, Tech Lead Ícaro).`
> ✅ `A solução fica do lado da squad Plataforma, dona da renderização de cadastro e login — não
> depende de mudar a configuração do Smartico nem de trabalho da squad Backoffice & Integrações.`

> ❌ `Nenhum item relacionado encontrado no workspace (busca realizada em 30/07 por "Smartico" e por
> "cadastro login rotas").`
> ✅ (omitir do card — mencionar no handoff da missão, se relevante para quem pediu a criação)

## Links, Decisões e Aberto para refinamento técnico: só com confirmação do PM

Essas três seções carregam **conteúdo que compromete o card publicamente** — um link errado, uma
decisão registrada sem ter sido tomada, ou uma dúvida que ninguém pediu para levantar. Por isso:

- Um achado da sua própria investigação (link candidato, dúvida que você levantou, sugestão de
  vínculo) é **proposto no handoff**, não escrito direto no card.
- Só escreva nessas seções o que já é decisão registrada (`knowledge/decisions/`) ou o que o PM
  confirmou explicitamente na conversa.
- Um item recém-criado nasce com essas seções **vazias ou mínimas** — não as preencha "para ser
  completo".

**❓ Aberto para refinamento técnico é exclusiva de decisão técnica de engenharia** — viabilidade de uma
abordagem, escolha de arquitetura, validação que só quem constrói pode dar (ex.: "caminho técnico X ainda
precisa ser validado pelo arquiteto"). **Pendência de produto, compliance ou negócio nunca entra aqui.** Esse
tipo de incerteza é discutido e resolvido entre o PM, o Orquestrador e o agente especialista certo
(`vigilancia-regulatoria` para compliance, `agente-discovery`/`agente-estrategico` para produto,
`agente-governanca` para qualidade) **antes** de o item ser criado ou considerado pronto — não fica registrado
no card como um "aberto" esperando que alguém resolva depois.

## Antecipe a pergunta de amanhã

Se existe uma pergunta óbvia que engenharia, design ou um stakeholder vai fazer amanhã, responda
hoje. É por isso que existem seções fixas como Restrições, Aberto para refinamento técnico e Dependências —
preencha-as com a mesma lente: riscos, suposições, limitações, dependências, métricas de sucesso.

## Espaçamento entre seções: sub-blocos colam, só `###` respira

Regra de formatação, não de narrativa — mas quebra a leitura do card quando ignorada, então é
guardrail:

- **Linha em branco só _entre_ seções de nível `###`** (🎯 Objetivo, 🧠 Contexto, 📋 Escopo,
  ✅ Critérios de Aceite…). Uma linha em branco separa uma seção da próxima — nunca duas.
- **Dentro de uma seção, sub-cabeçalhos em negrito colam nos bullets.** Sem linha em branco antes do
  sub-cabeçalho, sem linha em branco entre o sub-cabeçalho e seu primeiro item, e sem linha em branco
  entre um sub-bloco e o próximo.
- Vale sobretudo em **✅ Critérios de Aceite**, onde há vários sub-blocos em sequência (áreas
  funcionais + Qualidade + Instrumentação): todos colados, um bloco imediatamente após o outro. Um
  espaço extra ali cria um "buraco" visual que faz parecer que a seção acabou.

> ❌
> ```
> ### ✅ Critérios de Aceite
> **Migração e entrega**
> - [ ] Imagens passam a ser servidas a partir da AWS
> - [ ] Nenhuma imagem migrada permanece no bundle
>
> **Qualidade**
> - [ ] Carregamento validado em desktop e mobile
> ```
> ✅
> ```
> ### ✅ Critérios de Aceite
> **Migração e entrega**
> - [ ] Imagens passam a ser servidas a partir da AWS
> - [ ] Nenhuma imagem migrada permanece no bundle
> **Qualidade**
> - [ ] Carregamento validado em desktop e mobile
> ```

## Onde isso se aplica

| Seção | Como aplicar |
|---|---|
| 🎯 Objetivo / Objetivo do ciclo | 1-2 frases, mas ainda assim problema → valor, não só a ação |
| 🧠 Contexto (Delivery) | Problema → Impacto → Solução completo, com dado |
| 🧠 Contexto e Problema (Discovery) | Mesma estrutura; pode ter mais tensão/ambiguidade explícita — é discovery |
| Critérios de Aceite | Não é narrativa — aqui sim é objetivo e testável, sem prosa |
| Comentários de update | Contexto → decisão/fato → próximo passo (padrão em [clickup-method.md](clickup-method.md)) |
| Espaçamento (todas as seções) | Linha em branco só entre `###`; sub-blocos em negrito colados aos bullets (ver seção acima) |

---

Isso não substitui o tom de voz geral do Ithalo (frases de tamanho médio, sem clichês, sem emoji em
documento profissional) — é a aplicação específica dessa voz para a seção Contexto de specs no
ClickUp.
