# Relações do Knowledge Graph

Mapa das relações entre entidades dos diferentes domínios. Use para navegar o grafo e entender dependências.

**Fonte estruturada**: `knowledge/relations.yaml` — triples com `from`, `relation`, `to`, `domain`, `valid_from`. Use o YAML para queries e verificações de consistência. Use este arquivo para navegação narrativa.

**Ao alterar uma relação**: atualizar `relations.yaml` e registrar a decisão em `knowledge/decisions/` se a mudança for relevante.

---

## Relações Principais

### Feature → Integração → Compliance

```
Feature (Onboarding/Cadastro)
  ↓ depende de
KYC (processo)
  ↓ executado por
Serasa (fornecedor)
  ↓ gera
Status de aprovação
  ↓ impacta
Métrica: Conversão cadastro→depósito
```

### Feature → Evento → Métrica

```
Feature (Primeiro Depósito)
  ↓ gera
Evento: deposito_concluido
  ↓ alimenta
Métrica: Taxa de 1º depósito
  ↓ pertence a
KR: Conversão cadastro→1º depósito ≥ X%
  ↓ mede progresso em
Objetivo: Crescimento da base ativa
```

### Épico → Squad → Delivery

```
Decisão de produto (Discovery concluído)
  ↓ resulta em
Épico (Módulo: Carteira)
  ↓ entra no Backlog do folder
Squad: Experiência do jogador
  ↓ executa em
Sprint de Delivery
  ↓ gera
Correção (pós-homologação, se necessário)
```

### Regulação → Feature → Compliance

```
Lei 14.790/2023 + Portarias SPA/MF
  ↓ exige
KYC obrigatório antes de 1º depósito
  ↓ implementado em
Feature: Verificação de identidade
  ↓ monitorado por
Agente de Vigilância Regulatória
  ↓ reporta
Agente de Governança
```

### Smartico → Feature → Engajamento

```
Smartico (fornecedor, headless)
  ↓ integrado via
Deep links + API de missões
  ↓ alimenta
Feature: Sistema de missões e recompensas
  ↓ impacta
Métrica: Retenção 7/30 dias
```

---

## Tabela de Relações por Entidade

| De | Relação | Para | Domínio |
|---|---|---|---|
| Feature | pertence a | Módulo | produto |
| Feature | gera | Evento | produto |
| Feature | consome | API | produto + engenharia |
| Feature | depende de | Integração | produto + engenharia |
| Feature | impacta | Métrica | produto + negócio |
| Módulo | pertence a | Produto | produto |
| Evento | alimenta | Métrica | produto + negócio |
| Métrica | mede | KR | negócio |
| KR | pertence a | Objetivo | negócio |
| Integração | provida por | Fornecedor | engenharia + operação |
| Integração | consumida por | Sistema | engenharia |
| KYC | executado por | Serasa | operação |
| KYC | impacta | Feature (Onboarding) | operação + produto |
| Épico/Tarefa | pertence a | Squad | processo + pessoas |
| Correção | subtarefa de | Épico / Tarefa | processo |
| Bug | afeta | Feature em produção | processo + produto |
| Regulação | governa | Feature / Integração | operação |
| Stakeholder | influencia | Objetivo | pessoas + negócio |
| Squad | responsável por | Módulo | pessoas + produto |

---

## Perguntas Navegáveis no Grafo

- "Quais features dependem do KYC?" → Feature ← depende de ← KYC
- "Que eventos preciso instrumentar para medir conversão?" → Métrica → alimentada por → Evento → gerado por → Feature
- "Qual squad cuida do módulo de Jogos?" → Squad: Provedora de conteúdo
- "Que fornecedores têm risco regulatório?" → Serasa, SIGAP (compliance), Gateway PIX (AML)
- "O que gera uma Correção?" → homologação com bug / inconformidade com protótipo / critério de aceite não cumprido
