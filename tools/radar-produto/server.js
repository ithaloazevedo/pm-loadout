"use strict";

const http = require("node:http");
const fs = require("node:fs");
const path = require("node:path");

const PORT = process.env.PORT || 4173;
const CLICKUP_API = "https://api.clickup.com/api/v2";
const CLICKUP_API_V3 = "https://api.clickup.com/api/v3";
const WORKSPACE_ID = "9006076935"; // Vertical Tech workspace ("team" in ClickUp API v2 terms)
const SPACE_ID = "90114055709"; // Vertical Tech space

// Doc do ClickUp onde o report diário é publicado (páginas por squad + Resumo
// Executivo). Criado manualmente pelo Ithalo: app.clickup.com/9006076935/docs/8ccvn07-68891
const REPORT_DOC_ID = "8ccvn07-68891";

// Squad -> underlying ClickUp lists. Mudança estrutural de 2026-09-10: o folder
// Discovery & Design (e a lista compartilhada 901114029780) foi removido do
// ClickUp — descoberta agora é uma faixa de status dentro do próprio Backlog de
// cada squad, não mais uma lista separada. A entrada "discovery" que existia
// aqui foi removida porque a lista não existe mais (ver knowledge/domains/processo.md).
// Plataforma e Backoffice também migraram para Sprint Folders nativos do ClickUp
// (Plataforma: Sprint Folder 90118303225, sprint ativa 901114417832; Backoffice:
// Sprint Folder 90118303239, sprint ativa 901115365054) — Produto ainda não migrou.
// TODO: adicionar categoria de Sprint ativa quando o dashboard for revisado.
const SQUADS = {
  plataforma: { label: "Plataforma", listIds: ["901114029784", "901114029785"] },
  backoffice: { label: "Backoffice & Integração", listIds: ["901114029782", "901114029783"] },
  produto: { label: "Produto", listIds: ["901114029786", "901114029876"] }
};

loadEnvFile(path.join(__dirname, ".env"));
const TOKEN = process.env.CLICKUP_API_TOKEN || "";

function loadEnvFile(filePath) {
  if (!fs.existsSync(filePath)) return;
  const lines = fs.readFileSync(filePath, "utf8").split("\n");
  for (const line of lines) {
    const trimmed = line.trim();
    if (!trimmed || trimmed.startsWith("#")) continue;
    const idx = trimmed.indexOf("=");
    if (idx === -1) continue;
    const key = trimmed.slice(0, idx).trim();
    const value = trimmed.slice(idx + 1).trim().replace(/^["']|["']$/g, "");
    if (key && process.env[key] === undefined) process.env[key] = value;
  }
}

function sleep(ms) { return new Promise(function (resolve) { setTimeout(resolve, ms); }); }

function doFetchOnce(url, options) {
  if (!TOKEN) {
    return Promise.reject(new HttpError(500, "CLICKUP_API_TOKEN não configurado. Copie .env.example para .env e cole seu token pessoal do ClickUp."));
  }
  return fetch(url, Object.assign({
    headers: Object.assign({ Authorization: TOKEN, "Content-Type": "application/json" }, (options && options.headers) || {})
  }, options)).then(function (res) {
    return res.text().then(function (text) {
      let body;
      try { body = text ? JSON.parse(text) : {}; } catch (e) { body = { raw: text }; }
      if (!res.ok) {
        throw new HttpError(res.status, (body && (body.err || body.error)) || ("ClickUp respondeu " + res.status));
      }
      return body;
    });
  });
}
// A API v3 (Docs) do ClickUp já mostrou 500 intermitente em uso real (não é
// erro do nosso lado) — uma retentativa única com pequeno atraso é suficiente
// pelo que observamos.
function doFetch(url, options) {
  return doFetchOnce(url, options).catch(function (err) {
    if (err instanceof HttpError && err.status >= 500) {
      return sleep(800).then(function () { return doFetchOnce(url, options); });
    }
    throw err;
  });
}
function clickupFetch(pathAndQuery, options) { return doFetch(CLICKUP_API + pathAndQuery, options); }
function clickupFetchV3(pathAndQuery, options) { return doFetch(CLICKUP_API_V3 + pathAndQuery, options); }

class HttpError extends Error {
  constructor(status, message) { super(message); this.status = status; }
}

function normalizeTask(t) {
  return {
    id: t.id,
    custom_id: t.custom_id || null,
    name: t.name,
    status: t.status && t.status.status,
    url: t.url,
    priority: priorityToText(t.priority),
    assignees: (t.assignees || []).map(function (a) { return { id: a.id, username: a.username }; }),
    tags: (t.tags || []).map(function (tg) { return tg.name; }),
    due_date: t.due_date || null,
    date_closed: t.date_closed || null,
    date_updated: t.date_updated || null,
    date_created: t.date_created || null,
    list: t.list ? { id: t.list.id, name: t.list.name } : null,
    solicitante: extractSolicitante(t.custom_fields),
    parent: t.parent || null
  };
}

function extractSolicitante(customFields) {
  const f = (customFields || []).filter(function (cf) { return cf.name === "Solicitante" && cf.type === "users"; })[0];
  if (!f || f.value === undefined || f.value === null) return null;
  const arr = Array.isArray(f.value) ? f.value : [f.value];
  const names = arr.map(function (u) { return u && (u.username || u.email); }).filter(Boolean);
  return names.length ? { id: String(arr[0].id), username: names[0] } : null;
}

function priorityToText(p) {
  if (!p) return null;
  const n = typeof p === "object" ? parseInt(p.id || p.priority, 10) : parseInt(p, 10);
  return { 1: "urgent", 2: "high", 3: "normal", 4: "low" }[n] || null;
}
function priorityToNumber(text) {
  if (!text || text === "none") return null;
  return { urgent: 1, high: 2, normal: 3, low: 4 }[text] || null;
}

// A API do ClickUp pagina a 100 tarefas por página e não avisa quando corta —
// sem este loop, `include_closed=true` num board com muito histórico fechado
// descarta silenciosamente tudo que passa da primeira página (confirmado
// 18/08/2026: Execução de Plataforma/Backoffice tinham 291/149 tarefas reais
// contra as 100 que a chamada sem paginação devolvia).
function fetchListTasksAllPages(listId, includeClosed) {
  function loop(page, acc) {
    const qs = "?include_closed=" + (includeClosed ? "true" : "false") + "&subtasks=true&page=" + page;
    return clickupFetch("/list/" + listId + "/task" + qs).then(function (body) {
      const tasks = body.tasks || [];
      const next = acc.concat(tasks);
      if (body.last_page || tasks.length === 0 || page > 50) return next;
      return loop(page + 1, next);
    });
  }
  return loop(0, []);
}

function fetchSquadTasks(squadKey, includeClosed) {
  const squad = SQUADS[squadKey];
  if (!squad) return Promise.reject(new HttpError(404, "Squad desconhecido: " + squadKey));
  return Promise.all(squad.listIds.map(function (listId) {
    return fetchListTasksAllPages(listId, includeClosed);
  })).then(function (lists) {
    return lists.reduce(function (acc, l) { return acc.concat(l); }, []).map(normalizeTask);
  });
}

function fetchAvailableStatuses(listId) {
  return clickupFetch("/list/" + listId)
    .then(function (list) {
      if (Array.isArray(list.statuses) && list.statuses.length) return list.statuses;
      const folderId = list.folder && list.folder.id;
      if (!folderId) return [];
      return clickupFetch("/folder/" + folderId).then(function (folder) {
        return Array.isArray(folder.statuses) ? folder.statuses : [];
      });
    })
    .then(function (statuses) {
      if (statuses.length) return statuses;
      return clickupFetch("/space/" + SPACE_ID).then(function (space) {
        return Array.isArray(space.statuses) ? space.statuses : [];
      });
    })
    .then(function (statuses) { return statuses.map(function (s) { return s.status; }); })
    .catch(function () { return []; });
}

function fetchTaskDetail(taskId) {
  return clickupFetch("/task/" + taskId + "?custom_fields=true").then(function (t) {
    const listId = t.list && t.list.id;
    return (listId ? fetchAvailableStatuses(listId) : Promise.resolve([])).then(function (statuses) {
      return {
        id: t.id,
        name: t.name,
        status: t.status && t.status.status,
        available_statuses: statuses,
        priority: priorityToText(t.priority),
        due_date: t.due_date || null,
        assignees: (t.assignees || []).map(function (a) { return { id: a.id, username: a.username }; }),
        list: t.list ? { id: t.list.id, name: t.list.name } : null,
        folder: t.folder ? { id: t.folder.id, name: t.folder.name } : null,
        task_type: (!t.custom_item_id) ? "Tarefa" : ("Tipo personalizado #" + t.custom_item_id),
        custom_fields: (t.custom_fields || []).map(function (f) {
          return { id: f.id, name: f.name, type: f.type, type_config: f.type_config, value: f.value };
        }),
        url: t.url
      };
    });
  });
}

function updateTask(taskId, patch) {
  const body = {};
  if (patch.status !== undefined) body.status = patch.status;
  if (patch.priority !== undefined) body.priority = priorityToNumber(patch.priority);
  if (patch.due_date !== undefined) {
    body.due_date = patch.due_date === "none" ? null : new Date(patch.due_date + "T12:00:00").getTime();
  }
  // Reatribui a tarefa-pai (associar/mover para outro Épico). A API do ClickUp
  // não permite zerar o parent de uma subtarefa existente (virar tarefa solta de
  // novo) — só reatribuir para outro id de tarefa válido.
  if (patch.parent !== undefined && patch.parent !== null) body.parent = patch.parent;
  return clickupFetch("/task/" + taskId, { method: "PUT", body: JSON.stringify(body) }).then(function () {
    if (patch.assignees && (patch.assignees.add || patch.assignees.rem)) {
      return clickupFetch("/task/" + taskId, { method: "PUT", body: JSON.stringify({ assignees: patch.assignees }) });
    }
  });
}

// ---------- publicação do report diário no Doc do ClickUp ----------
function fetchDocPageTree() {
  // Cuidado: `max_page_depth=-1` (documentado como "sem limite") quebra este
  // endpoint no lado do ClickUp e retorna 500 — confirmado manualmente.
  // Omitir o parâmetro já retorna a árvore completa com subpáginas aninhadas.
  return clickupFetchV3("/workspaces/" + WORKSPACE_ID + "/docs/" + REPORT_DOC_ID + "/pages?content_format=text/plain")
    .then(function (body) { return Array.isArray(body) ? body : (body.pages || []); });
}

function findPageByName(pages, name) {
  for (let i = 0; i < pages.length; i++) if (pages[i].name === name) return pages[i];
  return null;
}

function createDocPage(opts) {
  const body = { name: opts.name || "", content: opts.content || "", content_format: "text/md" };
  if (opts.parentPageId) body.parent_page_id = opts.parentPageId;
  if (opts.subTitle) body.sub_title = opts.subTitle;
  return clickupFetchV3("/workspaces/" + WORKSPACE_ID + "/docs/" + REPORT_DOC_ID + "/pages", {
    method: "POST", body: JSON.stringify(body)
  });
}

function updateDocPage(pageId, opts) {
  const body = { content: opts.content, content_format: "text/md", content_edit_mode: "replace" };
  if (opts.name) body.name = opts.name;
  if (opts.subTitle) body.sub_title = opts.subTitle;
  return clickupFetchV3("/workspaces/" + WORKSPACE_ID + "/docs/" + REPORT_DOC_ID + "/pages/" + pageId, {
    method: "PUT", body: JSON.stringify(body)
  });
}

// Publica (cria ou atualiza) a subpágina do dia sob a página de topo
// `topPageName` — cria a página de topo também, se ainda não existir (ex.: a
// primeira vez que "Resumo Executivo — PAM" for gerado).
function publishReportPage(topPageName, dayLabel, content, subTitle) {
  return fetchDocPageTree().then(function (pages) {
    const topPage = findPageByName(pages, topPageName);
    function resolveDay(topPageId, existingChildren) {
      const existingDay = (existingChildren || []).filter(function (p) { return p.name === dayLabel; })[0];
      if (existingDay) {
        return updateDocPage(existingDay.id, { content: content, subTitle: subTitle })
          .then(function () { return { id: existingDay.id, created: false }; });
      }
      return createDocPage({ name: dayLabel, parentPageId: topPageId, content: content, subTitle: subTitle })
        .then(function (p) { return { id: p.id, created: true }; });
    }
    if (topPage) return resolveDay(topPage.id, topPage.pages);
    return createDocPage({ name: topPageName }).then(function (p) { return resolveDay(p.id, []); });
  }).then(function (result) {
    return Object.assign({ url: "https://app.clickup.com/" + WORKSPACE_ID + "/docs/" + REPORT_DOC_ID + "/" + result.id }, result);
  });
}

function fetchMembers() {
  return clickupFetch("/team").then(function (body) {
    const team = (body.teams || []).filter(function (t) { return t.id === WORKSPACE_ID; })[0] || (body.teams || [])[0];
    return (team ? team.members : []).map(function (m) {
      return { id: m.user.id, username: m.user.username || m.user.email || ("Usuário " + m.user.id) };
    });
  });
}

// ---------- coleta mecanizada para o update diário por pessoa ----------
// Mesmo princípio do report-semanal do claude-os: a coleta roda aqui, contra a
// API REST do ClickUp, e não como uma sequência de chamadas MCP feitas por um
// agente. O agente/LLM recebe só o recorte já filtrado do dia e faz apenas a
// síntese narrativa (Feito/Pendente/Pontos de atenção/Impedimentos/Próximos
// passos) — a parte que de fato exige leitura interpretativa.

// SP não observa horário de verão desde 2019 — mesmo offset fixo do weekly_report.py.
const SP_OFFSET_MS = 3 * 60 * 60 * 1000;

function localDayKey(epochMs) {
  const d = new Date(epochMs - SP_OFFSET_MS);
  return d.getUTCFullYear() + "-" + String(d.getUTCMonth() + 1).padStart(2, "0") + "-" + String(d.getUTCDate()).padStart(2, "0");
}
function sameLocalDay(epochMsStrOrNum, targetDateStr) {
  if (!epochMsStrOrNum) return false;
  const ms = typeof epochMsStrOrNum === "string" ? parseInt(epochMsStrOrNum, 10) : epochMsStrOrNum;
  if (!ms || Number.isNaN(ms)) return false;
  return localDayKey(ms) === targetDateStr;
}

// Roda até `limit` promessas por vez — a API do ClickUp já mostrou rate limit
// sob rajada de chamadas concorrentes (é o problema que esta coleta existe
// para evitar do lado do agente; não faz sentido recriá-lo aqui do lado do script).
function mapLimit(items, limit, fn) {
  const results = new Array(items.length);
  let next = 0;
  function worker() {
    const i = next++;
    if (i >= items.length) return Promise.resolve();
    return Promise.resolve(fn(items[i], i)).then(function (r) { results[i] = r; return worker(); });
  }
  const workers = [];
  for (let w = 0; w < Math.min(limit, items.length); w++) workers.push(worker());
  return Promise.all(workers).then(function () { return results; });
}

function fetchTaskComments(taskId) {
  return clickupFetch("/task/" + taskId + "/comment")
    .then(function (body) {
      return (body.comments || []).map(function (c) {
        return { date: c.date || null, user: (c.user && (c.user.username || c.user.email)) || null, text: c.comment_text || "" };
      });
    })
    .catch(function () { return null; }); // null = "não consegui buscar", diferente de "sem comentários" (lista vazia)
}

function fetchTaskStatusHistory(taskId) {
  return clickupFetch("/task/" + taskId + "/time_in_status")
    .then(function (body) {
      const history = (body.status_history || []).map(function (s) {
        return { status: s.status, since: s.total_time && s.total_time.since, type: s.type || null };
      });
      const current = body.current_status && { status: body.current_status.status, since: body.current_status.total_time && body.current_status.total_time.since };
      return { current: current || null, history: history };
    })
    .catch(function () { return null; });
}

// Para cada squad pedido, busca as tarefas (inclusive fechadas) e filtra pra
// quem teve `date_closed` ou `date_updated` caindo no dia-alvo — o mesmo tipo
// de proxy que o weekly_report.py usa (não existe log de atividade bruto por
// data na API do ClickUp). Só para esse recorte (tipicamente dezenas, não
// centenas de tarefas) é que comentários e histórico de status são buscados.
function fetchDailyActivity(squadKeys, targetDateStr) {
  return Promise.all(squadKeys.map(function (key) {
    const squad = SQUADS[key];
    if (!squad) return Promise.reject(new HttpError(404, "Squad desconhecido: " + key));
    return fetchSquadTasks(key, true).then(function (tasks) {
      return tasks
        .filter(function (t) { return sameLocalDay(t.date_closed, targetDateStr) || sameLocalDay(t.date_updated, targetDateStr); })
        .map(function (t) { return Object.assign({ squad: squad.label }, t); });
    });
  })).then(function (lists) {
    const flat = lists.reduce(function (acc, l) { return acc.concat(l); }, []);
    // Uma tarefa pode existir em duas squads (ex.: listas compartilhadas) — dedupe por id.
    const seen = {};
    const tasks = flat.filter(function (t) { return seen[t.id] ? false : (seen[t.id] = true); });
    return mapLimit(tasks, 4, function (t) {
      return Promise.all([fetchTaskComments(t.id), fetchTaskStatusHistory(t.id)]).then(function (r) {
        const allComments = r[0];
        return Object.assign({}, t, {
          comments: allComments === null ? null : allComments.filter(function (c) { return sameLocalDay(c.date, targetDateStr); }),
          status_history: r[1]
        });
      });
    });
  }).then(function (tasks) { return { date: targetDateStr, tasks: tasks }; });
}

// ---------- HTTP plumbing ----------
const MIME = { ".html": "text/html", ".js": "text/javascript", ".css": "text/css" };
const PUBLIC_DIR = path.join(__dirname, "public");

function sendJson(res, status, data) {
  res.writeHead(status, { "Content-Type": "application/json; charset=utf-8" });
  res.end(JSON.stringify(data));
}

function serveStatic(req, res) {
  let filePath = path.join(PUBLIC_DIR, req.url === "/" ? "/index.html" : req.url);
  if (!filePath.startsWith(PUBLIC_DIR)) { res.writeHead(403); res.end("Forbidden"); return; }
  fs.readFile(filePath, function (err, data) {
    if (err) { res.writeHead(404); res.end("Not found"); return; }
    res.writeHead(200, { "Content-Type": MIME[path.extname(filePath)] || "application/octet-stream" });
    res.end(data);
  });
}

const server = http.createServer(function (req, res) {
  const url = new URL(req.url, "http://localhost");
  const parts = url.pathname.split("/").filter(Boolean);

  if (parts[0] !== "api") return serveStatic(req, res);

  let promise;
  if (req.method === "GET" && parts[1] === "tasks" && parts[2]) {
    promise = fetchSquadTasks(parts[2], url.searchParams.get("include_closed") === "true").then(function (tasks) { return { tasks: tasks }; });
  } else if (req.method === "GET" && parts[1] === "task" && parts[2] && parts[3] === "comments") {
    // Checado antes da rota genérica de detalhe (abaixo) — senão "task/:id/comments"
    // também bateria em "parts[1]==='task' && parts[2]" e nunca chegaria aqui.
    promise = fetchTaskComments(parts[2]).then(function (comments) { return { comments: comments }; });
  } else if (req.method === "GET" && parts[1] === "task" && parts[2]) {
    promise = fetchTaskDetail(parts[2]);
  } else if (req.method === "PUT" && parts[1] === "task" && parts[2]) {
    promise = readBody(req).then(function (body) { return updateTask(parts[2], JSON.parse(body || "{}")); }).then(function () { return { ok: true }; });
  } else if (req.method === "GET" && parts[1] === "members") {
    promise = fetchMembers().then(function (members) { return { members: members }; });
  } else if (req.method === "GET" && parts[1] === "daily-activity") {
    const squadsParam = (url.searchParams.get("squads") || "").split(",").map(function (s) { return s.trim(); }).filter(Boolean);
    const dateParam = url.searchParams.get("date") || localDayKey(Date.now());
    if (!squadsParam.length) {
      promise = Promise.reject(new HttpError(400, "Parâmetro squads é obrigatório (ex.: ?squads=plataforma,backoffice)."));
    } else if (!/^\d{4}-\d{2}-\d{2}$/.test(dateParam)) {
      promise = Promise.reject(new HttpError(400, "Parâmetro date deve estar no formato YYYY-MM-DD."));
    } else {
      promise = fetchDailyActivity(squadsParam, dateParam);
    }
  } else if (req.method === "POST" && parts[1] === "report-doc" && parts[2] === "page") {
    promise = readBody(req).then(function (raw) {
      const b = JSON.parse(raw || "{}");
      if (!b.topPageName || !b.dayLabel || typeof b.content !== "string") {
        throw new HttpError(400, "topPageName, dayLabel e content são obrigatórios.");
      }
      return publishReportPage(b.topPageName, b.dayLabel, b.content, b.subTitle);
    });
  } else {
    sendJson(res, 404, { error: "Rota não encontrada" });
    return;
  }

  promise.then(function (data) { sendJson(res, 200, data); }).catch(function (err) {
    sendJson(res, err.status || 500, { error: err.message || "Erro inesperado" });
  });
});

function readBody(req) {
  return new Promise(function (resolve, reject) {
    let chunks = "";
    req.on("data", function (c) { chunks += c; });
    req.on("end", function () { resolve(chunks); });
    req.on("error", reject);
  });
}

server.listen(PORT, "127.0.0.1", function () {
  console.log("Radar de Produto rodando em http://localhost:" + PORT);
  if (!TOKEN) console.log("Aviso: CLICKUP_API_TOKEN não configurado — copie .env.example para .env e cole seu token.");
});
