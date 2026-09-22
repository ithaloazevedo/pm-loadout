# "Aberto para refinamento" renomeada e restrita a decisão técnica de engenharia

**Data**: 2026-08-11
**Tomada por**: Ithalo Mendes (via Orquestrador)
**Status**: APROVADA

---

## Contexto

Na tarefa de Delivery `868kq120w`/`868kpcu41` (teste A/B do fluxo de cadastro), a seção "❓ Aberto para
refinamento" acumulou tanto a validação técnica pendente do arquiteto (Bruno Urbano) quanto uma decisão de
desenho do experimento (MDE, duração, amostra) — misturando uma pendência de engenharia com uma pendência de
produto/analytics na mesma seção, sem distinção.

O PM sinalizou que não gosta desse uso genérico: a seção deveria existir **apenas** para decisão técnica
pendente do time de engenharia. Pendência de produto, compliance ou negócio deve ser discutida e resolvida
entre o PM, o Orquestrador e o agente especialista certo — não registrada no card como algo em aberto à espera
de terceiros.

Revendo `estilo-redacao.md`, o próprio guia de redação já orientava o oposto do que se quer agora: um exemplo
mostrava incerteza jurídica ("o artigo exato ainda está em confirmação com jurídico") sendo escrita na seção
Aberto — exatamente o padrão que deveria ter sido barrado.

## Opções Consideradas

1. **Manter a seção genérica ("qualquer dúvida a bater com a squad") e confiar em julgamento caso a caso** —
   Prós: nenhuma mudança de doc. Contras: sem critério objetivo, o mesmo padrão observado (compliance/produto
   misturado com técnica) tende a se repetir; já aconteceu uma vez.

2. **Renomear para "Aberto para refinamento técnico" e restringir o escopo a decisão técnica de engenharia,
   com triagem obrigatória no Orquestrador para tudo que não for técnico — escolhida.**
   - Prós: nome autoexplicativo evita a ambiguidade; a regra fica ancorada em três lugares que já se
     referenciam entre si (`template-delivery.md` define a seção, `estilo-redacao.md` define a regra de
     redação, `SKILL.md` do orquestrador garante a triagem antes do card) — sem duplicar o texto da regra em
     cada arquivo (mesma disciplina do precedente de observabilidade).
   - Contras: depende de o Orquestrador de fato acionar o agente especialista certo antes de aceitar uma spec
     como pronta — não há enforcement automático, é disciplina de processo.

3. **Criar uma seção nova separada por tipo de pendência (técnica / produto / compliance) dentro do próprio
   card** — Contras: mantém a pendência de produto/compliance visível no card como algo "em aberto", que é
   exatamente o padrão que o PM quer evitar — a resolução deve acontecer antes do card, não ficar registrada
   nele em outra aba.

## Decisão

Aprovada a Opção 2. Mudanças aplicadas nesta rodada:

- **Renomeação em todos os arquivos que referenciam a seção**: `template-delivery.md` (definição da seção),
  `agente-delivery.md`, `clickup-method.md`, `anti-pattern.md`, `estilo-redacao.md`.
- **Regra de escopo definida uma única vez**, em `estilo-redacao.md` → "Links, Decisões e Aberto para
  refinamento técnico: só com confirmação do PM": a seção é exclusiva de decisão técnica de engenharia
  (viabilidade, arquitetura, escolha entre abordagens). Pendência de produto/compliance/negócio nunca entra
  ali.
- **Exemplo de compliance na seção "Requisitos legais e normas" corrigido**: a incerteza sobre artigo exato de
  uma portaria deixa de ser exemplo de "vai para Aberto para refinamento" — passa a ser resolvida com
  `vigilancia-regulatoria`/jurídico **antes** de a frase ser escrita no Contexto.
- **Guardrail novo no `SKILL.md` do Orquestrador**: antes de considerar uma spec pronta para o
  `agente-delivery` criar/atualizar, toda pendência que não seja estritamente técnica precisa ser triada com o
  agente especialista certo (`vigilancia-regulatoria`, `agente-discovery`/`agente-estrategico`,
  `agente-governanca`) e resolvida com o PM na própria conversa — é isso que "garante que a discussão esteja
  acontecendo", em vez de depender de o agente-delivery filtrar sozinho no momento de escrever o card.

## Trade-offs Aceitos

- Nenhuma automação garante que o Orquestrador de fato rode a triagem — é uma disciplina reforçada por
  guardrail textual, não um bloqueio técnico. Se o padrão se repetir (pendência não-técnica voltando a
  aparecer em cards), é sinal de que precisa de um checklist mais forte no fluxo VALIDATE de `clickup-spec`.
- Ficou aberta, e não respondida aqui, a pergunta “onde registrar uma decisão de produto/analytics como MDE,
  duração e amostra de um teste A/B, se não no card?” — a resposta operacional adotada é: na conversa com o
  PM e, quando fechada, como fato no Contexto (não como pendência); não criei uma seção nova para isso.

## O que mudaria a decisão

Se a triagem manual se mostrar insuficiente (pendências não-técnicas continuarem aparecendo em cards mesmo
com o guardrail), o próximo passo é um checklist explícito no fluxo VALIDATE de `clickup-spec` que rejeite a
criação/aprovação de um item com conteúdo não-técnico em "Aberto para refinamento técnico" — hoje é regra
textual, poderia virar critério de validação ativa.

## Impacto

- **Produto**: nenhuma mudança de feature; muda como pendências de teste A/B, compliance e produto são
  tratadas antes de chegar ao ClickUp.
- **Técnico**: nenhuma integração nova; edições em `template-delivery.md`, `agente-delivery.md`,
  `clickup-method.md`, `anti-pattern.md`, `estilo-redacao.md`, `SKILL.md` do orquestrador.
- **Processo**: pendência de produto/compliance passa a ser resolvida em conversa (PM + Orquestrador + agente
  especialista) antes da criação/fechamento do card, não registrada como "aberto" nele.

## Links

- Tarefas que revelaram o uso genérico: `868kpcu41` / `868kq120w` ("[PAM] Estruturação de teste A/B cadastro")
- Decisão irmã (mesma sessão): [2026-08-11-remocao-drift-iniciativa-checklist-clickup.md](2026-08-11-remocao-drift-iniciativa-checklist-clickup.md)
- Regra de origem sobre especulação do agente: `agente-delivery.md` → "🚫 Especulação própria não vira conteúdo do card"
