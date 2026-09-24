# Fontes de contexto e operação

A fonte de autoria das skills e dos agentes é `.claude/`. A base Codex em `.agents/skills/` e `.codex/agents/` preserva o conteúdo de produto e adapta somente o necessário ao runtime. Consulte `services/runtime-sync.md` antes de editar saídas geradas.

| Informação | Fonte canônica | Como usar |
|---|---|---|
| Competências e regras | `.claude/skills/`, `.claude/agents/` | Ler só a skill/agente da missão; Codex usa a versão correspondente |
| Tom de voz | `knowledge/tom-de-voz.md` | Ler antes de escrever em nome do Ithalo |
| Contexto durável do produto | Repositório `blow-os`, conforme `config/pm-loadout.local.yaml` ou agente curador | Consultar arquivos pertinentes; registrar data da fonte e lacunas |
| Conceitos locais e decisões do PM Loadout | `knowledge/domains/`, `knowledge/decisions/` | Verificar se decisões recentes substituem exemplos ou registros antigos |
| Pesquisa e voz do usuário (achados, instrumentos, voz do cliente) | `knowledge/pesquisas/INDEX.md` | Checar achado existente antes de nova pesquisa; abrir o link/arquivo só quando a análise específica exigir o detalhe — o índice não substitui a leitura da fonte |
| Retrospectivas e ações de melhoria | `knowledge/retrospectivas/INDEX.md` e registros por reunião | Fonte local do aprendizado; não copiar transcrições integrais |
| Escopo, compromissos e execução | ClickUp | Consultar estado atual quando relevante; registro local não substitui estado vivo do card |
| Resultados observados | Fonte de dados indicada pela missão/agente de dados | Não confundir diagnóstico documentado com medição atual |

O blow-os pode ser localizado como repositório irmão `../blow-os`; o caminho local configurado prevalece. Contexto PAM hoje é indicado pelo curador em `vertical/frentes/pam/`. Confirme a existência antes de usar: nunca invente um pack ou migre seu nome para Codex-os. Fontes inacessíveis são lacunas explícitas. Documento local é uma evidência datada, não prova automática do estado atual em produção.

## Configuração

`config/pm-loadout.example.yaml` documenta os campos. `config/pm-loadout.local.yaml` é local e ignorado pelo Git; nunca inclui credenciais. Leia-o antes de usar conectores ou persistir conteúdo. Caminhos relativos são resolvidos a partir da raiz do PM Loadout.

A configuração orienta os agentes; não cria integração, concede acesso ou aplica permissões técnicas sozinha. `existing-authorized-tools` significa usar ferramentas já disponíveis e autorizadas, sem inventar um conector. O pedido de registrar uma retrospectiva autoriza o arquivo local e o índice; pedidos de apenas analisar não autorizam persistência. Envio ao canal, criação de Doc e criação de tarefas são ações distintas, executadas quando explicitamente solicitadas. Reutilize autorização da conversa.

## Instalações e atualidade

Execute `python3 scripts/audit-loadout.py` no projeto; use `--global` para comparar cópias homônimas nas pastas de instalação. Uma diferença pode ser adaptação legítima. O comando não prova qual cópia uma sessão carregou: confirme o caminho resolvido no runtime ao investigar divergência.

Não substitua nem exclua cópias globais automaticamente. Ao operar fora do projeto, indique o caminho canônico do PM Loadout no pedido. O repositório contém conhecimento e histórico que não acompanham uma simples cópia da pasta da skill.

## Atualização e conflitos

Guarde origem e data de verificação de fatos novos. Diferencie fato, hipótese, proposta e decisão. Se fontes discordarem, preserve a divergência e procure evidência pertinente à casa, ambiente e período da missão. Só altere a fonte canônica no escopo autorizado; mudanças no blow-os seguem o fluxo de contribuição do próprio repositório.

## Recuperação orientada a perguntas

Para cadastro, `knowledge/contexto/cadastro.json` conecta fontes do blow-os sem duplicar a arquitetura. `scripts/context-map.py` consulta a cadeia e identifica mudança de conteúdo; hash não revalida produção. Veja `docs/piloto-contexto-cadastro.md`. A escolha de skill segue a pergunta: `aprendizado-produto` fecha hipóteses e `lideranca` acompanha acordos com autoridade e privacidade explícitas.
