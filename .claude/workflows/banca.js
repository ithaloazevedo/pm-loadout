export const meta = {
  name: 'banca',
  description: 'Panel review: três perspectivas paralelas (Produto, Design, Tech) sobre uma decisão ou spec crítica',
  phases: [
    { title: 'Revisão', detail: 'Três lentes em paralelo — Produto, Design e Tech' },
    { title: 'Síntese', detail: 'Consolidar veredictos, objeções e mudanças mínimas' },
  ],
}

const REVIEW_SCHEMA = {
  type: 'object',
  properties: {
    role: { type: 'string' },
    objections: { type: 'array', items: { type: 'string' } },
    risks: { type: 'array', items: { type: 'string' } },
    mitigations: { type: 'array', items: { type: 'string' } },
    verdict: { type: 'string', enum: ['APROVA', 'APROVA COM RESSALVAS', 'BLOQUEIA'] },
    minimum_change: { type: 'string' },
  },
  required: ['role', 'objections', 'risks', 'mitigations', 'verdict', 'minimum_change'],
}

const SYNTHESIS_SCHEMA = {
  type: 'object',
  properties: {
    summary: { type: 'string' },
    consensus_verdict: { type: 'string', enum: ['APROVADO', 'APROVADO COM RESSALVAS', 'BLOQUEADO'] },
    blocking_issues: { type: 'array', items: { type: 'string' } },
    required_changes: { type: 'array', items: { type: 'string' } },
    next_step: { type: 'string' },
  },
  required: ['summary', 'consensus_verdict', 'blocking_issues', 'required_changes', 'next_step'],
}

const spec = args || ''
if (!spec) {
  log('Nenhuma spec fornecida como args. Rode: Workflow({name:"banca", args:"<spec ou descrição da decisão>"})')
}

const LENSES = [
  {
    key: 'produto',
    agentType: 'lente-produto',
    label: 'Head de Produto',
    prompt: `Você é o Head de Produto fazendo uma revisão crítica (banca) desta decisão ou spec:\n\n${spec}\n\nRevise sob a perspectiva de estratégia, evidência de usuário, custo de oportunidade e integridade do processo de produto.`,
  },
  {
    key: 'design',
    agentType: 'lente-design',
    label: 'Head de Design',
    prompt: `Você é o Head de Design fazendo uma revisão crítica (banca) desta decisão ou spec:\n\n${spec}\n\nRevise sob a perspectiva de experiência do usuário, coerência de design, acessibilidade e dívida de UX.`,
  },
  {
    key: 'tech',
    agentType: 'lente-tech',
    label: 'Head de Tecnologia',
    prompt: `Você é o Head de Tecnologia fazendo uma revisão crítica (banca) desta decisão ou spec:\n\n${spec}\n\nRevise sob a perspectiva de viabilidade técnica, arquitetura, segurança, compliance e risco de entrega.`,
  },
]

log('Iniciando revisão paralela: Produto · Design · Tech')

const reviews = await parallel(
  LENSES.map(lens => () =>
    agent(lens.prompt, {
      label: lens.key,
      phase: 'Revisão',
      schema: REVIEW_SCHEMA,
      agentType: lens.agentType,
    })
  )
)

const validReviews = reviews.filter(Boolean)

if (validReviews.length === 0) {
  log('Nenhuma revisão retornou. Verifique se os agentes lente-produto, lente-design e lente-tech estão disponíveis.')
  return null
}

const verdicts = validReviews.map(r => r.verdict)
const hasBlock = verdicts.includes('BLOQUEIA')
const hasReservations = verdicts.includes('APROVA COM RESSALVAS')

log(`Veredictos: ${verdicts.join(' · ')} — ${hasBlock ? 'há bloqueio' : hasReservations ? 'há ressalvas' : 'aprovação'}`)
log('Sintetizando parecer consolidado...')

const synthesis = await agent(
  `Você é o facilitador da banca. Sintetize os pareceres das três perspectivas abaixo em um veredicto consolidado claro e acionável.

Pareceres recebidos:
${JSON.stringify(validReviews, null, 2)}

Regras de síntese:
- Se qualquer perspectiva BLOQUEIA: veredicto = BLOQUEADO (a menos que o bloqueio seja sobre escopo fora do domínio da lente)
- Se há APROVA COM RESSALVAS mas nenhum bloqueio: veredicto = APROVADO COM RESSALVAS
- Se todas APROVAM: veredicto = APROVADO
- Liste apenas as mudanças realmente exigidas (não sugestões opcionais)
- O próximo passo deve ser concreto e atribuível`,
  {
    phase: 'Síntese',
    schema: SYNTHESIS_SCHEMA,
  }
)

return {
  reviews: validReviews,
  synthesis,
}
