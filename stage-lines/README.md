<!-- origin-meta
owner: RELEASE-MANIFEST.md
status: draft
last-verified: 2026-10-06
-->

# stg — stage part of a file by line number, without a terminal

`git add -p` can only be driven by a person at a TTY. So can every other interactive
selector in a developer's toolbox, which is why none of them are reachable from a script, a
CI job, an editor keybinding, or an AI coding agent.

`stg` gives the same operation a scriptable interface, addressed in the coordinates you are
already looking at: the line numbers of the file.

```
stg list                          every stageable change, as path:line
stg list --json                   the same, for a program
stg stage src/app.py:42           stage the change on line 42
stg stage src/app.py:42-51        stage every change in lines 42..51
stg stage src/app.py:42,51        two lines in one file
stg stage src/app.py:42 docs/a:8  several files at once
stg unstage src/app.py:42         the mirror, addressed by index line
```

Exit status: `0` nothing matched, `1` something did, `2` usage or git error. The `2` is the
point — **if it did not stage what you asked for, it says so instead of exiting 0.**

## Why it exists

`git add -p`'s `s` splits only at context boundaries, so two adjacent modified lines are one
change pair spanning both, and its header names the first. Line 2 of that pair is not
reachable through the prompt except through the `e` editor, which opens a patch in
`$EDITOR`.

```
$ git diff -U0
@@ -1,2 +1,2 @@
-a
-b
+A
+B
```

`stg stage f:2` stages `@@ -2 +2 @@ -b +B` and nothing else.

There is no `file:line` in git (`git add f:2` is a pathspec error), and the documented
workaround — slicing a hunk out of `git diff` and applying it — needs the file header
re-typed by hand and `--unidiff-zero`, and silently stages nothing if you get the line
numbers wrong.

Evidence, including what a 133-line pty driver achieves with the same goal:
[`EXPERIMENTS/037-line-staging/`](../EXPERIMENTS/037-line-staging/README.md).

## Install

No dependencies, no build step, standard library only, Python 3.6+.

```
git clone <this repo> && cd stage-lines
./stg list          # or: python3 stg list
```

Symlink it onto your `PATH` as `stg` if you want the bare name.

## What it does not do

- **A multi-line insertion or deletion is one change.** Half of a two-line append is not a
  hunk `git apply` can express without inventing context, so neither is it a thing `stg`
  will pretend to stage. Two adjacent *modifications* do split, because each is its own
  line pair.
- **Binary files.** Refused, with a message pointing at plain `git add`.
- **Renames and mode changes.** Not implemented; run `git add` for those.
- **Untracked files.** Listed, but not partially stageable — git has no index entry yet.
- It stages **un**staged changes by working-tree line, and unstages **s**taged changes by
  index line, because those are the two files you are reading when you want each.

## Tests

```
python3 test_stg.py
```

28 cases. Each builds a real git repository and asserts against real `git diff --cached`
output — no mocks, because the claim is that the index it leaves is a real index git will
commit. Covers single and multiple changes, ranges, multiple files, adjacent modifications,
multi-line insertions and deletions, deletions at the top and end of a file, files with no
trailing newline, CRLF, tabs, long lines, binary refusal, untracked files, `--json`,
out-of-range lines, and a stage/unstage round trip.

## Status

An experimental prototype. It is not released, and nothing here has been measured for
adoption — see the experiment record for what is and is not established.
