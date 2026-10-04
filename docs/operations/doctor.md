<!-- origin-meta
owner: docs/INDEX.md
status: active
last-verified: 2026-10-04
-->

# Environment doctor

`tools/origin doctor` answers one question: **can this machine do the work a
task requires?** It runs before a VM picks up a task, so a limitation is
recorded as a limitation instead of turning up later as a mystery failure.

Raw results go to `.origin/doctor.json`, which is gitignored. `--json` prints
them; `--offline` skips every network call.

It is deliberately **not** a CI gate. It probes the network and the machine, so
running it in CI would make the build flaky for reasons unrelated to the change
(`operations/ci.md`).

## What it reports

| Field | What it actually reads |
|---|---|
| `platform`, `python`, `cpu_count` | The running interpreter and `os.cpu_count()` |
| `memory`, `disk free` | `/proc/meminfo` and `shutil.disk_usage` on shared hardware, so they fluctuate |
| `tool *` | `--version` of each of `python3`, `git`, `node`, `rustc`, `gcc` |
| `versions *` | the same versions compared against the exercised-version records — see below |
| `git` | head, branch, clean, porcelain paths |
| `credentials_present` | **environment-variable presence only**, four names |
| an environment token | `GH_TOKEN` or `GITHUB_TOKEN` alone makes the verdict `broken`, not `unavailable`: it *is* a credential mechanism, and git cannot obtain one from it unaided. That is why the test fixture clears both rather than inheriting whatever the runner exported |
| `push_credential` | the mechanism git would actually use — see below |
| `scheduler` | `crontab`, `systemctl`, whether `systemd --user` is running |
| `network` | one HTTP status per probe URL |

## What the versions mean

Added in T-0033. `doctor` used to print the `tool *` versions it found and stop,
while two records state what the suite has actually run on —
[`../../tests/git-versions.json`](../../tests/git-versions.json) and
[`../../tests/python-versions.json`](../../tests/python-versions.json). A VM on
Python 3.15 was therefore indistinguishable in the report from one on 3.8.10, and
finding out otherwise meant opening a JSON file by hand.

The `versions *` lines now answer it, and they name the record they consulted:

```
versions python3   3.8.10     exercised (tests/python-versions.json: 3.8.10); full suite green (392 tests at T-0034); run on instance-20260717-0947, git 2.25.1
versions git       2.25.1     exercised (tests/git-versions.json: 2.25.1); full suite green (392 tests at T-0034); run on instance-20260717-0944 and instance-20260717-0947
versions rustc     (none)     no record - no record covers this tool
```

| State | What it means |
|---|---|
| `exercised (<record>: <entry>)` | An entry names this version. The entry's own `scope` follows, because a version that ran an older suite is not evidence about the current one, and then the machine or runner it ran on |
| `NOT exercised - <detail>` | The record was read and does not name this version. This is the state worth acting on |
| `record unreadable - <detail>` | The record is missing or does not parse. **Not** the same claim as the line above: this is "we could not look" |
| `no record - <detail>` | No record covers this tool at all. `node`, `rustc` and `gcc` are probed and are not covered by any suite record, and saying so is more honest than leaving them out |

**Ceilings, stated rather than implied.** `exercised` means a run happened, not
that the version is supported: the entry's `scope` is the honest wording and it
travels with the verdict. Matching is by dotted prefix, longest entry first,
because the records mix patch-level entries (`3.8.10`) with minor-level ones
(`3.12` and every other CI row — their run logs need admin rights) and a VM on
`3.12.7` must find them. The three-way distinction is the load-bearing part: a
comparison that cannot tell "we looked and it is not there" from "we could not
look" reports a confident answer in both cases, which is the failure T-0025 found
in this very report (`DECISIONS-GATING.md` D025, D030).

**Which machine `exercised` refers to, as of T-0034.** One record now covers two
environments per minor version — a portable CPython build on a VM, and a CI
matrix row — so a patch-level entry can shadow the minor-level one when they
happen to name the same version. `doctor` therefore reports the matched entry's
own `where` after its scope. Without it, a VM reading `exercised` would be
reading a claim about a runner it has never seen; the line still means "an entry
names your version", and now says which entry.

## The push credential

Added in T-0025. Before it, `doctor` read four environment variables and
nothing else, so it printed `credentials     none present` on three different
machines: one whose pushes worked, one whose helper pointed at a file `/tmp` had
taken, and one with no credential at all. That is a report of a property never
inspected, which `DECISIONS.md` D025 forbids.

| Field | What it reads |
|---|---|
| `remote` | the first remote's URL with any userinfo stripped, so the value is safe to record |
| `helpers` | every `credential.helper`, each classified `builtin`, `shell`, or `program`; a program carries its `exists`, `executable`, `mode`, and `outside_home` |
| `app` | key and id files under `~/.config/github-app` by path, mode, and byte count |
| `functional` | whether `git credential fill` obtained a **non-empty** password |
| `verdict` | `configured`, `broken`, or `unavailable` |
| `warnings` | what is wrong with each of the above, in words |

### What the verdict means, and what it does not

| Verdict | Means |
|---|---|
| `configured` | A mechanism is present and git can obtain a credential from it |
| `broken` | A mechanism is configured and does not work, or git could not obtain one |
| `unavailable` | No mechanism is configured at all |

**`configured` does not mean the credential can push**, and says nothing about
what it is permitted to do. Proving write authorisation needs either a write to
the remote or the App's settings page, and
[`github-app.md`](github-app.md) records that nobody here can read the latter.

Absence and breakage are different states on purpose. The first implementation
reported a fresh VM with no credential as `broken`, which is the incident that
cost this fleet a push and would have sent the next agent hunting a helper that
was never configured.

### Two designs that looked right and were not

| Design | Why it fails |
|---|---|
| `git ls-remote <remote>` to prove a credential | `observed` 2026-10-03: this remote is public, so `ls-remote` exits 0 with no credential at all. A gate built on it cannot fail — `FAILURES.md` F010 with extra steps |
| Listing the helper files | `instance-20260717-0947`'s helper survived the `/tmp` clear; the script it invoked did not. A report built from listings says `configured` on the machine that cannot push |

`git credential fill` is the probe that discriminates: exit 0 with the real
helper, 128 without, and git's own complaint differs between "the helper is
gone" and "nothing is configured".

### No value is ever recorded

`git credential fill` writes a live token to stdout. `tools/originlib/pushprobe.py`
captures it, reduces it to a boolean, and returns the exit code, that boolean,
and one line of git's complaint. Key files are reported by path, mode, and size
only, which extends the presence-only rule
[`../policy/permissions-and-safety.md`](../policy/permissions-and-safety.md)
already sets for environment tokens.
`tests/test_pushcred_safety.py` asserts the token is absent from the collected
report, the summary, `doctor.json`, and stdout.

### Offline

`--offline` skips the probe and says so (`functional.reason` is `offline`), and
the verdict then rests on the mechanism alone. A skipped probe is never reported
as a missing credential: "untested" and "absent" are different answers.

## A real defect this found on the VM that wrote it

`instance-20260717-0944`'s credential helper — mode `0700`, working, and
correctly reported by nothing — invoked `/tmp/github-app-jwt.sh`. `/tmp` is
cleared on reboot. The same dependency had already cost
`instance-20260717-0947` every push.

The warning names it before it breaks. The repair on 2026-10-04 moved the JWT
generator to `~/.config/github-app/jwt.sh`, repointed the helper, and then
**deleted `/tmp/github-app-jwt.sh`** — after which `git credential fill` still
exits 0 and the warning is gone. The dependency disappeared because the helper
changed, not because the check stopped looking.

`~/.config/github-app/get-token.py` on that VM returns HTTP 401 and is not the
generator the helper uses. It was left in place: it is not this repository's to
delete, and a broken credential artifact is worth recording rather than hiding.

## Writing a probe that cannot fail

Every probe here was falsified against the defect's own bytes before being
trusted (D025). The procedure, reusable:

1. Name the environments that must be distinguishable — a working credential, the
   recorded failure, and no credential.
2. Run the **existing** report on all three and record that it cannot tell them
   apart. One distinct output for three distinct realities is the defect.
3. Only then implement, and require one distinct output per environment.
4. A control that cannot fail is reported as unfired, not as passed (D024).

The harness must also be unable to touch the machine: an early version of this
one passed `Path.home()` as a sandbox HOME and overwrote this VM's real
`~/.gitconfig` (`FAILURES.md` F016).