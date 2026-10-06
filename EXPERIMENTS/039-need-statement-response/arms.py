#!/usr/bin/env python3
"""E039: build the two arms from the captured comment rows.

Arm A  - the 1401 need comments: reply subtree size, whether the requester came
         back, and whether an off-site link appears in the subtree.
Arm B  - every other comment in the same stories: the matched within-story
         control that makes H0 (position in a thread explains everything)
         checkable rather than merely arguable.

Subtree sizes, heights, hosts and "the author spoke again" are accumulated in one
reverse topological pass per story. The first version re-walked each node's
descendants, which is quadratic in depth and did not finish on 278k rows.

The novelty gate's denominator is each comment's OWN links, never its subtree's:
using subtree hosts would make every host in a busy thread look common and would
suppress novelty by construction.
"""
import json, os, re
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")

# Hosts excluded from the link census: every one of them is where the reply
# lives rather than what the reply is about. Excluding them can only lower the
# measured link rate, so it is the conservative direction.
HOF = re.compile(r"(news\.ycombinator\.com|google\.com|github\.com|youtube\.com|"
                 r"twitter\.com|x\.com|reddit\.com|arxiv\.org|wikipedia\.org|"
                 r"linkedin\.com|medium\.com|substack\.com|amazon\.com)", re.I)
TAG = re.compile(r"<[^>]+>")
ENT = {"&#x27;": "'", "&#39;": "'", "&quot;": '"', "&gt;": ">", "&lt;": "<",
       "&amp;": "&", "&#x2F;": "/", "&#x3D;": "="}
URL = re.compile(r"https?://([^\s\"'<>\)\]]+)", re.I)


def unescape(text):
    t = TAG.sub(" ", text or "")
    for k, v in ENT.items():
        t = t.replace(k, v)
    return t


def hosts(text):
    out = set()
    for m in URL.findall(unescape(text)):
        h = m.lower().split("/")[0].split("?")[0].split(":")[0]
        if h.startswith("www."):
            h = h[4:]
        if h and not HOF.search(h):
            out.add(h)
    return out


def main():
    corpus = os.path.join(HERE, "..", "012-candidate-harvest", "raw",
                          "hn_needs_2026-10-04.jsonl")
    needs = {str(json.loads(l)["id"]) for l in open(corpus)}

    by_story = defaultdict(list)
    for line in open(os.path.join(RAW, "comments.jsonl")):
        r = json.loads(line)
        by_story[r["story_id"]].append(r)

    arm_a, arm_b = [], []
    for sid in sorted(by_story):
        srows = by_story[sid]
        ids = {r["id"] for r in srows}
        kids = defaultdict(list)
        for r in srows:
            if r["parent_id"]:
                kids[r["parent_id"]].append(r["id"])

        # Parents before children.
        order, depth = [], {}
        roots = [r["id"] for r in srows if not r["parent_id"] or r["parent_id"] not in ids]
        stack, seen = list(roots), set(roots)
        while stack:
            cur = stack.pop()
            order.append(cur)
            for c in kids.get(cur, []):
                if c in seen:
                    continue
                seen.add(c)
                depth[c] = depth.get(cur, 0) + 1
                stack.append(c)
        for r in srows:
            if r["id"] not in seen:
                seen.add(r["id"])
                order.append(r["id"])
                depth.setdefault(r["id"], 1)

        text_of = {r["id"]: r["text"] for r in srows}
        author_of = {r["id"]: r["author"] for r in srows}
        own = {i: hosts(text_of[i]) for i in order}

        subtree = {i: 0 for i in order}
        height = {i: 0 for i in order}
        sub_hosts = {i: set(own[i]) for i in order}
        sub_links = {i: (1 if own[i] else 0) for i in order}
        returned = {i: False for i in order}
        for i in reversed(order):
            ch = kids.get(i) or []
            if not ch:
                continue
            subtree[i] = sum(1 + subtree[c] for c in ch)
            height[i] = max(height[c] for c in ch) + 1
            hs = set(sub_hosts[i])
            nl = sub_links[i]
            ret = returned[i]
            for c in ch:
                hs |= sub_hosts[c]
                nl += sub_links[c]
                if sub_links[c] and author_of.get(c) == author_of.get(i):
                    ret = True
            sub_hosts[i], sub_links[i], returned[i] = hs, nl, ret

        # Novelty denominator: each comment's own links.
        host_counts = defaultdict(int)
        for i in order:
            for h in own[i]:
                host_counts[h] += 1
        own_links = sum(host_counts.values())
        story_total = len(srows)

        for r in srows:
            cid = r["id"]
            sub = subtree[cid] > 0
            rec = {
                "id": cid, "story_id": sid, "author": r["author"],
                "created_at_i": r["created_at_i"], "story_total": story_total,
                "is_need": cid in needs,
                "direct_replies": len(kids.get(cid, [])),
                "subtree": subtree[cid], "depth": height[cid],
                "has_subtree": sub,
                "asker_returned": returned[cid] if sub else None,
                "link_replies": sub_links[cid] - 1 if sub else 0,
                "reply_hosts": sorted(sub_hosts[cid]),
                "novel_hosts": sorted(h for h in sub_hosts[cid]
                                      if own_links and host_counts.get(h, 0) * 100 < own_links),
            }
            (arm_a if rec["is_need"] else arm_b).append(rec)

    with open(os.path.join(RAW, "arms.jsonl"), "w") as f:
        for rec in arm_a:
            f.write(json.dumps(rec, sort_keys=True) + "\n")
    with open(os.path.join(RAW, "control.jsonl"), "w") as f:
        for rec in arm_b:
            f.write(json.dumps(rec, sort_keys=True) + "\n")
    print("arm A (needs): %d   arm B (controls): %d   stories: %d"
          % (len(arm_a), len(arm_b), len(by_story)))


if __name__ == "__main__":
    main()