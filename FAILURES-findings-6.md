<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-04
-->

# Failures — recorded findings, part 6 (F026 onwards)

Continues [`FAILURES-findings-5.md`](FAILURES-findings-5.md), which holds
F022–F025. **Identifiers are stable across all six files**: a reference to
`F026` means the same entry wherever it appears. New findings are appended here.

**What these two have in common with F022–F025.** Every one of them is a rule
this repository held about itself that turned out to be held by someone else at
the same time. F022 borrowed a predicate from a neighbouring question; F026 and
F027 are the same move at a larger scale — the mission held a belief about its
own method, and the belief had never been compared with anything outside the
repository.

The evidence for both is in
[`RESEARCH/PRIOR-ART-ORIGIN.md`](RESEARCH/PRIOR-ART-ORIGIN.md), sealed
2026-10-04. Sources were retrieved 2026-10-04; publication dates are given
separately.

## F026 — The byproduct thesis is disconfirmed: this mission's own tooling is prior art, and so is its discipline

Source: session `2026-10-04-045`, 2026-10-04. Full record:
[`RESEARCH/PRIOR-ART-ORIGIN.md`](RESEARCH/PRIOR-ART-ORIGIN.md).

**The belief under test.** `tools/origin` — ~9,800 lines, the mission's only
substantial artifact — was never counted among the candidates, because it was
never treated as one. It is a byproduct: it appeared because two VMs needed to
coordinate, and it has been used 88 times in two days. The implied thesis was
that building what you need as you go lands somewhere candidate ideation does
not, because the need is felt rather than imagined.

**What was checked, `observed`.** Three vocabularies: the user's (agent session
log, flight recorder, audit receipt), the infrastructure term (reconcile a
session record against version-control ground truth), and the academic term.

**What was found.** Two results, both about the mission itself.

1. **The mechanism is prior art, six weeks old.**
   [`gitreceipts`](https://github.com/jagmeetchawla/gitreceipts), MIT, Rust,
   `jagmeetchawla`, crates.io created 2026-07-23, v0.1.5 published 2026-08-10.
   Its description: *"reconcile a coding-agent session log against the git
   history it claims to explain."* Its `reconcile` module reports **both**
   directions — claims that never landed, and residue (files the commit says
   changed that the log never claimed) — so on that axis it covers more ground
   than `origin`, which reports residue only. (Not a superset of *all* of
   `origin`'s reconciliation: base-advance attribution, D039/T-0053, and
   declared exemptions, F022, are absent from it.) It also carries `Sibling
   Writes`, a cross-repository attribution count, which is this repository's
   landed-work attribution defect (D028, T-0024) solved independently. The recording half
   is older still: `rxNxkolai/opentrail` ("AgentTrace", created 2026-06-04)
   captures every tool call, command and file change per session and writes a
   graded receipt.

2. **The discipline is prior art too, and this is the part that was not
   expected.** From gitreceipts' own `KNOWN-LIMITATIONS.md` and
   `docs/COMPAT.md`, quoted verbatim: *"loosening the match far enough to cover
   it would start laundering real losses"*; *"console, HTML, and JSON always
   carry identical values… the three surfaces are three renderings of one
   receipt"*; and a field was removed because *"keeping a field that cannot mean
   what its name says is worse than the break"*. Those are the same three
   positions this repository reached independently over 87 sessions — recorded
   as `AGENTS.md`'s "do not weaken an integrity check to make a result look
   successful", D043 (defect 20, 47 generated reports repeating a row), and
   defect 14. One person, in Rust, in three weeks, with no contact with this
   repository.

**What this rules out.** The strong byproduct thesis. Building what you need as
you go does **not** escape the prior-art wall — it lands inside it, because the
need is a real need that other people have already met. `tools/origin` cannot be
presented as novel, and any public front door claiming otherwise would be making
a false statement.

**What it does not rule out.** It does not show the tool is not useful; two stars
and 158 downloads is not a measurement of usefulness. It does not show the
mechanism is worthless — the brief's rule holds, that a lack of users means
usefulness is unmeasured. And it does not rule out the one measured advantage
that survives: gitreceipts' own issue list (#10 multi-lane sessions, #8
cross-machine, #5 path-level rather than content-level verification, #9
harness-locked ingest) names four gaps this repository has two days of
documented, tested experience of.

**Ceiling on the finding.** The strongest available comparison was **not run**.
`cargo` is absent on this VM, so gitreceipts could not be installed, and the
head-to-head on real session logs is `unperformed`. No claim is made that
`origin` is better or worse at reconciliation. gitreceipts also reads Claude
Code JSONL; this repository's logs are `origin.session.event/1`, so it could not
audit these streams even with Rust present. GitHub search was restricted to
`name` and `description`; code search needs authentication.

**The consequence for the method, which is the real content of this entry.**
Twelve candidates, twelve prior-art deaths — F001, F006, F008, F009, F012, six
rejected inside `RESEARCH/D.md` and `RESEARCH/B.md`, and now the mission's own
tooling. **Prior-art survival cannot be the selection filter, because nothing
this mission produces passes it.** That is a fact about the procedure, not about
any one candidate, and it is the first time the mission has recorded one.

## F027 — Every project in this niche has zero users, so "plausible adoption path" cannot discriminate here

Source: session `2026-10-04-045`, 2026-10-04. Measurements in
[`RESEARCH/PRIOR-ART-ORIGIN.md`](RESEARCH/PRIOR-ART-ORIGIN.md) Finding 5.

**Measured, `observed`, 2026-10-04** from the GitHub API and crates.io:
`gitreceipts` 2 stars / 158 downloads; `opentrail` 2 stars;
`multi-agent-coordination-skill` 0 stars; `Tasktivity/git-receipts` 0 stars;
`tracewall`, `AgentLedger`, `agentlens` 0–1 stars. **`tools/origin`: 0 stars,
0 downloads**, used 88 times in two days by two agents on two machines.

**Why it is a failure and not an observation.** [`ROADMAP.md`](ROADMAP.md)
stage C admits a candidate only on four criteria, one of which is "a plausible
adoption path". In a niche where every project scores zero adoption, that
criterion returns the same answer for every candidate and therefore carries **no
information**. A filter that cannot distinguish is not a filter. Three of the
four stage-C criteria are now either flat or negative here: differentiation is
falsified for the mechanism (F026), adoption is flat, and practical value has
never been measured by anyone including this repository. Feasibility is the only
one left, and it is the easiest.

**Ceiling.** This is a small, self-selected sample of one niche. GitHub stars and
crate downloads are weak proxies for use, and a project can be genuinely
valuable at low star counts — `ripgrep` and `jq` are the standard objections, and
they are not refuted here. What is measured is the *absence of any outlier*, not
the absence of value.

**What it does not license.** It does not justify abandoning agent-run auditing,
and it does not justify treating the prior art as validated. The correct reading
is narrow and it is the one that changes a decision: **do not select the next
candidate from this niche, because this niche cannot distinguish candidates from
each other.** That is a reason to look elsewhere. It is not a reason to
conclude that nothing here is worth building.