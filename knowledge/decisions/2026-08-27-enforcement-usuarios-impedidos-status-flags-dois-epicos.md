# Enforcement de usuários impedidos separa status de permissões, abandona soft delete e vira dois Épicos irmãos (Backoffice & Integrações + Plataforma)

**Data**: 2026-08-27
**Tomada por**: Ithalo Mendes (via Orquestrador + agentes vigilancia-regulatoria, agente-spec, agente-delivery)
**Status**: APROVADA

---

## Contexto

Ithalo trouxe uma transcrição de reunião já organizada (problema, regra de negócio, arquitetura esperada, tarefas) sobre a implementação atual de usuários **impedidos** não estar aderente ao comportamento esperado: hoje o impedimento é tratado via soft delete ou mudança de status que não garante bloqueio imediato de todas as ações, gerando risco regulatório (usuário impedido pode continuar depositando/apostando/usando bônus dependendo do fluxo e do timing dos workers).

Pediu a criação de um Épico. Antes de fechar a spec, o Orquestrador acionou `vigilancia-regulatoria` (pendência de compliance não pode ficar em aberto no card, conforme [[2026-08-11-aberto-para-refinamento-tecnico-restricao-de-uso]]) e `agente-spec` em paralelo, seguindo o mesmo padrão do precedente [[2026-08-14-geolocalizacao-portaria-722-legitimuz]].

## Achados

1. **Regra de negócio já decidida em reunião é compatível com a regulação — e mais conservadora em alguns pontos**: confirmado por `vigilancia-regulatoria` (fontes: Lei 14.790/2023 Art. 26; Portaria SPA/MF 1.231/2024; Portaria 2.579/2025 + IN SPA/MF 31/2025 — autoexclusão/SIGAP; Portaria 2.217/2025 — Bolsa Família/BPC; Portaria 1.237/2026 — Novo Desenrola). Bloqueio imediato de novas apostas é requisito textual (Art. 7º, IN 31/2025). Login e saque liberados não é concessão de produto — a norma pressupõe conta operável para saque durante a janela de notificação (até 1 dia) e retirada de saldo (até 2 dias) antes do encerramento formal (até 3 dias). Bloquear depósito e bônus é decisão de risco do produto, mais conservadora que o texto normativo (que só menciona bloqueio de apostas), não um requisito legal literal.
2. **CPF, não o ID interno do operador, é a chave de correlação do SIGAP** (Art. 5º, IN 31/2025) — recriar cadastro com novo ID interno não quebra rastreabilidade perante o SIGAP, mas quebra continuidade de histórico interno de AML/compliance se esse histórico estiver amarrado ao ID antigo. Risco de arquitetura de dados interna, não descumprimento regulatório.
3. **A norma não exige checagem em tempo real contínuo** — o desenho regulatório do Módulo de Impedidos pressupõe consulta no cadastro, no primeiro login diário e no mínimo a cada 15 dias. A preocupação da reunião ("só login pode não bastar" dado sessões longas em app) é margem de segurança adicional escolhida pelo time, não gap de compliance.
4. **Zona cinzenta**: origens Serasa/KYC e regras internas da casa não têm norma externa equivalente à do SIGAP — aplicar o mesmo enforcement a essas origens é decisão de risco do produto, não mandato legal confirmado. Registrado como nota no card, não bloqueou a criação.
5. **Baixa confiança em alguns números de artigo** (Portaria 1.231/2024, ex. regra de "recriação de cadastro" pós-exclusão) — vieram de fonte secundária única, sem confirmação em texto primário do DOU. Não viraram critério de aceite fechado; registrados como pendência de validação com Jurídico/Compliance.
6. **Trabalho ativo e concorrente encontrado pelo `agente-spec`**: subtask `868kx9wwa` (filha de `868kx9w0e`), em desenvolvimento agora por Ícaro Lopes e Alex, aplicando update via coluna `deleted` — exatamente o padrão de soft delete que a reunião decidiu abandonar. Ithalo instruiu explicitamente **ignorar essa demanda** ("será fechada posteriormente") — não foi absorvida, coordenada nem referenciada nos novos épicos.
7. **Domínio historicamente vive em Backoffice & Integrações**: `agente-spec` encontrou 7+ itens finalizados de impedido/SIGAP nesse folder, só 2 do lado Plataforma. Mas dois pedaços do escopo (enforcement no PAM/Backend por endpoint, frontend respeitando as flags) são domínio técnico de Plataforma (dona do "PAM — front do usuário final", conforme `knowledge/domains/processo.md`).
8. **Nenhum Objetivo/Iniciativa com match direto** — candidato mais próximo é o Objetivo `868kcdz64` ("Escalar a operação multimarcas com autonomia e conformidade"), citado como texto sem vínculo formal.

## Opções Consideradas

**Estrutura do(s) épico(s):**

1. **Um único Épico cobrindo tudo (Backoffice + PAM/Backend + frontend)** — Prós: uma fonte única de verdade. Contras: squad Plataforma não teria visibilidade de roadmap/sprint própria para o trabalho de enforcement, que é tecnicamente dela.
2. **Um Épico só em Backoffice & Integrações, com a fatia de Plataforma registrada como "Aberto para refinamento técnico" a decidir depois** — Prós: não força decisão antes de dimensionar o esforço. Contras: adia uma decisão estrutural que já tinha evidência suficiente (squads diferentes, domínios técnicos diferentes) para ser tomada agora.
3. **Dois Épicos irmãos desde já, um por squad, linkados entre si** — escolhida. Prós: cada squad tem visibilidade própria de roadmap/sprint (mesmo padrão do precedente de geolocalização, que teve dois épicos irmãos por frente de execução); a divisão de domínio já era clara (Backoffice = origem/status/flags/soft delete; Plataforma = consumo das flags no PAM/Backend + frontend). Contras: assume que o esforço de Plataforma é grande o suficiente para merecer item próprio, sem esperar o refinamento técnico confirmar o tamanho.

## Decisão

Aprovada a Opção 3. Dois Épicos criados e linkados:

- **[868kxge57](https://app.clickup.com/t/868kxge57)** — Backoffice & Integrações (Delivery: Operação e afiliados): origem do impedimento → status → cálculo/atualização das flags individuais (incluindo nova flag "pode utilizar bônus") → remoção do soft delete do fluxo de impedimento.
- **[868kxgrc7](https://app.clickup.com/t/868kxgrc7)** — Plataforma (squad Experiência do Jogador): enforcement das flags no PAM/Backend por endpoint (depósito, aposta, bônus) + frontend respeitando as flags sem reimplementar a regra de origem.

Ambos: item único cobrindo Tradicional + Bravo (sem desmembrar por casa, PAM compartilhado); prioridade `urgent` (risco regulatório ativo); sem assignee (dono pendente de confirmação); KPI/Módulo do PAM = `Compliance`.

## Trade-offs Aceitos

- **Dono de execução pendente nos dois épicos** — nenhum assignee foi atribuído (regra: nunca automático, ver [[feedback-assignee-nunca-automatico]]).
- **Campos `Empresa` e `_Projeto` vazios no épico de Plataforma** — são campos de seleção única e o item é genuinamente multimarca; seguiu precedente real do próprio folder (`868kh28pd`), mas Ithalo ainda não confirmou se essa é a convenção definitiva para itens multimarca daqui pra frente.
- **Dependência parcial entre os épicos não é bloqueio total**: o enforcement de depósito/saque/login/aposta em Plataforma pode começar em paralelo ao épico de Backoffice (as flags já existem hoje); só a fatia de bônus depende da nova flag "pode utilizar bônus" nascer no épico de Backoffice primeiro.
- **Trabalho ativo em `868kx9wwa`/`868kx9w0e` deliberadamente ignorado** — decisão explícita de Ithalo, risco de retrabalho ou inconsistência transitória aceito conscientemente ("será fechada posteriormente").
- **Pontos regulatórios de baixa confiança não viraram critério de aceite** — ficam como pendência de validação com Jurídico/Compliance no DOU, não bloquearam a criação dos épicos.
- **Subtasks não criadas nesta rodada** — nascem depois do refinamento técnico conjunto entre as duas squads.

## O que mudaria a decisão

- Se o refinamento técnico entre Backoffice & Integrações e Plataforma concluir que o esforço de enforcement em Plataforma é pequeno, os dois épicos poderiam ser fundidos de volta ou um deles rebaixado a subtask do outro — decisão de squad, não do Orquestrador.
- Confirmação formal do Jurídico/Compliance sobre os pontos de baixa confiança (números de artigo da Portaria 1.231/2024, regra de "recriação de cadastro" pós-exclusão) pode adicionar ou remover critérios de aceite.
- Se Jurídico confirmar que Serasa/KYC/regras internas realmente não têm mandato externo equivalente ao SIGAP, pode haver uma diferenciação de enforcement por origem que hoje está tratada de forma unificada.

## Impacto

- **Produto**: módulo Compliance; jornadas de login, depósito, saque, aposta e uso de bônus, Tradicional e Bravo; Backoffice (nova flag "pode utilizar bônus"); integração com Smartico (bloqueio de benefícios a impedidos).
- **Técnico**: reformulação da lógica de impedimento no PAM (status → flags → enforcement no backend, fim do soft delete para esse fluxo); dupla camada de permissão (flag global da casa + individual) respeitada nos dois épicos; preservação de CPF como chave estável de histórico interno mesmo com soft delete restrito a exclusão voluntária.
- **Processo**: reforça o padrão de rodar `vigilancia-regulatoria` antes de fechar spec com pendência regulatória e de auditar duplicidade/trabalho ativo antes de criar itens novos; registra um novo precedente de split deliberado em épicos irmãos por squad quando o domínio técnico diverge, mesmo sem dimensionamento prévio do esforço.

## Links

- Épico Backoffice & Integrações: [868kxge57](https://app.clickup.com/t/868kxge57)
- Épico Plataforma: [868kxgrc7](https://app.clickup.com/t/868kxgrc7)
- Objetivo candidato (citado, sem vínculo formal): [868kcdz64](https://app.clickup.com/t/868kcdz64) — "Escalar a operação multimarcas com autonomia e conformidade"
- Trabalho ativo excluído por instrução do PM: `868kx9wwa` / `868kx9w0e`
- Decisão relacionada (padrão de triagem regulatória antes do card): [[2026-08-14-geolocalizacao-portaria-722-legitimuz]]
- Decisão relacionada (escopo de "Aberto para refinamento técnico"): [[2026-08-11-aberto-para-refinamento-tecnico-restricao-de-uso]]
- Decisão relacionada (precedente Empresa dupla): [[2026-07-30-bloqueio-campanhas-smartico-cadastro-login]]
- Fontes primárias regulatórias (confiança cruzada): [IN SPA/MF 31/2025 (LegisWeb)](https://www.legisweb.com.br/legislacao/?id=486084), [Editora Roncarati (Art. 7º)](https://www.editoraroncarati.com.br/v2/Diario-Oficial/Diario-Oficial/INSTRUCAO-NORMATIVA-SPA-MF-N%C2%BA-031-DE-07-11-2025.html), [Módulo de Impedidos — gov.br/Fazenda](https://www.gov.br/fazenda/pt-br/composicao/orgaos/secretaria-de-premios-e-apostas/modulo-de-impedidos)
