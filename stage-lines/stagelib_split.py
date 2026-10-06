"""Cut change runs into the smallest hunks `git apply` will take."""

from stagelib_change import Change


def _split_run(group, group_old, group_new):
    """Cut one maximal run of +/- lines into the smallest hunks git will take.

    git writes a hunk's removed lines first and its added lines after, so a run
    of `n` removes followed by `m` adds means: the first `min(n, m)` removes pair
    with the first `min(n, m)` adds, line for line. Cutting there is exactly
    what `git add -p`'s `s` command does, and each piece is a hunk `git apply`
    will take on its own. Any surplus on one side is a pure insertion or a pure
    deletion and cannot be cut further without inventing context.

    A side that consumes no lines still needs a start number: git writes the
    count of the *other* side and anchors the empty side at the line the content
    sits next to. ``@@ -9,0 +10,1 @@`` is an insertion after old line 9, and
    ``@@ -3,2 +2,0 @@`` is a deletion whose following line is new line 2.
    """
    content = [l for l in group if l[:1] in ("+", "-")]
    if not content:
        return []
    marks = {}
    seen = 0
    for line in group:
        if line.startswith("\\"):
            if seen:
                marks[seen - 1] = marks.get(seen - 1, []) + [line]
            continue
        seen += 1

    def take(idxs, old_at, new_at):
        body = []
        nold = nnew = 0
        for i in idxs:
            body.append(content[i])
            body.extend(marks.get(i, []))
            if content[i].startswith("-"):
                nold += 1
            else:
                nnew += 1
        return Change(old_start=group_old + old_at, old_lines=nold,
                      new_start=group_new + new_at, new_lines=nnew,
                      body=body)

    nrem = sum(1 for l in content if l.startswith("-"))
    nadd = len(content) - nrem
    pairs = min(nrem, nadd)
    out = []
    for j in range(pairs):
        # remove j pairs with add j, and each pair is a hunk on its own
        out.append(take([j, nrem + j], j, j))
    if nrem > nadd:
        # The surplus is a run of consecutive deletions, and it stays one change.
        # Each of them is addressed by the same line -- the line whose content moved
        # up into the gap -- so there is no coordinate that names one of them alone.
        # Splitting them would not add reach: every part of the run would answer to
        # the same address and be selected together anyway.
        out.append(take(list(range(nadd, nrem)), nadd, nadd))
    elif nadd > nrem:
        # The surplus is a run of consecutive insertions, and each of them *is* its
        # own line in the file as it reads now, so each is addressable. git apply
        # takes them one at a time once the counts say so -- `@@ -3,0 +4,1 @@` then
        # `@@ -3,0 +5,1 @@` over what git prints as `@@ -3,0 +4,2 @@`, verified in
        # EXPERIMENTS/038-staging-prior-art. Keeping them in one hunk meant asking
        # for line 4 of a two-line insertion staged both and still exited 0.
        #
        # Two different offsets, and conflating them picks the wrong line out of the
        # run. The surplus adds start at content index `nrem + pairs` -- the `nrem`
        # removes come first, then the `pairs` adds already paired with them -- while
        # the k-th of them sits `pairs + k` lines into the new file. In `@@ -4 +4,3 @@`
        # over `-d +X +Y +Z` that gives X paired with d, then Y at +5 and Z at +6.
        for k in range(nadd - nrem):
            out.append(take([nrem + pairs + k], 0, pairs + k))
    return out
