#!/usr/bin/env python3
"""E030 step 2 — resolve the two arms.

Treatment: a harvested comment that carries a framing phrase, resolves a departing
artifact candidate by the declared syntax test, and has >= 40 stripped words.
Control: comments on the SAME stories, by authors not in the treatment arm, with
no framing phrase, >= 40 stripped words, and not a reply to a treatment account.

Writes:
  raw/treatment.jsonl   the treatment arm, one row per account
  raw/control.jsonl     the control arm, one row per account
  raw/extract_log.jsonl the control-arm fetch log and the exclusion ledger

No rate is computed here. `recurrence.py` and `stats.py` do that.
"""

import json
import os
import random
import re

import common as C

SEED = 3004
STORIES = 60           # distinct stories sampled for the control arm
PAGES_PER_STORY = 2

_NAME = re.compile(r"^[A-Z][A-Za-z0-9._+#-]*$")
_PKG = re.compile(r"^[a-z0-9]+[._-][a-z0-9]")
# tokens that are name-shaped but never name an artifact
_NOT_ARTIFACT = {
    "i", "we", "you", "they", "it", "he", "she", "this", "that", "these", "those",
    "there", "here", "then", "the", "a", "an", "and", "but", "or", "so", "if",
    "when", "while", "after", "before", "because", "just", "also", "still",
    "now", "one", "two", "some", "any", "all", "my", "our", "your", "their",
    "its", "his", "her", "what", "which", "who", "how", "why", "not", "no",
    "yes", "was", "were", "is", "are", "be", "been", "being", "have", "has",
    "had", "do", "does", "did", "will", "would", "can", "could", "should",
    "may", "might", "must", "more", "most", "less", "least", "very", "much",
    "many", "few", "other", "another", "same", "different", "new", "old",
    "first", "last", "next", "back", "out", "up", "down", "over", "under",
    "about", "into", "from", "with", "without", "for", "to", "of", "in", "on",
    "at", "by", "as", "isn't", "don't", "doesn't", "didn't", "can't",
    "monday", "tuesday", "wednesday", "thursday", "friday", "saturday",
    "sunday", "january", "february", "march", "april", "may", "june", "july",
    "august", "september", "october", "november", "december",
}


def name_like(token):
    if token in _NOT_ARTIFACT:
        return False
    if _NAME.match(token) or _PKG.match(token):
        # a single capitalised sentence-initial word is still name-shaped; the
        # caller decides. Reject pure punctuation-ish and bare digits.
        return not token.isdigit()
    return False


def resolve_artifact(text):
    """First name-like token after a framing phrase, plus an optional second.

    Returns (artifact, framing, span) or (None, None, None). Deterministic and
    decided without reference to any corpus frequency (PROTOCOL.md, population
    step 2).
    """
    low = text.lower()
    best = None
    for framing in C.FRAMINGS:
        start = low.find(framing)
        if start < 0:
            continue
        span = text[start + len(framing): start + len(framing) + 40]
        span = re.split(r"[.,;:!?()\[\]\"'\n]", span)[0]
        toks = [t for t in re.split(r"\s+", span.strip()) if t]
        toks = [t.strip("-_<>()") for t in toks]
        picked = []
        for tok in toks:
            if name_like(tok):
                picked.append(tok)
                if len(picked) == 2:
                    break
            elif picked:
                break
        if picked and (best is None or start < best[3]):
            best = (" ".join(picked), framing, span.strip(), start)
    if best is None:
        return None, None, None
    return best[0], best[1], best[2]


def has_framing(text):
    low = text.lower()
    return [f for f in C.FRAMINGS if f in low]


def main():
    os.makedirs(C.RAW, exist_ok=True)
    harvest = C.read_jsonl("harvest.jsonl")
    ledger = []

    # ---- treatment arm -------------------------------------------------
    seen = set()
    treatment = []
    for row in harvest:
        oid = row["objectID"]
        if oid in seen:
            ledger.append({"stage": "dedupe", "objectID": oid})
            continue
        seen.add(oid)
        text = C.clean(row["text"])
        nwords = len(text.split())
        if nwords < C.MIN_WORDS:
            ledger.append({"stage": "too_short", "objectID": oid, "words": nwords})
            continue
        framings = has_framing(text)
        if not framings:
            ledger.append({"stage": "no_framing", "objectID": oid})
            continue
        artifact, framing, span = resolve_artifact(text)
        if not artifact:
            ledger.append({"stage": "artifact_unresolved", "objectID": oid,
                           "framings": framings})
            continue
        treatment.append({
            "objectID": oid,
            "author": row["author"],
            "story_id": row["story_id"],
            "story_title": row["story_title"],
            "created_at_i": row["created_at_i"],
            "artifact": artifact,
            "framing": framing,
            "span": span,
            "framings_present": framings,
            "words": nwords,
            "text": text,
        })
    C.log("treatment_arm", accounts=len(treatment))

    # ---- control arm ---------------------------------------------------
    rng = random.Random(SEED)
    story_ids = sorted({r["story_id"] for r in treatment})
    rng.shuffle(story_ids)
    chosen = sorted(story_ids[:STORIES])
    treat_authors = {r["author"] for r in treatment}
    treat_oids = {r["objectID"] for r in treatment}

    log_path = os.path.join(C.RAW, "extract_log.jsonl")
    with open(log_path, "w", encoding="utf-8") as fh_log:
        pool = {}
        for sid in chosen:
            for page in range(PAGES_PER_STORY):
                status, data, raw = C.algolia_pages(
                    "", "story_%s" % sid, page, 100, since=0)
                if data is None:
                    fh_log.write(json.dumps(
                        {"stage": "control_fetch_failed", "story_id": sid,
                         "page": page, "status": status}, sort_keys=True) + "\n")
                    continue
                hits = data.get("hits", [])
                fh_log.write(json.dumps(
                    {"stage": "control_fetch", "story_id": sid, "page": page,
                     "status": status, "hits": len(hits)}, sort_keys=True) + "\n")
                for hit in hits:
                    oid = hit.get("objectID")
                    if oid and oid not in pool:
                        pool[oid] = hit
                if len(hits) < 100:
                    break
        fh_log.flush()
    C.log("control_pool", stories=len(chosen), comments_in_pool=len(pool))

    control = []
    excluded = {"author_in_treatment": 0, "reply_to_treatment": 0,
                "has_framing": 0, "too_short": 0, "duplicate": 0, "no_author": 0}
    for oid, hit in pool.items():
        text = C.clean(hit.get("comment_text") or hit.get("story_text") or "")
        if not hit.get("author"):
            excluded["no_author"] += 1
            continue
        if hit["author"] in treat_authors:
            excluded["author_in_treatment"] += 1
            continue
        if oid in treat_oids or str(hit.get("parent_id")) in treat_oids:
            excluded["reply_to_treatment"] += 1
            continue
        if has_framing(text):
            excluded["has_framing"] += 1
            continue
        nwords = len(text.split())
        if nwords < C.MIN_WORDS:
            excluded["too_short"] += 1
            continue
        control.append({
            "objectID": oid,
            "author": hit["author"],
            "story_id": hit.get("story_id"),
            "story_title": hit.get("story_title") or hit.get("title") or "",
            "created_at_i": hit.get("created_at_i"),
            "artifact": None,
            "framing": None,
            "span": None,
            "framings_present": [],
            "words": nwords,
            "text": text,
        })

    # drop duplicate ids inside the pool
    uniq, dupes = [], 0
    seen_c = set()
    for row in control:
        if row["objectID"] in seen_c:
            dupes += 1
            continue
        seen_c.add(row["objectID"])
        uniq.append(row)
    excluded["duplicate"] = dupes
    control = uniq

    # story-stratified cap, as declared: no story contributes more than its
    # treatment share. The first version capped at the flat mean, which is not
    # the declared rule (recorded in AMENDMENT-3).
    by_story = {}
    for row in control:
        by_story.setdefault(row["story_id"], []).append(row)
    treat_per_story = {}
    for row in treatment:
        if row["story_id"] in chosen:
            treat_per_story[row["story_id"]] = treat_per_story.get(row["story_id"], 0) + 1
    total_treat = sum(treat_per_story.values()) or 1
    total_control = len(control) or 1
    trimmed, caps = [], {}
    for sid in sorted(by_story):
        share = treat_per_story.get(sid, 0) / float(total_treat)
        cap = max(1, int(round(total_control * share)))
        caps[sid] = cap
        trimmed.extend(by_story[sid][:cap])
    capped = len(control) - len(trimmed)

    C.write_jsonl("treatment.jsonl", treatment)
    C.write_jsonl("control.jsonl", trimmed)
    with open(log_path, "a", encoding="utf-8") as fh_log:
        for stage, n in sorted(excluded.items()):
            fh_log.write(json.dumps({"stage": "control_excluded", "reason": stage,
                                     "count": n}, sort_keys=True) + "\n")
        fh_log.write(json.dumps({"stage": "control_story_caps", "caps": caps,
                                 "dropped": capped}, sort_keys=True) + "\n")
        fh_log.write(json.dumps({"stage": "treatment_arm", "accounts": len(treatment)},
                                sort_keys=True) + "\n")

    C.log("arms_built", treatment=len(treatment), control=len(trimmed),
          control_capped=capped, stories=len(chosen),
          max_cap=max(caps.values()) if caps else 0)
    C.log("control_exclusions", **excluded)


if __name__ == "__main__":
    main()
