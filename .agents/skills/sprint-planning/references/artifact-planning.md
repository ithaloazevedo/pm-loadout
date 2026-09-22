# Contrato visual da planning

Padrão do artifact validado na Sprint 2 do Time PAM. Não é sugestão de estilo: é o formato que o PM
aprovou depois de doze iterações. Mantenha, e mude só quando ele pedir.

Carregue a skill `dataviz` antes de escrever os dois gráficos da visão executiva.

---

## Identidade

Conceito: **placar**. A planning é lida como um quadro de acompanhamento, não como um documento. Números
alinhados, estados legíveis de relance, nenhuma decoração que não carregue informação.

### Cores

Tema claro no `:root`, escuro redefinido em `@media (prefers-color-scheme: dark)` guardado por
`:root:not([data-theme="light"])` e de novo em `:root[data-theme="dark"]`.

| Token | Claro | Escuro | Uso |
|---|---|---|---|
| `--ground` | `#F2F3EF` | `#131611` | fundo da página |
| `--surface` | `#FFFFFF` | `#1B1F1A` | cartões e listas |
| `--surface-2` | `#FAFBF7` | `#20251F` | cabeçalho de grupo |
| `--ink` | `#171A16` | `#E9ECE5` | texto principal |
| `--ink-2` | `#3C423A` | `#C3C9BC` | texto de apoio |
| `--muted` | `#6B7168` | `#97A093` | rótulos e metadados |
| `--line` | `#DDE0D7` | `#2E342B` | divisores |
| `--accent` | `#1F6F5C` | `#57B896` | acento único |
| `--accent-soft` | `#E2EDE7` | `#1E2A24` | fundo de etiqueta de casa |
| `--accent-ink` | `#14503F` | `#8FD3B8` | texto sobre acento |

Cores semânticas de estado, separadas do acento:

| Estado | Token claro | Token escuro |
|---|---|---|
| entregue, em validação, indo para produção | `#2E7D5B` | `#5FBE92` |
| em andamento | `#9A6510` | `#D7A54B` |
| não iniciada | `#7A8079` | `#9AA396` |
| bloqueada | `#B3392E` | `#E08379` |
| em discussão | `#4655A0` | `#8E9BE0` |

### Tipografia

Google Fonts, com stack de fallback real em cada família.

- **Archivo** 500/600/700 — títulos, números grandes, nomes de pessoa.
- **Source Sans 3** 400/600 — texto corrido.
- **IBM Plex Mono** 400/500 — rótulos maiúsculos, etiquetas, posição na fila e qualquer número em coluna.

Todo número que se alinha em coluna recebe `font-variant-numeric: tabular-nums`.

---

## Componentes

### Cabeçalho fixo

Nome da sprint, período e casas atendidas. Abaixo, as abas como `role="tablist"` com `aria-selected` e
`aria-controls`. A aba escolhida é lembrada em `localStorage`, dentro de `try/catch`, e a página precisa
renderizar corretamente sem isso.

### Caixa de objetivo

Fundo `--surface`, borda esquerda de 3px em `--accent`. Rótulo em mono maiúsculo, frase do objetivo em
Archivo 600, e um parágrafo de apoio com no máximo 62 caracteres de largura de leitura.

### Faixa de números

Grade de no máximo cinco blocos, separados por 1px de `--line`. Número em Archivo 700, tamanho 27px,
tabular. Uma linha curta abaixo dizendo o que o número é. **Nunca mais de cinco** — a faixa serve para ler
de relance, e a partir do sexto ninguém lê nenhum.

### Gráficos da visão executiva

Dois, lado a lado, empilhando em uma coluna abaixo de 760px.

1. **Frente de valor** — barras horizontais ordenadas por volume. Rótulo à esquerda, valor na ponta da
   barra. Cada barra nomeia uma frente que o leitor reconhece: retenção, conversão, eficiência da
   operação, compliance.
2. **Casa** — comparação entre Tradicional e Bravo, deixando visível a parcela compartilhada. O item que
   serve as duas casas conta nas duas, e o gráfico precisa dizer isso no próprio desenho, não só na
   legenda.

Texto do gráfico usa os tokens de tema. Todo rótulo nomeia um valor que o gráfico alcança. Nada de
gradiente decorativo.

### Lista de itens

Grade de quatro colunas: faixa de estado (4px), posição na fila (mono, alinhada à direita), nome, etiqueta
de estado.

Abaixo do nome, as etiquetas: casa, frente de valor e, quando aplicável, marcas especiais. Etiqueta em mono
maiúsculo, 10.5px.

**Campo deduzido recebe borda inferior pontilhada e um `title` explicando que não está preenchido no
ClickUp.** É o único recurso do artifact que distingue dado de leitura, e não pode ser removido.

Marcas especiais existentes:

- `sem desenvolvedor alocado` — item só com produto e design.
- `sem previsão de conclusão nesta sprint` — entrou por capacidade, não por compromisso de ciclo.

### Rodapé de leitura

Uma frase explicando: o que o pontilhado significa e quantos itens foram deduzidos, de onde vem a ordem de
prioridade e quantos itens têm o campo preenchido, e que títulos foram reescritos para leitura executiva
com o original disponível no tooltip.

---

## O que não colocar

Aprendido removendo do modelo que funcionou:

- **Etiqueta redundante com o estado.** "Entra em execução agora" ao lado de "não iniciada" é a mesma
  informação duas vezes, e o ruído compete com o que importa.
- **Ranking de pessoas por volume.** Ordem alfabética entre devs. A lista não deve sugerir que quem tem
  mais itens trabalha mais.
- **Seção que existe por simetria.** "Por frente" e "por casa" viraram dois gráficos porque a lista inteira
  repetida em três recortes cansava sem acrescentar.
- **Emoji como marcador de seção.** O tom de voz é explícito: sem emoji em documentação.
- **Hero de altura de tela.** A primeira dobra precisa mostrar objetivo e números, não um título grande.

## Verificação antes de publicar

1. A página abre mostrando objetivo e números, sem rolar.
2. Funciona em 400px de largura, sem rolagem horizontal.
3. Tema claro e escuro, ambos legíveis, com `body` pintando fundo a partir de token.
4. Todo campo deduzido está marcado e contado no rodapé.
5. Nenhum nome de arquivo, endpoint, tabela ou ferramenta interna aparece.
6. O objetivo da sprint e os objetivos por dev foram validados pelo PM antes da publicação.
