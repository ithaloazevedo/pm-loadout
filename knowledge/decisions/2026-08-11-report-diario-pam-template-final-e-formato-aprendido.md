# Report diário do PAM: template final (sem responsável/squad na linha, dev/designer por squad, comentário só quando essencial)

**Data**: 2026-08-11
**Tomada por**: Ithalo Mendes (PM)
**Status**: APROVADA

---

## Contexto

Depois de publicar o report do dia 10/08/2026 no template pedido (Resumo do dia + 5 números + Novas
prioridades/Finalizado/Em teste/Bloqueado/Próxima prioridade por dev e designer), o Ithalo editou a
página manualmente antes de compartilhar e pediu para eu comparar o que mudou e guardar na memória o que
fizer sentido para os próximos reports ficarem mais próximos do que ele quer.

## Investigação

Comparei o conteúdo publicado por mim contra o conteúdo final editado por ele (via
`GET .../pages/:id?content_format=text/md`). Achados, por categoria — detalhados na memória
`feedback-report-diario-pam-formato`:

1. **Linha de tarefa sem responsável/squad** — ele removeu o sufixo "— Responsável · Squad" de toda
   linha nas seções de lista simples. Só "Próxima prioridade por dev/designer" mantém nome de pessoa,
   porque ali é o rótulo da linha, não repetição.
2. **Corta quase todo comentário** — de ~9 citações que incluí, manteve 1, reformatada como texto inline
   (`Nome (url): comentário`) em vez de citação em bloco.
3. **"Próxima prioridade por dev" agrupada por squad** — dois subtítulos em negrito
   (`**Time Backoffice & Integrações:**` / `**Time Plataforma:**`), não lista achatada alfabética.
4. **Texto executivo** — várias correções de tom (ver memória): declarar fato direto em vez de "o caso
   que chamamos de X"; "mitigado" ≠ "corrigido"; sem fricção de processo interno na narrativa; item
   secundário/não confirmado fica só na seção relevante, não repetido no parágrafo de abertura; frase de
   transição pro board vai direto pros bullets sem comentário depois.
5. **"Próxima prioridade por designer" sumiu da versão dele** — não confirmado se foi porque não havia
   item de designer relevante naquele dia ou decisão de tirar a seção. Registrado como aberto, não como
   regra.

Testei também uma hipótese técnica: será que URLs com ID customizado (`.../t/9006076935/VL-14233`, que
apareceram em alguns dos links editados por ele) resolvem o problema de "mencionar tarefa" documentado
na decisão anterior? **Não resolvem** — testei publicando os dois formatos (ID curto e customizado) numa
página descartável; a API normaliza ambos de forma idêntica (`[url](url)`). A diferença nos links dele
era só reflexo de ter copiado pelo botão "Copy Link" do ClickUp (que usa ID customizado quando a tarefa
tem um configurado).

Achado colateral: uma página de teste anterior (`8ccvn07-50231`, marcada `[pode apagar]`) tinha sido
apagada — mas pelo Ithalo, pela interface do ClickUp, não por mim. Confirma que a API não tem `DELETE`
de página, mas a UI tem essa capacidade.

## Decisão

1. **Memória nova**: `feedback-report-diario-pam-formato.md` — registra as 5 categorias de aprendizado
   acima, para orientar tom e formato das próximas gerações do report, ligada a `tom-de-voz-ithalo`.
2. **Código atualizado** em `tools/radar-produto/public/index.html`:
   - `taskRef()` simplificado para `[Nome](url)`, sem sufixo de responsável/squad.
   - `computeDailyPamData()` agora retorna `proximaPrioridadeDev` e `proximaPrioridadeDesigner`
     separados (split por roster fixo `DESIGNERS = ["Allison Macedo", "Linecker Gomes"]`, espelhando
     `knowledge/domains/pessoas.md`), cada um agrupável por squad.
   - `buildProximaPrioridadeBySquad()` (novo) gera os dois subtítulos em negrito por time.
   - `buildPamDailyMarkdown()` reescrito para o template final: título `# Resumo do dia dos times PAM`,
     sem a tabela de quebra por squad (o Ithalo tirou ao editar), ordem de seções
     Novas prioridades → Finalizado hoje → Em teste → Bloqueado → Próxima prioridade por dev → Próxima
     prioridade por designer.
   - Comentário de código atualizado para deixar explícito que o mecanismo de comentário deve ser usado
     com parcimônia, não como anexo automático.
3. **README atualizado** com o template final, a correção sobre URL de ID customizado, e a correção
   sobre apagar página (API não permite, UI permite).

## Trade-offs Aceitos

- **"Próxima prioridade por designer" pode desaparecer silenciosamente** em dias sem item de designer
  pendente — isso é esperado (`buildProximaPrioridadeBySquad` retorna "Ninguém com item pendente
  priorizado." nesse caso), não um bug. Se o Ithalo queria a seção removida de vez em vez de aparecer
  vazia, é um ajuste diferente do que foi implementado — fica para confirmar na próxima execução.
- A "parcimônia" de comentário continua sendo um julgamento editorial, não uma regra mecanizável — o
  filtro automático do botão (sem LLM) continua sendo só um piso mecânico (>15 caracteres), não aplica a
  parcimônia de verdade. Só uma sessão do Claude aplica o critério completo.
- Roster de designers (`DESIGNERS` em `index.html`) é uma lista fixa duplicada de `pessoas.md` — se a
  squad mudar (novo designer, alguém sai), precisa atualizar os dois lugares manualmente.

## O que mudaria a decisão

- Se o Ithalo confirmar que quer a seção "Próxima prioridade por designer" removida quando vazia (em vez
  de aparecer com a frase "Ninguém com item pendente priorizado."), ajustar `buildPamDailyMarkdown` para
  omitir a seção inteira nesse caso.
- Se a squad mudar a composição de designers, atualizar `DESIGNERS` em `public/index.html`.

## Impacto

- **Produto**: nenhum módulo de produto afetado — ferramenta interna de operação do PM.
- **Técnico**: `tools/radar-produto/public/index.html` (`taskRef`, `computeDailyPamData`,
  `buildProximaPrioridadeBySquad`, `buildPamDailyMarkdown`) e `README.md` alterados. Memória nova
  `feedback-report-diario-pam-formato`. Testado via API (custom ID vs ID curto); sintaxe do JS validada.
- **Processo**: nenhum.

## Links

- Código: `tools/radar-produto/public/index.html`, `tools/radar-produto/README.md`
- Memória: `feedback-report-diario-pam-formato.md`
- Doc de destino: [ClickUp — Report Status — PAM, 10/08/2026](https://app.clickup.com/9006076935/docs/8ccvn07-68891/8ccvn07-50191)
- Decisões relacionadas (mesmo report, dias anteriores):
  [[2026-08-10-report-diario-pam-fusao-e-novos-recortes]],
  [[2026-08-10-report-diario-pam-mencao-de-tarefa-nao-suportada-mantem-link]]
