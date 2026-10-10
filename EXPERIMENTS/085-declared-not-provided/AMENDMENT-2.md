<!-- origin-meta
owner: EXPERIMENTS/085-declared-not-provided/PROTOCOL.md
status: active
last-verified: 2026-10-10
-->

# E085 — Amendment 2 (declared after the corrected control run, before any repository scan)

## What the corrected run showed

With the forward-direction sub-tests, arm C is clean (**0 of 10** false flags)
and **B3 provider recovery is 10 of 10** — resolving every true provider's
wheel yields a module set containing the written module. That half of the tool,
the half deptry does not do, works on all ten controls.

**B1 detection is 2 of 2.** `Crypto` and `bs4` both resolve on PyPI to a real
project that does not provide the module, and both are detected.

Two things went against the amendment as written. Both are reported here
rather than scored around.

## Observation 1 — two arm B rows are not failures at all

| row | PyPI says | verdict |
|---|---|---|
| `serial` | a real project `serial` exists whose wheel **does** provide module `serial` | `pip install serial` then `import serial` **works**. This is a name collision, not a wrong project. |
| `attr` | a real project `attr` exists (version **0.3.2**) whose wheel provides module `attr` | `import attr` works, but you get a 2014-era standalone module instead of `attrs`. A quality problem, not an `ImportError`. |

The instrument caught both correctly. Had these been forced into the
positive-control population they would have scored as detector misses, which
would have been wrong. They are reported as `name-collision` and excluded from
every numerator and denominator. **Declared here, before arm A, so the
exclusion cannot be tuned to arm A's numbers.**

## Observation 2 — `sklearn` and `PIL` are sdist-only, and metadata cannot say whether that is loud or silent

`sklearn` and `PIL` both resolve on PyPI to a real project that publishes **no
wheel**. Whether `pip install` then fails loudly or installs silently depends
on whether the sdist builds and what its `setup.py` does — **which is not in
the metadata.** So this is a third population, and reading it as "loud" would
be an assumption, not a measurement (D082).

**This population is already measured, and the record already has it.** E070's
arm M installed exactly this population — sdist-only shadow names — in fresh
virtualenvs with pip's defaults and observed:

| name | install | why |
|---|---|---|
| `sklearn` | **exit 1** | the project's own `setup.py` exits 1 with "use 'scikit-learn' instead" |
| `beautifulsoup` | **exit 1** | BS3's 2008 `setup.py` raises `SyntaxError` under Python 3 and points at `beautifulsoup4` |
| `color` | **exit 1** | only sdist, discarded as unbuildable (version mismatch) |

**3 of 3 sdist-only shadow names failed loudly**, in the one place this record
actually ran the install. E070's own README records that those controls were
chosen, not sampled, so this is not a rate — it is the answer to "what does
this class do", for n = 3.

## The amendment

The detector's output classes are named, and each arm B row lands in exactly
one. G2 is met when B1, B2, B2b and arm C are all perfect and B3 is at least
8 of 10.

| class | meaning | arm B rows | must |
|---|---|---|---|
| `resolves-wrong-project` | a real PyPI project occupies the name and does **not** provide the module — **the silent class, the target** | `Crypto`, `bs4` | detector fires on **all** (B1) |
| `no-such-project` | no PyPI record; pip refuses loudly, which the user sees immediately | `cv2`, `skimage`, `yaml`, `dateutil` | classified here, **not** as a silent finding (B2) |
| `sdist-only-undecidable` | a real PyPI project with no wheel; loud or silent is not in the metadata | `sklearn`, `PIL` | classified into its own bucket, **not** folded into either of the above (B2b) |
| `name-collision` | the name resolves and does provide the module; installing it works | `serial`, `attr` | reported, excluded from all scoring |

`no-such-project` and `sdist-only-undecidable` are counted separately in the
arm A rate for the same reason: the loud class costs the user one visible
error, and folding it into the silent rate would overstate the target
population by exactly the amount that already works.