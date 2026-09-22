# "Mencionar tarefa" (chip nativo do ClickUp) não é suportado pela API de Docs — report diário do PAM mantém hyperlink normal

**Data**: 2026-08-10
**Tomada por**: Ithalo Mendes (PM)
**Status**: APROVADA

---

## Contexto

O Ithalo notou, num print da página publicada, que uma linha de tarefa aparecia duas vezes: uma como
hyperlink azul comum (o que o script publicava) e outra, logo abaixo, como um **chip nativo do
ClickUp** — chevron, badge de status ao vivo (ex.: "TESTE EM DEV") e avatar do responsável. A segunda
tinha sido adicionada por ele manualmente no editor do ClickUp. Pediu para os itens do report virarem
esse tipo de referência nativa — a funcionalidade chama-se **"Mencionar tarefa"** no ClickUp.

## Investigação (duas hipóteses testadas, uma confirmada por documentação oficial)

**Hipótese 1 (errada): URL solta em vez de link com texto customizado.** O Ithalo criou uma página de
exemplo (`8ccvn07-50211`) que, lida via API, mostrava o padrão `Nome da tarefa (url solta)`. Uma página
de teste descartável (`8ccvn07-50231`) confirmou que o ClickUp normaliza uma URL solta submetida via API
para `[url](url)` — mesma forma armazenada do exemplo. Isso foi publicado no report real como se
resolvesse o pedido. **Estava errado**: o Ithalo reportou que não funcionou — a URL solta apareceu como
**texto morto** na página renderizada, nem virou link clicável, muito menos chip. A normalização de
armazenamento não implica renderização como chip nem como link.

**Resposta definitiva, via documentação oficial do ClickUp**
(`developer.clickup.com/docs/docsimportexportlimitations`, "Limitações de Formatação — Docs API"):
"Embed a task" está **explicitamente na lista do que a API NÃO suporta** — junto de "Embed a Doc",
"Embed a Whiteboard", embeds de YouTube/Vimeo/Loom/Miro/Google Drive, etc. "Mencionar tarefa" é
exatamente esse tipo de embed: um bloco nativo do editor rich-text do ClickUp, sem representação em
`text/md` nem `text/plain` — as duas únicas formas que a API de criação/edição de página aceita
(`content_format`). Não existe sintaxe de markdown, HTML ou marcação especial que crie esse bloco via
API; só é possível pelo editor visual do ClickUp (digitando "@"/"@@" e selecionando a tarefa).

O que a mesma documentação confirma como **suportado**: "Website link" — ou seja, o hyperlink markdown
comum (`[texto](url)`) sempre funcionou e continua sendo a melhor opção disponível via API.

## Decisão

Revertido `taskRef()` em `public/index.html` e no script headless de publicação para o formato de
hyperlink normal: `[Nome da tarefa](url) — Responsável · Squad` — o que já era o formato original antes
da tentativa com URL solta. Republicado o report do dia com os links funcionando novamente (a versão com
URL solta, que ficou como texto morto, foi publicada por menos de uma execução antes desta correção).

**"Mencionar tarefa" fica descartado como objetivo técnico** — não é uma questão de formato ou sintaxe,
é uma limitação de plataforma documentada oficialmente. Não há mais o que tentar nesse sentido via API.

## Trade-offs Aceitos

- **O report não terá o chip com status ao vivo e avatar** que o Ithalo viu funcionando quando ele
  mesmo mencionou a tarefa manualmente no editor. Isso só é possível fazendo a menção à mão, tarefa por
  tarefa, dentro do ClickUp — inviável para um report gerado automaticamente todo dia.
- Ficam no Doc duas páginas de teste descartáveis desta investigação (`8ccvn07-50231`, marcada
  `[pode apagar]`) — a API não permite apagar página de Doc.
- Se no futuro o ClickUp expuser essa funcionalidade via API (mudança de plataforma, não deste código),
  vale revisitar.

## O que mudaria a decisão

- Lançamento futuro de suporte oficial da API do ClickUp a "Embed a task"/"Mencionar tarefa" em páginas
  de Doc — não hoje.

## Impacto

- **Produto**: nenhum módulo de produto afetado — ferramenta interna de operação do PM.
- **Técnico**: `tools/radar-produto/public/index.html` (`taskRef` revertido para hyperlink),
  `README.md` corrigido. Script headless de publicação (fora do repositório) revertido. Republicado no
  Doc real com os links restaurados.
- **Processo**: nenhum.

## Links

- Código: `tools/radar-produto/public/index.html` (`taskRef`), `tools/radar-produto/README.md`
- Fonte oficial: [ClickUp — Docs API Limitations](https://developer.clickup.com/docs/docsimportexportlimitations)
- Doc de destino: [ClickUp — Report Status — PAM, 10/08/2026](https://app.clickup.com/9006076935/docs/8ccvn07-68891/8ccvn07-50191)
- Exemplo do Ithalo (mostra o chip funcionando manualmente): [`8ccvn07-50211`](https://app.clickup.com/9006076935/docs/8ccvn07-68891/8ccvn07-50211)
- Página de teste descartável: [`8ccvn07-50231`](https://app.clickup.com/9006076935/docs/8ccvn07-68891/8ccvn07-50231) — `[pode apagar]`
- Decisão relacionada (fusão num único report + recortes novos): [[2026-08-10-report-diario-pam-fusao-e-novos-recortes]]
