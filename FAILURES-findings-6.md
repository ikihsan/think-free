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
## F028 — The flat adoption tail is a property of vocabulary age, not of this niche

Source: session `2026-10-04-046`, task T-0058. Raw census:
[`EXPERIMENTS/011-niche-adoption-census/results.json`](EXPERIMENTS/011-niche-adoption-census/results.json),
taken 2026-10-04 from the GitHub search API.

**Belief under test.** F027 left three readings open: flat adoption is
specific to agent-session auditing, general everywhere, or specific to
young vocabularies. This census probes all three with seven search
vocabularies.

**Measured, `observed` 2026-10-04.** In the same young vocabulary cluster
as F027's niche, the flat tail reproduces exactly: `lockfile drift` tops
out at 6 stars and `dependency quarantine` at 8 stars, with totals of 57
and 29 repositories. In established vocabularies the tail is heavy —
`reproducible builds` (top 4135), `build provenance` (top 1050),
`supply chain audit` (top 772), `artifact provenance` (top 1050) — but
the outliers are long-lived or vendor-official (`please` since 2016,
Open Build Service since 2011, GitHub's own attestation action). In
`agent session log` the first result is the 40k-star incumbent and
everything below it is under 400 stars.

**What this says.** A young problem-vocabulary contains only young
projects, and young projects score zero adoption whatever their merit, so
a stars-based "plausible adoption path" criterion is uninformative for
exactly the vocabulary this mission's twelve candidates were screened in.
The criterion discriminates only where the vocabulary is decades old —
where every survivor is already entrenched. That sharpens the F027
reading: the axis problem is not "this mission picks bad niches" but
"adoption-as-stars cannot discriminate among young candidate domains at
all."

**Ceiling.** One snapshot, one endpoint, search over names and
descriptions, stars as a weak proxy; `ripgrep`-class false negatives still
unrefuted, and no measurement of usefulness is made. What survives is the
narrow, decision-changing half: do not read a stars search as evidence
for or against a candidate in a vocabulary less than a few years old.

## F029 — Stars do not measure adoption in any of five niches, so F028's flat tail was never a statement about adoption

Source: session `2026-10-04-047`, T-0059. Raw results:
[`EXPERIMENTS/012-prior-art-predicts-adoption/results.json`](EXPERIMENTS/012-prior-art-predicts-adoption/results.json).
Instrument `observed` 2026-10-04.

**The belief under test.** `STATE-next-actions.md` item 0 holds that
prior-art survival cannot be the selection filter, on the inference that a
crowded niche is a solved niche. That inference has two links and neither had
been measured: F027 and F028 counted **votes**, and F028's conclusion — that the
flat adoption tail is vocabulary age — was drawn from stars. This entry measures
**installs** in the same five kinds of niche and reports what the two measures
have to do with each other.

**Measured, `observed`.** Top 25 repositories by stars in each of five niches,
then registry downloads over one month — npm `last-month`, PyPI per-month,
crates.io summed daily rows — with the largest single-registry figure credited
and the registry recorded.

| Niche | Age | Any measurable install | >1k/mo | max monthly installs | top-by-stars project | its installs | Spearman(stars, installs) |
|---|---|---|---|---|---|---|---|
| `agent session log` | young | 2/25 (0.08) | 1 | 1,864 | `PostHog/posthog` (40,135★) | **0** | −0.157 |
| `lockfile drift` | young | 3/25 (0.12) | 2 | 3,100 | `mcptrust/mcptrust` (6★) | 0 | 0.350 |
| `knitting chart` | young | **0/25** | 0 | 0 | `knitscape/knitscape` (64★) | 0 | undefined |
| `reproducible build` | mature | 4/25 (0.16) | 3 | 4,519 | `thought-machine/please` (2,616★) | **0** | 0.030 |
| `exif metadata` | mature | 7/25 (0.28) | 7 | 16,599,464 | `remove-ai-watermarks` (5,757★) | 8,100 | 0.070 |

**Three results, and the first two were not the ones expected.**

1. **Stars do not predict installs anywhere, including the mature niches.**
   `|rho| ≤ 0.35` in all five, and negative in one. So F028's heavy star tail
   in `reproducible builds` is **not** evidence of adoption, and its flat tail
   in young vocabularies is not evidence against it. F028 measured one thing;
   this measures another; the two are decoupled, which removes the reading
   either was offered as support for. F028's own ceiling already said stars were
   "a weak proxy"; the measurement says the proxy is unrelated.
2. **Measured on installs, vocabulary age does not rescue a niche.** Four of
   five niches are flat *including* the mature one: `reproducible build` tops out
   at 4,519 installs/month and its 2,616-star leader has none. Only
   `exif metadata` has real volume, and it is the one niche whose artifact is a
   small library with an unambiguous install path. This **contradicts** the
   prediction F028's framing invited, and it is the finding that matters.
3. **The instrument, not the world, produced two of the numbers.** 31 of 125
   projects (25%) had a package whose name matched the repository but whose
   metadata named a different owner. Unverified, the first run credited
   39,000,000 installs/month to `PostHog/posthog` — an analytics platform
   returned by a search for "agent session log" — and gave the mature niche's
   real incumbent 47 installs via an unrelated `npm:please` belonging to
   `mrdrozdov/please`. Both were wrong and both flattered the hypothesis.
   Attribution now requires the package's own declared repository to be the
   project measured, falsified in both directions before any result is used.

**What this rules out.** That "prior art exists" can mean "the problem is
served", *as a selection filter*. In three young vocabularies 88–100% of the
leading implementations have no measurable install, and the leaderboard's own
first entry has none in four of five. A niche being full of implementations is
the **expected state of every crowded vocabulary**, and is compatible with none
of them being used. Twelve prior-art deaths are therefore not twelve pieces of
evidence against twelve candidates.

**What it does not rule out.** It does not make any of the twelve candidates
worth building; it removes one reason for discarding them and supplies none.
It says nothing about usefulness, which stays `unmeasured`. It does not
vindicate stars as a proxy for the mature arm either — that is precisely what
result 1 refutes.

**Ceiling, and the gate's dead branch was not fully executable.** Registry
downloads count installs of packages. `thought-machine/please` is a real
2,616-star build system with real users and is invisible here, because it ships
as a Bazel binary. **Zero measured installs is not zero users**, and the mature
arm's most important incumbent is exactly the kind this instrument cannot see.
The pre-declared kill gate ("a dominant incumbent does exist somewhere, which
would vindicate the filter") could therefore not have fired on this sample, so
H surviving is a weaker result than the same verdict on a measurable arm would
be. Also: installs are not active use, and a package pulled by a CI default
counts once per job. One snapshot, one endpoint family, one machine, search over
names and descriptions. Renamed repositories, monorepos and packages that
declare no repository are dropped, which biases the measurement **downwards**.

**The axis this opens, offered as the next thing to falsify.** If
implementation count is universal and adoption is near-zero in every crowded
vocabulary, then the scarce thing is neither novelty nor reach but the
**install path**: whether a person who wants the artifact ends up running a
command, or has to find a repository, read it and trust it. That question is
answerable about a candidate *before it is built*, with no users and no market.
It is `inferred` from five niches of 25 and is not yet tested; the obvious
falsifier is a crowded niche whose incumbents are heavily installed.
