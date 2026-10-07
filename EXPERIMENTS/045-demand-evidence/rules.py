#!/usr/bin/env python3
"""E045's rule classifier — the instrument whose precision was measured.

Split out of `read.py` because this file is one thing: the rules that assign a
requester class and a gap class to an issue by pattern-matching the issue's own
text. Its measured agreement with the reader is precision 0.372, recall 0.552
(D069), and one of its classes (`line-coordinate`) matches `file:line` source
citations inside CI transcripts rather than git staging coordinates, which is
why 14 of its 43 rows are unrelated issues. Those numbers belong to the rules
and to nothing else, so the rules live where they can be read against them.

Every rule is a literal pattern over the issue's own text, so any row can be
re-derived by a reader who disagrees with the label. Nothing here consults the
reader's hand labels; that comparison happens in `read.py`, after the labels
have been loaded, and it is the only place the two are joined.
"""

import re

# The gap classes that count as the need item 0a measures. Kept here, with the
# rules, because the precision/recall figures are computed over this set and a
# reader re-checking the figures has to find the set they were computed over.
NEED_GAPS = ("select-lines", "line-coordinate", "unstage-one")

# --- requester class -------------------------------------------------------
# Decided from what the issue says about who is running the operation. The
# order matters: the first rule that matches wins, and every rule is a literal
# pattern over the issue's own text, so a reader can re-derive the row.
REQUESTER_RULES = [
    # A GUI/editor user asking for a feature in an editor or client repo.
    ("gui-human", [
        r"\bsublime\b", r"\bvs ?code\b", r"\bvisual studio code\b", r"\bvim\b",
        r"\bneovim\b", r"\bneogit\b", r"\bmagit\b", r"\bemacs\b", r"\bjetbrains\b",
        r"\bintellij\b", r"\bpycharm\b", r"\bwebstorm\b", r"\bidea\b",
        r"\bfork\b", r"\btower\b", r"\bsourcetree\b", r"\bgithub desktop\b",
        r"\beditor\b", r"\bide\b", r"\bgui\b", r"\bui\b", r"\bclient\b",
        r"\bkeybinding\b", r"\bshortcut\b", r"\bkey map\b", r"\bhotkey\b",
    ]),
    # An automated caller: a script, a hook, a bot, a tool, a library.
    ("script", [
        r"\bscript\b", r"\bshell script\b", r"\bbash\b", r"\bshell\b",
        r"\bpython script\b", r"\bpowershell\b", r"\bcommand line\b",
        r"\bcli\b", r"\bautomation\b", r"\bautomate\b", r"\bautomated\b",
        r"\bbatch\b", r"\bnon-?interactive\b", r"\bunattended\b",
        r"\bmakefile\b", r"\bci\b", r"\bcontinuous integration\b",
        r"\bjenkins\b", r"\bgithub action\b", r"\bworkflow\b",
        r"\btool\b", r"\blibrary\b", r"\bwrapper\b", r"\bplugin\b",
        r"\bapi\b", r"\bprogrammatic\b", r"\bhook\b",
    ]),
    # A coding agent: an LLM-driven editor/assistant, or a person driving one.
    ("agent", [
        r"\bcursor\b", r"\bcopilot\b", r"\bcline\b", r"\baider\b",
        r"\bclaude\b", r"\bchatgpt\b", r"\bgpt-?\d\b", r"\bllm\b",
        r"\blangchain\b", r"\bagent\b", r"\bagentic\b", r"\bmcp\b",
        r"\bmodel context protocol\b", r"\bautonomous\b", r"\bassistant\b",
        r"\bwindsurf\b", r"\bcline\b", r"\broo ?code\b", r"\bzed\b",
        r"\bbigcode\b", r"\bcontinue\b", r"\bdevin\b", r"\btabnine\b",
    ]),
]

# --- the interface the requester says they lack ----------------------------
# Ordered; the first match names the gap. Each entry is (label, patterns).
GAP_RULES = [
    # Wants to *select* lines rather than answer a whole-file prompt. This is
    # the operation stg performs, regardless of who asks.
    ("select-lines", [
        r"\bselect(?:ing|s)? (?:specific |particular |only |just )?lines?\b",
        r"\b(?:pick|choose|select) (?:which |what )?lines?\b",
        r"\bstage (?:just |only |specific |particular |a single |single |some |certain )?(?:changed |modified |selected )?lines?\b",
        r"\bstage (?:just |only |specific |particular |a single |single |some |certain )?(?:changed |modified )?(?:one|two|three|\d+)\s+lines?\b",
        r"\b(?:partial(?:ly)?|selective) st(?:age|aging) (?:a |of )?(?:single |one |specific |particular )?lines?\b",
        r"\bline[- ]?(?:level|wise|granular) (?:stage|staging)\b",
        r"\bstage (?:the )?lines? (?:you|we|i) (?:changed|modified)\b",
    ]),
    # Says the coordinate is the thing they have and cannot use.
    ("line-coordinate", [
        r"\bstage (?:by |at )?line (?:number|#|no\.?)\b",
        r"\bline numbers?\b", r"\b\d+-based line\b", r"\bfirst line of the hunk\b",
        r"\bgiven (?:a|the) line\b",
    ]),
    # git add -p exists but is interactive; asks for a non-interactive route.
    ("non-interactive", [
        r"\bnon-?interactive\b",
        r"\bwithout (?:being )?(?:interactive|interactive mode|manual|manually)\b",
        r"\bprogrammatic(?:ally)?\b", r"\bautomate[ds]?\b", r"\bautomation\b",
        r"\bnot? (?:possible|able) to (?:use )?(?:interactively)\b",
        r"\bunattended\b", r"\bfrom a script\b", r"\bvia (?:an? )?(?:api|script)\b",
    ]),
    # Splitting a hunk automatically rather than by hand.
    ("auto-split-hunk", [
        r"\bsplit (?:the )?hunks?\b", r"\bs\)\s*split\b", r"\bauto(?:matically)? split\b",
        r"\bsplitting hunks?\b", r"\bhunk too (?:large|big)\b",
    ]),
    # Revert/stage one change back out — the inverse of stg.
    ("unstage-one", [
        r"\bunstage (?:just |only |a single |single |some |specific |particular )?lines?\b",
        r"\bun-?stage (?:just |only )?(?:one|single|a)\b",
        r"\brevert (?:just |only |a single |single )?lines?\b",
    ]),
]


def first_match(rules, text):
    """The first rule that fires, with the matched span and its surroundings.

    The context is returned so a reader can see *why* a row was labelled the way
    it was without opening the issue, which is what makes the 0.372 precision
    checkable row by row rather than in aggregate.
    """
    tl = text.lower()
    for label, pats in rules:
        for p in pats:
            m = re.search(p, tl, re.IGNORECASE)
            if m:
                start = max(0, m.start() - 60)
                return label, m.group(0), text[start:m.end() + 60]
    return None, None, None


def has_diff_access(issue, text):
    """Does the requester say, or does the repository imply, that they can see
    a diff? Three evidence classes, reported separately, never collapsed.

    `none` is the class item 0a's population would have to come from, so it is
    returned as its own value rather than folded into a boolean: E045's result
    is that 0 of 189 rows carry it, and that number is only meaningful if the
    test for it is visible.
    """
    tl = text.lower()
    explicit = [
        r"\bgit diff\b", r"\bthe diff\b", r"\bdiff view\b", r"\bdiff pane\b",
        r"\bsee the (?:diff|change)\b", r"\bshow(?:s|ing)? (?:me )?the (?:diff|change)\b",
        r"\bdiff(?:ing)? (?:view|panel|tab|editor)\b",
    ]
    implied_gui = [
        r"\bhighlight(?:ed|ing)? (?:the |my |changed )?lines?\b",
        r"\bgutter\b", r"\bgitgutter\b", r"\bside[- ]by[- ]side\b",
        r"\bclick (?:on )?the (?:diff|line)\b", r"\bclicking (?:on )?the (?:diff|line)\b",
    ]
    for p in explicit:
        if re.search(p, tl, re.IGNORECASE):
            return "explicit"
    for p in implied_gui:
        if re.search(p, tl, re.IGNORECASE):
            return "gui-implied"
    return "none"