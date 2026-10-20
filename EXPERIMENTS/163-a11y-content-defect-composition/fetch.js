#!/usr/bin/env node
// E163 population fetch, arm 2.
//
// The selection rule is PROTOCOL.md's, fixed before any fetch: for each host in
// E162's hashed manifest, take the root page's own links whose path matches
// /(contact|accessib|search|apply|form|report)/i in document order, resolve
// them against the page's base, keep the first two distinct on-host URLs that
// answer 200 to a plain GET.
//
// Every body is written under raw/ with its sha256; raw/ is untracked (the
// manifest is the record, this script is the re-fetch).
const fs = require("fs");
const path = require("path");
const { JSDOM } = require("jsdom");
const crypto = require("crypto");

const HERE = __dirname;
const E162 = path.join(HERE, "..", "162-a11y-deterministic-repair");
const RAW = path.join(HERE, "raw");
const MANIFEST = path.join(HERE, "corpus-manifest.json");
const MATCH = /(contact|accessib|search|apply|form|report)/i;
const PER_HOST = 2;

const sha = (buf) => crypto.createHash("sha256").update(buf).digest("hex");

function readRootManifest() {
  const m = JSON.parse(fs.readFileSync(path.join(E162, "corpus-manifest.json"), "utf8"));
  const pages = Array.isArray(m) ? m : m.pages || [];
  return pages.filter((p) => p.status === 200);
}

function rawName(host, i) {
  return `${String(i).padStart(3, "0")}-${host.replace(/[^a-z0-9]+/gi, "_")}.html`;
}

function candidates(html, baseUrl) {
  const dom = new JSDOM(html, { url: baseUrl });
  const out = [];
  const seen = new Set();
  for (const a of dom.window.document.querySelectorAll("a[href]")) {
    let href = a.getAttribute("href") || "";
    if (!href || /^(mailto:|tel:|javascript:|#)/i.test(href)) continue;
    let u;
    try { u = new URL(href, baseUrl); } catch (e) { continue; }
    if (u.protocol !== "http:" && u.protocol !== "https:") continue;
    if (u.origin !== new URL(baseUrl).origin) continue;
    if (!MATCH.test(u.pathname)) continue;
    const key = u.href.replace(/#.*$/, "");
    if (seen.has(key)) continue;
    seen.add(key);
    out.push(key);
  }
  return out;
}

async function get(url) {
  const res = await fetch(url, {
    headers: { "user-agent": "think-free-e163/1.0 (accessibility composition study; contact: repository owner)" },
    redirect: "follow",
  });
  const buf = Buffer.from(await res.arrayBuffer());
  return { status: res.status, final_url: res.url || url, buf };
}

async function main() {
  fs.mkdirSync(RAW, { recursive: true });
  const roots = readRootManifest();
  const pages = [];
  let n = 0;
  for (const r of roots) {
    const rootFile = path.join(E162, "corpus", `${r.id}.html`);
    if (!fs.existsSync(rootFile)) { console.log(`skip ${r.id}: no stored body`); continue; }
    const html = fs.readFileSync(rootFile, "utf8");
    const cands = candidates(html, r.final_url || r.url).slice(0, 12);
    let kept = 0;
    for (const c of cands) {
      if (kept >= PER_HOST) break;
      let got;
      try { got = await get(c); } catch (e) {
        console.log(`fetch error ${c}: ${String(e).slice(0, 80)}`);
        continue;
      }
      if (got.status !== 200) { console.log(`skip ${c} -> ${got.status}`); continue; }
      const html2 = got.buf.toString("utf8");
      if (!/<html/i.test(html2)) { console.log(`skip ${c}: not html`); continue; }
      n += 1;
      const file = rawName(new URL(got.final_url).host, n);
      fs.writeFileSync(path.join(RAW, file), got.buf);
      pages.push({
        id: `${String(n).padStart(3, "0")}-${sha(got.buf).slice(0, 8)}`,
        frame: r.frame,
        host: new URL(got.final_url).host,
        url: c,
        final_url: got.final_url,
        file: `raw/${file}`,
        bytes: got.buf.length,
        sha256: sha(got.buf),
        from_root: r.id,
      });
      kept += 1;
      console.log(`${pages.length}\t${r.frame}\t${kept}\t${got.final_url}`);
    }
    if (kept < PER_HOST) console.log(`host ${r.host}: ${kept} qualifying page(s)`);
  }
  fs.writeFileSync(MANIFEST, JSON.stringify({
    note: "E163 arm 2. Selection rule in PROTOCOL.md, fixed before fetching. Arm 1 is EXPERIMENTS/162-a11y-deterministic-repair/corpus-manifest.json.",
    roots_considered: roots.length,
    pages,
  }, null, 1) + "\n");
  console.log(`\n${pages.length} pages from ${roots.length} hosts -> ${MANIFEST}`);
}

main().catch((e) => { console.error(e); process.exit(1); });