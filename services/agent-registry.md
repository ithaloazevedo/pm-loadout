# Serviço: Agent Registry

## Responsabilidade

Registro formal de cada agente da plataforma com missão, inputs, outputs, dependências e métricas de sucesso. Fonte de verdade para o Agente de Evolução auditar a arquitetura.

## Implementação

Arquivos YAML em `registry/`, um arquivo por agente.

## Schema

```yaml
id:              # identificador único (kebab-case)
name:            # nome legível
version:         # "1.0"
owner:           # PM ou papel responsável
mission:         # uma frase — o que o agente resolve
inputs:          # lista de entradas aceitas
outputs:         # lista de saídas produzidas
tools:           # ferramentas MCP ou built-in usadas
dependencies:    # outros agentes ou serviços necessários
knowledge:       # arquivos do KG que o agente deve ler
memory:          # que tipo de memória o agente consome
success_metrics: # como saber que o agente funcionou bem
failure_modes:   # padrões de falha comuns
handoff_rules:   # quando e para onde passar o trabalho
```

## Convenções

- `id` deve coincidir com o `name:` no frontmatter do arquivo `.md` do agente
- `version` incrementa quando responsabilidade ou schema mudam
- `failure_modes` são observados em uso real — adicionar quando identificados
- Nunca criar agente sem registro YAML correspondente

## Agentes Registrados

| ID | Arquivo YAML |
|---|---|
| `agente-estrategico` | `registry/agente-estrategico.yaml` |
| `agente-discovery` | `registry/agente-discovery.yaml` |
| `agente-spec` | `registry/agente-spec.yaml` |
| `agente-delivery` | `registry/agente-delivery.yaml` |
| `agente-insights` | `registry/agente-insights.yaml` |
| `agente-governanca` | `registry/agente-governanca.yaml` |
| `agente-evolucao` | `registry/agente-evolucao.yaml` |
| `curador-de-contexto` | `registry/curador-de-contexto.yaml` |
| `vigilancia-regulatoria` | `registry/vigilancia-regulatoria.yaml` |
| `prontidao-ia` | `registry/prontidao-ia.yaml` |
| `lente-produto` | `registry/lente-produto.yaml` |
| `lente-design` | `registry/lente-design.yaml` |
| `lente-tech` | `registry/lente-tech.yaml` |
| `agente-dados` | `registry/agente-dados.yaml` |
