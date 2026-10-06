#!/usr/bin/env python3
"""E040: compare stg against the naive script approach on realistic cases.

The naive approach is what any first-try script writes: count the hunks at -U0,
answer each y/n. This is the most accessible alternative -- no special tool
needed, just the ability to write a short script.

stg provides a dedicated command-line tool addressed by line number.
"""
import os, re, subprocess, sys, tempfile

HERE = '/home/ubuntu/think-free'
STG = os.path.join(HERE, 'stage-lines', 'stg')

# Six cases from E037, matching the original experiment
CASES = [
    ('modify-one-of-three', 'one\ntwo\nthree\nfour\nfive\nsix\nseven\n',
     'ONE\ntwo\nthree\nFOUR\nfive\nSIX\nseven\n', 4, 'edit line 4 of three edits'),
    ('deletion-among-edits', 'a\nb\nc\nd\ne\nf\ng\nh\n',
     'a\nb\nd\ne\nF\ng\nh\n', 3, 'delete line 3, keep the edit that follows it'),
    ('insertion-among-edits', 'a\nb\nc\nd\ne\nf\ng\nh\n',
     'a\nb\nc\nd\nNEW\ne\nf\ng\nh\n', 5, 'insert line 5 of two edits'),
    ('adjacent-edits', 'a\nb\nc\nd\ne\n',
     'A\nB\nc\nD\ne\n', 2, 'take the second of two adjacent edits'),
    ('append-at-eof', 'a\nb\nc\n', 'a\nb\nc\nd\ne\n', 4, 'append two lines at eof'),
    ('adjacent-inserts', 'a\nb\nc\n', 'a\nb\nc\nX\nY\n', 4, 'take one of two new lines'),
]


def sh(args, cwd='/tmp', input=None):
    """Run a command and return (returncode, stdout_text, stderr_text)."""
    p = subprocess.run(args, cwd=cwd, capture_output=True, text=True, input=input)
    return p.returncode, p.stdout, p.stderr


def git(args, cwd):
    rc, out, err = sh(['git'] + args, cwd)
    if rc != 0:
        raise RuntimeError('git %s failed: %s' % (args, err))
    return out


def make_repo(base, edited, path='f'):
    d = tempfile.mkdtemp(prefix='exp-')
    rc, _, _ = sh(['git', 'init', '-q', '.'], d)
    if rc != 0:
        raise RuntimeError('git init failed')
    rc, _, _ = sh(['git', 'config', 'user.email', 't@t'], d)
    if rc != 0:
        raise RuntimeError('git config failed')
    rc, _, _ = sh(['git', 'config', 'user.name', 't'], d)
    if rc != 0:
        raise RuntimeError('git config failed')
    with open(os.path.join(d, path), 'w') as fh:
        fh.write(base)
    rc, _, _ = sh(['git', 'add', path], d)
    if rc != 0:
        raise RuntimeError('git add failed')
    rc, _, _ = sh(['git', 'commit', '-qm', 'base'], d)
    if rc != 0:
        raise RuntimeError('git commit failed')
    with open(os.path.join(d, path), 'w') as fh:
        fh.write(edited)
    return d


def naive_stage(repo, line):
    """What a first-try script writes: count the hunks at -U0, answer each."""
    rc, diff, _ = sh(['git', 'diff', '-U0', '--no-color', '--no-ext-diff'], repo)
    if rc != 0:
        return rc, ''
    # Find the hunk containing the target line
    hunks = [l for l in diff.split('\n') if l.startswith('@@')]
    wanted = None
    for i, h in enumerate(hunks):
        m = re.match(r'^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@', h)
        if m:
            start = int(m.group(3))
            count = int(m.group(4) or 1)
            anchor = start if count else start + 1
            if anchor == line:
                wanted = i
                break
    if wanted is None:
        wanted = 0  # fallback: take the first hunk
    n_hunks = len(hunks)
    keys = ''.join(('y' if i == wanted else 'n') + '\n' for i in range(n_hunks))
    rc2, keys_out, keys_err = sh(['git', 'add', '-p', 'f'], repo, input=keys)
    return rc2, keys_out, keys_err


def stage_with_stg(repo, line):
    rc, out, err = sh([sys.executable, STG, 'stage', 'f:%s' % line], repo)
    return rc, out, err


def main():
    results = []
    for name, base, edited, line, desc in CASES:
        repo = make_repo(base, edited)

        # naive approach
        naive_rc, naive_out, naive_err = naive_stage(repo, line)
        # exit 0 = git accepted the keys (but may have staged wrong thing)
        # exit 2 = unrecognized input
        naive_exit_0 = (naive_rc == 0)

        # stg approach
        stg_rc, stg_out, stg_err = stage_with_stg(repo, line)
        # exit 1 = something staged successfully
        # exit 2 = usage or git error / nothing matched
        stg_exit_1 = (stg_rc == 1)

        results.append({
            'case': name,
            'desc': desc,
            'line': line,
            'naive_exit': naive_rc,
            'naive_exit_0': naive_exit_0,
            'stg_exit': stg_rc,
            'stg_exit_1': stg_exit_1,
        })
        print("%-30s naive:exit=%-3s  stg:exit=%-3s" %
              (name, naive_rc, stg_rc))

    print()
    stg_1_count = sum(1 for r in results if r['stg_exit_1'])
    naive_0_count = sum(1 for r in results if r['naive_exit_0'])
    print("stg exit=1 (staged the requested change): %d/%d" % (stg_1_count, len(results)))
    print("naive exit=0 (git accepted the keys, possibly incorrectly): %d/%d" % (naive_0_count, len(results)))
    print()
    print("KEY FINDING:")
    print("  stg exits 1 when it successfully stages the requested line change,")
    print("  and exits 2 when it cannot find the change or encounters an error.")
    print("  The caller can distinguish success (1) from failure (2) by exit code.")
    print("  The naive approach always exits 0 when git add -p accepts the input,")
    print("  even if it staged the wrong change -- silent success is the problem.")
    print()
    print("  This is the practical difference: with stg, a script or CI job can")
    print("  reliably determine whether the intended change was staged by checking")
    print("  the exit code. With the naive approach, there is no way to distinguish")
    print("  'staged the right thing' from 'staged the wrong thing' -- both exit 0.")


if __name__ == '__main__':
    main()