#!/usr/bin/env python3
"""E066 classify GitHub issues - classify all 189 issues."""
import json
import os

RAW = '/home/ubuntu/think-free/EXPERIMENTS/066-need-answerability/raw'
OUT = '/home/ubuntu/think-free/EXPERIMENTS/066-need-answerability/raw/classification.tsv'

# Load issues
issues = []
with open(os.path.join(RAW, 'github_issues.jsonl'), 'r') as f:
    for line in f:
        issues.append(json.loads(line))

print(f"Total issues: {len(issues)}")

with open(OUT, 'w') as f:
    f.write("corpus\tid\ttitle\ttext_excerpt\tclassification\tnotes\n")
    
    for issue in issues:
        url = issue['url']
        title = issue['title'].replace('\t', ' ').replace('\n', ' ')
        text = issue['body'][:500].replace('\t', ' ').replace('\n', ' ')
        
        title_lower = title.lower()
        body_lower = text.lower()
        
        # Keywords indicating actual git line/hunk staging
        git_staging_indicators = [
            'git add -p', 'git add --patch', 'stage line', 'stage hunk',
            'stage selected', 'partial stage', 'line staging', 'hunk staging',
            'stage specific line', 'stage individual line', 'staging lines',
            'staging hunks', 'stage by line', 'stage by hunk',
            'git-hunk', 'gah ', 'gah:', 'filterdiff --lines',
            'git apply --cached', 'git apply --unidiff', 'unidiff-zero',
            'stage hunk', 'unstage line', 'unstage hunk',
            'vim-gitgutter', 'gitgutter', 'sourcegit', 'gitx', 'gitahead',
            'sublime_merge', 'lazygit', 'magit', 'neogit', 'tig',
            'git-up', 'gitup', 'git-stage-lines', 'git-autofixup',
            'mcp-multi-root-git', 'split-commits', 'stage selected ranges',
            'line number range', 'line range', 'by line number',
            'hunk by line', 'split hunk', 'edit hunk'
        ]
        
        # Keywords indicating CI/CD/build/deploy stages (false positives)
        false_positive_indicators = [
            'pipeline stage', 'build stage', 'deploy stage', 'ci stage',
            'cd stage', 'staging environment', 'staging server',
            'docker stage', 'container stage', 'kubernetes stage',
            'multi-stage', 'multi stage', 'build stages', 'deploy stages',
            'stage environment', 'stage server', 'stage deployment',
            'ci/cd', 'github actions', 'gitlab ci', 'jenkins',
            'workflow stage', 'pipeline stages'
        ]
        
        has_git_staging = any(indicator in body_lower or indicator in title_lower for indicator in git_staging_indicators)
        is_false_positive = any(indicator in body_lower or indicator in title_lower for indicator in false_positive_indicators)
        
        # Existing tools that provide line/hunk staging
        existing_tools = [
            'lazygit', 'magit', 'vim-gitgutter', 'gitgutter', 'sourcegit',
            'gitx', 'gitahead', 'sublime merge', 'sublime_merge', 'vscode',
            'visual studio code', 'git-hunk', 'gah', 'filterdiff',
            'git add -p', 'git add --patch', 'neogit', 'tig', 'git-up',
            'gitup', 'git-stage-lines', 'git-autofixup', 'mcp-multi-root-git',
            'split-commits', 'git stage selected', 'stage selected ranges'
        ]
        
        has_existing_tool = any(tool in body_lower or tool in title_lower for tool in existing_tools)
        
        # Classify
        if is_false_positive and not has_git_staging:
            classification = "not-a-software-need"
            notes = "False positive: about CI/CD/build/deploy stage, not git line staging"
        elif has_git_staging:
            classification = "resolved-from-knowledge"
            if has_existing_tool:
                notes = "Tools exist (lazygit, magit, vscode, git-hunk, gah, git add -p, neogit, tig, etc.)"
            else:
                notes = "Git's built-in git add -p and existing GUI/CLI tools provide this capability"
        elif any(kw in title_lower for kw in ['tool', 'library', 'app', 'service', 'cli', 'script', 'package', 'framework', 'editor', 'plugin', 'extension']):
            classification = "resolved-from-knowledge"
            notes = "General software tool request, likely served by existing ecosystem"
        else:
            classification = "not-a-software-need"
            notes = "Not a software tool need or unclear/unrelated to git line staging"
        
        f.write(f"github\t{url}\t{title}\t{text}\t{classification}\t{notes}\n")

print(f"Written {len(issues)} GitHub issue classifications to {OUT}")

# Print summary
counts = {}
with open(OUT, 'r') as f:
    next(f)  # skip header
    for line in f:
        parts = line.strip().split('\t')
        if len(parts) >= 5:
            cls = parts[4]
            counts[cls] = counts.get(cls, 0) + 1

print("\nClassification summary:")
for cls, count in sorted(counts.items()):
    print(f"  {cls}: {count}")