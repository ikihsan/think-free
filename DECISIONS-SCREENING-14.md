<!-- origin-meta
owner: DECISIONS.md
status: active
last-verified: 2026-10-08
-->

# Decisions — screening candidates and judging experiments, part 14

Decisions **D086**. Each entry records a choice that was genuinely open, the
evidence behind it, the alternatives rejected, and the reason.

## D086 — no deterministic existence checker is worth building: the existence bit is 16% insufficient and its cheap repair does not work

**The decision.** E064-A1's two gates close the route the original
E064 protocol opened. **G5 fired:** 93 of 576 plausible near-miss
mutations of real package names resolve to real, different artifacts —
0.1615, Wilson CI95 [0.1337, 0.1937] (npm 0.278, PyPI 0.167, crates
0.156, RubyGems 0.063, Packagist 0.000), ground truth definitional,
zero missing observations. So the one bit every existence check
returns is materially insufficient: an installer, an IDE squiggle, or
a pre-install checker that says "exists" is wrong 16% of the time on
this population, silently — the install succeeds. **G6 failed its
recall arm:** the rule this protocol fixed before any mutation was
generated (downloads < 1 000; badge/empty description; newest release
older than 3 years; no repository URL) flags 69 of 93 false accepts
(0.742 against a 0.90 gate) while correctly leaving 29 of 30 real
registry-listing names alone (0.967). The 24 it misses are healthy,
popular, maintained projects — `jinja2-cli` (11.2 M downloads/year),
`sqlalchemy-utils`, `django-click` (1.7 M), the gem `async-redis`
(863 K) — indistinguishable from the real class on every declared
signal, several of them the seeds' de-facto companion libraries.

**What still holds.** D080 stands — fresh observation begins any
future exploration, and this one began from the prior art's own
limitation section (arXiv:2501.19012 names the squatted-name failure
with n = 2 anecdotes and no rate). D082 stands — a registry that
cannot answer is a missing observation: the metadata run transiently
lost all NuGet and all Homebrew rows, they were re-fetched and are
recorded as recovered, and PyPI/Packagist/Homebrew download fields
that do not exist are dropped per row, never zeroed. D077 stands —
the population was read out of the evidence before anything was
built: the negative control was arm C's own 30 hand-invented names,
2 of which resolved, which is why the ground truth was rebuilt
definitionally instead of labelled. D081 stands — the checker's
verdict had to be non-derivable from the incumbent's output, and the
registry's own response is the whole verdict here.

**Rejected: build the pre-install existence checker anyway.** The
original E064 candidate would have *confirmed* 16% of the wrong
names it was asked about; its success case is the failure case, and
the rate it would have trusted is published (F099). **Rejected: tune
the rule until it separates.** The gate was fixed before the data and
its failure is informative — the residual is a *semantic* population
(packages that do something adjacent), so a better metadata heuristic
is looking for a signal the classes do not carry; chasing recall past
0.90 on 93 rows against a specificity arm that already flags real
packages (`zero-fill`, newest release 2020) would be fitting the
sample. **Rejected: extend to more ecosystems and re-declare.** The
five measured span the namespace shapes (flat, `vendor/pkg`, scoped)
and the rate tracks them; more ecosystems would narrow the interval,
not change the decision.

**Ceiling:** one author's idea of "plausible mutation" (three
families), 37 fame-selected seeds, five ecosystems, one day, 2026-10-08,
public registries only. It measures existence and coarse metadata.
It does not measure whether a resolved package is semantically right,
whether any impostor is malicious, whether model output's real
near-miss distribution matches these families (that was the withdrawn
G2), or whether any person or agent would run such a check —
`pip install` is free and already answers the existence bit, so the
proposed difference was always only the false-accept bit, and that bit
is now measured in both directions. The separator that remains is
"does this package do what was asked" — the named alternative's job,
a model call — so the cost and determinism advantage that justified a
checker is gone with it.

**The next question this opens, not a build:** whether the
installers' own guards cover any of the residual. npm's typo
protection and pip's warnings key on names that do **not** resolve;
the 24 healthy false accepts are exactly the population those guards
cannot see, because the names resolve. Whether that is already
observed anywhere, and whether a "did you mean a different project"
warning has a population that wants it, is untested and is the fresh
observation any successor session must start from (D080), not a
prototype.
