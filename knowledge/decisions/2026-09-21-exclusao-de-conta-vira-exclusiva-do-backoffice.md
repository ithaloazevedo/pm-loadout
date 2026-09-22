# Exclusão de conta deixa de ser autoatendimento no app e passa a existir apenas no Backoffice, para qualquer conta e com estorno de saldo opcional

**Data**: 2026-09-21
**Tomada por**: Ithalo Mendes (via Orquestrador + agentes vigilancia-regulatoria, agente-delivery)
**Status**: APROVADA

---

## Contexto

Ithalo pediu a abertura de uma tarefa para dar ao operador do Backoffice a capacidade de excluir a conta de um usuário, com modal de dupla confirmação, e sinalizou que já havia existido uma versão disso "para o front, que foi cancelada, com o Melk".

A apuração no ClickUp e no log de decisões corrigiu e completou essa lembrança:

- O épico do front existe e é o [868kxmhp7](https://app.clickup.com/t/868kxmhp7) — "[PAM] Jornada de exclusão de conta", assinado por Linecker Gomes e Melk Zedeque. Ele **não está cancelado: está `finalizado`**, fechado em 03/09/2026 na lista Execução do PAM. Os dois últimos comentários do Melk explicam o que de fato ocorreu — "Foi desconsiderado, vai ser feito pelo backoffice para melhorar testes" (02/09) e "foi despriorizado e vamos fazer só no backoffice" (03/09). A lembrança do PM estava correta quanto ao abandono; o board é que registra o desfecho errado.
- O mecanismo técnico **já existe e já estava reservado para esse uso**. O épico [868kxge57](https://app.clickup.com/t/868kxge57), finalizado, estabeleceu textualmente que "soft delete passa a ser exclusivo de exclusão voluntária de conta", e as tarefas [868kxmpk3](https://app.clickup.com/t/868kxmpk3) e [868kxx9fk](https://app.clickup.com/t/868kxx9fk) executaram a separação, tirando o softdelete do fluxo de impedimento. Ou seja: o softdelete ficou sem gatilho quando o front caiu.
- Existe precedente direto de ferramenta interna equivalente: [868m398z8](https://app.clickup.com/t/868m398z8) — "Habilitar redução manual de saldo em contas teste no Backoffice (Bravo e Tradicional)", finalizado em 17/09/2026, card único cobrindo as duas casas, com as casas no título e log de auditoria entre os critérios de aceite.

A motivação declarada pelo PM é destravar **testes internos** (excluir e recadastrar para revalidar fluxos), não atender ao direito de eliminação da LGPD — o que inverte o enquadramento do épico original do front, que nasceu como jornada de autoatendimento LGPD.

## Opções Consideradas

**Alcance da funcionalidade:**
1. **Restringir a contas de teste** — recomendação do Orquestrador, por seguir o precedente do card de redução de saldo (que tem tela própria de conta teste e excluiu contas reais do escopo) e entregar a necessidade sem abrir superfície de risco sobre jogador real.
2. **Qualquer conta, incluindo jogador real** — escolhida. Cobre também a exclusão a pedido do titular, que perdeu o caminho quando o front foi despriorizado.
3. Começar por conta de teste e tratar jogador real como card separado.

**Tratamento do saldo remanescente:**
1. **Alertar e exigir zeragem pela redução manual já entregue em 17/09** — recomendação do Orquestrador, por custo quase zero e reaproveitamento de capacidade recém-construída.
2. **Estornar para a última conta bancária cadastrada** — escolhida.
3. Ignorar o saldo e excluir direto.

## Decisão

1. **Exclusão de conta passa a existir apenas a nível backoffice.** A jornada de autoatendimento no app não será retomada; consta em 🚫 Fora do card novo.
2. **Alcance amplo** (Opção 2): vale para qualquer conta, incluindo jogador real — não se restringe a contas de teste, apesar de a motivação principal ser teste interno.
3. **Saldo remanescente** (Opção 2): a interface alerta o valor e oferece ao operador estornar para a última conta bancária cadastrada do jogador, antes da exclusão.
4. **Reversão/reativação de conta excluída fica fora de escopo**, sem item previsto.
5. **Ação restrita a perfil de operador**; qual perfil exatamente será definido com a operação, tratado como configuração de permissão e não como pendência de spec.
6. **Log de auditoria entra como critério de aceite** (quem executou, quando, o que mudou).
7. Card único cobrindo Tradicional e Bravo, sem desmembrar por casa — mesmo padrão de [[2026-08-27-enforcement-usuarios-impedidos-status-flags-dois-epicos]] (PAM compartilhado) e do gêmeo `868m398z8`.

Card criado: [868m7nu02](https://app.clickup.com/t/868m7nu02) — "Habilitar exclusão de conta de usuário pelo Backoffice, com dupla confirmação (Tradicional e Bravo)", tipo Tarefa, Backlog `901114029784` (folder Sprints PAM), sem assignee, sem prioridade definida.

## Achados regulatórios incorporados

O PM instruiu explicitamente **não aprofundar o refino regulatório** ("esse ponto é mais para testes internos do que para usuários"). A apuração já em curso trouxe três pontos que foram absorvidos sem abrir discussão:

- **Log de quem executou é exigência setorial vinculante, não zelo de produto.** Portaria SPA/MF nº 722/2024, Anexo I item 40 "m" III, lista "desativação da conta" entre os eventos que o sistema de apostas deve armazenar; Anexo IV item 10 "f" exige "identificação do usuário que realizou a alteração". Virou critério de aceite.
- **O estorno para a última conta cadastrada tem respaldo normativo direto.** Portaria SPA/MF nº 1.231/2024, art. 37, ao tratar de encerramento de conta inativa, determina "transferir o saldo remanescente para a conta cadastrada do apostador" — o desenho escolhido pelo PM espelha a regra, e não a contraria.
- **Autoatendimento não é exigência legal.** Não existe norma, na LGPD ou em regulamento da ANPD, que obrigue self-service para o direito de eliminação: o art. 18 §3º pressupõe requerimento dirigido a agente de tratamento, e a Res. CD/ANPD nº 2/2022 art. 7º deixa o canal livre. A ANPD também **não** fixou prazo numérico para atender pedido de eliminação (art. 18 §5º remete a regulamento inexistente; o tema segue na Fase 1 da agenda regulatória). Logo, mover a exclusão para o backoffice **não** cria descumprimento.

## Trade-offs Aceitos

- **Alcance amplo sem os controles que o alcance amplo pediria.** Ao cobrir jogador real e não só conta de teste, a ferramenta passa a poder encerrar conta de pessoa real sem que o card preveja reversão. Erro de alvo do operador é irreversível dentro do escopo entregue — a dupla confirmação é a única barreira.
- **Encerramento por iniciativa da casa não está coberto.** Se a ferramenta for usada para encerrar conta por decisão da operação (não a pedido do titular), a Portaria SPA/MF nº 1.231/2024 art. 52 exige processo de apuração com contraditório e prazo de resposta não inferior a 7 dias, e o art. 56 exige registro apartado e redundante com a decisão e sua fundamentação. O card não cobre esse fluxo; o risco é de uso da ferramenta fora do previsto, não do que está especificado.
- **Estorno custa mais que a alternativa disponível.** A função de redução manual de saldo em conta teste foi entregue 4 dias antes (17/09) e resolveria o caso de teste a custo quase zero. Optou-se pelo estorno, que exige decidir entre reusar o fluxo de saque ou criar transação administrativa própria — pendência técnica registrada no card.
- **Registro histórico do épico do front segue incorreto.** `868kxmhp7` permanece como `finalizado` em vez de `despriorizado`, o que faz o board sugerir que a Tradicional entregou autoatendimento de exclusão — leitura sensível, dado que a casa já respondeu ofício de PROCON sobre autoexclusão e temas de conta.

## O que mudaria a decisão

- Um pedido formal de titular (ANPD/PROCON) sobre demora ou dificuldade de exclusão poderia reabrir a discussão de autoatendimento no app.
- Se o refinamento técnico concluir que o estorno exige transação administrativa própria, o item provavelmente deixa de caber como Tarefa e vira Épico com subtask dedicada ao estorno.
- Um incidente de exclusão indevida de jogador real colocaria a reversão de volta no escopo.

## Impacto

- **Produto**: Backoffice do operador (Tradicional e Bravo); jornada de exclusão de conta do PAM.
- **Técnico**: consome o softdelete já existente e reservado; ponto aberto sobre o mecanismo de estorno.
- **Processo**: reforça o padrão de card único para itens que cobrem as duas casas quando o sistema é compartilhado, e o de auditar o histórico real (comentários, não só status) antes de confiar no estado de um card fechado.

## Links

- Card criado: https://app.clickup.com/t/868m7nu02
- Versão anterior no app, despriorizada: https://app.clickup.com/t/868kxmhp7
- Card que reservou o softdelete para exclusão voluntária: https://app.clickup.com/t/868kxge57
- Gêmeo de ferramenta de backoffice nas duas casas: https://app.clickup.com/t/868m398z8
- Decisão anterior sobre o texto da jornada do front: [[2026-08-28-exclusao-conta-texto-permanente-mantido-apesar-retencao-legal]]
- Precedente de card único para as duas casas: [[2026-08-27-enforcement-usuarios-impedidos-status-flags-dois-epicos]]
