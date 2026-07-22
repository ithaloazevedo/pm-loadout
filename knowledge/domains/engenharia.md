# Domínio: Engenharia

Entidades técnicas que descrevem como o sistema é construído e como as partes se comunicam.

---

## Sistema

**Definição**: Componente de software com responsabilidade bem definida, implantado de forma independente.

**Atributos**: nome, responsabilidade, squad dona, tecnologia principal, repositório

**Exemplos**:
- PAM (Player Account Management) — gestão de conta do jogador
- Backoffice — operações internas
- Game Engine / Integrador de provedoras

**Relações**:
- consome → Integração
- expõe → API
- produz → Evento

---

## Integração

**Definição**: Conexão entre o sistema interno e um fornecedor ou serviço externo.

**Atributos**: nome, fornecedor, tipo (API REST / webhook / SDK), autenticação, SLA, ambiente (homolog/prod), status

**Exemplos**:
- Serasa (KYC — consulta de documentos)
- SIGAP (Sistema de Gestão de Apostas — compliance regulatório)
- Smartico (gamificação, missões — headless, via deep links)
- Provedoras de jogos (slots, crash, ao vivo)
- Gateway PIX (depósitos e saques)

**Relações**:
- provida por → Fornecedor (ver `operacao.md`)
- consumida por → Sistema / Feature

---

## Banco de Dados

**Definição**: Sistema de armazenamento persistente de dados.

**Atributos**: tipo (relacional/NoSQL), responsabilidade, sistema dono

**Relações**:
- pertence a → Sistema

---

## Fila / Mensageria

**Definição**: Mecanismo assíncrono de comunicação entre sistemas.

**Atributos**: tecnologia, tópicos/filas principais, produtor, consumidor, SLA de processamento

**Relações**:
- conecta → Sistema ↔ Sistema

---

## Webhook

**Definição**: Notificação HTTP enviada por um fornecedor quando um evento ocorre.

**Atributos**: fornecedor, evento disparador, endpoint receptor, retry policy

**Exemplos**:
- Webhook de KYC aprovado (Serasa → PAM)
- Webhook de pagamento confirmado (Gateway PIX → Carteira)

**Relações**:
- enviado por → Fornecedor / Integração
- recebido por → Sistema

---

## Evento de Sistema

**Definição**: Mensagem interna gerada por um sistema quando algo importante ocorre.

Diferente de Evento de produto (rastreamento analítico): evento de sistema é infraestrutura; evento de produto é analytics.

**Exemplos**:
- `payment.confirmed`
- `kyc.approved`
- `session.started`

**Relações**:
- gerado por → Sistema
- consumido por → Sistema / Fila
