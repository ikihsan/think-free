# Session 2026-10-05-003-test-whether-agent-configuration-copied

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-05
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `unfinished`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-05T02:21:07+00:00
- **Duration:** ?s
- **Host:** `instance-20260717-0947`
- **Branch:** `research/origin`

## Goal

Test whether agent-configuration copied into repositories goes stale, which is the one external consequence F037's copy-not-install finding opens

## Summary

_(none recorded)_

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| EXPERIMENTS/019-copied-config-drift/README.md | 5fb7d8a47a6d | 6138 |
| EXPERIMENTS/019-copied-config-drift/README.md | 7c54a0dba99f | 8234 |
| EXPERIMENTS/019-copied-config-drift/README.md | 262bbcd29c5d | 10433 |
| EXPERIMENTS/019-copied-config-drift/a5_structural.py | 1d928c5c6967 | 5242 |
| EXPERIMENTS/019-copied-config-drift/analyse.py | 87f141e6f965 | 7968 |
| EXPERIMENTS/019-copied-config-drift/bodies.py | f396ef0cc690 | 1627 |
| EXPERIMENTS/019-copied-config-drift/control.py | 850ece0a220d | 4374 |
| EXPERIMENTS/019-copied-config-drift/population.py | 186a9246b3e9 | 4241 |
| EXPERIMENTS/019-copied-config-drift/raw/bodies.json | 0a24269a74ef | 8446 |
| EXPERIMENTS/019-copied-config-drift/raw/body--ChrisWiles__claude-code-showcase--.claude__settings.json | 9d6424bdc976 | 3588 |
| EXPERIMENTS/019-copied-config-drift/raw/body--ChrisWiles__claude-code-showcase--README.md | e3133e917bd1 | 30914 |
| EXPERIMENTS/019-copied-config-drift/raw/body--Donchitos__Claude-Code-Game-Studios--.claude__settings.json | 7b324b0a1fdd | 7874 |
| EXPERIMENTS/019-copied-config-drift/raw/body--Donchitos__Claude-Code-Game-Studios--README.md | 89ea6c28f235 | 23355 |
| EXPERIMENTS/019-copied-config-drift/raw/body--FlorianBruniaux__claude-code-ultimate-guide--.claude__settings.json | b745187676ee | 2310 |
| EXPERIMENTS/019-copied-config-drift/raw/body--FlorianBruniaux__claude-code-ultimate-guide--README.md | 45e2bdf7ff4f | 28297 |
| EXPERIMENTS/019-copied-config-drift/raw/body--FragmentedPacket__test-claude-settings-repo--.claude__settings.json | 34e9f8af47e4 | 190 |
| EXPERIMENTS/019-copied-config-drift/raw/body--FragmentedPacket__test-claude-settings-repo--README.md | 7981d7ab27b1 | 93 |
| EXPERIMENTS/019-copied-config-drift/raw/body--adriancooney__claude-code-configurator--.claude__settings.json | 7f94cf6995aa | 5794 |
| EXPERIMENTS/019-copied-config-drift/raw/body--adriancooney__claude-code-configurator--.claude__settings.local.json | a901fc8e851b | 1087 |
| EXPERIMENTS/019-copied-config-drift/raw/body--adriancooney__claude-code-configurator--README.md | 040c4d3cacd2 | 728 |
| EXPERIMENTS/019-copied-config-drift/raw/body--alirezarezvani__claude-skills--.claude__settings.json | 47bb780e6e3c | 310 |
| EXPERIMENTS/019-copied-config-drift/raw/body--alirezarezvani__claude-skills--README.md | f7a1b881bc5a | 26216 |
| EXPERIMENTS/019-copied-config-drift/raw/body--carlrannaberg__claudekit--.claude__settings.json | 7c36d4748289 | 3212 |
| EXPERIMENTS/019-copied-config-drift/raw/body--carlrannaberg__claudekit--README.md | 07bef1cbf6dc | 23214 |
| EXPERIMENTS/019-copied-config-drift/raw/body--centminmod__my-claude-code-setup--.claude__settings.json | 5222143aa63c | 387 |
| EXPERIMENTS/019-copied-config-drift/raw/body--centminmod__my-claude-code-setup--.claude__settings.local.json | d5c3e50bd91b | 3208 |
| EXPERIMENTS/019-copied-config-drift/raw/body--centminmod__my-claude-code-setup--README.md | 99826710a877 | 75014 |
| EXPERIMENTS/019-copied-config-drift/raw/body--coleam00__claude-memory-compiler--.claude__settings.json | 4c8e40ec0efb | 735 |
| EXPERIMENTS/019-copied-config-drift/raw/body--coleam00__claude-memory-compiler--README.md | 2a285afe7358 | 3865 |
| EXPERIMENTS/019-copied-config-drift/raw/body--diet103__claude-code-infrastructure-showcase--.claude__settings.json | c27d45f0ead2 | 1785 |
| EXPERIMENTS/019-copied-config-drift/raw/body--diet103__claude-code-infrastructure-showcase--README.md | 4d703af886bb | 24092 |
| EXPERIMENTS/019-copied-config-drift/raw/body--disler__claude-code-hooks-mastery--.claude__settings.json | eaf791775aaa | 3572 |
| EXPERIMENTS/019-copied-config-drift/raw/body--disler__claude-code-hooks-mastery--README.md | 7cae681798e7 | 41392 |
| EXPERIMENTS/019-copied-config-drift/raw/body--disler__claude-code-hooks-multi-agent-observability--.claude__settings.json | cebd79bd63d0 | 5461 |
| EXPERIMENTS/019-copied-config-drift/raw/body--disler__claude-code-hooks-multi-agent-observability--README.md | 2c947e433045 | 22236 |
| EXPERIMENTS/019-copied-config-drift/raw/body--disler__pi-vs-claude-code--.claude__settings.json | 4f0bc12ea00a | 127 |
| EXPERIMENTS/019-copied-config-drift/raw/body--disler__pi-vs-claude-code--README.md | 8800e49fc8ca | 30167 |
| EXPERIMENTS/019-copied-config-drift/raw/body--entireio__cli--.claude__settings.json | c24c66854209 | 2900 |
| EXPERIMENTS/019-copied-config-drift/raw/body--entireio__cli--README.md | 8334980176a1 | 44205 |
| EXPERIMENTS/019-copied-config-drift/raw/body--fcakyon__claude-codex-settings--.claude__settings.json | 82fac6351552 | 20833 |
| EXPERIMENTS/019-copied-config-drift/raw/body--fcakyon__claude-codex-settings--README.md | 385c636855ad | 104876 |
| EXPERIMENTS/019-copied-config-drift/raw/body--hoangsonww__Claude-Code-Agent-Monitor--.claude__settings.json | 8417e4cea220 | 2747 |
| EXPERIMENTS/019-copied-config-drift/raw/body--hoangsonww__Claude-Code-Agent-Monitor--README.md | 136279c014cf | 227906 |
| EXPERIMENTS/019-copied-config-drift/raw/body--krusemediallc__arcads-claude-code--.claude__settings.json | 414984341eb8 | 258 |
| EXPERIMENTS/019-copied-config-drift/raw/body--krusemediallc__arcads-claude-code--README.md | 8a812303ad1c | 25736 |
| EXPERIMENTS/019-copied-config-drift/raw/body--laboqaba935-jpg__super--.claude__settings.json | 6b836b4c2b95 | 79 |
| EXPERIMENTS/019-copied-config-drift/raw/body--laboqaba935-jpg__super--README.md | bed19b4fe84e | 109 |
| EXPERIMENTS/019-copied-config-drift/raw/body--matt1398__claude-devtools--.claude__settings.json | b7d76f7f9931 | 2157 |
| EXPERIMENTS/019-copied-config-drift/raw/body--matt1398__claude-devtools--README.md | 81654a0ecc6e | 13434 |
| EXPERIMENTS/019-copied-config-drift/raw/body--mksglu__context-mode--.claude__settings.json | ea72bfb78b61 | 284 |
| EXPERIMENTS/019-copied-config-drift/raw/body--mksglu__context-mode--README.md | 9308e09043c4 | 94871 |
| EXPERIMENTS/019-copied-config-drift/raw/body--parcadei__Continuous-Claude-v3--.claude__settings.json | 7636de376cad | 7091 |
| EXPERIMENTS/019-copied-config-drift/raw/body--parcadei__Continuous-Claude-v3--README.md | 0dfb39d0039d | 51706 |
| EXPERIMENTS/019-copied-config-drift/raw/body--pedrohcgs__claude-code-my-workflow--.claude__settings.json | aeffad287fac | 3461 |
| EXPERIMENTS/019-copied-config-drift/raw/body--pedrohcgs__claude-code-my-workflow--README.md | 344acb25048f | 49858 |
| EXPERIMENTS/019-copied-config-drift/raw/body--s0ld13rr__claude-code-backdoor--.claude__settings.json | ed1304611487 | 212 |
| EXPERIMENTS/019-copied-config-drift/raw/body--s0ld13rr__claude-code-backdoor--README.md | afdb10a8c9d4 | 2382 |
| EXPERIMENTS/019-copied-config-drift/raw/body--shanraisshan__claude-code-best-practice--.claude__settings.json | 3d4ede9a1774 | 12061 |
| EXPERIMENTS/019-copied-config-drift/raw/body--shanraisshan__claude-code-best-practice--README.md | 6f25dbe1c348 | 74433 |
| EXPERIMENTS/019-copied-config-drift/raw/body--shanraisshan__claude-code-hooks--.claude__settings.json | 590a16a460f4 | 9686 |
| EXPERIMENTS/019-copied-config-drift/raw/body--shanraisshan__claude-code-hooks--README.md | dc8690a422b8 | 8829 |
| EXPERIMENTS/019-copied-config-drift/raw/body--shdsjh123-cpu__claude-code-blog-builder--.claude__settings.json | 643032db0198 | 603 |
| EXPERIMENTS/019-copied-config-drift/raw/body--shdsjh123-cpu__claude-code-blog-builder--.claude__settings.local.json | c77c29b8a02b | 1270 |
| EXPERIMENTS/019-copied-config-drift/raw/body--shdsjh123-cpu__claude-code-blog-builder--README.md | ee92ceee4b7b | 4901 |
| EXPERIMENTS/019-copied-config-drift/raw/body--shintaro-sprech__agent-orchestrator-template--.claude__settings.json | 376240a9bdc3 | 1035 |
| EXPERIMENTS/019-copied-config-drift/raw/body--shintaro-sprech__agent-orchestrator-template--README.md | b34977129e67 | 7514 |
| EXPERIMENTS/019-copied-config-drift/raw/body--theaiautomators__claude-code-agentic-rag-masterclass--.claude__settings.json | c0e60608112e | 795 |
| EXPERIMENTS/019-copied-config-drift/raw/body--theaiautomators__claude-code-agentic-rag-masterclass--README.md | a0f861df405c | 2721 |
| EXPERIMENTS/019-copied-config-drift/raw/body--thedotmack__claude-mem--.claude__settings.json | f17ade64fc4d | 154 |
| EXPERIMENTS/019-copied-config-drift/raw/body--thedotmack__claude-mem--README.md | 289f3c28ddd1 | 19085 |
| EXPERIMENTS/019-copied-config-drift/raw/body--ursisterbtw__ccprompts--.claude__settings.json | b93c7f9f63b5 | 481 |
| EXPERIMENTS/019-copied-config-drift/raw/body--ursisterbtw__ccprompts--README.md | 834aafe08771 | 6818 |
| EXPERIMENTS/019-copied-config-drift/raw/body--wesammustafa__Claude-Code-Everything-You-Need-to-Know--.claude__settings.json | d0fe2deb635a | 660 |
| EXPERIMENTS/019-copied-config-drift/raw/body--wesammustafa__Claude-Code-Everything-You-Need-to-Know--README.md | 073664964f2c | 61972 |
| EXPERIMENTS/019-copied-config-drift/raw/control.json | c41ee253ac37 | 14805 |
| EXPERIMENTS/019-copied-config-drift/raw/population.json | 52f3e4f2533e | 31730 |
| EXPERIMENTS/019-copied-config-drift/raw/probe--ChrisWiles__claude-code-showcase--settings | 9d6424bdc976 | 3588 |
| EXPERIMENTS/019-copied-config-drift/raw/probe--ChrisWiles__claude-code-showcase--skills | 4ad779140508 | 2849 |
| EXPERIMENTS/019-copied-config-drift/raw/probe--Donchitos__Claude-Code-Game-Studios--settings | 7b324b0a1fdd | 7874 |
| EXPERIMENTS/019-copied-config-drift/raw/probe--FlorianBruniaux__claude-code-ultimate-guide--settings | b745187676ee | 2310 |
| EXPERIMENTS/019-copied-config-drift/raw/probe--FragmentedPacket__test-claude-settings-repo--settings | 34e9f8af47e4 | 190 |
| EXPERIMENTS/019-copied-config-drift/raw/probe--adriancooney__claude-code-configurator--settings | 7f94cf6995aa | 5794 |
| EXPERIMENTS/019-copied-config-drift/raw/probe--alirezarezvani__claude-skills--commands | 778f4b834409 | 7012 |
| EXPERIMENTS/019-copied-config-drift/raw/probe--alirezarezvani__claude-skills--settings | 47bb780e6e3c | 310 |
| EXPERIMENTS/019-copied-config-drift/raw/probe--carlrannaberg__claudekit--agents | 91e98da9102e | 26 |
| EXPERIMENTS/019-copied-config-drift/raw/probe--carlrannaberg__claudekit--settings | 7c36d4748289 | 3212 |
| EXPERIMENTS/019-copied-config-drift/raw/probe--centminmod__my-claude-code-setup--settings | 5222143aa63c | 387 |
| EXPERIMENTS/019-copied-config-drift/raw/probe--coleam00__claude-memory-compiler--settings | 4c8e40ec0efb | 735 |
| EXPERIMENTS/019-copied-config-drift/raw/probe--diet103__claude-code-infrastructure-showcase--agents | 06cc24cc4075 | 6093 |
| EXPERIMENTS/019-copied-config-drift/raw/probe--diet103__claude-code-infrastructure-showcase--hooks | ce830a5b65c2 | 6232 |
| EXPERIMENTS/019-copied-config-drift/raw/probe--diet103__claude-code-infrastructure-showcase--settings | c27d45f0ead2 | 1785 |
| EXPERIMENTS/019-copied-config-drift/raw/probe--diet103__claude-code-infrastructure-showcase--skills | 54f4d0cc16e2 | 7669 |
| EXPERIMENTS/019-copied-config-drift/raw/probe--disler__claude-code-hooks-mastery--settings | eaf791775aaa | 3572 |
| EXPERIMENTS/019-copied-config-drift/raw/probe--disler__claude-code-hooks-multi-agent-observability--settings | cebd79bd63d0 | 5461 |
| EXPERIMENTS/019-copied-config-drift/raw/probe--disler__pi-vs-claude-code--settings | 4f0bc12ea00a | 127 |
| EXPERIMENTS/019-copied-config-drift/raw/probe--entireio__cli--settings | c24c66854209 | 2900 |
| EXPERIMENTS/019-copied-config-drift/raw/probe--fcakyon__claude-codex-settings--settings | 82fac6351552 | 20833 |
| EXPERIMENTS/019-copied-config-drift/raw/probe--hoangsonww__Claude-Code-Agent-Monitor--settings | 8417e4cea220 | 2747 |
| EXPERIMENTS/019-copied-config-drift/raw/probe--krusemediallc__arcads-claude-code--settings | 414984341eb8 | 258 |
| EXPERIMENTS/019-copied-config-drift/raw/probe--laboqaba935-jpg__super--settings | 6b836b4c2b95 | 79 |
| EXPERIMENTS/019-copied-config-drift/raw/probe--matt1398__claude-devtools--settings | b7d76f7f9931 | 2157 |
| EXPERIMENTS/019-copied-config-drift/raw/probe--mksglu__context-mode--settings | ea72bfb78b61 | 284 |
| EXPERIMENTS/019-copied-config-drift/raw/probe--parcadei__Continuous-Claude-v3--hooks | 38eddcaec826 | 3902 |
| EXPERIMENTS/019-copied-config-drift/raw/probe--parcadei__Continuous-Claude-v3--settings | 7636de376cad | 7091 |
| EXPERIMENTS/019-copied-config-drift/raw/probe--parcadei__Continuous-Claude-v3--skills | 450c3fa631e8 | 2558 |
| EXPERIMENTS/019-copied-config-drift/raw/probe--pedrohcgs__claude-code-my-workflow--settings | aeffad287fac | 3461 |
| EXPERIMENTS/019-copied-config-drift/raw/probe--s0ld13rr__claude-code-backdoor--settings | ed1304611487 | 212 |
| EXPERIMENTS/019-copied-config-drift/raw/probe--shanraisshan__claude-code-best-practice--settings | 3d4ede9a1774 | 12061 |
| EXPERIMENTS/019-copied-config-drift/raw/probe--shanraisshan__claude-code-hooks--settings | 590a16a460f4 | 9686 |
| EXPERIMENTS/019-copied-config-drift/raw/probe--shdsjh123-cpu__claude-code-blog-builder--settings | 643032db0198 | 603 |
| EXPERIMENTS/019-copied-config-drift/raw/probe--shintaro-sprech__agent-orchestrator-template--settings | 376240a9bdc3 | 1035 |
| EXPERIMENTS/019-copied-config-drift/raw/probe--theaiautomators__claude-code-agentic-rag-masterclass--settings | c0e60608112e | 795 |
| EXPERIMENTS/019-copied-config-drift/raw/probe--thedotmack__claude-mem--settings | f17ade64fc4d | 154 |
| EXPERIMENTS/019-copied-config-drift/raw/probe--ursisterbtw__ccprompts--settings | b93c7f9f63b5 | 481 |
| EXPERIMENTS/019-copied-config-drift/raw/probe--wesammustafa__Claude-Code-Everything-You-Need-to-Know--settings | d0fe2deb635a | 660 |
| EXPERIMENTS/019-copied-config-drift/raw/probe_validation.json | 6576d465593a | 3355 |
| EXPERIMENTS/019-copied-config-drift/raw/surface.json | 959183e4f1e6 | 6188 |
| EXPERIMENTS/019-copied-config-drift/raw/trees.json | 5f2631f7d8c2 | 319925 |
| EXPERIMENTS/019-copied-config-drift/results.json | be0867023cd0 | 4524 |
| EXPERIMENTS/019-copied-config-drift/results_a5.json | 623f4fb41207 | 8834 |
| EXPERIMENTS/019-copied-config-drift/surface.py | df111faf7eb5 | 2318 |
| EXPERIMENTS/019-copied-config-drift/trees.py | d8e08c799df3 | 3656 |
| EXPERIMENTS/019-copied-config-drift/validate_probe.py | 65e017d2a216 | 3286 |
| EXPERIMENTS/020-copied-config-drift/README.md | 03d00b14dac6 | 13380 |
| EXPERIMENTS/020-copied-config-drift/results.json | 47e47f6fe821 | 6256 |
| tests/test_copied_config_drift.py | b742cf444822 | 6289 |
| FAILURES-findings-15.md | 01754f7217dd | 13620 |
| ROADMAP.md | 2c3f835163e2 | 20007 |
| STATE.md | a20e31ec0eb6 | 30539 |
| STATE-next-actions.md | 0e5c1d247352 | 21628 |
| STATE-constraints.md | 15f3f217f8f1 | 9837 |
| FAILURES.md | a5401589c06a | 8777 |
| FAILURES-findings-15.md | 5395e9cf0602 | 13617 |
| EXPERIMENTS/README.md | 6f58a1e0f3c1 | 3395 |
| docs/INDEX.md | 73a32a9d0ff6 | 24993 |
| DECISIONS.md | b0bb42886da8 | 7599 |
| DECISIONS-SCREENING-2.md | d160d84639cd | 18452 |
| tests/test_copied_config_drift.py | a356d129641e | 6932 |
| tasks/CLAIMS.jsonl | 8851dceb6c31 | 66205 |
| tasks/INDEX.md | ce02678550e2 | 8941 |
| tasks/README.md | 36c8e7a5bebe | 2624 |
| tasks/T-0001-write-falsification-kill-gates-for-the-three-hel.md | db8c6a87bbbd | 2098 |
| tasks/T-0002-run-investigation-e-the-experimental-engineer-ro.md | 53b150d6a94e | 1900 |
| tasks/T-0003-run-investigation-f-the-adoption-researcher-role.md | 80507f9bd456 | 1841 |
| tasks/T-0004-make-concurrent-multi-vm-sessions-safe-isolated.md | 10f60fbe97b0 | 4371 |
| tasks/T-0005-a1-run-the-bounded-sidewalk-survey-masking-exper.md | 9ad86c67489d | 887 |
| tasks/T-0006-002-a1-masking-sensitivity-sweep-over-budget-k-a.md | 0219fe628855 | 734 |
| tasks/T-0007-002-a1-masking-distance-limited-fieldwork-cost-b.md | e3c03f6cd691 | 1300 |
| tasks/T-0008-apply-the-information-sufficiency-witness-to-the.md | 510f7c33d99d | 2671 |
| tasks/T-0009-repair-the-knitting-witness-input-set-by-adding.md | 99b17e806f2f | 2688 |
| tasks/T-0010-run-the-knitting-stage-a-planner-comparison-loca.md | 573fe278832f | 2488 |
| tasks/T-0011-knitting-stage-a-follow-up-bounded-neighbourhood.md | 6fcecb073999 | 2055 |
| tasks/T-0012-screen-all-six-sealed-investigations-with-e-s-fa.md | a9a374f2a76c | 2909 |
| tasks/T-0013-run-e3-s-build-timestamp-census-over-200-recent.md | 26c375a1c308 | 3474 |
| tasks/T-0014-c2-ventilation-kill-gate-adaptive-next-measureme.md | b021931cba52 | 2778 |
| tasks/T-0015-run-the-knitting-candidate-s-remaining-kill-gate.md | 1c9f08d0c549 | 3323 |
| tasks/T-0016-make-the-test-suite-pass-on-the-ci-runner-s-pyth.md | 7729e7ad24fd | 2255 |
| tasks/T-0017-build-one-source-twice-under-different-source-da.md | f0db3413eea3 | 5826 |
| tasks/T-0018-record-exercised-git-versions-machine-readably-a.md | cd873e63caf5 | 1520 |
| tasks/T-0019-snapshot-side-a-of-the-e2-dependency-closure-dri.md | 1bc7e63a7e02 | 1867 |
| tasks/T-0020-tell-an-in-flight-session-apart-from-an-abandone.md | 8c8e8132190f | 6495 |
| tasks/T-0021-resolve-the-merge-conflict-markers-committed-to.md | 5264e02b5cad | 3954 |
| tasks/T-0022-implement-origin-release-check-so-release-manife.md | 36599cc36be8 | 5563 |
| tasks/T-0023-repair-the-two-operations-documents-whose-stated.md | d329d1fad195 | 4135 |
| tasks/T-0024-stop-session-reconciliation-and-the-documentatio.md | 9b3b6624ec04 | 6434 |
| tasks/T-0025-record-the-measured-result-of-the-pushed-ci-run.md | ecd0e25c1fcb | 3416 |
| tasks/T-0026-make-task-new-leave-no-orphan-a-new-task-file-re.md | a8b6bdf12d82 | 4252 |
| tasks/T-0027-make-the-published-claim-commit-carry-the-regene.md | 3f85552e5245 | 3519 |
| tasks/T-0028-record-the-ci-run-history-around-the-orphan-fix.md | 10af69e73dcb | 2883 |
| tasks/T-0029-make-origin-doctor-report-the-push-credential-me.md | eb0e3c5028d6 | 7195 |
| tasks/T-0030-refuse-a-commit-that-gives-one-finding-decision.md | 780adde2cfc5 | 3071 |
| tasks/T-0031-allocate-f-d-and-t-identifiers-from-the-shared-b.md | 9b90733eef91 | 5372 |
| tasks/T-0032-record-the-python-versions-the-suite-has-actuall.md | 9ac33ef9bd5b | 6496 |
| tasks/T-0033-make-doctor-compare-this-vm-s-git-and-interprete.md | 3a6e5ab4b731 | 5355 |
| tasks/T-0034-run-the-test-suite-on-the-python-versions-tests.md | 1cb3179da822 | 7394 |
| tasks/T-0035-stop-the-credential-sandbox-from-inheriting-a-ci.md | d92134f31ae0 | 5527 |
| tasks/T-0036-report-a-duplicate-defect-number-in-state-defect.md | 372433d4b7aa | 4422 |
| tasks/T-0037-explain-the-four-red-ci-runs-since-the-version-m.md | fac29bd23685 | 6151 |
| tasks/T-0038-record-that-the-public-check-run-annotations-wer.md | b885818dba8c | 2179 |
| tasks/T-0039-make-acceptance-and-steps-append-on-task-new-so.md | 658857dcefa9 | 1980 |
| tasks/T-0040-make-a-red-doc-lint-release-check-or-skills-gate.md | 1d936ce4f0e7 | 6226 |
| tasks/T-0041-make-sync-land-rebuild-any-generated-file-the-re.md | b6cdb0e774e0 | 2376 |
| tasks/T-0042-report-a-decision-file-whose-own-header-disagree.md | 00fc226bfac8 | 7525 |
| tasks/T-0043-split-tools-originlib-identifiers-py-so-doc-lint.md | 733893f55d5b | 5782 |
| tasks/T-0044-date-the-lease-tests-from-the-clock-the-code-act.md | a1666ee9861c | 4576 |
| tasks/T-0045-run-release-check-from-preflight-and-classify-de.md | b3e7031d51b7 | 4456 |
| tasks/T-0046-measure-how-github-files-an-annotation-on-the-fi.md | 12b14b56a8b3 | 8168 |
| tasks/T-0047-attribute-a-task-file-that-a-task-command-rewrot.md | 5640f27c3475 | 9823 |
| tasks/T-0048-teach-sync-land-to-finish-a-paused-rebase-whose.md | 9d5f32ec9157 | 7444 |
| tasks/T-0049-record-the-measured-ci-state-on-the-tip-and-the.md | 1f05eb9d6b2e | 4723 |
| tasks/T-0050-separate-the-line-cap-exemption-from-reconciliat.md | ba661ec2149c | 5942 |
| tasks/T-0051-make-doc-lint-s-broken-link-verdict-a-function-o.md | 3a044675864f | 6648 |
| tasks/T-0052-report-a-row-a-document-s-own-table-already-cont.md | 9992ced14d65 | 7023 |
| tasks/T-0053-record-a-base-advance-when-a-paused-rebase-is-co.md | 1e86eb1b14b9 | 1818 |
| tasks/T-0054-measure-every-commit-on-the-base-branch-that-red.md | 2b6a3318d733 | 5104 |
| tasks/T-0055-publish-a-task-claim-from-inside-an-open-session.md | d0c44d890287 | 2491 |
| tasks/T-0056-hold-a-mission-record-s-restated-experiment-numb.md | faf36696acc1 | 3793 |
| tasks/T-0057-make-the-ci-failure-annotation-carry-the-excepti.md | f37ba49a8458 | 4225 |
| tasks/T-0058-test-whether-flat-adoption-is-general-or-niche-s.md | c8c4620dd83b | 1033 |
| tasks/T-0059-measure-whether-prior-art-exists-can-predict-any.md | 8d80eedf6076 | 2242 |
| tasks/T-0060-measure-whether-the-incumbents-a-prior-art-scree.md | 694aa9b36893 | 2401 |
| tasks/T-0061-test-whether-a-prior-art-screen-s-population-in.md | 3e550048105f | 3174 |
| tasks/T-0062-re-adjudicate-e012-s-19-prior-art-kills-on-three.md | 6fe1abca66aa | 3512 |
| tasks/T-0063-test-whether-f033-s-project-level-denominator-hi.md | b53897c2f12d | 2181 |
| tasks/T-0064-measure-whether-the-young-vocabulary-s-artifacts.md | 280a954db75c | 2613 |
| tasks/T-0065-test-whether-agent-configuration-copied-into-rep.md | 57ba73d01557 | 2731 |

## Commands

11 captured, 2 non-zero exit.

| # | command | exit | ms |
|---|---|---|---|
| 5 | ['python3', 'EXPERIMENTS/019-copied-config-drift/population.py'] | 0 | 242661 |
| 6 | ['python3', 'EXPERIMENTS/019-copied-config-drift/bodies.py'] | 1 | 618 |
| 7 | ['python3', 'EXPERIMENTS/019-copied-config-drift/bodies.py'] | 0 | 47659 |
| 10 | ['python3', 'EXPERIMENTS/019-copied-config-drift/analyse.py'] | 0 | 301 |
| 11 | ['python3', 'EXPERIMENTS/019-copied-config-drift/surface.py'] | 0 | 106060 |
| 12 | ['python3', 'EXPERIMENTS/019-copied-config-drift/validate_probe.py'] | 0 | 10768 |
| 13 | ['python3', 'EXPERIMENTS/019-copied-config-drift/trees.py'] | 0 | 166631 |
| 14 | ['python3', 'EXPERIMENTS/019-copied-config-drift/a5_structural.py'] | 0 | 163 |
| 15 | ['python3', 'EXPERIMENTS/019-copied-config-drift/control.py'] | 0 | 299035 |
| 154 | ['env', 'PYTHONPATH=tools:tests', 'python3', '-m', 'unittest', 'discover', '-s', 'tests', '-t', 'tests'] | 1 | 383367 |
| 155 | ['env', 'PYTHONPATH=tools:tests', 'python3', '-m', 'unittest', 'discover', '-s', 'tests', '-t', 'tests'] | 0 | 371183 |

## Integrity

| check | result |
|---|---|
| session_end event | MISSING - session may be unfinished |
| undeclared file changes | 0 |
| declared artifacts now missing | 0 |
| integrity errors | 0 |
| redactions applied to command output | 0 |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 02:21:07 | session_start | Test whether agent-configuration copied into repositories goes stale, which is the one external consequence F037's copy-not-install finding opens |
| 2 | 02:23:10 | task_rewrite | appended a create record for T-0064 |
| 3 | 02:23:54 | artifact | wrote EXPERIMENTS/019-copied-config-drift/README.md |
| 4 | 02:23:55 | milestone | E019 protocol written with both gates and both falsification arms declared before the first fetch |
| 5 | 02:28:30 | command | $ python3 EXPERIMENTS/019-copied-config-drift/population.py |
| 6 | 02:29:14 | command | $ python3 EXPERIMENTS/019-copied-config-drift/bodies.py |
| 7 | 02:30:10 | command | $ python3 EXPERIMENTS/019-copied-config-drift/bodies.py |
| 8 | 02:31:24 | artifact | wrote EXPERIMENTS/019-copied-config-drift/README.md |
| 9 | 02:31:24 | milestone | README attribution rule yields 0 of 31; declared a second attribution channel before running it, gate threshold unchanged |
| 10 | 02:31:56 | command | $ python3 EXPERIMENTS/019-copied-config-drift/analyse.py |
| 11 | 02:35:16 | command | $ python3 EXPERIMENTS/019-copied-config-drift/surface.py |
| 12 | 02:35:56 | command | $ python3 EXPERIMENTS/019-copied-config-drift/validate_probe.py |
| 13 | 02:39:18 | command | $ python3 EXPERIMENTS/019-copied-config-drift/trees.py |
| 14 | 02:39:46 | command | $ python3 EXPERIMENTS/019-copied-config-drift/a5_structural.py |
| 15 | 02:45:43 | command | $ python3 EXPERIMENTS/019-copied-config-drift/control.py |
| 16 | 02:46:32 | artifact | wrote EXPERIMENTS/019-copied-config-drift/README.md |
| 17 | 02:46:32 | artifact | wrote EXPERIMENTS/019-copied-config-drift/a5_structural.py |
| 18 | 02:46:32 | artifact | wrote EXPERIMENTS/019-copied-config-drift/analyse.py |
| 19 | 02:46:32 | artifact | wrote EXPERIMENTS/019-copied-config-drift/bodies.py |
| 20 | 02:46:32 | artifact | wrote EXPERIMENTS/019-copied-config-drift/control.py |
| 21 | 02:46:32 | artifact | wrote EXPERIMENTS/019-copied-config-drift/population.py |
| 22 | 02:46:33 | artifact | wrote EXPERIMENTS/019-copied-config-drift/raw/bodies.json |
| 23 | 02:46:33 | artifact | wrote EXPERIMENTS/019-copied-config-drift/raw/body--ChrisWiles__claude-code-showcase--.claude__settings.json |
| 24 | 02:46:33 | artifact | wrote EXPERIMENTS/019-copied-config-drift/raw/body--ChrisWiles__claude-code-showcase--README.md |
| 25 | 02:46:33 | artifact | wrote EXPERIMENTS/019-copied-config-drift/raw/body--Donchitos__Claude-Code-Game-Studios--.claude__settings.json |
| 26 | 02:46:34 | artifact | wrote EXPERIMENTS/019-copied-config-drift/raw/body--Donchitos__Claude-Code-Game-Studios--README.md |
| 27 | 02:46:34 | artifact | wrote EXPERIMENTS/019-copied-config-drift/raw/body--FlorianBruniaux__claude-code-ultimate-guide--.claude__settings.json |
| 28 | 02:46:34 | artifact | wrote EXPERIMENTS/019-copied-config-drift/raw/body--FlorianBruniaux__claude-code-ultimate-guide--README.md |
| 29 | 02:46:34 | artifact | wrote EXPERIMENTS/019-copied-config-drift/raw/body--FragmentedPacket__test-claude-settings-repo--.claude__settings.json |
| 30 | 02:46:34 | artifact | wrote EXPERIMENTS/019-copied-config-drift/raw/body--FragmentedPacket__test-claude-settings-repo--README.md |
| 31 | 02:46:34 | artifact | wrote EXPERIMENTS/019-copied-config-drift/raw/body--adriancooney__claude-code-configurator--.claude__settings.json |
| 32 | 02:46:35 | artifact | wrote EXPERIMENTS/019-copied-config-drift/raw/body--adriancooney__claude-code-configurator--.claude__settings.local.json |
| 33 | 02:46:35 | artifact | wrote EXPERIMENTS/019-copied-config-drift/raw/body--adriancooney__claude-code-configurator--README.md |
| 34 | 02:46:35 | artifact | wrote EXPERIMENTS/019-copied-config-drift/raw/body--alirezarezvani__claude-skills--.claude__settings.json |
| 35 | 02:46:35 | artifact | wrote EXPERIMENTS/019-copied-config-drift/raw/body--alirezarezvani__claude-skills--README.md |
| 36 | 02:46:35 | artifact | wrote EXPERIMENTS/019-copied-config-drift/raw/body--carlrannaberg__claudekit--.claude__settings.json |
| 37 | 02:46:36 | artifact | wrote EXPERIMENTS/019-copied-config-drift/raw/body--carlrannaberg__claudekit--README.md |
| 38 | 02:46:36 | artifact | wrote EXPERIMENTS/019-copied-config-drift/raw/body--centminmod__my-claude-code-setup--.claude__settings.json |
| 39 | 02:46:36 | artifact | wrote EXPERIMENTS/019-copied-config-drift/raw/body--centminmod__my-claude-code-setup--.claude__settings.local.json |
| 40 | 02:46:36 | artifact | wrote EXPERIMENTS/019-copied-config-drift/raw/body--centminmod__my-claude-code-setup--README.md |
| 221 | 03:24:32 | artifact | wrote tasks/T-0056-hold-a-mission-record-s-restated-experiment-numb.md |
| 222 | 03:24:32 | artifact | wrote tasks/T-0057-make-the-ci-failure-annotation-carry-the-excepti.md |
| 223 | 03:24:33 | artifact | wrote tasks/T-0058-test-whether-flat-adoption-is-general-or-niche-s.md |
| 224 | 03:24:33 | artifact | wrote tasks/T-0059-measure-whether-prior-art-exists-can-predict-any.md |
| 225 | 03:24:33 | artifact | wrote tasks/T-0060-measure-whether-the-incumbents-a-prior-art-scree.md |
| 226 | 03:24:33 | artifact | wrote tasks/T-0061-test-whether-a-prior-art-screen-s-population-in.md |
| 227 | 03:24:33 | artifact | wrote tasks/T-0062-re-adjudicate-e012-s-19-prior-art-kills-on-three.md |
| 228 | 03:24:34 | artifact | wrote tasks/T-0063-test-whether-f033-s-project-level-denominator-hi.md |
| 229 | 03:24:34 | artifact | wrote tasks/T-0064-measure-whether-the-young-vocabulary-s-artifacts.md |
| 230 | 03:24:34 | artifact | wrote tasks/T-0065-test-whether-agent-configuration-copied-into-rep.md |

_180 middle events omitted; see `events.jsonl`._

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-05-003-test-whether-agent-configuration-copied/events.jsonl
```

> Truncated to 300 lines. Full record: `sessions/2026-10-05-003-test-whether-agent-configuration-copied/events.jsonl`
