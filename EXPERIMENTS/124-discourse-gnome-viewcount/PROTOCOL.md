# E124 — Fresh observation: discourse.gnome.org (GNOME Developer Forum)

<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-12
-->

## Summary

Fresh observation in a new domain per D083: **discourse.gnome.org** — the GNOME project's Discourse forum for desktop, GTK, libadwaita, Flatpak, and platform development.

**G1 PASS, G2 FAIL** — Classifier coverage 37.2% (< 60% floor). Domain CLOSED per kill gate.

## Results

| Metric | Value | Gate |
|---|---|---|
| Total topics | 500 | — |
| View_count > 0 | 100% | G1 PASS |
| Classifier coverage | 37.2% | **G2 FAIL** (< 60%) |
| Need-related | 133 (26.6%) | — |
| Random | 53 (10.6%) | — |
| Unclassified | 314 (62.8%) | — |

## Critical Finding: Question Style Mismatch

The improved classifier (with blog/announcement exclusion patterns) achieves only 37.2% coverage on discourse.gnome.org, compared to 87.6% on meta.discourse.org (E123).

**Root cause**: GNOME forum topics use different question styles not captured by standard Q&A patterns:

| Style | Example Topics (unclassified) | Missing Pattern |
|---|---|---|
| Noun phrase questions | "Google Drive in GNOME 50", "Useful documentation for GTK" | — |
| Abbreviated how-to | "How Install Gtk 4.X on Raspberry Pi OS", "Install on mobile" | `how install`, `install on` |
| Technical feature requests | "Add a setting to change trackpad scroll speed", "Way to remove widgets" | — |
| Error messages as titles | "'LooseVersion' object has no attribute 'version'" | Error message patterns |
| Noun phrase + ? | "Gtk4 - Blueprint as default .ui format?" | — |

The classifier patterns (designed for Q&A support forums) assume standard question forms ("how to", "why does", "what is", "error", "fix", etc.). Developer/design forums use abbreviated, noun-phrase, and error-message styles.

## Classifier Improvement Test

The E124 improved classifier (`classifier_gnome.py`) adds:
- Blog/announcement exclusion patterns (from E123 finding)
- Genuine "getting started" question patterns
- Test accuracy: 86.7% on meta.discourse.org blog post test cases

But these improvements **don't address the fundamental style mismatch** on developer forums.

## Conclusion

**The 60% coverage floor is a domain-dependent boundary condition.** The E119/E123 classifier works on Q&A-style support forums (meta.discourse.org, E077 non-software Discourse, E082 embedded Discourse) but FAILS on developer/design forums (GNOME 37.2%, Jupyter 50.4%).

Per D083, this domain is closed for candidate generation. Further Discourse experiments require either:
1. A developer-forum-specific classifier with patterns for error-message titles, noun-phrase questions, informal problem statements
2. Restriction to Q&A-style support forums where the current classifier works

## Reproduction

```bash
cd EXPERIMENTS/124-discourse-gnome-viewcount
python3 fetch_gnome.py           # Fetch data (done)
python3 measure_gnome.py data_gnome.jsonl  # Measure gates
python3 analyze_coverage.py      # Analyze coverage gap
```