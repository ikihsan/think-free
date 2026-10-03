<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-03
-->

# Review protocol

The adversarial step. Its purpose is not to confirm work but to find the reason
it is worthless, while that reason is still cheap to act on.

Checklist derived from `RESEARCH/D.md`, which is the original adversarial
report and remains the worked example.

## When

- Before committing a result that claims something works.
- Before committing to a candidate project.
- Before publishing anything externally.
- Whenever a session's outcome is `partial` or `failed`, to decide whether the
  remaining work is worth anything.

Review is a separate pass from implementation. An agent reviewing its own work
in the same breath it wrote it will confirm rather than attack, because the
reasoning that produced the work is still loaded.

## The questions

1. **What evidence would convince us to stop developing this?** If that cannot
   be answered, there is no project, only an activity.
2. **What simpler solution would erase our advantage?** Name it, then check
   whether it already exists.
3. **Are we solving a real problem, or a problem invented to justify the
   solution?** Look for a user, not a scenario.
4. **Would anyone adopt this without knowing an AI wrote it?** If adoption
   depends on that framing, the value is in the framing.
5. **Does this deliver value beyond its demonstration?** A demo is a single
   point; a product must work outside it.
6. **Could an independent engineer reproduce every claim?** Try the reproduction
   command from a clean clone. If it needs this machine, say so.
7. **What are we overlooking because our agents share training biases?** If four
   independent investigations converged, ask whether they converged because the
   answer is right or because they are the same model.

## Adversarial protocol

From `RESEARCH/D.md`, condensed:

1. **Write a falsifiable claim card.** One user, one recurring task, their
   current workaround, the mechanism, the minimum meaningful improvement, and
   the permitted inputs. Replace "universal", "automatic", and "safe" with
   explicit scope.
2. **Search three vocabularies.** The user's terms, the academic term, the
   infrastructure term. Open limitation sections, not just landing pages.
3. **Build the strongest cheap baseline.** Configure the real competitor, or a
   short script, or the manual workflow. Count setup and repair time for all of
   them. Failing to install a rival once proves nothing.
4. **Test information sufficiency first.** Two realities, identical inputs,
   different required outputs. If they cannot be distinguished, narrow, observe
   more, or abstain.
5. **Prepare twenty cases before implementing.** Eight ordinary, six
   boundary or adversarial, six held out from another context. Store source,
   licence, ground truth, and hashes. Keep holdout answers away from the
   implementer.
6. **Measure task outcomes and transferred labour.** Correctness, severe-error
   rate, abstention coverage, elapsed time, review time, setup steps, memory,
   dependencies. Review time belongs in the total.
7. **Run withdrawal and change tests.** Remove the network, the cache, the
   upstream service, the clean input. Change one version. Let an old client
   return. Find out who repairs it, and whether correct output silently becomes
   wrong.
8. **Use a predeclared kill gate.** A suggested exploratory gate: preserve or
   improve severe-error outcomes and improve a relevant task metric by at least
   30% on held-out cases, including setup and correction cost. This is a
   heuristic, not a law, and a 30% gain on a trivial task is meaningless.
9. **Separate technical survival from adoption.** Technical survival means the
   mechanism works. It does not mean anyone wants it.
10. **Prefer a contribution.** If the missing step is small, a patch to an
    existing project delivers the same value with less to maintain.

## Recording the outcome

Write the review into the candidate's record in `HYPOTHESES.md`, with:

- the strongest objection found, not the weakest;
- what evidence would settle it;
- whether the decision changed, and if not, why the objection did not hold.

A review that changes nothing is still worth recording. The next session needs
to know the objection was already considered.

## Limits of this protocol

Agents sharing a model share priors. Four independent investigations in
`RESEARCH/` are procedurally independent and not epistemically independent.
Agreement among them is weak evidence; disagreement is strong.

Adversarial review can also overcorrect: it can kill a candidate for missing a
user when the actual problem is that the user has not been asked yet. Record
that distinction rather than resolving it by assumption.