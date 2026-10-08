import json, re, subprocess, sys, tarfile, io, os, urllib.request

def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "think-free-e055"})
    return urllib.request.urlopen(req, timeout=60).read()

def doc_flags(slug):
    for branch in ("main", "master"):
        try:
            tar = get(f"https://codeload.github.com/{slug}/tar.gz/refs/heads/{branch}"); break
        except Exception: continue
    else: return None
    tf = tarfile.open(fileobj=io.BytesIO(tar))
    claimed, helpblocks = set(), set()
    for member in tf:
        if member.name.endswith((".md", ".rst")) and member.size < 400000:
            text = tf.extractfile(member).read().decode("utf-8", "replace")
            claimed.update(re.findall(r"--[a-z][a-z0-9-]+", text))
            for block in re.findall(r"```.*?```", text, re.S):
                if "--help" in block or "Options:" in block or "options:" in block or "usage:" in block.lower():
                    helpblocks.update(re.findall(r"--[a-z][a-z0-9-]+", block))
    return claimed, helpblocks

def exposed(mod, argv0):
    exposed, sub = set(), set()
    queue, seen = [[argv0]], set()
    while queue:
        cmd = queue.pop(0)
        key = " ".join(cmd)
        if key in seen: continue
        seen.add(key)
        try:
            p = subprocess.run(["python3", "-m", mod, *cmd[1:], "--help"], capture_output=True, text=True, timeout=60, env={**os.environ, "PYTHONPATH": "/tmp/opencode/e055/pkgs"})
            out = p.stdout + p.stderr
        except Exception: out = ""
        exposed.update(re.findall(r"--[a-z][a-z0-9-]+", out))
        m = re.search(r"\{([a-z,\-]+)\}", out)
        if m and any(s in out.lower() for s in ("command", "positional")):
            for w in m.group(1).split(","):
                if w != "help": queue.append(cmd + [w])
        m2 = re.search(r"(?:commands|subcommands):\s*\n(.*?)(\n\n|\Z)", out, re.S | re.I)
        if m2:
            for line in m2.group(1).splitlines():
                w = line.strip().split()
                if w and re.match(r"^[a-z][a-z0-9-]*$", w[0]) and w[0] != "help":
                    queue.append(cmd + [w[0]])
    return exposed, seen

if __name__ == "__main__":
    slug, mod, argv0 = sys.argv[1], sys.argv[2], sys.argv[3]
    docs = doc_flags(slug)
    if docs is None: print(json.dumps({"error": "no tarball"})); sys.exit()
    claimed, helpblocks = docs
    exp, seen = exposed(mod, argv0)
    print(json.dumps({"slug": slug, "help_pages": sorted(seen),
        "doc_flags": len(claimed), "exposed_flags": len(exp),
        "doc_not_exposed": sorted(claimed - exp),
        "helpblock_not_exposed": sorted(helpblocks - exp),
        "exposed_not_in_docs": sorted(exp - claimed)}, indent=1))
