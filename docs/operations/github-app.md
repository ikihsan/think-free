<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-03
-->

# GitHub App

**Status: one App exists and authenticates every push.** The design below was
written before it existed and has **never been checked against the App that was
actually configured** — its least-privilege table is an intention, not a
verification. Read the two sections apart.

| Claim | Evidence |
|---|---|
| An App installation pushes to this repository | `observed`: 123 of 133 commits are authored `Ihsan Ai Server Bot <ihsan-ai-server-bot[bot]@users.noreply.github.com>`, and `[bot]` is the suffix GitHub gives an App identity rather than a user. Pushes fail without it (D018) |
| Its identity is durable across reboots | `observed`: App id `5173845`, recorded in D018; the private key and a JWT generator live under `~/.config/github-app/`, not `/tmp` |
| Its **permissions** are least-privilege | **Unverified.** Nothing in this repository can read an App's permission set. Assume the table below describes intent until someone reads the App's settings |
| Its **installation scope** is one repository | **Unverified** beyond this repository. The remote here is one repository; other installations are not observable from here |
| Key material never reaches the record | `observed` 2026-10-03: 111 files under `sessions/` and `.origin/doctor.json` carry no secret shape. `doctor` now also runs `git credential fill`, whose output is discarded: `tests/test_pushcred_safety.py` asserts the token is absent from the report, the summary, `doctor.json`, and stdout |

Safety rules that constrain any implementation:
[`../policy/permissions-and-safety.md`](../policy/permissions-and-safety.md).

## What the App is for

One thing: letting an authorised machine turn a merged, reviewed change into
work on a VM, and to report the result back as a pull request. It is not an
agent with repository write access of its own accord.

If the App can post a comment, it can also be made to post anything. Its
authority must therefore be narrow enough that the worst outcome of a
misconfigured workflow is a pull request that a human declines to merge.

## Least-privilege permissions

Repository permissions, per the App's actual need. **This table has not been
compared with the App's real settings**; it is the design the App should be
checked against, and that check is still outstanding.

| Permission | Level | Why |
|---|---|---|
| Contents | Read and write | Push a task branch, open a pull request |
| Pull requests | Read and write | Open and update the result PR |
| Issues | Read and write | Report failures as issues |
| Metadata | Read-only | Mandatory; identifies the repository |
| Actions | Read-only | Read workflow runs, if a workflow reports status |
| Workflows | **None** | Must not modify CI definitions |
| Administration | **None** | Not needed for any intended operation |
| Secrets | **None** | Must never read repository or environment secrets |
| Pages, Deployments, Environments | **None** | Not needed |

Account permissions: **none**. The App must not be able to read or write
anything outside the repositories it is installed on.

Installation: **only on the repositories that need it**, not "all repositories".
One installation on one repository is the configuration that makes an incident
small.

## Authentication

A GitHub App authenticates with a private key. Consequences, all of which are
non-negotiable:

- The private key lives **only on the machine that needs it**, in a file with
  `0600` permissions, readable by that machine's user and nobody else.
- It is **never** committed, never written into `sessions/`, never logged, and
  never passed as a command-line argument where it lands in shell history or in
  the process list.
- `tools/origin` does not read, store, or transmit it. If a future tool needs it,
  the tool reads it at the moment of use and never copies it.
- Rotation is routine. If a key may have been exposed, rotate first and remove
  it second, per `../policy/permissions-and-safety.md`.
- Prefer a fine-grained personal access token or an SSH deploy key for a single
  machine if the App's multi-repository features are not needed. Least privilege
  argues for the simplest credential that works.

## Threat model

| Threat | Mitigation |
|---|---|
| Leaked key | `0600` on one machine; routine rotation; presence-only credential checks |
| Prompt injection from an issue or PR body | Retrieved content is data, never instructions. No App action may be triggered by issue text alone |
| A compromised VM acting outside its task | Task claim bounds the work; verification bounds completion; the App only opens PRs |
| A merged malicious change | The App proposes; a human merges. Never auto-merge |
| Runaway resource use | `doctor` reports limits; quotas are a per-machine policy decision, currently unimplemented |
| Silent divergence between VMs | One file per task, one directory per session; generated indexes regenerate after merge |

## Interaction with git

The simplest correct mechanism needs no App at all: an agent with push access
opens a branch and a pull request using git over SSH or HTTPS. The App earns its
keep only when something must happen **without a human present**:

1. a human merges a task definition or a scheduled trigger fires;
2. a machine claims the task and runs it;
3. the machine pushes a branch and opens a PR describing what it did;
4. a human reads the session report linked from the PR and merges or rejects.

Steps 2 and 3 are the only ones the App performs.

**Where the credential must live.** The helper and everything it invokes belong
under `~/.config/github-app/`. A generator under `/tmp` works until `/tmp` is
cleared, and `STATE.md` records that this cost `instance-20260717-0947` a day of
pushes. `doctor` reports such a dependency before it fails; see
[`doctor.md`](doctor.md).

## What a PR from a VM must contain

- The task id and the exact verification command with its exit code.
- A link to the session report, which contains the command log.
- The outcome: `worked`, `partial`, or `failed`.
- Anything the run could not do, stated plainly.
- No claim of user testing or adoption, because an automated run has none.

A PR that omits the verification command is not reviewable and should be closed
without discussion.

## Implementation checklist

Ticked only where this repository can show it happened. Everything about the
App's own settings stays open, because an agent cannot observe them.

- [x] Create the App in repository settings with the permissions above.
      **Existence** observed through bot authorship; the permission set is not.
- [x] Install it on `ikihsan/think-free`. Installed elsewhere is not observable.
- [x] Generate the private key; store it on the runner with `0600`. One key on
      `instance-20260717-0944` was found at `0644` inside a `0700` directory and
      repaired on 2026-10-03 (T-0023); the file mode is the requirement, not the
      enclosing directory.
- [x] Verify the key never appears in `sessions/`, in `doctor.json`, or in any
      log: 111 files under `sessions/` and `.origin/doctor.json` carry no secret
      shape (T-0023). This is the check that had to pass before the App was used
      alongside other credentials, and it passes.
- [ ] Compare the App's real permissions against the table above. **The largest
      open item on this page.**
- [x] Add a credential-presence check to `doctor` for the App (presence only).
      T-0025: `doctor` now reports the configured `credential.helper`, whether each
      named helper exists and is executable, App key files by path and mode, and
      whether `git credential fill` obtains a credential — under the key name
      `push_credential`. See [`doctor.md`](doctor.md) for the contract and its
      ceilings. Values are never read, printed, or written. It found a live
      defect on `instance-20260717-0944`: the helper was intact but invoked
      `/tmp/github-app-jwt.sh`, one `/tmp` clear from failing, exactly as
      `instance-20260717-0947` had been.
- [ ] Implement claim-and-run against one repository. Tasks are claimed and the
      claim is pushed today, but by an interactive agent using the App's
      credential, not by the App reacting to an event.
- [ ] Implement PR creation with the contents below. Branches are pushed
      directly to `research/origin`; no VM opens a pull request.
- [ ] Add a workflow that reports the task's verification status. CI reports
      branch status; nothing reports *per task*.
- [ ] Write a rotation procedure and a revocation procedure.

## Open questions

- Do the App's real permissions match the table above? Nothing here answers it.
- Single repository or several? The design assumes one; only this one is
  observable.
- Poll interval or push-based trigger? Undecided; polling is simpler and wastes
  quota.
- Should PR creation require a human to press a button, or be automatic for
  tasks marked safe? Automatic opens the door to spam and should be opt-in per
  task, never global.
- What is the retention policy for session logs produced by fleet runs?