"""The refusal: a rate is withheld unless the instrument that produced it holds.

This is the whole proposal. Every number in F118, F121 and F122 was printed
normally by a harness whose own controls were green. The difference between
those runs and a trustworthy one is not more gates -- the gates were the thing
that failed -- it is a harness that reports *what kind of instrument produced
this*, alongside the rate.

`report()` returns the text a caller may print, and `may_report()` is the gate:
false whenever any check is not OK. Callers that want a number regardless can
still have one; they have to ask for it by name, which is the entire difference
between a withheld rate and a printed one.
"""

EXIT_OK = 0
EXIT_USAGE = 1
EXIT_WITHHELD = 3

CLEAN = ("OK", "NO_LABELLED_CORRECT_ITEMS")


def blocking(checks):
    """The checks that withhold the rate, with their reason."""
    out = []
    for check in checks:
        if check.get("verdict") not in CLEAN:
            out.append({"check": check.get("check"), "verdict": check.get("verdict"),
                        "reason": check.get("reason", "")})
    return out


def may_report(checks):
    return not blocking(checks)


def headline(checks, rate=None, label="rate"):
    """The text a harness may print. Withheld, with the reason, when it may not."""
    held = blocking(checks)
    if held:
        lines = ["WITHHELD: %s not reported. %d of %d instrument checks failed."
                 % (label, len(held), len(checks))]
        for h in held:
            lines.append("  - %s: %s -- %s" % (h["check"], h["verdict"], h["reason"]))
        lines.append("Run the checks against your own instrument, or pass --anyway "
                     "to print a number this tool does not stand behind.")
        return "\n".join(lines), EXIT_WITHHELD
    return "%s: %s (all %d instrument checks OK)" % (label, rate, len(checks)), EXIT_OK


def render(checks, rate=None, label="rate", anyway=False):
    """Human-readable report plus the exit code a CLI should return."""
    body = []
    for check in checks:
        body.append("%-26s %-26s %s" % (check.get("check", "?"), check.get("verdict", "?"),
                                        check.get("summary", "")))
        if check.get("verdict") not in CLEAN and check.get("reason"):
            body.append("    %s" % check["reason"])
    text, code = headline(checks, rate, label)
    if anyway and code == EXIT_WITHHELD:
        text = "%s (reported under --anyway; instrument checks failed)" % rate
        code = EXIT_OK
    return "\n".join(body + ["", text]), code