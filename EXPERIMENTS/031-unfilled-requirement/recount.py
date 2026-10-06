#!/usr/bin/env python3
"""E031 step 1 — restratify E030's captures and freeze the reader views.

No network access. Reads ../030-departure-recurrence/raw/{treatment,control}.jsonl,
splits the treatment arm into the seek and move strata by E030's framing phrase,
samples the three arms with the declared seeds, shuffles the nonsense rows, and
writes:

  raw/strata.json                 the stratum counts and the source digests read
  raw/view_<arm>.txt              one per arm, byte-identical question block
  raw/view_nonsense.txt           the shuffled rows, same question block
  raw/view_reread.txt             the disjoint re-read sample for reader 2
  raw/view_digests.json           sha256 of every view and of every source file
  raw/e031_rows.jsonl             the id -> objectID -> arm key
  raw/e031_clause_text.json       clause id -> the row's own text, for the
                                  verbatim-substring check in verify_labels.py

Arm labels, framing words, author names, story titles, artifact names and word
counts are absent from every view (checked by verify_labels.py, gate A2).
"""

import json
import os
import random
import re

import common as C

ARMS = ["seek", "move", "ordinary"]


def stratum_of(row):
    """Declared strata: by framing phrase, never by anything read here."""
    fps = row.get("framings_present") or []
    fp = set(fps)
    if fp & set(C.SEEK_FRAMINGS):
        return "seek"
    if fp & set(C.MOVE_FRAMINGS):
        return "move"
    return None


def render(rows, path, header_note, with_q3=True):
    lines = []
    for i, row in enumerate(rows, 1):
        rid = row["rid"]
        lines.append("=" * 72)
        lines.append("ID: %s" % rid)
        for q in C.QUESTION_BLOCK:
            lines.append(q)
        if with_q3:
            lines.append("    (q3 is asked separately; write q1 and q2 only here.)")
        lines.append("COMMENT:")
        lines.append(row["text"].strip())
        lines.append("")
    body = header_note + "\n" + "\n".join(lines)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(body)
    return C.sha256_bytes(body)


def shuffle_tokens(text, rng):
    """Deterministic content-token shuffle for a nonsense row."""
    toks = text.split()
    out = list(toks)
    for _ in range(200):
        idx = [i for i, t in enumerate(out) if len(t) >= 4]
        if len(idx) < 2:
            break
        i, j = rng.sample(idx, 2)
        out[i], out[j] = out[j], out[i]
    return " ".join(out)


def main():
    os.makedirs(C.RAW, exist_ok=True)
    treat = C.read_jsonl(os.path.join(C.E030_RAW, "treatment.jsonl"))
    ctrl = C.read_jsonl(os.path.join(C.E030_RAW, "control.jsonl"))

    seek_rows, move_rows = [], []
    for r in treat:
        s = stratum_of(r)
        if s == "seek":
            seek_rows.append(r)
        elif s == "move":
            move_rows.append(r)

    # gate A1: the stratum counts must equal PROTOCOL.md's table
    declared = {"seek": 326, "move": 593}
    for arm, rows in (("seek", seek_rows), ("move", move_rows)):
        if len(rows) != declared[arm]:
            C.log("stratum_mismatch", arm=arm, got=len(rows), declared=declared[arm])
            raise SystemExit(3)

    arms = {"seek": seek_rows, "move": move_rows, "ordinary": ctrl}

    rng = random.Random(C.SEED_SAMPLE)
    sample, key = {}, []
    for arm in ARMS:
        pool = sorted(arms[arm], key=lambda r: r["objectID"])
        sel = rng.sample(pool, C.N_PER_ARM)
        sample[arm] = sel
        prefix = {"seek": "S", "move": "M", "ordinary": "O"}[arm]
        for i, r in enumerate(sel, 1):
            rid = "%s%02d" % (prefix, i)
            sample[arm][i - 1] = dict(r, rid=rid)
            key.append({"id": rid, "arm": arm, "objectID": r["objectID"],
                        "author": r.get("author"),
                        "artifact": r.get("artifact"),
                        "story_id": r.get("story_id"),
                        "words": len(r["text"].split())})

    # nonsense rows: A3 rows whose content tokens are shuffled
    srng = random.Random(C.SEED_SHUFFLE)
    used = set(r["objectID"] for r in sample["ordinary"])
    pool = [r for r in ctrl if r["objectID"] not in used]
    pool = sorted(pool, key=lambda r: r["objectID"])
    nonsense = []
    for i, r in enumerate(srng.sample(pool, C.N_NONSENSE), 1):
        rid = "N%02d" % i
        nonsense.append({"rid": rid, "text": shuffle_tokens(C.clean(r["text"]), srng),
                         "objectID": r["objectID"]})
        key.append({"id": rid, "arm": "nonsense", "objectID": r["objectID"],
                    "author": r.get("author"), "artifact": None,
                    "story_id": r.get("story_id"),
                    "words": len(r["text"].split())})

    # re-read sample for reader 2: disjoint from the main views
    rrng = random.Random(C.SEED_SAMPLE + 1)
    reread, rr_seen = [], set(r["objectID"] for r in sample["seek"] + sample["move"]
                              + sample["ordinary"] + nonsense)
    for arm in ("seek", "move"):
        pool = [r for r in arms[arm] if r["objectID"] not in rr_seen]
        pool = sorted(pool, key=lambda r: r["objectID"])
        pick = rrng.sample(pool, C.N_REREAD // 2)
        for r in pick:
            rr_seen.add(r["objectID"])
        for r in pick:
            reread.append(dict(r, rid="R%02d" % (len(reread) + 1)))
            key.append({"id": reread[-1]["rid"], "arm": "reread",
                        "objectID": r["objectID"], "author": r.get("author"),
                        "artifact": r.get("artifact"), "story_id": r.get("story_id"),
                        "words": len(r["text"].split())})

    note = ("E031 reader view. One comment. You are told nothing about where it "
            "came from, who wrote it, or which group it is in.")
    digests = {}
    for arm in ARMS:
        name = "view_%s.txt" % arm
        digests[name] = render(sample[arm], os.path.join(C.RAW, name), note)
    digests["view_nonsense.txt"] = render(nonsense, os.path.join(C.RAW, "view_nonsense.txt"),
                                          note)
    digests["view_reread.txt"] = render(reread, os.path.join(C.RAW, "view_reread.txt"),
                                        note, with_q3=False)

    src = {
        "treatment.jsonl": C.sha256_file(os.path.join(C.E030_RAW, "treatment.jsonl")),
        "control.jsonl": C.sha256_file(os.path.join(C.E030_RAW, "control.jsonl")),
    }
    strata = {
        "declared": True,
        "seek_rows": len(seek_rows), "move_rows": len(move_rows),
        "ordinary_rows": len(ctrl),
        "n_per_arm": C.N_PER_ARM, "n_nonsense": C.N_NONSENSE,
        "n_reread": len(reread), "seed_sample": C.SEED_SAMPLE,
        "seed_shuffle": C.SEED_SHUFFLE,
        "source_sha256": src, "views": digests,
    }
    with open(os.path.join(C.RAW, "strata.json"), "w", encoding="utf-8") as fh:
        json.dump(strata, fh, indent=2, sort_keys=True)
        fh.write("\n")
    with open(os.path.join(C.RAW, "view_digests.json"), "w", encoding="utf-8") as fh:
        json.dump(digests, fh, indent=2, sort_keys=True)
        fh.write("\n")

    C.write_jsonl(os.path.join(C.RAW, "e031_rows.jsonl"), key)
    # clause-text key: the verbatim source each q2 phrase must be a substring of
    clause_text = {}
    for arm in ARMS:
        for r in sample[arm]:
            clause_text[r["rid"]] = C.clean(r["text"])
    for r in nonsense:
        clause_text[r["rid"]] = r["text"]
    for r in reread:
        clause_text[r["rid"]] = C.clean(r["text"])
    with open(os.path.join(C.RAW, "e031_clause_text.json"), "w", encoding="utf-8") as fh:
        json.dump(clause_text, fh, sort_keys=True)
        fh.write("\n")

    C.log("views_written", seek=len(sample["seek"]), move=len(sample["move"]),
          ordinary=len(sample["ordinary"]), nonsense=len(nonsense),
          reread=len(reread), n_views=len(digests))


if __name__ == "__main__":
    main()