#!/bin/sh
# E047 setup — fetch the shipped hook runners this experiment tests.
#
# Everything lands under $E047_ROOT (default /tmp/opencode/e047), never in the
# repository: these are third-party binaries and a Python venv, and the point of
# the experiment is to run what a user would install, not to vendor it.
#
# Each fetch records the resolved version and the sha256 of the bytes actually
# used, so a result can be tied to the artifact that produced it. A runner that
# cannot be fetched is recorded as such and skipped; it is never approximated.
#
# Usage: sh setup.sh
set -eu

ROOT="${E047_ROOT:-/tmp/opencode/e047}"
mkdir -p "$ROOT/bin" "$ROOT/logs"

say() { printf '%s\n' "$*"; }

# --- node (for the npm-distributed runners) -------------------------------
if [ ! -x "$ROOT/bin/node" ]; then
  ver=$(curl -sS https://nodejs.org/dist/index.json \
        | python3 -c 'import json,sys; print(json.load(sys.stdin)[0]["version"])')
  say "node: fetching $ver"
  curl -sSL -o "$ROOT/logs/node.tar.xz" \
    "https://nodejs.org/dist/$ver/node-$ver-linux-x64.tar.xz"
  sha256sum "$ROOT/logs/node.tar.xz" | tee "$ROOT/logs/node.sha256"
  mkdir -p "$ROOT/node"
  tar -xJf "$ROOT/logs/node.tar.xz" -C "$ROOT/node" --strip-components=1
  say "$ver" > "$ROOT/logs/node.version"
fi
PATH="$ROOT/node/bin:$PATH"
export PATH
say "node: $(node --version)  npm: $(npm --version)"

# --- a current git --------------------------------------------------------
# This VM's system git is 2.25.1. lefthook 2.x refuses to run below 2.31 and
# lint-staged 17 refuses below 2.32, so with the system git the two runners this
# question is actually about cannot execute at all — which would leave the
# experiment's central comparison unmeasured while looking like a result about
# them. Git is therefore built from source, with the tarball's sha256 recorded.
if [ ! -x "$ROOT/git/bin/git" ]; then
  ver=$(curl -sS "https://mirrors.edge.kernel.org/pub/software/scm/git/" \
        | grep -o 'git-2\.[0-9]*\.[0-9]*\.tar\.xz' | sort -V | tail -1 \
        | sed 's/\.tar\.xz//')
  if [ -z "$ver" ]; then
    say "git: could not resolve a version from the kernel.org mirror"
    exit 1
  fi
  say "git: building $ver from source (system git is $(git --version | awk '{print $3}'))"
  curl -sSL -o "$ROOT/logs/git.tar.xz" \
    "https://mirrors.edge.kernel.org/pub/software/scm/git/$ver.tar.xz"
  sha256sum "$ROOT/logs/git.tar.xz" | tee "$ROOT/logs/git.sha256"
  mkdir -p "$ROOT/git-src"
  tar -xJf "$ROOT/logs/git.tar.xz" -C "$ROOT/git-src" --strip-components=1
  # The three switches below are git's own, and each is a part of git these arms
  # never call: NO_RUST because git 2.5x builds a Rust `libgitcore` by default
  # and this VM has no cargo; NO_TCLTK because git-gui needs tcl/tk, which are
  # absent and which no hook runner invokes; NO_GETTEXT for the same reason as
  # --disable-nls. None of them touches the porcelain the experiment drives.
  ( cd "$ROOT/git-src" \
    && ./configure --prefix="$ROOT/git" --without-openssl \
                    --disable-nls CFLAGS="-O1" >"$ROOT/logs/git-configure.log" 2>&1 \
    && make -j"$(nproc)" NO_RUST=1 NO_TCLTK=1 NO_GETTEXT=1 \
         >"$ROOT/logs/git-make.log" 2>&1 \
    && make NO_RUST=1 NO_TCLTK=1 NO_GETTEXT=1 install \
         >>"$ROOT/logs/git-make.log" 2>&1 )
  printf '%s\n' "$ver" > "$ROOT/logs/git.version"
fi
say "git: $("$ROOT/git/bin/git" --version)  (built at $ROOT/git/bin/git)"

# --- lefthook (a released Go binary) --------------------------------------
if [ ! -x "$ROOT/bin/lefthook" ]; then
  say "lefthook: resolving the latest release"
  tag=$(curl -sS https://api.github.com/repos/evilmartians/lefthook/releases/latest \
        | python3 -c '
import json,sys
r = json.load(sys.stdin)
print(r["tag_name"])
')
  say "lefthook: $tag"
  printf '%s\n' "$tag" > "$ROOT/logs/lefthook.version"
  # The release publishes a bare executable, gzipped; there is no tarball. Take
  # the name from the API rather than assembling it, so a change to the naming
  # scheme is an error here instead of a silent 404.
  asset=$(curl -sS "https://api.github.com/repos/evilmartians/lefthook/releases/latest" \
        | python3 -c '
import json,sys
r = json.load(sys.stdin)
want = "Linux_x86_64.gz"
for a in r["assets"]:
    if a["name"].endswith(want):
        print(a["browser_download_url"]); break
else:
    sys.exit("no asset ending " + want)
')
  curl -sSL -o "$ROOT/logs/lefthook.gz" "$asset"
  sha256sum "$ROOT/logs/lefthook.gz" | tee "$ROOT/logs/lefthook.sha256"
  gunzip -c "$ROOT/logs/lefthook.gz" > "$ROOT/bin/lefthook"
  chmod +x "$ROOT/bin/lefthook"
fi
say "lefthook: $("$ROOT/bin/lefthook" version 2>&1 | head -1)"

# --- a current CPython, for pre-commit ------------------------------------
# This VM has Python 3.8 and no python3-venv. pre-commit 3 and 4 require 3.9+,
# so testing pre-commit here without a newer interpreter would test a
# two-major-version-old release and record its behaviour as the current
# behaviour. That is a measurement of the wrong thing, so a standalone CPython
# 3.12 is fetched instead and the version actually used is recorded.
if [ ! -x "$ROOT/py/bin/python3" ]; then
  say "python: fetching a standalone CPython 3.12 (this VM has 3.8, pre-commit 3+ needs 3.9+)"
  url=$(curl -sS https://api.github.com/repos/astral-sh/python-build-standalone/releases/latest \
        | python3 -c '
import json,sys
r = json.load(sys.stdin)
for a in r["assets"]:
    n = a["name"]
    if ("cpython-3.12" in n and "install_only_stripped" in n
            and "x86_64-unknown-linux-gnu" in n and "freethreaded" not in n):
        print(a["browser_download_url"]); break
else:
    sys.exit("no standalone cpython-3.12 asset matched")
')
  curl -sSL -o "$ROOT/logs/python.tar.gz" "$url"
  sha256sum "$ROOT/logs/python.tar.gz" | tee "$ROOT/logs/python.sha256"
  mkdir -p "$ROOT/py"
  tar -xzf "$ROOT/logs/python.tar.gz" -C "$ROOT/py" --strip-components=1
fi
say "python: $("$ROOT/py/bin/python3" --version)"

# --- pre-commit (PyPI) ----------------------------------------------------
if [ ! -x "$ROOT/venv/bin/pre-commit" ]; then
  say "pre-commit: creating the venv"
  rm -rf "$ROOT/venv"
  "$ROOT/py/bin/python3" -m venv "$ROOT/venv"
  "$ROOT/venv/bin/python" -m pip install --quiet --disable-pip-version-check \
    --upgrade pip >"$ROOT/logs/pip.log" 2>&1
  "$ROOT/venv/bin/python" -m pip install --quiet --disable-pip-version-check \
    pre-commit >>"$ROOT/logs/pip.log" 2>&1
fi
"$ROOT/venv/bin/pre-commit" --version | tee "$ROOT/logs/pre-commit.version"

# --- the npm-distributed runners and the formatter ------------------------
# lint-staged and husky are the two npm-distributed hook runners in the
# population, and prettier is the formatter the `stage_fixed` pattern is
# written for. All three go into one throwaway prefix with a real package.json
# listing them: installed separately with --no-save, npm prunes the earlier ones
# as extraneous on the next install, which silently cost this script one run and
# would have produced two arms that do nothing and report "clean".
mkdir -p "$ROOT/npm"
cat > "$ROOT/npm/package.json" <<'JSON'
{
  "name": "e047-runners",
  "private": true,
  "description": "throwaway prefix: the npm hook runners E047 tests",
  "devDependencies": {
    "lint-staged": "latest",
    "husky": "latest",
    "prettier": "latest"
  }
}
JSON
if [ ! -d "$ROOT/npm/node_modules/lint-staged" ] \
   || [ ! -d "$ROOT/npm/node_modules/husky" ] \
   || [ ! -d "$ROOT/npm/node_modules/prettier" ]; then
  say "npm: installing lint-staged, husky and prettier"
  (cd "$ROOT/npm" && npm install --silent --no-audit --no-fund \
    >"$ROOT/logs/npm.log" 2>&1) || say "npm: install FAILED (see logs/npm.log)"
fi
for pkg in lint-staged husky prettier; do
  "$ROOT/node/bin/node" -e '
console.log(require(process.argv[2]).name + " " + require(process.argv[2]).version);
' "$ROOT" "$ROOT/npm/node_modules/$pkg/package.json" 2>/dev/null \
    | tee "$ROOT/logs/$pkg.version" || say "$pkg: NOT INSTALLED"
done

say ""
say "setup complete: $ROOT"