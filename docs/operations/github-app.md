<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-03
-->

# GitHub App design

**Status: design, not implemented.** No GitHub App exists yet. Nothing in this
repository depends on one. This document exists so that creating it later is a
known, reviewable step rather than an improvisation.

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

Repository permissions, per the App's actual need:

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

## What a PR from a VM must contain

- The task id and the exact verification command with its exit code.
- A link to the session report, which contains the command log.
- The outcome: `worked`, `partial`, or `failed`.
- Anything the run could not do, stated plainly.
- No claim of user testing or adoption, because an automated run has none.

A PR that omits the verification command is not reviewable and should be closed
without discussion.

## Implementation checklist

Not yet done, in dependency order:

- [ ] Create the App in repository settings with the permissions above.
- [ ] Install it on exactly the repositories intended.
- [ ] Generate the private key; store it on the runner with `0600`.
- [ ] Verify the key never appears in `sessions/`, in `doctor.json`, or in any
      log: run a command that uses it and check with
      `tools/origin skills check` and `origin session verify`.
- [ ] Add a credential-presence check to `doctor` for the App (presence only).
- [ ] Implement claim-and-run against one repository.
- [ ] Implement PR creation with the contents above.
- [ ] Add a workflow that reports the task's verification status.
- [ ] Write a rotation procedure and a revocation procedure.

Until the key-handling verification passes, the App must not be used on a
machine holding other credentials.

## Open questions

- Single repository or several? The design assumes one.
- Poll interval or push-based trigger? Undecided; polling is simpler and wastes
  quota.
- Should PR creation require a human to press a button, or be automatic for
  tasks marked safe? Automatic opens the door to spam and should be opt-in per
  task, never global.
- What is the retention policy for session logs produced by fleet runs?