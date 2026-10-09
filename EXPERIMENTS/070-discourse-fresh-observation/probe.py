#!/usr/bin/env python3
"""
Probe candidate Discourse instances for public API access and non-technical domains.
Run before harvest to finalize the instance list.
"""
import json
import sys
import time
import urllib.request
import urllib.error

CANDIDATES = [
    # Cooking/food
    ("Anova Culinary", "https://community.anovaculinary.com"),
    ("Serious Eats", "https://forum.seriouseats.com"),
    ("Kenji Lopez-Alt", "https://discourse.kenjilopezalt.com"),
    
    # Coffee
    ("Home-Barista", "https://forum.home-barista.com"),
    ("Decent Espresso", "https://discourse.decentespresso.com"),
    
    # Photography
    ("Pixls.us", "https://discuss.pixls.us"),
    ("Fuji X Forum", "https://forum.fujixforum.com"),
    ("DPReview", "https://www.dpreview.com/forums"),  # not Discourse
    
    # Automotive
    ("TDI Club", "https://forums.tdi.club"),
    ("Miata.net", "https://forum.miata.net"),
    ("Bob is the Oil Guy", "https://www.bobistheoilguy.com/forums"),
    
    # Woodworking
    ("Sawmill Creek", "https://forum.sawmillcreek.org"),
    ("Woodworking Talk", "https://www.woodworkingtalk.com"),
    ("Lumberjocks", "https://lumberjocks.com"),
    
    # Gardening
    ("Garden.org", "https://garden.org"),
    ("GardenWeb", "https://forums.gardenweb.com"),
    ("Houzz", "https://www.houzz.com/discussions"),
    
    # Home improvement/DIY
    ("DIY Chatroom", "https://www.diychatroom.com"),
    ("Home Improvement Stack Exchange", "https://diy.stackexchange.com"),  # SE, not Discourse
    
    # Mechanical keyboards (borderline technical hobby)
    ("KeebTalk", "https://keebtalk.com"),
    
    # Other hobbies
    ("Reddit Discourse", "https://discourse.reddit.com"),  # meta
    ("Fountain Pens", "https://www.fountainpennetwork.com/forum"),
    ("Watch enthusiasts", "https://forums.watchuseek.com"),
]

def probe_discourse(base_url):
    """Probe a Discourse instance for public API access."""
    api_url = f"{base_url.rstrip('/')}/latest.json"
    try:
        req = urllib.request.Request(api_url, headers={'User-Agent': 'ThinkFree-E070/1.0'})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            topic_list = data.get('topic_list', {})
            topics = topic_list.get('topics', [])
            return {
                'accessible': True,
                'topic_count': len(topics),
                'has_more': topic_list.get('more_topics_url') is not None,
                'sample_topic': topics[0] if topics else None,
                'error': None
            }
    except urllib.error.HTTPError as e:
        return {'accessible': False, 'error': f'HTTP {e.code}: {e.reason}'}
    except urllib.error.URLError as e:
        return {'accessible': False, 'error': f'URL error: {e.reason}'}
    except json.JSONDecodeError as e:
        return {'accessible': False, 'error': f'JSON decode: {e}'}
    except Exception as e:
        return {'accessible': False, 'error': f'{type(e).__name__}: {e}'}

def check_solved_plugin(base_url):
    """Check if discourse-solved plugin is enabled."""
    # The solved plugin adds a 'solved' field to topics
    # We can check by looking at a topic's full data
    api_url = f"{base_url.rstrip('/')}/t/1.json"
    try:
        req = urllib.request.Request(api_url, headers={'User-Agent': 'ThinkFree-E070/1.0'})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            # Check for solved fields
            has_solved = 'solved' in data or 'accepted_answer' in data
            return has_solved
    except:
        return False

def main():
    print("Probing Discourse instances...\n")
    results = []
    
    for name, url in CANDIDATES:
        print(f"  {name}: {url}")
        result = probe_discourse(url)
        result['name'] = name
        result['url'] = url
        
        if result['accessible']:
            print(f"    ✓ Accessible - {result['topic_count']} topics on latest page")
            # Check solved plugin on first topic if available
            if result['sample_topic']:
                topic_id = result['sample_topic'].get('id')
                if topic_id:
                    solved = check_solved_plugin(url)
                    result['has_solved_plugin'] = solved
                    print(f"    Solved plugin: {'yes' if solved else 'no'}")
        else:
            print(f"    ✗ Failed: {result['error']}")
        
        results.append(result)
        time.sleep(0.5)  # Be polite
    
    import os
    # Save results
    out_path = os.path.join(os.path.dirname(__file__), 'raw', 'probe-results.json')
    with open(out_path, 'w') as f:
        json.dump(results, f, indent=2)
    
    # Print summary
    print("\n=== VIABLE INSTANCES ===")
    viable = [r for r in results if r['accessible']]
    for r in viable:
        print(f"  {r['name']}: {r['url']} ({r['topic_count']} topics, solved={r.get('has_solved_plugin', 'unknown')})")
    
    print(f"\nTotal viable: {len(viable)}/{len(CANDIDATES)}")
    return viable

if __name__ == '__main__':
    viable = main()
    if len(viable) < 5:
        print("\nWARNING: Fewer than 5 viable instances found. May need to expand candidate list.")
        sys.exit(1)
    else:
        print("\nSufficient instances found. Proceed to harvest.")
        sys.exit(0)