"""Shared constants and request helpers for the E038 harvest."""
import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")
GH = "https://api.github.com"
SE = "https://api.stackexchange.com/2.3"
GREP = "https://grep.app/api/search"
DEBIAN = "https://codesearch.debian.net/api/v1/search"
UA = "think-free-research/1.0 (E038; contact: local repository)"

# ---------------------------------------------------------------------------
# Pool A: the interface, by mechanism name. Terms fixed in PROTOCOL.md section 3
# before any response was read. Each is a string a maintainer would plausibly type.
# ---------------------------------------------------------------------------
CODE_TERMS = [
    "stage selected ranges",
    "stageSelectedRanges",
    "stage_ranges",
    "stageRanges",
    "magit-stage-region",
    "stage a single line",
    "stage one line",
    "stage part of a file",
    "partial staging",
    "partial stage",
    "line-range staging",
    "stagerange",
    "rangeToStage",
    "stageLines",
    "stage_lines",
    "splitHunk",
    "split_hunk",
    "hunk by line",
    "unidiff-zero",
    "filterdiff",
    "git apply --cached",
    "add -p non-interactive",
    "add -p script",
    "interactive.diffFilter",
]

REPO_QUERIES = [
    "git add -p in:name,description,readme",
    "stage lines git in:name,description,readme",
    "partial staging git in:name,description,readme",
    "stg git staging in:name,description",
    "stage-lines in:name",
    "git hunk stage in:name,description,readme",
]

# ---------------------------------------------------------------------------
# Pool B: the capability in users' words. Four phrasings, two sites, plus the
# control that varies only the field (PROTOCOL.md section 3, Pool C).
# ---------------------------------------------------------------------------
NEED_SITES = ["stackoverflow", "superuser"]
NEED_QUERIES = [
    ("intitle", "stage specific lines"),
    ("intitle", "stage particular lines"),
    ("intitle", "stage only some of my changes"),
    ("intitle", "partially stage a file"),
    ("intitle", "git add -p line"),
    ("intitle", "git add line number"),
    ("intitle", "stage by line"),
    ("intitle", "stage only one line"),
    ("q", "git add -p non-interactive"),
    ("q", "git add -p script"),
    ("q", "git add -p automation"),
    ("q", "stage single line git"),
    ("q", "select lines to commit git"),
    ("q", "stage part of a line"),
    ("q", "stage only the lines I changed"),
]
# Control that varies only the field: the negative phrase, same route, same site.
NEGATIVE = "zzqxwv nonexistent phrase 4198"
# One-term deletions, applied to the two largest need rows after the first pass.
DELETIONS = [("intitle", "stage lines"), ("q", "git add -p non-interactive")]

PROBE = [
    ("probe-gh-code", GH + "/search/code?q=stageSelectedRanges&per_page=1"),
    ("probe-gh-repos", GH + "/search/repositories?q=stage+lines+git&per_page=1"),
    ("probe-grep-app", GREP + "?q=stageSelectedRanges"),
    ("probe-debian", DEBIAN + "?q=magit-stage-region&literal=1&per_page=1"),
    ("probe-se-info", SE + "/info?site=stackoverflow"),
    # Added after the first probe pass, when the first five had answered. All five
    # probes above are kept; this is a second pass, not a replacement.
    ("probe-gh-issues", GH + "/search/issues?q=%22stage+specific+lines%22&per_page=3"),
    ("probe-gh-rate", GH + "/rate_limit"),
    ("probe-so-rendered", "https://stackoverflow.com/search?q=stage+specific+lines"),
    ("probe-git-scm-add", "https://git-scm.com/docs/git-add"),
    ("probe-manpages-filterdiff",
     "https://manpages.debian.org/bookworm/patchutils/filterdiff.1.en.html"),
]

# ---------------------------------------------------------------------------
# Pool A2: primary sources, named before they were fetched. A source that answers
# is read in full; a source that 404s stays in the log as evidence of the gap.
# ---------------------------------------------------------------------------
SOURCES = [
    ("src-git-add-adoc",
     "https://raw.githubusercontent.com/git/git/master/Documentation/git-add.adoc"),
    ("src-git-apply-adoc",
     "https://raw.githubusercontent.com/git/git/master/Documentation/git-apply.adoc"),
    ("src-vscode-git-package",
     "https://raw.githubusercontent.com/microsoft/vscode/main/extensions/git/package.json"),
    ("src-vscode-git-readme",
     "https://raw.githubusercontent.com/microsoft/vscode/main/extensions/git/README.md"),
    ("src-magit-manual", "https://magit.vc/manual.html"),
    ("src-filterdiff-man",
     "https://manpages.debian.org/bookworm/patchutils/filterdiff.1.en.html"),
    ("src-neogit-readme",
     "https://raw.githubusercontent.com/NeogitOrg/neogit/master/README.md"),
    ("src-jj-reference", "https://raw.githubusercontent.com/jj-vcs/jj/main/docs/reference.md"),
]


def rows(path):
    if not os.path.exists(path):
        return
    with open(path) as fh:
        for line in fh:
            line = line.strip()
            if line:
                try:
                    yield json.loads(line)
                except ValueError:
                    continue


def get(url, headers=None):
    """Accept is set per-host: an HTML page served to an application/json client
    answers 406, which is an instrument artefact rather than a property of the
    source. API hosts get JSON; everything else gets what a browser sends."""
    hdrs = {"User-Agent": UA}
    hdrs["Accept"] = ("application/vnd.github+json" if GH in url else
                      "application/json" if SE in url else
                      "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8")
    if headers:
        hdrs.update(headers)
    req = urllib.request.Request(url, headers=hdrs)
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            status, body, final = r.status, r.read().decode("utf-8", "replace"), r.url
    except urllib.error.HTTPError as e:
        status, body, final = e.code, e.read().decode("utf-8", "replace"), url
    except Exception as e:                                        # noqa: BLE001
        status, body, final = -1, repr(e), url
    try:
        parsed = json.loads(body)
    except ValueError:
        parsed = {"_unparsed": body[:300]}
    n_items = None
    if isinstance(parsed, dict):
        for key in ("items", "results", "hits"):
            if key in parsed:
                n_items = len(parsed[key])
    return {
        "url": url, "final_url": final, "status": status,
        "elapsed_s": round(time.time() - t0, 3), "body": body,
        "n_items": n_items,
        "quota_remaining": parsed.get("quota_remaining") if isinstance(parsed, dict) else None,
        "error_message": parsed.get("error_message") or parsed.get("message"),
        "total_count": parsed.get("total_count") if isinstance(parsed, dict) else None,
    }


def emit(handle, record):
    handle.write(json.dumps(record, sort_keys=True) + "\n")
    handle.flush()


def label(rec):
    return "%-28s %3d items=%-5s total=%-8s q=%-5s %s" % (
        rec["measure"], rec["status"], rec["n_items"], rec["total_count"],
        rec["quota_remaining"], rec["error_message"] or "")


def do(handle, measure, url, **extra):
    rec = get(url)
    rec["measure"] = measure
    rec["ts"] = int(time.time())
    rec.update(extra)
    emit(handle, rec)
    print(label(rec), flush=True)
    time.sleep(0.4)
    return rec


def done():
    return set(r["measure"] for r in rows(os.path.join(RAW, "requests.jsonl")))


def budget():
    rec = get(SE + "/info?site=stackoverflow")
    print("SE quota_remaining", rec["quota_remaining"], "status", rec["status"])

