"""E171 G0: the classifier's positive control, built before any class label.

The protocol requires 10 probe rows whose classes were fixed **by
construction** -- the presence of an explicit operative sentence in the thread
makes the class readable without judgement.  The probe is built here from the
committed thread text and nothing else, and is written to disk so the labels
below cannot be re-chosen after seeing them.

Ten rows: the five highest-scoring rows with a version number anywhere in
the thread and the five highest-scoring rows without one (AMENDMENT 2), so
the probe carries both constructed classes and G0 can discriminate.
"""
import json
import re

TH = "EXPERIMENTS/169-version-pinned-reach/threads-all.json"
CL = "EXPERIMENTS/168-version-pinned-need/classified.jsonl"
G = "EXPERIMENTS/168-version-pinned-need/grades-unaided.jsonl"

VER = re.compile(r"\bv?\d+\.\d+(\.\d+)?\b|\bversion\s+\d", re.I)


def strip(h):
    h = re.sub(r"<pre[^>]*>.*?</pre>", " [CODE] ", h, flags=re.S)
    h = re.sub(r"<[^>]+>", " ", h)
    import html as _h
    return re.sub(r"\s+", " ", _h.unescape(h)).strip()


def build():
    cl = {str(r["qid"]): r for r in
          (json.loads(l) for l in open(CL))}
    byidx = {r["idx"]: str(r["qid"]) for r in cl.values()}
    grades = [json.loads(l) for l in open(G)]
    threads = json.load(open(TH))

    with_v, without_v = [], []
    for gr in grades:
        q = byidx[gr["idx"]]
        th = threads.get(q)
        if not th or not th["answers"]:
            continue
        # The operative answer, after AMENDMENT 1: the thread's resolution,
        # read across every answer.  For probe *construction* the signal used
        # is simply whether any answer carries a version number, which is a
        # property of the text and not a class label.
        texts = [(int(a["score"] or 0), strip(a["body"])) for a in th["answers"]]
        top = max(texts, key=lambda p: p[0])
        row = {"idx": gr["idx"], "qid": q, "verdict": gr["verdict"],
               "vp_sub": gr["vp_sub"], "n_answers": len(texts),
               "top_score": top[0], "top_text": top[1],
               "any_version": any(VER.search(t) for _, t in texts),
               "all_text": " || ".join(t for _, t in texts)}
        (with_v if row["any_version"] else without_v).append(row)

    for pool in (with_v, without_v):
        pool.sort(key=lambda r: (-r["top_score"], r["idx"]))

    # AMENDMENT 2: the original selection (with_v[:5] + with_v[-2:-7:-1] + ...)
    # filled all 10 slots from with_v alone, leaving a single-class probe on
    # which G0 is vacuous.  Five highest-scoring rows of each presence class.
    probe = with_v[:5] + without_v[:5]
    return probe, len(with_v), len(without_v)


if __name__ == "__main__":
    probe, nv, nnv = build()
    # Construction label, fixed by the row's presence class.  Written now, by
    # the selection rule, not by reading the sentence.
    for r in probe:
        r["constructed_label"] = "version_fact" if r["any_version"] else "not_version_fact"
    json.dump(probe, open("EXPERIMENTS/171-resolution-fact-locus/raw/g0-probe.json", "w"),
              indent=1)
    print("rows with a version somewhere in the thread: %d" % nv)
    print("rows without: %d" % nnv)
    print("probe size %d" % len(probe))
    for r in probe:
        print("  idx %-3d %-9s %-9s any_version=%-5s top=%d  -> %s"
              % (r["idx"], r["verdict"], r["vp_sub"], r["any_version"],
                 r["top_score"], r["constructed_label"]))