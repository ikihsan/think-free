#!/usr/bin/env python3
"""Probe additional candidate Discourse instances."""
import urllib.request
import json
import time

# More non-technical Discourse candidates
candidates = [
    ("community.home-assistant.io", "home automation"),  # technical but home
    ("forum.arduino.cc", "electronics"),  # technical hobby
    ("community.ezra.com", "camping"),  # camping
    ("community.glowforge.com", "crafts"),  # crafting
    ("community.raspberrypi.com", "electronics"),  # technical
    ("community.mycroft.ai", "voice assistant"),  # technical
    ("forums.moneytree.com", "finance"),  # unknown platform
    ("community.fly.io", "tech"),  # too technical
    ("forum.obsproject.com", "streaming"),  # streaming
    ("community.homey.app", "home automation"),  # home automation
    ("community.roonlabs.com", "audio"),  # audio
    ("community.syncthing.net", "tech"),  # too technical
    ("discuss.haskell.org", "programming"),  # too technical
    ("community.coinbase.com", "crypto"),  # crypto forum
    ("community.truenas.com", "storage"),  # technical
    ("forum.discourse.org", "meta"),  # meta
    ("community.librenms.org", "tech"),  # too technical
    ("community.zigbee2mqtt.io", "home automation"),  # home automation
    ("community.unraid.net", "storage"),  # tech
    ("forums.tomshardware.com", "hardware"),  # hardware
]

results = []
for domain, topic in candidates:
    try:
        url = f"https://{domain}/latest.json"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=8) as resp:
            data = json.loads(resp.read())
            topics = data.get("topic_list", {}).get("topics", [])
            results.append({
                "domain": domain,
                "topic": topic,
                "status": "ok",
                "topics_returned": len(topics),
                "first_title": topics[0]["title"][:50] if topics else None,
                "has_views": "views" in topics[0] if topics else False,
            })
    except Exception as e:
        results.append({"domain": domain, "topic": topic, "status": f"err: {str(e)[:60]}"})
    time.sleep(0.3)

ok = [r for r in results if r.get("status") == "ok"]
print(f"Found {len(ok)} active instances:")
for r in ok:
    print(f"  {r['domain']} ({r['topic']}): {r.get('first_title', 'N/A')}")
print()
print("Failed:")
for r in results:
    if r.get("status") != "ok":
        print(f"  {r['domain']}: {r['status']}")
