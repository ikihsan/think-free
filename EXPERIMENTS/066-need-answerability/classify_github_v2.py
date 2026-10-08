#!/usr/bin/env python3
"""E066 classify GitHub issues - more precise classification."""
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
        repo = issue['repository']
        
        title_lower = title.lower()
        body_lower = text.lower()
        full_text = (title + ' ' + text).lower()
        
        # Check if it's ACTUALLY about git line/hunk staging
        # Must have explicit reference to staging lines, hunks, or partial staging in git context
        git_staging_patterns = [
            'stage line', 'stage hunk', 'stage selected', 'partial stage',
            'line staging', 'hunk staging', 'stage specific line',
            'stage individual line', 'staging lines', 'staging hunks',
            'stage by line', 'stage by hunk', 'split hunk', 'edit hunk',
            'git add -p', 'git add --patch', 'git-hunk', 'gah ', 'gah:',
            'filterdiff --lines', 'git apply --cached', 'git apply --unidiff',
            'unidiff-zero', 'unstage line', 'unstage hunk',
            'vim-gitgutter', 'gitgutter', 'sourcegit', 'gitx', 'gitahead',
            'sublime_merge', 'lazygit', 'magit', 'neogit', 'tig',
            'git-up', 'gitup', 'git-stage-lines', 'git-autofixup',
            'mcp-multi-root-git', 'split-commits', 'stage selected ranges',
            'line number range', 'line range', 'by line number',
            'hunk by line', 'stage selected range'
        ]
        
        # Check for actual git context
        git_context = any(kw in full_text for kw in ['git ', 'github', 'git-', 'hunk', 'diff ', 'commit', 'index', 'staging area', 'working tree', 'working-tree'])
        
        has_git_staging = any(pattern in full_text for pattern in git_staging_patterns) and git_context
        
        # False positives: CI/CD stages, build stages, pipeline stages, etc.
        false_positive_patterns = [
            'pipeline stage', 'build stage', 'deploy stage', 'ci stage',
            'cd stage', 'staging environment', 'staging server',
            'docker stage', 'container stage', 'kubernetes stage',
            'multi-stage', 'multi stage', 'build stages', 'deploy stages',
            'stage environment', 'stage server', 'stage deployment',
            'ci/cd', 'github actions', 'gitlab ci', 'jenkins',
            'workflow stage', 'pipeline stages', 'stage:', 'stages:',
            'drop stage', 'build pipeline', 'deploy pipeline',
            'release stage', 'test stage', 'staging area'  # but not git staging area
        ]
        
        is_false_positive = any(pattern in full_text for pattern in false_positive_patterns) and not has_git_staging
        
        # Existing tools that provide line/hunk staging
        existing_tools = [
            'lazygit', 'magit', 'vim-gitgutter', 'gitgutter', 'sourcegit',
            'gitx', 'gitahead', 'sublime merge', 'sublime_merge', 'vscode',
            'visual studio code', 'git-hunk', 'gah', 'filterdiff',
            'git add -p', 'git add --patch', 'neogit', 'tig', 'git-up',
            'gitup', 'git-stage-lines', 'git-autofixup', 'mcp-multi-root-git',
            'split-commits', 'git stage selected', 'stage selected ranges'
        ]
        
        has_existing_tool = any(tool in full_text for tool in existing_tools)
        
        # Classify
        if is_false_positive:
            classification = "not-a-software-need"
            notes = "False positive: about CI/CD/build/deploy stage, not git line staging"
        elif has_git_staging:
            classification = "resolved-from-knowledge"
            if has_existing_tool:
                notes = "Tools exist (lazygit, magit, vscode, git-hunk, gah, git add -p, neogit, tig, etc.)"
            else:
                notes = "Git's built-in git add -p and existing GUI/CLI tools provide this capability"
        elif repo in ['jesseduffield/lazygit', 'Blankeos/lazygitrs', 'NeogitOrg/neogit', 'sublimehq/sublime_merge', 'airblade/vim-gitgutter', 'sblm/gitgutter', 'sourcegit-scm/sourcegit', 'rowanj/gitx', 'gitahead/gitahead', 'git-up/GitUp', 'wkentaro/git-hunk', 'ThatXliner/gah', 'torbiak/git-autofixup', 'Rethunk-AI/mcp-multi-root-git', 'jonas/tig', 'pashaninm/lazygit']:
            # These are repos specifically about git tools - if they have an issue about staging, it's likely real
            if 'stage' in full_text or 'hunk' in full_text:
                classification = "resolved-from-knowledge"
                notes = "Git tool repo requesting staging feature; tools exist in ecosystem"
            else:
                classification = "not-a-software-need"
                notes = "Git tool repo but issue not about line/hunk staging"
        else:
            classification = "not-a-software-need"
            notes = "Not about git line/hunk staging"
        
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