<!-- origin-meta
owner: RESEARCH.md
status: sealed
last-verified: 2026-10-03
-->

# Investigation E — experimental engineering

Independent report. Written 2026-10-03 after reading `MISSION.md` only. The
other reports (A–D) were not read before writing; where their hypotheses
surface here it is a coincidence the reader should test, not an input.

## Scope and machine reality

This report does not survey the world. It answers one question: which
mechanisms can be subjected to a *cheap, hard* experiment on this machine
(12 CPUs, ~15 GiB RAM, stdlib Python plus NumPy, public internet, no GPU,
no proprietary services)? A mechanism qualifies only if the experiment that
could kill it is smaller than the argument for keeping it.

All results below are `untested`. What is described is the observation, the
mechanism that would explain it, what we assume, what prior art says, the
strongest objection, the smallest falsifying experiment, and the epistemic
limits of what that experiment could show.

## Mechanism E1 — retry storms are a synchronization failure, not a load failure

**Observation.** When a dependency fails, clients often retry on fixed or
short delays. Anecdotally, outages outlast the root cause by minutes, and
recovery is sawtooth rather than monotonic. `source-supported` (fleet
postmortems describe this pattern; see prior art).

**Mechanism.** Correlated retries re-synchronize the failing population:
all clients wake together, overload the recovering service, and get
rejected again together. Bounded exponential backoff *with jitter* breaks
the correlation, turning a deterministic convoy into independent arrivals.

**Assumptions.** Retries are the dominant post-root-cause load; clients
share similar timers; the service has a sharp knee.

**Prior art.** AWS Architecture Blog, "Exponential Backoff And Jitter"
(Marc Brooker, 2015, retrieved 2026-10-03); Netflix Hystrix documentation.
The idea is known; what is untested is the cheap claim that jitter, not
backoff alone, does the work.

**Strongest objection.** Modern client libraries already add jitter by
default, so there is nothing left to build or test.

**Smallest falsifying experiment.** Deterministic discrete-time simulator,
stdlib Python, ~100 lines: N clients, one server with capacity C, failures
injected as a window of overload. Arms: (a) fixed delay, (b) exponential
backoff, (c) exponential backoff + uniform jitter. Metrics: time-to-full
recovery p50, total rejected requests during recovery. Kill gate: if (c) is
not decisively better than (b) (say, >2x recovery time or >10x rejected
load) at equal mean retry rate, the mechanism as stated is noise on this
machine and should be dropped.

**What would make it uninformative.** A simulator cannot be evidence about
real services; it can only falsify the *internal consistency* of the
mechanism. A positive result is a license to build a real fault-injection
test, not a validated claim.

## Mechanism E2 — dependency lockfiles are weak witnesses of reproducibility

**Observation.** Lockfiles (`Pipfile.lock`, `poetry.lock`, `package-lock.json`,
`Cargo.lock`) are treated by users and CI as proof that a build today equals
a build yesterday. Registry-side changes (yanked releases, re-published
wheels for the same version, platform-marker rewrites, transitive metadata
updates) can silently invalidate that proof.

**Mechanism.** The witness is unstable because it records names and
hashes at one instant, while the failure mode is time-varying. A stronger
witness is the *closure*: the sorted set of (name, version, artifact hash,
source URL) tuples actually installed, recomputed and diffed across time.

**Assumptions.** Registries mutate or yank at a non-trivial rate; hash
pinning covers artifacts but not the resolution step; most projects never
re-verify.

**Prior art.** PyPA `pip` documentation on hash-checking mode; the
npm `left-pad` incident (2016); research on dependency confusion (Alex
Birsan, 2021). Prior art supports the instability of names; it does not
measure the *rate* on this machine's ecosystems.

**Strongest objection.** Major registries mostly forbid re-publishing the
same version, so with hash pinning the closure is in fact stable, and the
proposal measures a rare event expensively.

**Smallest falsifying experiment.** Pick the top-50 PyPI packages by
download; download their locked closures (e.g. via `pip download` with the
current resolver twice, a few days apart, or against two published
lockfiles from different dates), hash each artifact, and count version or
hash changes in the closure. If the closure is bit-stable across the
snapshot, the mechanism is too weak to productize.

**What would make it uninformative.** Two snapshots days apart probe only
fast drift; slow drift (weeks-to-months yanks) is the interesting regime
and requires either archival lockfiles or patience.

## Mechanism E3 — build timestamps are the easiest determinism violation to count

**Observation.** Many `sdist`/wheel artifacts embed wall-clock times
(zip entry dates, `SOURCE_DATE_EPOCH` unset). Reproducible-builds efforts
report this as a leading failure cause. `source-supported` (ReproZip/
reproducible-builds.org reports).

**Mechanism.** Because timestamp embedding is local to the build, it is
cheap to count: build the same source twice with different
`SOURCE_DATE_EPOCH` values and diff the artifact bytes. The population
claim ("this fraction of releases fail determinism because of timestamps")
is measurable from a sample.

**Assumptions.** Public artifacts carry their timestamps in a detectable
place (zip header dates, embedded strings); the sample is representative.

**Prior art.** Debian reproducible-builds project, `SOURCE_DATE_EPOCH`
spec (reproducible-builds.org, retrieved 2026-10-03), reprotest tool.
The mechanism is known; the untested claim is the *size* of the timestamp
component in today's dominant ecosystems, and therefore whether it is
worth fixing first.

**Strongest objection.** Modern wheels are zips with fixed 1980 dates or
`SOURCE_DATE_EPOCH` honored by `setuptools`/`hatchling`, so the timestamp
component is near zero and the counting exercise reports a solved problem.

**Smallest falsifying experiment.** Sample 200 recent PyPI wheels across
ten popular packages; for each, record zip entry date fields and scan the
METADATA/ RECORD for epoch-0 or 1980 normalization. Fraction with
non-normalized timestamps estimates the violation rate. If <5%, E3 is
a weak lead and the experiment ends.

**What would make it uninformative.** A 200-wheel sample cannot bound the
tail of ecosystems (conda, npm tarballs, Maven jars). A decisive count for
PyPI wheels only is a license to broaden, not a census.

## Cross-cutting rules for this repository

1. Every prototype claim in this repository must ship its kill gate next to
   its hypothesis (the current `HYPOTHESES.md` convention). E1–E3 each have
   one above; none has been run.
2. A simulator result falsifies a mechanism; it never validates a product.
3. Prefer experiments whose uninformative case is also informative
   (E2's stable closure kills the candidate cheaply).
4. Absence of a result is not a result. All three mechanisms are `untested`
   and remain so until an experiment is committed with raw output.

## Explicit epistemic limits

- This report cites prior art by name and date retrieved; versions of that
  prior art may change. Every mechanism here could already be solved in the
  current tooling versions; the cheap experiments above are how to check.
- The machine is one x86_64 Linux box; nothing here transfers to ARM,
  Windows, or mobile populations without re-measurement.
- The author shares a model prior with every other agent reading this
  repository. These should be treated as candidates for human-reviewed
  experiments, not conclusions.
- Investigations E and F have no dependency on A–D's hypotheses; if the
  later synthesis finds overlap, it should say so explicitly rather than
  merging the reports.
