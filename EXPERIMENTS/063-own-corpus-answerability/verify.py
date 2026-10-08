#!/usr/bin/env python3
"""G2 for E063: do the artifacts named as remedies actually exist?

A rubric that names a tool that does not exist is inflating the served numerator
(F036's shape: an instrument that answers well-formed and unrelated). For every
remedy artifact named in a `served` row, resolve it on a public index, and run the
two controls the mission's probe rule requires: a known-answer control (a package
that certainly exists) and a nonsense-token control (a name that certainly does
not).

Stdlib only. Writes raw/remedy-verification.json.
"""
import json
import os
import ssl
import sys
import urllib.error
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")
CTX = ssl.create_default_context()
UA = "think-free-e063/1.0 (answerability check)"

# (name, kind, urls). kind is how the probe is read: pypi/npm/github/host.
# Several artifacts live under an owner I first guessed wrong, or on a mirror;
# the protocol counts an artifact as verified if it resolves on a channel that
# actually carries it, and the first (wrong) URL is kept in the record so the
# correction is visible rather than silent.
ARTIFACTS = [
    ("skopeo", "github", ["https://api.github.com/repos/containers/skopeo"]),
    ("umoci", "github", ["https://api.github.com/repos/opencontainers/umoci"]),
    ("hnrss.org", "host", ["https://hnrss.org/user?id=pg",
                           "https://hnrss.org/"]),
    ("exiftool", "host", ["https://exiftool.org/"]),
    ("camelot-py", "pypi", ["https://pypi.org/pypi/camelot-py/json"]),
    ("tabula-py", "pypi", ["https://pypi.org/pypi/tabula-py/json"]),
    ("pdfplumber", "pypi", ["https://pypi.org/pypi/pdfplumber/json"]),
    ("geopy", "pypi", ["https://pypi.org/pypi/geopy/json"]),
    ("censusgeocode", "pypi", ["https://pypi.org/pypi/censusgeocode/json"]),
    ("nominatim", "host", ["https://nominatim.org/"]),
    ("migra", "github", ["https://api.github.com/repos/djrobstep/migra"]),
    ("difftastic", "github", ["https://api.github.com/repos/Wilfred/difftastic"]),
    ("kyverno", "github", ["https://api.github.com/repos/kyverno/kyverno"]),
    ("NeatVI", "github", ["https://api.github.com/repos/vivid/NeatVI",
                          "https://api.github.com/repos/aligrudi/neatvi"]),
    ("chafa", "github", ["https://api.github.com/repos/hpjansson/chafa"]),
    ("xpra", "github", ["https://api.github.com/repos/Xpra-org/xpra"]),
    ("newsboat", "github", ["https://api.github.com/repos/newsboat/newsboat"]),
    ("miniflux", "github", ["https://api.github.com/repos/miniflux/v2"]),
    ("RSSHub", "github", ["https://api.github.com/repos/DIYgod/RSSHub"]),
    ("pgn.js", "github", ["https://api.github.com/repos/chessboardjs/pgn.js"]),
    ("chessground", "github", ["https://api.github.com/repos/lichess-org/chessground"]),
    ("qpwgraph", "github", ["https://api.github.com/repos/rpcosta/qpwgraph",
                            "https://api.github.com/repos/rncbc/qpwgraph"]),
    ("pavucontrol", "github", ["https://api.github.com/repos/pavucontrol/pavucontrol",
                               "https://api.github.com/repos/pulseaudio/pavucontrol"]),
    # controls
    ("CONTROL-known-answer-requests", "pypi",
     ["https://pypi.org/pypi/requests/json"]),
    ("CONTROL-nonsense-token-9f3", "pypi",
     ["https://pypi.org/pypi/zzq-not-a-real-package-9f3/json"]),
    ("CONTROL-nonsense-token-4b1", "github",
     ["https://api.github.com/repos/zzq-not-a-real-org-4b1/zzq-not-a-real-repo-4b1"]),
]


def probe(url, timeout=20):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=CTX) as resp:
            body = resp.read(400)
            return {"status": resp.getcode(), "bytes": len(body)}
    except urllib.error.HTTPError as exc:
        return {"status": exc.code, "error": "http"}
    except Exception as exc:  # noqa: BLE001 - a transport failure is data
        return {"status": None, "error": type(exc).__name__}


def main():
    results = {}
    for name, kind, urls in ARTIFACTS:
        attempts = []
        for url in urls:
            got = probe(url)
            attempts.append(dict(got, url=url))
            if got["status"] == 200:
                break
        results[name] = {
            "kind": kind,
            "status": attempts[-1]["status"],
            "resolved_on": attempts[-1]["url"] if attempts[-1]["status"] == 200
                           else None,
            "attempts": attempts,
        }
        sys.stderr.write("%-32s %s\n" % (name, results[name]["status"]))
    named = {k: v for k, v in results.items() if not k.startswith("CONTROL-")}
    resolved = [k for k, v in named.items() if v["status"] == 200]
    known = results["CONTROL-known-answer-requests"]["status"]
    nonsense = [v["status"] for k, v in results.items()
                if k.startswith("CONTROL-nonsense")]
    out = {
        "n_named": len(named),
        "n_resolved_200": len(resolved),
        "share_resolved": round(len(resolved) / float(len(named)), 4),
        "unverified": sorted(k for k in named if k not in resolved),
        "gate_met": (len(resolved) / float(len(named)) >= 0.90
                     and known == 200 and all(s in (404, 403, None) for s in nonsense)),
        "controls": {
            "known_answer_status": known,
            "nonsense_statuses": nonsense,
        },
        "per_artifact": results,
    }
    with open(os.path.join(RAW, "remedy-verification.json"), "w") as fh:
        json.dump(out, fh, indent=1, sort_keys=True)
    print(json.dumps({k: v for k, v in out.items() if k != "per_artifact"},
                     indent=1, sort_keys=True))


if __name__ == "__main__":
    main()
