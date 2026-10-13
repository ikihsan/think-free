<!-- origin-meta
owner: EXPERIMENTS/INDEX.md
status: active
last-verified: 2026-10-13
-->

# E127 — can a self-contained program serve the 6 program-shaped rows from E126?

Predeclared **before any row is attempted**.
Follows E126 (`../126-stackoverflow-service-test/`), which found 6
program-shaped rows in 299 screened Stack Overflow questions.

## Question

Of the 6 program-shaped rows from E126 — rows whose remedy is a
self-contained program the asker runs, not an answer — what share can
be served by a self-contained program, and does an existing tool
already serve them?

**Why this is the one residue.** Every venue class has been measured
and all are served by a free general assistant (E062, E091, E092,
E114, E115, E116, E126). The program-shaped class is the one where
a software tool (not an answer) could serve a residue. If these 6
rows are served by existing tools, the venue sweep closes completely.
If they are not, this is the first candidate population the mission
has found.

## Population

The 6 program-shaped rows from E126's screening:

| question_id | views | arm | title |
|---|---|---|---|
| 79626775 | 459 | A | Divide electrical loads into 3 groups with near-equal sum |
| 80009197 | 446 | B | Copy lines with 5 as second-to-last digit and line below |
| 80008980 | 152 | B | Ballistic trajectory with quadratic drag, terminal plot |
| 80008992 | 134 | B | Map variables from config file |
| 80009401 | 113 | B | Extract internal links and anchor text from HTML |
| 80009138 | 86 | B | Validate JSON response fields in Postman |

## What "served by a program" means

**Served:** a self-contained program (a script the asker runs on
their own data) produces the artifact the asker needs — the divided
groups, the copied lines, the trajectory plot, the mapped variables,
the extracted links, the validation result. The program must run on
the asker's own data without the asker writing new code.

**Not served:** the task is not well-defined enough for a program,
the program cannot produce the artifact, or the remedy is not a
program at all (e.g., a tool-specific configuration).

## Prior art

For each row, check whether an existing tool already serves it:
- Python standard library (re, json, math, etc.)
- BeautifulSoup / lxml for HTML parsing
- Postman's built-in test script feature
- Any other existing tool

If an existing tool serves the row, the row is **served by prior
art** — the asker needs to learn the tool, not a new tool.

## Gates

| gate | rule |
|---|---|
| **G1 population** | all 6 rows attempted |
| **K1 served by program** | share of rows a self-contained program can serve, with Wilson CI95 |
| **K2 prior art** | share of rows an existing tool already serves, with Wilson CI95 |

## Decision this changes

If all 6 rows are served by existing tools, the venue sweep closes
completely — every venue class is served, and the program-shaped
residue is served by prior art. If some rows are not served by
existing tools, this is the first candidate population the mission
has found, and the next step is to prototype a tool for the
unserved rows.

## What this does not establish

- That the 6 rows are representative of all program-shaped needs
  on Stack Overflow (they are 6 of 299 screened rows, from two
  strata).
- That a tool serving these 6 rows would be useful to anyone
  outside this sample.
- That the program-shaped class is large enough to be a candidate
  population (6 rows is a lower bound, not an estimate).
