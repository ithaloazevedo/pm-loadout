# Comunicações executivas e comentários de update sobre investigação em andamento sempre abrem com recap + número inline por achado

**Data**: 2026-08-13
**Tomada por**: Ithalo Mendes (PM)
**Status**: APROVADA

---

## Contexto

Na thread do caso "Pinata Wins — 25 giros" no ClickUp (workspace Vertical Tech), o Vitor Vianna cobrou
atualização de Ithalo e Ícaro sobre três perguntas em aberto que ele mesmo tinha levantado num
comentário anterior (com relatório em PDF anexo). Rascunhamos uma primeira versão da resposta —
tecnicamente correta, indo direto das perguntas (P1/P2/P3) para as respostas (R1/R2/R3) — mas ela
presumia que quem lesse já tinha aberto o PDF anterior para entender do que se tratava cada pergunta.

O Ithalo pediu explicitamente: "importante apresentar as evidências de forma mais clara,
contextualizando quem não leu relatórios anteriores de forma didática". A versão revisada — que abre
com um recap do que é a campanha/o caso, e traz o número junto de cada achado (ex.: "278 dos 374 casos
(74%) nunca apostaram no jogo X") antes da conclusão de cada item — foi aprovada com "gostei muito
dessa abordagem" e postada por ele mesmo na thread real. Na sequência, pediu para isso virar prática
padrão em "comunicações executivas e até mesmo em documentações de produto", e sinalizou que o resumo
executivo do report diário do PAM precisa do mesmo tratamento.

## Opções Consideradas

1. **Guardar só como memória de sessão** — mais rápido, mas repete o problema já observado com a
   regra Problema→Impacto→Solução: sem estar embutida em arquivo de sistema, fica sujeita a não ser
   recuperada/aplicada em sessões futuras sem o contexto certo.
   - Prós: nenhum atrito de manutenção de arquivo.
   - Contras: não é o que o Ithalo pediu; ele quer padrão, não lembrança implícita.

2. **Institucionalizar nos arquivos de referência que já orientam redação de comentário/update** —
   `estilo-redacao.md` e `clickup-method.md` (usados por `agente-delivery`/`agente-spec`), mais nota na
   memória do report diário do PAM.
   - Prós: mesmo tratamento já validado para a regra anterior de estilo; qualquer agente que carregar
     essas referências aplica a regra automaticamente, sem depender de recall de memória.
   - Contras: exige manter três pontos sincronizados (estilo-redacao.md, clickup-method.md, memória do
     report diário) em vez de um só.

## Decisão

Opção 2. Institucionalizada em três pontos:

1. `.claude/skills/clickup-spec/references/estilo-redacao.md` — nova seção "Recap antes de responder —
   quem não acompanhou o histórico não pode ficar perdido", e a linha "Comentários de update" da tabela
   final atualizada para citar a regra.
2. `.claude/skills/clickup-spec/references/clickup-method.md` — novo modelo de comentário "Resposta a
   investigação em andamento", ao lado dos demais modelos de update (Objetivo criado, Discovery
   iniciado/concluído, Delivery iniciado, Bug em produção).
3. Memória `feedback-report-diario-pam-formato.md` — nota nova aplicando a mesma prática ao parágrafo
   executivo do report diário do PAM (versão mais enxuta: 1-2 frases de recap, não um bloco por
   pergunta).

Memória nova `feedback-comunicacao-recap-evidencias-didaticas.md` registra o racional e linka os três
pontos acima como fonte estrutural.

## Trade-offs Aceitos

- Comentários e resumos ficam algumas frases mais longos por causa do recap — aceito porque o custo de
  retrabalho/mal-entendido de quem não acompanhou o histórico é maior que o custo de 1-2 frases extras.
- Três pontos para manter sincronizados em vez de um. Se um dos três for editado no futuro sem revisar
  os outros, a regra pode divergir entre "comentário de card" e "resumo executivo diário" — aceito
  porque cada ponto já tem uma nuance de aplicação diferente (bloco por pergunta vs. recap enxuto de
  1-2 frases) que não caberia bem numa fonte única.

## O que mudaria a decisão

Se o Ithalo sinalizar que o recap está deixando comunicações repetitivas em contextos onde a audiência
já é 100% ciente do histórico (ex.: troca fechada entre PM e o mesmo analista, sem terceiros
acompanhando), tornar o recap condicional à audiência em vez de sempre-presente.

## Impacto

- **Produto**: nenhum módulo de produto afetado.
- **Técnico**: nenhum sistema alterado — é regra de redação aplicada por quem escreve o
  comentário/report (humano ou agente), não lógica mecanizada em `tools/radar-produto`.
- **Processo**: muda a forma de redigir comentários de update que respondem investigação em andamento e
  o parágrafo executivo do report diário do PAM.

## Links

- Thread de origem: [ClickUp — caso Pinata Wins 25 giros](https://app.clickup.com/9006076935/chat/r/8ccvn07-66191/t/80110054544583)
- Arquivos alterados: `.claude/skills/clickup-spec/references/estilo-redacao.md`,
  `.claude/skills/clickup-spec/references/clickup-method.md`
- Memórias: `feedback-comunicacao-recap-evidencias-didaticas.md`,
  `feedback-report-diario-pam-formato.md` (atualizada)
- Decisão relacionada (mesmo tratamento aplicado antes, para outra regra de estilo):
  [[2026-08-10-evolucao-operacional-pm-loadout]]
