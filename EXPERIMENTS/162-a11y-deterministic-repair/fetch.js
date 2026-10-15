#!/usr/bin/env node
// Fetch the declared frames in order, one page per site, and hash every byte.
// No page is replaced after a finding is seen: replacement happens only on a
// fetch failure, and the failure is recorded.
const fs = require("fs");
const path = require("path");
const crypto = require("crypto");

const HERE = __dirname;
const OUT = path.join(HERE, "corpus");
const UA = "think-free-e162/1.0 (+accessibility mechanism experiment; contact: repository maintainer)";

async function main() {
  fs.mkdirSync(OUT, { recursive: true });
  const lines = fs.readFileSync(path.join(HERE, "frames.txt"), "utf8").split("\n");
  const wanted = lines
    .map((l) => l.trim())
    .filter((l) => l && !l.startsWith("#"))
    .map((l) => l.split(/\s+/));

  const manifest = { fetched_at: new Date().toISOString(), pages: [], skipped: [] };

  for (const [frame, url] of wanted) {
    const n = manifest.pages.length;
    let res, text, finalUrl = url, status = null;
    try {
      const ctrl = new AbortController();
      const t = setTimeout(() => ctrl.abort(), 25000);
      res = await fetch(url, {
        headers: { "user-agent": UA, accept: "text/html,application/xhtml+xml" },
        redirect: "follow",
        signal: ctrl.signal,
      });
      clearTimeout(t);
      status = res.status;
      finalUrl = res.url || url;
      text = await res.text();
    } catch (err) {
      manifest.skipped.push({ frame, url, reason: String(err && err.message).slice(0, 120) });
      process.stdout.write(`SKIP ${frame} ${url} ${err && err.message}\n`);
      continue;
    }
    const buf = Buffer.from(text, "utf8");
    const html = buf.toString("utf8");
    const id = `${frame}${n}-${crypto.createHash("sha1").update(url).digest("hex").slice(0, 8)}`;
    fs.writeFileSync(path.join(OUT, `${id}.html`), html);
    manifest.pages.push({
      id,
      frame,
      requested_url: url,
      final_url: finalUrl,
      status,
      content_type: res.headers.get("content-type") || "",
      bytes: buf.length,
      sha256: crypto.createHash("sha256").update(buf).digest("hex"),
      file: `corpus/${id}.html`,
    });
    process.stdout.write(`OK   ${id} ${status} ${buf.length}B ${finalUrl}\n`);
  }

  fs.writeFileSync(
    path.join(HERE, "corpus-manifest.json"),
    JSON.stringify(manifest, null, 1) + "\n"
  );
  const byFrame = {};
  for (const p of manifest.pages) byFrame[p.frame] = (byFrame[p.frame] || 0) + 1;
  process.stdout.write(`\n${manifest.pages.length} pages ${JSON.stringify(byFrame)}\n`);
}

main().catch((e) => { console.error(e); process.exit(1); });