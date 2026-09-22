# Épico de integração de provedores desmembrado em 6 épicos individuais, desvinculado do OKR de Receita B2B

**Data**: 2026-09-18
**Tomada por**: Ithalo Mendes (via Orquestrador + agente-delivery)
**Status**: APROVADA

---

## Contexto

O épico `868kf0wep` (título "Integração PG Soft") estava mal descrito: misturava três provedores (NGX, PGSoft, Evolution) sob um "portfólio estratégico" único, vinculado ao OKR "Receita B2B ≥X% da receita da vertical" (`868keau77`). O vínculo estava errado — esse OKR é sobre a Vertical vender tecnologia/conteúdo a terceiros (ex.: distribuição de Loteria via PNP/NGX), enquanto a motivação real desta iniciativa é o oposto: a PAM (Tradicional + Bravo) reduzir o custo de GGR pago a agregadores (Softswiss, Plug n Play) ao negociar diretamente com provedores de jogos, além de habilitar ações comerciais exclusivas (torneios, promoções — ex.: a Hacksaw já forneceu giros grátis ilimitados como parceira).

O card também citava "Hacksaw já tem task existente, não duplicar" apontando para `868kavbhj` — mas essa task estava finalizada e tratava de um pedido pontual (adicionar jogos de uma planilha GLI ao catálogo), não da integração comercial/técnica direta.

O PM trouxe a lista definitiva de provedores a integrar diretamente, com prioridade: PGSoft (maior), Pragmatic (segunda maior), Hacksaw (normal), Evolution e Zitro (baixa) — e pediu um épico por provedor em vez de um portfólio único.

## Opções Consideradas

1. **Manter um épico-portfólio único cobrindo os provedores** — mais simples de rastrear em um lugar, mas mistura ciclos de negociação comercial independentes e já havia se mostrado propenso a description drift (múltiplos provedores, um objetivo genérico).
2. **Um épico por provedor** — cada integração tem seu próprio ciclo de negociação comercial, prioridade e critérios de aceite; mais fácil de sequenciar e não bloqueia um provedor pelo atraso de outro.

## Decisão

Um épico por provedor. `868kf0wep` foi reaproveitado como o épico da PGSoft (reescrito do zero). Foram criados 5 novos: Pragmatic, Hacksaw, Evolution, Zitro e NGX (este último entrou como 6º provedor por decisão do PM, mesmo não estando na lista original — sua prioridade foi assumida como baixa, mesmo nível de Evolution/Zitro, **pendente de confirmação explícita do PM**). Nenhum dos 6 ficou vinculado ao OKR de Receita B2B. Nenhuma Iniciativa-pai foi criada — o nível Iniciativa/Objetivo foi removido do processo em 2026-09-10 (ver decisão [2026-09-10-migracao-esteira-continua-para-sprints-remocao-okr-e-discovery](2026-09-10-migracao-esteira-continua-para-sprints-remocao-okr-e-discovery.md)); os 6 ficam soltos como Projeto de Delivery direto no Backlog do folder Delivery:Backoffice & Integração.

## Trade-offs Aceitos

- Perde-se a visão consolidada num único card; rastrear o "portfólio de provedores diretos" como conjunto exige olhar os 6 separadamente (nenhum painel de agregação foi criado — não fazia parte do pedido).
- Campanhas/torneios/promoções específicas com cada provedor ficaram fora do escopo de cada épico técnico — tratadas como iniciativa futura de CRM/Marketing após a integração estar em produção.

## O que mudaria a decisão

Se o negócio quiser voltar a rastrear os 6 como uma única aposta estratégica (ex.: para reporte a diretoria), pode fazer sentido reintroduzir um agrupamento — mas isso exigiria decidir um novo mecanismo, já que o nível Iniciativa foi removido do processo.

## Impacto

- **Produto**: portfólio de provedores diretos passa a ser gerenciado como 6 iniciativas independentes, cada uma com seu próprio contrato comercial como pré-condição.
- **Técnico**: cada integração exige API própria, homologação, kill switch por provedor; certificação GLI e modelo de wallet (agregado vs. individual) ficam abertos para refinamento técnico por provedor.
- **Processo**: nenhuma mudança de fluxo — segue o modelo Projeto de Delivery direto no Backlog, sem Iniciativa-pai.

## Links

- PGSoft (atualizado): https://app.clickup.com/t/868kf0wep
- Pragmatic Play (novo): https://app.clickup.com/t/868m6yk8j
- Hacksaw (novo): https://app.clickup.com/t/868m6ykbw
- Evolution (novo): https://app.clickup.com/t/868m6ykd5
- Zitro (novo): https://app.clickup.com/t/868m6ykev
- NGX (novo, prioridade pendente de confirmação): https://app.clickup.com/t/868m6ykhm
- Task antiga de catálogo Hacksaw (não é duplicata, finalizada): https://app.clickup.com/t/868kavbhj
- Integração PNP (agregador, trilha separada — Hugo): https://app.clickup.com/t/868kapw4g
