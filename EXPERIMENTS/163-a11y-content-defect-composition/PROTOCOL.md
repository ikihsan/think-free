<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-15
-->

# E163 — protocol, declared before any new page was fetched

## The question this inherits

E162 closed the deterministic repairer *as written*: a table allowed to apply a
repair only where the correct value is readable from the document eliminated
**0 of 125** AA-tagged axe instances. It named what it did not close: **a wider
table**, whose only reachable class is a name derivable from authored text
*somewhere else* in the document rather than on the node.

That leaves exactly one question worth money: **how big is that class?** If it
is a few percent, accessibility remediation is an authoring task and every tool
that promises otherwise is selling a score. If it is a fifth of the real defects,
there is a small, honest, useful program — and its usefulness is not "more
violations fixed", it is **which defects a team should fix first**, which E162
measured is the opposite of what the raw denominator says (92 of 125, 73.6%, were
anchors no user navigates to).

**Question.** With machine-generated elements excluded, what is the composition
of real WCAG-tagged defects, and what share of them has a name derivable from
authored text elsewhere in the document?

## What is new here, and what is not

Not new: the oracle (axe-core 4.14.0 in jsdom, page scripts not executed), the
corpus of 27 hashed pages, and the plumbing classification — all three come
from E162 and are reused unchanged. **The filtering rule is E162 §4's, adopted
before any new page was fetched**, because changing it after seeing the new
pages' numbers would be choosing the denominator to suit the answer.

New: a larger population, and a derivation probe that looks *outside* the node.

## Population, declared before fetching

**Arm 1 — the 27 pages already fetched and hashed** (`corpus-manifest.json`,
re-fetchable with E162's `fetch.js`). Not re-chosen.

**Arm 2 — functional sub-pages of the same 21 hosts that returned 200.** The
selection rule is deterministic and was fixed before fetching:

> For each host in E162's manifest, parse the stored root page, take the links
> whose `href` path matches `/(contact|accessib|search|apply|form|report)/i`,
> in document order, resolve them against the page's own base URL, keep the
> first **two** distinct resolved URLs per host that are on the same host and
> return 200 to a plain GET, and fetch those.

Root pages are the least representative pages a site has — they are marketing.
The pages a user meets with a defect are the ones with a form, a search box and
a contact form, and the rule above reaches them without a human choosing.

Target **≥ 40 new pages**; if fewer qualify, the count actually obtained is
reported and no threshold is moved. One page per resolved URL; no page is
replaced after any finding is seen.

**This is not a prevalence population** and no claim about how broken the web is
will be made. It is a composition population: *given that these pages have
defects, what are they made of once the plumbing is removed.*

## The derivation probe (the thing this experiment is for)

For each **content-bearing** WCAG-tagged instance whose defect is a missing or
incorrect name, search the same document for authored text that a person
plausibly wrote to describe that element, in this declared order:

| # | source | example |
|---|---|---|
| D1 | `aria-labelledby` target's text | `<button aria-labelledby="x">` with `#x` labelled |
| D2 | `aria-describedby` target's text | |
| D3 | `<label for=id>` / wrapping `<label>` | `<label>Full name <input></label>` |
| D4 | `<figcaption>` of the enclosing `<figure>` | |
| D5 | `title` attribute on the element or its nearest labelled ancestor | |
| D6 | `value` attribute of the control | `<input type="submit" value="Search">` |
| D7 | a `<th>`'s text, for a `td` with no header | |
| D8 | the nearest preceding heading (`h1`–`h6`) | for a nameless `<a>` or `<img>` |
| D9 | the element's own visible text content | control, already named — not a defect |

Each derivation is recorded with its source and its text, and the record is
kept so a reader can check the judgement rather than take it.

**D8 is the aggressive one and it is declared as such**: it is how a code
documentation page's line anchors would acquire the code line beside them, which
E162 called cosmetic. D8 is therefore counted **both ways** — inside C3 and
outside it — and no threshold moves after the number is seen.

## Gates, declared before fetching

| Gate | Declared | Meaning |
|---|---|---|
| **G0 oracle validity** | axe runs on ≥ 90% of fetched pages; ≥ 20 pages have ≥1 AA instance | the instrument works on this population |
| G1 composition concentration | the top **3** classes hold ≥ **50%** of content-bearing AA instances | a triage order is defensible |
| G2 no single page dominates | no page holds > **25%** of content-bearing AA instances | the composition is a population fact |
| **G3 derivable share (the build gate)** | ≥ **20%** of content-bearing AA instances have a derivable name from **D1–D7** | a deterministic triage-and-derive tool is worth building |

**Kill gate.** G3 is the decision this experiment exists for. **G3 ≤ 5% closes
the deterministic triage-and-derive line** and the honest conclusion is that
accessibility remediation is an authoring task — which is a useful, publishable
answer, and the one E162's mechanism already implies. G3 ≥ 20% with G1 and G2
met is a build trigger: the program is "name what to fix first, and fix the
derivable ones".

**Gate honesty, declared now.** G1 and G2 are descriptive, not selective: any
composition passes or fails them as it falls, and a FAIL is a finding about the
population rather than about a program. G0 is about the instrument. Only G3 can
decide a build, and only G3's threshold is argued: a fifth of the real defects
is the point at which a deterministic pass beats a person reading a report.

## What this experiment cannot decide

- **Demand.** Nothing here measures whether anyone would install such a tool.
- **Screen-reader outcomes.** A derived name is judged a *plausible* source, not
  a measured improvement; E162's `fabrication` proxy is reused and carries the
  same ceiling.
- **Real-browser behaviour.** jsdom performs no layout, so `color-contrast`
  stays in `incomplete` and every number is DOM-decidable.
- **Whether the derived name is the name a person would have written.** The
  record makes it checkable; the judgement is the author's, and a wrong D8 is
  why D8 is counted both ways.

## Prior art

Probed separately before any build decision, in `PRIOR-ART.md`, for the triage
and prioritization class specifically (E162 probed the autofix class).