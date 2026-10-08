# E057 — Outside developer tooling, does one practical step recur and go unserved?

<!-- origin-meta
owner: EXPERIMENTS/PLAN.md
status: active
last-verified: 2026-10-08
-->

## Question

In a non-developer-tool practice population observable as public artifacts,
is there a **step** that (a) recurs across distinct practitioners, (b) is
currently done by hand or by a general-purpose tool whose own output cannot
show whether the result is right, and (c) is left unserved by incumbents
enumerated from the population's own vocabulary?

## Why this question, and not another screen

The candidate seat is empty and every candidate this mission has produced came
out of this mission's own priors: six sealed reports, sixteen candidates, and
`RESEARCH/SYNTHESIS.md` §4 records that four independent reports share one
model's priors, so agreement among them is weak evidence. Six invention claims
have been tested and none validated. Re-screening the prior-derived list a
seventh time cannot fix a generator that produced the list. So this experiment
does not screen; it observes an **independent population** and reads what that
population says it cannot do (D080).

## Population, and the rule that picks it

**Stack Exchange, all 365 sites, enumerated from the API's own site list**
(`api.stackexchange.com/2.3/sites`), one fetch per 250 sites. A site is
excluded when its name contains any token in the published list below, and no
other criterion is applied. From the survivors, the **12 alphabetically first**
are the population — chosen before any question text is read, so the sample is
not the one that looks promising.

```
meta | language | linguist | software | linux | ubuntu | unix | windows | server |
web | code | program | develop | devops | android | ios | apple | google |
language | mathemat | physic | chemi | bioinformat | comput | cryptograph |
signal | data sci | artificial intelligence | llm | quantum | robot | blender |
game | arduino | raspberry | internet of things | bitcoin | ethereum | cardano |
stack | dba | ux | graphic | video | music | sound design | the workplace |
project management | drupal | joomla | magento | salesforce | sharepoint |
sitecore | wordpress | network engineering | information security |
hardware recommendations | vi and vim | emacs | tex | elementary |
retrocomput | open source | open data | geographic information |
operations research | quantitative | econom | politic | history | literature |
philosoph | buddhis | christian | hindu | islam | mytholog | skeptic |
anime | poker | board | card | chess | proof assistants | worldbuilding |
puzzling | academia | ask different | my yodeya | mi yodeya
```

Two of these exclusions are known over-reach and are declared as such:
`music` (Practice & Theory) and `retrocomput` are not developer tooling, and
their absence is a ceiling on this run, not a claim about them.

## Stratum

Questions **open** (`closed=no`) with **no accepted answer** (`hasaccepted=no`),
`pagesize=100`, descending and ascending by `votes`, restricted to 36 months.
The stratum is defined by *unanswered*, not by score. The ascending arm is the
score tail, because E033 measured recurrence at 4.5× the Active tab's rate in
the tail and near zero in the top-voted tertile; the descending arm is that top
tertile and serves as **control B1**.

## Gates, declared before the fetch

| gate | condition |
|---|---|
| **G1 population** | a cluster of the same step across **≥8 distinct users in one site**, or **≥5 distinct users across ≥2 sites** |
| **G2 serving** | an enumeration built from the population's own vocabulary names **0** incumbents that perform the step |
| **G3 verdict** | the step's correctness is decidable from artifacts, and **no incumbent's primary output reveals it** (D081) |

**Decision rule: build nothing unless G1, G2 and G3 all hold for the same
cluster.** `KILL` if G1 fails for every cluster, or if G2 fails for every
cluster that passes G1.

## Ceilings, declared before the fetch

1. **One site family, English, self-selected questioners, and a question is a
   *formulable* need.** F060 measured on this corpus's parent that it answers
   57% of its statements and names anything new in 0 of 1391. A null here
   therefore does **not** establish that no such step exists; it establishes
   that this channel does not show one.
2. **Title-level clustering reads a question's framing, not its practice.** A
   cluster is a hypothesis to be read, never a finding.
3. **36 months, one stratum, 12 sites, 100 questions per arm.** The exclusion
   list is a set of priors and is published above so it can be argued with.
4. **No user is contacted and nothing is published.** Reading public text is
   the whole instrument.

## Reproduction

```
python3 EXPERIMENTS/057-unserved-step/fetch.py     # writes raw/sites.json, raw/*.json
python3 EXPERIMENTS/057-unserved-step/cluster.py   # writes raw/clusters.json
```
