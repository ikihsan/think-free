<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-15
-->

# Think Free — View-Count Principle Investigation Summary

============================================================

## Mission Status: View-Count Principle Investigation

The view-count principle has been extensively tested across 15+ domains. The principle
posits that on platforms with per-request metadata (view_count/download_count/star_count),
need-related content has systematic activity advantages (higher counts) compared to random content.

### Domains Where the Principle WORKS (all gates pass):
- **PyPI** (E071): need-related packages more active (82.93% vs 57.50%)
- **NPM** (E072): supported (82.93% vs 57.50% analog, 100% need-related active vs 0% random)
- **Discourse forums** (E077): all 4 gates pass; 11.7% unserved-open-like fraction
- **Stack Exchange non-software** (E062): 17/20 unremedied needs served by general assistant today
- **Electrical Engineering SE** (E144): program-shaped residue 17.5% (41/234)
- **RubyGems** (E109): need-related gems have higher download counts (p=0.0045, Cliff's delta=0.214)
- **GitHub code repositories** (E148, E149): need-related repos have systematically higher star counts

### Domains Where the Principle FAILS or Has Boundaries:
- **CRAN**: no differential activity
- **Maven Central**: no differential activity
- **GitHub issues API**: no arrival field recorded
- **Web search**: 0 results with meaningful content
- **Automotive OBD2 codes**: G2 FAIL (29% vs 30% threshold)
- **3D printer fault codes**: G3 FAIL (1.8 models/fault vs 10)
- **PX4 drone fault codes**: G1 FAIL (~39 cases vs 100)
- **Medical device fault codes**: various gates fail
- **Embedded/MCU fault codes**: insufficient effect size
- **Industrial SCADA**: 76.2% unserved fraction (domain variation, not need-related)
- **CFPB consumer complaints**: 0.8% unserved fraction
- **Physics SE**: view_count present but no differential activity (p_need = p_random = 1.0)
- **crates.io**: classifier vocabulary mismatch (default listings lack need-indicator terms)
- **Reddit**: API accessibility boundary (network security block prevented data collection)
- **VS Code Marketplace (Open VSX)**: API sampling limitation — search API returns only top 100 per query sorted by downloads, preventing adequate sampling of general (theme/icon/keymap/snippet) extensions. Population kill gate fired (24 general vs 4,519 need-related). Cliff's delta = -0.055 (negligible). Inconclusive due to API constraints, not measured effect.

### Key Quantitative Findings from E148+E149:
- **E148** (n=80 repos): need-related mean 151,550 stars vs random 122,890 (~23% higher);
  72.2% of need-related repos exceed random median
- **E149** (n=80 repos, improved classification v2): need-related mean 160,328 stars vs random 77,690
  (~106% higher); 98.0% of need-related repos exceed random median; Cliff's delta ≈ 0.55
- Improved classification v2 (keywords + topics) identified 62.5% need-related vs 22.5% in E148

### Boundary Condition:
The principle works on platforms with per-request metadata (view_count/download_count/star_count)
where need-related content has systematic activity advantages. It does NOT generalize to platforms
without such metadata, nor to platforms where the effect size between need-related and random content
is too small to justify a candidate.

### Experiment Artifacts:
- EXPERIMENTS/E148-github-repo-viewcount/RESULT.md: Fresh observation on GitHub repos
- EXPERIMENTS/E149-github-repo-viewcount-followup/RESULT.md: Follow-up with improved classification
- EXPERIMENTS/151-vscode-marketplace-viewcount/RESULT.md: VS Code Marketplace (Open VSX) test — inconclusive due to API sampling limitations
- STATE-next-actions.md: Updated with E148 in documented observations, domain list updated to 15+ domains

### Named Next Action (per D083):
"fresh observation in a domain this mission has not touched, chosen by a stated rule rather than by comfort."

## Decision and Continuation

The view-count principle's boundaries are now well-mapped across 15+ domains. The principle
provides a robust measurement methodology but has not yielded a validated invention candidate
despite its consistency. The named next action — "fresh observation in a domain this mission
has not touched, chosen by a stated rule rather than by comfort" — remains the standing
constraint for the next investigation session.

### Next Step Options:

**Option A: Fresh observation in a new domain axis**
- Test the view-count principle on a platform with per-request metadata the mission has not touched
- Candidates include Mozilla Add-ons, Chrome Web Store,
  GitLab code repositories, GitHub user/organization follower counts
- Rationale: Tests the principle's breadth beyond established domains

**Option B: Synthesize findings and prepare for candidate generation consideration**
- Document the principle's established boundaries and viability
- Determine whether any domain offers a path to candidate generation
- Rationale: Comprehensive evidence accumulated across 15+ domains

**Option C: Run a targeted refinement experiment on GitHub repos**
- Improve classification scheme and test with larger sample or different metrics

Given the mission's workflow and D083's stated rule, Option A is recommended as most consistent.
Option B is also valuable for making the mission's knowledge accessible.