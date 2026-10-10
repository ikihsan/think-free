<!-- origin-meta
owner: EXPERIMENTS/PLAN.md
status: active
last-verified: 2026-10-10
-->

# E089 — the 93 "false accepts" are mostly projects with adjacent names, not substitutes

Session `2026-10-10-005`, VM `instance-20260717-0944`. Protocol declared in
[`PROTOCOL.md`](PROTOCOL.md) **before any row was labelled**.

**No candidate. No prototype.** This reads 93 descriptions E064 had already
fetched, committed, and never opened, and reports what the package authors say
their own packages are.

## The question

E064's headline — **0.1615**, quoted in `STATE.md` and F099 as the evidence that
"the existence bit every installer, IDE and checker returns is materially
insufficient" — counts every mutation of a real package name that resolves to a
real package. Its own protocol is explicit about the ground truth:

> Ground truth is definitional, so no labeller is involved and no label can be
> argued with … the *intended* artifact of every mutated name is the original.
> Any mutation that resolves is a **false accept by construction**.

**"By construction" is an assumption, and it was never measured.** Whether
anyone who installs `requests-utils` means `requests` is a fact about people,
not a fact about the mutation operator. E089 is that measurement.

## Verdict

| gate | outcome |
|---|---|
| **G1 population** | **met.** 93 of 93 rows carry exactly one hand label; 0 missing, 0 extra, 0 invalid. |
| **G2 the rule discriminates** | **met.** **0 of 30** controls — the intended artifacts themselves — are labelled `equivalent`, against a gate of ≤ 4. |
| **G3 the decision** | **11 of 93 = 0.118**, Wilson CI95 **[0.067, 0.199]**. |

The declared reading bands were ≥ 0.50 ("0.1615 counts adjacency") and < 0.10
("0.1615 stands"). **0.118 falls between them; neither declared reading fires,
and the number is reported as it falls rather than moved into a band.**

## What the authors say

| label | n | share | what it means |
|---|---|---|---|
| `equivalent` | **11** | 0.118 | claims to provide the seed's capability under its own name — a reimplementation, a drop-in replacement, a clone, an alternative |
| `derivative` | 44 | 0.473 | builds on, adapts or wraps the seed for a stated purpose, and is its own thing |
| `other` | 38 | 0.409 | a separate project with an adjacent name, or **parked** |

**13 of the 38 `other` rows are parked names** — no description, `Reserved`, or
`security holding package` (`chalk-utils`, `commander-js`, `lodash-utils`,
`nanoid-js`, `nanoid-rs`, `node-axios`, `node-winston`, `winston-js`, `zod-js`,
`django-requests`, `fastapi-click`, `rand-cli`, `tokio-cli`). A parked name is
the **loudest** outcome available: the install succeeds and imports nothing.

The 11 `equivalent` rows, in full, with their own words:

- `fast-requests` — "无与伦比的简单且强大的requests" (*unparalleled, simple and powerful requests*)
- `fast-rich` — "A drop-in replacement for Python Rich, powered by Rust"
- `tenacity-rs` — "Drop-in replacement for tenacity with a Rust core. Same API"
- `zod-rs` — "Drop-in replacement for zod v4"
- `node-chalk` — "This is clone of chalk but only node version"
- `simple-chalk` — "an alternative to chalk package"
- `mini-chalk` — "A lightweight alternative to Chalk with no dependencies"
- `mini-dayjs` — "A lightweight date manipulation library similar to Dayjs"
- `simple-requests` — "Asynchronous requests in Python without thinking about it"
- `simple-sqlalchemy` — "A simplified, enhanced SQLAlchemy package"
- `async-redis` — "A Redis client library"

Seven of the eleven say the word themselves: *replacement*, *clone*,
*alternative*. **An `equivalent` label is not in practice a judgement call — it is
a phrase in the description**, which is why a reader is not the weak link here.

## The correction, stated as an arithmetic

| | count | share of the 576 mutations |
|---|---|---|
| E064's headline: mutations that resolve | 93 | **0.1615** |
| of those, self-declared substitutes | **11** | **0.0191** |

**0.1615 overstates the silent-substitution hazard by 8.5×** on E064's own
population. It is a correct count of *name adjacency under a mutation operator*;
it is not a count of installations that quietly went to the wrong project.

This agrees with the one independent measurement of the same class on real
declared dependencies: E085/F108 hand-read 6 flagged rows and found **3 true, 3
false**, a silent rate of **0.6%** — between E089's ≤1.9% ceiling and zero, and
**an order of magnitude below 0.1615**. Two measurements on different
populations now point the same way.

## What changes, and what does not

- **The package-name line stays closed** — on a number that can now be defended,
  instead of on a definitional assumption.
- **F099 and the dashboard sentence change.** "The existence bit is materially
  insufficient" is not supported at the strength the 0.1615 phrasing implies.
- **The existence bit is still not sufficient.** 11 real packages present
  themselves as drop-in replacements for other real packages, and nothing in the
  ecosystem says so. That is a real hazard at ~1.9% of plausible near-miss names
  and ~0.6% of real declared dependencies — worth a mention, not worth the
  candidate the 0.1615 was spent on.

## Ceiling and limits

- 93 rows, four ecosystems; **Packagist `not_exercised`** (E064 resolved 0 of 48
  there, so there is nothing to read).
- Descriptions as fetched by E064 on 2026-10-08; a package that has since been
  re-described would move its label.
- This measures **what authors claim**, not installs, intent, or harm. A
  `derivative` package can still mislead; the claim is that the row does not
  present itself as the thing the reader asked for.
- The population is **generated affix mutations** (suffix/prefix/synonym), which
  is not what a person types. That biases the whole E064 line, not just this
  reading, and is not corrected here.
- One reader. Mitigated, not eliminated: `selfcheck.py` requires **93 of 93**
  population labels and **30 of 30** control labels to be traceable *verbatim* to
  the source bytes (`observed`: 7 quotes were not verbatim on the first pass and
  were corrected against the file before the count was read).

## Reproducing

```bash
python3 EXPERIMENTS/089-substitute-or-neighbour/selfcheck.py   # exit 0
python3 EXPERIMENTS/089-substitute-or-neighbour/analyze.py      # exit 0
```

`analyze.py` verifies the sha256 of both E064 inputs against
`input-digests.json`, pinned at the moment the labels were written, and exits 3
rather than counting if a single population row is unlabelled. It classifies
nothing; it counts `labels.tsv`.