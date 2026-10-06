#!/usr/bin/env python3
"""E038 hand labels for the precision sample, and the precision they imply.

The keyword classifier in readout.py put 100 of 195 GitHub issues in "in-population".
Reading the mechanically selected sample shows most of those are not the need: a pull
request about a CI budget, a docs audit, a CSS rail. A classifier that cannot
distinguish the population from the corpus reports a number nothing measured.

So every row of the sample was read and labelled by hand against one question:

  Does this row state, or build, a way to select part of a working-tree change BY LINE
  NUMBER -- a caller naming a line and getting that change and nothing else?

Labels, and what each means for the population:
  yes-line    the need or the thing that serves it, in the candidate's terms
  yes-adjacent  the same operation, but not by line: hunk staging, editing a hunk,
                staging selections. Real demand, different interface.
  no          something else entirely

The two `yes-` labels are kept apart because the candidate's claim is about the
coordinate, not the operation. A row that wants hunk staging is evidence that people
want partial staging, not that they want a line number.

  python3 precision.py --score
"""
import sys

from precision import sample

# Hand labels, one per sampled row, in sample order. Written after reading every row.
HAND = {
    1: "yes-adjacent",    # lazygit: "add ability to edit hunk", wants finer than a line
    2: "no",              # nextpnr: post-placement frequency report
    3: "no",              # Onward: project scaffolding
    4: "no",              # academicOps: auto-mode classifier
    5: "no",              # spacemacs: magit status buffer rendering
    6: "yes-line",        # sublime_merge #976: Stage Line unusable when lines adjacent
    7: "no",              # Data_science_dev: perf ticket
    8: "no",              # AstroForge: docs close-out
    9: "no",              # AstroForge: docs close-out
    10: "no",             # kianos: history baseline
    11: "no",             # nushell: future ideas
    12: "yes-adjacent",   # GitUp: stage/unstage buttons next to chunks
    13: "no",             # SimplyBuild: discovery labels
    14: "no",             # rust: compilation progress
    15: "no",             # aws-cdk-cli: strips newlines from subprocess output
    16: "no",             # elastickv: encryption guard primitive
    17: "no",             # git-autofixup: temp index performance
    18: "no",             # trainspotting: collapse language stages
    19: "no",             # airi: mobile message padding
    20: "no",             # sublime_merge #1330: scroll position after stage all
    21: "no",             # ssv: widen test context budgets
    22: "no",             # kasb: upgrade stage reporting
    23: "no",             # agenthub: receipt readback
    24: "no",             # monorepo: browse-by setting
    25: "no",             # Trends2Targets: dead constant
    26: "no",             # compound-engineering-plugin: model tier
    27: "no",             # relay-ide: device UX spec
    28: "yes-adjacent",   # vscode: "Stage selected ranges" changes encoding
    29: "no",             # Stocket: two-stage LLM pipeline
    30: "yes-adjacent",   # sublime_merge #465: want to split hunks, currently by selection
    31: "no",             # financial-asset-relationship-db: lock ttl graph
    32: "yes-adjacent",   # tig #4: diff line numbers offset from file line numbers
    33: "no",             # ha-bambulab: model not detected
    34: "yes-line",       # vim-gitgutter #446: batch stage by line number range
    35: "no",             # DFIR-Companion: intrusion shape
    36: "no",             # DavidHLP: CSS rail overlap
    37: "no",             # GlobalyApp: spreadsheet staging status
    38: "no",             # perl-lsp-swarm: client stage expectations
    39: "no",             # OSS-2026-Mirobot: photo line extraction (drawing lines)
    40: "no",             # paperclip-rs: file_size_check coverage
    41: "no",             # IndustryGrow: spec topology figures
    42: "no",             # csl-orig: corrections batch
    43: "no",             # dnd3.5-spellbook: dice QA coverage
    44: "no",             # claude-all-in-one: conformance case
    45: "no",             # pmo-platform: milestone derivation
    46: "no",             # doctrine: tailwind fixes
    47: "no",             # horde: rev stamp
    48: "no",             # opencode-workflow-guard: TTY hang guard
    49: "no",             # gather: ship to production
    50: "no",             # claude: split-commits skill
    51: "yes-line",       # mcp-multi-root-git #3: hunk-level staging absent, agents
                          # cannot split single-file edits into n commits
    52: "no",             # EbookAutomation: VQA calibration
    53: "no",             # xum: one spawn for repo config
    54: "yes-adjacent",   # agent-orchestra: hook re-stages whole file, defeats add -p
    55: "no",             # amp-benchkit: LabJack stdout
    56: "no",             # AMEDEO: directory structure instructions
    57: "no",             # mcp-server: worktree automation
    58: "no",             # DekkhO: automated suggestion
    59: "yes-adjacent",   # nextjs-app-template: partial-stage warning in lefthook
    60: "no",             # Xafrun: dependency bump
    61: "no",             # tkt: worktree per change
}


def score():
    rows_ = sample()
    missing = [r["n"] for r in rows_ if r["n"] not in HAND]
    if missing:
        print("UNLABELLED rows: %s" % missing)
    labelled = [r for r in rows_ if r["n"] in HAND]
    n = len(labelled)
    line = [r for r in labelled if HAND[r["n"]] == "yes-line"]
    adj = [r for r in labelled if HAND[r["n"]] == "yes-adjacent"]
    no = [r for r in labelled if HAND[r["n"]] == "no"]
    kw = [r for r in labelled if r["keyword_label"] == "in-population"]
    tp = [r for r in kw if HAND[r["n"]] == "yes-line"]
    print("hand-labelled rows: %d" % n)
    print("  yes-line      %2d  (%.3f of the sample)" % (len(line), len(line) / n))
    print("  yes-adjacent  %2d  (%.3f)" % (len(adj), len(adj) / n))
    print("  no            %2d  (%.3f)" % (len(no), len(no) / n))
    print("\nprecision of the keyword classifier's in-population label:")
    print("  it labelled %d rows in-population" % len(kw))
    print("  %d of those are yes-line          precision %.3f"
          % (len(tp), len(tp) / len(kw) if kw else 0))
    print("  %d of those are yes-adjacent, %d are no"
          % (len(kw) - len(tp) - sum(1 for r in kw if HAND[r["n"]] == "no"),
             sum(1 for r in kw if HAND[r["n"]] == "no")))
    print("\nrecall against the hand labels:")
    print("  %d of %d yes-line rows the classifier did not label in-population: %s"
          % (sum(1 for r in line if r["keyword_label"] != "in-population"),
             len(line),
             [r["n"] for r in line if r["keyword_label"] != "in-population"]))
    print("\nrows that are about the operation but not the coordinate:")
    for r in adj:
        print("  [%2d] %-24s %s" % (r["n"], r["repo"], r["title"]))
    print("\nrows that are the coordinate itself:")
    for r in line:
        print("  [%2d] %-24s %s\n      %s" % (r["n"], r["repo"], r["title"], r["url"]))


if __name__ == "__main__":
    if "--score" in sys.argv:
        score()
    else:
        sample()
