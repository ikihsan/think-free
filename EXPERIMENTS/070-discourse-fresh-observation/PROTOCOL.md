<!-- origin-meta
owner: EXPERIMENTS/PLAN.md
status: active
last-verified: 2026-10-08
-->

# E070 — Fresh observation in non-software domain via Discourse forums

Session `2026-10-08-028`, VM `instance-20260717-0944`, declared 2026-10-08.

## The question

Every population this mission has measured for candidate need comes from one route (software venues: GitHub, PyPI, HN, Stack Overflow) or one platform confound (Stack Exchange's non-software sites, whose members are technical enough to be on a software-shaped platform). **Seven measurements say the seat for a candidate is empty** (F029, F051, F039, F059, F081, F084, F085). E062/E069 measured non-software Stack Exchange and found: 17 of 20 top-arrival unremedied needs are served by a free general assistant today, and the view_count instrument generalizes (100% VC-positive, 14% unserved-open-like). But the Stack Exchange confound remains: its users are a self-selected technical population.

This experiment measures the discriminator E062 named but could not test: **a genuinely non-technical population on a different platform**. Discourse forums host communities for cooking, automotive repair, woodworking, photography, gardening, home improvement — users who are there for the hobby, not for technical Q&A. The platform records view_counts, has different mechanics (likes/bookmarks/solved-plugin instead of accepted answers), and the outcome channel is measurable.

### The candidate decision this changes

Stated in advance, because an audit of a discovery method is only worth running if it moves a decision (owner brief §4).

- **If the Discourse unserved-open fraction is materially higher than Stack Exchange non-software (14%) and software (0%)**, the mission's candidate source moves to this domain, and the next session harvests candidates from Discourse forums. This is an executable action.
- **If it is comparable or lower**, then the emptiness is not a platform artifact — the find-a-new-venue route remains deferred (not closed, per D083, because E062's null branch was an artifact of its rubric). The instrument (view_count + unserved-open) is validated on a third platform, which is itself a durable gain.

Either result is a decision, and neither result is a candidate. **This experiment is not expected to produce a product, and the README must not imply that it did.**

## Population and arms

| arm | source | domain | what it carries |
|---|---|---|---|
| **1 (treatment)** | Discourse forums: 5+ non-technical communities, ≥ 100 topics each with view_count and outcome status | varied (cooking, automotive, woodworking, photography, gardening, home improvement) | title, body, view_count, likes, replies, solved-status, tags, creation_date |
| **2 (control)** | E062 non-software Stack Exchange corpus (110 no-remedy rows, raw/noremedy-classified.tsv) | non-software on SE platform | title, body, view_count, is_answered, accepted_answer_id, closed_reason, score, tags |

**Why Discourse, and why it is not interchangeable with Stack Exchange.**
- Different platform mechanics: flat/threaded replies, likes/bookmarks, "solved" plugin (not accepted answer), trust levels, no reputation gatekeeping
- User base: hobbyists who joined for the topic, not programmers who happen to cook/ride bikes
- Public API: standardized across instances, returns view_count, like_count, reply_count, solved status
- Outcome channel: "solved" status (via discourse-solved plugin) or reply_count + like_count on OP as proxy
- Multiple independent instances: each forum is a separate community, reducing platform-level confounding

**The confound I can name in advance.** Discourse forums often have a "solved" plugin but not all enable it. Where absent, I'll use a heuristic: topic has ≥ 3 replies AND OP has ≥ 1 like on a reply as "resolved". This is declared as a limitation, not a gate failure.

## Gates, all declared before any row is fetched or read

| gate | condition | if not met |
|---|---|---|
| **G1 retrieval** | ≥ 500 topics across ≥ 5 distinct Discourse instances, each carrying title, body, view_count, like_count, reply_count, solved-status (or proxy), tags, creation_date; harvest reconciled against each instance's reported topic counts | the route is not measurable at this cost. Stop; record the ceiling. |
| **G2 control validity** | the reader separates 40 seeded control statements — 20 known unserved-open-like (from E069's 7 unserved-open-like rows), 20 known served-like — at ≥ 0.85 accuracy | the rubric is not usable and the fraction is not measurable. Stop. |
| **G3 the measurement** | the unserved-open-like fraction of arm 1 (unremedied topics), with Wilson CI95, over ≥ 500 topics; and the same fraction over arm 2's 110 no-remedy rows | this is the result; no gate |
| **G4 view_count validation** | ≥ 95% of harvested topics have view_count > 0 (independent arrivals observed), matching E069's 100% VC-positive rate | the view_count instrument does not generalize to this platform. Record the gap. |

**Positive control, stated as a requirement on the instrument, not on the world:**
the reader must recover seeded positives (G2). A rubric with no positive control is the shape F029 took — 50 candidates screened, 0 survived, and the screens never demonstrated they could find one.

**Denominators.** Every fraction is over rows read, and rows not read are reported as rows not read. Per D082, an arm that produced no observation is a missing observation, never a zero and never a denominator.

## The rubric, written before the rows

A topic is **unserved-open-like** when all three hold:

1. **No platform-recorded resolution** — solved-status is false/absent, AND (reply_count < 3 OR no reply has like_count ≥ 1 from OP)
2. **States a concrete need** — title or body asks for a technique, material, product, source, diagnosis of a physical artifact, or judgement about safety/quality (not a discussion, show-off, or meta question)
3. **Not a request for content, service, price, access, or human work** — same as E062 clause 3, but "the requester's own data" in a physical domain means their physical artifact (their car, their stain, their plant), which is expected and not disqualifying. **This clause is revised from E062**: physical-domain needs inherently consume the requester's physical input; that does not make them un-tool-shaped. The disqualifier is whether a program would need *private data the requester holds but cannot share* (account credentials, private repo, proprietary spec sheet not in public domain).

**Two readers** on an overlapping subsample (20% of unremedied topics, minimum 30), with κ reported, because E023's withdrawal (F043, D055) and E029's reader arm failure (F049) showed single-reader classification is unreliable.

## Sub-test: answerability of top-arrival unremedied needs

Declared before any row is labelled, per E062 AMENDMENT-2:

Read the top 20 unremedied topics by view_count (arrival) and attempt each one against the **strongest accessible alternative** — a general-purpose assistant answering from its own knowledge, free and instant. Each row labelled with what that alternative can and cannot supply. Written to `raw/answerability-top20.tsv`.

Labels: `resolved-from-knowledge`, `resolved-needs-per-model-spec`, `unresolved-no-public-data`, `unresolved-human-work`, `unresolved-other`.

**Falsifier.** If a general assistant resolves most top-arrival unremedied needs, the candidate space in this population is served and there is nothing here to build. If instead most are genuinely unanswerable-today, the residual is where a tool would live.

**Named asymmetry.** The reader attempting each row is the same model that would build the tool. It is also the free, instant incumbent. The finding is bounded by the *incumbent* framing: the question is whether a gap exists between what a free general assistant supplies and what the requester needed.

**Sample.** Arrival-ranked top 20 of unremedied topics, all instances, read in full. Not random: arrival rank is the only ordering that separates widely-felt unremedied need from a one-off.

**Ceiling.** 20 rows, multiple instances, one stratum, one reader that is also the proposed builder, questions of varying age. Measures whether *today's* unremedied population is served by *today's* incumbent.

## Ceiling, stated now

One platform (Discourse) across multiple independent instances; one retrieval route (public API); one rubric with two readers over a subsample; and communities whose members are self-selected for the hobby. This measures the *shape* of non-technical populations' unmet need on a non-Stack-Exchange platform. It does not measure demand, does not measure adoption, and does not close any candidate.

## Reproduce

```bash
python3 EXPERIMENTS/070-discourse-fresh-observation/harvest.py     # arm 1, Discourse forums
python3 EXPERIMENTS/070-discourse-fresh-observation/outcome.py     # every gate above
```

Needs internet access for Discourse API calls, and Python 3.8+ with `requests` or `urllib`.

## Discourse instances to harvest (pre-registered)

Selected for: non-technical domain, active community, public API enabled, discourse-solved plugin or measurable engagement.

1. **community.opencooper.com** — OpenCooper (automotive/cooper) — *verify domain*
2. **discourse.ubuntu.com** — too technical, exclude
3. **forum.prusa3d.com** — 3D printing (borderline technical, but hobbyist)
4. **community.silabs.com** — too technical
5. **forum.freecad.org** — too technical
6. **discourse.gnome.org** — too technical
7. **meta.discourse.org** — meta, exclude

**Need to identify 5+ genuine non-technical Discourse instances.** Will probe candidate domains before harvest.

Candidate domains to probe:
- Cooking/food: `community.anovaculinary.com`, `forum.seriouseats.com` (check if Discourse)
- Automotive: `forums.tdi.club` (check), `forum.miata.net` (check)
- Woodworking: `forum.sawmillcreek.org` (check), `woodworking.talk` (check)
- Photography: `discuss.pixls.us` (Discourse, raw photography), `forum.fujixforum.com` (check)
- Gardening: `garden.org` (check), `forums.gardenweb.com` (check)
- Home improvement: `community.homeassistant.io` (technical), `diychatroom.com` (check)
- Coffee: `forum.home-barista.com` (check), `discourse.decentespresso.com` (Discourse, espresso)
- Mechanical keyboards: `geekhack.org` (SMF, not Discourse), `keebtalk.com` (Discourse, but technical hobby)

**Actual instance list will be finalized in harvest.py after probing.** The protocol declares the selection criteria, not the specific URLs, to avoid cherry-picking.