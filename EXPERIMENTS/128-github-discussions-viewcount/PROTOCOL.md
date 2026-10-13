<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-12
-->

# E128 — Fresh observation: view-count principle on GitHub Discussions

## Question

Does the view-count principle generalize to GitHub Discussions? Specifically, do need-related discussions (questions, help requests, debugging, troubleshooting) in technical repositories have systematically higher engagement (reactions, comments) than random discussions?

## Why this matters

The view-count principle has been validated on package registries (PyPI, NPM, NuGet, Hex.pm, Packagist, RubyGems), container registries (Docker Hub - mixed), ML model registries (Hugging Face - fail), Q&A forums (Discourse, Stack Exchange), code repositories (GitHub - harvest artifact), and IDE marketplaces (VS Code - weak effect δ=0.158).

GitHub Discussions is a fundamentally different platform structure: discussions attached to code repositories on a code hosting platform, with categories (Q&A, Ideas, General, Announcements), reactions (👍, 👎, 😄, 🎉, 🤔, ❤️, 🚀, 👀), and comments. This tests the principle on a platform that combines code hosting with community discussion.

## Population

GitHub Discussions from popular technical repositories, accessed via public REST API:
`https://api.github.com/repos/{owner}/{repo}/discussions?per_page=100&page={page}`

Repositories to sample:
- vercel/next.js (web framework)
- facebook/react (UI library)
- tensorflow/tensorflow (ML framework)
- pytorch/pytorch (ML framework)
- kubernetes/kubernetes (orchestration)
- rust-lang/rust (language)
- golang/go (language)
- nodejs/node (runtime)
- denoland/deno (runtime)
- ansible/ansible (automation)
- hashicorp/terraform (IaC)
- prometheus/prometheus (monitoring)
- grafana/grafana (visualization)
- elastic/elasticsearch (search)
- redis/redis (database)
- postgresql/postgresql (database)
- mongodb/mongo (database)
- apache/kafka (streaming)
- apache/spark (analytics)
- hashicorp/consul (service mesh)

Need-related patterns (declared before measurement, anchored word-boundary):
- Question forms: how do, how can, how to, why does, what is, how does, how is, how would, how will, how could, can you, could you, would you, can anyone, could anyone, would anyone, does anyone, do you, is there, are there
- Problem statements: fix, debug, troubleshoot, error, issue, problem, bug, crash, fail, exception, not working, cannot, stuck, help
- Direct requests: help me, please help, need help, advise, advice, recommend, suggest, guidance
- Technical: lint, format, refactor, test, deploy, ci, cd, git, docker, kubernetes, api, database, sql, nosql

Excluded patterns (hard exclusion):
- Announcements: announce, release, launch, introducing, showcase, show off, my new, welcome, update, version
- Meta: meta, moderator, mod post, rules, FAQ, wiki, guideline, contributing
- Showcase: portfolio, project, built, created, made, demo, example, tutorial, guide, learning, practice, exercise
- Hiring: hiring, job, career, salary, interview, resume
- Off-topic: meme, joke, fun, off topic, watercooler, random

## Gates (declared before measurement)

| Gate | Description | Threshold |
|------|-------------|-----------|
| G1 | Arrival metric coverage | ≥95% have reactions.total_count > 0 OR comments > 0 |
| G2 | Classifier coverage | ≥60% floor AND need fraction ≥5% |
| G3 | Separation (Cliff's delta) | δ > 0.2 AND p < 0.05 (need vs random engagement) |
| G4 | Need-related active rate | ≥50% have > 10 total engagement (reactions + comments) |

## Kill gate

If G3 fails, the principle does not generalize to this domain. This maps the principle's boundary.

## Method

1. Harvest discussions from 20 technical repositories (100 per repo = 2000 total)
2. Classify by patterns in title + body
3. Measure engagement = reactions.total_count + comments
4. Matched harvest: pool classified, sort by engagement desc, split need/random
5. Compute Cliff's delta and Mann-Whitney U test

## Prior art

GitHub Discussions launched in 2020. Major repos have thousands of discussions. No prior view-count analysis known.

## Uncertainty

- Reactions may reflect agreement/entertainment, not need
- Discussions are repo-specific (not cross-repo discovery)
- Categories mix Q&A with Ideas/Announcements
- Popular repos have high baseline engagement

## Artifacts

| File | What it is |
|------|------------|
| `PROTOCOL.md` | This file |
| `harvest.py` | Harvesting script |
| `measure_github_discussions.py` | Measurement script |
| `raw_data.jsonl` | Raw harvested data |
| `classified_data.jsonl` | Classified discussions |
| `results.json` | Gate results |
| `RESULT.md` | Analysis and conclusion |
