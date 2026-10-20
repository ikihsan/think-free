"""Inspect GitHub HTML search result structure so the rank parser is exact."""
import re
import urllib.parse
import urllib.request

UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
      "Chrome/120.0 Safari/537.36 think-free-e170")


def fetch(q):
    url = "https://github.com/search?" + urllib.parse.urlencode(
        {"q": q, "type": "issues"})
    req = urllib.request.Request(url, headers={"User-Agent": UA,
                                               "Accept": "text/html"})
    with urllib.request.urlopen(req, timeout=40) as fh:
        return fh.read().decode("utf-8", "replace")


html = fetch('"Docker.app will damage your computer"')
for pat in [r'class="search results-count"[^>]*>([^<]*)<',
            r'([\d,]+)\s+results?',
            r'data-testid="results-list"',
            r'issue-list-item',
            r'href="(/[^"]*?/(?:issues|pull)/\d+)"']:
    found = re.findall(pat, html)
    print("PATTERN %-50s -> %d : %s" % (pat[:50], len(found),
                                         list(dict.fromkeys(found))[:6]))
idx = html.find("search results-count")
print("SNIPPET:", re.sub(r"\s+", " ", html[idx - 200:idx + 300]) if idx > 0 else "n/a")