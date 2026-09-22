# Serviço: Observabilidade

**Status**: protocolo mínimo disponível; automação e dashboards permanecem evolução futura.

## Responsabilidade

Registrar interações da plataforma para entender padrões de uso, identificar gargalos e alimentar o Agente de Evolução.

## Protocolo mínimo

Registre uma entrada curta somente ao término de missões relevantes, retrospectivas ou mudanças arquiteturais. Não registre conversas triviais nem conteúdo sensível. O destino é `knowledge/observability/YYYY-MM.md`, versionado e criado sob demanda. O responsável pela consolidação mensal é o `agente-evolucao`; a revisão ocorre no primeiro ciclo útil do mês seguinte.

```yaml
date: YYYY-MM-DD
mission: priorizar | discovery | especificar | validar | aprender | outro
skills: [orquestrador, ice]
result: decision | artifact | blocked | no-conclusion
blocker: null
rework: false
human_intervention: false
artifact: knowledge/decisions/...
```

O orquestrador propõe a entrada ao encerrar uma missão aplicável; ela só é gravada com a política de persistência do workspace. Enquanto não houver automação, o `agente-evolucao` consolida o arquivo mensal na revisão definida acima. Não crie uma base paralela de telemetria sem aprovação.

## Gatilho Imediato — Erro Rastreável a Doc/Skill

O ciclo mensal cobre padrão de uso. Ele não cobre erro pontual comprovado — nesse caso o sinal não pode esperar a consolidação do mês seguinte.

**Critério objetivo** (evita autoavaliação subjetiva do agente sobre "foi a doc ou fui eu"): o gatilho imediato dispara quando, na mesma interação, `blocker=true` OU `rework=true` OU `human_intervention=true` **e** o valor incorreto é rastreável a um doc/skill referenciada — não a uma inferência livre do agente. Julgamento de escopo do próprio agente (ex.: classificar como Tarefa algo que deveria ser Epic) não entra aqui — vai para o registro mensal normal.

**Fast-track de correção factual trivial**: quando o erro é um fato divergente comprovado (ID, enum ou nome de campo rejeitado pela própria API/ferramenta), o agente corrige o doc/skill diretamente e registra a entrada de observabilidade imediatamente — sem esperar aprovação prévia de `agente-governanca`. A entrada gravada é a auditoria retrospectiva: se o padrão se repetir, governança revisa depois. Correção que envolve decisão estrutural (ex.: qual arquivo vira fonte única para um enum duplicado em vários lugares) não é fast-track — segue o pipeline formal `agente-evolucao` → `agente-governanca`.

Agentes operacionais (ex.: `agente-delivery`, `agente-dados`) aplicam este critério por referência — não reafirmem o texto acima no arquivo do agente; duplicar a regra em cada agente é o mesmo padrão de drift que causou o incidente que originou esta seção (ver `knowledge/decisions/2026-08-11-gatilho-imediato-observabilidade-doc-desatualizada.md`).

## Dados a evitar

- credenciais, PII, conteúdo de entrevistas e dados operacionais identificáveis;
- transcrições completas de conversa;
- métricas de produtividade individual usadas para avaliação de pessoas.

## Campos obrigatórios

Por interação, quando o protocolo mínimo for aplicável:
- Agente ou skill utilizado
- Missão classificada pelo Orquestrador
- Resultado (artefato produzido / decisão tomada / sem conclusão)
- Falha ou retrabalho ocorrido
- Intervenção humana necessária

## Métricas Importantes

| Métrica | O que indica |
|---|---|
| Agente mais utilizado | Onde está o valor central da plataforma |
| Sequências recorrentes | Candidatos a loadout nomeado ou novo agente |
| Missões sem artefato | Falhas de orquestração |
| Skills nunca usadas | Candidatos a remoção |
| Perguntas bloqueantes recorrentes | Lacunas de contexto no KG |

## Relação com Agente de Evolução

O Agente de Evolução consome dados de observabilidade para:
1. Identificar padrões de uso
2. Detectar sobreposição entre agentes
3. Propor criação, fusão ou remoção de agentes
4. Submeter proposta ao Agente de Governança para aprovação
