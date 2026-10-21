<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-20
-->

# E202 — protocol, declared before any page was fetched

## The question this inherits

E162 closed the deterministic repairer *as written*: on 27 real pages a
repairer forbidden to invent text eliminated **0 of 125** AA-tagged axe
instances, and its §4 measured why the denominator looks the way it does —
**90 of those 125 instances (72.0%) are one syntax highlighter's per-line
anchors**, and 92 of 125 (73.6%) aim at machine-generated anchors no user
navigates to. Those anchors have the shape

```html
<a id="__codelineno-24-1" name="__codelineno-24-1" href="#__codelineno-24-1"></a>
```

— empty, pointing at themselves, emitted by `pymdownx.highlight` when
`anchor_linenums` is on. axe calls them `link-name` violations. E162 could not
touch them without inventing a name, so it did not.

**Question.** Can the dominant class be eliminated by a *deterministic,
invention-free* rewrite of the anchor element that keeps its line-permalink
target, and does the rewrite survive an independent oracle on a population
chosen without reference to this question?

**Why this is worth one experiment.** Every published accessibility number on
docs pages is computed on a denominator that is mostly this plumbing (E162 §4).
If the plumbing can be removed by a mechanical rewrite that invents nothing and
loses no deep link, the unfiltered score stops lying for free. If it cannot,
the honest answer is that the only remedy is the build configuration, and the
rewrite route closes.

## What is new here, and what is not

Not new, reused unchanged: axe-core 4.14.0 running in jsdom with page scripts
not executed, the round-trip-through-the-serializer cost every arm pays, the
fabrication set (`visibleText` before vs after), and the gate discipline
(`analyze.js` computes verdicts from recorded bytes against the thresholds
below).

New: a **fresh population** fetched for this experiment, a **rewrite arm**
(E162 never modified the DOM in place for this class), and **two declared
baselines** rather than none.

## Population, declared before fetching

A targeted population, not a prevalence population: *given that these pages
carry the highlighter's anchors, what does the rewrite do to the oracle's
verdict.* Selection is mechanical and runs in this fixed order:

> **Query A.** `GET https://api.github.com/search/repositories?q=topic:mkdocs&sort=stars&order=desc&per_page=50`
> (unauthenticated, one request). Store the raw response as
> `raw/repo-search-A.json`. Take each returned `homepage` that is an `http(s)`
> URL, in response order, deduplicated by host; fetch each with a plain GET,
> 20 s timeout, one retry; store body and status.
> **Query B** runs **only if** fewer than 12 fetched pages qualify after A:
> `q=topic:mkdocs-material&sort=stars&order=desc&per_page=50`, stored as
> `raw/repo-search-B.json`, same handling. No other query, ever.
>
> A page **qualifies** if its stored HTML contains `__codelineno` or
> `anchor_linenums`. For each qualifying host, fetch at most **two** further
> same-host pages: the first two links in document order whose `href` path
> matches `/guide|tutorial|usage|example|getting-started|user-guide/i`.
> Qualifying sub-pages join the population; the rule never changes after a
> number is seen.

Target **≥ 12 qualifying pages across ≥ 6 hosts** (G4). If fewer qualify, the
count obtained is reported and no threshold is moved. Pages are never replaced
after any finding is seen; every fetched body and its sha256 goes in
`corpus-manifest.json` before any arm exists.

## Arms, declared before fetching

| Arm | What it does | What it must not do |
|---|---|---|
| **0** | the fetched page, round-tripped through the serializer (control) | — |
| **1 — candidate** | every element that is a link (or has an `href`) whose href fragment equals its own `id`/`name` **and whose text content is empty** becomes `<span id="…"></span>`: the target survives, the link semantics go, **no text and no attribute value is invented** | invent a name; drop the `id` |
| **2 — strongest available baseline** | inject `<style>`: `a[id^="__codelineno"],a[name^="__codelineno"],a[href=""]{visibility:hidden}` — the mitigation the upstream projects document | change the DOM |
| **3 — upstream config, simulated** | delete those anchor elements, i.e. `anchor_linenums: false` after the fact | claim it is free: it destroys the permalink target, and that loss is counted |

Arm 1's transform is applied to *all* empty self-links, not only
`__codelineno` ones, so the two empty `<a href="">` E162 found are in scope.

## Controls, declared before measurement

- **K1 — does the oracle see CSS at all?** On a committed fixture page
  (`fixtures/k1.html`) holding one empty self-link inside the arm-2 rule and one
  bare on the same page: the bare one must be reported as `link-name` (else the
  oracle is blind to this class and **nothing here is evaluable**), and the
  CSS-hidden one must not be reported. If axe reports the hidden one anyway,
  **arm 2 is `not evaluable` on this oracle** and no arm-1-vs-arm-2 comparison
  is made; that is a ceiling on jsdom, reported as such.
- **K2 — fabrication.** After each arm, the set of visible/attributed strings
  must be a superset of arm 0's with **nothing added**. Any added string is a
  fabrication and fails G2 by itself, whatever the other numbers say.
- **K3 — target survival.** After arm 1, every rewritten fragment must resolve:
  `document.getElementById(id)` (or a `[name=]` lookup) must find a node for
  100% of them. Arm 3's lost targets are counted the same way.

## Gates, declared before fetching

| Gate | Declared | Meaning |
|---|---|---|
| **G0 oracle validity** | axe completes on ≥ 90% of fetched pages; ≥ 8 qualifying pages hold ≥ 1 AA-tagged instance | the instrument works here |
| **G4 population** | ≥ 12 qualifying pages across ≥ 6 hosts | the finding is not one site |
| **G1 elimination (the candidate gate)** | arm 1 eliminates ≥ **90%** of AA-tagged instances whose axe target is an empty self-link, measured on every qualifying page | the rewrite removes the class |
| **G2 no fabrication** | **0** added strings (K2), on every arm and every page | it invents nothing |
| **G3 no regression** | arm 1 introduces **no new rule id** and **no page's total AA count increases** | it does not trade one violation for another |
| **G5 target survival** | arm 1 keeps **100%** of rewritten targets resolvable (K3) | the line permalink still works |
| **D — demand** | ≥ **3** independent public reports naming this class survive re-checking under capture | someone would want the fix |

**Kill gate.** **G1 < 60%, or G2 > 0, or G3 violated, or G5 < 100%** — any of
these fires and the rewrite route is closed: the honest conclusion is that the
remedy lives in the build configuration (`anchor_linenums: false`, or authored
text inside the anchor), and arm 3's lost-target count is the price of that
route.

**Baseline dominance, declared now.** If K1 passes **and** arm 2 eliminates as
much of the class as arm 1 does, then arm 1 is **dominated** — the CSS route
changes nothing in the DOM, loses no target and needs no migration — and this
experiment's answer is a negative one about the rewrite, whatever G1 says.
Arm 1's only claim to preference is that it works where the stylesheet is not
shipped (a raw HTML export, a pasted fragment, a renderer that drops `<style>`),
which is a scope statement, not a score.

**Gate honesty.** G0 and G4 are about instrument and population. G2 and G5 are
mechanical and cannot be argued. G1 and G3 are the claim. D is measured before
the build so a wanted-looking result cannot buy its own demand.

## What this experiment cannot decide

- **Real-browser behaviour.** jsdom performs no layout and no navigation, so
  whether a line permalink still *scrolls* is asserted from target survival,
  not measured.
- **Assistive-technology outcomes.** `link-name` eliminated is a rule verdict,
  not a screen-reader measurement (E162's ceiling, unchanged).
- **Prevalence.** A `topic:mkdocs` sample says nothing about how common the
  pattern is on the web; the qualifying rate of the harvest is reported as a
  property of the query, not of the web.
- **Demand beyond the declared bar.** D is three public reports, not users.

## Prior art and demand

Probed and recorded in `PRIOR-ART.md` **before** this protocol's gates were
argued: the upstream mitigation (`anchor_linenums` + `visibility:hidden`), the
projects that already ship a fix, and the reports naming the problem. The
strongest baseline here is theirs, not ours — that is the point of arm 2.
