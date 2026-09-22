# Replicação pontual do pm-loadout para o Blow OS

**Data:** 2026-09-22
**Decisor:** Ithalo (PM)
**Status:** decidido e executado — MR mergeado na main do blow-os

## Contexto

O Blow OS já tinha nove agentes copiados do pm-loadout, sete deles divergentes, e uma `clickup-spec`
parada no modelo anterior ao de sprints: 39 menções a Iniciativa, OKR e Discovery, zero a sprint.
Quem abrisse o repositório e pedisse uma spec recebia o formato errado.

## Decisão

Replicar skills e agentes uma vez, sem automação. O pm-loadout continua sendo a ferramenta de
trabalho do PM e onde a plataforma evolui. O Blow OS é vitrine de consumo para stakeholders não
técnicos.

Entraram 21 skills, cinco agentes novos e o `agente-dados`. Ficaram de fora `registry/`, `services/`,
`prompts/` e os arquivos de arquitetura: são superfície de autoria da plataforma, e replicá-los
convidaria edição no repositório errado.

## Por que não automatizar

O diagnóstico reforçou a decisão em vez de contrariá-la. Um script de sincronização teria copiado o
`pessoas.md` junto, violando a política do próprio repositório, teria trazido as 69 decisões criando
um segundo log competindo com o `/syncar`, e teria sobrescrito `curador-de-contexto` e
`vigilancia-regulatoria` — que têm o mesmo nome nos dois repositórios mas são agentes diferentes.

As adaptações feitas à mão são exatamente o que a automação destruiria.

## Três regras que saíram disso

**Nome igual não é agente igual.** Antes de sobrescrever, comparar conteúdo. Dois agentes do Blow OS
foram construídos lá, com escopo próprio.

**Adaptação de runtime se preserva.** Em `agente-governanca`, `agente-estrategico` e
`agente-evolucao`, o corpo veio do pm-loadout e a seção de governança do Blow OS ficou.

**Convenção de nome depende do conjunto, não do repositório.** A renomeação de `query-pam` para
`query-trad` vale no pm-loadout, onde o par são duas casas. No Blow OS a família é `query-<domínio>`
— `query-pam`, `query-aml`, `query-slot` — e ali `query-pam` é o nome certo. Forçar o mesmo nome nos
dois seria drift no sentido contrário. A renomeação foi desfeita lá durante a resolução do merge.

## O que quase passou despercebido

A primeira versão da branch pôs 21 skills no lugar sem criar caminho até elas: 19 das 25
compartilhadas não apareciam em índice nenhum que uma pessoa lê. O que falhou não foi a cópia, foi a
definição de pronto. Skill que ninguém sabe que existe não entrega nada.

Também não foi replicado o `knowledge/domains/pessoas.md`: ele tem desligamento de pessoa e tabela de
influência de stakeholder, e o `CLAUDE.md` do Blow OS proíbe documento confidencial ali. Entrou só a
distribuição de papéis, que é o recorte que as skills usam.

## Próximos passos

Dezenove skills próprias do Blow OS seguem sem menção no guia de recursos — anteriores a esta
mudança. O `CODEOWNERS` não tem entrada para `/.claude/`, então toda aprovação de skill recai no
fallback `* @isaac`.
