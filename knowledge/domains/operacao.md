# Domínio: Operação

Entidades que descrevem o ecossistema operacional — fornecedores, gateways, compliance e parceiros.

---

## Fornecedor

**Definição**: Empresa externa que provê serviço ou tecnologia consumida pela Vertical.

**Atributos**: nome, serviço prestado, tipo de contrato, SLA, contato técnico, status (ativo / em avaliação / descontinuado)

**Fornecedores ativos**:

| Fornecedor | Serviço | Domínio |
|---|---|---|
| **Serasa** | KYC — consulta de documentos e validação de identidade | Compliance |
| **SIGAP** | Sistema regulatório de apostas (Ministério da Fazenda) | Compliance |
| **Smartico** | Gamificação, missões, fidelidade — integração headless via deep links | Produto |
| **Provedoras de jogos** | Conteúdo de jogos (slots, crash, ao vivo) | Jogos |
| **Gateway PIX** | Processamento de depósitos e saques via PIX | Carteira |

**Relações**:
- provê → Integração
- sujeito a → Compliance

---

## Gateway de Pagamento

**Definição**: Fornecedor que processa transações financeiras (depósitos e saques).

**Atributos**: nome, métodos suportados (PIX, cartão, boleto), tempo médio de liquidação, taxa, SLA de disponibilidade

**Relações**:
- é um tipo de → Fornecedor
- conecta → Carteira ↔ Sistema bancário

---

## KYC (Know Your Customer)

**Definição**: Processo de verificação de identidade do usuário exigido por regulação.

**Atributos**: etapas (CPF, documento, selfie, biometria), fornecedor, tempo médio de aprovação, taxa de aprovação, motivos de recusa

**Status de KYC de um usuário**: pendente → em análise → aprovado → reprovado → pendência documental

**Regulação**: obrigatório conforme Lei 14.790/2023 e Portarias SPA/MF.

**Relações**:
- executado por → Fornecedor (Serasa)
- impacta → Feature (Onboarding)
- impacta → Métrica (Taxa de conversão cadastro→depósito)

---

## Compliance e Regulação

**Definição**: Conjunto de requisitos legais e regulatórios que a operação deve cumprir.

**Normas vigentes**:
- **Lei 14.790/2023** — marco regulatório das apostas esportivas de quota fixa no Brasil
- **Portarias SPA/MF** — regulamentação operacional do Ministério da Fazenda
- **GLI Standards** — padrões internacionais de integridade de jogos
- **LGPD** — proteção de dados pessoais dos usuários
- **SIGAP** — sistema federal de gestão e controle de apostas

**Relações**:
- governa → Produto / Feature / Integração
- monitorado por → Agente Vigilância Regulatória

---

## Antifraude

**Definição**: Sistemas e processos para detectar e prevenir fraudes na plataforma.

**Atributos**: tipo (conta / transação / jogo), fornecedor, taxa de falso positivo, cobertura

**Relações**:
- integrado a → PAM / Carteira
- alimentado por → Evento de Sistema

---

## Parceiro / Casa de Apostas

**Definição**: Cliente do PAM que utiliza a plataforma da Vertical para operar sua marca.

**Atributos**: nome da marca, URL, segmento de usuários, configuração específica

**Contexto**: A Vertical é provedora de tecnologia (PAM). As casas de apostas são clientes — elas operam suas marcas sobre a plataforma da Vertical.

**Exemplos**:
- Tradicional (casa principal — produto próprio da Vertical)
- Bravo (segunda marca)
