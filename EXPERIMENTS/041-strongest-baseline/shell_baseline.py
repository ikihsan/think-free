"""Strongest shell baseline for line-addressable staging.

Parses git diff -U0, splits adjacent changes per-line (pairing removes with adds),
selects the hunk covering the requested working-tree line, applies with git apply.
"""
import os
import re
import subprocess


class ShellBaseline:
    def __init__(self):
        pass

    def stage(self, repo, path, line):
        """Stage the change at the given working-tree line.
        
        Returns: (exit_code, stdout, stderr, staged_blob_or_None)
        Exit codes: 0=nothing to do, 1=success, 2=error
        """
        # Get diff
        result = subprocess.run(
            ["git", "diff", "-U0", "--no-color", "--", path],
            cwd=repo, capture_output=True
        )
        if result.returncode != 0:
            return 2, "", result.stderr.decode(), None
        
        diff_text = result.stdout.decode()
        
        # Parse and split hunks
        header_lines, hunks = self._parse_and_split_hunks(diff_text)
        
        # Find hunk(s) covering the requested line
        selected = self._select_hunks_for_line(hunks, line)
        
        if not selected:
            # No change to stage - return current index content (HEAD)
            staged = self._get_staged_blob(repo, path)
            return 2, "", f"no hunk covers line {line}\n", staged
        
        # Build patch
        patch = self._build_patch(header_lines, selected)
        
        # Apply
        result = subprocess.run(
            ["git", "apply", "--cached", "--unidiff-zero", "-"],
            cwd=repo, input=patch.encode(), capture_output=True
        )
        
        # Get staged blob
        staged = self._get_staged_blob(repo, path)
        
        if result.returncode == 0:
            return 1, "applied\n", "", staged
        else:
            return 2, "", result.stderr.decode(), staged

    def _parse_and_split_hunks(self, diff_text):
        """Parse -U0 diff and split multi-line changes into per-line hunks.
        
        Pairing rule: removed lines pair with added lines line-for-line.
        Surplus adds are individual; surplus removes are one hunk.
        """
        # Parse raw hunks
        raw_hunks = []
        header_lines = []
        for line in diff_text.splitlines(keepends=True):
            if line.startswith("@@"):
                m = re.match(r"^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@", line)
                if m:
                    raw_hunks.append({
                        "old_start": int(m.group(1)),
                        "old_lines": int(m.group(2) or 1),
                        "new_start": int(m.group(3)),
                        "new_lines": int(m.group(4) or 1),
                        "header": line,
                        "body": []
                    })
            elif raw_hunks:
                raw_hunks[-1]["body"].append(line)
            else:
                header_lines.append(line)
        
        # Split each raw hunk
        split_hunks = []
        for hunk in raw_hunks:
            split_hunks.extend(self._split_hunk(hunk))
        
        return header_lines, split_hunks

    def _split_hunk(self, hunk):
        """Split a raw hunk into per-line changes."""
        body = hunk["body"]
        # Extract +/- lines (and \ No newline markers attached to them)
        content = []
        i = 0
        while i < len(body):
            line = body[i]
            if line.startswith(("+", "-")):
                # Include any following \ No newline marker
                content.append(line)
                i += 1
                while i < len(body) and body[i].startswith("\\"):
                    content[-1] += "\n" + body[i]
                    i += 1
            else:
                i += 1
        
        if not content:
            return []
        
        # Count removes and adds
        nrem = sum(1 for l in content if l.startswith("-"))
        nadd = len(content) - nrem
        pairs = min(nrem, nadd)
        
        out = []
        old_start = hunk["old_start"]
        new_start = hunk["new_start"]
        
        # Paired changes (remove + add)
        for j in range(pairs):
            old_at = j
            new_at = j
            new_body = [content[j], content[nrem + j]]
            out.append({
                "old_start": old_start + old_at,
                "old_lines": 1,
                "new_start": new_start + new_at,
                "new_lines": 1,
                "body": new_body
            })
        
        # Surplus removes - stay as one hunk
        if nrem > nadd:
            surplus_rem = content[pairs:nrem]
            out.append({
                "old_start": old_start + pairs,
                "old_lines": len(surplus_rem),
                "new_start": new_start + pairs,
                "new_lines": 0,
                "body": surplus_rem
            })
        
        # Surplus adds - each is its own line
        elif nadd > nrem:
            for k in range(nadd - nrem):
                idx = nrem + pairs + k
                out.append({
                    "old_start": old_start + pairs,
                    "old_lines": 0,
                    "new_start": new_start + pairs + k,
                    "new_lines": 1,
                    "body": [content[idx]]
                })
        
        return out

    def _select_hunks_for_line(self, hunks, line):
        """Select hunks whose new-side span covers the requested line."""
        selected = []
        for hunk in hunks:
            if hunk["new_lines"] > 0:
                covered = range(hunk["new_start"], hunk["new_start"] + hunk["new_lines"])
            else:
                covered = [hunk["new_start"] + 1]  # deletion anchor
            if line in covered:
                selected.append(hunk)
        return selected

    def _build_patch(self, header_lines, hunks):
        out = []
        for line in header_lines:
            if not line.startswith("index "):
                out.append(line.rstrip("\n"))
        for hunk in hunks:
            out.append(f"@@ -{hunk['old_start']},{hunk['old_lines']} +{hunk['new_start']},{hunk['new_lines']} @@")
            for body_line in hunk["body"]:
                out.append(body_line.rstrip("\n"))
        return "\n".join(out) + "\n"

    def _get_staged_blob(self, repo, path):
        result = subprocess.run(
            ["git", "show", f":{path}"],
            cwd=repo, capture_output=True
        )
        if result.returncode == 0:
            return result.stdout.decode()
        return None