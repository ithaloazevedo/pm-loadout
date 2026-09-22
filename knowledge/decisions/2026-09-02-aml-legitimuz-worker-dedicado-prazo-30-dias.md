# O requisito de aceite do AML é o prazo de 30 dias por transação, não a reativação da Legitimuz — e a política publicada das casas obriga drenagem contínua

**Data**: 2026-09-02
**Tomada por**: Ithalo Mendes (via Orquestrador + agentes vigilancia-regulatoria e agente-delivery)
**Status**: APROVADA

---

## Contexto

O Tech Lead trouxe no chat que a integração de AML com a Legitimuz **foi desativada em produção nas duas casas** (Tradicional e Bravo) e pediu a abertura de uma task. O escopo que ele descreveu era técnico e específico: as transações destinadas ao AML são processadas no mesmo worker e na mesma fila do PIX, a latência e as falhas da API da Legitimuz degradavam os pagamentos, então o AML precisa de worker dedicado em fila separada.

O enquadramento recebido, portanto, era de melhoria de arquitetura. O que o levantamento mostrou é que se trata de um controle regulatório mandatório desligado em produção, com prazo já correndo — e que o épico de origem [868kckzxv](https://app.clickup.com/t/868kckzxv) ("Integrar Legitimuz (AML)", finalizado) tinha exatamente este critério de aceite: *"Falha na API da Legitimuz não interrompe fluxo de depósito (degradação graciosa)"*. O critério não se sustentou em produção — o trabalho é fechá-lo, não construir algo novo.

## Achados

1. **O prazo conta da transação, não do fix.** Portaria SPA/MF nº 1.143/2024, art. 26, § 2º: o procedimento de análise deve encerrar em **30 dias contados da data da aposta ou da operação associada**. As transações da janela de indisponibilidade já estão com o relógio correndo, e as mais antigas vencem primeiro. Logo, drenar o backlog não é limpeza pós-fix opcional: o backlog **é** o prazo.
2. **A norma não exige tempo real nem automação.** O art. 23 impõe implantar o procedimento de monitoramento, seleção e análise — obrigação de estado, não de cadência. Arquitetura assíncrona com fila dedicada satisfaz a conformidade. É essa folga normativa que permite resolver a degradação do PIX sem abrir mão do controle: separa-se o recurso, não a cadência.
3. **A política publicada das próprias casas é mais rigorosa que a norma.** As políticas de PLD/FT de Tradicional e Bravo (versão agosto/2026, texto idêntico nas duas) comprometem: *"Manter um sistema interno de monitoramento contínuo de transações financeiras"* e *"monitorará de forma contínua todas as transações realizadas pelos clientes"*. O art. 6º da Portaria 1.143/2024 exige mecanismos de checagem do efetivo atendimento da própria política — o compromisso publicado passa a ser o padrão exigível. **Consequência prática: processamento em lote noturno deixa de ser opção livre de desenho, ainda que a norma o admitisse.**
4. **A análise precisa ficar documentada mesmo quando não gera comunicação.** Art. 26, § 1º: análise e conclusão documentadas e disponíveis para demonstração à SPA, independentemente de resultarem em comunicação ao Coaf. Um período sem registro de análise é, ele próprio, a prova documental da lacuna diante do fiscal — a ausência não passa como "nada suspeito ocorreu".
5. **Compliance não foi acionado.** Varredura no canal interno de Compliance e Regulatório não encontrou nenhuma menção à desativação. O time de compliance segue tratando SIGAP, termos e KYC sem essa informação.
6. **Culpa basta.** Lei 9.613/1998, art. 12, § 2º, IV: a multa por deixar de comunicar alcança conduta culposa, sem exigir dolo. Uma indisponibilidade autoinfligida por decisão técnica interna é culpa em sentido próprio, e o registro da decisão de desativar a documenta.
7. **Duração é fator de dosimetria.** Lei 14.790/2023, art. 42, I manda considerar a gravidade **e a duração** da infração — argumento direto contra deixar o item parado na esteira.

## Opções Consideradas

**Escopo do card:**

1. **Escopo literal do pedido** — worker dedicado e fila separada.
   - Prós: entrega exatamente o que a engenharia pediu, menor superfície.
   - Contras: o card pode ser fechado com o AML ainda desativado e o backlog intocado; o risco regulatório continua aberto sem registro.
2. **Isolar e reativar, sem tratar a janela.**
   - Prós: fecha o controle daqui para frente.
   - Contras: as transações do período sem análise ficam sem dono, e são justamente as que vencem primeiro.
3. **Isolar, reativar e tratar a janela, com o aceite formulado pelo prazo.**
   - Prós: fecha o problema, não o sintoma; preserva a liberdade de arquitetura que resolve o PIX.
   - Contras: card maior, exige dado de produção (data da desativação) que ainda não estava disponível.

**Formulação do critério de aceite:**

1. "Reativar a integração com a Legitimuz" — amarra o aceite ao fornecedor e ao desenho antigo, que é o que quebrou.
2. "Toda transação com análise concluída e documentada em até 30 dias da sua data" — amarra ao requisito regulatório real e deixa a arquitetura livre.

## Decisão

1. **Opção 3 de escopo**, com o **critério de aceite formulado pelo prazo (opção 2)**: o card entrega worker e fila dedicados, reativação em produção nas duas casas, drenagem do backlog e isolamento de falha — e o aceite mede *"nenhuma transação sem análise concluída por mais de 30 dias contados da data da própria transação"*, não *"integração religada"*.
2. **Drenagem contínua, não em lote** — decorrência do achado 3. O item de refinamento técnico trata apenas de throughput suportado e comportamento sob backpressure, não de se o processamento é contínuo.
3. **Item único cobrindo Tradicional e Bravo**, seguindo o precedente já registrado em [2026-08-14-geolocalizacao-portaria-722-legitimuz](2026-08-14-geolocalizacao-portaria-722-legitimuz.md) — a implementação é uma no PAM compartilhado.
4. **Tipo Tarefa, não Épico nem Bug.** O épico guarda-chuva já existe e está finalizado; o sintoma em produção (PIX degradado) já foi mitigado pela desativação, então o que resta é trabalho estrutural. `_Classe` = **Solicitação de Mudança** (escolha do PM; o Orquestrador havia recomendado *Incidente* para manter o caso visível nos relatórios de incidente).
5. **Nasce em Execução**, folder Delivery: Operação e afiliados — entra na sprint corrente, coerente com um controle de compliance desligado. Assignee Hugo Fernandes Vieira, confirmado pelo PM.
6. **As obrigações acessórias ficam fora do card**, como frente de compliance explícita: relatório de incidente à SPA (Portaria 722/2024, Anexo IV), triagem da comunicação anual de não ocorrência e revisão da política publicada.

## Trade-offs Aceitos

- **O card nasceu sem o dado que dimensiona o próprio risco.** A data exata da desativação por casa e o volume de transações não analisadas ficaram como primeiro item de refinamento técnico. É dado de produção, não decisão — mas até chegar, não se sabe se algum lote já venceu os 30 dias, isto é, se o caso é "corrigir" ou "corrigir, remediar e reportar".
- **Instrumentação entrou no escopo além do pedido.** Alarme de fila acumulada e observabilidade da idade da transação mais antiga não foram pedidos, mas sem eles o teto de 30 dias não é verificável e uma próxima interrupção volta a passar silenciosa.
- **Campo `Empresa` ficou vazio** — não existe na lista Execução de Operação e afiliados (verificado nos quatro escopos). A cobertura das duas casas está registrada só na narrativa do card. Mesmo trade-off já aceito em precedentes anteriores.
- **A frente de compliance foi identificada mas não iniciada** nesta missão — depende de o PM levar ao time de compliance.
- **Numeração de artigos não conferida em versão certificada.** Há notícia de retificação da Portaria 1.143/2024 não localizada em fonte oficial; o texto do DOU apresenta anomalia no art. 16 compatível com erro de publicação. As citações servem ao card interno, mas não devem ir para peça jurídica externa sem conferência de compliance.

## O que mudaria a decisão

- **Data da desativação além de 30 dias**: o caso deixa de ser prevenção e passa a descumprimento consumado sobre um lote, exigindo remediação documentada e provável reporte — muda a prioridade e traz compliance para dentro da frente.
- **Revisão da política publicada de PLD/FT** removendo o compromisso de monitoramento contínuo: reabriria o lote noturno como opção de desenho.
- **Se o mesmo desligamento derrubou outros controles** (triagem de PEP, listas do CSNU/Lei 13.810, CPF check): o escopo está subdimensionado e o card precisa ser desmembrado.
- **Se a Legitimuz não suportar o throughput** do consumo contínuo: pode ser necessário reavaliar fornecedor ou negociar limite, o que sai do escopo de engenharia.

## Impacto

- **Produto**: módulo AML — Prevenção a fraudes; fluxos de depósito, saque e aposta, Tradicional e Bravo.
- **Técnico**: separação de worker e fila do processamento AML em relação ao PIX; reativação da integração Legitimuz (API server-side, distinta do SDK client-side de geolocalização do épico 868kr6b33); política de timeout, retry e dead-letter; observabilidade de fila.
- **Processo**: reforça dois padrões. (1) Rodar `vigilancia-regulatoria` antes de fechar spec com exposição regulatória — aqui, o levantamento **mudou o critério de aceite**, não só acrescentou contexto. (2) Checar a **política interna publicada**, não só a norma: quando a empresa promete mais do que a lei exige, o compromisso publicado é o padrão exigível, e isso restringe decisões de arquitetura.

## Links

- Card criado: [868m0b3ph](https://app.clickup.com/t/868m0b3ph) — "Isolar o processamento de AML em worker e fila dedicados e reativar a integração Legitimuz nas duas casas"
- Épico de origem: [868kckzxv](https://app.clickup.com/t/868kckzxv) — "Integrar Legitimuz (AML)", finalizado, com o critério de degradação graciosa que não se sustentou
- Objetivo vinculado: [868kcdz64](https://app.clickup.com/t/868kcdz64) — "Escalar a operação multimarcas com autonomia e conformidade"
- Decisão relacionada (precedente de item único para as duas casas e mesma integração): [2026-08-14-geolocalizacao-portaria-722-legitimuz](2026-08-14-geolocalizacao-portaria-722-legitimuz.md)
- Decisão relacionada (outro uso da mesma integração): [2026-08-18-correcao-campo-sexo-cpf-check-legitimuz-nao-e-genero-autodeclarado](2026-08-18-correcao-campo-sexo-cpf-check-legitimuz-nao-e-genero-autodeclarado.md)
- Fontes primárias: [Portaria SPA/MF nº 1.143/2024 (DOU)](https://www.in.gov.br/en/web/dou/-/portaria-spa/mf-n-1.143-de-11-de-julho-de-2024-571718850), [Portaria SPA/MF nº 722/2024 (DOU)](https://www.in.gov.br/en/web/dou/-/portaria-spa/mf-n-722-de-2-de--maio-de-2024-557715851), [Lei nº 14.790/2023](https://www.planalto.gov.br/ccivil_03/_ato2023-2026/2023/lei/l14790.htm), [Lei nº 9.613/1998](https://www.planalto.gov.br/ccivil_03/leis/l9613.htm)
