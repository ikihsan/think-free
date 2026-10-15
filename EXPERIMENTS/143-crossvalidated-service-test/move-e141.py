#!/usr/bin/env python3
"""One-off: insert the closed E141 entry into STATE-history.md (newest first).

The E141 block was already removed from STATE.md. We recover it from the
committed STATE.md (HEAD) and insert it at the top of the history content,
right after the description block and before the first existing entry.
"""
import subprocess
os_chdir = '/home/ubuntu/think-free'
import os
os.chdir(os_chdir)

# Get committed STATE.md and extract the E141 block
committed = subprocess.check_output(['git', 'show', 'HEAD:STATE.md']).decode()
start = committed.index("**E141 completed (2026-10-15):")
end = committed.index("**E142 completed (2026-10-15):")
e141_block = committed[start:end].rstrip() + "\n"

with open('STATE-history.md') as f:
    hist = f.read()

# Insert after the description, before the first content entry.
# The description ends with the STATE-history-2.md link line, then blank, then content.
anchor = "is in [`STATE-history-2.md`](STATE-history-2.md)."
i = hist.index(anchor) + len(anchor)
# hist[i:] starts with "\n\n" then the first entry. Insert the E141 block there.
rest = hist[i:]
# rest begins with leading newlines; keep one blank line separator
new_hist = hist[:i] + "\n\n" + e141_block + rest.lstrip('\n')
# ensure exactly one blank line between E141 block and next entry
new_hist = new_hist.replace(e141_block + "\n\n\n", e141_block + "\n\n")

with open('STATE-history.md', 'w') as f:
    f.write(new_hist)

print("STATE-history.md lines:", new_hist.count('\n'))
print("E141 block lines:", e141_block.count('\n'))
