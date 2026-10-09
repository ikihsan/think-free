#!/usr/bin/env python3
"""Probe candidate Discourse instances for the E074 measurement."""
import urllib.request
import json
import time
import sys

candidates = [
    ("community.anovaculinary.com", "cooking"),
    ("forum.seriouseats.com", "cooking"),
    ("forums.tdi.club", "automotive"),
    ("forum.miata.net", "automotive"),
    ("forum.sawmillcreek.org", "woodworking"),
    ("discuss.pixls.us", "photography"),
    ("forum.fujixforum.com", "photography"),
    ("forum.home-barista.com", "coffee"),
    ("discourse.decentespresso.com", "coffee"),
    ("diychatroom.com", "home improvement"),
    ("keebtalk.com", "mechanical keyboards"),
    ("community.spiceworks.com", "IT/home"),
]

results = []
for domain, topic in candidates:
    try:
        url = f"https://{domain}/latest.json"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read())
            topics = data.get("topic_list", {}).get("topics", [])
            per_page = data.get("topic_list", {}).get("per_page", 0)
            results.append({
                "domain": domain,
                "topic": topic,
                "status": "ok",
                "topics_returned": len(topics),
                "per_page": per_page,
                "first_topic_title": topics[0]["title"][:60] if topics else None,
                "has_view_count": "views" in topics[0] if topics else False,
                "has_like_count": "like_count" in topics[0] if topics else False,
                "has_reply_count": "reply_count" in topics[0] if topics else False,
            })
    except Exception as e:
        results.append({
            "domain": domain,
            "topic": topic,
            "status": f"error: {str(e)[:80]}",
        })
    time.sleep(0.5)

print(json.dumps(results, indent=2))
