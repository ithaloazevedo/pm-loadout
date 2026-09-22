# Tarefa de reset cíclico do usuário de teste inclui Produção no escopo, apesar de recomendação técnica contrária

**Data**: 2026-08-12
**Tomada por**: Ithalo Mendes
**Status**: APROVADA

---

## Contexto

Um artefato de avaliação técnica de viabilidade propôs um mecanismo para excluir/recriar ciclicamente um usuário de teste "geral", para validar repetidamente o fluxo de 12 etapas de cadastro (CPF, senha, termos, telefone/e-mail, PIX, KYC/verificação facial) tanto em Alpha quanto em Produção.

O próprio artefato concluiu: viável em Alpha (Plan A — whitelist de CPFs, endpoint protegido, flags `isEnableCadastroNoKyc`/`isEnablePhone`); **não recomendado** em Produção, por: exclusão de conta ser soft-delete irreversível (Portaria SPA/MF 1.231/2024, artigo específico ainda não confirmado por nós), verificação facial obrigatória para exclusão (incompatível com ciclos automatizados), ausência de CPFs sintéticos (usaria dado de pessoa real), custo por ciclo de SMS/KYC, contaminação de trilha de auditoria regulatória, e 2 de 7 elementos de estado do usuário vivendo em sistemas fora do controle da empresa (Legitimuz/Serasa, Smartico CRM).

O Orquestrador recomendou escopar a tarefa como Alpha-only e tratar Produção como decisão separada, com compliance. O PM optou por manter Produção no escopo da mesma tarefa mesmo assim.

## Opções Consideradas

1. **Escopo Alpha-only** — segue a recomendação técnica, sem risco regulatório imediato; produção fica como decisão futura separada.
   - Prós: nenhum risco de compliance/segurança assumido agora.
   - Contras: não resolve a necessidade real do time de validar o fluxo também em produção.

2. **Escopo Alpha + Produção na mesma tarefa** — inclui produção, mas com bloqueadores explícitos de execução (sign-off de Compliance obrigatório antes de qualquer dev na parte de produção).
   - Prós: mantém a necessidade de produção visível e priorizada, em vez de perdê-la como decisão futura que pode nunca ser retomada.
   - Contras: card nasce com uma parte que não pode ser desenvolvida sem aprovação externa — risco de ambiguidade se o bloqueador não for respeitado no dia a dia da squad.

## Decisão

Optou-se pela **Opção 2**, por pedido explícito do PM. A parte de Produção foi mantida no card `868kq8zem` ("Mecanismo de reset cíclico do usuário de teste geral para validar o fluxo de cadastro (Alpha e Produção)", folder Delivery: Plataforma, assignee Gabriel Moreschi), mas os três pontos de risco (sign-off de Compliance, confirmação do artigo exato da Portaria 1.231/2024, desenho técnico alternativo a ciclos de exclusão real) foram registrados como **critérios de aceite bloqueantes** na área "Ambiente Produção" — não como nota de rodapé, e não como resolvidos.

## Trade-offs Aceitos

- A squad pode começar a parte de Alpha imediatamente; a parte de Produção fica tecnicamente pronta para refinamento, mas não pode entrar em desenvolvimento sem aprovação explícita de Compliance/Jurídico.
- Corre-se o risco de o bloqueador ser ignorado no dia a dia se ninguém acionar Compliance proativamente — não há trigger automático além do critério de aceite escrito no card.

## O que mudaria a decisão

- Compliance/Jurídico confirmar que a leitura de "exclusão de conta é irreversível sob a Portaria 1.231/2024" está correta e que não há caminho técnico viável para produção — nesse caso a parte de produção do card deveria ser cancelada ou redesenhada por completo, não apenas ajustada.
- Se, ao contrário, Compliance aprovar um desenho alternativo (ex.: contas de teste permanentes pré-provisionadas, fora de relatórios/auditoria), o card deveria ser atualizado para refletir esse desenho em vez do ciclo de exclusão/recriação original.

## Impacto

- **Produto**: módulo Cadastro e acesso, fluxo de onboarding/KYC — squad Plataforma.
- **Técnico**: qualquer trabalho de Produção depende de definição de compliance antes de tocar exclusão de conta, verificação facial ou sistemas externos (Legitimuz/Serasa, Smartico).
- **Processo**: primeiro caso registrado nesta sessão em que o PM optou conscientemente por manter um subescopo de alto risco regulatório dentro de uma tarefa de prioridade baixa, em vez de segregá-lo — vale observar se esse padrão se repete e se o bloqueador realmente impede execução prematura na prática.

## Links

- Card no ClickUp: [868kq8zem](https://app.clickup.com/t/868kq8zem) — Mecanismo de reset cíclico do usuário de teste geral para validar o fluxo de cadastro (Alpha e Produção)
