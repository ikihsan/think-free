<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-03
-->

# Evidence labels

Every claim carries one of these labels. They are not decoration: an unlabelled
claim is treated as `untested` regardless of how confident it sounds. Full
definitions live in `docs/policy/evidence-labels.md`; this file is the summary
that belongs in the agent's head.

| Label | Means | Requires |
|---|---|---|
| `observed` | It happened, in this environment, reproducibly | Command, exit code, raw output, environment |
| `source-supported` | A source says so, and you read it | URL, publication date, retrieval date, what it actually says |
| `inferred` | A conclusion from observed or sourced facts | The facts, and the reasoning |
| `speculative` | A guess worth recording | Nothing, but it must be labelled |
| `untested` | A claim with no evidence behind it yet | The experiment that would settle it |

## The rules that matter

**A test result is not a product result.** Passing tests establish that a
mechanism works. They say nothing about whether anyone wants it, whether it is
better than the alternative, or whether it would survive contact with real
data. These are four separate questions and a result answers one of them.

**A search that finds nothing is not evidence of originality.** Search indexes
are incomplete, terminology is unstable, and abandoned work is invisible. Before
any novelty claim, search the user's vocabulary, the academic term, and the
infrastructure term, and open the limitation sections of what you find.

**A vendor claim is not a measurement.** "Handles 10,000 files" on a product
page is `source-supported` as a statement about the page and `untested` as a
statement about the software. Say which one you mean.

**Synthetic data cannot establish prevalence.** A synthetic fixture can falsify
a universal claim. It cannot tell you how often a failure occurs in the wild,
and a planted defect must never be reported as a discovered one.

**One timing is not a benchmark.** Local timings are useful for detecting
regressions and worthless as comparative evidence. Record what was included,
repeat it, and preserve every run.

**Retrieval date is not publication date.** A page retrieved today may be a
decade old. Record both, and prefer the source's own stated date.

**Negative results are results.** A disproved hypothesis with a clear reason is
worth more than an unfalsified hunch, because it removes an option. Distinguish
a failed implementation from a failed idea: "my parser was wrong" and "the
approach does not work" are different findings and lead to different next steps.

**Sunk cost is not evidence.** Work already spent does not make a candidate
worth continuing. Re-evaluate on the current evidence, not on the investment.