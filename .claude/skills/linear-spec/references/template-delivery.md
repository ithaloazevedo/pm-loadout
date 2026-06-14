# Template: Projeto de Delivery

Use quando o Discovery foi concluído — direção validada, escopo fechado, engenharia pode iniciar planejamento.

---

## Template

```markdown
## [Verbo no Imperativo] + [Nome do Projeto]

**Iniciativa:** [Nome da Iniciativa]
**Discovery:** [Link do Projeto de Discovery]
**Dono:** [Nome]

---

### 🎯 Objetivo
[1-2 frases sobre o que este projeto entrega e qual KPI move]

### 🧠 Contexto
[Problema validado no discovery, dados que justificam, o que já sabemos sobre a direção]

### 📋 Escopo
✅ **Dentro:**
- Usuário consegue [capacidade 1]
- Usuário consegue [capacidade 2]

🚫 **Fora:**
- [O que explicitamente não será feito neste projeto — evita scope creep]

### ✅ Critérios de Aceite

**[Área funcional 1]**
- [ ] [comportamento específico e testável]
- [ ] [comportamento específico e testável]

**[Área funcional 2]**
- [ ] [comportamento específico e testável]

### 🔗 Links
- Figma: [link]
- Discovery: [link]
- Pré-requisito: [link se houver]
```

---

## Exemplo Real: Redesenhar a Biblioteca de Conteúdos do Portal Plus

### Antes (input bruto do Discovery)

```
O discovery validou a direção: pastas visíveis na tela e busca mais eficiente
resolvem o problema central sem explodir a arquitetura de conteúdo existente.

KPIs: redução de dead clicks e quick backs na Biblioteca.
```

**Problemas:** sem critérios de aceite por área funcional, escopo não descrito em linguagem de capacidade do usuário, sem vínculo explícito ao Discovery.

---

### Depois (estruturado)

## Redesenhar a Biblioteca de Conteúdos do Portal Plus

**Iniciativa:** Elevar a encontrabilidade de recursos no Portal Arcoplus
**Discovery:** [Prototipar a Biblioteca de Conteúdos do Portal Arcoplus](https://linear.app/isaac/project/...)
**Dono:** [Nome do PM responsável]

---

### 🎯 Objetivo
Entregar a nova experiência de navegação da Biblioteca de Conteúdos — DS atualizado, busca transversal e filtros combinados — reduzindo dead clicks e quick backs que indicam que usuários não conseguem encontrar materiais de forma autônoma.

### 🧠 Contexto
A navegação atual usa um menu dropdown ("Meus Materiais") que a maioria dos usuários não percebe como clicável. O discovery validou: pastas visíveis em grade e busca eficiente resolvem o problema documentado sem alterar a arquitetura de conteúdo.

### 📋 Escopo
✅ **Dentro:**
- Usuário vê as pastas da Biblioteca diretamente na tela — sem dropdown, sem clique extra
- Usuário busca qualquer arquivo por nome, independente da pasta em que está
- Usuário filtra o conteúdo por Ano escolar, Formato e Ordenação — de forma combinada e persistente
- Usuário retoma rapidamente conteúdos acessados via seção "Vistos recentemente"
- Design System da Biblioteca atualizado — componentes, tokens e tipografia alinhados

🚫 **Fora:**
- Reorganização editorial das categorias (responsabilidade do time de conteúdo)
- Componente de Notificação e configuração no backoffice (projeto separado)
- Migração da hierarquia de pastas no backoffice (projeto separado — pré-requisito)

### ✅ Critérios de Aceite

**Navegação e estrutura**
- [ ] Menu dropdown "Meus Materiais" removido — pastas exibidas diretamente como grid na home
- [ ] Único modo de visualização disponível é grade (lista removida)
- [ ] Breadcrumb atualizado em cada nível: `Início > Biblioteca de conteúdos > [Nome da pasta]`

**Busca**
- [ ] Busca retorna apenas arquivos de qualquer pasta da Biblioteca
- [ ] Campo exibe ícone X durante busca ativa; ao clicar limpa e retorna ao estado anterior
- [ ] Estado com resultado: listagem de cards com label "Resultado"
- [ ] Estado sem resultado: mensagem "Nenhum material encontrado - Tente novamente"

**Filtros**
- [ ] Filtros disponíveis: Ano escolar, Formato e Ordenação — presentes na home e dentro de pastas
- [ ] Filtros são cumulativos e podem ser combinados com a busca
- [ ] Filtros persistem em todas as telas até o usuário clicar em "Limpar filtros"
- [ ] Pastas sem itens correspondentes ao filtro somem da grade

**Seção Vistos recentemente**
- [ ] Aparece somente quando o usuário acessou ao menos 1 conteúdo — sem seção vazia
- [ ] Exibe no máximo 3 cards, da esquerda para direita (mais recente → menos recente)

**Estados da interface**
- [ ] Padrão completo: com histórico + curadoria ativa
- [ ] Primeiro acesso: sem histórico, sem curadoria — apenas Conteúdos
- [ ] Busca com resultado / Busca sem resultado / Loading / Pasta vazia / Erro de carregamento

### 🔗 Links
- Figma: [Navegabilidade Plus](https://www.figma.com/...)
- Discovery: [Prototipar a Biblioteca de Conteúdos do Portal Arcoplus](https://linear.app/...)
- Pré-requisito: [Simplificar a arquitetura de conteúdos do backoffice](https://linear.app/...)
