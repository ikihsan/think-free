#!/usr/bin/env python3
"""E023: draw the two arms and their reply text. It does not label.

`served` is a judgement, so it is labelled by hand into `raw/labels.tsv`, one
line per row, exactly as E022 did. A row with no label reads as `unlabelled`,
never as `not_served`.

The need arm is drawn by E022's own stated rule and seed so it is reproducible
and so the reader re-reads rows E022 already read without seeing its labels --
A1 exists to measure label reliability, which is only meaningful if the reader
does not already know the answer.

The control arm is drawn from the same stories, from comments matching none of
the 23 trigger phrases, and **restricted to answered comments**. That restriction
is the whole experiment: `served` is conditional on a reply existing, so
comparing an answered need against an unanswered control would measure
`answered` again -- the cell E022 already controlled and the one its conclusion
does not rest on.

Only external dependency is the public Algolia and Firebase APIs.
"""
import argparse
import json
import os
import random
import re
import time
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")
OUTCOMES = os.path.join(HERE, "..", "022-need-outcomes", "raw", "outcomes.jsonl")
CONTROL = os.path.join(HERE, "..", "022-need-outcomes", "raw", "control.jsonl")
E022_LABELS = os.path.join(HERE, "..", "022-need-outcomes", "raw", "labels.tsv")

SAMPLE_N = 39          # E022 labelled 40 and dropped 1 unreadable; same size here
SEED = 20261005        # E022's seed, so the need arm is the same draw rule
ALGOLIA_ITEM = "https://hn.algolia.com/api/v1/items/%s"
FIREBASE = "https://hacker-news.firebaseio.com/v0/item/%s.json"
LABELS = os.path.join(RAW, "labels.tsv")

TAG = re.compile(r"<[^>]+>")
HTMLISH = re.compile(r"<(?:!DOCTYPE|html|head|body)\b", re.I)
# Deliberately over-inclusive, and copied verbatim from E022's serve_sample.py
# so the two experiments agree on what "artifactish" means. E022 recorded that
# this rule fires on 39 of 40 rows and agrees with its hand labels on 16, so it
# is reported beside the labels and never alone.
ARTIFACTISH = re.compile(
    r"(https?://[^\s<>]+|`[^`]{2,40}`|\b(?:[A-Z][a-z0-9]+){1,}[A-Za-z0-9_+.-]*\b)")


def html_to_text(t):
    t = TAG.sub(" ", t or "")
    t = (t.replace("&#x27;", "'").replace("&#39;", "'")
          .replace("&quot;", '"').replace("&gt;", ">")
          .replace("&lt;", "<").replace("&amp;", "&").replace("&gt;", ">"))
    return re.sub(r"\s+", " ", t).strip()


def fetch(url, timeout=25):
    for attempt in range(3):
        try:
            with urllib.request.urlopen(url, timeout=timeout) as r:
                return r.status, r.read().decode("utf-8", "replace")
        except urllib.error.HTTPError as e:
            # A 404 is an answer, not a retry. F036's shape is an HTTP 200 with
            # the wrong body, which this cannot see.
            if e.code in (404, 403, 400):
                return e.code, ""
        except Exception:
            pass
        time.sleep(0.4 * (attempt + 1))
    return None, ""


def choose_need_arm():
    rows = [json.loads(l) for l in open(OUTCOMES)]
    answered = [r for r in rows if r["answered"]]
    rng = random.Random(SEED)
    idx = list(range(len(answered)))
    rng.shuffle(idx)
    return [answered[i] for i in idx[:SAMPLE_N]]


def choose_control_arm(need_rows):
    """Same stories, no trigger match, answered, sampled by the same rule.

    The story restriction is what makes the two arms comparable: a thread that
    attracts one kind of comment attracts the other, and that thread-level
    effect is the thing `served` could be measuring instead of the need.
    """
    stories = set(r["story_id"] for r in need_rows)
    rows = [json.loads(l) for l in open(CONTROL)]
    pool = [r for r in rows
            if r["answered"] and not r["has_trigger"] and r["story_id"] in stories]
    rng = random.Random(SEED)
    idx = list(range(len(pool)))
    rng.shuffle(idx)
    return [pool[i] for i in idx[:SAMPLE_N]], len(pool)


def replies_for(cid):
    """Depth-1 replies with their text, via Algolia's tree endpoint."""
    st, body = fetch(ALGOLIA_ITEM % cid)
    if st != 200:
        return None, []
    try:
        obj = json.loads(body)
    except ValueError:
        return None, []
    kids = obj.get("children") or []
    out = []
    for c in kids[:6]:
        out.append({"author": c.get("author"),
                    "text": html_to_text(c.get("text"))[:400]})
    return obj, out


def read_payload(status, body):
    """E022's `fetch_item` classification, applied here so a row that fails to
    read is `unreadable` and never `not_served`.

    Firebase answers **HTTP 200 with the literal body `null`** for an absent id.
    That is this API's absence signal, not a success: E022 recorded the same
    shape and gave it its own status. Treating the status code alone as the
    answer would make every fabricated id read as a real item, which is exactly
    the class F032 logged as "an HTTP 200 meaning something other than success".
    """
    if status != 200:
        return "refused", None
    if HTMLISH.search(body[:400]):
        return "challenge", None
    try:
        obj = json.loads(body)
    except ValueError:
        return "not_json", None
    if obj is None:
        return "null_body", None
    if not isinstance(obj, dict):
        return "not_json", None
    return "ok", obj


def nonsense_control():
    """C3, repeated. A fabricated id must yield no reply tree.

    F036's instrument answered HTTP 200 with ten well-formed unrelated results
    for every one of 38 queries. Nothing inside a capture distinguishes that
    from a real one, so both readers are asked directly.

    The assertion is **no reply tree**, not a particular status code: Firebase
    answers 200-with-null for an absent id, which is a distinguishable refusal
    and not a success. Asserting `404` here would fail the run for the wrong
    reason, which is the mistake this experiment exists to avoid elsewhere.
    """
    out = []
    for fake in ("999999999999", "888888888888", "777777777777"):
        st, body = fetch(FIREBASE % fake)
        status, obj = read_payload(st, body)
        st2, body2 = fetch(ALGOLIA_ITEM % fake)
        alg_status, alg_obj = read_payload(st2, body2)
        out.append({
            "id": fake,
            "firebase": {"http": st, "status": status},
            "algolia": {
                "http": st2, "status": alg_status,
                "n_children": len((alg_obj or {}).get("children") or [])
                if isinstance(alg_obj, dict) else 0,
            },
        })
        time.sleep(0.3)
    return out


def control_is_clean(nc):
    """A fabricated id carries no reply tree on either reader."""
    for n in nc:
        if n["firebase"]["status"] == "ok":
            return False
        if n["algolia"]["n_children"] != 0:
            return False
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--verify", action="store_true")
    args = ap.parse_args()
    os.makedirs(RAW, exist_ok=True)

    need = choose_need_arm()
    control, pool_n = choose_control_arm(need)

    if args.verify:
        # The falsification the control is required to pass: a fabricated id
        # yields no reply tree. If it does not, every number below is about the
        # fetcher rather than the population.
        nc = nonsense_control()
        clean = control_is_clean(nc)
        print(json.dumps({"nonsense_control": nc, "clean": clean,
                          "assertion": "no reply tree on either reader"}, indent=1))
        return 0 if clean else 3

    # Keep E022's labels unconsulted by the reader: they are read afterwards, for
    # the agreement statistic only.
    prior = {}
    if os.path.exists(E022_LABELS):
        for line in open(E022_LABELS):
            parts = line.rstrip("\n").split("\t")
            if len(parts) >= 2:
                prior[parts[0]] = parts[1]

    need_text = {}
    for line in open(os.path.join(HERE, "..", "012-candidate-harvest",
                                  "raw", "hn_needs_2026-10-04.jsonl")):
        o = json.loads(line)
        cid = str(o.get("id") or o.get("comment_id"))
        if cid:
            need_text[cid] = html_to_text(o.get("text") or o.get("need") or "")

    for arm, rows in (("need", need), ("control", control)):
        path = os.path.join(RAW, "%s_arm.jsonl" % arm)
        # Resume, never overwrite. E021 lost nine counts to a clobbered capture
        # and this repository's standing repair is that a capture holding an
        # answer is not rewritten. A partial run leaves partial bytes; it does
        # not leave a reason to re-fetch them.
        done = {}
        if os.path.exists(path):
            for line in open(path):
                line = line.strip()
                if line:
                    o = json.loads(line)
                    done[o["comment_id"]] = o
        with open(path, "a") as f:
            for r in rows:
                cid = r["comment_id"]
                if cid in done:
                    continue
                item, replies = replies_for(cid)
                # The comment's own text: the need arm from E012's capture, the
                # control arm from the same tree endpoint. A row whose own text
                # cannot be read is `unreadable` and is never labelled.
                if arm == "need":
                    body = need_text.get(cid, "")
                else:
                    body = ""
                    st, b = fetch(ALGOLIA_ITEM % cid)
                    if st == 200:
                        try:
                            body = html_to_text(json.loads(b).get("text") or "")
                        except ValueError:
                            body = ""
                f.write(json.dumps({
                    "arm": arm,
                    "comment_id": cid,
                    "story_id": r["story_id"],
                    "n_replies": r["n_replies"],
                    "status": "ok" if item is not None else "unreadable",
                    "text": body[:900],
                    "replies": replies,
                    "lex_hits": len(ARTIFACTISH.findall(
                        " ".join(x["text"] for x in replies))),
                }) + "\n")
                time.sleep(0.35)
        print("wrote", path, len(rows))

    with open(os.path.join(RAW, "nonsense_control.json"), "w") as f:
        json.dump(nonsense_control(), f, indent=1)
    with open(os.path.join(RAW, "arm_pool_size.json"), "w") as f:
        json.dump({"control_pool_answered_in_need_stories": pool_n}, f, indent=1)
    print("control pool (answered, same stories):", pool_n)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())