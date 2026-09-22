# Instalação via Claude Code chat

Cole o prompt abaixo diretamente no chat do Claude Code (CLI, app desktop ou extensão do VS Code).
O Claude vai clonar o repo e copiar os arquivos para `~/.claude/` automaticamente.

---

## Prompt de instalação

```
Por favor, instale o pm-loadout no meu Claude Code. Execute os seguintes comandos shell:

1. Clone o repo numa pasta temporária:
   git clone https://github.com/ithaloazevedo/pm-loadout.git /tmp/pm-loadout

2. Crie as pastas globais do Claude Code (se não existirem):
   mkdir -p ~/.claude/skills ~/.claude/agents ~/.claude/workflows

3. Copie skills, agentes e o workflow banca:
   cp -R /tmp/pm-loadout/.claude/skills/* ~/.claude/skills/
   cp -R /tmp/pm-loadout/.claude/agents/* ~/.claude/agents/
   cp /tmp/pm-loadout/.claude/workflows/banca.js ~/.claude/workflows/

4. Limpe a pasta temporária:
   rm -rf /tmp/pm-loadout

Confirme quando terminar e liste as skills instaladas em ~/.claude/skills/.
```

---

Depois de instalado, reinicie o Claude Code e use `/orquestrador` para começar.
