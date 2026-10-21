#!/usr/bin/env node
// E202 stage 2 — AMENDMENT-1. Same sub-page rule as the protocol, applied to
// every HTTP-200 root instead of only to roots that already qualified.
// Runs before any axe verdict exists; stage-1 records and counts are kept.
const fs = require("fs");
const path = require("path");

const HERE = __dirname;
const MAN = path.join(HERE, "corpus-manifest.json");
const UA = "think-free-research (accessibility research; contact via repository)";
const TIMEOUT_MS = 20000;
const CONCURRENCY = 6;
const SUB_RE = /\/(guide|tutorial|usage|example|getting-started|user-guide)/i;
const sha = (b) => require("crypto").createHash("sha256").update(b).digest("hex");

async function get(url) {
  try {
    const ctrl = new AbortController();
    const timer = setTimeout(() => ctrl.abort(), TIMEOUT_MS);
    const res = await fetch(url, {
      redirect: "follow", signal: ctrl.signal,
      headers: { "User-Agent": UA, "Accept": "text/html,application/xhtml+xml,*/*" },
    });
    const buf = Buffer.from(await res.arrayBuffer());
    clearTimeout(timer);
    return { status: res.status, body: buf };
  } catch (e) {
    return { status: 0, body: Buffer.alloc(0), error: String((e && e.message) || e) };
  }
}

async function mapLimit(items, limit, fn) {
  const out = new Array(items.length);
  let i = 0;
  await Promise.all(new Array(Math.min(limit, items.length)).fill(0).map(async () => {
    while (i < items.length) { const idx = i++; out[idx] = await fn(items[idx], idx); }
  }));
  return out;
}

const qualifies = (b) => { const s = b.toString("utf8"); return s.includes("__codelineno") || s.includes("anchor_linenums"); };

function sameHostLinks(html, host, want) {
  const out = [];
  const re = /<a\b[^>]*\bhref=["']([^"'#][^"']*)["'][^>]*>/gi;
  let m;
  while ((m = re.exec(html))) {
    let abs;
    try { abs = new URL(m[1], "https://" + host); } catch { continue; }
    if (abs.host !== host) continue;
    if (!SUB_RE.test(abs.pathname)) continue;
    if (!out.includes(abs.href)) out.push(abs.href);
    if (out.length >= want) break;
  }
  return out;
}

async function main() {
  const man = JSON.parse(fs.readFileSync(MAN, "utf8"));
  const stage1 = man.stage1 || {
    fetched: man.fetched, http200: man.pages.filter((p) => p.status === 200).length,
    qualifying: man.qualifying, hosts: (man.hosts || []).length,
  };
  const pages = man.pages;
  const have = new Set(pages.map((p) => p.url));
  const roots = pages.filter((p) => p.kind === "root" && p.status === 200);
  const byHost = new Map();
  for (const r of roots) if (!byHost.has(r.host)) byHost.set(r.host, r);

  const targets = [];
  for (const [host, root] of byHost) {
    const html = fs.readFileSync(path.join(HERE, root.file), "utf8");
    for (const u of sameHostLinks(html, host, 2)) {
      if (have.has(u)) continue;
      if (targets.some((t) => t.url === u)) continue;
      have.add(u);
      targets.push({ url: u, host, kind: "sub", repo: root.repo, stage: 2 });
    }
  }
  console.log(`stage 2 targets: ${targets.length}`);

  const added = (await mapLimit(targets, CONCURRENCY, async (t) => {
    const r = await get(t.url);
    const idx = String(pages.length).padStart(3, "0");
    const safe = t.host.replace(/[^a-z0-9.-]/gi, "_");
    const file = `pages/${idx}-${safe}-sub2.html`;
    fs.writeFileSync(path.join(HERE, file), r.body);
    return {
      url: t.url, host: t.host, kind: "sub", stage: 2, repo: t.repo || null,
      status: r.status, file, bytes: r.body.length, sha256: sha(r.body),
      error: r.error || null,
      qualifies: r.status === 200 ? qualifies(r.body) : false,
    };
  })).filter(Boolean);
  pages.push(...added);

  const qualifying = pages.filter((p) => p.qualifies);
  const out = {
    generated_by: man.generated_by,
    rule: man.rule,
    amendment: "EXPERIMENTS/202-line-anchor-rewrite/AMENDMENT-1.md (stage 2)",
    query_A: man.query_A,
    query_B: man.query_B,
    stage1,
    stage2: {
      targets: targets.length, fetched: added.length,
      http200: added.filter((p) => p.status === 200).length,
      qualifying: added.filter((p) => p.qualifies).length,
    },
    fetched: pages.length,
    http200: pages.filter((p) => p.status === 200).length,
    qualifying: qualifying.length,
    hosts: [...new Set(qualifying.map((p) => p.host))],
    pages,
  };
  fs.writeFileSync(MAN, JSON.stringify(out, null, 2) + "\n");
  console.log(`stage1 qualifying=${stage1.qualifying}  stage2 qualifying=${out.stage2.qualifying}  union=${out.qualifying} hosts=${out.hosts.length} fetched=${out.fetched}`);
}

main().catch((e) => { console.error(e); process.exit(1); });
