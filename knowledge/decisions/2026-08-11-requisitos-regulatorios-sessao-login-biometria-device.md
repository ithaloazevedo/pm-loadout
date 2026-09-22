# Requisitos de expiração de sessão travados na spec de login com biometria/senha do device, antes de confirmação jurídica completa

**Data**: 2026-08-11
**Tomada por**: Ithalo Mendes (via Orquestrador + agente vigilancia-regulatoria)
**Status**: APROVADA

---

## Contexto

O Discovery "[PAM] Melhorias jornada de login" (squad Plataforma) foi promovido a Delivery em 868khhfn0 (nome atual do card: "Autenticação persistente para o app (login com biometria/senha do celular)"). O mecanismo definido pelo Product Designer (Linecker Gomes): a partir do 2º login, se o aparelho tiver senha/biometria do SO configurada, o usuário pode optar por "usar senha do celular" — a partir daí, todo login passa a ser autenticado exclusivamente pelo biometria/PIN nativo do device, sem verificação pelo backend do operador, e sem expiração de sessão definida.

O card de Discovery original já continha, como critério de saída não cumprido, "Direção validada com Tech Lead / Compliance" e a pergunta "há restrição regulatória sobre duração máxima de sessão para conta de apostas?" — nenhuma das duas havia sido respondida quando o discovery foi dado como finalizado.

Antes de deixar a spec seguir para sprint, o Orquestrador acionou o agente `vigilancia-regulatoria` para checar essa lacuna.

## Achado

A Portaria SPA/MF nº 722/2024 (base legal: Lei 14.790/2023) tem dois artigos numéricos diretamente aplicáveis:

- **Art. 14**: exige novo processo de autenticação após 30 minutos de inatividade em um dispositivo.
- **Art. 16**: exige autenticação multifatorial verificada pelo sistema de apostas ao menos 1x a cada 7 dias, ou no primeiro acesso após inatividade superior a 7 dias.

O mecanismo como especificado (sessão sem expiração, autenticação 100% local via SO, sem sinal ao backend) colide com os dois. Biometria como fator de login é permitida pela norma (Art. 11, 15) — o problema não é usar biometria, é a ausência de expiração de sessão e a dúvida sobre se um sinal puramente local do SO conta como "autenticação multifatorial verificada pelo sistema de apostas" na acepção da norma.

**Ressalva de confiabilidade**: os números dos artigos foram triangulados em duas bases jurídicas secundárias (LegisWeb, BNLData) que replicam o texto da portaria. O fetch direto ao DOU (in.gov.br) falhou tecnicamente nesta consulta — alta confiança, mas não é confirmação primária.

## Opções Consideradas

1. **Esperar confirmação jurídica completa (texto primário no DOU + parecer formal de compliance) antes de tocar a spec** — mais seguro, mas trava o card indefinidamente sem prazo claro de resposta do jurídico.
2. **Travar os dois números (30 min de inatividade, MFA a cada 7 dias) como critério de aceite obrigatório agora, com a confirmação jurídica primária como pendência explícita de "Aberto para refinamento" antes de entrar em sprint** — segue adiante com o piso regulatório mais conservador conhecido, sem bloquear o card por completo.

## Decisão

Optou-se pela **Opção 2**. Os dois requisitos (expiração de sessão ≤ 30 min de inatividade; MFA verificada pelo backend ≤ 7 dias) foram adicionados a Critérios de Aceite do card 868khhfn0 como piso mínimo obrigatório, não como parâmetro de produto livre. A dúvida sobre se "usar senha do celular" sem sinal ao backend conta como MFA ficou registrada em Aberto para refinamento, junto com a pendência de confirmar o texto literal dos Arts. 14/16 direto no DOU.

## Trade-offs Aceitos

- Seguimos com uma leitura conservadora da norma sem confirmação jurídica primária formal — se compliance ou o texto oficial divergirem, a spec precisa ser revisada.
- O card não pode entrar em sprint enquanto a seção Aberto para refinamento não for resolvida (regra do próprio template de Delivery) — ou seja, a decisão de negócio ("vamos construir isso") avançou, mas a execução real fica bloqueada até Tech Lead + Compliance decidirem o ponto do sinal ao backend.

## O que mudaria a decisão

- Confirmação do texto literal dos Arts. 14 e 16 direto no DOU divergindo do que foi triangulado nas fontes secundárias.
- Parecer de compliance definindo um piso diferente (mais ou menos conservador) para expiração de sessão ou MFA.
- Decisão de Tech Lead/Compliance sobre se o mecanismo precisa de um sinal verificável pelo backend para contar como MFA.

## Impacto

- **Produto**: módulo Cadastro e acesso — jornada de login do app mobile (squad Plataforma).
- **Técnico**: mecanismo de persistência de sessão precisa implementar expiração ativa (30 min de inatividade) e ciclo de reautenticação forçada (7 dias), não apenas delegar ao SO.
- **Processo**: card não pode entrar em sprint até compliance confirmar o texto primário e Tech Lead/Compliance resolverem o ponto do sinal ao backend.

## Links

- Card no ClickUp: [868khhfn0](https://app.clickup.com/t/868khhfn0) — Autenticação persistente para o app (login com biometria/senha do celular)
- Comentário de decisão no card: `90110259725394`
- Discovery original: mesmo card, seção Discovery reescrita na promoção a Delivery
