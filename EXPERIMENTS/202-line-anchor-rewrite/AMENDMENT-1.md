<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-20
-->

# E202 — AMENDMENT-1, declared before any oracle run

**Declared 2026-10-20, after the stage-1 harvest and before axe has run on a
single page of this corpus.** Nothing in `results-*.json` exists yet; there is
no verdict to fit the population to.

## What stage 1 measured, unchanged

The PROTOCOL.md rule (query A, query B only if qualifying < 12, sub-pages only
for hosts whose **root** already qualified) fetched **69 pages, 65 returned
200, and 3 qualify** — `johnthagen.github.io/python-blueprint/`,
`fasthttp.ndugram.dev`, `h4m5t.top/SecNotes`:

| Stage-1 coverage | |
|---|---|
| fetched | 69 (37 after query A, 32 after query B) |
| HTTP 200 | 65 |
| qualifying (`__codelineno` or `anchor_linenums` present) | **3** = 4.6% of 65 |
| distinct qualifying hosts | 3 |

**G4 (≥ 12 qualifying pages across ≥ 6 hosts) cannot be met by this rule**, and
that is a property of the rule, not yet of the web: the rule gates sub-page
fetching on the *root* page qualifying, and a project's root page is its
landing page — it carries no code block to anchor (E163 made the identical
observation about roots). The coverage number above is a result and stays in
the record: **the pattern is on 3 of 65 documentation home pages.**

## The amendment

> **Stage 2.** For every host with an HTTP-200 root page fetched in stage 1 —
> qualifying or not — fetch at most **two** further same-host pages: the first
> two links in document order whose `href` path matches
> `/guide|tutorial|usage|example|getting-started|user-guide/i`, already the
> protocol's sub-page rule, now applied without the qualification gate. Store
> them as stage-2 records with the same sha256 discipline. Qualify them by the
> same content test. The population for every gate is the **union** of stage-1
> and stage-2 qualifying pages, and **both coverage numbers are reported
> separately**.

## Why this is not fitting the population to an answer

1. Selection still depends on nothing but URL structure and the page's own
   bytes; **no axe verdict has been computed on any page of this corpus.**
2. The stage-1 failure is reported first, at full size, in `RESULT.md`, so the
   amendment cannot hide it.
3. The oracle, the arms, the gates, the kill gate and the fabrication set are
   untouched; only the number of pages the rule is allowed to look at changed.

## What would have been cheating (named so it is checkable)

Re-running stage 1 with a broader qualifier (`<pre`, `hl_lines`, `highlight`),
dropping the 3 qualifying pages that came from small personal sites, choosing
sub-page patterns after reading page content, or changing any gate threshold.
None of these happens; if stage 2 still yields < 12 qualifying pages, **G4
fails as declared** and the result is reported on the smaller population.
