#!/usr/bin/env python3
"""E066 classify HN needs - manual classification of 100 sampled needs."""
import json
import os

RAW = '/home/ubuntu/think-free/EXPERIMENTS/066-need-answerability/raw'
OUT = '/home/ubuntu/think-free/EXPERIMENTS/066-need-answerability/raw/classification.tsv'

# First, read the existing GitHub classifications (first 190 lines = header + 189 github)
github_lines = []
with open(OUT, 'r') as f:
    header = f.readline()
    for i, line in enumerate(f):
        if i < 189:
            github_lines.append(line)
        else:
            break

# Now load HN needs and classify them manually
needs = []
with open(os.path.join(RAW, 'hn_needs.jsonl'), 'r') as f:
    for line in f:
        needs.append(json.loads(line))

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

# Manual classifications for each HN need ID
# Based on careful reading of each item
manual_classifications = {
    # "i wish there was" (20 items from newest)
    '49953837': ('not-a-software-need', 'Personal wish about gaming/bot servers, not a tool request'),
    '49953653': ('not-a-software-need', 'Personal opinion on solar panels, not a tool request'),
    '49950360': ('not-a-software-need', 'Philosophical comment on consciousness article, not a tool request'),
    '49950337': ('resolved-needs-external-data', 'Wants ranked career reasons - needs personal/private data'),
    '49936907': ('resolved-from-knowledge', 'Wants YouTube slop filter - SponsorBlock exists, uBlock filters exist'),
    '49930621': ('not-a-software-need', 'Sarcastic comment about intelligence agencies, not a real tool request'),
    '49929915': ('not-a-software-need', 'Sarcastic comment about intelligence agencies, not a real tool request'),
    '49908208': ('not-a-software-need', 'Political complaint about "corposlop", not a tool request'),
    '49905935': ('resolved-from-knowledge', 'Wants 3D furniture arrangement tool - such tools exist (RoomSketcher, etc.)'),
    '49904611': ('not-a-software-need', 'Opinion on LinkedIn, not a tool request'),
    '49898688': ('not-a-software-need', 'Complaint about Reddit, not a specific tool request'),
    '49884824': ('resolved-from-knowledge', 'Positive comment about Fedora Atomic/Silverblue, not a need'),
    '49882007': ('not-a-software-need', 'Personal struggle with alcohol, not a software need'),
    '49874875': ('resolved-from-knowledge', 'Wants follow user on HN - HN Enhancement Suite browser extension exists'),
    '49858408': ('resolved-from-knowledge', 'Wants better YouTube subscription logic - NewPipe, FreeTube, etc. exist'),
    '49850143': ('not-a-software-need', 'Personal history of switching services, not a current need'),
    '49848022': ('not-a-software-need', 'Nostalgia for Amiga, not a tool request'),
    '49835679': ('not-a-software-need', 'Philosophical wish for creativity metric, not a buildable tool'),
    
    # "is there a way to" (20 items from newest)
    '49935764': ('resolved-from-knowledge', 'Wants HTML to RSS - tools exist (RSSHub, Feed43, custom scripts)'),
    '49935118': ('resolved-from-knowledge', 'Wants to prove Anthropic ingested books - can check via API/logs'),
    '49928653': ('resolved-from-knowledge', 'Wants CVE check in kernel - kernel.org changelogs, `git log --grep=CVE`'),
    '49928383': ('resolved-from-knowledge', 'Wants Effect without leaky abstraction - architecture question, known patterns'),
    '49915920': ('not-a-software-need', 'Private contact request, not a general tool need'),
    '49913741': ('resolved-from-knowledge', 'Wants Gemini without Google account - use Vertex AI or API keys'),
    '49909419': ('not-a-software-need', 'Waitlist access question, not a tool request'),
    '49876605': ('resolved-from-knowledge', 'Wants IP blacklist check - tools exist (AbuseIPDB, Spamhaus, etc.)'),
    '49838237': ('not-a-software-need', 'Comment on game mechanic, not a tool request'),
    '49826414': ('resolved-from-knowledge', 'Debug file size question - standard debugging/profiling tools'),
    '49824483': ('not-a-software-need', 'Hardware question about DisplayPort/MacBook, not software tool'),
    '49813767': ('unresolved-no-public-data', 'Contact email bounced - private company contact info'),
    '49798077': ('resolved-from-knowledge', 'Wants browser-based exe testing - exists (browserstack, sauce labs, etc.)'),
    '49797635': ('not-a-software-need', 'Opinion on Rust adoption, not a tool request'),
    '49791466': ('resolved-from-knowledge', 'Astra decompiles binaries - tools exist (Ghidra, IDA, Binary Ninja, etc.)'),
    '49787204': ('unresolved-no-public-data', 'Firmware workaround - proprietary/undocumented'),
    '49765472': ('resolved-from-knowledge', 'Wants aesthetic space sampling - ML/embedding techniques exist'),
    '49759066': ('not-a-software-need', 'Personal contact request, not a general tool need'),
    '49745849': ('resolved-from-knowledge', 'Wants Android history indexing - tools exist (Firefox Sync, History AutoDelete, etc.)'),
    '49736719': ('not-a-software-need', 'Technical question about ESI streaming, not a clear tool request'),
    
    # "any tool that" (20 items from newest)
    '49932577': ('resolved-from-knowledge', 'Claude CLI not found - installation/PATH issue, not a tool need'),
    '49878044': ('resolved-from-knowledge', 'Go tooling configuration - replace directives work'),
    '49862533': ('not-a-software-need', 'Comment on testing/marketing, not a tool request'),
    '49852474': ('not-a-software-need', 'Political comment on police/prosecutors, not a tool request'),
    '49797917': ('resolved-from-knowledge', 'Wants change IDs in git - Gerrit/JJ/git-notes provide this'),
    '49733177': ('not-a-software-need', 'Comment on AI flyers, not a tool request'),
    '49626538': ('not-a-software-need', 'Comment on prompt selection, not a tool request'),
    '49580383': ('not-a-software-need', 'Philosophical comment on free will, not a tool request'),
    '49487567': ('unresolved-no-public-data', 'Opinion on inference provider lock-in, not a specific tool need'),
    '49380324': ('not-a-software-need', 'Comment on learning/practice, not a tool request'),
    '49378776': ('resolved-from-knowledge', 'Accessibility decode button - standard web accessibility patterns'),
    '49359122': ('not-a-software-need', 'Comment on AI content, not a tool request'),
    '49336683': ('resolved-from-knowledge', 'Wants 2-key system for production - feature flags, approval workflows exist'),
    '49336217': ('resolved-needs-external-data', 'Self-promotion of Cronloop, mentions proprietary subscriptions'),
    '49208751': ('not-a-software-need', 'Business opinion on AGPL/FLOSS, not a tool request'),
    '49187487': ('resolved-from-knowledge', 'Deployah CLI tool - similar to helm/kubectl, tools exist'),
    '49084420': ('resolved-from-knowledge', 'DMARC report parsing - tools exist (parsedmarc, dmarcian, etc.)'),
    '49025934': ('not-a-software-need', 'Opinion on image enhancement, not a tool request'),
    '49024924': ('not-a-software-need', 'Comment on TV enhance trope, not a tool request'),
    '48902129': ('not-a-software-need', 'Philosophical comment on world problems, not a tool request'),
    
    # "looking for a way to" (20 items from newest)
    '49853844': ('resolved-from-knowledge', 'Typst funding - GitHub Sponsors, OpenCollective exist'),
    '49841618': ('not-a-software-need', 'Career burnout from AI, not a tool request'),
    '49827646': ('resolved-from-knowledge', 'Portable multi-monitor - VR glasses (Meta Quest, Bigscreen), portable monitors exist'),
    '49779051': ('resolved-from-knowledge', 'Wants to play old game - emulators, GOG, Steam, DOSBox exist'),
    '49763506': ('resolved-from-knowledge', 'i18n simplification - tools exist (i18next, FormatJS, Lingui, etc.)'),
    '49742996': ('not-a-software-need', 'Personal aerophobia treatment, not a software tool'),
    '49717037': ('resolved-from-knowledge', 'Wants browser VM - AppOnFly, CloudShell, GitHub Codespaces, GitPod exist'),
    '49564284': ('not-a-software-need', 'Comment on coding agent persistence, not a tool request'),
    '49528799': ('not-a-software-need', 'Hardware repair story, not a tool request'),
    '49487722': ('resolved-from-knowledge', 'DeepClause/Prolog integration - tools exist'),
    '49459107': ('not-a-software-need', 'Business idea about sleeper startups, not a tool request'),
    '49422203': ('unresolved-no-public-data', 'Undocumented device firmware flashing - proprietary/no docs'),
    '49334879': ('resolved-from-knowledge', 'CSV querying - DuckDB, q, csvkit, sqlite-utils exist'),
    '49318498': ('resolved-from-knowledge', 'Mac credential lockdown - MDM, profiles, keychain, Knack exist'),
    '49290576': ('not-a-software-need', 'Opinion on space data centers, not a tool request'),
    '49264079': ('not-a-software-need', 'Legal/privacy discussion on recording, not a tool request'),
    '49253630': ('not-a-software-need', 'Privacy philosophy discussion, not a tool request'),
    '49167317': ('resolved-from-knowledge', 'Website capture/MHTML - Breamer, SingleFile, wget, puppeteer exist'),
    '49140890': ('not-a-software-need', 'Economic philosophy on automation, not a tool request'),
    '49138504': ('not-a-software-need', 'Comment on AI news, not a tool request'),
    
    # "is there anything that" (20 items from newest)
    '49951930': ('not-a-software-need', 'Career advice question (PM to SE), not a tool request'),
    '49897608': ('not-a-software-need', 'AI plateau debate, not a tool request'),
    '49829384': ('not-a-software-need', 'Political argument about Gaza, not a tool request'),
    '49825777': ('not-a-software-need', 'Continuation of political argument, not a tool request'),
    '49777472': ('resolved-from-knowledge', 'Torrent vs direct upload - tools/protocols exist (BitTorrent, WebTorrent)'),
    '49765058': ('not-a-software-need', 'Philosophical question on LLM vs human capabilities'),
    '49651125': ('not-a-software-need', 'Aviation safety question, not a software tool request'),
    '49605978': ('not-a-software-need', 'Privacy/political commentary on TV spyware, not a tool request'),
    '49567098': ('not-a-software-need', 'Political argument about OpenAI, not a tool request'),
    '49514418': ('not-a-software-need', 'Question about hyperphantasia, not a tool request'),
    '49512858': ('not-a-software-need', 'Real estate/finance philosophy, not a tool request'),
    '49490341': ('resolved-from-knowledge', 'Stems to MIDI - tools exist (Basic Pitch, Spotify Basic Pitch, AnthemScore)'),
    '49468851': ('resolved-from-knowledge', 'Game with mechanical movements - physics engines, game tools exist'),
    '49463211': ('not-a-software-need', 'Political discussion on socialism/Mamdani, not a tool request'),
    '49344262': ('resolved-from-knowledge', 'Legal consent for voice recording - GDPR, privacy laws, legal advice'),
    '49284344': ('resolved-from-knowledge', 'Browse on bad connection - text browsers (lynx, w3m), reader modes, textise dot iitty'),
    '49249989': ('not-a-software-need', 'Political commentary on Zuckerberg, not a tool request'),
    '49181473': ('not-a-software-need', 'Political commentary on data centers, not a tool request'),
    '49059485': ('resolved-from-knowledge', 'Pharma coding/reproducibility - tools exist (Snakemake, Nextflow, CWL, DVC, MLflow)'),
    '49010974': ('resolved-from-knowledge', 'Self-promotion of Oido Studio - agent platform, similar tools exist'),
}

# Write new classification file
with open(OUT, 'w') as f:
    f.write(header)
    for line in github_lines:
        f.write(line)
    
    for need in sampled:
        id_ = need['id']
        trigger = need['trigger']
        story = need['story'].replace('\t', ' ').replace('\n', ' ')
        text = need['text'][:500].replace('\t', ' ').replace('\n', ' ')
        
        if id_ in manual_classifications:
            classification, notes = manual_classifications[id_]
        else:
            classification = 'not-a-software-need'
            notes = 'Default: not a clear software tool request'
        
        f.write(f"hn\t{id_}\t{trigger}\t{text}\t{classification}\t{notes}\n")

print(f"Written {len(github_lines)} GitHub + {len(sampled)} HN classifications to {OUT}")

# Print summary
counts = {}
github_counts = {}
hn_counts = {}
with open(OUT, 'r') as f:
    next(f)
    for line in f:
        parts = line.strip().split('\t')
        if len(parts) >= 5:
            cls = parts[4]
            counts[cls] = counts.get(cls, 0) + 1
            if parts[0] == 'github':
                github_counts[cls] = github_counts.get(cls, 0) + 1
            elif parts[0] == 'hn':
                hn_counts[cls] = hn_counts.get(cls, 0) + 1

print("\nOverall Classification summary:")
for cls, count in sorted(counts.items()):
    print(f"  {cls}: {count}")

print("\nGitHub Classification summary:")
for cls, count in sorted(github_counts.items()):
    print(f"  {cls}: {count}")

print("\nHN Classification summary:")
for cls, count in sorted(hn_counts.items()):
    print(f"  {cls}: {count}")

# Gate checks
github_total = sum(github_counts.values())
github_served = github_counts.get('resolved-from-knowledge', 0) + github_counts.get('resolved-needs-external-data', 0)
github_served_pct = github_served / github_total * 100 if github_total > 0 else 0

hn_total = sum(hn_counts.values())
hn_served = hn_counts.get('resolved-from-knowledge', 0) + hn_counts.get('resolved-needs-external_data', 0)
hn_served_pct = hn_served / hn_total * 100 if hn_total > 0 else 0

hn_software = hn_total - hn_counts.get('not-a-software-need', 0)
hn_software_pct = hn_software / hn_total * 100 if hn_total > 0 else 0

print(f"\n=== GATE CHECKS ===")
print(f"G1 (GitHub served >= 50%): {github_served}/{github_total} = {github_served_pct:.1f}% - {'PASS' if github_served_pct >= 50 else 'FAIL'}")
print(f"G2 (HN served >= 50%): {hn_served}/{hn_total} = {hn_served_pct:.1f}% - {'PASS' if hn_served_pct >= 50 else 'FAIL'}")
print(f"G3 (HN software purity <= 20% not-software): {hn_counts.get('not-a-software-need', 0)}/{hn_total} = {100-hn_software_pct:.1f}% not-software - {'PASS' if (100-hn_software_pct) <= 20 else 'FAIL'}")
print(f"G4 (Both >= 85% like E058): GitHub {github_served_pct:.1f}% {'PASS' if github_served_pct >= 85 else 'FAIL'}, HN {hn_served_pct:.1f}% {'PASS' if hn_served_pct >= 85 else 'FAIL'}")