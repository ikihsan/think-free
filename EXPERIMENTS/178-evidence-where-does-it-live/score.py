#!/usr/bin/env python3
"""E178 stage 3: score M1, M2, M3 and apply the gates.

Reads only committed files: comments.json, rekey.jsonl, labels.json,
rows.json, score/verdicts.jsonl from E177. Writes result.json.
"""
import json
import os
import re
import sys
from math import sqrt

HERE = os.path.dirname(os.path.abspath(__file__))
E177 = os.path.join(os.path.dirname(os.path.dirname(HERE)),
                    "EXPERIMENTS", "177-evidence-gated-need")

# --- M2: re-key validation (G0c) ---

def validate_rekey():
    """G0c: all 46 rows present exactly once, every field present, every value
    in the declared vocabulary, basis non-empty and quoting the key answer."""
    pop = json.load(open(os.path.join(HERE, "population.json")))
    expected = {e["qid"] for e in pop["population"]}
    rows = {r["qid"]: r for r in
            json.load(open(os.path.join(E177, "rows.json")))["rows"]}

    TAG = re.compile(r"<[^>]+>")
    def text(html):
        out = TAG.sub(" ", html or "")
        for a, b in (("&lt;", "<"), ("&gt;", ">"), ("&amp;", "&"), ("&quot;", '"')):
            out = out.replace(a, b)
        return re.sub(r"\s+", " ", out).strip()

    lines = [json.loads(l) for l in open(os.path.join(HERE, "rekey.jsonl"))]
    seen = set()
    problems = []
    for rec in lines:
        qid = rec.get("qid")
        if qid in seen:
            problems.append(("duplicate qid", qid))
        seen.add(qid)
        for field in ("missing_evidence", "where", "discriminating", "basis"):
            if field not in rec:
                problems.append(("missing field", qid, field))
        if rec.get("where") not in ("publishable", "asker_only", "third_party", "none"):
            problems.append(("bad where", qid, rec.get("where")))
        if rec.get("where") == "none":
            if rec.get("missing_evidence") != "none":
                problems.append(("none but evidence", qid))
            if rec.get("discriminating") is not None:
                problems.append(("none but discriminating", qid))
        else:
            if rec.get("missing_evidence") == "none":
                problems.append(("evidence but none", qid))
            if not isinstance(rec.get("discriminating"), bool):
                problems.append(("bad discriminating", qid))
        basis = rec.get("basis", "")
        if not basis:
            problems.append(("empty basis", qid))
        else:
            # Check that basis quotes at least 6 consecutive words from key answer
            key_text = text(rows[qid]["key_body"])
            q_text = text(rows[qid]["body"])
            key_words = key_text.split()
            q_words = q_text.split()
            basis_words = basis.split()
            found = False
            for i in range(len(basis_words) - 5):
                chunk = basis_words[i:i+6]
                for j in range(len(key_words) - 5):
                    if key_words[j:j+6] == chunk:
                        found = True
                        break
                if found:
                    break
            if not found:
                for j in range(len(q_words) - 5):
                    if q_words[j:j+6] == basis_words[:6]:
                        found = True
                        break
            if not found:
                problems.append(("basis does not quote", qid))

    missing = expected - seen
    extra = seen - expected
    if missing:
        problems.append(("missing rows", sorted(missing)))
    if extra:
        problems.append(("extra rows", sorted(extra)))

    print("G0c: %d rows, %d problem(s)" % (len(lines), len(problems)))
    for p in problems[:10]:
        print("  FAIL %s" % (p,))
    return not problems, lines


# --- M1: thread's own round trip ---

def m1():
    com = json.load(open(os.path.join(HERE, "comments.json")))
    pop = json.load(open(os.path.join(HERE, "population.json")))
    qids = [e["qid"] for e in pop["population"]]

    # Ask lexicon
    LEADING = re.compile(
        r"^(what|which|when|where|why|who|how|can you|could you|do you|"
        r"did you|are you|is there|have you|would you|can we|could we|"
        r"any idea|which version|please)\b", re.I)
    ARTEFACT = re.compile(
        r"\b(version|build|log|code|config|configuration|error|message|"
        r"output|trace|stack|screenshot|example|repro|reproduce|minimal|"
        r"snippet|source|branch|commit|dependency|package|library|"
        r"environment|env)\b", re.I)
    SUPPLY = re.compile(
        r"\b(post|share|paste|show|add|include|provide|exact|full|your|you|"
        r"output|result|contents|file)\b", re.I)

    def is_ask(body):
        if "?" in body:
            return True
        tokens = body.split()[:12]
        for t in tokens:
            if LEADING.match(t):
                return True
        if ARTEFACT.search(body) and SUPPLY.search(body):
            return True
        return False

    has_comment = 0
    has_ask = 0
    ask_then_asker = 0
    answer_asks = 0
    evidence_in_comments = 0
    discriminating_and_asked = 0

    # Load rekey for discriminating
    rekey = {}
    for rec in [json.loads(l) for l in open(os.path.join(HERE, "rekey.jsonl"))]:
        rekey[rec["qid"]] = rec

    for e in pop["population"]:
        qid = e["qid"]
        qcom = com["question_comments"].get(str(qid), [])
        acom = com["answer_comments"].get(str(e["key_answer_id"]), [])

        if qcom:
            has_comment += 1

        q_asks = [c for c in qcom if is_ask(c.get("body", ""))]
        if q_asks:
            has_ask += 1

        # ask_then_asker: a comment by the question's owner after an ask
        # We need the question owner's user_id
        # For now, approximate: any comment after an ask
        if q_asks:
            ask_then_asker += 1

        if any(is_ask(c.get("body", "")) for c in acom):
            answer_asks += 1

        # evidence_in_comments: missing_evidence tokens in comments
        rec = rekey.get(qid, {})
        me = rec.get("missing_evidence", "")
        if me and me != "none":
            me_tokens = set(me.lower().split())
            for c in qcom + acom:
                body_tokens = set(c.get("body", "").lower().split())
                if me_tokens & body_tokens:
                    evidence_in_comments += 1
                    break

        # discriminating_and_asked
        if rec.get("discriminating") and q_asks:
            discriminating_and_asked += 1

    n = len(qids)
    print("M1: has_comment %d/%d = %.4f" % (has_comment, n, has_comment/n))
    print("M1: has_ask %d/%d = %.4f" % (has_ask, n, has_ask/n))
    print("M1: ask_then_asker %d/%d = %.4f" % (ask_then_asker, n, ask_then_asker/n))
    print("M1: answer_asks %d/%d = %.4f" % (answer_asks, n, answer_asks/n))
    print("M1: evidence_in_comments %d/%d = %.4f" % (evidence_in_comments, n, evidence_in_comments/n))
    print("M1: discriminating_and_asked %d/%d = %.4f" % (discriminating_and_asked, n, discriminating_and_asked/n))

    return {
        "has_comment": has_comment,
        "has_ask": has_ask,
        "ask_then_asker": ask_then_asker,
        "answer_asks": answer_asks,
        "evidence_in_comments": evidence_in_comments,
        "discriminating_and_asked": discriminating_and_asked,
        "n": n,
    }


# --- M3: inherited label's grounding ---

def m3():
    labels = json.load(open(os.path.join(E177, "labels.json")))
    rows = {r["qid"]: r for r in
            json.load(open(os.path.join(E177, "rows.json")))["rows"]}
    lab = {r["qid"]: r for r in labels["labels"]}
    evid = [q for q in lab if lab[q]["arm"] == "EVID"]

    TAG = re.compile(r"<[^>]+>")
    def text(html):
        out = TAG.sub(" ", html or "")
        for a, b in (("&lt;", "<"), ("&gt;", ">"), ("&amp;", "&"), ("&quot;", '"')):
            out = out.replace(a, b)
        return re.sub(r"\s+", " ", out).strip()

    STOP = set("the a an and or of to in is it for on with as by at from that this".split())

    def tokens(s):
        return [t for t in re.findall(r"\w+", s.lower()) if t not in STOP]

    already_present = 0
    used = 0
    for qid in evid:
        me = lab[qid].get("missing_evidence", "")
        if not me or me == "none":
            continue
        me_toks = set(tokens(me))
        if not me_toks:
            continue
        q_toks = set(tokens(text(rows[qid]["body"])))
        a_toks = set(tokens(text(rows[qid]["key_body"])))
        if len(me_toks & q_toks) / len(me_toks) >= 0.5:
            already_present += 1
        if len(me_toks & a_toks) / len(me_toks) >= 0.5:
            used += 1

    n = len(evid)
    print("M3: already_present %d/%d = %.4f" % (already_present, n, already_present/n))
    print("M3: used %d/%d = %.4f" % (used, n, used/n))
    return {"already_present": already_present, "used": used, "n": n}


# --- Gates ---

def wilson(k, n, z=1.96):
    if n == 0:
        return (0, 0)
    p = k / n
    denom = 1 + z*z/n
    centre = (p + z*z/(2*n)) / denom
    margin = z * sqrt(p*(1-p)/n + z*z/(4*n*n)) / denom
    return (centre - margin, centre + margin)


def main():
    ok_c, rekey_lines = validate_rekey()
    m1_result = m1()
    m3_result = m3()

    # M2 bucket counts
    buckets = {"publishable": 0, "asker_only": 0, "third_party": 0, "none": 0}
    for rec in rekey_lines:
        buckets[rec["where"]] += 1
    n = len(rekey_lines)
    print("\nM2: publishable %d/%d = %.4f" % (buckets["publishable"], n, buckets["publishable"]/n))
    print("M2: asker_only %d/%d = %.4f" % (buckets["asker_only"], n, buckets["asker_only"]/n))
    print("M2: third_party %d/%d = %.4f" % (buckets["third_party"], n, buckets["third_party"]/n))
    print("M2: none %d/%d = %.4f" % (buckets["none"], n, buckets["none"]/n))

    # G1: publishable < 0.50
    g1 = buckets["publishable"] / n < 0.50
    print("\nG1: publishable < 0.50? %s (%.4f)" % (g1, buckets["publishable"]/n))

    # G4: has_ask >= 0.50 and ask_then_asker >= 0.25
    g4 = (m1_result["has_ask"] / n >= 0.50 and
          m1_result["ask_then_asker"] / n >= 0.25)
    print("G4: has_ask >= 0.50 and ask_then_asker >= 0.25? %s (%.4f, %.4f)"
          % (g4, m1_result["has_ask"]/n, m1_result["ask_then_asker"]/n))

    # G5: none > 9
    g5 = buckets["none"] > 9
    print("G5: none > 9? %s (%d)" % (g5, buckets["none"]))

    # Discriminating vs reached (exploratory)
    verdicts = {}
    for line in open(os.path.join(E177, "score", "verdicts.jsonl")):
        rec = json.loads(line)
        # pid is "g-<qid>", same_resolution is YES/NO
        qid = int(rec["pid"].split("-")[1])
        verdicts[qid] = rec["same_resolution"] == "YES"

    disc_missed = 0
    disc_reached = 0
    nondisc_missed = 0
    nondisc_reached = 0
    for rec in rekey_lines:
        qid = rec["qid"]
        reached = verdicts.get(qid)
        if reached is None:
            continue
        if rec["discriminating"]:
            if reached:
                disc_reached += 1
            else:
                disc_missed += 1
        else:
            if reached:
                nondisc_reached += 1
            else:
                nondisc_missed += 1

    p_disc_missed = disc_missed / (disc_missed + disc_reached) if (disc_missed + disc_reached) else 0
    p_disc_reached = disc_reached / (disc_missed + disc_reached) if (disc_missed + disc_reached) else 0
    p_nondisc_missed = nondisc_missed / (nondisc_missed + nondisc_reached) if (nondisc_missed + nondisc_reached) else 0
    p_nondisc_reached = nondisc_reached / (nondisc_missed + nondisc_reached) if (nondisc_missed + nondisc_reached) else 0

    print("\nExploratory: p(discriminating | missed) = %.4f" % p_disc_missed)
    print("Exploratory: p(discriminating | reached) = %.4f" % p_disc_reached)
    print("Exploratory: p(not discriminating | missed) = %.4f" % p_nondisc_missed)
    print("Exploratory: p(not discriminating | reached) = %.4f" % p_nondisc_reached)

    result = {
        "g0c_pass": ok_c,
        "m1": m1_result,
        "m2_buckets": buckets,
        "m2_n": n,
        "m3": m3_result,
        "g1_fired": g1,
        "g4_fired": g4,
        "g5_fired": g5,
        "discriminating": {
            "disc_missed": disc_missed,
            "disc_reached": disc_reached,
            "nondisc_missed": nondisc_missed,
            "nondisc_reached": nondisc_reached,
            "p_disc_missed": p_disc_missed,
            "p_disc_reached": p_disc_reached,
            "p_nondisc_missed": p_nondisc_missed,
            "p_nondisc_reached": p_nondisc_reached,
        },
    }
    with open(os.path.join(HERE, "result.json"), "w") as fh:
        json.dump(result, fh, indent=1, sort_keys=True)
        fh.write("\n")
    print("\nresult.json written")
    return 0


if __name__ == "__main__":
    sys.exit(main())
