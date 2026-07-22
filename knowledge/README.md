# Knowledge Graph — PM Agentic Platform

O Knowledge Graph é a fonte única de verdade sobre o domínio de produto. Agentes consultam os arquivos relevantes antes de responder para garantir que o contexto organizacional está presente.

## Estrutura

```
knowledge/
├── domains/          # Entidades por domínio
│   ├── produto.md    # Feature, Módulo, Fluxo, Tela, Evento, API
│   ├── negocio.md    # Objetivo, OKR, Métrica, KPI, Hipótese, Experimento
│   ├── processo.md   # Esteiras de Discovery e Delivery, tipos de item
│   ├── engenharia.md # Sistema, Integração, DB, Fila, Webhook
│   ├── operacao.md   # Fornecedor, Gateway, KYC, PIX, Compliance
│   └── pessoas.md    # Stakeholders, Squads, Times, Responsáveis
├── relations.md      # Relações entre entidades entre domínios
└── decisions/
    ├── TEMPLATE.md   # Template para registrar decisões
    └── INDEX.md      # Índice de decisões registradas
```

## Como Usar

### Para agentes
Antes de responder a uma missão, identifique quais domínios são relevantes e leia os arquivos correspondentes. Exemplo:
- Missão de spec de feature → leia `domains/produto.md` e `domains/processo.md`
- Missão de priorização → leia `domains/negocio.md`
- Missão com risco de integração → leia `domains/engenharia.md` e `domains/operacao.md`

### Para registrar decisões
Use `decisions/TEMPLATE.md`. Após preencher, adicione uma linha no `decisions/INDEX.md`.

### Para atualizar entidades
Quando uma decisão estrutural introduz uma nova entidade (novo sistema, novo fornecedor, nova métrica), atualize o arquivo de domínio correspondente.

## Camadas do Grafo

| Camada | Arquivos | Tipo de informação |
|---|---|---|
| **Estrutural** | produto, engenharia | Entidades estáveis — mudam raramente |
| **Operacional** | processo, operacao, pessoas | Entidades semi-estáveis — mudam a cada ciclo |
| **Dinâmica** | negocio, decisions | Entidades vivas — mudam a cada sprint/quarter |
