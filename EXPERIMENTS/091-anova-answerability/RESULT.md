<!-- origin-meta
owner: EXPERIMENTS/INDEX.md
status: active
last-verified: 2026-10-11
-->

# E091 result — the block was false, the generalization fails, and the reason is composition

Session `2026-10-11-003`. Protocol `PROTOCOL.md`, design correction `AMENDMENT-1.md`,
gate evidence `G0.md`, raw attempts `ATTEMPTS.md`, grades `grades.py`,
arithmetic `score.py`, composition `compose.py`.

The stated block — *"no GPT-4o or Claude 3.5 Sonnet API access"* — did not hold.
`PROTOCOL.md` line 26 says *"or equivalent"*, E062 and E066 ran this exact
construction, and the agent writing this file **is** a general assistant answering
from its own knowledge. One experiment line, and task T-0090 carrying it, stood
unrun behind a condition the record had already met twice.

## 1. Gates

| gate | result |
|---|---|
| **G0 discrimination** | **PASS** — 10/10 answerable answered, 10/10 unanswerable declined, on probes labelled by construction and independent of thread outcome |
| **A1 population** | **PASS** — 20 of 20 rows re-fetched with full text, `full.jsonl`, digests in `fetch.py --verify` |
| **K1 served share ≥ 0.50** | **FAIL** — 5 of 20 = 0.2500, Wilson CI95 [0.1119, 0.4687], lower bound 0.1119 |
| **K2 cannot reject E062** | **REJECTED** — this venue's upper bound 0.4687 is below E062's lower bound 0.6396 |

Arm B attempt-first subset (the only rows whose attempts were written before any
thread was read): 3 of 7 = 0.4286, CI95 [0.1582, 0.7495]. K1 fails there too.

**Arm A, assessed on all 20 rows: 0 of 20 remedies are a self-contained
program.** They are: a router configuration, a C-clamp, a board replacement, a
jumper wire, a firmware mute the vendor declined to build, a return against an
order, a support-team account intervention, or four separate vendor software bugs.

## 2. Three defects in the inherited harness, and two I introduced

The session's worker process died after writing `score.py` but before running it.
Running it exposed defects that would each have changed the writeup:

1. **Exposure was inferred from prose.** The harness selected the
   "attempt-first" subset by searching each row's reason text for the literal
   string `PRIOR EXPOSED`. Ten rows are marked `THREAD-EXPOSED` and contain no
   such string, so they counted as attempt-first: it reported **18** rows where
   its own comment says **7**, and printed an "attempt-first subset" figure that
   was mostly thread-exposed rows. Repaired by carrying an explicit per-row flag
   in `grades.py`.
2. **One row's flag contradicted its own reason.** `6924` carried `served=False`
   beside a reason reading *"Graded served on that basis"*. Resolved to `False` —
   the thread never converges (reply [7], "I give up") and the residual blocker
   is an app-availability fact no explanation reaches — which is the direction
   that does not inflate the served share. The correction is recorded in the row.
3. **Arm A divided by a denominator it had not filled.** Tool-shapedness was
   scored for 10 rows and divided by all 20, so 10 unassessed rows silently
   counted as `False`. All 20 are now assessed.

Then, in the analysis written this session:

4. **The Fisher tail started at the wrong term.** `fisher_greater` summed from
   `col1` rather than from the observed count, dropping every term below the
   maximum whenever the comparison row had any successes. On this experiment's
   own table it reported **p = 0.001354** for a true one-tailed value of
   **0.030702** — a fabricated 22x significance, on the finding driving the
   writeup. `test_fisher.py` now checks the function against exhaustive
   enumeration of the 2×2 across 120 random tables (agrees to 1e-12) and pins the
   two live values.
5. **The same analysis printed a comparison row built from the population size.**
   "16 served of 16" where the truth was "1 of 13", driven `p` to a fabricated
   `0.000000`, and would have made the headline look overwhelming. The numbers
   above are from neither run.

## 3. What actually explains the difference

K1 and K2 ask whether an assistant serves these needs. They do not. What the 20
committed threads show is *what kind of need this venue contains*.

Classifying each row by **the remedy the thread actually converged on**, with no
reference to the assistant grades:

| class | served | unserved | of 20 |
|---|---|---|---|
| **answerable** — knowledge, or an action the asker can take alone | 4 | 3 | 0.35 |
| **repair** — a physical repair or an artifact | 1 | 6 | 0.35 |
| **vendor** — a return, an account action, a product decision, a software fix | 0 | 6 | 0.30 |

**13 of 20 = 0.65 of this venue's highest-arrival needs require the vendor or a
screwdriver.** The assistant served answerable-class needs at 4 of 7 and the
other 13 at 1 of 13 (Fisher one-tailed p = 0.0307); against vendor-bound rows
alone, 4 of 7 versus 0 of 6 (p = 0.0490). Every served row except `722` — a
C-clamp — is in the answerable class, and no vendor-bound row is served at all.

So the rejection of E062's generalization is **not** evidence that a general
assistant is weak here. It is evidence that the two venues hold different
populations. E062 sampled *Steam*, where the thing you own is software and the
remedy is a config change or a guide. This venue is a consumer-hardware vendor
forum, where the highest-arrival needs are overwhelmingly "my appliance is
broken", and the remedy is a return, a board swap, or a firmware change only the
vendor can ship.

## 4. The claim this actually supports

**The served share is not a property of a community. It is a property of what the
community owns.** Where the thing under discussion is software, a free general
assistant serves ~0.85 of stated needs. Where it is a physical product, the same
assistant serves ~0.25, and the residual is a support queue rather than a
knowledge gap — and, per F096, that queue is often worked privately, which is
what threads like `3051` (a support escalation shipping the right SKU) and
`12987` (a confirmed vendor bug) show happening inside the public record.

This retires the premise under which E062, E077, E082 and E084 were compared.
Those numbers were never measuring the same quantity across venues, so their
agreement and disagreement were both uninformative about communities.

It also corrects the sampling. **Any future unserved-share measurement must
screen out vendor- and repair-bound needs, or report the mix beside the rate.**
Screens built on arrival counts will always over-represent broken products,
because a broken product is what generates arrivals.

## 5. What this does not establish

- **It is one venue, 20 rows, one reader.** The composition table is a single
  reader's classification of 20 threads. E062's Steam population was not
  re-classified here, so the contrast is between two numbers produced by
  different sessions with the same instrument — which is the comparison the
  mission should distrust least, but has not verified.
- **The cleanest subset shows nothing.** Restricted to the 7 rows whose attempts
  were written before any thread was read — the only grades not exposed to the
  same reader who assigned the classes — the contrast is 2 of 4 versus 1 of 3,
  p = 0.6286. That subset is too small to confirm the explanation. It is
  reported for exactly that reason and is not leaned on.
- **The class is post-hoc.** It was assigned after the grades existed, by the same
  reader, from the same threads. The circularity is not fully excludable. What
  makes it more than a restatement is that the classification is defined on the
  thread's remedy and predicts served share in a graded direction, but that is
  weaker than a pre-registered test would have been.
- **No candidate.** Arm A is 0 of 20. The one row nearest tool-shaped, `4681`
  (check your Wi-Fi password against Anova's published 8–18-character, no-special-
  characters rule), is a one-off against one vendor's web page that the vendor's
  own setup wizard already covers.

## 6. Decision

The Anova venue is **closed** as a candidate route: not "needs go unserved" but
"needs go unserved to a seller or a screwdriver", which is the distinction
`AMENDMENT-1.md` §4 said Arm A existed to draw.

The instrument claim is **withdrawn**, not merely unsupported. "Unserved share"
was recorded as a venue-level property and is a property of ownership type
instead. Any cross-venue number already in the record is a number about a
population, not a community.

**Next action.** The one class in this experiment where a program could add value
is diagnosis of a specific appliance from a described symptom — the answerable
rows `86` and `26273` were both correct-in-kind diagnosis errors, not refusals.
The mission closed appliance-fault-code tooling four times (E079, E082, E083,
E084) on **population** gates, never on demonstrated absence of need. The next
action is a runnable test of whether appliance-fault diagnosis is a general need
outside one vendor's own forum — either it reopens that line with a concrete
reason, or it closes it for good.
