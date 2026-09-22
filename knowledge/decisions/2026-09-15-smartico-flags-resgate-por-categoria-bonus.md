# Sincronização com a Smartico expande de status único do Cashback para 5 flags booleanas de resgate por categoria de bônus

**Data**: 2026-09-15
**Tomada por**: Ithalo Mendes (PM), via Orquestrador + agente-spec + agente-delivery
**Status**: APROVADA

---

## Contexto

O card [868m4jcw5](https://app.clickup.com/t/9006076935/868m4jcw5) nasceu escopado para sincronizar, numa única propriedade genérica da Smartico (`core_custom_prop1`, então sem uso por nenhuma automação), o status de resgate de apenas 3 bônus de Cashback Manual (`web_bonus_id` 8506, 8539, 8540), lido de `web_bonus_entities.status` no PAM.

Isso é consequência direta da decisão [[2026-09-01-resgate-manual-bonus-expira-sem-credito-tradicional]]: desde que a Banca de Benefícios da Tradicional passou a exigir resgate manual (bônus expira sem crédito se o jogador não resgatar no prazo), a taxa de resgate caiu de ~80% para ~50% — o risco que aquela decisão já registrava como algo a monitorar se confirmou.

Após refinamento com Hugo Fernandes Vieira (engenharia) e Vitor Vianna (solicitante), o PM decidiu expandir o escopo: em vez de refletir só Cashback, a Smartico passa a receber, para cada uma das 5 categorias de bônus da Banca de Benefícios, uma propriedade booleana por jogador — permitindo ao CRM automatizar notificações (app, SMS, e-mail) por categoria para induzir o resgate antes da expiração.

## Opções Consideradas

1. **Manter escopo restrito a Cashback, tratar as outras 4 categorias como cards futuros**
   - Prós: entrega mais rápida, sem depender de validar fonte de dado das outras categorias.
   - Contras: não resolve o problema de negócio (queda de conversão) para 4 das 5 categorias; motivo original do refinamento era justamente ampliar.

2. **Expandir para as 5 categorias com uma flag booleana por categoria e por jogador** (escolhida)
   - Prós: cobre o problema de negócio por completo; modelo mais simples para o CRM consumir (booleano vs. status codificado `P`/`B`); reaproveita a fonte já validada (`web_bonus_entities.status`) como padrão a estender.
   - Contras: assume, sem validação técnica ainda feita, que as outras 4 categorias têm fonte de status no PAM tão granular quanto a de Cashback — risco registrado como pendência técnica.

## Decisão

Escolhida a **Opção 2**. O card único é atualizado (não criado de novo) para cobrir as 5 categorias, com uma propriedade booleana por categoria:

- `tem_ficha_gratis_resgatavel` (Fichas Grátis)
- `tem_giro_gratis_resgatavel` (Giros Grátis)
- `tem_supercotacao_resgatavel` (Supercotação)
- `tem_cashback_resgatavel` (Cashback — substitui o uso de `core_custom_prop1`)
- `tem_saldo_bonus_resgatavel` (Saldo Bônus)

**Regra única para as 5**: `true` enquanto existir pelo menos um bônus pendente de resgate naquela categoria para o jogador; `false` quando não houver nenhum pendente (resgatado ou expirado).

Essa regra foi desenhada deliberadamente para **não decidir** política de expiração — a tarefa apenas espelha o estado real do PAM. Isso destrava, sem reabrir, o conflito registrado em [[2026-09-01-resgate-manual-bonus-expira-sem-credito-tradicional]] entre a regra geral ("expira sem crédito") e a proposta divergente de auto-resgate do cashback (`868kt4t1j`): qualquer que seja o mecanismo interno de cada categoria, a flag só reflete se há algo pendente agora.

Nomenclatura confirmada com o PM entre duas opções — prevaleceu a forma padronizada (singular consistente, com `_gratis` explícito) sobre a forma abreviada inicialmente esboçada, para reduzir ambiguidade de termos como "ficha"/"giro" isolados no domínio de cassino.

## Trade-offs Aceitos

Aceita-se abrir mão de confirmar, antes de fechar a spec, se as 4 categorias além de Cashback têm de fato uma fonte de status no PAM tão granular quanto `web_bonus_entities.status` — isso fica como pendência técnica explícita ("Aberto para refinamento técnico"), não como bloqueio de produto, porque é uma pergunta que só engenharia responde e não muda a direção do escopo, só sua viabilidade de implementação imediata.

Aceita-se também que o mapeamento categoria → `web_bonus_id` continue potencialmente manual (como já é hoje só para Cashback), com risco de manutenção: bônus novo lançado no futuro não entraria automaticamente na sincronização até alguém curar a lista.

## O que mudaria a decisão

- Se a investigação técnica revelar que uma ou mais categorias não têm fonte de status equivalente no PAM, essa categoria pode precisar de escopo/abordagem própria (card separado), quebrando a premissa de "mesmo padrão para as 5".
- Se a Smartico já usar `core_custom_prop1` (ou as properties equivalentes) em outra automação não identificada, há conflito a resolver antes do build.
- Taxa de resgate após o lançamento: se a automação de CRM não recuperar parte da queda de 80%→50%, vale reavaliar se o gargalo é falta de dado (resolvido por este card) ou o desenho do resgate manual em si.

## Impacto

- **Produto**: Banca de Benefícios (Tradicional) — habilita o CRM a agir por categoria de bônus pendente de resgate, mitigando o efeito colateral já previsto pela decisão de resgate manual.
- **Técnico**: PAM (`web_bonus_entities.status`, possível necessidade de taxonomia de categoria no catálogo de bônus), Smartico (properties customizadas por jogador, mecanismo de sincronização a definir).
- **Processo**: nenhuma mudança de fluxo — segue como Tarefa avulsa no folder Delivery: Backoffice & Integração, mesmo assignee/solicitante do card original.

## Atualização — 2026-09-15: par de evento (client action) fica em card separado, squad Plataforma

No mesmo dia, o PM pediu que a Smartico também receba um **evento pontual** de resgate — uma client action `bonus_resgatado`, disparada no instante exato em que o jogador resgata um bônus, complementar ao **estado** (as 5 flags booleanas) já coberto acima. Estado e evento resolvem necessidades diferentes: a flag permite consultar "tem algo pendente agora?" a qualquer momento; a client action permite ao CRM reagir no mesmo instante do resgate (parar um lembrete, disparar um agradecimento), sem esperar o próximo ciclo de sincronização.

**Decisão de escopo**: card separado, não uma seção a mais no 868m4jcw5, porque o time responsável é outro. Quem constrói a tela "Meus Bônus" e o fluxo de resgate manual em si é o squad Plataforma (Experiência do Jogador) — não Backoffice & Integrações, que só lê o resultado depois no PAM. O card nasceu no Backlog do folder Delivery: Plataforma, sem assignee definido ainda.

**Decisão de modelagem**: uma client action única e genérica (`bonus_resgatado`) com a categoria como atributo — não uma ação por categoria — usando os mesmos valores de categoria das 5 flags (`cashback`, `ficha_gratis`, `giro_gratis`, `supercotacao`, `saldo_bonus`), para não precisar criar um novo tipo de evento na Smartico a cada categoria nova. Payload inclui também identificador do bônus, timestamp e valor do bônus resgatado (este último para personalizar mensagens de agradecimento no CRM — disponibilidade técnica ainda não confirmada, ver Aberto para refinamento técnico do card).

Os dois cards foram linkados como "Relacionado" para que ninguém leia um isoladamente e assuma que é a solução completa.

## Links

- Card no ClickUp (estado — 5 flags booleanas): [Sincronizar o status de resgate por categoria de bônus com a Smartico para o CRM agir antes da expiração](https://app.clickup.com/t/9006076935/868m4jcw5)
- Card no ClickUp (evento — client action de resgate): [Notificar a Smartico assim que o jogador resgatar um bônus, para o CRM agir no mesmo instante (client action)](https://app.clickup.com/t/868m5k7v1)
- Decisão anterior relacionada: [[2026-09-01-resgate-manual-bonus-expira-sem-credito-tradicional]]
- Card do cashback com regra divergente ainda não unificada: https://app.clickup.com/t/868kt4t1j
