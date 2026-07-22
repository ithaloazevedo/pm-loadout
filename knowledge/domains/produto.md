# Domínio: Produto

Entidades que descrevem a superfície funcional do produto — o que é entregue ao usuário.

---

## Produto

**Definição**: O produto completo entregue a uma casa de apostas (cliente do PAM) ou ao usuário final.

**Atributos**: nome, empresa (Tradicional / Bravo / Vertical), público-alvo, status (ativo / em desenvolvimento / descontinuado)

**Exemplos**: Loteria Tradicional (casa + app)

**Relações**:
- composto por → Módulo
- medido por → Métrica

---

## Módulo

**Definição**: Agrupamento funcional de features que forma uma área coesa da experiência.

**Atributos**: nome, produto pai, responsável de produto, squad responsável

**Exemplos (Tradicional)**:
- Onboarding (cadastro, KYC, verificação)
- Carteira (depósito, saque, saldo)
- Jogos (catálogo, lobby, sessão)
- Conta (perfil, preferências, documentos)
- Responsible Gaming (limites, autoexclusão)

**Relações**:
- pertence a → Produto
- composto por → Feature

---

## Feature

**Definição**: Capacidade específica entregue a um usuário dentro de um Módulo.

**Atributos**: nome (em linguagem do usuário), módulo pai, status (em discovery / em delivery / live / descontinuada), squad responsável

**Exemplos**:
- Cadastro simplificado (Módulo: Onboarding)
- Consulta de saldo (Módulo: Carteira)
- Autoexclusão temporária (Módulo: Responsible Gaming)

**Relações**:
- pertence a → Módulo
- gera → Evento
- consome → API
- impacta → Métrica
- depende de → Integração

---

## Fluxo

**Definição**: Sequência de telas e ações que o usuário percorre para completar um job.

**Atributos**: nome, feature principal, telas envolvidas, ponto de entrada, ponto de saída, happy path

**Exemplos**:
- Fluxo de cadastro (entrada: tela inicial → saída: conta criada e verificada)
- Fluxo de primeiro depósito (entrada: tela de carteira → saída: saldo creditado)

**Relações**:
- pertence a → Feature
- composto por → Tela
- gera → Evento

---

## Tela

**Definição**: Interface visual específica que o usuário interage.

**Atributos**: nome, fluxo pai, componentes, estado (design / em desenvolvimento / live)

**Relações**:
- pertence a → Fluxo
- gera → Evento

---

## Evento

**Definição**: Ação rastreável do usuário ou do sistema que gera dado analítico.

**Atributos**: nome (snake_case), tipo (frontend / backend), propriedades, sistema de coleta

**Exemplos**:
- `cadastro_iniciado`
- `kyc_aprovado`
- `deposito_concluido`
- `sessao_jogo_encerrada`

**Relações**:
- gerado por → Feature / Tela / Fluxo
- alimenta → Métrica

---

## API / Endpoint

**Definição**: Interface de comunicação entre sistemas.

**Atributos**: path, método (GET/POST/etc.), sistema provedor, autenticação, SLA

**Relações**:
- consumida por → Feature
- provida por → Integração / Microserviço
