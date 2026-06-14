# Anti-patterns a Evitar

## Conteúdo
- Anti-patterns no título
- Anti-patterns na descrição
- Exemplos concretos de descrições (evitar vs. recomendado)

---

## No Título

| Anti-pattern | Exemplo | Problema |
|--------------|---------|----------|
| Estimativas | `[25hF][35hB] Criar fluxo` | Polui título, usar campo dedicado |
| Múltiplos prefixos | `[2FA][Login][Portal]` | Confuso, focar no valor |
| Siglas sem contexto | `[EI] Ajuste RN1` | Incompreensível para outros |
| Muito genérico | `Ajustes na API` | Não comunica valor |
| Só implementação | `Refatorar UserService` | Não explica o benefício |

## Na Descrição

| Anti-pattern | Problema |
|--------------|----------|
| User Story extensa | Linear recomenda evitar "Como... Quero... Para que..." |
| Spec técnica completa | Manter em doc separado, linkar na issue |
| Sem contexto | Título não é suficiente, adicionar contexto |
| Cópia do título | Descrição deve agregar informação |
| Lista de tarefas técnicas | Descrição da issue pai não deve ser checklist de implementação |
| Descrição vazia | Mesmo issues simples precisam de contexto mínimo |

---

## Exemplos Concretos de Descrições

### User Story extensa (evitar)

```
Como usuário administrador do Portal,
Quero poder filtrar turmas por segmento,
Para que eu consiga encontrar mais rapidamente a turma que preciso gerenciar,
Dado que hoje existem mais de 200 turmas no sistema
E o carregamento da página demora mais de 5 segundos...
```

### Descrição concisa (recomendado)

```
## Contexto
Administradores com muitas turmas (~200+) têm dificuldade para localizar turmas específicas.

## Resultado Esperado
Filtro por segmento na tela de turmas, reduzindo o tempo de busca.

## Critérios de Aceite
- [ ] Filtro por segmento funcional na listagem
- [ ] Filtro persiste ao navegar entre páginas
```

### Spec técnica na descrição (evitar)

```
Criar endpoint POST /api/v2/turmas/filter que recebe { segmento: string, nome: string }
e retorna array de TurmaDTO. Usar cache Redis com TTL de 5min.
Criar componente FilterBar com react-select. Usar debounce de 300ms...
```

### Descrição com link para spec (recomendado)

```
## Contexto
Necessidade de filtros avançados na tela de turmas para escolas com grande volume.

## Resultado Esperado
Usuário consegue filtrar turmas por segmento e nome com resposta rápida.

## Links
- [Spec técnica detalhada](link-para-doc)
- [Design no Figma](link-para-figma)
```

### Descrição vazia ou cópia do título (evitar)

```
Título: Melhorar performance da consulta de escolas
Descrição: Melhorar a performance da consulta de escolas.
```

### Descrição que agrega valor (recomendado)

```
## Contexto
A consulta de escolas no painel administrativo leva ~8s para carregar em regiões
com mais de 500 escolas, impactando a produtividade do time de operações.

## Resultado Esperado
Consulta carrega em menos de 2s para qualquer volume de escolas.

## Critérios de Aceite
- [ ] Tempo de resposta < 2s para 1000+ escolas
- [ ] Sem degradação em outras consultas do painel
```
