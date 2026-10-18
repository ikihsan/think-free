#!/usr/bin/env python3
"""E181: emit facts.jsonl for the rows `EXT` judged, and refuse anything unquoted.

The reader judgement is the twenty `FACTS` entries below. This script does not
judge; it only types what the reader decided and then proves, mechanically,
that every `quote` is a verbatim substring of the file the reader saw, and that
every `quote` appears in the comment section and not in the question. A typo in
a quote is an unrecoverable contamination once answers exist, so it is caught
here rather than by a later reader.

Run: python3 EXPERIMENTS/181-fact-supply-closes-gap/write_facts.py <rows...>
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

# (n, qid, fact, source, quote)  -- quote is a verbatim substring of ext/<nn>-<qid>.txt
FACTS = [
    (5, 79602687,
     "The reporter's resolved Expo Metro config has `unstable_enablePackageExports` set to false, "
     "and they are on Expo 53.0.6 rather than the 53.0.5 the question names.",
     "answer_comments",
     "Plus logging the config also shows the unstable_enablePackageExports got set to false. "
     "The only difference in our versions is I'm on Expo 53.0.6."),
    (6, 79843062,
     "The project has EntityFrameworkCore.Design version 10.x installed, which the reporter confirms.",
     "question_comments",
     "I found out that those folders appear when installing EntityFrameworkCore.Design (Version >= 10)"),
    (7, 79818015,
     "The reporter is on iOS 26.3 and the transparent container is still present there.",
     "question_comments",
     "This is still an issue in 26.3."),
    (8, 79871713,
     "It still reproduces on iOS 26.3 with Xcode 26.2, beyond the 26.1 and 26.2 the reporter reports.",
     "question_comments",
     "xcode 26.2, iOS 26.3"),
    (9, 79754247,
     "The warning appears only in the `apk` output; an app bundle built from the same project is clean.",
     "question_comments",
     "I have found out that this happens only with apk. With bundle everything is OK."),
    (13, 79791886,
     "The reporter's C library has RAND_MAX = 32767, against a range span of 20001.",
     "question_comments",
     "`RAND_MAX` = 32,767"),
    (14, 79718097,
     "The x86-64 System V ABI guarantees a 128-byte red zone below RSP that asynchronous signal "
     "handlers cannot clobber, which is what makes the mov-then-sub sequence legal without touching RSP.",
     "question_comments",
     "The x86-64 System V ABI has a red zone, 128 bytes below RSP which are guaranteed not to be "
     "asynchronously clobbered"),
    (16, 79380514,
     "The project installed Tailwind CSS v4, not v3; the question never states the version.",
     "question_comments",
     "The question is relevant specifically to TailwindCSS v4"),
    (18, 79665976,
     "uv on the home machine was installed by the curl installer, not by pip install.",
     "answer_comments",
     "However, my machine at home is using the uv installed by curl, not by pip install."),
    (20, 79663905,
     "The reporter is on an early iOS 26 beta - beta 2 through beta 8 - not a release build.",
     "question_comments",
     "It's still not fixed as of Xcode 26/iOS 26 beta 2."),
]

NULLS = [
    (1, 79723342, "the question already names `build.gradle`, and every comment adds advice or a "
                  "fix rather than an observation of the reporter's setup"),
    (2, 79408101, "comments link another answer and one person reports the same failure; no "
                  "observation of the reporter's setup is recorded"),
    (3, 79556333, "comments supply the styling recipe itself, which is the resolution, not a fact "
                  "the reporter is missing"),
    (4, 79817405, "comments report other reporters' .NET SDK versions and a version that worked "
                  "for them; the reporter's own SDK and EF package versions are never stated"),
    (10, 79368095, "comments are duplicate-flag discussion between two users and contain no fact"),
    (11, 79428308, "the single comment restates the cleanup the question already reports trying"),
    (12, 79600161, "comments offer alternatives and forks and one reporter's own replacement; no "
                   "observation of the reporter's setup is recorded"),
    (15, 79779187, "the one question comment asks whether a deprecated SDK is in use; it records no "
                   "fact and the accepted answer's comments are about other reporters' API keys"),
    (17, 79335513, "comments give the remedy (run as administrator, install 'just for me'); the "
                   "reporter's own install scope is never stated"),
    (19, 79818917, "the question already lists all four installed package versions, and the comment "
                   "names the module that fixed it, which is the resolution"),
]


def main():
    pop = json.load(open(os.path.join(HERE, "population.json")))
    by_qid = dict((m["qid"], m) for m in pop["manifest"])
    rows = set(sys.argv[1:])
    extra = json.load(open(os.path.join(HERE, "extra_facts.json"))) \
        if os.path.exists(os.path.join(HERE, "extra_facts.json")) else []
    out = []
    for entry in FACTS + [tuple(e) for e in extra]:
        n, qid, fact, source, quote = entry[0], entry[1], entry[2], entry[3], entry[4]
        if rows and qid not in rows:
            continue
        m = by_qid[qid]
        body = open(os.path.join(HERE, m["file"])).read()
        head = body.index("COMMENTS ON THE QUESTION")
        assert quote in body, "quote %d/%d is not verbatim in %s" % (n, qid, m["file"])
        assert quote not in body[:head], "quote %d/%d appears in the QUESTION" % (n, qid)
        want = ("COMMENTS ON THE QUESTION" if source == "question_comments"
                else "COMMENTS ON THE ANSWER THAT WAS ACCEPTED")
        tail = body[body.index(want):]
        assert quote in tail, "quote %d/%d is not in the %s section" % (n, qid, source)
        out.append({"n": n, "qid": qid, "fact": fact, "source": source, "quote": quote})
    for n, qid, why in NULLS:
        if rows and qid not in rows:
            continue
        out.append({"n": n, "qid": qid, "fact": None, "source": None, "quote": None,
                    "null_reason": why})
    out.sort(key=lambda r: r["n"])
    with open(os.path.join(HERE, "facts.jsonl"), "w") as fh:
        for r in out:
            fh.write(json.dumps(r, sort_keys=True) + "\n")
    got = sum(1 for r in out if r["fact"])
    print("rows %d, facts %d (%.4f), nulls %d" % (len(out), got, got / float(len(out)),
                                                 len(out) - got))
    assert len(out) == len(set(r["qid"] for r in out)), "duplicate qid"
    assert len(out) == len(by_qid), "expected %d rows, wrote %d" % (len(by_qid), len(out))


if __name__ == "__main__":
    main()