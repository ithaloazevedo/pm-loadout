# LEIA-ME — Dashboard Geral/Turnover (setup local, autenticação via IAM)

Recorte do dashboard pessoal de Performance do Jonatas, contendo as abas
**Geral**, **Turnover** e **Funil de Aquisição**.

> **Atualização (2026-08-18, Ithalo):** adicionada a aba **Funil de Aquisição**
> — jornada granular de cadastro (13 passos) a partir das flags novas
> `entities.json_flags.cadastroProgresso`, instrumentadas em 05/08/2026. Cobre
> funil completo, ranking de etapas com mais perdas, evolução por dia, sinais
> de atrito e tempo mediana/p90 entre passos. Ver `.claude/skills/dashboard-tradicional/SKILL.md`
> para o detalhe de rotas. Nessa mudança, a seção "Funil de Aquisição" que já
> existia dentro da aba Geral (retenção FTD → 2º...7º+ depósito) foi renomeada
> para "Funil de Recorrência de Depósito", para não colidir de nome com a aba
> nova — são coisas diferentes.

> **Atualização (2026-08-10, Ithalo):** este pacote originalmente pedia uma
> credencial fixa de usuário/senha do Postgres, compartilhada pelo Jonatas.
> Trocado para autenticar com o **token IAM da AWS do próprio usuário que
> roda o app** — mesma identidade usada no acesso pessoal ao `trad_prd`
> (ver seu manual de acesso ao banco). Vantagens: nada de senha compartilhada
> entre pessoas, tudo fica registrado no seu nome, e o acesso é revogado na
> hora se sua chave AWS for desativada. Se outra pessoa for rodar este app,
> ela usa a própria identidade AWS — não a sua.
>
> **Atualização (2026-08-10):** movido de `~/Downloads/export-backoffice/`
> para dentro do repositório (`tools/dashboard-tradicional/`), no mesmo
> padrão do `tools/radar-produto/` — para não depender de uma pasta solta
> fora do projeto.

---

## Passo 1 — Pré-requisitos (uma vez só)

- AWS CLI instalado e configurado com um profile que tenha acesso de leitura
  ao `trad_prd` (ver seu manual de acesso pessoal ao banco — mesmo profile
  usado para `psql`/`trad-prd`).
- Certificado SSL da AWS baixado:
  ```bash
  curl -sS -o "$HOME/global-bundle.pem" https://truststore.pki.rds.amazonaws.com/global/global-bundle.pem
  ```

## Passo 2 — Instale as dependências (num virtualenv, não no Python do sistema)

```bash
cd tools/dashboard-tradicional   # a partir da raiz do pm-loadout
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Passo 3 — Configure as variáveis de ambiente (opcional)

O app já vem com os valores corretos como padrão (host do `trad_prd`, banco,
usuário `ithalo_mendes`, profile `trad-prd-ithalo_mendes`, região
`us-east-1`). Só defina algo abaixo se precisar sobrescrever:

```bash
export DB_HOST="..."          # padrão: cluster read-only do trad_prd
export DB_PORT=5432
export DB_NAME="trad_prd"
export DB_USER="ithalo_mendes"        # deve ser o mesmo usuário IAM/DB do seu profile
export AWS_PROFILE="trad-prd-ithalo_mendes"
export AWS_REGION="us-east-1"
export SSL_ROOT_CERT="$HOME/global-bundle.pem"
export PORT=5051              # opcional — porta em que o dashboard vai responder
```

Nunca escreva credencial nenhuma direto em `geral_app.py` nem faça commit
de nada disso em repositório.

## Passo 4 — Rode

```bash
source .venv/bin/activate   # se ainda não estiver ativo
python3 geral_app.py
```

O app gera um token IAM novo automaticamente a cada ~10 minutos (o token da
AWS vale 15min) — não precisa fazer nada manual pra manter a sessão viva.

## Passo 5 — Acesse

```
http://localhost:5051
```
(ou a porta definida em `PORT`)

---

## Problemas comuns

| Sintoma | Causa provável |
|---|---|
| `Certificado SSL não encontrado em ...` | Rode o comando `curl` do Passo 1 pra baixar o `global-bundle.pem`. |
| Erro do `aws rds generate-db-auth-token` no log | Profile AWS não configurado ou expirado — rode `aws sts get-caller-identity --profile trad-prd-ithalo_mendes` pra confirmar. |
| Timeout / connection refused ao conectar no banco | O RDS provavelmente só aceita conexão de dentro da VPN/rede interna — confirmar com infra. |
| `PAM authentication failed` / `password authentication failed` | Token expirado no meio de uma conexão muito longa, ou usuário do banco não bate com o profile IAM — confirmar `DB_USER` = usuário IAM correto. |

## O que tem neste pacote

- `geral_app.py` — backend Flask com as rotas de Geral, Turnover e Funil de
  Aquisição (funil de cadastro por flags de estado, funil de recorrência
  FTD→2º/3º/.../7º+ depósito, funil de jornada granular de cadastro em 13
  passos + ranking de perdas + sinais de atrito + tempo entre passos, GGR/NGR,
  tráfego pago, taxonomia de frente por btag).
- `dashboard.html` — frontend das três abas (JS puro, Chart.js via CDN).
- `requirements.txt` — dependências Python (`flask`, `psycopg2-binary`).
- `.venv/` — virtualenv local (não versionar).

O banco é **somente leitura**. Não há rota de escrita em lugar nenhum do
código.

Este é um recorte de um dashboard pessoal maior — as abas Novos, Tráfego
Pago e Coorte foram removidas de propósito, não fazem parte desta entrega.
Se precisar de alguma métrica ou rota que não está aqui, é só pedir pro
Jonatas (jonatas.souza@tradicional.bet.br).
