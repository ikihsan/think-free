"""E034 — behavioural checks for the reader, and the runner that proves they can fail.

PROTOCOL.md section 3 is a claim about *which end of the score distribution each arm
reads*, and F055 is this mission's record of a selection parameter that did not do what
the author believed (E032's `sort=votes`, which prefers answered questions and is 4.5x
rarer in duplicate closures than the tail). So the checks below are aimed at the arms
and the label, not at the arithmetic: an arm that silently reads the wrong end, or a
label that counts a missing `closed_reason` as a duplicate, would produce a plausible
report and a wrong one.

`python3 check.py` runs the checks and then the falsification: each mutation below is
applied to a copy of reask.py in a temp directory and the checks are re-run against it.
A mutation that still passes is a blind spot in this file and is reported as such.
"""

import collections
import importlib.util
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def _load(path=None, name="reask_under_test"):
    path = path or os.path.join(HERE, "reask.py")
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def check(reask):
    """Returns a list of (name, ok, detail). Every failure is a wrong report, not a crash."""
    out = []

    def rec(name, ok, detail=""):
        out.append((name, bool(ok), detail))

    # 1. The arms must be different requests. If `tail` and `head` were the same URL the
    #    pooled comparison would be one arm counted twice and every gate would be green.
    tail = reask.url_for("stackoverflow", "git", "tail", 1, 25)
    head = reask.url_for("stackoverflow", "git", "head", 1, 25)
    default = reask.url_for("stackoverflow", "git", "default", 1, 25)
    rec("tail is sort=votes order=asc", "sort=votes&order=asc" in tail, tail)
    rec("head is sort=votes order=desc", "sort=votes&order=desc" in head, head)
    rec("default is sort=activity order=desc", "sort=activity&order=desc" in default, default)
    rec("the three arms are three distinct URLs", len({tail, head, default}) == 3)
    rec("page is carried in the URL", tail.endswith("&page=1"), tail)
    rec("the declared tag list is the protocol's eight, in declared order",
        [t[2] for t in reask.TAGS if t[2] in reask.DECLARED_TAGS]
        == reask.DECLARED_TAGS, str(reask.DECLARED_TAGS))
    rec("the declared list has eight tags", len(reask.DECLARED_TAGS) == 8)
    rec("every declared tag appears in TAGS",
        set(reask.DECLARED_TAGS) <= {t[2] for t in reask.TAGS})
    declared_strata = collections.Counter(t[0] for t in reask.TAGS
                                          if t[2] in reask.DECLARED_TAGS)
    rec("every stratum has exactly two declared tags",
        all(v == 2 for v in declared_strata.values()) and len(declared_strata) == 4,
        str(dict(declared_strata)))
    amended = [t[2] for t in reask.TAGS if t[2] not in reask.DECLARED_TAGS]
    rec("AMENDMENT-1 added exactly the two R2 tags, one per site",
        sorted(amended) == ["baggage", "calculus"]
        and len({t[1] for t in reask.TAGS if t[2] in amended}) == 2, str(amended))
    rec("no tag was visited twice",
        len({(s, t) for _st, s, t in reask.TAGS}) == len(reask.TAGS))

    # 2. Wilson against a published reference. k=54, n=1000 is E033's headline and its
    #    published CI95 is [0.0416, 0.0698]; if this drifts, every gate below drifts.
    lo, hi = reask.wilson(54, 1000)
    rec("wilson(54,1000) reproduces E033's published CI95",
        abs(lo - 0.0416) < 5e-5 and abs(hi - 0.0698) < 5e-5, "[%.4f, %.4f]" % (lo, hi))
    rec("wilson(0,0) is undefined, not zero",
        reask.wilson(0, 0) == (None, None), str(reask.wilson(0, 0)))
    rec("wilson(0,100) has lower bound 0 and no negative width",
        reask.wilson(0, 100)[0] == 0.0 and reask.wilson(0, 100)[1] > 0.0)

    # 3. The label. A missing closure reason must not become a duplicate closure: that
    #    single imputation would inflate every rate in the run and no gate would notice,
    #    because the gates only compare rates to each other.
    rows = [
        {"closed_reason": "Duplicate", "score": 0},
        {"closed_reason": None, "score": 1},
        {"closed_reason": "OffTopic", "score": 2},
        {"closed_reason": None, "score": 3},
    ]
    k, n, p, lo, hi = reask._rate(rows)
    rec("only the literal Duplicate counts", k == 1 and n == 4, "k=%d n=%d" % (k, n))
    rec("a None closure reason is not a duplicate", p == 0.25, str(p))
    rec("denominator is the fetched row count", n == 4)
    rec("an empty arm has no rate rather than a rate of zero",
        reask._rate([]) == (0, 0, None, None, None), str(reask._rate([])))
    rec("every other literal closure reason is excluded",
        reask._rate([{"closed_reason": r} for r in
                     ("OffTopic", "NotAnswered", "TooBroad", "OpinionBased",
                      "Duplicate", "duplicate", "DUPLICATE", "")])[0] == 1)

    # 4. The report must not be able to read an undeclared tag. A tag with no rows gets a
    #    printed zero row, not a silent omission, so a reader can see the arm was empty.
    buf = io.StringIO()
    tagset = {t[2] for t in reask.TAGS}
    one = reask.DECLARED_TAGS[0]     # a tag the `declared` sample owns, so its rows print
    site_of = {t[2]: t[1] for t in reask.TAGS}
    reask.report(rows=[dict(r, arm="tail", tag=one, site="stackoverflow", stratum="S1")
                       for r in rows], streams=buf)
    text = buf.getvalue()
    rec("report names every declared tag",
        all(t in text for t in reask.DECLARED_TAGS), text[:300])
    rec("report prints a row for an empty arm", "  0  -" in text, text)
    rec("report does not crash when only one arm has rows",
        "n=0" in text and one in text)

    # 5. Through the report, not around it: a 30-row arm must report n=30. Truncating to
    #    the page budget inside report would leave every rate correct-looking and wrong,
    #    because a 25-row cap changes almost nothing at a rate near 0.08.
    big = [dict(r, arm="tail", tag=one, site="stackoverflow", stratum="S1")
           for r in ([{"closed_reason": "Duplicate", "score": -3}] * 3
                     + [{"closed_reason": None, "score": -2}] * 27)]
    buf = io.StringIO()
    reask.report(rows=big, streams=buf)
    lines = [l for l in buf.getvalue().splitlines()
             if l.startswith(site_of[one] + "/" + one + " ")]
    line = lines[0] if lines else ""
    rec("a 30-row arm reports n=30", "  30  " in line, line)
    rec("a 30-row arm reports dup 3", " 3  0.1000 " in line, line)
    rng = line[line.index("["):line.index("]") + 1] if "[" in line else ""
    nums = [int(x) for x in rng.strip("[]").split(",")] if rng.strip("[]") else []
    rec("the reported score range is ascending", nums == sorted(nums) and len(nums) == 2,
        rng)

    # 6. The pooled section must contain every arm, or the headline comparison is one arm,
    #    and its n must be the pooled row count rather than one page of it.
    buf = io.StringIO()
    reask.report(rows=big, streams=buf)
    text = buf.getvalue()
    line = [l for l in text.splitlines() if l.startswith(site_of[one] + "/" + one + " ")][0]
    rec("a 30-row arm reports n=30", "  30  " in line, line)
    rec("a 30-row arm reports dup 3", " 3  0.1000 " in line, line)
    rng = line[line.index("["):line.index("]") + 1] if "[" in line else ""
    nums = [int(x) for x in rng.strip("[]").split(",")] if rng.strip("[]") else []
    rec("the reported score range is ascending", nums == sorted(nums) and len(nums) == 2,
        rng)
    rec("the report labels the sample it is printing",
        "sample declared" in text and "no rows committed" in text, text[:200])
    rec("a sample with no committed rows says so rather than printing nothing",
        "R2: no rows committed" in text, text[-300:])
    pline = [l for l in text.splitlines() if l.strip().startswith("tail ")][-1]
    rec("the pooled row count is the sum of the arms, not one page",
        "n=30 " in pline, pline)
    rec("the pooled duplicate count is the sum too", "dup   3" in pline, pline)

    # 7. The sample registry is the single source of truth. A sample declared in one place
    #    and fetched in another is how an empty arm becomes indistinguishable from a failed
    #    one, and the report iterates the registry rather than the rows.
    samples = getattr(reask, "SAMPLES", None)
    rec("a sample registry exists", samples is not None)
    if samples:
        rec("the registry holds the declared sample plus both amendments",
            list(samples) == ["declared", "R1", "R2"], str(list(samples)))
        rec("the declared sample carries the declared eight tags",
            list(samples["declared"][1]) == reask.DECLARED_TAGS)
        rec("both amendment samples carry the tail arm only",
            all(samples[s][0] == "tail" for s in ("R1", "R2")))
        r1, r2 = list(samples["R1"][1]), list(samples["R2"][1])
        rec("no tag appears twice inside one amendment sample",
            len(r1) == len(set(r1)) and len(r2) == len(set(r2)))
        rec("R1 re-samples declared tags and R2 adds new ones",
            set(r1) <= set(reask.DECLARED_TAGS)
            and not (set(r2) & set(reask.DECLARED_TAGS)), "%s / %s" % (r1, r2))
        rec("every tag in the registry is in TAGS",
            set(r1) | set(r2) <= {t[2] for t in reask.TAGS})
        rec("the registry's tags cover TAGS exactly once each",
            sorted(set(reask.DECLARED_TAGS) | set(r1) | set(r2))
            == sorted(t[2] for t in reask.TAGS),
            str(sorted(t[2] for t in reask.TAGS)))
        rec("both amendments start past the declared pages",
            samples["R1"][2] > 1 and samples["R2"][2] == 1,
            str([samples[s][2] for s in ("R1", "R2")]))

    # 8. The declared gates must read the declared sample and nothing else. `load()`
    #    returns every sample, so a gate table built from it double-counts the two tags R1
    #    re-reads at a later page and reports the replication back as the result — with
    #    every interval still plausible. This is the shape of defect 22 and F024.
    if os.path.isdir(os.path.join(HERE, "raw")):
        try:
            import measures
        except Exception as exc:
            rec("measures imports for the declared-population check", False, str(exc))
        else:
            built = measures.build()
            dcl = built["declared"]
            rec("the declared population carries no amendment row",
                all(r.get("sample", "declared") == "declared" for r in dcl),
                str(sorted({r.get("sample") for r in dcl})))
            rec("the declared population has no customs tail rows from a later page",
                all(r.get("sample", "declared") == "declared" for r in dcl
                    if r["tag"] == "customs" and r["arm"] == "tail"))
            rec("load() spans every sample while the declared arms do not",
                len(reask.load()) >= len(dcl) and len(dcl) == 2124,
                "load=%d declared=%d" % (len(reask.load()), len(dcl)))
            rec("the R1 sample is held apart from the declared arms",
                len(built["samples"]["r1"]) == 196,
                str(len(built["samples"]["r1"])))
    return out


def main():
    path = os.path.join(HERE, "reask.py")
    res = check(_load(path))
    width = max(len(n) for n, _o, _d in res)
    bad = 0
    for name, ok, detail in res:
        if not ok:
            bad += 1
        print("%-*s %s %s" % (width, name, "ok  " if ok else "FAIL", detail if not ok else ""))
    print("\n%d checks, %d failed\n" % (len(res), bad))

    print("falsification — each mutation must be caught:")
    import falsify
    f = falsify.run(check)
    fwidth = max(len(n) for n, _v, _d in f)
    missed = 0
    for name, verdict, detail in f:
        if verdict != "caught":
            missed += 1
        print("%-*s %-10s %s" % (fwidth, name, verdict, detail))
    print("\n%d mutations, %d not caught" % (len(f), missed))
    return 1 if (bad or missed) else 0


if __name__ == "__main__":
    sys.exit(main())
