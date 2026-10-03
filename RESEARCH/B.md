# B — Problem archaeology

Sealed independent first pass: 2026-10-03. Researcher: B. Read `MISSION.md`; did not read other research, unrelated repositories, or personal memory. Public sources retrieved 2026-10-03. No code experiments, user interviews, installations, external writes, or runtime validation were performed. Source claims below are not independently reproduced results.

## Decision

**Advance one narrow hypothesis to falsification: independent, conservative verification of photo-library migration semantics against the actual destination. Do not select a product yet.** The pain is concrete and repeated, but adjacent prior art is strong. A generalized migration app, metadata fixer, checksum report, or “safe cloud exit” is already occupied territory. The possible distinction is a destination-observed, relationship-aware audit with explicit unsupported/ambiguous states, independent of the importer that performed the migration.

I investigated four materially different areas: personal-photo preservation, domestic heating, sewing/fabrication, and care handoffs. I am withholding a second promoted hypothesis because searches found direct alternatives or a weak path from software to the underlying problem. This is more useful than padding the shortlist.

## 1. Photo preservation: the normalized struggle

**Observed in primary user reports:** people migrate an irreplaceable archive, see a nominally successful import, then discover semantic damage and run repair scripts, delete/reimport, or inspect files manually. A successful copy and a usable preserved library are different claims.

- [Immich issue 24917](https://github.com/immich-app/immich/issues/24917), opened 2025-12-29: the reporter describes roughly 24,000 photos and 1,000 videos, pre-import EXIF repair, thousands still grouped under import date, then deletion/reimport with surprising duplicate behavior. Closed status does not establish a current unfixed defect. The value of this report is the costly workaround sequence and uncertainty, not a claim that all current imports fail.
- [immich-go issue 1422](https://github.com/simulot/immich-go/issues/1422), opened 2026-08-18: a detailed report includes a four-JPEG/two-sidecar reproducer and API logs. It alleges that processing an edited image first can skip its original or delete the edited upload. The shown end state has two assets from four distinct files while the importer reports zero errors. A larger reported migration lost one version in 702 original/edit pairs and encountered lost tag assignments. These are the reporter's measurements, not mine; their current reproduction remains necessary.
- [immich-go discussion 650](https://github.com/simulot/immich-go/discussions/650), 2025-era discussion, exact publication date not established in this pass: a user reports most of a 202 GB Takeout not uploading. The response explains a multi-category accounting identity including discarded, duplicate, missing-associated-metadata, and server-error states. **Inference:** even complete-looking totals require users to understand what each exclusion means.
- [Google Photos community report](https://support.google.com/photos/thread/328281808?hl=en&msgid=328483859), 2025-era, exact date not established: reports missing Takeout sidecars. **Boundary:** an audit of an export cannot certify that the cloud service exported everything. Never label an export-to-destination match “safe to delete the cloud account.”

### Hypothesis B1: a migration witness

**Proposed mechanism, untested:** ingest a source export read-only, capture a read-only destination snapshot after its asynchronous jobs settle, and compare a small explicit set of preservation contracts. Start with Google Takeout → Immich because there are public reproducers and accessible destination state.

The model would preserve provenance for each expectation: archive path and source field → expected media role/relationship → observed destination asset and field. Initially check exact media identity, capture time plus timezone semantics, original/edited membership, album membership, and supported tags. Keep unsupported semantics separate from missing data. Uncertain source-to-destination matching must produce an unresolved item, never a guessed “pass.” Do not silently treat a visually similar image as the original. Metadata rewriting and transcoding complicate byte identity; the first version should conservatively decline those identity claims rather than adopt an undocumented similarity heuristic.

The useful artifact is a compact discrepancy packet: “these two distinct source files became one destination asset”; “these 19 source album edges are absent”; “time comparison cannot be established because the source has no timezone”; every claim links to evidence. No automatic repair or deletion is necessary to test value.

**Exact possible distinction:** third-party post-migration observation of the destination's actual media and relationship graph, with machine-readable invariants and a reproducible adversarial fixture corpus. This is a testable scope distinction, not an originality claim.

### Nearest prior art — strong objections

| Existing work | What the primary source says | Consequence for this hypothesis |
|---|---|---|
| [immich-go](https://github.com/simulot/immich-go/blob/main/docs/commands/upload.md) | Specialized Google Photos migration, metadata matching and upload options. | Do not build another importer. Check whether a focused upstream verification mode is sufficient. |
| [Immich system integrity](https://docs.immich.app/administration/system-integrity/) | Detects untracked files, missing files, and checksum mismatches against its own database. | Strong existing integrity checks; proposed comparison must add source-relative missing relationships or incorrect accepted metadata. |
| [OSXPhotos compare](https://rhettbull.github.io/osxphotos/cli#compare) | Compares two Apple Photos libraries; machine-readable output and a difference exit status exist. | Comparing libraries is established prior art. Cross-application semantics and interoperability would need to earn their maintenance cost. |
| [PhotoMigrator](https://github.com/jaimetur/PhotoMigrator/blob/main/help/03-automatic-migration.md) | Migrates supported platforms, handles people labels and metadata sources, and keeps some unmatched material for review. | Broad migration coverage already exists. Inspect its code and output before writing an overlapping tool. No absence of a `verify` text match proves a missing capability. |
| [FolioSort Exit Kit](https://www.foliosort.app/features/exit-kit) | Vendor claims local export cleanup, hash-verified moves and an exportable Exit Report. Also maps iCloud albums to keywords and favourites to ratings. | “Exit report,” privacy, local operation and checksum validation are not differentiators. Its page describes file-move verification; whether it interrogates a destination app remains unverified. These are vendor claims, not benchmarked results. |
| [mxpf/photo-system-automation](https://github.com/mxpf/photo-system-automation) | Local archive auditor for a device → kDrive → Ente workflow. It checks Takeout archive sets and package parity, including sidecars. Its README explicitly distinguishes local package verification from checking the uploaded Ente account. | Closest conceptual prior art found. An auditor is not novel; actual destination observation is the narrow remaining gap to investigate. Extending this work might be better than starting a project. |

### Why the problem persists

**Source-supported:** the issue reproducer illustrates why importer bookkeeping can share the bug it is meant to report: identity/indexing heuristics collapse distinct siblings; asynchronously applied destination changes can invalidate previously successful operations. Library integrity against its own database cannot detect something that was never represented in that database.

**Inference:** source formats encode important meaning outside the bytes, apps disagree on identity and metadata priorities, and some meanings have no destination equivalent. In particular, albums-as-keywords and favourites-as-ratings are transformations, not exact semantic preservation. The hard part is declaring what is preserved and what is unknown without creating false confidence. Independently written adapters could still repeat the same mistaken interpretation.

### Smallest experiment that could change the decision

1. Inspect the current importer and comparator capabilities above; abandon a standalone tool if an existing mode already emits an equivalent source-relative destination report.
2. Reproduce issue 1422 in an isolated disposable Immich instance using its synthetic fixture or a regenerated equivalent. Pin versions. Do not touch a real archive. If fixed, retain the fixture and inject a known target-side omission to test the checker; report these as separate results.
3. Implement only the conservative source manifest plus destination snapshot comparison needed for four distinct files, two original/edit relationships, an album, and capture times. Add small mutation cases: missing original, missing edit, wrong album, lost relationship, shifted date, ambiguous filename, unsupported timezone. Require every deliberately violated supported invariant to be reported and zero unjustified passes; ambiguous cases must remain unresolved.
4. Compare output against importer logs, Immich integrity checks, and PhotoMigrator/OSXPhotos where applicable. **Falsifier:** no actionable discrepancy beyond existing reports, or maintaining unambiguous identity requires importer-specific invasive instrumentation. A successful synthetic test establishes only technical feasibility.
5. Only after that, with consent through an appropriate future recruitment channel, ask a few people actively migrating archives to run a local audit. No outreach was performed. **Usefulness falsifier:** reports are mostly unactionable ambiguity, users cannot understand what is at risk, or a simple existing command produces equivalent reassurance. Measure review time and concrete decisions changed; do not substitute downloads or stars.

**Adoption inference:** initially useful as a read-only companion to existing migration guides and a regression corpus for maintainers. A small library/fixture contribution to an established project may be the superior outcome. The recurring-use case is periodic export verification; the one-time migration market alone may not sustain a substantial standalone community.

**Remaining uncertainty:** current bug status; API completeness and pagination; source export omissions; stability of server-side metadata; realistic false-positive rate; whether users need a standalone product; availability of representative consented archives; licences of reusable fixtures; exact prior-art coverage. No claim of global novelty is justified.

## 2. Domestic heat pumps: serious pain, crowded and physically constrained

**Normalized struggle:** owners are unsure whether poor bills or comfort mean equipment failure, setup error, bad measurement, or ordinary weather effects. Their workaround is installing monitors and posting graphs for expert interpretation.

- [OpenEnergyMonitor heat-loss documentation](https://openenergymonitor.org/docs/heatpumpmonitor/measured_heat_loss.html) already analyzes measured heat demand and provides tools for understanding the gap between calculated and observed load. [Its heat-loss implementation](https://github.com/openenergymonitor/heatpumpmonitor.org/blob/main/www/views/heatloss.php) includes prediction intervals. A generic heat-loss calculator or graph explanation is weak differentiation.
- [Community report: monitoring says SCOP zero](https://community.openenergymonitor.org/t/heatpumpmonitor-electrical-consumption-not-showing-scop-is-0/25529), 2024-02-07: a new owner reports contradictory graphs and zero values after adding metering. The diagnosis involves a feed returning nulls. This illustrates measurement-pipeline faults masquerading as equipment behavior.
- [Home Assistant owner report](https://www.reddit.com/r/homeassistant/comments/1vh1a4f/stiebel_eltron_heat_pump_monitoring/), September 2026 approximate: the owner says repeated trivial heat-pump faults were hidden for days or weeks because resistive backup still heated the house. This is a concrete reason to monitor, but a single anecdote cannot establish prevalence or economic benefit.
- [NIST FDD project](https://www.nist.gov/programs-projects/fault-detection-and-diagnostics-air-conditioners-and-heat-pumps), created 2011-10-17, updated 2026-02-19: historical primary evidence of sustained work on adaptive fault detection and evaluation. Its account says different equipment responds differently to the same fault, and validation needs realistic cycling/noisy-transient data. It supplies open-source research links. This directly contradicts an easy “infer every fault from a graph” premise.
- [Stooklijn](https://github.com/Appesteijn/stooklijn) already offers heat-pump performance analysis, recommendations and cycling handling for a specific ecosystem. [HEAPO](https://arxiv.org/abs/2503.16993), March 2025, provides an open dataset with smart-meter data and on-site inspection protocols; useful for a future experimental comparison, not proof that a new product is needed.

**Parked possibility:** a read-only detector for silent fallback to resistance heating, with evidence of an observed mode change and a clear “cannot distinguish with available sensors” state. It may be useful, but existing Home Assistant alerts or equipment-native notifications may be enough. Distinguishing faults from intentional defrost/hot-water/backup operation and proving cross-device benefit require domain validation. I do not promote it without inspecting existing alert configurations and benchmarking a baseline on labeled data.

## 3. Sewing/fabrication: a real workaround, already addressed

**Normalized struggle:** preserve real-world scale when moving a PDF pattern onto fabric; avoid printing, taping sheets, subscriptions and copyshop expense. Projecting introduces alignment, focus, movement and calibration work.

[Pattern Projector's primary documentation](https://www.patternprojector.com/en) already describes a free open-source PWA, four-corner calibration against a known grid, persistent projection tools, multipage stitching, scale checks, mirroring and grain-line alignment. A [user report](https://www.reddit.com/r/sewingpatterns/comments/1uxd64z/using_a_projector_to_display_a_pattern_on_fabric/) describes a sub-five-minute calibration workflow; other community reports still ask for help. A [September/October 2026 creator post](https://www.reddit.com/r/ProjectorsForSewing/comments/1wu6arm/projector_sewing_interface_ideas/) describes self-calibration using an onboard camera; a [2026 beta-app announcement](https://www.reddit.com/r/ProjectorsForSewing/comments/1rafus9/looking_for_beta_testers_for_new_projector_sewing/) already proposes phone-camera calibration and compensation for thick fabric.

**Decision:** reject “automatic sewing-projector calibration” as this pass's invention. Improvement may be worthwhile upstream, but a material capability gap is not demonstrated. Hardware, focus and nonplanar fabric remain constraints; finding complaints is insufficient to justify another app.

## 4. Care handoffs: consequential, insufficiently differentiated

[HSSIB's 2025-07-10 investigation announcement](https://www.hssib.org.uk/news-events-blog/investigation-finds-patients-suffer-harm-as-electronic-communications-fail-to-support-their-safe-discharge-from-hospital/) describes harm when electronic hospital-discharge communication fails. The [full investigation](https://www.hssib.org.uk/patient-safety-investigations/workforce-and-patient-safety/fifth-investigation-report/) was surfaced but repeated page opening failed; do not imply a full-document review. The original possible idea was a patient-owned, source-linked discrepancy packet across medication lists, to support clinician review without deciding treatment.

Direct prior art surfaced quickly: [CareClear](https://devpost.com/software/careclear) describes extracting instructions from documents, patient confirmation, conflict flags and appointment questions; [MedSignal](https://github.com/jenishk20/MedSignal) describes local source-linked clinical facts, contradiction checks and reviewable handoffs. These descriptions do not establish clinical effectiveness, but they do defeat a basic novelty claim. **Decision:** do not promote. Missing responsibility, delayed transmission and staff capacity may dominate the problem, and an independent app can add another conflicting record.

## Search record and limits

Representative exact queries used, followed by opening the primary URLs above:

- `site.github.com immich migration Google Takeout missing metadata duplicate edited photos issue`
- `photo migration verify completeness metadata audit tool Google Takeout Immich`
- `osxphotos export verify compare metadata sidecar check missing photos`
- `site.github.com "photo" "migration" "audit" "metadata"`
- `site.github.com paperless-ngx "redact" "Discussion"` — noisy, abandoned; no claim of a gap.
- `site.projectorsforsewing.com calibration distorted pattern problem`
- `site.patternprojector.com calibration camera automatic projector`
- `site.community.openenergymonitor.org heat pump performance installer monitoring problem`
- `site.community.openenergymonitor.org heat pump heat loss estimation uncertainty solar gains room temperature`
- `open source heat pump diagnostics automatic analysis cycling recommendations monitoring`
- `site.hssib.org.uk medication not given discharge acute hospital community July 2026 report` — found relevant July **2025** material; query year was not treated as evidence.
- `"patient" "medication" "contradictions" open source reconciliation app`
- `"Keeping the Bits in Place" migration raster image data 2005` — surfaced a historical image-migration paper; publisher PDF opening failed, so no substantive finding here relies on it.

Search is not exhaustive. English-language, indexable technical communities are overrepresented. Search-result dates sometimes conflict with explicit page dates; explicit dates were preferred and uncertain dates labeled. No popularity metric was used as evidence of usefulness. The strongest next action is a small falsification experiment for B1 plus a deeper audit of its closest existing alternatives, not immediate product construction.
