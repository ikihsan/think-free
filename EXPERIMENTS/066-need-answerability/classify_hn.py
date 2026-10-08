#!/usr/bin/env python3
"""E066 classify HN needs - classify 100 sampled needs."""
import json
import os

RAW = '/home/ubuntu/think-free/EXPERIMENTS/066-need-answerability/raw'
OUT = '/home/ubuntu/think-free/EXPERIMENTS/066-need-answerability/raw/classification.tsv'

# Load HN needs
needs = []
with open(os.path.join(RAW, 'hn_needs.jsonl'), 'r') as f:
    for line in f:
        needs.append(json.loads(line))

# Sample: 20 from each of top 5 triggers
by_trigger = {}
for need in needs:
    trigger = need['trigger']
    if trigger not in by_trigger:
        by_trigger[trigger] = []
    by_trigger[trigger].append(need)

sorted_triggers = sorted(by_trigger.items(), key=lambda x: len(x[1]), reverse=True)[:5]
sampled = []
for trigger, trigger_needs in sorted_triggers:
    sampled.extend(trigger_needs[:20])

print(f"Sampled HN needs: {len(sampled)}")
for trigger, trigger_needs in sorted_triggers:
    print(f"  {trigger}: {len(trigger_needs)} total, taking 20")

# Append to existing classification file
with open(OUT, 'a') as f:
    for need in sampled:
        id_ = need['id']
        trigger = need['trigger']
        story = need['story'].replace('\t', ' ').replace('\n', ' ')
        text = need['text'][:500].replace('\t', ' ').replace('\n', ' ')
        
        full_text = (trigger + ' ' + story + ' ' + text).lower()
        
        # Classify HN needs
        # Software/tool needs that are answerable from general knowledge
        software_keywords = [
            'tool', 'library', 'app', 'service', 'cli', 'script', 'package',
            'framework', 'editor', 'plugin', 'extension', 'api', 'sdk',
            'software', 'program', 'application', 'utility', 'script',
            'github', 'gitlab', 'npm', 'pypi', 'cargo', 'crates', 'pip',
            'docker', 'kubernetes', 'aws', 'gcp', 'azure', 'cloud',
            'database', 'sql', 'nosql', 'redis', 'postgres', 'mysql',
            'react', 'vue', 'angular', 'svelte', 'nextjs', 'node',
            'python', 'javascript', 'typescript', 'rust', 'go', 'java',
            'compiler', 'interpreter', 'linter', 'formatter', 'bundler',
            'test', 'testing', 'ci', 'cd', 'deploy', 'monitoring',
            'logging', 'analytics', 'metrics', 'dashboard', 'visualization',
            'ui', 'ux', 'frontend', 'backend', 'fullstack', 'mobile',
            'ios', 'android', 'swift', 'kotlin', 'flutter', 'react native',
            'machine learning', 'ml', 'ai', 'llm', 'gpt', 'claude',
            'embedding', 'vector', 'database', 'search', 'index',
            'auth', 'authentication', 'authorization', 'oauth', 'jwt',
            'payment', 'stripe', 'subscription', 'billing', 'invoice',
            'email', 'sms', 'notification', 'webhook', 'queue',
            'cache', 'redis', 'memcached', 'cdn', 'load balancer',
            'proxy', 'reverse proxy', 'nginx', 'apache', 'traefik',
            'security', 'encryption', 'ssl', 'tls', 'certificate',
            'backup', 'restore', 'disaster recovery', 'migration',
            'etl', 'pipeline', 'data', 'analytics', 'warehouse',
            'bi', 'business intelligence', 'reporting', 'chart',
            'graph', 'visualization', 'map', 'gis', 'geospatial',
            'blockchain', 'crypto', 'web3', 'smart contract', 'defi',
            'game', 'engine', 'unity', 'unreal', 'godot',
            'video', 'audio', 'streaming', 'encoding', 'transcoding',
            'image', 'photo', 'ocr', 'computer vision', 'nlp',
            'translation', 'localization', 'i18n', 'accessibility',
            'pdf', 'document', 'spreadsheet', 'excel', 'csv', 'json',
            'xml', 'yaml', 'toml', 'config', 'configuration',
            'dotfile', 'vim', 'emacs', 'vscode', 'ide', 'editor',
            'terminal', 'shell', 'bash', 'zsh', 'fish', 'powershell',
            'ssh', 'vpn', 'proxy', 'tunnel', 'network', 'dns',
            'monitoring', 'alerting', 'observability', 'tracing',
            'profiling', 'debugging', 'profiling', 'benchmark',
        ]
        
        # Not software needs
        not_software_keywords = [
            'boredom', 'bored', 'netflix', 'movie', 'tv', 'book', 'read',
            'life', 'career', 'job', 'salary', 'money', 'finance',
            'investment', 'stock', 'crypto', 'bitcoin', 'ethereum',
            'health', 'medical', 'doctor', 'hospital', 'insurance',
            'law', 'legal', 'lawyer', 'court', 'contract', 'tax',
            'politics', 'government', 'policy', 'election', 'vote',
            'relationship', 'dating', 'marriage', 'divorce', 'friend',
            'family', 'parent', 'child', 'school', 'university', 'college',
            'education', 'degree', 'phd', 'master', 'bachelor',
            'travel', 'vacation', 'hotel', 'flight', 'visa', 'passport',
            'food', 'recipe', 'cooking', 'restaurant', 'diet', 'nutrition',
            'exercise', 'fitness', 'gym', 'running', 'weight', 'muscle',
            'sleep', 'insomnia', 'anxiety', 'depression', 'therapy',
            'music', 'song', 'band', 'concert', 'instrument', 'guitar',
            'art', 'painting', 'drawing', 'design', 'creative', 'write',
            'blog', 'newsletter', 'podcast', 'youtube', 'streamer',
            'social media', 'twitter', 'linkedin', 'facebook', 'instagram',
            'tiktok', 'reddit', 'hacker news', 'hn', 'lobste.rs',
            'community', 'forum', 'discord', 'slack', 'irc', 'matrix',
            'open source', 'oss', 'license', 'mit', 'gpl', 'apache',
            'contribution', 'contributor', 'maintainer', 'project',
            'startup', 'founder', 'cofounder', 'vc', 'venture', 'capital',
            'hiring', 'recruiting', 'interview', 'resume', 'cv',
            'remote work', 'wfh', 'office', 'commute', 'productivity',
            'time management', 'todo', 'task', 'project management',
            'note', 'note taking', 'obsidian', 'notion', 'roam',
            'knowledge management', 'personal knowledge', 'pkm',
            'second brain', 'zettelkasten', 'wiki', 'documentation',
        ]
        
        is_software = any(kw in full_text for kw in software_keywords)
        is_not_software = any(kw in full_text for kw in not_software_keywords)
        
        # Specific check: "is there a tool that" + software context
        if trigger in ['is there a tool that', 'is there a library that', 'is there a cli', 'is there a python library',
                       'looking for a tool', 'looking for a library', 'looking for a way to',
                       'what tool do you use', 'what do you use for', 'what do you use to',
                       'does anyone know a tool', 'does anyone know a good', 'does anyone know any',
                       'any tool that', 'is there anything like', 'is there a self-hosted',
                       'is there an open source', 'we need a tool', 'nobody has built']:
            is_software = True
            is_not_software = False
        
        # Check for specific external data needs
        needs_external_data = any(kw in full_text for kw in [
            'serial number', 'vin', 'model number', 'part number', 'spec sheet',
            'manufacturer', 'datasheet', 'proprietary', 'private api', 'internal',
            'company', 'enterprise', 'legacy', 'mainframe', 'cobol', 'fortran',
            'specific model', 'exact model', 'my device', 'my car', 'my bike',
            'my laptop', 'my phone', 'my printer', 'my router', 'my camera'
        ])
        
        # Check for unresolvable (no public data)
        unresolvable = any(kw in full_text for kw in [
            'lost', 'forgotten', 'deleted', 'destroyed', 'burned', 'corrupted',
            'no record', 'never recorded', 'nobody knows', 'unknown', 'mystery',
            'ancient', 'historical', 'archaeological', 'fossil', 'extinct'
        ])
        
        if is_not_software and not is_software:
            classification = "not-a-software-need"
            notes = "Not a software/tool need (personal, life, health, etc.)"
        elif needs_external_data:
            classification = "resolved-needs-external-data"
            notes = "Method known but needs proprietary/private/specific data (serial, spec sheet, etc.)"
        elif unresolvable:
            classification = "unresolved-no-public-data"
            notes = "Data never recorded or no public source exists"
        elif is_software:
            classification = "resolved-from-knowledge"
            notes = "Software/tool need answerable from general knowledge (libraries, tools, frameworks exist)"
        else:
            classification = "resolved-from-knowledge"
            notes = "Likely software-related need, answerable from general knowledge"
        
        f.write(f"hn\t{id_}\t{trigger}\t{text}\t{classification}\t{notes}\n")

print(f"Appended {len(sampled)} HN need classifications to {OUT}")

# Print summary for HN only
hn_counts = {}
with open(OUT, 'r') as f:
    next(f)  # skip header
    for line in f:
        parts = line.strip().split('\t')
        if len(parts) >= 5 and parts[0] == 'hn':
            cls = parts[4]
            hn_counts[cls] = hn_counts.get(cls, 0) + 1

print("\nHN Classification summary:")
for cls, count in sorted(hn_counts.items()):
    print(f"  {cls}: {count}")

# Overall summary
all_counts = {}
with open(OUT, 'r') as f:
    next(f)
    for line in f:
        parts = line.strip().split('\t')
        if len(parts) >= 5:
            cls = parts[4]
            all_counts[cls] = all_counts.get(cls, 0) + 1

print("\nOverall Classification summary:")
for cls, count in sorted(all_counts.items()):
    print(f"  {cls}: {count}")