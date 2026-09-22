# Template: Ticket Operacional

Vive na lista **Operação, sustentação e infraestrutura** (`901114236869`, espaço Vertical Tech). Use para
pedidos pontuais de execução — acesso, infraestrutura, configuração, suporte a terceiros — que não envolvem
decisão de produto, pesquisa ou escopo de UX. Assim como todo item do processo hoje, não tem hierarquia
vinculada acima dele (não existe mais nível Objetivo nem Discovery em lugar nenhum do fluxo); não exige
`Módulo do PAM` nem campos de priorização. Fluxo de status: `pendente` → `em progresso` → `em validação` →
`completo`.

---

## Template

> **Sem bloco de cabeçalho.** O solicitante vai no campo nativo **Solicitante** (quando existir na lista),
> não em texto. Dono é o assignee da task — nunca infira sozinho, confirme com o usuário. **Espaçamento:**
> linha em branco só **entre** seções `###`.

```markdown
### 🎯 Objetivo
[1-2 frases: o que precisa ser feito, para quem/por quem, e por quê]

### ✅ Critérios de Aceite
- [ ] [ação específica e verificável — ex.: acesso concedido, configuração aplicada, confirmado por quem pediu]
```

**Regras de uso:**

- **Sem Contexto, sem Escopo, sem Links.** Se a tarefa precisar de qualquer uma dessas seções para fazer
  sentido, ela não é mais um ticket operacional simples — reavalie se cabe em Discovery/Delivery.
- **Solicitante é campo, não texto.** Preencha o custom field `Solicitante` em vez de escrever "solicitado
  por X" no corpo.
- **Quem executa nem sempre é membro do ClickUp.** Quando a ação depende de alguém fora do workspace (ex.:
  fornecedor ou time de infra externo), nomeie essa pessoa no Objetivo — não force um assignee que não existe
  como membro do workspace.
- **Critérios de aceite são o resultado, não os passos.** Um item por resultado verificável (ex.: "Fulano tem
  acesso X confirmado"), não a sequência de execução.

---

## Exemplo Real: Liberar acesso de criação e alteração de tabelas no banco de produção

### 🎯 Objetivo
Gisélio libera para Gabriel Moreschi e Rayan o acesso de criação e alteração de tabelas no banco de produção
— hoje o time não consegue criar tabelas nem alterar a tabela `global_configs`, o que bloqueia demandas da
squad Plataforma.

### ✅ Critérios de Aceite
- [ ] Gabriel Moreschi tem acesso de criação e alteração de tabelas confirmado no banco de produção
- [ ] Rayan tem acesso de criação e alteração de tabelas confirmado no banco de produção
