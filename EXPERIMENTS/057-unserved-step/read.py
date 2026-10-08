"""E057 read: per row, record what the requester holds, what they have already
tried, and what interface they say is missing. G2 (serving) is decided from the named
tools, not from search results.
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

# tool names and the vocabulary a search would need; matched case-insensitively as
# whole words or url fragments, and reported with the row they came from.
TOOLS = [
    "bricklink", "brickset", "rebrickable", "brickognize", "brick scout", "brick scout app",
    "pick a brick", "lego ideas", "lego.com", "google lens", "lens.google", "google images",
    "reverse image", "yandex", "tineye", "pimEyes", "bing visual", "duckduckgo",
    "ebay", "mercari", "worthpoint", "brickhunter", "brickset.com", "the pirate bay",
    "pewpew", "brickset id", "set number", "stud.io", "lego digital designer", "ldd",
    "bike database", "bikes Database".lower(), "bicycle database", "vintage bike",
    "serial number", "bike stamp", "forum", "facebook group", "reddit",
    "iNaturalist", "inaturalist", "seek", "plantnet", "picturethis", "google lens",
    "merlin bird id", "birdsoftheworld", "ebird", "mushroom observer", "observer.org",
    "bugguide", "nature gate", "leaflet", "whatistheplant", "plant.id",
    "chatgpt", "gpt-4", "claude", "copilot", "gemini", "perplexity",
    "wikipedia", "wiki", "eBay sold listings", "sold listings", "sold.completed",
]
TOOLS.sort(key=len, reverse=True)

# what the requester says they already tried or already know
TRIED = re.compile(
    r"\b(i (?:have |)(?:already )?tried|searched|googled|looked (?:up|for)|checked|"
    r"used|downloaded|uploaded|posted|asked|reversed|found (?:nothing|no))\b", re.I)
# what interface is absent: the ask that no named tool answers
LACK = re.compile(
    r"\b(no (?:body|box|instructions?|manual|list|number|name)|"
    r"without (?:the )?(?:box|instructions?|manual|part numbers?)|"
    r"can(?:'|no)t (?:find|figure|tell)|cannot (?:find|figure|tell)|"
    r"don(?:'|’)t know (?:the )?(?:model|make|set|brand|year|part number|shape|colour|color)|"
    r"(?:do not|don(?:'|’))t know (?:what|which|how))\b", re.I)


def main():
    summary = {}
    for param, name in (("bricks", "Bricks"), ("bicycles", "Bicycles"), ("biology", "Biology")):
        fn = os.path.join(HERE, "bodies-%s.json" % param)
        if not os.path.exists(fn):
            continue
        rows = json.load(open(fn))
        named = {}
        ntried = nlack = 0
        with open(os.path.join(HERE, "read-%s.txt" % param), "w") as fh:
            fh.write("# E057 per-row read: %s (%d bodies)\n\n" % (name, len(rows)))
            for r in rows:
                text = (r["title"] + " . " + r["body"]).lower()
                hits = sorted(set(t for t in TOOLS if t in text))
                for t in hits:
                    named[t] = named.get(t, 0) + 1
                tried = bool(TRIED.search(r["body"]))
                lack = bool(LACK.search(r["body"]))
                ntried += tried
                nlack += lack
                fh.write("== q%s uid=%s%s%s\n" % (r["question_id"], r["uid"],
                                                 "  [tried-something]" if tried else "",
                                                 "  [states-missing]" if lack else ""))
                fh.write("   TITLE: %s\n" % r["title"])
                fh.write("   BODY : %s\n\n" % r["body"][:1400])
        summary[name] = {"bodies": len(rows), "named_tools": named,
                          "rows_saying_they_tried_something": ntried,
                          "rows_stating_what_is_missing": nlack}
    with open(os.path.join(HERE, "read-index.json"), "w") as fh:
        json.dump(summary, fh, indent=1)
    print(json.dumps(summary, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
