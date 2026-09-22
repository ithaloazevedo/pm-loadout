# Três Épicos de bônus no backoffice, órfãos e sem documentação, viram épicos irmãos documentados — sem consolidar num só

**Data**: 2026-09-18
**Tomada por**: Ithalo Mendes (PM), via Orquestrador + agente-delivery (levantamento) + agente-spec (desenho) + agente-delivery (escrita)
**Status**: APROVADA

---

## Contexto

O PM identificou "várias tasks relacionadas ao bônus no backoffice" soltas no Backlog do folder Delivery:
Operação e afiliados (lista `901114029782`) e pediu para transformar isso num épico — ou alguns épicos — com
o(s) pai(is) bem documentado(s) cobrindo o escopo completo.

O levantamento revelou que a estrutura já existia, só nunca foi documentada: **3 Épicos-irmãos** haviam sido
criados em 24/08/2026, todos em `em refinamento`, todos com **descrição vazia**, conectados a 17 itens-filho
por linked task (não hierarquia subtask/parent) — 15 desses filhos eram só título, sem escopo. O item mais
maduro e urgente do conjunto (868kw7jau, confiabilidade da integração com a Smartico) nasceu do incidente
**PROMOCOD15** (21/08/2026, prejuízo apurado de R$ 300.000: corrida de clique + bug de deploy que zerou o
teto de uma campanha promocional) e estava linkado ao épico errado por tema, não por conteúdo real. O Épico
de "Proteção contra abuso" também carregava 2 vínculos cross-squad (itens do time PAM/Plataforma, não do
Backoffice).

## Opções Consideradas

1. **Consolidar em 1 épico único "Bônus no Backoffice"** com os 17 itens como subtasks.
   - Prós: visão executiva mais simples.
   - Contras: mistura 3 temas heterogêneos (dados/formulário, máquina de estados, segurança/antifraude) num
     item difícil de fechar em sprints; a hierarquia do workspace é achatada — Épico é o nível mais alto do
     processo, não há nível "pai" acima dele para abrigar um guarda-chuva formal.

2. **Manter os 3 Épicos separados por sub-tema, documentando cada um** (escolhida)
   - Prós: cada sub-tema é uma entrega própria, com objetivo/escopo/critérios de aceite distintos; preserva a
     estrutura já criada no ClickUp, só corrige vínculos e preenche a documentação que nunca existiu.
   - Contras: nenhum guarda-chuva único para reportar "bônus no backoffice" como iniciativa agregada — mas
     esse nível não existe no processo atual de qualquer forma (ver `knowledge/domains/processo.md`).

## Decisão

Escolhida a **Opção 2**. Os 3 Épicos seguem separados e foram documentados via `template-delivery.md`:

- **[868kw7h51](https://app.clickup.com/t/868kw7h51) — Padronização e sincronização da gestão de bônus no
  backoffice com a Smartico**: reúne a confiabilidade ponta a ponta da integração (868kw7jau, decorrente do
  PROMOCOD15, mantido aqui por decisão do PM apesar do conteúdo tangenciar "proteção contra abuso") e a
  padronização operacional do formulário/dados de bônus (6 itens antes só com título).
- **[868kw7h58](https://app.clickup.com/t/868kw7h58) — Ciclo de vida e status do bônus**: item mais maduro
  (868kw7jdm, medir progresso por giros da campanha em vez de por jogador) já está em desenho ativo com
  Allison Macedo — os outros dois (status Inativo/Completo) seguem como hipótese a validar em refinamento,
  sem evidência registrada até aqui.
- **[868kw7h5c](https://app.clickup.com/t/868kw7h5c) — Proteção contra abuso de bônus**: gestão individual e
  em massa de bônus ativos concedidos indevidamente (868kw88rr, 868kw88ma — únicos 2 itens que já tinham
  descrição completa antes desta missão). **Desvinculados** 868kparmw e 868kw7jem (squad PAM/Plataforma, sem
  relação direta com o tema) — não foram excluídos, só desvinculados deste épico.

**Dupla checagem antes de liberar um bônus** (critério do Épico 1): definida como regra interna simples —
qualquer dupla de operadores distintos, sem papéis formais nem envolvimento de compliance/jurídico.

## Trade-offs Aceitos

- Os 6 itens de padronização do Épico 1 e os 2 itens de status do Épico 2 seguem com Critérios de Aceite
  **inferidos a partir só do título** (nunca tiveram escopo escrito por ninguém) — aceito como ponto de
  partida para validar em refinamento com a squad, não como fato confirmado.
- 868kw8yw8 (épico anterior de integração com a Smartico, marcado "finalizado" em 01/09 mas contestado pela
  própria 868kw7jau, e na pasta errada — Delivery: Plataforma em vez de Backoffice) **não foi tocado** — fica
  como pendência separada, fora do escopo desta missão.
- 3 tasks com "bônus" no título ficaram **fora** dos 3 épicos por não se encaixarem nos sub-temas sem
  investigação própria: 868kmm8qn (bônus de loteria por modalidade — pode ser tema de Provedora/Loteria, não
  backoffice), 868kf41ng (repasse de conhecimento — tarefa operacional, não entrega de produto), 868kw7jf0
  (alerta de estouro financeiro — já pertence a outro épico de risco de pagamento).
- Nenhum dos 3 épicos ganhou assignee — atribuição fica pendente de decisão manual do PM.

## O que mudaria a decisão

- Se a verificação item a item de 868kw7jau concluir que as frentes do épico anterior (868kw8yw8) não foram
  implementadas, isso reforça (não contradiz) a decisão de mantê-lo como frente ativa do Épico 1.
- Se o refinamento com a squad invalidar a hipótese dos status Inativo/Completo do Épico 2 (ex.: não há caso
  de uso real para "Inativo"), o épico perde 2 de seus 3 itens e pode valer reavaliar se ainda se sustenta
  como épico próprio ou vira só uma extensão do item de progresso por giros.
- Se a fusão organizacional Backoffice+Plataforma em Time PAM (ver
  [[2026-09-18-fusao-backoffice-plataforma-em-time-pam]]) evoluir para fusão também da estrutura técnica no
  ClickUp, os vínculos cross-squad removidos do Épico 3 podem fazer sentido de outra forma — reavaliar então.

## Impacto

- **Produto**: Backoffice (gestão de bônus, telas de Ações Rápidas → Bônus, formulário de criação de bônus).
  Nenhuma mudança de escopo de produto além da documentação — os itens já existiam, só não tinham conteúdo.
- **Técnico**: integração com a Smartico (as 33 views trad_prd→Smartico, código promocional), backoffice
  (formulário de bônus, tela de perfil do jogador), sem decisão de arquitetura tomada aqui (mecanismo de
  sincronização e estratégia de migração de ID seguem em "Aberto para refinamento técnico").
- **Processo**: nenhuma mudança de fluxo — os 3 itens seguem `em refinamento` no Backlog do squad Backoffice,
  status e task_type inalterados.

## Links

- Épico 1: https://app.clickup.com/t/868kw7h51
- Épico 2: https://app.clickup.com/t/868kw7h58
- Épico 3: https://app.clickup.com/t/868kw7h5c
- Item do incidente PROMOCOD15: https://app.clickup.com/t/868kw7jau
- Decisão relacionada (fusão organizacional que motivou parte da ambiguidade cross-squad):
  [[2026-09-18-fusao-backoffice-plataforma-em-time-pam]]
- Decisão relacionada (origem do vínculo removido 868kparmw):
  [[2026-09-02-banca-beneficios-bloqueio-apenas-sem-ftd]]
