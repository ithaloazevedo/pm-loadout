# Knowledge Graph — PM Agentic Platform

Esta base reúne conceitos locais, decisões e histórico de uso do PM Loadout. O contexto durável de domínio é consultado no blow-os; a divisão de fontes está em `docs/fontes-de-contexto.md`. Agentes consultam os arquivos relevantes antes de responder para garantir que o contexto organizacional está presente.

## Estrutura

```
knowledge/
├── domains/          # Entidades por domínio
│   ├── produto.md    # Feature, Módulo, Fluxo, Tela, Evento, API
│   ├── negocio.md    # Métrica, KPI, Hipótese, Experimento
│   ├── processo.md   # Esteiras de Discovery e Delivery, tipos de item
│   ├── engenharia.md # Sistema, Integração, DB, Fila, Webhook
│   ├── operacao.md   # Fornecedor, Gateway, KYC, PIX, Compliance
│   └── pessoas.md    # Stakeholders, Squads, Times, Responsáveis
├── relations.md      # Relações entre entidades entre domínios
├── decisions/
│   ├── TEMPLATE.md   # Template para registrar decisões
│   └── INDEX.md      # Índice de decisões registradas
└── pesquisas/
    └── INDEX.md      # Achados/análises (link), instrumentos de pesquisa (arquivo) e voz do cliente
```

## Como Usar

### Para agentes
Antes de responder a uma missão, identifique quais domínios são relevantes e leia os arquivos correspondentes. Exemplo:
- Missão de spec de feature → leia `domains/produto.md` e `domains/processo.md`
- Missão de priorização → leia `domains/negocio.md`
- Missão com risco de integração → leia `domains/engenharia.md` e `domains/operacao.md`

### Para registrar decisões
Use `decisions/TEMPLATE.md`. Após preencher, adicione uma linha no `decisions/INDEX.md`.

### Para registrar pesquisa e voz do usuário
Use `pesquisas/INDEX.md`. Achado/análise pronta (ex.: artifact do claude.ai) entra como link + achado
principal em uma frase — não copiar o conteúdo. Instrumento de pesquisa sem fonte externa estável (survey,
formulário) entra como arquivo completo na própria pasta. Fonte viva (ex.: canal de voz do cliente) entra
como ponteiro; snapshot sintetizado vira entrada datada.

### Para atualizar entidades
Quando uma decisão estrutural introduz uma nova entidade (novo sistema, novo fornecedor, nova métrica), atualize o arquivo de domínio correspondente.

## Camadas do Grafo

| Camada | Arquivos | Tipo de informação |
|---|---|---|
| **Estrutural** | produto, engenharia | Entidades estáveis — mudam raramente |
| **Operacional** | processo, operacao, pessoas | Entidades semi-estáveis — mudam a cada ciclo |
| **Dinâmica** | negocio, decisions | Entidades vivas — mudam a cada sprint/quarter |

## Retrospectivas de sprint

Registros em `retrospectivas/`, com índice em [retrospectivas/INDEX.md](retrospectivas/INDEX.md). O histórico é compartilhado por Claude e Codex. A skill `retrospectiva` distingue relatos, sugestões, acordos e acompanhamento de ações. Não duplicar transcrições integrais ou registrar exemplos fictícios como reuniões reais.
