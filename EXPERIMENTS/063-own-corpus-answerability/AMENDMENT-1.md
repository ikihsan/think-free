<!-- origin-meta
owner: EXPERIMENTS/PLAN.md
status: active
last-verified: 2026-10-08
-->

# E063 — AMENDMENT-1

Written 2026-10-08, session `2026-10-08-013`, after the labelling pass and before
any verdict was written down. Four deviations from `PROTOCOL.md`, each declared
with what it does to the result.

## A1. A sixth label, `no-need-stated`

The protocol listed five labels. Twelve of the 71 arm A rows carry a need trigger
("I wish there was", "looking for a tool") and then state **no request at all** —
the text is an argument, an announcement, or a reply to somebody else. Calling
those `served` would have inflated the numerator with rows that ask for nothing;
calling them `unserved` would have inflated the denominator with rows that ask for
nothing. So they get their own label and are reported three ways: over all rows
(the declared denominator), over rows stating a need, and in the label
composition. `unserved-open` stayed at **0 in every arm**, which is the label that
would have opened a candidate and the one I most expected to be self-granted.

## A2. Rule R — an assistant that can *implement* the thing counts as serving it

Not declared, and it is the decision this experiment turns on, so it is named
here rather than buried in the labels.

**Rule R:** a row is `served` when a free general assistant hands the requester a
remedy they could execute today — an existing artifact, a complete procedure, or
the working implementation, which a 2026 assistant writes on request.

The alternative was to count implementation as *not* service, on the argument that
"a developer must write the patch" is a want, not a need. Rule R takes the
opposite side, because the requester of a need statement in 2026 has the same
access I do, and because choosing the stricter rule would have made every
feature request an unserved population — which is the shape of the mistake this
experiment exists to detect.

**What it costs:** it decides almost all of arm B. Every one of the 31 served arm
B rows is repository work an assistant could implement; under the strict reading
arm B falls to **0 of 32**. The headline therefore rests on a stated rule rather
than on the world, and `outcome.py` reports the strict reading as well.

## A3. G3 is replaced, not met

The declared gate was Cohen's κ ≥ 0.60 between two blind passes over 40 rows. I
am the only reader available in this session, and pass 2 happened in the same
context as pass 1, so a κ from it measures my memory of my own labels. A number
produced that way would look like a check while testing nothing, which is the
failure mode D081 was written against.

**Replaced by G3′ — sensitivity of the headline to the three arguable boundary
decisions**, computed in `outcome.py`:

1. Rule R on vs off (`A_strictest`, `B_strictest`);
2. open-web lookup allowed vs knowledge-only (`S2_RETRIEVAL`);
3. `no-need-stated` rows in the denominator or out.

This is harder to pass than a κ, because it returns a range that can straddle the
decision threshold. **It does straddle it in one arm: arm B, 0.97 on Rule R and
0.00 without it.** Arm A survives the strictest reading at 0.6197 against the
declared 0.60, so the decision for arm A does not depend on the rule.

## A4. The queue file lists each control twice

The interleaving loop appended the controls to a list that already contained them,
so `raw/queue.tsv` has 143 rows for 123 unique rows. Labels are keyed by
`blind_id`, so no row is double-counted and the denominators are unaffected. Left
in place rather than regenerated, because the reading order actually used is the
record of how the pass ran; `raw/queue-unique.tsv` is the deduplicated copy.
