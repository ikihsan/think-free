# D — Independent adversarial investigation

Sealed initial report, 2026-10-03. Investigator: D / Adversarial Skeptic.

## Independence and decision

I read `MISSION.md` and public primary sources. I did not inspect other investigators' reports, personal memory, unrelated repositories, or other investigators' findings. No product was assumed. No external messages, purchases, account changes, or public writes were made. This report is the only file written. Searches are listed below so another investigator can challenge the selection bias.

**Decision: no candidate is sufficiently supported by this investigation to nominate as the invention.** Five attractive claim families fail an initial adversarial gate. This does not mean their problem areas are exhausted. It means a broad promise in these areas is not enough: useful narrower contributions require tests against mature alternatives and the actual human bottleneck.

The common trap is confusing a proxy with the outcome: consistent replicas with correct shared intent; a clean scanner report with accessible task completion; recognized buildings with trustworthy humanitarian maps; a runnable package with reproducible science; predicted appliance signals with actionable energy savings.

## 1. “Automatically make or certify any website accessible”

**Source-supported observation.** W3C explicitly says some accessibility checks require manual intervention and tools can produce inaccurate results. Its evaluation-tools directory covers more than 100 tools. [W3C Evaluation Tools Overview](https://www.w3.org/WAI/test-evaluate/tools/) (page updated 2020-04-28; retrieved 2026-10-03).

**Prior art.** axe-core already distinguishes violations, passes, inapplicable checks, and checks requiring manual review. Its README reports an average automatic issue-detection figure; that is the project's claim, not a universal coverage guarantee and not independently validated here. [axe-core API](https://github.com/dequelabs/axe-core/blob/develop/doc/API.md), [repository](https://github.com/dequelabs/axe-core) (living documentation, retrieved 2026-10-03). W3C also already has an automation harness for executing ARIA-AT test plans without a human operator. [ARIA-AT automation harness](https://github.com/w3c/aria-at-automation-harness) (living repository, retrieved 2026-10-03).

**Adversarial inference.** Another DOM scanner, generic issue dashboard, or screen-reader automation wrapper has a very high differentiation burden. A page can contain a present but misleading image description, an apparently valid control whose workflow is unusable, or a task that loses state. Passing structural rules does not establish correct meaning or task success. This is an objection to universal certification, not a proof that useful automation is impossible.

**Hidden maintenance.** Browser/assistive-technology combinations, dynamic application state, and evolving test expectations. W3C's assistive-technology support guidance says tests need not require identical spoken output and generally use default configurations. A string-equality oracle would therefore be a poor substitute for conveyed information. [W3C AT support tables](https://www.w3.org/WAI/ARIA/apg/about/at-support-tables/) (living guidance, retrieved 2026-10-03).

**Falsifier for a future candidate.** Compare against axe-core plus ARIA-AT on task-level cases, including keyboard-only completion, focus restoration, dynamic errors, and misleading but syntactically valid text alternatives. Blind assessment by qualified users must establish fewer missed task blockers at no greater review effort. This environment can run fixtures; it cannot supply authentic disability-user validation. Do not label a local automation demo as that validation.

## 2. “Infer every appliance and reduce bills using only existing smart-meter data”

**Source-supported observation and prior art.** NILMTK is an existing open-source toolkit whose original publication dates to 2014. A current author-maintained NILMBench2026 page reports evaluation of 16 models, three datasets, and two resolutions, and reports substantial deterioration on unseen buildings and datasets. These are authors' results, not reproduced results from this investigation. [NILMTK](https://github.com/nilmtk/nilmtk), [NILMBench2026 author page](https://nilmtk.github.io/nilmbench/paper.html) (retrieved 2026-10-03; publication status of the 2026 conference claim not independently verified).

**Hard limit, with an executed synthetic witness.** Aggregate power is many-to-one. Without additional assumptions or observations, distinct appliance realities can be identical at the meter. I executed:

```python
import numpy as np
a = np.array([0, 1000, 1000, 0, 1000, 0], dtype=float)
b = np.zeros_like(a)
c = np.array([0, 500, 500, 0, 500, 0], dtype=float)
d = c.copy()
print('observed aggregate equal:', np.array_equal(a+b, c+d))
print('world A appliance energies in sample-watts:', float(a.sum()), float(b.sum()))
print('world B appliance energies in sample-watts:', float(c.sum()), float(d.sum()))
print('max aggregate difference:', float(np.abs((a+b)-(c+d)).max()))
```

Observed output, exit code 0:

```text
observed aggregate equal: True
world A appliance energies in sample-watts: 3000.0 0.0
world B appliance energies in sample-watts: 1500.0 1500.0
max aggregate difference: 0.0
```

The arrays are artificial, not measured households. The result proves non-identifiability for an unrestricted aggregate-only claim; it does not measure the prevalence of ambiguity or refute useful probabilistic estimation under realistic priors. Extra current/voltage features, submetering, user labels, or household-specific training change the problem and their costs must enter the claim.

**Demand gap.** Appliance prediction accuracy is not evidence of lower bills. The intervention must identify an affordable action, distinguish avoidable use from necessary use, and show a benefit exceeding equipment and setup costs. None of those benefits was established here.

**Falsifier.** Freeze a household-held-out split before fitting anything; compare with NILMTK baselines and simple consumption summaries. Include absent appliances and unfamiliar devices, report abstention/coverage as well as error, and explicitly charge for calibration and extra sensors. Only then test whether recommendations change a household decision. Random windows from the same household are insufficient evidence for a universal deployment claim.

## 3. “Automatically build and maintain trustworthy maps for underserved places”

**Source-supported problem.** In a 2021 operational account, HOT described a mismatch between the number of mappers and the number of validators; it described validation as both quality assurance and mapper mentoring. The historical staffing claim must not be presented as a current count. [HOT: Validators making an outsized contribution](https://website.hotosm.org/en/news/validators-experienced-mappers-making-an-outsized-contribution/) (2021-05-24; indexed primary-source text retrieved 2026-10-03; direct page fetch timed out).

**Prior art.** HOT Tasking Manager already organizes mapping and validation work. HOT announced production availability of fAIr, its AI-assisted mapping service, in 2024. “Open-source map annotation plus humans” therefore is not a new mechanism. [Tasking Manager documentation](https://hotosm.github.io/tasking-manager/), [fAIr production announcement](https://www.hotosm.org/en/news/fair-in-production-is-available-for-everyone/) (announcement describes a 2024-05-31 release; retrieved 2026-10-03).

**Coordination and maintenance constraints.** OSM's import guidelines require conflation and address already deleted objects, demolished buildings, and mismatched existing features. They call for documenting the import and community review; they also explicitly name JOSM conflation and QGIS as existing tools. [OSM Import Guidelines](https://wiki.openstreetmap.org/wiki/Import/Guidelines) (page last edited 2026-09-09; retrieved 2026-10-03).

**Adversarial inference.** A detector can increase the validation backlog or resurrect correctly deleted data. More geometry is not necessarily a better map. Matching objects across versions, managing provenance and age, and accounting for local knowledge can dominate model inference cost. Volunteer cleanup is a real operating cost even if no invoice arrives.

**Falsifier.** On an offline snapshot, compare a proposed workflow with current JOSM/Tasking Manager practice. Seed duplicate, demolished, previously deleted, and category-mismatched features. Measure correctly resolved cases per reviewer-minute and unresolved severe errors, including review and correction time. No upload is needed. Historical validator bottlenecks justify studying this metric; they do not validate demand for a new standalone tool.

**Residual status.** Reducing qualified-review time is a credible problem hypothesis. I do not nominate a tool: this pass did not establish an unmet mechanism or acquire permission and participants for a representative reviewer study.

## 4. “Capture any computation once and reproduce it forever”

**Prior art.** ReproZip was published in 2013 and already traces system calls, captures dependencies and configuration, and bundles experiments for another environment. Current documentation describes Linux capture with multiple unpacking methods, including virtual-machine approaches. [2013 ReproZip paper page](https://www.usenix.org/conference/tapp13/technical-sessions/presentation/chirigati), [current ReproZip documentation](https://docs.reprozip.org/en/latest/) (retrieved 2026-10-03).

**Documented limits.** ReproZip's FAQ states that remote servers are not captured by tracing a local client; database data may need explicit inclusion; it does not save the pre-execution state of files modified during tracing; graphics replay can depend on matching hardware/drivers; it cannot automatically connect captures from multiple machines. [ReproZip FAQ](https://docs.reprozip.org/en/latest/faq.html) (living documentation, retrieved 2026-10-03).

**Adversarial inference.** A successful replay only establishes the tested execution under its recorded conditions. It does not establish coverage of unexecuted paths, correctness of scientific assumptions, possession of remote data, or future availability of every dependency. A recorder cannot archive a resource it never obtained.

**Second prior-art trap.** “Perturb the environment to expose hidden dependencies” also has direct precedent. `reprotest` already varies aspects such as build paths, locale, file order, and hostname for reproducible-build checks. [Reproducible Builds: adding build variance](https://reproducible-builds.org/docs/adding-build-variance/) (living documentation, retrieved 2026-10-03).

**Falsifier.** Create ten tiny known-ground-truth computations: local pure program; absolute path; time; randomness; locale; unrecorded input; mutable database; remote request; missing library; multi-process state. Compare with ReproZip and reprotest where applicable. Block network, remove caches, vary environment, and assess correct dependency diagnosis and successful restored output, not merely package creation. A missing capability warrants an upstream patch before assuming a new platform is necessary.

## 5. “A universal local-first layer makes every application work offline and sync safely”

**Prior art.** Ink & Switch's 2019 local-first essay discusses CRDTs and Automerge, including preserving conflicting concurrent values for application/user resolution. Cambria, published in October 2020, implements bidirectional schema translations and demonstrates collaboration between schema versions. [Local-first software](https://www.inkandswitch.com/essay/local-first/), [Project Cambria](https://www.inkandswitch.com/cambria/) (retrieved 2026-10-03).

**Adversarial inference.** Deterministic convergence is not preservation of every business invariant or of user intent. Two offline actors can each make a locally acceptable reservation that exceeds one shared capacity when combined. Avoiding the violation needs an explicit policy—coordination, prior allocation of rights, rejection, or compensation—and each changes the user promise. Schema versioning and access policy are additional product responsibilities, not solved by selecting a replicated container.

**Falsifier.** Test concurrent deletion/edit, duplicate identity, capacity reservation, schema upgrade/downgrade, and a device returning after a long partition. Specify expected user-visible outcomes before choosing a data type. Compare the result with existing CRDT libraries and a simpler single-writer/offline-queue baseline. Any benchmark reporting only convergence or operations per second leaves the hard product claim untested.

## Reusable adversarial protocol for the next round

This is a proposed protocol, not an experiment already run. Only the aggregate-power witness above was executed.

1. **Write a falsifiable claim card.** Name one user, one recurring task, their current workaround, the proposed mechanism, the minimum meaningful improvement, and its permitted inputs. Replace “universal,” “automatic,” and “safe” with explicit scope. Name an observable failure that would stop development.
2. **Search for the same mechanism under three vocabularies.** Search the user's vocabulary, the academic term, and the infrastructure term. Open implementation docs and limitation sections. Include abandoned attempts. A missing search result is not novelty evidence.
3. **Build the strongest cheap baseline.** Configure an established open-source project, a short script, and a manual workflow where feasible. Count setup and repair time for all alternatives. Failure to install a rival once does not establish inferiority.
4. **Test information sufficiency first.** Construct two underlying realities that give the proposed system the same input but need different outputs. If possible, either narrow the claim, request another observation, or permit abstention. More computation cannot resolve identical inputs by itself.
5. **Prepare 20 small cases before implementation.** Eight ordinary cases, six boundary/adversarial cases, and six held-out cases from another source or context. Store source/license, ground truth, rationale, and hashes. Synthetic cases can reject a universal assertion but cannot establish real demand or deployment performance. Keep holdout answers unavailable to the implementation author when possible.
6. **Measure task outcomes and transferred labor.** Record correctness, severe-error rate, abstention coverage, elapsed time, human review/correction time, setup steps, peak RAM, disk, and external dependencies. Review time belongs in total cost. For preliminary timing, repeat at least three times and preserve all raw runs; report small-sample uncertainty instead of significance theater.
7. **Run withdrawal and change tests.** Remove the internet, a cache, an upstream service, and an assumed clean input; change one schema/version; let an old client return. Determine who repairs the failure and whether previously correct output becomes silently wrong.
8. **Use a predeclared kill gate.** Suggested exploratory gate: proceed only if the candidate preserves or improves severe-error outcomes and improves a relevant task metric by at least 30% on held-out cases, including setup and correction costs. This threshold is a proposed decision heuristic, not a validated law. A 30% gain on a trivial task or an irrelevant proxy does not count.
9. **Separate technical survival from adoption.** After technical survival, seek authorized observation of a real user's existing task. No unsolicited contact was authorized or performed in this investigation. Without authentic user evidence, mark the result “technical hypothesis survives,” not “useful product validated.”
10. **Prefer a contribution when the missing step is small.** If a plugin or patch to an existing project delivers equivalent value, test that route. A new repository is not itself differentiation.

All preliminary cases can be designed around the supplied limits: CPU-only, small files, less than 1 GiB working RAM per experiment, and bounded runtimes. Full NILM training, representative assistive-technology testing, or production humanitarian validation are not implied by these local capabilities.

## Search record and uncertainty

Representative executed search strings:

```text
site.w3.org WAI evaluating web accessibility tools cannot check all
site.github.com dequelabs axe-core incomplete manual review
site.w3.org ARIA AT project test assistive technologies
site.github.com NVAccess nvda screen reader test automation
NILM generalization unseen households benchmark primary paper cross dataset evaluation
site.github.com nilmtk nilmtk
site.hotosm.org mapping data validation local knowledge challenges
site.openstreetmap.org wiki Import Guidelines community consultation
site.hotosm.org fAIr validation mapping AI human in the loop
site.github.com hotosm map validation prioritization quality assessment tasking manager
ReproZip limitations network hardware GPU reproducibility documentation
site.reproducible-builds.org reprotest variations environment test reproducible
site.datalad.org reproducible executions rerun
site.guix.gnu.org reproducible research containers
site.inkandswitch.com local first software sync conflicts CRDT
```

Retrieval date for all sources: 2026-10-03. Search snippets sometimes report inconsistent relative publication/crawl dates; dated claims above use explicit source dates where visible. Undated documentation is identified as living documentation. Search results from Reddit and Wikipedia were not used as technical evidence. Some searches found additional related systems, but only inspected evidence is used to support decisions here.

This is a time-bounded adversarial sample, not an exhaustive survey. It is biased toward mechanisms with inspectable public documentation and therefore toward software-adjacent opportunities, despite including energy, accessibility, and humanitarian mapping. It establishes neither the absence of novelty nor the absence of demand in any field. It establishes concrete reasons to reject five broad claims and gives the next investigator inexpensive ways to test narrower ones.
