# Exemplos e Transformações

## Conteúdo
- Transformações antes/depois por time
- Exemplo completo de estruturação
- Bons e maus títulos

---

## Transformações: Antes → Depois

### Time [Canais] Canal LMS

| Antes (Técnico) | Depois (Valor) |
|-----------------|----------------|
| `[2FA][25hF][35hB] Direcionamento após login + criação do endpoint /login/2fa` | `Direcionar usuário para fluxo 2FA após login` |
| `[2FA][12hF][15hB] Tela de digitar código + validação + endpoint /login/2fa/verify` | `Validar código 2FA e liberar acesso ao Portal` |
| `[2FA][9hF][6hB] Reenvio de código + endpoint /login/2fa/resend` | `Permitir reenvio do código 2FA por email` |
| `[2FA][4hF][5hB] Skip (pular 2FA) + endpoint /login/2fa/skip` | `Permitir que usuário pule o 2FA temporariamente` |
| `Monitoramento de erros no login` | `Reduzir tempo de detecção de falhas no login` |
| `Adicionar observabilidade no Personalizar plataforma` | `Adicionar dashboard de observabilidade para personalização do Portal` |
| `[EI] Ajuste de regra de visualização` | `Ajustar regras de visualização para perfis EI` |
| `Correções de Notificações` | `Corrigir entrega de notificações para perfis administrativos` |

### Time [LMS] Canais (Plus)

| Antes (Técnico) | Depois (Valor) |
|-----------------|----------------|
| `[Gestão de turmas] Nova header` | `Simplificar navegação na tela de Turmas` |
| `[Gestão de turmas] Refatoração da tabela de turmas` | `Facilitar localização e gestão de turmas na tabela` |
| `[Gestão de turmas] Novos filtros` | `Permitir filtrar turmas por nome, segmento e pendências` |
| `[Gestão de turmas] Modal de onboarding orientativo para a progressão de turmas` | `Orientar usuário sobre progressão de turmas no primeiro acesso do ano` |
| `Melhoria Consulta de Escolas` | `Melhorar performance da consulta de escolas` |
| `Zerar Diffs de Dados de Integração Ecossistema nas Integrações Cross → Plus` | `Garantir consistência dos dados de ecossistema entre Cross e Plus` |
| `Zerar Diffs de Dados de Integração Parceria SAS nas Integrações Cross → Plus` | `Garantir consistência dos dados de parceria SAS entre Cross e Plus` |
| `Evoluir configuração de exibição da barra de progressão para nível de escola` | `Permitir configurar barra de progressão por escola (não por usuário)` |
| `Salvar ano de progressão na criação de turma` | `Registrar ano de progressão automaticamente ao criar turma` |
| `Spike: Avaliar uso de accordions no editor HTML (Jodit) do Jornada` | `Investigar viabilidade de accordions no editor do Jornada` |

---

## Exemplo Completo de Estruturação

### ❌ Estrutura Técnica (Evitar)

```
CLMS-4231: [2FA][12hF][15hB] Tela de digitar código + validação + endpoint /login/2fa/verify
├── CLMS-4289: [1h][BFF] Criar o endpoint /login/2fa/verify
├── CLMS-4290: [3h][BFF] Verificar se o código está correto
├── CLMS-4295: [2h][Frontend] Integrar tela "Digite seu código"
├── CLMS-4296: [2h][Frontend] Mostrar erro quando código errado
└── CLMS-4298: [6h][Frontend] Redirecionar para Portal após sucesso
```

**Problemas:**
- Título da issue pai mistura implementação com valor
- Estimativas poluem o título
- Prefixos técnicos na issue pai

### ✅ Estrutura de Valor (Recomendado)

```
CLMS-4231: Validar código 2FA e liberar acesso ao Portal
│
│   Descrição:
│   ## Contexto
│   Usuários administrativos precisam validar identidade via código
│   enviado por email antes de acessar o Portal.
│
│   ## Resultado Esperado
│   Após digitar código correto, usuário acessa o Portal.
│   Se incorreto, visualiza erro e pode tentar novamente.
│
├── [BFF] Criar endpoint /login/2fa/verify
├── [BFF] Validar código contra Redis e retornar resultado
├── [Frontend] Criar tela "Digite seu código" com input de 6 dígitos
├── [Frontend] Exibir mensagem de erro quando código inválido
└── [Frontend] Redirecionar para home do Portal após validação
```

**Pontos positivos:**
- Título da issue pai foca no valor entregue
- Sub-issues têm prefixos técnicos claros
- Descrição concisa com contexto e resultado esperado
- Estimativas no campo dedicado (não no título)

---

## Bons e Maus Títulos

### Bons títulos

| Título | Por que é bom |
|--------|---------------|
| `Permitir validação 2FA no login do Portal` | Descreve o benefício para o usuário |
| `Melhorar performance da abertura de tela de turmas` | Resultado claro e mensurável |
| `Adicionar dashboard de observabilidade para login` | Valor entregue ao time de operações |
| `Simplificar navegação na tela de Turmas` | Benefício de UX explícito |
| `Garantir consistência dos dados entre Cross e Plus` | Resultado de negócio claro |

### Títulos a evitar

| Título | Problema | Sugestão |
|--------|----------|----------|
| `[BFF] Criar endpoint /login/2fa/verify` | Implementação, não valor | Usar como sub-issue |
| `[Frontend] Integrar tela de código 2FA` | Acoplado ao "como" | Usar como sub-issue |
| `[2FA][25hF][35hB] Direcionamento após login` | Poluído com estimativas e siglas | `Direcionar usuário para fluxo 2FA após login` |
| `Refatorar componente X` | Não explica o benefício | `Melhorar performance do componente X` |
| `Ajustes na API` | Vago demais | Especificar qual melhoria |
