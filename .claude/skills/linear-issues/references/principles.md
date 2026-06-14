# Princípios Fundamentais

## Conteúdo
- Valor vs. implementação
- Hierarquia de issues
- Issues pai = valor
- Sub-issues = técnica
- Estrutura de título

---

> **Issues devem descrever o VALOR entregue, não a implementação técnica.**

A pessoa que lê o título de uma issue deve entender o benefício ou resultado esperado, sem precisar conhecer detalhes técnicos da solução.

## Hierarquia de Issues

```
📦 Issue Pai (VALOR)
   │
   │   Foco: O QUE será entregue
   │   Público: Qualquer pessoa do time/empresa
   │
   └── 🔧 Sub-issues (TÉCNICA)
       │
       │   Foco: COMO será implementado
       │   Público: Time técnico
       │
       ├── [BFF] Criar endpoint X
       ├── [Frontend] Implementar tela Y
       └── [Infra] Configurar Z
```

## Issues Pai = VALOR

- Título descreve o **resultado/benefício**, não a implementação
- **Sem prefixos técnicos** como `[BFF]`, `[Frontend]`, `[API]`
- **Sem estimativas no título** - usar campo dedicado
- Qualquer pessoa do time deve entender o benefício

## Sub-issues = TÉCNICA

- Prefixos técnicos são bem-vindos: `[BFF]`, `[Frontend]`, `[API]`, `[Infra]`
- Descrevem implementação específica e atômica
- Vinculadas à issue pai
- Pode incluir estimativas de horas no título se o time preferir

## Estrutura de Título

```
[Verbo de ação] + [resultado/benefício] + [contexto se necessário]
```

**Verbos por tipo:**

| Tipo de Entrega | Verbos |
|-----------------|--------|
| Nova funcionalidade | Permitir, Adicionar, Criar, Implementar |
| Melhoria | Melhorar, Otimizar, Simplificar, Facilitar |
| Correção | Corrigir, Resolver, Eliminar |
| Remoção | Remover, Descontinuar |
