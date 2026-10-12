"""The classification rules E115 measured, separate from the fetcher.

Split out of `harvest.py` at the 300-line cap, by invariant rather than by
size: the regexes and the section splitter are what a reader checks against
M1.md, and they change when a rule's phrasing changes.  `harvest.py` is how
the bytes get here; this is what decides what they mean.

Standard library only.  Declared against EXPERIMENTS/115-applicability-thresholds/PROTOCOL.md.

**Both defect shapes recorded in M1.md live in this file**, deliberately left
in place rather than quietly repaired, because the precision figure (11 of 15
flagged spans hand-read as real) is a statement about *this* extractor:

- `THRESHOLD` anchors on `\\b`, which matches between the comma and the `0` of
  "1,000" and so reports "000 or more employees" (F116's substring class, in
  the exact place the E113 protocol said to guard against it).
- `THRESHOLD` matches "salaries less than employees at the GS-11, step 1" --
  a comparison between two salaries -- because "less than" and "employees" are
  adjacent.

The unit tests in `test_classify.py` pin both, so the numbers in M1.md stay
reproducible if this file is ever changed.
"""

import re

# The extraction rule.  One regex for the shape, one for the counting rule.
# ---------------------------------------------------------------------------

# A threshold is a number immediately governing an applicability verb, inside
# a section whose own heading is a scope paragraph ("Scope and purpose",
# "Applicability", ...).  Requires a word boundary on the number so that
# "1953" does not match "53" and "220" does not match "1200".
THRESHOLD = re.compile(
    r"\b(?:"
    r"(?:fewer|less|more|greater|at\s+least|at\s+most|under|over|exceed(?:s|ing)?)"
    r"\s+than\s+|"
    r"(?:ten|fifteen|twenty|thirty|fifty|one\s+hundred|twenty-five)"
    r"\s+(?:or\s+more|or\s+fewer|or\s+more\s+employees|full-time\s+employees)"
    r"\b|"
    r"\d{1,4}\s+(?:or\s+more|or\s+fewer|or\s+more\s+employees|or\s+more\s+persons)"
    r")\s*"
    r"(?:\(\d+\)\s*)?"
    r"\b(?:employees|persons|workers|participants|members|individuals|"
    r"full-time\s+employees|part-time\s+employees|teachers|children|"
    r"students|residents|beds|families)\b",
    re.IGNORECASE,
)

# Numerator qualifiers: the counting rule is not plain headcount when the rule
# text names a type of person, a role, or a conversion.
NUMERATOR = re.compile(
    r"\b(full-time\s+equivalent|fte\b|full-time\s+part-time\s+employees|"
    r"excluding\s+(?:any\s+)?(?:owner|partners?|self\s+employed)|"
    r"including\s+(?:any\s+)?(?:partners?|owners?|family\s+members)|"
    r"partners?\s+or\s+sole\s+proprietors|"
    r"residents\s+or\s+patients|"
    r"employees\s+on\s+the\s+payroll)\b",
    re.IGNORECASE,
)

# Window qualifiers: a rate over a period is not a rate at a moment.
WINDOW = re.compile(
    r"\b(any\s+time\s+(?:during|in|not\s+more\s+than)|"
    r"(?:preceding|previous|last|past)\s+\d+|"
    r"\d+\s+workweeks?|"
    r"calendar\s+year|fiscal\s+year|"
    r"12\s+months?|three\s+months?|30\s+days?)\b",
    re.IGNORECASE,
)

SCOPE_HEADING = re.compile(
    r"\b(scope|applicability|application|purpose|definitions?)\b", re.IGNORECASE
)

TAG = re.compile(r"<[^>]+>")
ENT = {"&amp;": "&", "&lt;": "<", "&gt;": ">", "&quot;": '"', "&apos;": "'"}
# The eCFR emits numeric character references (`&#xA7;` for the section sign)
# alongside the named ones; leaving them in makes a heading unreadable and a
# heading is half of what decides whether a row is a scope section.
NUMENT = re.compile(r"&#(?:x([0-9A-Fa-f]+)|([0-9]+));")


def _unnumerify(match):
    hexpart, decpart = match.group(1), match.group(2)
    try:
        code = int(hexpart, 16) if hexpart else int(decpart)
        return chr(code)
    except (ValueError, OverflowError):
        return match.group(0)


def totext(xml_bytes):
    s = TAG.sub(" ", xml_bytes.decode("utf-8", "replace"))
    for k, v in ENT.items():
        s = s.replace(k, v)
    s = NUMENT.sub(_unnumerify, s)
    return re.sub(r"\s+", " ", s)


def label(section_text):
    """Return (label, dict).  Never raises, never silently drops.

    `section_text` is the XML of one section, as bytes.
    """
    flat = totext(section_text)
    found = []
    for m in THRESHOLD.finditer(flat):
        start = max(0, m.start() - 220)
        window = flat[start:m.end() + 220]
        num = NUMERATOR.search(window)
        win = WINDOW.search(window)
        found.append(
            {
                "span": m.group(0)[:160],
                "context": window[:440],
                "numerator": num.group(0) if num else None,
                "window": win.group(0) if win else None,
                "divergent": bool(num or win),
            }
        )
    if not found:
        return "unlabelled", {"threshold_spans": []}
    divergent = sum(1 for r in found if r["divergent"])
    lab = "matched" if divergent else "need"
    return lab, {
        "threshold_spans": found,
        "n_threshold_spans": len(found),
        "n_divergent_spans": divergent,
    }

SECTION_SPLIT = re.compile(r'<DIV8\b[^>]*TYPE="SECTION"[^>]*>')
HEAD_TAG = re.compile(r"<HEAD>(.*?)</HEAD>", re.DOTALL | re.IGNORECASE)
CITATION_TAG = re.compile(r'citation&quot;:&quot;([^&]*)&quot;')


def label_part(body):
    """Split one part's XML into its sections and label each one.

    The eCFR part XML nests subparts as DIV6 and sections as DIV8 with
    TYPE="SECTION".  Splitting on DIV8 alone keeps a section's own body with
    its own heading; splitting on HEAD (the first attempt) shredded the part
    header and subpart headers into rows that are not sections at all.
    """
    text = body.decode("utf-8", "replace")
    pieces = SECTION_SPLIT.split(text)
    # pieces[0] is the part header and whatever precedes the first section;
    # it is not a section and is reported separately by the caller.
    out = []
    for chunk in pieces[1:]:
        m = HEAD_TAG.search(chunk)
        heading = totext(m.group(1).encode()) if m else ""
        cite = CITATION_TAG.search(chunk[: chunk.find(">") + 1])
        # A section's body is everything after its own HEAD.
        body_text = (chunk[m.end():] if m else chunk).encode("utf-8", "replace")
        lab, detail = label(body_text)
        rec = {
            "heading": heading[:220],
            "citation": cite.group(1) if cite else None,
            "heading_is_scope": bool(SCOPE_HEADING.search(heading)),
            "label_outcome": lab,
        }
        rec.update(detail)
        out.append(rec)
    return out

