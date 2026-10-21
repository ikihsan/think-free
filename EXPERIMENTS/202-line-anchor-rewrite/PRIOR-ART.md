<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-20
-->

# E202 — prior art and demand, recorded before the gates were argued

**Declared 2026-10-20 before any gate was computed.** The protocol
([`PROTOCOL.md`](PROTOCOL.md)) requires the upstream mitigation, the projects
that ship a fix, and the reports naming the problem to be probed and recorded
*before* its gates are argued, so a wanted-looking result cannot buy its own
demand. This file is that record.

## 1. Does a post-hoc rewriter or stripper already exist? No.

GitHub repository search for `codelineno` returns **0 repositories**
(`raw/pa-repos-codelineno.json`, `total_count: 0`). No dedicated tool, no
published package, no snippet library exists for rewriting or removing the
anchors after the fact.

## 2. The upstream mitigation, and the projects that ship it

The anchors are emitted by `pymdownx.highlight` when `anchor_linenums` is on.
The mitigation the upstream documentation and the ecosystem use is **CSS
`visibility:hidden` on the empty self-links**, not a DOM rewrite:

```css
a[id^="__codelineno"], a[name^="__codelineno"], a[href=""]{visibility:hidden}
```

That rule is arm 2 of this experiment, declared as the strongest available
baseline before the harvest. The upstream docs page
(`raw/pymdown-highlight-docs.html`, sha256 `b1e61eea…f404`) documents
`anchor_linenums` as the option that produces them; the visibility remedy is
shipped downstream. Search results that name the remedy and its effects:

- `__codelineno visibility` → **7** issues, including
  [`radiusred/codecrew-www#57`](https://github.com/radiusred/codecrew-www/issues/57)
  (empty line-anchor links are invisible keyboard tab stops) and
  [`mkdocs/mkdocs#3690`](https://github.com/mkdocs/mkdocs/issues/3690)
  (anchor validation false positives after the 1.6 upgrade).
- `anchor_linenums accessibility` → **19** issues.
- `"__codelineno" "link-name"` → **9** issues.
- `__codelineno remove` → **53** issues.

Removal is a common **manual** action (53 reports) performed site by site; it is
not a product. Several projects ship a CSS or config fix in their own docs
config (for example `cloudfoundry/docs-bosh`, `syn54x/ferro-orm`,
`zensical/docs`), which is the same remedy as arm 2 or arm 3.

## 3. Demand (gate D): three independent public reports, captured

| report | date | what it names | raw capture (sha256) |
|---|---|---|---|
| [`radiusred/codecrew-www#57`](https://github.com/radiusred/codecrew-www/issues/57) | 2026-09-26 | "every fenced code block … carries empty line-anchor links, each one an invisible keyboard Tab stop"; 77 on one page | `f2f3a3d0…8e9a5f` |
| [`coleam00/mcp-crawl4ai-rag#5`](https://github.com/coleam00/mcp-crawl4ai-rag/issues/5) | 2025-05-08 | "Noisy Anchor Links (`#__codelineno-*`) … Consume Excessive Tokens" in crawled Markdown | `8f9c572e…bbe2` |
| [`gpt-cmdr/ras-commander#462`](https://github.com/gpt-cmdr/ras-commander/issues/462) | 2026-10-01 | "duplicate generated line IDs … (`__span-0-60` and `__codelineno-0-60`)" | `e0aff01a…6a8c` |

Three reports from three unrelated owners and three unrelated sites survive
re-checking under capture (the bodies are stored in `raw/issue-*.json` with the
hashes above). **D = 3 of 3.**

**One honest caveat.** The third report names the *identifier* `__codelineno`
but its complaint is **duplicate** line IDs, not empty anchors; it is a
related-not-identical defect. The first two are directly about empty or noisy
self-links. D is declared as "reports naming this class", so it passes, but it
is not three independent confirmations of the same defect.

## 4. What this means for the experiment

- The **remedy is established**: CSS hiding is the ecosystem's answer, and it
  is already shipped. The rewrite is not a novel remedy.
- **No rewriter exists**, so there is a gap — but a gap is not a candidate, and
  arm 2 is the incumbent this experiment measures against.
- The protocol's declared **baseline-dominance clause** is therefore the
  decisive one: if the CSS route removes as much of the class as the rewrite,
  the rewrite is dominated and the answer is negative about the rewrite
  *whatever G1 says*. That clause is what [`RESULT.md`](RESULT.md) turns on.

## 5. Method and captures

Unauthenticated GitHub REST search, one request per query, recorded raw:

| query | file | sha256 |
|---|---|---|
| `__codelineno visibility` | `raw/pa-codelineno-visibility.json` | `6137e792…e6264` |
| `anchor_linenums accessibility` | `raw/pa-anchor-linenums-a11y.json` | `9e91ee07…3dfb` |
| `"__codelineno" "link-name"` | `raw/pa-linkname-codelineno.json` | `e9762fa3…1941` |
| `__codelineno remove` | `raw/pa-codelineno-remove.json` | `f2b225b3…c183d` |
| repositories `codelineno` | `raw/pa-repos-codelineno.json` | `4af480b8…a5f` |
| pymdown-extensions highlight docs | `raw/pymdown-highlight-docs.html` | `b1e61eea…f404` |

Search answers are the platform's relevance ranking, not a prevalence
measurement; the counts are recorded as what the query returned, which is what
prior art needs and nothing more.
