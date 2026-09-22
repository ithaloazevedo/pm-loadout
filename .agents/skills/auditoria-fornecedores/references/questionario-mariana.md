# Questionário — Auditoria de Faturas de Fornecedores

Perguntas para destravar o refinamento da skill `auditoria-fornecedores`. Não são bloqueantes
para usar a skill hoje — cada pergunta sem resposta vira uma suposição declarada explicitamente
na hora da consulta. Boa parte já foi respondida diretamente pelo PM (ver
`references/aprendizados.md` para o registro vivo); o que sobra aqui é o que só a Mariana sabe
responder na prática.

## Já respondido (pelo PM, 2026-09-10/11 — detalhe completo em `aprendizados.md`)

- **Formato da fatura varia por fornecedor** — a skill aceita a Mariana descrever em linguagem
  natural (fornecedor + item + período + quantidade se houver + valor).
- **Serasa e Legitimuz são os dois fornecedores de KYC/CPF Check usados hoje, simultaneamente**
  — coexistem na mesma tabela (`kyc_pending_actions.data->>'kycProvider'`).
- **Objetivo é validar o VALOR da fatura, não integrar com o financeiro interno (`organizze`)**
  — a skill trabalha só com o que a Mariana informa da fatura + o banco.
- **A quantidade de uso nem sempre vem na fatura** — a skill sempre pergunta explicitamente
  quando não vier, porque é o que permite traduzir a contagem do banco em R$.
- **Cada item da fatura é tratado isoladamente** — Serasa/Legitimuz cobram cada tipo de
  ação (ex.: validação facial vs. revalidação de login) como item separado, nunca somado.

## Ainda em aberto — para a Mariana

1. Existe algum identificador que aparece tanto na fatura quanto no banco (ex.: ID de
   transação do provedor de jogo) que dê pra bater 1 a 1, além de comparar totais?
2. Quando o fornecedor de jogo fatura "transações", conta cada débito de aposta E cada
   crédito de prêmio separadamente, ou uma por rodada? (No banco, uma aposta pode gerar mais
   de uma linha em transações — isso muda o total esperado.)
3. Com que frequência você recebe cada fatura (mensal, quinzenal)? Define a janela padrão.
4. O fornecedor usa algum fuso horário específico no corte do período (UTC vs. horário de
   Brasília)? Pequenas diferenças de corte já geram divergência que não é erro real.
