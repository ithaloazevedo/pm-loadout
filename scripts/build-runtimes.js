#!/usr/bin/env node
'use strict';

/**
 * Gera as partes de .agents/ e .codex/ que não têm adaptação de runtime, a partir da fonte
 * única em .claude/ — ver services/runtime-sync.md.
 *
 * Escopo (deliberadamente restrito — ver knowledge/decisions/2026-08-11-geracao-automatica-runtimes-codex-agents.md):
 *   .claude/agents/*.md                              → .codex/agents/*.toml
 *   .claude/skills/clickup-spec/references/**         → .agents/skills/clickup-spec/references/** (cópia verbatim)
 *
 * Fora do escopo, de propósito: o SKILL.md de topo de cada skill em .claude/skills/ (têm
 * adaptação de runtime legítima para o Codex — não gerar por cima). Não toca em nenhuma outra skill.
 *
 * Uso: node scripts/build-runtimes.js
 */

const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const AGENTS_SRC_DIR = path.join(ROOT, '.claude', 'agents');
const AGENTS_DEST_DIR = path.join(ROOT, '.codex', 'agents');
const REFERENCES_SRC_DIR = path.join(ROOT, '.claude', 'skills', 'clickup-spec', 'references');
const REFERENCES_DEST_DIR = path.join(ROOT, '.agents', 'skills', 'clickup-spec', 'references');

function parseFrontmatter(raw, filePath) {
  const match = raw.match(/^---\r?\n([\s\S]*?)\r?\n---\r?\n?([\s\S]*)$/);
  if (!match) {
    throw new Error(`${filePath}: frontmatter "---...---" não encontrado no início do arquivo`);
  }
  const [, frontmatter, rest] = match;
  const nameMatch = frontmatter.match(/^name:\s*(.+)$/m);
  const descMatch = frontmatter.match(/^description:\s*(.+)$/m);
  if (!nameMatch) throw new Error(`${filePath}: campo "name" não encontrado no frontmatter`);
  if (!descMatch) throw new Error(`${filePath}: campo "description" não encontrado no frontmatter`);
  return {
    name: nameMatch[1].trim(),
    description: descMatch[1].trim(),
    body: rest.replace(/^\r?\n/, ''),
  };
}

function escapeTomlBasicString(value) {
  return value.replace(/\\/g, '\\\\').replace(/"/g, '\\"');
}

function buildAgentToml(filePath) {
  const raw = fs.readFileSync(filePath, 'utf8');
  const { name, description, body } = parseFrontmatter(raw, filePath);

  if (body.includes('"""')) {
    const before = body.slice(0, body.indexOf('"""'));
    const line = before.split('\n').length;
    throw new Error(
      `${filePath}: corpo contém a sequência """ na linha ~${line} do corpo — quebraria a string TOML ` +
        `multi-line ("""..."""). Geração abortada para este arquivo; troque por outra marcação (ex.: \`\`\`) e rode de novo.`
    );
  }

  const trimmedBody = body.replace(/\s+$/, '');
  const toml =
    `name = "${escapeTomlBasicString(name)}"\n` +
    `description = "${escapeTomlBasicString(description)}"\n` +
    `developer_instructions = """\n${trimmedBody}\n"""\n`;

  return { name, toml };
}

function writeIfChanged(destPath, content) {
  const previous = fs.existsSync(destPath) ? fs.readFileSync(destPath) : null;
  const buf = Buffer.isBuffer(content) ? content : Buffer.from(content, 'utf8');
  if (previous !== null && Buffer.compare(previous, buf) === 0) {
    return 'unchanged';
  }
  fs.mkdirSync(path.dirname(destPath), { recursive: true });
  fs.writeFileSync(destPath, buf);
  return previous === null ? 'created' : 'updated';
}

function pruneOrphans(destDir, expectedNames) {
  if (!fs.existsSync(destDir)) return [];
  const removed = [];
  for (const entry of fs.readdirSync(destDir)) {
    if (!expectedNames.has(entry)) {
      fs.rmSync(path.join(destDir, entry), { recursive: true, force: true });
      removed.push(path.join(destDir, entry));
    }
  }
  return removed;
}

function syncAgents() {
  if (!fs.existsSync(AGENTS_SRC_DIR)) {
    throw new Error(`Fonte não encontrada: ${AGENTS_SRC_DIR}`);
  }
  fs.mkdirSync(AGENTS_DEST_DIR, { recursive: true });

  const sourceFiles = fs.readdirSync(AGENTS_SRC_DIR).filter((f) => f.endsWith('.md'));
  const results = { created: [], updated: [], unchanged: [], errors: [] };
  const expected = new Set();

  for (const file of sourceFiles) {
    const srcPath = path.join(AGENTS_SRC_DIR, file);
    try {
      const { name, toml } = buildAgentToml(srcPath);
      const destFile = `${name}.toml`;
      expected.add(destFile);
      const status = writeIfChanged(path.join(AGENTS_DEST_DIR, destFile), toml);
      results[status].push(destFile);
    } catch (err) {
      results.errors.push(err.message);
    }
  }

  results.removed = pruneOrphans(AGENTS_DEST_DIR, expected);
  return results;
}

function collectFiles(dir, base = dir) {
  let files = [];
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      files = files.concat(collectFiles(full, base));
    } else {
      files.push(path.relative(base, full));
    }
  }
  return files;
}

function syncReferences() {
  if (!fs.existsSync(REFERENCES_SRC_DIR)) {
    throw new Error(`Fonte não encontrada: ${REFERENCES_SRC_DIR}`);
  }
  const relFiles = collectFiles(REFERENCES_SRC_DIR);
  const results = { created: [], updated: [], unchanged: [], errors: [] };
  const expected = new Set(relFiles.map((f) => f.split(path.sep)[0]));

  for (const rel of relFiles) {
    const srcPath = path.join(REFERENCES_SRC_DIR, rel);
    const destPath = path.join(REFERENCES_DEST_DIR, rel);
    try {
      const status = writeIfChanged(destPath, fs.readFileSync(srcPath));
      results[status].push(rel);
    } catch (err) {
      results.errors.push(`${srcPath}: ${err.message}`);
    }
  }

  results.removed = pruneOrphans(REFERENCES_DEST_DIR, expected);
  return results;
}

function report(label, result) {
  console.log(`\n${label}`);
  console.log(`  criado: ${result.created.length} | atualizado: ${result.updated.length} | sem mudança: ${result.unchanged.length} | removido (órfão): ${result.removed.length}`);
  for (const f of [...result.created, ...result.updated]) console.log(`    ~ ${f}`);
  for (const f of result.removed) console.log(`    - removido: ${f}`);
  for (const e of result.errors) console.error(`    ERRO: ${e}`);
}

function main() {
  const agentsResult = syncAgents();
  report('.codex/agents/*.toml ← .claude/agents/*.md', agentsResult);

  const refsResult = syncReferences();
  report('.agents/skills/clickup-spec/references/** ← .claude/skills/clickup-spec/references/**', refsResult);

  const hadErrors = agentsResult.errors.length > 0 || refsResult.errors.length > 0;
  if (hadErrors) {
    console.error('\nGeração concluída com erros — revise os arquivos listados acima antes de commitar.');
    process.exit(1);
  }
  console.log('\nOK. Fora deste escopo (fork manual legítimo, não gerado): SKILL.md de topo de cada skill — ver services/runtime-sync.md.');
}

main();
