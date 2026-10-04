import json, urllib.request, urllib.parse, time, re, sys, hashlib
BASE="https://hn.algolia.com/api/v1/search"
TRIGGERS=[
 "is there a tool that","is there a library that","is there an app that","is there a service that",
 "is there anything that","is there a way to","is there a cli","is there a python library",
 "what do you use for","what do you use to","what tool do you use","does anyone know a tool",
 "does anyone know a good","does anyone know any","i wish there was","looking for a tool",
 "looking for a library","looking for a way to","is there a self-hosted","is there an open source",
 "i d love a tool","we need a tool","nobody has built","is there an open-source",
 "is there a way of","any tool that","is there anything like",
]
FLOOR=1704067200  # 2024-01-01
URL=re.compile(r"https?://\S+"); TAG=re.compile(r"<[^>]+>")
def fetch(query,page):
    p={"query":query,"hitsPerPage":"100","page":str(page),
       "tags":"comment","numericFilters":"created_at_i>%d"%FLOOR}
    url=BASE+"?"+urllib.parse.urlencode(p)
    req=urllib.request.Request(url,headers={"User-Agent":"think-free-research"})
    with urllib.request.urlopen(req,timeout=30) as r: return json.load(r)
seen=set(); n=0
with open("hn_recent.jsonl","w") as f:
    for trig in TRIGGERS:
        for page in range(0,10):
            try: d=fetch(trig,page)
            except Exception as e:
                print("ERR",trig,page,repr(e)[:80],file=sys.stderr); time.sleep(2); break
            hits=d.get("hits") or []
            if not hits: break
            for h in hits:
                oid=h.get("objectID")
                if oid in seen: continue
                seen.add(oid)
                txt=TAG.sub(" ",h.get("comment_text") or "")
                low=txt.lower()
                if trig not in low: continue
                if len(URL.findall(txt))>=3: continue
                body=URL.sub(" ",txt)
                body=re.sub(r"&#x27;|&#39;|&quot;|&gt;|&lt;|&amp;"," ",body)
                body=re.sub(r"[^A-Za-z0-9 ,'\.\-\+/]"," ",body)
                body=re.sub(r"\s+"," ",body).strip()
                if len(body)<60: continue
                f.write(json.dumps({"id":oid,"trigger":trig,"story":h.get("story_title"),
                    "story_id":h.get("story_id"),"created":h.get("created_at"),
                    "created_i":h.get("created_at_i"),"text":body[:1600]})+"\n"); n+=1
            time.sleep(0.3)
print("kept",n,"from",len(seen),"scanned (>= 2024-01-01)")
