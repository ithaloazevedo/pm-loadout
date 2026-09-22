# Bloquear campanhas Smartico nas rotas de cadastro e login — item único para Tradicional + Bravo, classificado como Bug

**Data**: 2026-07-30
**Tomada por**: Ithalo Mendes
**Status**: APROVADA

---

## Contexto

Hoje a plataforma permite configurar campanhas do Smartico (fornecedor de gamificação/missões, integração headless via deep links) para serem renderizadas nas rotas de cadastro e login — comportamento indesejado, já ativo em produção, que precisa ser bloqueado tanto para a casa Tradicional quanto para a Bravo.

Achado relevante durante a investigação: existe uma tarefa correlata já finalizada — "Alteração no Processo de Login/Cadastro da Bravo" — que tinha uma subtask para **inserir** um banner redirecionando ao modal do Smartico nessas mesmas rotas. Ou seja, o comportamento que agora queremos bloquear foi, em algum momento, implementado deliberadamente pelo menos para a Bravo.

## Opções Consideradas

1. **Classificar como Bug** — comportamento indesejado já observável/reproduzível em produção.
   - Prós: segue a regra do workspace (produção → Bug; dev/homologação → Correção); reflete que o impacto (real ou potencial) já existe hoje.
   - Contras: nenhuma campanha Smartico precisa estar ativa nessas rotas *neste momento* para o Bug ser válido — a falha é a possibilidade de configuração existir, não um incidente pontual.

2. **Classificar como Tarefa de hardening** — tratar como melhoria preventiva.
   - Prós: mais alinhado a "nunca aconteceu, estamos prevenindo".
   - Contras: descartada — o achado da tarefa correlata da Bravo mostra que essa configuração já foi usada deliberadamente, então não é puramente hipotética.

3. **Um item por casa (Tradicional e Bravo separados)** vs. **um item único cobrindo as duas**.
   - Prós do item único: evita duplicidade enquanto não se sabe se o bloqueio é implementado de forma compartilhada (PAM único) ou por casa.
   - Contras: campo `_Projeto` (single-select Tradicional/Bravo) fica em branco, pois não suporta as duas casas simultaneamente.

## Decisão

Criado um único item tipo **Bug** — [Bloquear a renderização de campanhas Smartico nas rotas de cadastro e login](https://app.clickup.com/t/868kj5v0j) — cobrindo Tradicional e Bravo, no folder Delivery: Plataforma (squad Plataforma/Experiência do Jogador, dona das rotas de cadastro/login).

Fator decisivo: não há evidência de que a validação de bloqueio seja implementada separadamente por casa (o PAM é plataforma compartilhada) — desmembrar antecipadamente criaria duplicidade sem necessidade confirmada. A pergunta de arquitetura (bloqueio compartilhado vs. por casa, e em qual camada — configuração do Smartico no lado de Backoffice & Integrações vs. renderização da rota no lado de Plataforma) ficou registrada como pendência aberta dentro do próprio item, sem bloquear a criação.

## Trade-offs Aceitos

- Campo `_Projeto` (Tradicional/Bravo exclusivo entre si) ficou vazio — só o campo guarda-chuva `Empresa = Vertical` foi preenchido.
- Risco de o item precisar ser desmembrado em subtasks por casa mais adiante, se Plataforma e Backoffice & Integrações confirmarem que a implementação é separada.
- Nenhum vínculo formal a Objetivo/Iniciativa — o candidato mais próximo ("Elevar a conversão Cadastro → FTD de 37% para 70%") foi citado no corpo do item como sugestão, não linkado, por falta de match direto e claro.

## O que mudaria a decisão

- Se Plataforma (Gabriel/Rayan) e Backoffice & Integrações (Hugo/Ícaro) confirmarem que o bloqueio precisa de implementação separada por casa, o item deve ser desmembrado em subtasks (ou em um item complementar do lado de Backoffice & Integrações, na camada de configuração do Smartico).
- Se surgir evidência de que a rota de login carrega telas de jogo responsável, vale reavaliar acionamento de `vigilancia-regulatoria`.

## Impacto

- **Produto**: rotas de cadastro e login, Tradicional e Bravo.
- **Técnico**: integração Smartico (configuração de campanhas) e camada de renderização das rotas de cadastro/login no PAM.
- **Processo**: nenhuma mudança de processo; reforça o padrão de registrar pendência de arquitetura dentro do próprio item em vez de bloquear a criação por falta de confirmação técnica.

## Links

- Card criado: [868kj5v0j](https://app.clickup.com/t/868kj5v0j) — "Bloquear a renderização de campanhas Smartico nas rotas de cadastro e login"
- Tarefa correlata (histórico, finalizada): "Alteração no Processo de Login/Cadastro da Bravo" — subtask de inserção do banner Smartico nessas mesmas rotas.

---

## Atualização (30/07/2026)

Duas pendências deste registro foram resolvidas pelo próprio Ithalo, na sequência da mesma missão:

1. **Requisito regulatório confirmado**, com base legal verificada em fonte oficial primária: **Lei nº 14.790/2023, art. 29, I** — veda ao agente operador conceder "adiantamento, antecipação, bonificação ou vantagem prévia, ainda que a mero título de promoção, de divulgação ou de propaganda, para a realização de aposta". Missões/recompensas do Smartico exibidas antes do cadastro ou da primeira aposta se qualificam como essa vantagem prévia vedada. Regra de negócio explícita por trás do bloqueio: não incentivar cadastro com bônus ou equivalente.
   - Camada complementar, confiança menor, citada no card com ressalva: Portaria SPA/MF nº 1.231/2024 detalha a vedação, mas o artigo exato ficou inconclusivo (duas leituras conflitantes do PDF oficial — art. 3º §4º II ou art. 42 §1º II) — pendente de confirmação jurídica antes de citar número de artigo. Uma Nota Técnica SEI nº 229/2025 da SPA é reportada por fontes secundárias, não verificada em fonte primária.
2. **Pendência de arquitetura resolvida** (item 2 de "O que mudaria a decisão" acima, já não se aplica): o bloqueio vive 100% do lado da squad Plataforma, sem depender de mudança na configuração do Smartico pela squad Backoffice & Integrações.

Efeitos no card: prioridade alterada de `none` para `Urgente` (requisito regulatório ativo, mesmo padrão de outros itens regulatórios do workspace); campo KPIs trocado de `Segurança` para `Compliance`; novo grupo de Critérios de Aceite específico de compliance; seção "Aberto para refinamento" reduzida às duas pendências jurídicas remanescentes (artigo exato da Portaria 1.231/2024; existência/protocolo da Nota Técnica SEI 229/2025) — não bloqueiam o desenvolvimento, só impedem citação formal externa desses dois dispositivos até confirmação.

## Atualização 2 (30/07/2026) — pendências jurídicas resolvidas via `vigilancia-regulatoria`

As duas pendências acima foram fechadas com fonte oficial primária:

1. **Artigo exato confirmado**: **Portaria SPA/MF nº 1.231/2024, art. 42, §1º, II** (texto lido diretamente do DOU — https://www.in.gov.br/en/web/dou/-/portaria-spa/mf-n-1.231-de-31-de-julho-de-2024-575670297). A leitura alternativa "art. 3º §4º II" **não existe** no texto vigente — o Art. 3º não tem parágrafos; a confusão veio de dispositivos do Art. 4º. Confirmado sem alteração posterior (checadas as Portarias 2.217/2025 e 1.964/2026 — nenhuma altera o §1º do art. 42).
2. **Nota Técnica SEI nº 229/2025/MF confirmada existente** (gov.br/fazenda, código verificador SEI 47749330). Trata primariamente de cálculo de GGR para destinações da Lei 13.756/2018, mas cita o art. 42 §1º II como fundamento e transcreve a Pergunta 78 do FAQ oficial do Ministério da Fazenda: a vedação de vantagem prévia vale "para realização de cadastro ou para realização da primeira aposta" — ou seja, **deixa de se aplicar a um apostador que já apostou ao menos uma vez**.

**Novo ponto em aberto, gerado por essa apuração (ainda não decidido):** o card bloqueia renderização de campanha Smartico na rota de **login** de forma incondicional. A leitura oficial (Pergunta 78 do FAQ) sugere que a vedação legal é restrita a quem ainda não fez a primeira aposta — um apostador recorrente que já apostou não estaria mais protegido por essa norma específica. Falta decidir se o bloqueio de produto deve continuar amplo (mais simples, mais conservador do ponto de vista regulatório) ou ser restrito ao fluxo pré-primeira-aposta (potencialmente menos restritivo para o produto, mais complexo de implementar). Aguardando confirmação do PM antes de alterar critério de aceite ou Contexto.

Fontes: ver `🔗 Links` do card, atualizado nesta missão.
