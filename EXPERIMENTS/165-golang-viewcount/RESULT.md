<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-15
-->

# E165: Go Module Ecosystem (pkg.go.dev) View-Count Principle Test — RESULT

## Summary
**ALL GATES FAIL** (G1, G2, G3 fail; G4 passes)

The view-count principle does **not** generalize to the Go module ecosystem (pkg.go.dev) with the current classifier vocabulary. Two distinct issues were found:

1. **G1 FAIL (Classifier vocabulary mismatch)**: Only 19 packages classified as "general" vs 150 as "need-related" (threshold: 30 per class). The pre-declared keyword rules are mismatched for Go module naming conventions.

2. **G2 FAIL (Weak effect size)**: Cliff's delta = 0.0744 < 0.147 threshold. Even with the flawed classification, the effect size is small.

3. **G3 FAIL (No differential activity)**: Both classes show 100% arrival rate (all packages have imported_by > 0).

4. **G4 PASS**: "Imported by" metadata is universally present (100% coverage).

## Detailed Results

### Harvest
- **225 unique packages** harvested from 13 search queries
- All 225 packages have "Imported by" counts (range: 29 – 2,032,418; median: 4,185)
- Metadata coverage: 100% (G4 PASS)

### Classification Breakdown
| Class | Count | Threshold | Status |
|-------|-------|-----------|--------|
| Need-related | 150 | ≥30 | PASS |
| General | 19 | ≥30 | **FAIL** |
| Unclassified | 56 | — | — |

### Gate Verdicts
| Gate | Metric | Value | Threshold | Verdict |
|------|--------|-------|-----------|---------|
| G1 | Need-related count | 150 | ≥30 | PASS |
| G1 | General count | 19 | ≥30 | **FAIL** |
| G2 | Cliff's delta | 0.0744 | ≥0.147 | **FAIL** |
| G3 | Need arrival rate | 100% | ≥80% | PASS (but...) |
| G3 | General arrival rate | 100% | <80% | **FAIL** (no differential) |
| G4 | Metadata coverage | 100% | ≥95% | PASS |

### Statistics
- **Need-related**: median=3,705, mean=39,313
- **General**: median=3,003, mean=15,311
- **Mann-Whitney U**: Not computed (G2 failed on primary metric)

## Classifier Vocabulary Analysis

The pre-declared keyword rules produced systematic misclassifications:

### Over-classification as "need-related" (false positives)
| Keyword | Problematic matches (primary/original packages) |
|---------|-------------------------------------------------|
| `client` | `github.com/aws/aws-sdk-go`, `go.mongodb.org/mongo-driver`, `github.com/docker/docker/client`, `k8s.io/client-go` — all PRIMARY SDKs/clients |
| `driver` | `database/sql/driver` (stdlib interface), `github.com/go-sql-driver/mysql` (primary MySQL driver), `github.com/lib/pq` (primary Postgres driver) |
| `wrapper` | `golang.org/x/text/transform` (stdlib), `go.uber.org/zap/buffer` (internal wrapper), `github.com/kr/pty` (wrapper for another lib but primary in its niche) |
| `middleware` | `github.com/gin-contrib/cors`, `github.com/go-chi/chi/v5/middleware`, `github.com/labstack/echo/v4/middleware` — PRIMARY framework middleware |
| `plugin` | `plugin` (stdlib), `github.com/hashicorp/go-plugin` (primary plugin system) |
| `v2`/`v3` path | `github.com/labstack/echo/v4`, `github.com/gofiber/fiber/v3`, `github.com/urfave/cli/v3` — legitimate major versions of PRIMARY frameworks |

### Under-classification as "general" (false negatives)
The general keyword list only included specific known primary framework names (gin, echo, fiber, beego, iris, revel, chi, gorilla, httprouter). It missed:
- Standard library packages (`net/http`, `context`, `path`, `io/ioutil`, `image`, etc.)
- Kubernetes ecosystem (`k8s.io/`, `sigs.k8s.io/`) — primary infrastructure
- Prometheus ecosystem (`github.com/prometheus/`)
- Uber Go libraries (`go.uber.org/`)
- HashiCorp libraries (`github.com/hashicorp/`)
- Google Go libraries (`google.golang.org/`, `golang.org/x/`)
- Many other primary/original packages

### Unclassified packages (56)
Many legitimate primary packages fell through both keyword sets: `github.com/sirupsen/logrus`, `github.com/rs/zerolog`, `github.com/stretchr/testify`, `google.golang.org/grpc/metadata`, `github.com/prometheus/common/model`, stdlib packages (`image`, `image/color`, `net/http/pprof`, `runtime/pprof`), etc.

## Comparison with Prior Experiments

This mirrors the **classifier vocabulary mismatch** observed in:
- **E146 (crates.io)**: Default listing crates lack need-indicator terms in names/descriptions
- **E157/E162/E163 (GitLab)**: GitHub-designed keywords produce only 22-25% need-related classification (below G1 threshold)
- **E164 (View-count prototype)**: Platform-adapted vocabularies needed; GitHub-designed classifier produced 23.3% need-related on GitLab

The view-count principle's underlying mechanism (differential activity for need-related content) may still exist on pkg.go.dev, but **the classifier must be platform-adapted** to test it properly.

## Kill Gate Fired
**G1 FAIL on general class count** — the classifier vocabulary is mismatched for Go modules. Per protocol: "If G1 FAILS (insufficient classification rate) → stop, principle not testable on this platform with current vocabulary."

## Conclusion
The view-count principle test on pkg.go.dev is **inconclusive due to classifier vocabulary mismatch**, not due to absence of the principle's mechanism. The "Imported by" metadata is universally available (G4 PASS) and shows wide dynamic range, but the pre-declared Go-agnostic keyword rules cannot distinguish need-related from general packages in the Go ecosystem.

**Named next action**: If pursuing Go modules further, develop a Go-adapted classifier vocabulary (e.g., using suffix patterns like `*-adapter`, `*-wrapper`, `*-middleware` in module path; excluding stdlib and known primary prefixes) and re-run. However, per standing constraints, the mission returns to fresh observation in a new untouched domain rather than iterating on classifier adaptation.

## Files
- `raw_harvest.json` — 225 packages with path, synopsis, imported_by, query
- `classified.json` — same with classification labels
- `gate_results.json` — gate verdicts and statistics
- `PROTOCOL.md` — pre-declared protocol
- `harvest.py`, `classify.py`, `measure.py`, `run.py` — experiment code