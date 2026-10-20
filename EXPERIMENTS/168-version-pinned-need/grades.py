#!/usr/bin/env python3
"""E168 step 5: grade the 24 unaided attempts against their threads.

Rubric, inherited verbatim from E126: `served` means the attempt names the
thread's resolution, or names the correct fault with a resolution that would
fix the same thing. One reader, as in every prior run of this instrument.

The baseline this is compared against is E126's own 27/40 = 0.675 on the
same pool with the same instrument. It is NOT re-measured here: E126's 40
graded rows include 20 that overlap this pool, and re-reading them would
mean reading threads after writing this run's attempts, which breaks this
run's blinding. The comparison is therefore across-run and is declared
approximate for that reason.

`grade` values are `served` / `unserved`. `near_miss` marks a grade the
reader would defend the other way.
"""
import json
import os
import sys
from math import sqrt

HERE = os.path.dirname(os.path.abspath(__file__))

# idx -> (verdict, near_miss, reason)
GRADES = {
    0:  ("served", False,
         "Attempt names the fault class (Gatekeeper cannot validate the app's "
         "signature) and one of its two remedies - reinstall from Docker's "
         "signed download - is the thread's resolution. The specific cause "
         "the thread's lowest-scored answer gives (Docker revoked its own "
         "signing certificate) is not named, and the xattr half of the "
         "attempt is not in the thread."),
    1:  ("unserved", False,
         "Thread resolution is the Referrer-Policy response header, with "
         "Cloudflare overwriting it as a follow-on; the asker had already "
         "tried the attribute form. Attempt's remedy is the `origin` query "
         "parameter, which the thread does not mention."),
    16: ("unserved", False,
         "Thread resolution is a single undocumented setting, "
         "typescript.updateImportsOnPaste.enabled=false. Attempt names "
         "extensions, formatOnPaste, the WSL clipboard bridge and the "
         "file watcher - none of which is the cause."),
    17: ("served", False,
         "Thread resolution is pinning bcrypt to 4.3.0 because bcrypt 5.0.0 "
         "broke passlib. Attempt names the passlib/bcrypt version "
         "incompatibility and recommends pinning the bcrypt version; the "
         "specific version number is absent but the fault and the remedy "
         "class match."),
    20: ("unserved", False,
         "Thread resolution is chown-ing the ShipIt cache and clearing the "
         "quarantine attribute on the app. Attempt attributes the loop to "
         "the logged network failure and recommends manual updates, which "
         "is a different fault."),
    31: ("unserved", False,
         "Thread resolution is setting the correct active Visual Studio "
         "account. Attempt covers extension version, credential store, clock "
         "and proxy - none of them the cause."),
    32: ("unserved", False,
         "Thread resolution is a source edit: passing explicit template "
         "arguments, Traits::template CallSeqFactory<>(...). Attempt calls "
         "it a clang regression and recommends downgrading Xcode or raising "
         "the pods."),
    35: ("served", False,
         "Thread resolution is that Copilot does not yet support Claude 4 "
         "with stand-alone API keys; use a Copilot account or wait. Attempt "
         "concludes with exactly that condition after its update advice."),
    36: ("served", True,
         "Thread gives a tool-side cause (an Android Studio bug with "
         "compressed libraries, fixed in 2025.1.3 Canary 2) plus zipalign. "
         "Attempt's cause is packaging configuration, but its remedy "
         "(uncompressed native libs, zipalign to 16 KB) is the remedy half "
         "of the thread's answer and would plausibly clear it. Graded served "
         "on the remedy; a fault-only reader would grade unserved."),
    37: ("served", False,
         "Thread resolution is wrapping the universal reset in @layer base "
         "so Tailwind v4 utilities outrank it. Attempt states that, and the "
         "v4 cascade change."),
    38: ("unserved", False,
         "Thread resolution is that a model must support tool calling to "
         "appear in the Chat picker. Attempt explains the picker as a "
         "different list with a per-provider default, which would not fix "
         "it."),
    43: ("unserved", False,
         "Thread resolutions are Rosetta on Apple Silicon and an Excluded "
         "Architectures misconfiguration. Attempt attributes it to a stale "
         "destination id and device cleanup, which is not either."),
    48: ("served", False,
         "Thread resolution is passing an https origin to "
         "YoutubePlayerParams. Attempt says the WebView's origin is not an "
         "https origin and that it must be supplied, which is the same fix "
         "arrived at from the wrong direction."),
    55: ("unserved", False,
         "Thread answer is that there is an open issue and no fix. Attempt "
         "supplies a Play services version-mismatch story and an upgrade "
         "path, which the thread does not support."),
    60: ("unserved", True,
         "Thread resolution is declaring <attribution android:tag=...> in "
         "the manifest and building an attribution context. Attempt tells "
         "the reader to declare a tag in the manifest - right shape, wrong "
         "element (PROPERTY_ATTRIBUTION_TAG, not <attribution>) - and also "
         "hedges that it is probably another app's log line, which the thread "
         "contradicts. Graded unserved; a lenient reader could call it "
         "served."),
    61: ("served", False,
         "Thread resolution is that flutter_barcode_scanner is not "
         "maintained and needs a fork for Flutter 3.29. Attempt names the "
         "removed v1 embedding API (PluginRegistry.Registrar) and the two "
         "options: upgrade the package or pin Flutter back."),
    62: ("unserved", False,
         "Thread resolution is withTintColor(...) combined with "
         ".withRenderingMode(.alwaysOriginal) on the image. Attempt "
         "recommends explicit per-view tint or UIHostingConfiguration, which "
         "is a different mechanism."),
    63: ("served", False,
         "Thread resolution is the Angular 20 filename convention change "
         "(app.component.ts no longer generated), fixed in VS 2026. Attempt "
         "states that rename. Its first claim, that the telemetry prompt "
         "aborts generation, is wrong but additive."),
    64: ("served", False,
         "Thread resolution is depending on androidx.core:core 1.17.0-beta01 "
         "explicitly. Attempt says the docs are for a newer core than the "
         "one resolved and to raise the dependency - same fault, same "
         "remedy, without the beta coordinate."),
    65: ("unserved", False,
         "Thread resolutions are adding the openssl gem, or moving to Ruby "
         "3.4.7 built against OpenSSL 3.5.4, because Ruby's bundled OpenSSL "
         "extension is incompatible with OpenSSL 3.6.0. Attempt blames a "
         "CRL_CHECK verify flag and recommends changing verification."),
    66: ("served", True,
         "Thread resolutions are a conda-forge library-path fix script and "
         "`conda update --all` after the macOS 15.4 upgrade. Attempt "
         "recommends reinstalling numpy through conda, which is the same "
         "channel-level remedy without the specific lib-path fault. Graded "
         "served on remedy class."),
    67: ("unserved", False,
         "Thread resolutions are that the folders come from the "
         "EntityFrameworkCore.Design NuGet package and disappear on upgrade "
         "to 10.0.2+. Attempt attributes them to MSBuild node reuse, which "
         "is a different origin."),
    68: ("served", False,
         "Thread resolution is pip install -U 'pip<25.3'. Attempt names "
         "exactly that incompatibility and the two ways out: pin pip or "
         "upgrade pip-tools."),
    69: ("unserved", True,
         "Thread resolution is that simulator push notifications are a "
         "long-standing iOS limitation - use a real device and wait. Attempt "
         "recommends capability and entitlement configuration and attributes "
         "the missing token to a simulator without a signed-in Apple ID. "
         "Close to the thread's cause, wrong remedy. Graded unserved."),
}


def wilson(k, n, z=1.96):
    if n == 0:
        return (0.0, 1.0)
    p = k / n
    d = 1 + z * z / n
    c = p + z * z / (2 * n)
    h = z * sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return (max(0.0, (c - h) / d), min(1.0, (c + h) / d))


def fisher_right(a, b, c, d):
    """Two-sided Fisher exact p for table [[a,b],[c,d]]."""
    from math import comb
    n = a + b + c + d
    r1, c1 = a + b, a + c

    def p_of(x):
        return (comb(r1, x) * comb(n - r1, c1 - x) / comb(n, c1))
    obs = p_of(a)
    lo, hi = max(0, c1 - (n - r1)), min(r1, c1)
    return sum(p_of(x) for x in range(lo, hi + 1)
               if p_of(x) <= obs * (1 + 1e-9))


def main():
    rows = {r["idx"]: r for r in
            (json.loads(l) for l in
             open(os.path.join(HERE, "classified.jsonl")))}
    sampled = [i for i in GRADES]
    for i in sampled:
        assert i in rows and rows[i]["vp"] == 1, "bad sample row %s" % i

    served = [i for i in sampled if GRADES[i][0] == "served"]
    unserved = [i for i in sampled if GRADES[i][0] == "unserved"]
    near = [i for i in sampled if GRADES[i][1]]
    k, n = len(served), len(sampled)
    lo, hi = wilson(k, n)

    # E126's same-instrument baseline on the same pool.
    b_k, b_n = 27, 40
    b_lo, b_hi = wilson(b_k, b_n)

    out = []
    for i in sorted(sampled):
        v, nm, why = GRADES[i]
        out.append({"idx": i, "verdict": v, "near_miss": nm,
                    "reason": why, "vp_sub": rows[i]["vp_sub"],
                    "e126_sub": rows[i]["e126_sub"],
                    "views": rows[i]["views"]})
    with open(os.path.join(HERE, "grades-unaided.jsonl"), "w") as fh:
        for r in out:
            fh.write(json.dumps(r) + "\n")

    p = fisher_right(k, n - k, b_k, b_n - b_k)
    print(json.dumps({
        "unaided_n": n,
        "unaided_served": k,
        "unaided_served_share": round(k / n, 4),
        "unaided_wilson95": [round(lo, 4), round(hi, 4)],
        "baseline_e126_served_share": round(b_k / b_n, 4),
        "baseline_wilson95": [round(b_lo, 4), round(b_hi, 4)],
        "difference": round(k / n - b_k / b_n, 4),
        "fisher_two_sided_p": round(p, 4),
        "g2_condition_a_served_le_0_50": bool(k / n <= 0.50),
        "g2_condition_b_gap_ge_0_20": bool(b_k / b_n - k / n >= 0.20),
        "g2_gate": bool(k / n <= 0.50 and b_k / b_n - k / n >= 0.20),
        "near_miss_rows": sorted(near),
        "near_miss_effect": {
            "all_near_miss_served": round(
                (k + len([i for i in near if GRADES[i][0] == "served"])) / n,
                4),
            "all_near_miss_unserved": round(
                (k - len([i for i in near if GRADES[i][0] == "served"])) / n,
                4),
        },
        "unserved_rows": sorted(unserved),
    }, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())