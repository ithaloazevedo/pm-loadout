# Templates: Issues de PM

Issues criadas pelo PM — Improvement e Bug. Para issues técnicas de engenharia, use o skill `linear-issues`.

---

## Template: Improvement

Use para melhorias em funcionalidades existentes, ajustes de experiência ou otimizações identificadas pelo PM.

```markdown
## [Verbo no Imperativo] + [descrição da melhoria]

**Projeto:** [Projeto de Delivery vinculado]
**Tipo:** Improvement

---

### 🎯 O que melhorar
[O que existe hoje e o que deveria ser diferente — 1-2 frases. Seja específico sobre o comportamento atual.]

### 💡 Solução proposta
[O que deve ser feito — objetivo, não prescritivo de implementação. O assignee decide o como.]

### ✅ Critério de aceite
- [ ] [comportamento esperado após a melhoria — binário e testável]
```

---

## Template: Bug

Use para reportar comportamentos incorretos ou quebrados que o PM identificou — via teste, feedback de usuário ou monitoramento.

```markdown
## [Comportamento atual] → [Comportamento esperado]

**Projeto:** [Projeto de Delivery vinculado]
**Tipo:** Bug

---

### 🐛 Comportamento atual
[O que está acontecendo, com contexto de onde/quando ocorre — plataforma, perfil de usuário, fluxo]

### ✅ Comportamento esperado
[O que deveria acontecer nesta situação]

### 🔁 Como reproduzir
1. [Passo 1]
2. [Passo 2]
3. [Resultado observado]

### 📎 Evidência
[Print, link de sessão, log, feedback direto de usuário — se houver. Citações literais de usuários são preferíveis a paráfrases.]
```

---

---

## Exemplo Real: Improvement

## Persistir filtros ao navegar entre pastas da Biblioteca

**Projeto:** Redesenhar a Biblioteca de Conteúdos do Portal Plus
**Tipo:** Improvement

---

### 🎯 O que melhorar
Hoje, ao entrar em uma pasta com filtros ativos (ex: Ano escolar = "6º ano"), os filtros são resetados. O usuário precisa reaplicá-los manualmente a cada pasta navegada.

### 💡 Solução proposta
Os filtros ativos devem persistir ao navegar entre pastas e subpastas — sendo resetados apenas ao clicar explicitamente em "Limpar filtros".

### ✅ Critério de aceite
- [ ] Ao selecionar um filtro e clicar em uma pasta, o filtro continua ativo dentro da pasta e em subpastas navegadas em seguida

---

## Exemplo Real: Bug

## Campo de busca não exibe ícone X durante busca ativa → Usuário não consegue limpar sem apagar manualmente

**Projeto:** Redesenhar a Biblioteca de Conteúdos do Portal Plus
**Tipo:** Bug

---

### 🐛 Comportamento atual
O campo de busca da Biblioteca não exibe o ícone X ao digitar um termo. Para limpar a busca, o usuário precisa apagar o texto caractere a caractere — não há ação rápida de limpar.

### ✅ Comportamento esperado
Ao digitar no campo de busca, o ícone X deve aparecer à direita do campo. Ao clicar no X, a busca é limpa e a tela retorna ao estado anterior (sem resultado de busca).

### 🔁 Como reproduzir
1. Acessar a Biblioteca de Conteúdos no Portal Nave à Vela
2. Digitar qualquer termo no campo de busca
3. O ícone X não aparece — não é possível limpar com um clique

### 📎 Evidência
*"Tentei buscar por um material e não consegui limpar a busca sem apagar tudo, foi bem chato"* — feedback via CSAT Q1/2026

---

## Boas práticas

- **Improvement**: descreva o problema, não a solução técnica. O assignee define a implementação.
- **Bug**: quote feedback de usuários diretamente quando disponível — é mais autêntico e rápido do que parafrasear.
- **Título de Bug**: use o padrão `[o que acontece] → [o que deveria acontecer]` para deixar claro tanto o problema quanto a expectativa.
- **Critério de aceite**: um único critério é suficiente para a maioria das issues. Mais de três indica que pode ser um projeto, não uma issue.
