<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-12
-->

# E115 M2 — the cases, and the reference answers, fixed before any answer exists

Written 2026-10-12 **before the assistant was asked anything**. `answers.jsonl`
does not exist yet and this file does not depend on it. If the answers later
disagree with the key here, the key is right until shown otherwise by the
cited clause.

## Why these cases and not others

`PROTOCOL.md` required that the correct answer be **computable by hand from
the rule text alone**. That eliminates most real compliance questions, because
most turn on facts no rule states. What survives is the subset where the
regulation supplies the counting rule *and* the fact pattern supplies every
input. That subset is where a mechanical checker is even conceivable, so it is
the right subset to test: if the assistant is right here, the population is
served where a tool could exist at all.

**Selection is not by difficulty.** Every rule in this set was read during M1
and every fact pattern was written from the rule's own counting rule. Cases
that the naive headcount would also get right are included on purpose —
`P1`, `P3`, `P6`, `P9` — because a screen that only contains cases the
incumbent fails would be the F116 shape (a screen over rows it had selected).

## The verbatim rule text, as given to the assistant

Each case names the clauses actually used. Full text is in `parts-title29.jsonl`.

- **F1** — 29 CFR 825.104(a): *"An employer covered by FMLA is any person
  engaged in commerce or in any industry or activity affecting commerce, who
  employs 50 or more employees for each working day during each of 20 or more
  calendar workweeks in the current or preceding calendar year."*
- **F2** — 29 CFR 825.105(b): *"Any employee whose name appears on the employer's
  payroll will be considered employed each working day of the calendar week,
  and must be counted whether or not any compensation is received for the week."*
- **F3** — 29 CFR 825.105(c): *"Employees on paid or unpaid leave ... are
  counted as long as the employer has a reasonable expectation that the
  employee will later return to active employment. If there is no
  employer/employee relationship (as when an employee is laid off, whether
  temporarily or permanently) such individual is not counted."*
- **F4** — 29 CFR 825.111(a): worksite determined by physical proximity and
  shared staff/equipment; *"The workers who have New Jersey as their worksite
  would not be counted in determining eligibility of employees whose home base
  is the Ohio worksite, but would be counted in determining eligibility of
  employees whose home base is New Jersey."*
- **O1** — 29 CFR 1904.1(a)(1): *"If your company had 10 or fewer employees at
  all times during the last calendar year, you do not need to keep OSHA injury
  and illness records"*, and § 1904.1(b)(1): *"The partial exemption for size is
  based on the number of employees in the entire company"*; § 1904.1(b)(2): you
  must determine *"peak employment during the last calendar year"*.
- **O2** — 29 CFR 1904.2(a)(1): the industry exemption applies to *"your business
  establishment ... classified in a specific industry group listed in appendix A"*
  and § 1904.2(b)(1) it *"applies to individual business establishments"*.
- **L1** — 29 CFR 1910.38(b): an emergency action plan *"must be in writing"*,
  but *"an employer with 10 or fewer employees may communicate the plan orally
  to employees."*

## The cases

Each asks one question whose answer is yes/no. `key` is the hand-computed
answer; `why` cites the clause that decides it and is not a judgement about
what a "reasonable" employer would do.

| id | facts given to the assistant | question | key | why |
|---|---|---|---|---|
| **P1** | Private company. Current headcount 200. No other facts. | Covered by FMLA? | **YES** | F1: 200 ≥ 50, and no workweek or day qualifier is violated. The easy direction, deliberately included. |
| **P2** | Private company. Headcount reached 60 during the week of 3 March, and has been 8 employees on every other working day of the past two calendar years. | Covered by FMLA? | **NO** | F1 requires 50+ on **each working day of each of 20+ workweeks**. Only one week qualified. Naive headcount answers "peak was 60, so yes". |
| **P3** | Company has 48 employees on the payroll each week, and has had 48 for the past three calendar years. | Covered by FMLA? | **NO** | F1: 48 < 50. The direction the easy cases agree with. |
| **P4** | Company has 60 employees. 12 of them are currently laid off with no reasonable expectation of return. | Is the employer's headcount for FMLA coverage 60 or 48? | **48** | F3: a laid-off employee with no employer/employee relationship is not counted. 60 − 12 = 48, which is below the threshold. Naive headcount says 60. |
| **P5** | 55 employees are on the payroll for every working day of the past year. Each has appeared on the payroll for the past 18 months, but received no compensation for the most recent 3 weeks (payroll processing delay). Are they counted? | Counted toward the 50-employee coverage test? | **YES** | F2: counted *"whether or not any compensation is received for the week"*. |
| **P6** | A company employs 90 people in Ohio and 90 in New Jersey, in two separate buildings in different cities, with **separate shift supervisors and separate vehicles**. An employee works at the Ohio site. For FMLA eligibility of that Ohio employee, is the New Jersey headcount included? | Included? | **NO** | F4: separate buildings not in proximity and not sharing staff/equipment are separate worksites; the NJ workers "would not be counted in determining eligibility of employees whose home base is the Ohio worksite". |
| **P7** | Same company, same separate-worksite facts, but the employee works at the **New Jersey** site. | Is the Ohio headcount included for that employee's eligibility? | **YES** | F4: NJ-based workers "would be counted in determining eligibility of employees whose home base is New Jersey". |
| **P7b** | A company employs 90 people in Ohio and 90 in New Jersey, in two buildings **900 feet apart, sharing one shift supervisor and one fleet of vans**, used for the same purpose. For FMLA eligibility of an employee at the Ohio building, is the headcount at the New Jersey building a *separate worksite*, or the same worksite? | Same worksite? | **SAME (one worksite, 180 employees)** | F4 as stated in § 825.111(a)(1): buildings in proximity, same purpose, sharing staff and equipment **are a single worksite**. This is the clause that decides it, and it is the opposite direction from P6 — it is in the set to stop the case set from being one-directional. |
| **P8** | A company had 30 employees in March, 30 in April, and 9 in every month since May. | Exempt from OSHA injury-and-illness recordkeeping under 1904.1? | **NO** | O1: the test is **peak employment during the last calendar year**; 30 > 10 at any time. Naive "current headcount is 9, so exempt" is the trap and it is wrong. |
| **P9** | A company has had exactly 10 employees at all times for the past calendar year. | Exempt from OSHA recordkeeping under 1904.1? | **YES** | O1: "10 or fewer ... at all times during the last calendar year". |
| **P10** | A company has 5 employees and 3 establishments. Establishment A is in an appendix-A industry; establishments B and C are not. | Must establishments B and C keep OSHA records? | **YES** | O2: the exemption *"applies to individual business establishments"*, so only A is exempt. Naive whole-company reading says no records anywhere. |
| **P11** | A company has 5 employees and 2 establishments. Establishment A is in an appendix-A industry; establishment B is in an appendix-A industry too. | Must either keep records? | **NO** | O2: both are in listed industry groups. |
| **P12** | A company has 9 employees. It has exactly one establishment. | May its emergency action plan be communicated orally rather than in writing? | **YES** | L1: "an employer with 10 or fewer employees may communicate the plan orally". |
| **P13** | A company has 11 employees. It has exactly one establishment. | May its emergency action plan be communicated orally? | **NO** | L1: the written requirement binds above 10. |

## The reference key, committed

**14 cases: 6 YES, 8 NO** (answers: YES NO NO NO YES NO YES **SAME** NO YES YES YES NO NO).

**Of the 14, the naive headcount reading gets 8 right and 6 wrong** (P2, P4,
P6, P8, P10, and P7b in the opposite direction). Those six are the population
the counting rule creates, and this file is where the claim "6 of 14" comes
from. That figure is a property of **these cases**, not of the world, and is
not to be quoted as a rate.

## What the assistant is given

For each case: the verbatim clause(s) in `## The verbatim rule text` above
relevant to that case, the facts, and the question. No instruction about what
the question is testing, no mention of the key, no mention of counting rules.

## Known ceiling on this design

The assistant and the reference key were written by the same agent. That is a
single reader with no second coder, and this record has been burned by that
before (F049: a reader who labelled 222 correct ids in the wrong order). The
mitigation available here is that every `key` cites a clause and can be checked
against the committed regulation text without trusting me — which is a weaker
guarantee than a second coder and stronger than an assertion.