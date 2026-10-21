<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-20
-->

# E202 — AMENDMENT-3, declared before the merged G0 verdict exists

**Declared 2026-10-20 after all three shards of AMENDMENT-2 finished and before
the merge script was run.** What was known at declaration time: which files
appear in more than one record and what each record says (that census is what
found the ambiguity below). What was **not** computed at declaration time: any
completion rate, any denominator's numerator, any gate verdict on the sweep.
`gates.json` (arms, K1–K3, G1–G3, G5, dominance) is unchanged by this
amendment and was already written at 13:54.

## 1 — The merge rule contains an ambiguity, resolved here before the verdict

AMENDMENT-2 declares: *"main record's successful pages first, then every part
file, deduplicated by `file` … a page appearing in two records with **different
outcomes** is a defect and stops the merge."* It also declares that the todo
set is *"every HTTP-200 page with no successful record yet … **including the
three timeouts**"*, i.e. the three `axe timeout` pages are in scope precisely so
they get **one retry**.

Both clauses are satisfied by the data except on **one file**:

| file | main | part | kind |
|---|---|---|---|
| `pages/005-github.com.html` | `axe timeout` | `axe timeout` | same outcome |
| `pages/011-python-dev.best-of.org.html` | `axe timeout` | `axe timeout` | same outcome |
| `pages/006-aws-nuke.ekristen.dev.html` | `axe timeout` | **completed** | **different outcome** |

**Reading adopted (and named in every verdict line): the retry supersedes the
timeout.** Reason: the amendment puts the three timeouts into the todo set in
order to retry them, and names *dropping* them from the denominator as the
cheating move; if a successful retry were a merge-stopping defect, the amendment
would forbid the very action it declares. "Different outcomes" is therefore read
as **two completed runs of the same file disagreeing**, which is the
non-determinism the sentence can actually be about.

**The other reading is reported, not hidden.** Read literally, the merge stops
on `006-aws-nuke` and G0 clause 1 is *not evaluable* — the report would say so
instead of printing a rate. So every G0 number below is printed **twice**:
`with_retry_supersession` (primary, the reading above) and
`literal_no_supersession` (the `006` record counts as a failure in every
denominator it appears in). The verdict line names which it uses.

**Completed-run agreement, computed as part of this census:** six files carry
two *completed* sweep records (see §2). All six pairs agree exactly on
`n`, on the WCAG-tagged count and on the rule-id set. **Zero disagreements**
between two completed runs of the same bytes — the oracle's determinism is a
by-product result, not a gate.

## 2 — A fetch defect found by the census: `fetch2.js` overwrites its own files

`fetch2.js` computed the output index as `String(pages.length)` **inside**
concurrent callbacks, while `pages.push(...)` happens only after every fetch
resolves, so every stage-2 file was written as `pages/069-<host>-sub2.html`.
Two same-host targets therefore share one path and the second write overwrites
the first.

**Measured extent:** 98 manifest records → **85 distinct files**; **13 files
carry two records**, and on **6 of them the two records' `sha256` differ**, so
one stored body was overwritten and is gone. Five of those six were HTTP-200
bodies (`www.mkdocs.org/user-guide`, `mkdocstrings.github.io/usage/theming`,
`properdocs.org/user-guide`, `mkdocs.peaceiris.com/getting-started/download-boilerplate`,
`arabic.naveeraashraf.com/getting-started`); the sixth was a status-0 fetch with
no body. On the other 7 the two records agree byte-for-byte (two 404 bodies, or
the same URL differing only by a `#fragment`).

**Scope, stated before any verdict:** the three qualifying pages
(`010-johnthagen`, `063-fasthttp` root, `068-h4m5t`) are stage-1 roots and
**none of them is in the collision set**, so no arm measurement, no fabrication
count and no survival count is affected. What the defect does change is the
*denominator vocabulary*: HTTP-200 is **79 records but 73 distinct files**, and
5 fetched HTTP-200 URLs never reached the oracle. Declared as an instrument
defect; reported at both levels.

## 3 — AMENDMENT-2's own census sentence does not reconcile; corrected here

AMENDMENT-2 wrote: *"The corpus holds 98 fetched pages, 79 with HTTP 200, and
**85 stored bodies** (13 fetch failures have no body at all)."* Against the
manifest: **85 is the distinct-file count**, not the body count; records with a
body number **94** (distinct files with a body: **82**); fetch failures with no
body are **4 records / 3 distinct files**, not 13. The 13 is exactly the number
of duplicate records from §2, so that sentence mislabelled the collision as
fetch failures — **the label was wrong, the arithmetic was the collision's.**

**Denominator set used in `RESULT.md`**, each reported at record level and
file level, each printed under both readings from §1:

| label | records | distinct files |
|---|---:|---:|
| `D200` — HTTP 200 *(the sweep's declared denominator)* | 79 | 73 |
| `DALL` — every fetched record (literal "fetched pages") | 98 | 85 |
| `DBODY` — records with a stored body | 94 | 82 |

Nothing in §1–§3 changes a threshold, a page set, an arm or a gate. What they
change is which words the denominator carries, and they are all printed.
