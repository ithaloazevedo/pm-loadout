# Domínio: Pessoas

Entidades que descrevem quem faz o quê — times, papéis e stakeholders.

---

## Times (atualizado 2026-09-18)

| Time | Team Lead | Tech Lead | Desenvolvedores | Product Designer | Product Manager | QA |
|---|---|---|---|---|---|---|
| **Time PAM** | Rayan | Ícaro | Hugo, Alex, Gabriel Moreschi (⚠️ ver nota), Railton, Melk | Allison, Mateus Sperandio | Ithalo | David |
| **Produto** | Marcelinho | Kennedy | Gabriel, Marcos | Mateus | Victor Tarelho | Primo |

> **Fusão 2026-09-18**: Backoffice & Integrações e Plataforma (Experiência do Jogador) — os dois times de Ithalo — viraram um **Time PAM** único, com responsabilidade ponta a ponta: PAM, backoffice, experiência do jogador e as integrações com provedor, KYC, AML, agregadores etc. Liderança única: **Rayan** (antes Tech Lead da Plataforma) assume Team Lead; **Ícaro** (antes Tech Lead do Backoffice & Integrações) segue Tech Lead. Ithalo deixa de ser PM dividido em dois backlogs — agora é PM de um único time, com escopo maior. Ver [[2026-09-18-fusao-backoffice-plataforma-em-time-pam]].

> ⚠️ **Pendência**: o papel de **Gabriel Moreschi** (Team Lead anterior da Plataforma) no time fundido não foi confirmado — listado acima como desenvolvedor por suposição, a confirmar com Ithalo antes de tratar como fato.

> ⚠️ **Tony (QA, antes compartilhado entre Backoffice & Integrações e Plataforma) saiu da empresa (2026-09-18)** — substituído por **David** como QA único do Time PAM.

> ⚠️ **Linecker Gomes saiu da empresa (2026-09-18)** — substituído por **Mateus Sperandio** como Product Designer na frente de experiência do jogador. Atenção: existem dois "Mateus" na organização — o designer do time **Produto** (só "Mateus") e **Mateus Sperandio** (Time PAM). Usar sempre o nome completo para não confundir.

> Esta estrutura substitui a de 30/07/2026 (Backoffice & Integrações / Plataforma / Produto como três times separados), que por sua vez substituiu a anterior (Experiência do jogador / Operação e afiliados / Provedora de conteúdo) e a versão intermediária de 08/07/2026 (Provedor de Jogos / Experiência do Jogador / Back Office e Integrações). Ver [[2026-07-30-estrutura-times-e-papeis]].

---

## Papéis

Times enxutos — Team Lead e Tech Lead também são mão na massa (não são cargos puramente de gestão).

| Papel | Foco | Responsabilidades |
|---|---|---|
| **Team Lead** | Pessoas e entrega | Gestão de pessoas (1-on-1, carreira), planejamento (sprint, tracking de entrega), remove impedimentos, fala com parceiros de negócio |
| **Tech Lead** | Técnico | Padrão de código e review de PR, arquitetura e escolha de ferramentas, mentoria técnica dos devs |
| **Product Manager** | O quê e por quê | Dono do roadmap, specs e critérios de aceite |
| **Product Designer** | Como da experiência | Protótipos em Figma |
| **QA** | Qualidade | Valida critérios de aceite, levanta correções pós-homologação |
| **Desenvolvedor(a)** | Implementação | Constrói, participa de code review, levanta risco técnico cedo |
| **Data Analyst** | Dados | Instrumenta eventos, constrói dashboards, valida hipóteses |

---

## Stakeholders

| Stakeholder | Nível de influência | Interesse principal |
|---|---|---|
| **CEO (Isaac)** | Alto — decisor final | Crescimento, compliance, posicionamento |
| **Diretoria** | Alto | Metas de negócio, resultados financeiros |
| **Head de Produto** | Alto | Roadmap, qualidade de entrega, métricas |
| **Head de Tecnologia** | Alto | Arquitetura, estabilidade, segurança |
| **Clientes (casas)** | Médio-alto | Funcionalidades específicas, SLA |
| **Usuário final** | Médio | Experiência, confiança, facilidade de uso |
| **Regulador (SPA/MF)** | Alto | Conformidade com Lei 14.790 e Portarias |

---

## Personas (Tradicional)

**Persona principal**: Jogador de loteria mobile-first, 34–54 anos, familiarizado com apostas informais, buscando praticidade e confiança.

**Atributos**:
- Dispositivo preferencial: smartphone Android
- Comportamento: aposta pequena, frequente, motivada por entretenimento e esperança de ganho
- Barreira principal: desconfiança em plataformas digitais, dificuldade no cadastro
- Motivação: praticidade (sem filas), bônus, familiaridade com o formato lotérico

> Para personas detalhadas e atualizadas, consultar o context pack no claude-os via `curador-de-contexto`.
