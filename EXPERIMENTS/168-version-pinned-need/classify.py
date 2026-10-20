#!/usr/bin/env python3
"""E168 step 2: the `version_pinned` classifier, title + tags only.

Pass 1 is title+tags ONLY and never reads a body. That is a deliberate
property, not a shortcut: the candidate under test is a tool, so the label
this produces is the label a tool could produce. Pass 3 (audit_precision.py)
then reads bodies of a random sample of the vp=1 rows to estimate what that
title-only classifier is worth, which generalises better than hand-checking
all ~90 rows.

Labels live in `LABELS` below, keyed by pool index, so the classifier is a
fixed table a later reader can audit row by row. `sub` is `docs`, `local`, or
`-` for vp=0; `priv` marks the vp=0 rows whose reason is that the varying
fact lives only in the asker's own code.

E126 already labelled the same pool `answerable` / `specific` / `program`
from the full post. That is an INDEPENDENT prior classification and is used
as the cross-check, not as input.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
POOL = os.path.join(HERE, "..", "126-stackoverflow-service-test",
                    "screening.jsonl")
GRADED = os.path.join(HERE, "..", "126-stackoverflow-service-test",
                      "grading-results.jsonl")

# idx -> (vp, sub, one-line reason)
LABELS = {
    0: (1, "docs", "macOS Gatekeeper 'will damage your computer' state"),
    1: (1, "docs", "YouTube IFrame API Error 153, referrerPolicy behaviour"),
    16: (1, "docs", "VS Code paste latency, extension/host version"),
    17: (1, "docs", "passlib/bcrypt 72-byte boundary under a host platform"),
    20: (1, "docs", "a VS Code release shows an update-helper prompt"),
    29: (0, "-", "their own Angular source, not a version-varying fact"),
    31: (1, "docs", "Copilot sign-in inside VS 2022, auth flow per build"),
    32: (1, "docs", "Xcode 16.3 gRPC-Core pod template-arg error"),
    35: (1, "docs", "which Claude model VS Code surfaces, per release"),
    36: (1, "docs", "16 KB page-size APK requirement, Android by version"),
    37: (1, "docs", "Tailwind v4 utility-name/spacing change"),
    38: (1, "docs", "Copilot Chat Ollama provider support per VS Code build"),
    43: (1, "docs", "Flutter iOS build after the iOS 26 SDK rollout"),
    48: (1, "docs", "youtube_player_iframe error codes 15/153"),
    53: (0, "priv", "their own injected Google ads snippet"),
    55: (1, "docs", "com.google.android.gms calling package, play-services"),
    60: (1, "docs", "attributionTag manifest requirement by Android API"),
    61: (1, "docs", "Flutter 3.29 upgrade broke Android startup"),
    62: (1, "docs", "iOS 26 UIBarButtonItem tint behaviour"),
    63: (1, "docs", "VS Angular template vs ASP.NET Core project layout"),
    64: (1, "docs", "WindowCompat.enableEdgeToEdge added in androidx.core"),
    65: (1, "local", "macOS/OpenSSL trust store CRL verification state"),
    66: (1, "local", "numpy import broken by the macOS 15.4 upgrade"),
    67: (1, "docs", ".NET 10 SDK BuildHost shortcut behaviour"),
    68: (1, "local", "pip-compile resolution stack trace, own environment"),
    69: (1, "docs", "apns-token-not-set after Flutter Firebase changes"),
    72: (1, "docs", "PEP 695 type alias, Python/PyCharm version"),
    73: (1, "docs", "package-visibility <queries> requirement, Android 11+"),
    74: (1, "docs", "Copilot default model selection setting"),
    75: (1, "docs", "iOS 26 Menu view hierarchy"),
    77: (1, "docs", "Android Studio 2025.2.2 renamed the Android view"),
    83: (1, "docs", "IsNullOrEmpty removed from Microsoft.Identity.Web?"),
    85: (1, "local", "RSelenium driver connection, own R/selenium versions"),
    97: (1, "docs", "RStudio console history, per release"),
    102: (1, "docs", "Android SDK 35 edge-to-edge deprecated APIs"),
    105: (1, "docs", ".NET 10 overload resolution ambiguity"),
    107: (1, "docs", "Android Studio 2025.2.3 branch-switch freeze"),
    112: (1, "docs", "PostgreSQL generic-plan switch, version dependent"),
    135: (1, "docs", "VS Code Data Wrangler DataFrame-name display"),
    136: (1, "docs", "node.js unhandled rejection semantics per major"),
    144: (1, "docs", "copy_n ambiguity differs between GCC 9 and GCC 13"),
    150: (1, "local", "x86 emulation vs native on an M4 host"),
    152: (1, "docs", "GCC concept satisfaction, version dependent"),
    158: (1, "docs", "Liquid Glass icon asset set, macOS 26"),
    160: (1, "docs", "Swing menu padding change, Java 21 to Java 25"),
    161: (1, "docs", "LazyVim Tutor Marks restore, config key per release"),
    165: (1, "docs", ".NET 10 JIT struct-register promotion"),
    167: (1, "docs", "shipping a C++ modules dylib, toolchain specific"),
    171: (1, "local", "compiles under GCC, fails under Clang"),
    172: (1, "docs", "Clang trunk fold+expanded-constraints rejection"),
    174: (1, "local", "NSight Systems finds no CUDA events on their run"),
    184: (1, "docs", "Unicode case folding differs by implementation"),
    187: (1, "local", "Clang accepts, GCC/MSVC reject, C++20 overloads"),
    192: (1, "docs", "compiler divergence on incomplete default argument"),
    196: (1, "docs", "primitive types in patterns, Java 23"),
    209: (1, "docs", "DolphinDB loadTable().to_pandas() transfer semantics"),
    214: (1, "local", "PHP site stopped displaying, nothing changed"),
    225: (1, "docs", "VS 2026 Copilot opening Markdown preview tabs"),
    226: (1, "local", "PHP 8 mail() works from CLI, not via the web server"),
    228: (1, "docs", "Joomla 4 403 on inline JavaScript in a custom module"),
    229: (0, "-", "Boost.Beast async stall, code-level"),
    232: (1, "docs", "IntelliJ code completion in comments, per release"),
    234: (1, "docs", "Nubra historical_data() TimeSeriesPoint shape"),
    237: (1, "docs", "Mac App Store update does not relaunch a menu bar app"),
    244: (1, "docs", "Unity 6000.5.7f1 TMPro font corruption"),
    252: (1, "docs", "NativeWind v5 / Tailwind v4 @theme variables"),
    254: (1, "docs", "Debian 13 hardened image, libarchive apt failure"),
    256: (1, "docs", "Shopify App Bridge 4.x embedded app checks pending"),
    257: (1, "docs", "jpackage + WiX 3.11 candle exit code 14"),
    258: (1, "docs", "Android 15 magnification reset on home screen switch"),
    261: (1, "docs", "Tableau MAKEPOINT on a Geographic Role field"),
    262: (1, "docs", "Google Play alternative-billing policy per version"),
    263: (0, "local", "driver/debug-context state on their machine"),
    264: (1, "docs", "Apache IoTDB LAG offset type-width behaviour"),
    265: (0, "local", "one Samsung device only; environment-specific"),
    267: (1, "docs", "what browsers will accept as a cert in 2026"),
    269: (1, "docs", "Mercado Pago Preapproval API 400, sandbox rules"),
    271: (0, "local", "Zorin 18.1 live CD on a specific Thinkpad"),
    272: (1, "docs", "androidx.compose material icon import path"),
    277: (1, "docs", "SSMS pinned to an old SQL Server version"),
    279: (1, "docs", "PhonePe per-transaction UPI cap for a Flutter app"),
    283: (0, "-", "brms model stalls; code/config level"),
    284: (1, "local", "nf-core duplicate-name, their pinned channel versions"),
    285: (1, "docs", "Propshaft .manifest.json reload behaviour"),
    286: (1, "docs", "Tomcat 10 on Debian 13 with JDK 21"),
    287: (1, "docs", "StoreKit TestFlight vs development-build currency"),
    290: (1, "docs", "React Router 8 @react-router/dev/routes in prod build"),
    293: (1, "docs", "VSIX ProjectTemplate asset indexing in VS 2026"),
    294: (1, "docs", "APS Free 403 AUTH-001 with client_credentials"),
    295: (1, "docs", "Oracle APEX Human Task release action"),
    296: (1, "docs", "MATLAB fitcsvm vs fitcecoc, per release"),
    298: (1, "docs", "Eclipse Only W button, workbench setting"),
}


def wilson(k, n, z=1.96):
    if n == 0:
        return (0.0, 1.0)
    p = k / n
    d = 1 + z * z / n
    c = p + z * z / (2 * n)
    h = z * ((p * (1 - p) / n + z * z / (4 * n * n)) ** 0.5)
    return (max(0.0, (c - h) / d), min(1.0, (c + h) / d))


def main():
    graded = set()
    with open(GRADED) as fh:
        for line in fh:
            graded.add(int(json.loads(line)["question_id"]))

    rows = []
    with open(POOL) as fh:
        for i, line in enumerate(fh):
            r = json.loads(line)
            qid = int(r["question_id"])
            if r.get("dropped"):
                continue
            rows.append({
                "idx": i,
                "qid": qid,
                "views": r.get("view_count", 0),
                "arm": r.get("arm"),
                "tags": r.get("tags", []),
                "title": (r.get("title") or "")[:200],
                "e126_sub": r.get("sub"),
                "e126_shape": r.get("shape"),
                "in_e126_graded40": qid in graded,
                "vp": None,
                "vp_sub": None,
                "reason": None,
            })

    missing = [r["idx"] for r in rows if r["idx"] not in LABELS]
    for r in rows:
        if r["idx"] in LABELS:
            vp, sub, reason = LABELS[r["idx"]]
            r["vp"], r["vp_sub"], r["reason"] = vp, sub, reason

    with open(os.path.join(HERE, "classified.jsonl"), "w") as fh:
        for r in rows:
            fh.write(json.dumps(r) + "\n")

    n = len(rows)
    vp1 = [r for r in rows if r["vp"] == 1]
    sub_docs = [r for r in vp1 if r["vp_sub"] == "docs"]
    sub_local = [r for r in vp1 if r["vp_sub"] == "local"]
    elig = [r for r in rows if not r["in_e126_graded40"]]

    # Cross-check against E126's independent full-post classification.
    e126_spec = {r["idx"] for r in rows if r["e126_sub"] == "specific"}
    mine = {r["idx"] for r in vp1}
    both = len(mine & e126_spec)
    mine_only = sorted(mine - e126_spec)
    e126_only = sorted(e126_spec - mine)

    k, m = len(vp1), n
    lo, hi = wilson(k, m)
    print(json.dumps({
        "pool_rows": n,
        "vp1_count": k,
        "vp1_share": round(k / m, 4),
        "vp1_wilson95": [round(lo, 4), round(hi, 4)],
        "vp1_wilson95_lower_gt_2pct": lo > 0.02,
        "g1_gate": bool(k / m >= 0.05 and lo > 0.02),
        "sub_docs": len(sub_docs),
        "sub_local": len(sub_local),
        "eligible_ungraded_rows": len(elig),
        "crosscheck_vs_e126_specific": {
            "e126_specific": len(e126_spec),
            "mine_vp1": len(mine),
            "intersection": both,
            "jaccard": round(both / len(mine | e126_spec), 4),
            "vp1_not_in_e126_specific": mine_only,
            "e126_specific_i_called_vp0": e126_only,
        },
    }, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())