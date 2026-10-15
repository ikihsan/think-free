#!/usr/bin/env python3
"""E141: answer extraction, normalization, and the two equivalence relations.

Split out of recover.py, which passed the 300-line cap. Nothing here knows about
cells, controls or gates; recover.py owns all of that and re-exports these names,
so the audit scripts keep importing one module.

Lineage: `boxed_all` and `normalize` are verbatim from
EXPERIMENTS/136-leaderboard-free-text-aggregate/recompute_math.py, which
reproduced 437/437 per-instance verdicts and the published macro to full printed
precision on P1. `extract_gold_number` and `extract_pred_number` are verbatim
from EXPERIMENTS/136-leaderboard-free-text-aggregate/recompute_gsm.py (E138).
`rational_value` and `float_value` are new in E141.
"""
import re
from fractions import Fraction

TOLERANCE = 1e-9

NUM_RE = re.compile(r"[+-]?(?:\d+(?:,\d{3})*(?:\.\d+)?|\.\d+)")
NUM_CAP = r"(" + NUM_RE.pattern + r")"
THOUSANDS = re.compile(r"(?<![\d.,])(\d{1,3}(?:,\d{3})+)(?![\d,])")


# ---------------------------------------------------------------- extraction

def boxed_all(text):
    """All \\boxed{...} contents, balanced-brace aware, in order.

    Verbatim from E136's recompute_math.py.
    """
    out = []
    i = 0
    while text and i < len(text):
        j = text.find("\\boxed{", i)
        if j < 0:
            break
        k = j + len("\\boxed{")
        depth = 1
        start = k
        while depth > 0 and k < len(text):
            if text[k] == "{":
                depth += 1
            elif text[k] == "}":
                depth -= 1
            k += 1
        out.append(text[start:k - 1])
        i = k
    return out


def normalize(s):
    """E136's calibrated normalization, verbatim. No sympy on this VM.

    The brace-less-\\frac repair is load-bearing: without it `\\frac14` and
    `\\frac{1}{4}` normalize differently, which is what G0a caught on the first
    run of E141.
    """
    s = s.strip()
    s = s.replace("\\dfrac", "\\frac").replace("\\tfrac", "\\frac")
    s = s.replace("\\cfrac", "\\frac")
    s = s.replace("\\left", "").replace("\\right", "")
    s = re.sub(r"\\[,;! ]", "", s)
    s = s.replace("~", "").replace("$", "")
    s = re.sub(r"\\(?:mbox|text)\{([^{}]*)\}", r"\1", s)
    s = s.replace("^{\\circ}", "").replace("^\\circ", "")
    s = s.replace("\\circ", "").replace("\\degree", "")
    s = s.replace("\\%", "").replace("%", "")
    s = s.replace("\\infty", "inf").replace("infinity", "inf")
    s = s.replace("\\cdot", "*").replace("\\times", "*")
    s = re.sub(r"\\frac([0-9A-Za-z])([0-9A-Za-z])", r"\\frac{\1}{\2}", s)

    def frac_sub(m):
        return "((" + m.group(1) + ")/(" + m.group(2) + "))"
    prev = None
    while prev != s:
        prev = s
        s = re.sub(r"\\frac\{([^{}]*)\}\{([^{}]*)\}", frac_sub, s)

    def sqrt_sub(m):
        if m.group(1):
            return "(( " + m.group(2) + " )**(1/(" + m.group(1) + ")))"
        return "sqrt(" + m.group(2) + ")"
    prev = None
    while prev != s:
        prev = s
        s = re.sub(r"\\sqrt(?:\[([^{}]*)\])?\{([^{}]*)\}", sqrt_sub, s)

    s = re.sub(r"\\begin\{[a-zA-Z*]+\}", "", s)
    s = re.sub(r"\\end\{[a-zA-Z*]+\}", "", s)
    s = s.replace("\\\\", "&")
    s = s.replace("\\", "")
    s = s.replace("^", "**")
    s = s.replace("{,}", ",")
    s = re.sub(r"\s+", "", s)
    s = s.strip().rstrip(".").rstrip(",")
    if s.endswith("."):
        s = s[:-1]
    return s


def extract_gold_number(text):
    """GSM gold: 'The answer is N', then 'Answer: N', then the last number."""
    if not text:
        return None
    for pat in (r"[Tt]he answer is\s+" + NUM_CAP,
                r"[Aa]nswer:\s*" + NUM_CAP):
        m = re.search(pat, text)
        if m:
            return m.group(1).replace(",", "")
    found = list(re.finditer(NUM_CAP, text))
    return found[-1].group(1).replace(",", "") if found else None


def extract_pred_number(text):
    """GSM prediction: the last '#### N', else the last number in the text."""
    if not text:
        return None
    found = list(re.finditer(r"####\s*" + NUM_CAP, text))
    if not found:
        found = list(re.finditer(NUM_CAP, text))
    return found[-1].group(1).replace(",", "") if found else None


# ------------------------------------------------------- the rational reader

# `\*\*` is tried before the single-character class on purpose. With the order
# reversed, `2**3` tokenizes as `2 * * 3` and the parser refuses it as an
# operator with no operand -- conservative rather than wrong, but it silently
# costs recall on every answer containing a power. Fails if this moves.
TOKEN = re.compile(r"(\d+(?:\.\d+)?|\.\d+|\*\*|[+\-*/()])")


class _Refused(Exception):
    """The string is not in the grammar, so no equality can be proven from it."""


def _parse_expr(toks, i):
    value, i = _parse_term(toks, i)
    while i < len(toks) and toks[i] in ("+", "-"):
        op = toks[i]
        rhs, i = _parse_term(toks, i + 1)
        value = value + rhs if op == "+" else value - rhs
    return value, i


def _parse_term(toks, i):
    value, i = _parse_factor(toks, i)
    while i < len(toks) and toks[i] in ("*", "/"):
        op = toks[i]
        rhs, i = _parse_factor(toks, i + 1)
        if op == "/":
            if rhs == 0:
                raise _Refused("division by zero")
            value = value / rhs
        else:
            value = value * rhs
    return value, i


def _parse_factor(toks, i):
    base, i = _parse_unary(toks, i)
    if i < len(toks) and toks[i] == "**":
        exponent, i = _parse_factor(toks, i + 1)     # right-associative
        if not isinstance(exponent, Fraction) or exponent.denominator != 1:
            raise _Refused("non-integer exponent")
        if abs(exponent.numerator) > 64:
            raise _Refused("exponent too large to be exact")
        base = base ** exponent.numerator
    return base, i


def _parse_unary(toks, i):
    if i < len(toks) and toks[i] in ("+", "-"):
        op = toks[i]
        value, i = _parse_unary(toks, i + 1)
        return (-value if op == "-" else value), i
    return _parse_atom(toks, i)


def _parse_atom(toks, i):
    if i >= len(toks):
        raise _Refused("unexpected end")
    tok = toks[i]
    if tok == "(":
        value, i = _parse_expr(toks, i + 1)
        if i >= len(toks) or toks[i] != ")":
            raise _Refused("unbalanced parenthesis")
        return value, i + 1
    if tok in ("+", "-", "*", "/", "**"):
        raise _Refused("operator with no operand")
    if tok[0].isdigit() or tok[0] == ".":
        return Fraction(tok), i + 1
    raise _Refused("not in the grammar: %r" % tok)


def rational_value(s):
    """Exact rational value of a normalized answer, or None if unprovable.

    A recursive-descent reader over a deliberately narrow grammar: decimal and
    integer literals, + - * /, parentheses, integer exponentiation, and a unary
    sign. Nothing is `eval`'d, so no string can smuggle in a name or a call.
    Variables, roots, `&`, letters, `sqrt`, `inf` and juxtaposition (`5(3)`) are
    all outside the grammar, and an out-of-grammar string makes the row
    unrecoverable rather than equal -- so the recovery count is a lower bound on
    what a real equivalence relation could recover, which is the safe direction
    for a claim that under-crediting is material.

    A comma is removed only where it is a thousands separator (`1,000`), never
    between one-to-three digit groups (`(3,4)` stays a tuple and is refused),
    because `1,2` is ambiguous and guessing would be a false positive.
    """
    if not s:
        return None
    s = THOUSANDS.sub(lambda m: m.group(1).replace(",", ""), s)
    toks = TOKEN.findall(s)
    if "".join(toks) != s:
        return None
    try:
        value, i = _parse_expr(toks, 0)
    except (_Refused, ZeroDivisionError, ValueError, OverflowError):
        return None
    if i != len(toks) or not isinstance(value, Fraction):
        return None
    return value


def float_value(s):
    """Float value for the T2 tier only, or None if unprovable.

    Derived from `rational_value` rather than from an `eval`, so the tolerance
    tier is judged on exactly the expressions the exact tier reads. It is
    therefore no more permissive than T1's grammar, only more forgiving about
    agreement; the tier exists to expose near-misses (0.333 against 1/3), not to
    widen what counts as an answer.
    """
    v = rational_value(s)
    return None if v is None else float(v)


# ------------------------------------------------------------------- relations

def norm_eq(a, b):
    """E136's reproduction of the harness's own rule."""
    if a is None or b is None:
        return False
    return normalize(a) == normalize(b)


def eq_t1(a, b):
    """norm_eq, or exact rational equality. Returns (bool, reason)."""
    if a is None or b is None:
        return False, "no_answer"
    na, nb = normalize(a), normalize(b)
    if na == nb:
        return True, "norm_eq"
    ra, rb = rational_value(na), rational_value(nb)
    if ra is not None and rb is not None and ra == rb:
        return True, "rational_equal"
    return False, "not_equal"


def eq_t2(a, b):
    """Float agreement within TOLERANCE, and not already eq_t1."""
    if a is None or b is None:
        return False
    ok, _ = eq_t1(a, b)
    if ok:
        return False
    fa, fb = float_value(normalize(a)), float_value(normalize(b))
    if fa is None or fb is None:
        return False
    scale = max(abs(fa), abs(fb), 1.0)
    return abs(fa - fb) <= TOLERANCE * scale