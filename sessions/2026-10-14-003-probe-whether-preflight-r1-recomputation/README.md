# Session 2026-10-14-003-probe-whether-preflight-r1-recomputation

<!-- origin-meta
owner: sessions/INDEX.md
status: active
last-verified: 2026-10-14
-->

<!-- generated-by: origin; do not edit by hand -->

## Outcome

- **Result:** `worked`
- **Agent:** `unknown-agent`
- **Started:** 2026-10-14T04:28:15+00:00
- **Duration:** 2716.0s
- **Host:** `instance-20260717-0947`
- **Branch:** `research/origin`

## Goal

Probe whether preflight R1 recomputation reaches leaderboard-published LLM benchmark numbers

## Summary

E135 probe completed (resumed an unfinished session on this VM). Question: does preflight's R1 recomputation reach the number a leaderboard publishes? Cell C2 (Stanford HELM lite v1.0.0, MMLU abstract_algebra, multiple_choice_joint, 01-ai/yi-34b): G1 PASS, G2 PASS — the run ships per-instance golds (references tagged correct), raw completions, letter-to-choice mapping, run spec, per-instance verdicts and aggregates, all unauthenticated on public GCS, and the HELM site renders its numbers from the same bytes (helm.js fetches the crfm-helm-public bucket). G3 AGREE: recompute.py, a 71-line stdlib-only script that never reads a verdict column, recomputed valid 3/11 = 0.272727... and test 40/100 = 0.4000, equal to the published stats.json means to full printed precision, and agreed with the harness's own per-instance verdicts on 111/111 rows. C1 (Open LLM Leaderboard v2) and C3 (Chatbot Arena) fail G2 as probed: C1's detail dataset is auth-restricted and raw runs live in submitters' repos; C3's votes are gated:auto and its Elo is fit on the full vote population, not the published sample. Kill gate did not fire (requires G2 failure on all three cells), so the leaderboard direction stays open; per the protocol this is the weaker stated outcome — reach demonstrated, external value still unobserved, D111 stands, preflight stays unreleased. Two instrument facts recorded: the published valid/test split is 11/100 rows, so a pooled 111-row recomputation (0.3874) would falsely report disagreement — the split key is part of the instrument; and the parse rule was never stressed because all 111 completions are single letters (max_tokens=1), so the agreement validates plumbing, not a parser. Third-party bytes recorded by sha256 in fetched-manifest.json, never committed (D091/D092 rule). doc lint green.

## Next

Named next action (from RESULT.md): point R1 at a leaderboard cell whose completions are free text and whose published number is an aggregate over multiple runs (e.g. a HELM scenario aggregate or a suite mean), where a parser and a weighting rule are both exercised — that is the first cell where recomputation could disagree with the published number for a reason other than plumbing. Declare the protocol before any fetch, as E135 did.

## Artifacts

| path | sha256 (first 12) | bytes |
|---|---|---|
| EXPERIMENTS/135-preflight-leaderboard-reach/RESULT.md | 38b3583791f5 | 5637 |
| EXPERIMENTS/135-preflight-leaderboard-reach/recompute.py | d23baf5f642a | 3057 |
| EXPERIMENTS/135-preflight-leaderboard-reach/reconcile.py | f71340d2cb63 | 3331 |
| EXPERIMENTS/135-preflight-leaderboard-reach/completion_shapes.py | 23365b7b9b01 | 1281 |
| STATE.md | bec2e3cb8fe5 | 42841 |
| EXPERIMENTS/135-preflight-leaderboard-reach/manifest_fetched.py | aa886d75f8c7 | 2244 |
| EXPERIMENTS/135-preflight-leaderboard-reach/fetched-manifest.json | 3677ebb8bec2 | 1832 |

## Commands

33 captured, 1 non-zero exit.

| # | command | exit | ms |
|---|---|---|---|
| 2 | ['curl', '-s', '-o', '/dev/null', '-w', 'C1-space %{http_code} %{size_download}\\n', '--max-time', '30', 'https://huggingface.co/spaces/open-llm-leade | 0 | 878 |
| 3 | ['curl', '-s', '--max-time', '30', 'https://huggingface.co/api/spaces/open-llm-leaderboard/open_llm_leaderboard'] | 0 | 284 |
| 4 | ['curl', '-s', '--max-time', '30', 'https://huggingface.co/api/datasets?author=open-llm-leaderboard&limit=30'] | 0 | 278 |
| 5 | ['curl', '-s', '--max-time', '30', 'https://huggingface.co/api/datasets/open-llm-leaderboard/gpt2-details'] | 0 | 631 |
| 6 | ['curl', '-s', '--max-time', '60', 'https://huggingface.co/datasets/open-llm-leaderboard/gpt2-details/resolve/main/gpt2/results_2024-06-04T15-21-52.17 | 0 | 275 |
| 7 | ['curl', '-s', '--max-time', '30', 'https://huggingface.co/api/datasets?author=open-llm-leaderboard&limit=100'] | 0 | 414 |
| 8 | ['curl', '-s', '--max-time', '30', 'https://huggingface.co/api/spaces/open-llm-leaderboard/open_llm_leaderboard'] | 0 | 345 |
| 9 | ['curl', '-s', '-o', '/dev/null', '-w', '%{http_code}\\n', '--max-time', '20', 'https://open-llm-leaderboard-open-llm-leaderboard.hf.space/gradio_api/ | 0 | 1005 |
| 10 | ['curl', '-s', '-o', '/dev/null', '-w', '%{http_code}\\n', '--max-time', '20', 'https://open-llm-leaderboard.hf.space/gradio_api/info'] | 0 | 877 |
| 11 | ['curl', '-s', '--max-time', '30', 'https://open-llm-leaderboard-open-llm-leaderboard.hf.space/gradio_api/info', '-o', '/tmp/opencode/e135_gradio.json | 0 | 823 |
| 12 | ['curl', '-s', '-o', '/dev/null', '-w', 'HELM-front %{http_code} %{size_download}\\n', '--max-time', '30', 'https://crfm.stanford.edu/helm/'] | 0 | 433 |
| 13 | ['curl', '-s', '--max-time', '30', 'https://api.github.com/repos/stanford-crfm/helm'] | 0 | 869 |
| 14 | ['curl', '-s', '--max-time', '30', 'https://crfm.stanford.edu/helm/mmlu/v1.0.0/', '-o', '/dev/null', '-w', 'mmlu-page %{http_code} %{size_download}\\n | 0 | 272 |
| 15 | ['curl', '-s', '--max-time', '30', 'https://crfm.stanford.edu/helm/config.js'] | 0 | 347 |
| 16 | ['curl', '-s', '--max-time', '30', 'https://storage.googleapis.com/crfm-helm-public/home/benchmark_output/runs/v1.0.0/', '-o', '/dev/null', '-w', 'run | 0 | 1730 |
| 17 | ['curl', '-s', '--max-time', '60', 'https://storage.googleapis.com/crfm-helm-public/home/benchmark_output/benchmark_output/runs/v1.0.0/mmlu:model=open | 0 | 1638 |
| 18 | ['curl', '-s', '--max-time', '30', 'https://storage.googleapis.com/crfm-helm-public/home/benchmark_output/releases/v1.0.0/summary.json', '-o', '/tmp/o | 0 | 1710 |
| 19 | ['curl', '-s', '--max-time', '30', 'https://storage.googleapis.com/storage/v1/b/crfm-helm-public/o?prefix=home/benchmark_output/releases/&maxResults=1 | 0 | 1680 |
| 20 | ['curl', '-s', '--max-time', '30', 'https://storage.googleapis.com/storage/v1/b/crfm-helm-public/o?prefix=home/benchmark_output/&delimiter=/'] | 0 | 1637 |
| 21 | ['curl', '-s', '--max-time', '30', 'https://storage.googleapis.com/crfm-helm-public/lite/benchmark_output/releases/v1.0.0/summary.json', '-o', '/tmp/o | 0 | 1753 |
| 22 | ['curl', '-s', '--max-time', '60', 'https://storage.googleapis.com/crfm-helm-public/lite/benchmark_output/runs/v1.0.0/mmlu:subject=abstract_algebra,me | 0 | 1717 |
| 23 | ['curl', '-s', '--max-time', '60', 'https://storage.googleapis.com/crfm-helm-public/lite/benchmark_output/runs/v1.0.0/mmlu:subject=abstract_algebra,me | 0 | 2014 |
| 24 | ['curl', '-s', '--max-time', '60', 'https://storage.googleapis.com/crfm-helm-public/lite/benchmark_output/runs/v1.0.0/mmlu:subject=abstract_algebra,me | 0 | 1889 |
| 25 | ['curl', '-s', '--max-time', '60', 'https://storage.googleapis.com/crfm-helm-public/lite/benchmark_output/runs/v1.0.0/mmlu:subject=abstract_algebra,me | 0 | 1713 |
| 26 | ['python3', 'EXPERIMENTS/135-preflight-leaderboard-reach/recompute.py'] | 1 | 680 |
| 27 | ['python3', 'EXPERIMENTS/135-preflight-leaderboard-reach/recompute.py'] | 0 | 214 |
| 28 | ['python3', 'EXPERIMENTS/135-preflight-leaderboard-reach/reconcile.py'] | 0 | 133 |
| 29 | ['bash', '-c', 'curl -s --max-time 60 "https://crfm.stanford.edu/helm/v1.0.0/runs/mmlu:subject=abstract_algebra,method=multiple_choice_joint,model=01- | 0 | 739 |
| 30 | ['bash', '-c', 'head -c 400 /tmp/opencode/e15_helm_scenario_api.json 2>/dev/null; head -c 400 /tmp/opencode/e135_helm_scenario_api.json; echo; curl -s | 0 | 397 |
| 31 | ['bash', '-c', '\necho "--- C3: lmsys chatbot_arena_conversations dataset metadata (unauthenticated)"\ncurl -s --max-time 30 "https://huggingface.co/a | 0 | 1276 |
| 32 | ['bash', '-c', '\necho "--- C1: OLLM v2 gradio API on the canonical space host"\ncurl -sL --max-time 30 "https://huggingface.co/spaces/HuggingFaceH4/o | 0 | 1103 |
| 33 | ['python3', 'EXPERIMENTS/135-preflight-leaderboard-reach/completion_shapes.py'] | 0 | 109 |
| 39 | ['python3', 'EXPERIMENTS/135-preflight-leaderboard-reach/manifest_fetched.py'] | 0 | 985 |

## Integrity

| check | result |
|---|---|
| undeclared file changes | 1 |
| declared artifacts now missing | 0 |
| integrity errors | 0 |
| redactions applied to command output | 0 |
|   undeclared | EXPERIMENTS/135-preflight-leaderboard-reach/PROTOCOL.md |

## Timeline

| seq | time | kind | summary |
|---|---|---|---|
| 1 | 04:28:15 | session_start | Probe whether preflight R1 recomputation reaches leaderboard-published LLM benchmark numbers |
| 2 | 04:29:05 | command | $ curl -s -o /dev/null -w C1-space %{http_code} %{size_download}\n --max-time 30 https://huggingface.co/spaces/open-llm-leaderboard/open_llm_l |
| 3 | 04:29:07 | command | $ curl -s --max-time 30 https://huggingface.co/api/spaces/open-llm-leaderboard/open_llm_leaderboard |
| 4 | 04:29:11 | command | $ curl -s --max-time 30 https://huggingface.co/api/datasets?author=open-llm-leaderboard&limit=30 |
| 5 | 04:29:16 | command | $ curl -s --max-time 30 https://huggingface.co/api/datasets/open-llm-leaderboard/gpt2-details |
| 6 | 04:29:23 | command | $ curl -s --max-time 60 https://huggingface.co/datasets/open-llm-leaderboard/gpt2-details/resolve/main/gpt2/results_2024-06-04T15-21-52.173543 |
| 7 | 04:29:32 | command | $ curl -s --max-time 30 https://huggingface.co/api/datasets?author=open-llm-leaderboard&limit=100 |
| 8 | 04:29:41 | command | $ curl -s --max-time 30 https://huggingface.co/api/spaces/open-llm-leaderboard/open_llm_leaderboard |
| 9 | 04:29:55 | command | $ curl -s -o /dev/null -w %{http_code}\n --max-time 20 https://open-llm-leaderboard-open-llm-leaderboard.hf.space/gradio_api/info |
| 10 | 04:29:57 | command | $ curl -s -o /dev/null -w %{http_code}\n --max-time 20 https://open-llm-leaderboard.hf.space/gradio_api/info |
| 11 | 04:30:02 | command | $ curl -s --max-time 30 https://open-llm-leaderboard-open-llm-leaderboard.hf.space/gradio_api/info -o /tmp/opencode/e135_gradio.json |
| 12 | 04:30:35 | command | $ curl -s -o /dev/null -w HELM-front %{http_code} %{size_download}\n --max-time 30 https://crfm.stanford.edu/helm/ |
| 13 | 04:30:36 | command | $ curl -s --max-time 30 https://api.github.com/repos/stanford-crfm/helm |
| 14 | 04:30:41 | command | $ curl -s --max-time 30 https://crfm.stanford.edu/helm/mmlu/v1.0.0/ -o /dev/null -w mmlu-page %{http_code} %{size_download}\n |
| 15 | 04:30:46 | command | $ curl -s --max-time 30 https://crfm.stanford.edu/helm/config.js |
| 16 | 04:30:53 | command | $ curl -s --max-time 30 https://storage.googleapis.com/crfm-helm-public/home/benchmark_output/runs/v1.0.0/ -o /dev/null -w runs-dir %{http_cod |
| 17 | 04:30:56 | command | $ curl -s --max-time 60 https://storage.googleapis.com/crfm-helm-public/home/benchmark_output/benchmark_output/runs/v1.0.0/mmlu:model=openai__ |
| 18 | 04:31:07 | command | $ curl -s --max-time 30 https://storage.googleapis.com/crfm-helm-public/home/benchmark_output/releases/v1.0.0/summary.json -o /tmp/opencode/he |
| 19 | 04:31:15 | command | $ curl -s --max-time 30 https://storage.googleapis.com/storage/v1/b/crfm-helm-public/o?prefix=home/benchmark_output/releases/&maxResults=10 |
| 20 | 04:31:17 | command | $ curl -s --max-time 30 https://storage.googleapis.com/storage/v1/b/crfm-helm-public/o?prefix=home/benchmark_output/&delimiter=/ |
| 21 | 04:32:18 | command | $ curl -s --max-time 30 https://storage.googleapis.com/crfm-helm-public/lite/benchmark_output/releases/v1.0.0/summary.json -o /tmp/opencode/he |
| 22 | 04:32:37 | command | $ curl -s --max-time 60 https://storage.googleapis.com/crfm-helm-public/lite/benchmark_output/runs/v1.0.0/mmlu:subject=abstract_algebra,method |
| 23 | 04:32:40 | command | $ curl -s --max-time 60 https://storage.googleapis.com/crfm-helm-public/lite/benchmark_output/runs/v1.0.0/mmlu:subject=abstract_algebra,method |
| 24 | 04:32:43 | command | $ curl -s --max-time 60 https://storage.googleapis.com/crfm-helm-public/lite/benchmark_output/runs/v1.0.0/mmlu:subject=abstract_algebra,method |
| 25 | 04:32:46 | command | $ curl -s --max-time 60 https://storage.googleapis.com/crfm-helm-public/lite/benchmark_output/runs/v1.0.0/mmlu:subject=abstract_algebra,method |
| 26 | 04:39:07 | command | $ python3 EXPERIMENTS/135-preflight-leaderboard-reach/recompute.py |
| 27 | 04:39:25 | command | $ python3 EXPERIMENTS/135-preflight-leaderboard-reach/recompute.py |
| 28 | 04:40:20 | command | $ python3 EXPERIMENTS/135-preflight-leaderboard-reach/reconcile.py |
| 29 | 04:42:13 | command | $ bash -c curl -s --max-time 60 "https://crfm.stanford.edu/helm/v1.0.0/runs/mmlu:subject=abstract_algebra,method=multiple_choice_joint,model=0 |
| 30 | 04:42:22 | command | $ bash -c head -c 400 /tmp/opencode/e15_helm_scenario_api.json 2>/dev/null; head -c 400 /tmp/opencode/e135_helm_scenario_api.json; echo; curl |
| 31 | 04:44:55 | command | $ bash -c  echo "--- C3: lmsys chatbot_arena_conversations dataset metadata (unauthenticated)" curl -s --max-time 30 "https://huggingface.co/a |
| 32 | 04:45:12 | command | $ bash -c  echo "--- C1: OLLM v2 gradio API on the canonical space host" curl -sL --max-time 30 "https://huggingface.co/spaces/HuggingFaceH4/o |
| 33 | 04:46:08 | command | $ python3 EXPERIMENTS/135-preflight-leaderboard-reach/completion_shapes.py |
| 34 | 04:55:05 | artifact | wrote EXPERIMENTS/135-preflight-leaderboard-reach/RESULT.md |
| 35 | 04:55:07 | artifact | wrote EXPERIMENTS/135-preflight-leaderboard-reach/recompute.py |
| 36 | 04:55:08 | artifact | wrote EXPERIMENTS/135-preflight-leaderboard-reach/reconcile.py |
| 37 | 04:55:09 | artifact | wrote EXPERIMENTS/135-preflight-leaderboard-reach/completion_shapes.py |
| 38 | 04:55:11 | artifact | wrote STATE.md |
| 39 | 05:07:41 | command | $ python3 EXPERIMENTS/135-preflight-leaderboard-reach/manifest_fetched.py |
| 40 | 05:08:16 | artifact | wrote EXPERIMENTS/135-preflight-leaderboard-reach/manifest_fetched.py |
| 41 | 05:08:21 | artifact | wrote EXPERIMENTS/135-preflight-leaderboard-reach/fetched-manifest.json |
| 42 | 05:13:31 | unlogged_change | changed but never declared as an artifact: EXPERIMENTS/135-preflight-leaderboard-reach/PROTOCOL.md |
| 43 | 05:13:31 | doc_update | updated STATE.md |
| 44 | 05:13:31 | session_end | E135 probe completed (resumed an unfinished session on this VM). Question: does preflight's R1 recomputation reach the number a leaderboard publishes? |

## Reproduce this record

```bash
tools/origin session verify
cat sessions/2026-10-14-003-probe-whether-preflight-r1-recomputation/events.jsonl
```
