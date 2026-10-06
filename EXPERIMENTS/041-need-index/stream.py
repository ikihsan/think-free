#!/usr/bin/env python3
"""E041 streaming instrument: E040's arithmetic, one document in memory at a time.

E040's `gates.vectors()` materialises every document's vector before returning.
For the U2 text unit over 44,669 GitHub issues that is ~1.95M term entries held
as dicts at once, and on this host — 952 MiB of RAM, 2 CPUs, Python 3.8.10, no
NumPy — the peak pushes the process into swap. Measured directly: three runs of
`tally.py` reached U1 in 7-15 seconds and then spent **33+ minutes of wall clock
on 3.5 minutes of CPU**, in `D (disk sleep)`, never finishing U2.

`stream_vectors()` computes the *same numbers* in two passes, so peak memory is
the inverted index plus one document:

  pass 1  document frequency for every term, which is all `idf` needs
  pass 2  each document's vector, emitted into the index and then dropped

The equivalence is not asserted on faith. `selftest.py` rebuilds a sample with
E040's own `vectors()` and requires every cosine to match to 1e-9, and
`tally.py` runs that check on 200 documents before it trusts the streaming path
for the corpus. F014's rule applies: a faster instrument is not the same
instrument until the fast one is shown to agree with the slow one.
"""
import array
import math
import os
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
E040DIR = os.path.join(os.path.dirname(HERE), "040-need-clustering")
sys.path.insert(0, E040DIR)

from gates import tokens as _tokens      # noqa: E402
from gates import vectors as _vectors    # noqa: E402
from gates import BIGRAM_WEIGHT          # noqa: E402

tokens = _tokens


def _vector_from(toks, df, n):
    """E040's vector for one document: unigrams at count, bigrams at 0.5."""
    v = {}
    for w, c in Counter(toks).items():
        v[w] = (1.0 + math.log(c)) * math.log(n / df[w])
    for a, b in zip(toks, toks[1:]):
        g = a + "_" + b
        v[g] = v.get(g, 0.0) + BIGRAM_WEIGHT * math.log(n / df.get(g, 1))
    norm = math.sqrt(sum(x * x for x in v.values())) or 1.0
    return {k: x / norm for k, x in v.items()}


def stream_vectors(texts, keep_indices):
    """Return (postings_idx, postings_wts, kept_vectors) for a text sequence.

    `kept_vectors` holds only the rows named in `keep_indices`, which is how the
    caller keeps the 77 vectors it still needs while the other 44,592 are dropped
    as they are indexed.
    """
    toks = [_tokens(t) for t in texts]
    n = len(toks) or 1
    df = Counter()
    for t in toks:
        df.update(set(t))
    idx, wts = {}, {}
    keep = {}
    kis = set(keep_indices)
    for i, t in enumerate(toks):
        v = _vector_from(t, df, n)
        if i in kis:
            keep[i] = v
        _emit(idx, wts, i, v)
        toks[i] = None
    return idx, wts, keep


def stream_iter(text_iter_factory, keep_indices):
    """As `stream_vectors`, for a re-iterable stream of texts.

    The token list is never held: pass one counts document frequency, and pass
    two walks the source a second time. The caller's text source therefore never
    needs to be a list, so the corpus is not resident twice.

    `text_iter_factory` is a **callable returning a fresh iterator**, not an
    iterator: two passes need two. Passing a generator raises `TypeError` here,
    which is loud; passing a *list* works but defeats the memory purpose, so the
    caller is responsible and the emptiness is checked downstream.
    """
    df = Counter()
    n = 0
    for t in text_iter_factory():
        n += 1
        df.update(set(_tokens(t)))
    n = n or 1
    idx, wts = {}, {}
    keep = {}
    kis = set(keep_indices)
    for i, t in enumerate(text_iter_factory()):
        v = _vector_from(_tokens(t), df, n)
        if i in kis:
            keep[i] = v
        _emit(idx, wts, i, v)
    return idx, wts, keep


def _emit(idx, wts, i, v):
    for term, w in v.items():
        if term in idx:
            idx[term].append(i)
            wts[term].append(w)
        else:
            idx[term] = array.array("i", [i])
            wts[term] = array.array("d", [w])


def score_row(idx, wts, vi, i):
    """Cosine of row i against every other row, via the inverted index."""
    acc = {}
    for term, w in vi.items():
        js = idx.get(term)
        if not js:
            continue
        ws = wts[term]
        for k in range(len(js)):
            j = js[k]
            if j != i:
                acc[j] = acc.get(j, 0.0) + w * ws[k]
    return acc


def dense_row(vecs, i):
    """The same cosine computed the slow, obvious way, for the equivalence check."""
    acc = {}
    vi = vecs[i]
    for j, vj in enumerate(vecs):
        if i == j:
            continue
        a, b = (vi, vj) if len(vi) <= len(vj) else (vj, vi)
        s = 0.0
        for k, x in a.items():
            y = b.get(k)
            if y is not None:
                s += x * y
        acc[j] = s
    return acc


def check_equivalent(texts, n_check=200, tol=1e-9):
    """Streaming vs E040's `vectors()`: every cosine must agree to `tol`.

    Returns (ok, worst_absolute_difference, n_pairs_compared).
    """
    if len(texts) < n_check:
        n_check = len(texts)
    sample = texts[:n_check]
    ref = _vectors(sample)
    idx, wts, _keep = stream_vectors(sample, range(len(sample)))
    worst = 0.0
    compared = 0
    for i in range(len(sample)):
        # the streaming path does not keep every vector, so rebuild this row's
        # postings contribution directly from the index for the comparison
        vi = {}
        for term in ref[i]:
            js = idx.get(term)
            if js is not None and i in js:
                k = list(js).index(i)
                vi[term] = wts[term][k]
        fast = score_row(idx, wts, vi, i)
        slow = dense_row(ref, i)
        for j, s in slow.items():
            compared += 1
            worst = max(worst, abs(fast.get(j, 0.0) - s))
    return worst <= tol, worst, compared
