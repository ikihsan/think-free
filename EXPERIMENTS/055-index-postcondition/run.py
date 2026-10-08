#!/usr/bin/env python3
"""E055: run every stager arm, then ask `indexcheck` what the index holds.

    python3 run.py            # controls, arms, results.json, the KILL-C verdict
    python3 run.py --verify   # controls only, for the task's verify command

Declared in PROTOCOL.md. Four properties here are load-bearing, and each is a
failure this record has already recorded once:

- **An arm that cannot run is `not_evaluated`, never a pass.** E047's arms refused
  to start on git 2.25.1 and both refusal and success read as "no sweep" (F010,
  F084). `require_git` stops the run below 2.28.
- **The grader never reads an arm's output.** `indexcheck.py` gets E038's
  hand-written `want_content` and the repository, and nothing else.
- **Both grader controls run before any arm.** A grader that accepts a wrong index
  cannot be trusted to reject one, and one that rejects a correct index cannot be
  trusted to accept one. If either fails, the arms are not run at all.
- **KILL-C is computed, not narrated.** `kill_c()` is a pure function of the rows,
  and `test_gates_falsified.py` asserts it can return each answer.
- **The artifact names the code that wrote it.** Every `raw/` file carries the sha256
  of each script, and `--verify` recomputes them, because `ceiling.py` was once edited
  ten seconds after it wrote `raw/ceiling.json` and the mismatch was invisible from
  the artifact alone. See `provenance.py`.
"""

import hashlib
import json
import os
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "038-staging-prior-art"))

import controls                                                    # noqa: E402
import k3probe                                                      # noqa: E402
import probecontrols                                                # noqa: E402
import provenance                                                   # noqa: E402
from arms import ARMS                                               # noqa: E402
from compare import CASES as E038_CASES, CONTEXTS                  # noqa: E402
from controls import make_repo, score                              # noqa: E402
from gitenv import ctx_env, require_git                             # noqa: E402

# Every control, in the order it is run. Split by invariant into `controls` (the
# grader's bounds) and `probecontrols` (the probe's), and composed here so the set
# that gates the run is stated in one place rather than in either module.
ALL = controls.GRADER_CONTROLS + probecontrols.PROBE_CONTROLS

# An arm carries K2 only if it takes a **line coordinate in its own best case** and
# is shipped. `git-hunk-naive` passes a file line where the tool wants a body
# position on purpose (`arms.py`); `naive` never addresses a line at all, so
# "staged the whole hunk" is its documented behaviour and not a claim it broke;
# `pty_driver` is this repository's own harness, and `stg` is unreleased. All four
# stay in the tally and are reported; none may carry a gate about an incumbent.
SHIPPED = ("filterdiff", "git-hunk-native")


def run_arms(root, cases=None, arms=None):
    """Every case × context × arm. `cases` and `arms` narrow it for a control."""
    rows = []
    for name, base, edited, want, want_content in (cases or E038_CASES):
        for context in CONTEXTS:
            env = ctx_env(context)
            for arm, fn in (arms or ARMS):
                d = make_repo(base, edited, root,
                              "a-%s-%s-%s" % (name, context, arm))
                try:
                    # The probe runs BEFORE the arm, on the pristine fixture. Run 2's
                    # first version ran it after, and every probe came back empty:
                    # `git diff` no longer shows lines the arm has already staged, so
                    # K3 was decided by a blind probe rather than by a measurement --
                    # indistinguishable from having no probe at all. C7 pins the
                    # ordering so it cannot move again silently.
                    probe = (k3probe.derive_verdict(d, want, env)
                             if arm in SHIPPED else None)
                    res = fn(d, want, env)
                    if isinstance(res, tuple):       # (exit, out, err) from sh()
                        res = {"exit": res[0], "out": res[1], "err": res[2]}
                    if "not_evaluated" in res and res.get("exit") is None:
                        row = {"case": name, "diff_context": context, "arm": arm,
                               "not_evaluated": res["not_evaluated"],
                               "grader": "not_evaluated", "counted": False}
                    else:
                        verdict, got, ok = score(d, want_content)
                        row = {"case": name, "diff_context": context, "arm": arm,
                               "exit": res.get("exit"), "counted": True,
                               "grader": verdict, "index_holds_intent": ok,
                               "silent": bool(res.get("exit") == 0 and not ok),
                               "index_sha256": hashlib.sha256(got).hexdigest()
                               if got is not None else None,
                               "index_preview": got.decode("utf-8", "replace")[:120]
                               if got is not None else None,
                               "selector": res.get("selector"),
                               "out": (res.get("out", "") + res.get("err", ""))[:240]}
                        if probe is not None:
                            row["k3"] = probe
                finally:
                    shutil.rmtree(d, ignore_errors=True)
                rows.append(row)
    return rows


def summarise(rows):
    out = {}
    for row in rows:
        a = out.setdefault(row["arm"], {
            "counted": 0, "holds": 0, "refused_nonzero": 0, "not_evaluated": 0,
            "silent_wrong": 0, "wrong": 0})
        if not row["counted"]:
            a["not_evaluated"] += 1
            continue
        a["counted"] += 1
        if row["index_holds_intent"]:
            a["holds"] += 1
        else:
            a["wrong"] += 1
            if row["silent"]:
                a["silent_wrong"] += 1
            else:
                a["refused_nonzero"] += 1
    return out


def kill_c(rows, control_rows):
    """The declared build decision, as a function of the rows alone.

    K2 asks whether a shipped arm exited 0 on a wrong index. K3 asks whether that
    arm's own output would have told the caller. Both are counted on **index bytes**,
    never on case names, because E038 carries cases with identical base and identical
    intent and a count taken over names reads one observation as six (F052).

    K3's operationalisation, corrected twice and recorded in PROTOCOL.md's
    amendments: it holds for a row when the lines the tool's own `--as-numbered-lines`
    reports name nothing but the line the caller asked for — the tool then claims a
    request it did not honour. A report naming any other line is *derivable* by the
    caller from the tool, so the checker adds nothing there. Both halves of the report
    are read, because `after` cannot see a carried deletion and `before` cannot see a
    carried addition; reading only `after` reported a superset on a row where the tool
    had in fact claimed exactly the wanted line.
    """
    tally = summarise(rows)
    silent = {a: t["silent_wrong"] for a, t in tally.items() if a in SHIPPED}
    k1 = all(c["fired"] for c in control_rows)
    k2 = any(v > 0 for v in silent.values())
    k3_evidence, k3 = [], False
    for row in rows:
        if row["arm"] not in SHIPPED or not row.get("silent"):
            continue
        probe = row.get("k3") or {"why": "no probe was recorded for this row"}
        entry = {"arm": row["arm"], "case": row["case"],
                 "diff_context": row["diff_context"],
                 "wrote_lines": probe.get("wrote_lines"),
                 "removed_old_lines": probe.get("removed_old_lines"),
                 "named_beyond_want": probe.get("named_lines_beyond_want"),
                 "index_sha256": row.get("index_sha256"),
                 "arm_output": (row.get("out") or "").strip()[:160],
                 "tool_claims_exactly_the_wanted_line":
                     probe.get("claims_only_the_wanted_line"),
                 "caller_can_derive_the_verdict":
                     probe.get("caller_can_derive_the_verdict"),
                 "probe_saw_a_line": probe.get("saw_any_line"),
                 "why": probe.get("why")}
        k3_evidence.append(entry)
        if probe.get("claims_only_the_wanted_line"):
            k3 = True
    # A probe that reported nothing is not a negative answer. Run 2's first version
    # counted it as one and returned `do_not_build` from a blind instrument, which is
    # the same failure as a parser that quietly stops matching: the number looks
    # clean and means nothing. Undecided rows make the whole verdict undecided.
    undecided = [e for e in k3_evidence if not e["probe_saw_a_line"]]
    distinct = {}
    for e in k3_evidence:
        distinct.setdefault(e["index_sha256"], []).append("%s/ctx=%s"
                                                          % (e["case"], e["diff_context"]))
    if undecided:
        verdict = "undecided"
    elif k1 and k2 and k3:
        verdict = "build"
    else:
        verdict = "do_not_build"
    return {"K1_controls_fired": k1,
            "K2_a_shipped_arm_exited_0_on_a_wrong_index": k2,
            "K3_a_shipped_arm_claimed_exactly_what_it_did_not_stage": k3,
            "silent_wrong_by_shipped_arm": silent,
            "silent_wrong_distinct_index_states": len(distinct),
            "silent_wrong_state_members": {k[:12]: v for k, v in distinct.items()},
            "k3_rows_probed": len(k3_evidence),
            "k3_rows_undecided": undecided,
            "k3_evidence": k3_evidence,
            "verdict": verdict}


def main(argv):
    verify_only = "--verify" in argv
    ok, ver = require_git()
    print("git: %s (need >= 2.28)" % ver)
    if not ok:
        print("REFUSING TO RUN: below git 2.28 the git-hunk arm cannot start, and "
              "an arm that never started reads as a clean result (F010, F084).")
        return 3
    root = tempfile.mkdtemp(prefix="e055-")
    try:
        control_rows = [fn(root, E038_CASES) for fn in ALL]
        for c in control_rows:
            print("%-34s fired=%-5s %s" % (
                c["name"], c["fired"],
                {k: v for k, v in c.items()
                 if k not in ("name", "fired", "detail", "failed", "missed",
                              "raw")}))
        if not all(c["fired"] for c in control_rows):
            print("REFUSING TO RUN ARMS: a control that should have fired did not.")
            return 3
        if verify_only:
            print("controls only (--verify)")
            # The artifact left by the last full run, and whether these bytes wrote
            # it. A run whose code no longer matches its own `raw/` cannot be
            # reproduced from the tree, which is the defect provenance.py exists for;
            # this is the command the task's verify step points at, so it is where
            # the check has to be to run at all (D025, F013).
            ok_prov, diff, note = provenance.check(
                os.path.join(HERE, "raw", "results.json"))
            print("provenance: %s%s" % (note,
                                        "" if ok_prov else "  <- RE-RUN to rebind"))
            for name in diff:
                print("  differs: %s" % name)
            return 0
        rows = run_arms(root)
    finally:
        shutil.rmtree(root, ignore_errors=True)

    doc = {"git_version": ver, "controls": control_rows, "rows": rows,
           "tally": summarise(rows),
           "provenance": {"scripts": provenance.stamp()}}
    doc["KILL_C"] = kill_c(rows, control_rows)
    raw = os.path.join(HERE, "raw")
    if not os.path.isdir(raw):
        os.makedirs(raw)
    with open(os.path.join(raw, "results.json"), "w") as fh:
        json.dump(doc, fh, sort_keys=True, indent=1)

    print("\n%-18s %7s %7s %9s %12s  %s" % ("arm", "counted", "holds", "refused",
                                          "silent-wrong", "not_evaluated"))
    for arm in sorted(doc["tally"]):
        t = doc["tally"][arm]
        print("%-18s %7d %7d %9d %12d  %d%s"
              % (arm, t["counted"], t["holds"], t["refused_nonzero"],
                 t["silent_wrong"], t["not_evaluated"],
                 "   <- carries K2" if arm in SHIPPED else ""))
    print("\nKILL_C: %s" % doc["KILL_C"]["verdict"])
    for key in sorted(k for k in doc["KILL_C"] if k.startswith("K")):
        print("  %-58s %s" % (key, doc["KILL_C"][key]))
    print("  silent-wrong rows in %d distinct index state(s); %d probed"
          % (doc["KILL_C"]["silent_wrong_distinct_index_states"],
             doc["KILL_C"]["k3_rows_probed"]))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
