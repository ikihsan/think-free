<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-07
-->

# Hypotheses — results, part 3: E046, the packaging claim against real changes

Split out of [`HYPOTHESES-candidates.md`](HYPOTHESES-candidates.md) at the 300-line cap.
Each result belongs to the candidate whose claim it settles, so this file is reached from
that one and not from the results index.

## E046 — the packaging claim, measured on real changes, did not hold

E037–E042 each closed with the same sentence: *"does not test renames, mode
changes, `--intent-to-add`, binary files, untracked files, or multi-file
scenarios."* Six times that was treated as disclosure. E046 read it as a work
list and ran it: **114 real file changes drawn from real commits** in this
repository, `psf/requests` and `jqlang/jq`, stratified by the shapes that
sentence names, every address staged one at a time and judged by git's own
patches rather than by `stg`'s coordinates.

**Four defects, all in the released source, none reachable from the ten synthetic
cases** (F076–F078, F080):

- **no line of any new file could be staged** — 435 of 435 addresses across 15
  real file-creation commits. Creating a file is the most common thing there is
  to do in a repository.
- **one address could name two changes and stage both** — a real commit here:
  `stg STATE-next-actions.md:80` removed eight lines and added one, printed the
  coordinate twice, and exited 1.
- **an address that could not change anything reported success** — 9 of one real
  jq file's 190 addresses left the index byte-identical to HEAD at exit 1.
- **two lines silently merged into one in the index, reported as staged** — on a
  real `requests` file whose last line has no newline. The only finding that
  corrupts rather than mis-selects.

All four are fixed, with 7 tests added (30 → 37, all green). After the fixes the
same corpus gives **1,614 of 1,615 addresses staged exactly as addressed and 1
refused by name**, no mis-staging, and completeness reproduced on every case where
the replay is faithful. Controls: positive 30/30 over E038's own matrix,
negative 17 of 17 wrong index states rejected.

**What this does to the candidate.** Mechanism differentiation stays falsified
(E041, E042). The packaging claim — *a ready-to-use tool you can trust on your
actual changes* — was the only differentiator left, and it was **unmeasured and
wrong** on the shapes the record had itself listed as untested. That is not a
reason to drop `stg`; it is the argument for D075: a candidate's own limitations
section is a measurement plan, executed over real input before the candidate is
called release-ready rather than after.

Evidence: [`EXPERIMENTS/046-real-changes/README.md`](EXPERIMENTS/046-real-changes/README.md).
