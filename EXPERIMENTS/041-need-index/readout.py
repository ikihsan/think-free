#!/usr/bin/env python3
"""E041 arm scoring: one text unit, one process, sized to fit this host.

Split out of `instrument.py` at the 300-line cap **by invariant**: this file reads
a text unit and produces partner ranks; `instrument.py` evaluates gates over those
ranks and decides what they mean. A threshold and the statistic it licenses must not
be editable in the same place.

The process shape is not a style choice. Measured on this host — 2 CPUs, 952 MiB
RAM, Python 3.8.10, no NumPy — with a 44,669-row corpus and a ~400 MB inverted
index:

| shape | result |
|---|---|
| one process, both units, E040's `vectors()` | never finished U2: 33+ min wall, 3.5 min CPU, `D (disk sleep)` |
| one process, streaming index, both units | U1 in 7 s, then U2: 10 min wall, 2m16s CPU, 716 MB of it swapped out |
| `os.fork()` per unit | same: fork shares the parent's pages copy-on-write, so the child inherits the corpus |
| **separate `exec` per unit, corpus streamed** | **U1 in 20 s, U2 in 552 s, no swap** |

So each unit runs as its own process and leaves only `raw/unit_<U>.json` behind.
Before its index is trusted it rebuilds a sample with **E040's own `vectors()`** and
requires every cosine to agree to 1e-9: a faster instrument is not the same
instrument until that is shown, not asserted.

Run directly for one unit: `--unit U1`. The driver in `instrument.py` spawns both.
"""
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "040-need-clustering"))

import stream  # noqa: E402
from arms import normalise  # noqa: E402

TAUS = [0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.50, 0.60]
EQUIV_SAMPLE = 120
EQUIV_TOL = 1e-9

UNIT_SPECS = {
    "U1": lambda r: r["title"],
    "U2": lambda r: (r["title"] + " " + r["body"]).strip(),
}


def note(stage, **kw):
    """One line per stage, written to disk by atomic replace.

    Five attempts at this run were lost to restarted hosts, several after ten
    minutes of wall clock each. A stage that records itself costs nothing and makes
    the next attempt resume from evidence rather than from nothing.
    """
    path = os.path.join(RAW, "tally_progress.json")
    rec = {}
    if os.path.exists(path):
        try:
            with open(path) as fh:
                rec = json.load(fh)
        except ValueError:
            rec = {}
    rec[stage] = dict(kw, at=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
    tmp = path + ".tmp"
    with open(tmp, "w") as fh:
        json.dump(rec, fh, indent=1, sort_keys=True)
    os.replace(tmp, path)
    print("[%s] %s %s" % (time.strftime("%H:%M:%S"), stage,
                          json.dumps(kw, sort_keys=True)), flush=True)


def load_meta():
    with open(os.path.join(RAW, "arms_summary.json")) as fh:
        s = json.load(fh)
    with open(os.path.join(RAW, "arms.jsonl")) as fh:
        pairs = [json.loads(l) for l in fh]
    return s, pairs


def corpus_iter(excluded):
    """A re-iterable *callable* yielding the corpus once per call.

    `stream.stream_iter` walks its input twice — once for document frequency, once
    to emit postings — so a plain generator is exhausted after the first pass and
    the index comes back **empty**, which reports every count as zero rather than
    as an error. This is a function, not a generator object, for that reason.
    """
    def gen():
        seen = set()
        with open(os.path.join(RAW, "corpus.jsonl")) as fh:
            for line in fh:
                r = json.loads(line)
                k = (r["repo"], r["number"])
                if k in seen or r["repo"] in excluded:
                    continue
                seen.add(k)
                yield {"repo": r["repo"], "number": r["number"],
                       "key": "%s#%s" % (r["repo"], r["number"]),
                       "title": r.get("title") or "", "body": r.get("body") or "",
                       "state_reason": r.get("state_reason")}
    return gen


def unit_texts(unit, rows_iter):
    for r in rows_iter:
        yield UNIT_SPECS[unit](r)


def pick_n0(pairs, rows):
    """One row from a different repository per P row, by a fixed rule.

    Rule: among corpus rows from a repository that is not the pair's own, take the
    one whose index is closest to a deterministic hash of the pair key.
    Deterministic, unseeded, and independent of every similarity.
    """
    by_repo = {}
    for j, r in enumerate(rows):
        by_repo.setdefault(r["repo"], []).append(j)
    others = sorted(by_repo)
    out = []
    for p in pairs:
        pool = []
        for repo in others:
            if repo != p["repo"]:
                pool.extend(by_repo[repo])
        if not pool:
            out.append(None)
            continue
        h = 0
        for ch in p["dup"]:
            h = (h * 131 + ord(ch)) % 1000003
        out.append(pool[h % len(pool)])
    return out


def score_pair(acc, target_row, corpus_rows, pair_row, n_corpus):
    """Partner rank, target cosine, best impostor and N0 cosine for one pair."""
    i = pair_row["dup_row"]
    tscore = acc.get(target_row, 0.0)
    # Rank of the judged partner among every row in the pool, by counting the rows
    # strictly above it.
    rank = 1 + sum(1 for v in acc.values() if v > tscore)
    # Ties at the top are resolved pessimistically -- the target is ranked last
    # among those tied to it. The conservative choice, stated rather than left to
    # happen.
    if rank == 1:
        rank += sum(1 for v in acc.values() if v >= tscore) - 1
    best_j, best_v = None, -1.0
    for j, v in acc.items():
        if j != target_row and v > best_v:
            best_j, best_v = j, v
    return {"dup": pair_row["dup"], "target": pair_row["target"],
            "repo": pair_row["repo"], "stratum": pair_row["stratum"],
            "target_cos": round(tscore, 6), "rank": rank, "top1": rank == 1,
            "impostor": corpus_rows[best_j]["key"] if best_j is not None else None,
            "impostor_cos": round(best_v, 6),
            "beats_impostor": tscore > best_v,
            "pool": n_corpus - 1,
            "own_repo_pool": pair_row["own_pool"],
            # base rate: share of this row's pool at or above each tau
            "null_above": {("%.2f" % t): round(
                sum(1 for v in acc.values() if v >= t) / max(1, len(acc)), 6)
                for t in TAUS}}


def run_unit(unit):
    """Score one text unit and write `raw/unit_<U>.json`."""
    summary_in, pairs = load_meta()
    excluded = set(summary_in["repos_excluded_automation"])
    rows = list(corpus_iter(excluded)())
    assert len(rows) == summary_in["corpus_rows"], (
        "corpus count %d != arms.py %d" % (len(rows), summary_in["corpus_rows"]))

    # Equivalence first: the streaming index must reproduce E040's own vectors()
    # before it is allowed near the corpus.
    sample = [UNIT_SPECS[unit](r) for r in rows[:EQUIV_SAMPLE]]
    ok, worst, compared = stream.check_equivalent(sample, len(sample),
                                                  tol=EQUIV_TOL)
    if not ok:
        raise SystemExit("streaming instrument disagrees with E040's by %.3e "
                         "over %d pairs; refusing to report" % (worst, compared))
    note("instrument_checked_%s" % unit, equivalent=True,
         worst_abs_diff="%.3e" % worst, pairs_compared=compared)

    # The text source is walked from the file rather than from the row list, so
    # the token stream never exists alongside a second copy of every document.
    def texts():
        return (normalise(t)
                for t in unit_texts(unit, corpus_iter(excluded)()))

    wanted = sorted({p["dup_row"] for p in pairs})
    t0 = time.time()
    idx, wts, keep = stream.stream_iter(texts, wanted)
    if not idx:
        raise SystemExit("streaming index is empty; the text stream was not "
                         "re-iterable, so this run would report zeros")
    note("index_built_%s" % unit, seconds=round(time.time() - t0, 1),
         posting_terms=len(idx), kept_vectors=len(keep))

    # Pair rows carry their own-repository pool size, which `arms.py` knows and
    # this file would otherwise recompute per pair.
    own = {}
    for r in rows:
        own[r["repo"]] = own.get(r["repo"], 0) + 1
    n0_idx = pick_n0(pairs, rows)
    for p in pairs:
        p["own_pool"] = own.get(p["repo"], 1) - 1

    out_rows = []
    t0 = time.time()
    for k, p in enumerate(pairs):
        i = p["dup_row"]
        acc = stream.score_row(idx, wts, keep[i], i)
        rec = score_pair(acc, p["target_row"], rows, p, len(rows))
        n0j = n0_idx[k]
        rec["n0"] = rows[n0j]["key"] if n0j is not None else None
        rec["n0_cos"] = (round(acc.get(n0j, 0.0), 6)
                         if n0j is not None else None)
        out_rows.append(rec)
        acc = None
    note("unit_done_%s" % unit, pairs=len(out_rows),
         score_seconds=round(time.time() - t0, 1))

    res = {"unit": unit, "corpus_rows": len(rows), "pairs": len(out_rows),
           "rows": out_rows}
    path = os.path.join(RAW, "unit_%s.json" % unit)
    tmp = path + ".tmp"
    with open(tmp, "w") as fh:
        json.dump(res, fh, indent=1, sort_keys=True)
    os.replace(tmp, path)
    return 0


def run_g4(unit, frozen):
    """E040's arms A and B, scored by the frozen instrument at the frozen tau."""
    out = {}
    e040 = os.path.join(os.path.dirname(HERE), "040-need-clustering", "raw")
    for arm in ("A", "B"):
        texts = []
        with open(os.path.join(e040, "arm_%s.jsonl" % arm)) as fh:
            for line in fh:
                texts.append(json.loads(line)["text"])
        sub = texts[:1391]
        del texts
        idx, wts, keep_all = stream.stream_vectors(sub, range(len(sub)))
        hit = 0
        for i in range(len(sub)):
            acc = stream.score_row(idx, wts, keep_all[i], i)
            if any(v >= frozen for v in acc.values()):
                hit += 1
            acc = None
        del keep_all, idx, wts
        out[arm] = round(hit / len(sub), 6)
        out["n_%s" % arm] = len(sub)
    if out.get("A") and out.get("B"):
        out["ratio"] = out["A"] / out["B"]
        out["met"] = out["ratio"] >= 1.5
    else:
        # A zero-denominator control arm is a third state, not a failed ratio
        # (F067): printing "not met" here would read as red on a result that is
        # otherwise strongly positive.
        out["ratio"] = None
        out["met"] = ("not_evaluated (a control arm is 0, so the ratio has no "
                      "denominator -- F067)")
    return out


def run_g4_unit(unit, frozen):
    res = run_g4(unit, float(frozen))
    path = os.path.join(RAW, "g4_%s.json" % unit)
    tmp = path + ".tmp"
    with open(tmp, "w") as fh:
        json.dump(res, fh, indent=1, sort_keys=True)
    os.replace(tmp, path)
    return 0
