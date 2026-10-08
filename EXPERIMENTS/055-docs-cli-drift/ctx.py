import json, re, sys, tarfile, io, urllib.request
def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "think-free-e055"})
    return urllib.request.urlopen(req, timeout=60).read()
slug = sys.argv[1]; flags = json.load(open(sys.argv[2]))
for branch in ("main", "master"):
    try: tar = get(f"https://codeload.github.com/{slug}/tar.gz/refs/heads/{branch}"); break
    except Exception: continue
tf = tarfile.open(fileobj=io.BytesIO(tar))
texts = []
for m in tf:
    if m.name.endswith((".md", ".rst")) and m.size < 400000:
        texts.append(tf.extractfile(m).read().decode("utf-8", "replace"))
blob = "\n".join(texts)
for f in flags:
    for m in re.finditer(re.escape(f), blob):
        s = max(0, m.start()-70); line = blob[s:m.end()+50].replace("\n", " ")
        print(f, "<<", line.strip()[:130]); break
