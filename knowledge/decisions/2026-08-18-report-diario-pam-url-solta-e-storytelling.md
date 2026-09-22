# Report diário do PAM: reverte para URL solta (chip manual) e resumo executivo com storytelling ancorado em Voz do Cliente

**Data**: 2026-08-18
**Tomada por**: Ithalo Mendes (PM)
**Status**: APROVADA

---

## Contexto

Depois de publicar o report de 17/08/2026 no formato `[Nome da tarefa](url)` (hyperlink markdown,
decisão vigente desde 10-11/08/2026), o Ithalo comparou por print a página de 11/08/2026 — que mostra
cada tarefa como **chip nativo do ClickUp** (badge de status colorido tipo "FINALIZADO", avatar do
responsável) — com a de 17/08/2026, que mostra hyperlinks azuis comuns, sem chip. Pediu duas mudanças:
(1) toda referência de tarefa no report deve ser **URL solta**, porque é assim que ele consegue converter
em chip depois; (2) o resumo executivo deve ter mais storytelling e contexto de valor (o que importa para
as áreas), e menos recitação de número bruto.

## Investigação

O chip da página de 11/08/2026 **não veio da API** — isso já estava confirmado pela decisão
`2026-08-10-report-diario-pam-mencao-de-tarefa-nao-suportada-mantem-link.md`: "Embed a task" está
explicitamente fora do suporte da API de Docs do ClickUp, documentado oficialmente. O que mudou não foi
essa limitação (continua valendo, sem exceção), mas o entendimento do **mecanismo real**: o chip nasce
quando uma pessoa cola uma URL de tarefa dentro do editor visual do ClickUp — é um comportamento do
editor no momento do *paste*, não uma propriedade do conteúdo já salvo. O Ithalo faz isso manualmente,
tarefa por tarefa, toda vez que revisa o report (mesmo padrão documentado desde 10-11/08/2026: ele sempre
edita a versão publicada antes de compartilhar).

Isso explica por que ele quer URL solta em vez de link markdown no conteúdo que a API grava: uma URL
visível como texto simples é diretamente selecionável para copiar e colar de novo (acionando a conversão);
uma URL escondida atrás de `[Nome da tarefa](...)` exige "copiar link" em vez de selecionar texto — mais
fricção, sem ganho, já que ele vai substituir a referência de qualquer forma. A publicação via API
continua incapaz de gerar o chip diretamente — isso não mudou e não muda com este ajuste.

Sobre o resumo executivo: o Ithalo anexou também o relatório semanal de Voz do Cliente (10-17/08/2026,
1.046 sinais, 88% negativo). O board de Execução tem uma tarefa Pendente — "Suspeita de falha na
integração PAM ↔ Smartico (evento bet-win)... rollback de aposta" (868kp3yk7, Backoffice, alta
prioridade, com o Ícaro) — que é a mesma investigação por trás da 2ª dor mais citada no relatório de Voz
do Cliente (bug no Pinata Wins bloqueando saques, ~18 sinais). Já a dor nº1 do relatório (bônus não
creditam automaticamente, ~95 sinais) **não tem hoje um item dedicado e óbvio no board de Execução** —
gap real, não uma lacuna de dado.

## Decisão

1. **`taskRef()` em `tools/radar-produto/public/index.html`** volta a retornar só `t.url` (sem colchetes
   markdown). `buildProximaPrioridadeBySquad()` ajustado para `"Nome: " + t.url` (nome da pessoa
   continua, só a URL da tarefa fica solta).
2. **README.md** atualizado: a seção sobre referência de tarefa agora explica o mecanismo real (paste no
   editor visual aciona o chip, não o formato salvo via API) e deixa claro que isso não contorna a
   limitação de "Embed a task" — só viabiliza a conversão manual subsequente.
3. **Memória `feedback-clickup-url-crua-em-chat` corrigida**: a exceção antiga ("Doc via API exige
   markdown") estava errada e foi revogada — URL solta vale também no conteúdo publicado no Doc.
4. **Resumo executivo de 17/08/2026 reescrito** com storytelling ancorado em Voz do Cliente: abre citando
   as duas dores mais citadas no relatório semanal (bônus não creditando, Pinata Wins), conecta a segunda
   à tarefa Pendente correspondente no board, credita a resolução do incidente do Indique e Ganhe do
   próprio dia, e fecha no bloqueio que precisa de decisão (bonus abuser aguardando diretoria) — sem
   recitar contagens que já aparecem nos bullets abaixo.
5. Página `17/08/2026` do Doc **atualizada** (mesma página, não duplicada) com o novo texto executivo e
   todas as referências de tarefa em URL solta.

## Trade-offs Aceitos

- **Legibilidade cai para quem só lê o report sem converter os chips**: uma URL solta, sem nome de
  tarefa, não diz nada a quem não vai clicar ou converter — só quem abre o link (ou faz o paste-to-chip)
  recupera o contexto. Aceito porque o Ithalo é quem edita a página todo dia antes de ela circular mais
  amplamente, e o público final (diretoria) provavelmente só vê a versão já convertida em chip.
- O gap identificado (bônus não creditam automaticamente, dor nº1 do cliente, sem item dedicado no board)
  foi só **sinalizado** no resumo executivo — não foi criado um item de Discovery/Delivery para isso nesta
  sessão. Fica como recomendação, não como ação executada.

## O que mudaria a decisão

- Se o Ithalo decidir que quer o report legível por quem não vai converter chip nenhum (ex.: for
  compartilhado fora do time, para alguém que só lê), voltar para `[Nome](url)` ou usar um formato híbrido
  (nome antes da URL, mas na mesma linha, se isso não atrapalhar a seleção da URL).
- Se o ClickUp um dia suportar "Embed a task" via API, revisitar a automação de ponta a ponta (assunto já
  registrado como encerrado na decisão de 10/08/2026, mas reaberto ali mesmo como condição de mudança).

## Impacto

- **Produto**: nenhum módulo de produto afetado — ferramenta interna de operação do PM. Achado colateral
  relevante para produto: gap real de rastreamento para a dor nº1 de cliente (bônus não creditando)
  merece virar item de Discovery, fora do escopo desta decisão.
- **Técnico**: `tools/radar-produto/public/index.html` (`taskRef`, `buildProximaPrioridadeBySquad`) e
  `README.md` alterados. Memória `feedback-clickup-url-crua-em-chat` corrigida.
- **Processo**: primeira vez que o resumo executivo do report diário cruza dados de outro relatório
  (Voz do Cliente) em vez de só narrar atividade do board — vale repetir quando houver relatório de VoC
  disponível na janela do report.

## Links

- Código: `tools/radar-produto/public/index.html` (`taskRef`, `buildProximaPrioridadeBySquad`),
  `tools/radar-produto/README.md`
- Memórias: `feedback-clickup-url-crua-em-chat` (corrigida), `feedback-report-diario-pam-formato`
  (atualizada)
- Doc publicado: [ClickUp — Report Status — PAM, 17/08/2026](https://app.clickup.com/9006076935/docs/8ccvn07-68891/8ccvn07-50331)
- Decisões relacionadas: [[2026-08-10-report-diario-pam-mencao-de-tarefa-nao-suportada-mantem-link]],
  [[2026-08-11-report-diario-pam-template-final-e-formato-aprendido]],
  [[2026-08-18-report-diario-pam-paginacao-e-report-retroativo]]
