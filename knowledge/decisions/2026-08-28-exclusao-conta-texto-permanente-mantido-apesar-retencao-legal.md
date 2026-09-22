# Jornada de exclusão de conta: texto "removidos de forma permanente" mantido apesar da retenção legal obrigatória de dados

**Data**: 2026-08-28
**Tomada por**: Ithalo Mendes (via Orquestrador + agente vigilancia-regulatoria)
**Status**: APROVADA

---

## Contexto

A Tradicional está lançando a jornada de "Excluir conta" (card [868kxmhp7](https://app.clickup.com/t/9006076935/868kxmhp7)), com fluxo já desenhado no Figma: saldo > R$1 bloqueia a exclusão (modal informativa pedindo saque); saldo ≤ R$1 permite exclusão com dupla confirmação, executando um **softdelete** do usuário.

O texto da modal principal (já validado no Figma) diz: *"Ao excluir sua conta, seu acesso será encerrado e seus dados serão removidos de forma permanente."*

Antes de especificar a tarefa como pronta para build, o Orquestrador acionou o agente `vigilancia-regulatoria` para checar se esse texto é compatível com as obrigações legais do setor de apostas.

## Opções Consideradas

1. **Ajustar o texto agora** — trocar "removidos de forma permanente" por linguagem que reflita a retenção legal (ex.: "dados exigidos por lei são retidos pelo prazo legal antes de eliminação").
   - Prós: elimina o risco de transparência/LGPD antes do lançamento.
   - Contras: exige retrabalho de copy/design já aprovado no Figma; atraso no lançamento.

2. **Manter o texto do Figma como está** — seguir com o design já aprovado, assumindo o risco apontado.
   - Prós: sem retrabalho, sem atraso.
   - Contras: risco de transparência (LGPD art. 6º, VI) e mensagem juridicamente imprecisa para o usuário.

3. **Pausar e acionar compliance/jurídico formalmente** antes de especificar.
   - Prós: elimina qualquer dúvida antes do build.
   - Contras: atraso indefinido para uma tarefa marcada como urgente.

## Decisão

Ithalo optou pela **Opção 2: manter o texto do Figma como está**, mesmo após o achado da vigilância regulatória de que:
- Casas de apostas são "pessoas obrigadas" ao regime de PLD/AML (Lei 9.613/1998, art. 10 §2º) e devem reter cadastro/KYC e histórico de transações por no mínimo 5 anos após encerramento da conta.
- A LGPD (art. 16, I) trata isso como exceção expressa ao direito de eliminação (art. 18) — a lei permite reter os dados, mas o texto atual não comunica isso ao usuário.
- O desenho técnico (softdelete) está correto; o problema identificado era exclusivamente de comunicação/transparência.

## Trade-offs Aceitos

- Risco de reclamação de usuário ou órgão de defesa do consumidor/ANPD por informação imprecisa sobre eliminação "permanente" dos dados, quando na prática KYC e histórico financeiro continuam retidos por obrigação legal (mínimo 5 anos, Lei 9.613/1998).
- Prazo exato de retenção (se são os 5 anos da Lei 9.613 ou algo distinto via Portaria SPA/MF nº 1.143/2024) não foi confirmado formalmente com compliance — a decisão segue sem esse número travado.

## O que mudaria a decisão

- Uma reclamação formal (ANPD, PROCON) ou pedido de auditoria que aponte o texto como enganoso.
- Compliance/jurídico formalizar que o prazo/tratamento exige comunicação explícita ao usuário.

## Impacto

- **Produto**: seção "Excluir conta" em Minha conta (PAM) — Tradicional.
- **Técnico**: softdelete do usuário, mantendo dados de KYC/transações internamente pelo prazo legal.
- **Processo**: nenhuma mudança — a spec segue para o `agente-delivery` sem pendência de compliance aberta no card, pois a decisão consciente de risco já foi tomada aqui.

## Links

- Card no ClickUp: [868kxmhp7](https://app.clickup.com/t/9006076935/868kxmhp7)
- Figma (modal principal): https://www.figma.com/design/UeS0CuNPLXxQ7Jl1Gq0Rqh/PAM---Minha-conta-%7C-Perfil?node-id=6047-5674
- Figma (bloqueio por saldo): https://www.figma.com/design/UeS0CuNPLXxQ7Jl1Gq0Rqh/PAM---Minha-conta-%7C-Perfil?node-id=6047-5676
- Figma (dupla confirmação): https://www.figma.com/design/UeS0CuNPLXxQ7Jl1Gq0Rqh/PAM---Minha-conta-%7C-Perfil?node-id=6047-5675
