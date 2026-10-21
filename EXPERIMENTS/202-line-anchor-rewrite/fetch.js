#!/usr/bin/env node
// E202 population fetch. The selection rule is PROTOCOL.md's, fixed before
// this file existed: one repository search, its homepages in response order,
// then up to two same-host sub-pages per qualifying host.
const fs = require("fs");
const path = require("path");

const HERE = __dirname;
const RAW = path.join(HERE, "raw");
const PAGES = path.join(HERE, "pages");
const UA = "think-free-research (accessibility research; contact via repository)";
const TIMEOUT_MS = 20000;
const CONCURRENCY = 6;
const SUB_RE = /\/(guide|tutorial|usage|example|getting-started|user-guide)/i;

fs.mkdirSync(RAW, { recursive: true });
fs.mkdirSync(PAGES, { recursive: true });

async function get(url) {
  try {
    const ctrl = new AbortController();
    const timer = setTimeout(() => ctrl.abort(), TIMEOUT_MS);
    const res = await fetch(url, {
      redirect: "follow",
      signal: ctrl.signal,
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
  const workers = new Array(Math.min(limit, items.length)).fill(0).map(async () => {
    while (i < items.length) {
      const idx = i++;
      out[idx] = await fn(items[idx], idx);
    }
  });
  await Promise.all(workers);
  return out;
}

function qualifies(buf) {
  const s = buf.toString("utf8");
  return s.includes("__codelineno") || s.includes("anchor_linenums");
}

function homepagesFrom(file) {
  const raw = JSON.parse(fs.readFileSync(path.join(RAW, file), "utf8"));
  const seen = new Set();
  const out = [];
  for (const item of raw.items || []) {
    const hp = item.homepage;
    if (!hp || !/^https?:\/\//i.test(hp)) continue;
    let host;
    try { host = new URL(hp).host; } catch { continue; }
    if (seen.has(host)) continue;
    seen.add(host);
    out.push({ repo: item.full_name, url: hp, host });
  }
  return { total_count: raw.total_count, returned: (raw.items || []).length, homepages: out };
}

function sameHostLinks(html, host) {
  const out = [];
  const re = /<a\b[^>]*\bhref=["']([^"'#][^"']*)["'][^>]*>/gi;
  let m;
  while ((m = re.exec(html))) {
    const href = m[1];
    if (!/^https?:/i.test(href) && !href.startsWith("/")) continue;
    let abs;
    try { abs = new URL(href, "https://" + host); } catch { continue; }
    if (abs.host !== host) continue;
    if (!SUB_RE.test(abs.pathname)) continue;
    if (!out.includes(abs.href)) out.push(abs.href);
    if (out.length >= 2) break;
  }
  return out;
}

async function main() {
  const sha = (b) => require("crypto").createHash("sha256").update(b).digest("hex");
  const records = [];
  const seenUrl = new Set();

  const A = homepagesFrom("search-repoA.json");
  let targets = A.homepages.map((h) => ({ ...h, kind: "root" }));

  async function fetchAll(list) {
    return mapLimit(list, CONCURRENCY, async (t) => {
      if (seenUrl.has(t.url)) return null;
      seenUrl.add(t.url);
      const r = await get(t.url);
      const idx = String(records.length).padStart(3, "0");
      const safe = t.host.replace(/[^a-z0-9.-]/gi, "_");
      const file = `pages/${idx}-${safe}${t.kind === "root" ? "" : "-sub"}.html`;
      fs.writeFileSync(path.join(HERE, file), r.body);
      const rec = {
        url: t.url, host: t.host, kind: t.kind, repo: t.repo || null,
        status: r.status, file, bytes: r.body.length, sha256: sha(r.body),
        error: r.error || null,
        qualifies: r.status === 200 ? qualifies(r.body) : false,
      };
      records.push(rec);
      return rec;
    });
  }

  await fetchAll(targets);
  let qualified = records.filter((r) => r.qualifies);
  console.log(`after query A: fetched=${records.length} qualifying=${qualified.length}`);

  if (qualified.length < 12) {
    if (!fs.existsSync(path.join(RAW, "search-repoB.json"))) {
      const b = await get("https://api.github.com/search/repositories?q=topic:mkdocs-material&sort=stars&order=desc&per_page=50");
      fs.writeFileSync(path.join(RAW, "search-repoB.json"), b.body);
      console.log(`query B status=${b.status}`);
    }
    const B = homepagesFrom("search-repoB.json");
    const have = new Set(records.map((r) => r.url));
    const extra = B.homepages.filter((h) => !have.has(h.url)).map((h) => ({ ...h, kind: "root" }));
    await fetchAll(extra);
    qualified = records.filter((r) => r.qualifies);
    console.log(`after query B: fetched=${records.length} qualifying=${qualified.length}`);
  }

  // up to two same-host sub-pages per qualifying host
  const byHost = new Map();
  for (const r of qualified) if (!byHost.has(r.host)) byHost.set(r.host, r);
  const subs = [];
  for (const [, root] of byHost) {
    const html = fs.readFileSync(path.join(HERE, root.file), "utf8");
    for (const u of sameHostLinks(html, root.host)) {
      if (subs.filter((s) => s.host === root.host).length >= 2) break;
      if (seenUrl.has(u)) continue;
      subs.push({ url: u, host: root.host, kind: "sub", repo: root.repo });
    }
  }
  await fetchAll(subs);
  qualified = records.filter((r) => r.qualifies);

  const manifest = {
    generated_by: "EXPERIMENTS/202-line-anchor-rewrite/fetch.js",
    rule: "PROTOCOL.md population rule (query A, then B only if qualifying < 12)",
    query_A: { file: "raw/search-repoA.json", total_count: A.total_count, returned: A.returned },
    query_B: fs.existsSync(path.join(RAW, "search-repoB.json"))
      ? { file: "raw/search-repoB.json" } : null,
    fetched: records.length,
    qualifying: qualified.length,
    hosts: [...new Set(qualified.map((r) => r.host))],
    pages: records,
  };
  fs.writeFileSync(path.join(HERE, "corpus-manifest.json"), JSON.stringify(manifest, null, 2) + "\n");
  console.log(`wrote corpus-manifest.json: fetched=${records.length} qualifying=${qualified.length} hosts=${manifest.hosts.length}`);
}

main().catch((e) => { console.error(e); process.exit(1); });
