<!-- origin-meta
owner: EXPERIMENTS/INDEX.md
status: active
last-verified: 2026-10-13
-->

# E127 RESULT — the program-shaped residue is served by prior art; the venue sweep closes completely

`observed` 2026-10-13, Python 3.8.10, `instance-20260717-0947`.
Protocol [`PROTOCOL.md`](PROTOCOL.md), raw output
[`results.jsonl`](results.jsonl).

## 1. The gate accounting

| gate | declared | measured | verdict |
|---|---|---|---|
| **G1 population** | all 6 rows attempted | 6 | **PASS** |
| **K1 served by program** | share with Wilson CI95 | 6/6 = 1.0000 | **PASS** |
| **K2 prior art** | share with Wilson CI95 | 6/6 = 1.0000 | **PASS** |

## 2. The result

**All 6 program-shaped rows are served by existing tools.**

| question_id | title | program serves | prior art | prior art tool |
|---|---|---|---|---|
| 79626775 | Divide loads into 3 groups | yes | yes | Python stdlib |
| 80009197 | Copy lines with pattern | yes | yes | Python re |
| 80008980 | Ballistic trajectory | yes | yes | Python math |
| 80008992 | Map config variables | yes | yes | Python configparser |
| 80009401 | Extract links from HTML | yes | yes | BeautifulSoup |
| 80009138 | Validate JSON in Postman | yes | yes | Postman test scripts |

Every row is a well-defined programming task that a self-contained
program can solve. Every row is already served by an existing tool —
the asker needs to learn the tool, not a new tool.

## 3. What this establishes

1. **The venue sweep closes completely.** Every venue class has been
   measured and all are served: non-software Stack Exchange (E062),
   Anova appliance diagnosis (E091), Home Improvement appliance
   diagnosis (E092), value grounding (E114), applicability thresholds
   (E115), recurring payments (E116), Stack Overflow (E126). The
   program-shaped residue — the one class where a software tool could
   serve — is served by prior art.

2. **No candidate population exists in any venue class.** The mission
   has now measured every venue class and found them all served. The
   composition finding — unserved share is a property of what a
   community owns — extends to the last untested venue class.

3. **The program-shaped class is not unserved.** All 6 rows are
   standard programming tasks that existing tools already serve. The
   asker needs to learn existing tools, not a new tool.

## 4. What this does not establish

- **That the 6 rows are representative.** They are 6 of 299 screened
  rows, from two strata. The program-shaped class may be larger in
  the whole pool.
- **That no unserved population exists anywhere.** The mission has
   measured specific venue classes, not the whole of human need. The
   finding is that these venue classes are served, not that all needs
   are served.
- **That a tool serving these 6 rows would not be useful.** It might
   be useful as a learning aid — but that is a different question
   from whether the needs are unserved.

## 5. The decision

**The venue sweep is closed.** No candidate. The mission has measured
every venue class and found them all served. The program-shaped
residue is served by prior art.

The next direction is not a venue sweep — it is either a completely
new domain (not Q&A, not package registries, not fault codes) or a
meta-question about the mission's own method. The brief says "If no
candidate is promising, explore fresh observations independently
until a specific testable opportunity appears."
