#!/usr/bin/env python3
"""pyprovides - which distribution provides this module, with nothing installed.

The mechanism this rests on was built and measured in
EXPERIMENTS/085-declared-not-provided. This is a prototype: the resolver's
mechanism and its correctness are observed; its usefulness to anyone is not.

A wheel is a zip file, and a zip's central directory sits at the end of the
file and names every entry. So the full list of modules a distribution ships
can be read with two HTTP Range requests and zero payload bytes. Nothing is
downloaded and nothing is installed, which is the gap this fills: deptry
0.25.1 resolves imports against an installed virtualenv and reports nothing
at all when the project is uninstalled.

Standard library only. Python 3.8+.
"""

from .constants import (__version__, USER_AGENT, EOCD_SIG, CD_SIG, TAIL_BYTES,
                        CODE_EXT, CACHE_DIR, RANKED_CACHE, RANKED_LOCAL,
                        KNOWN_ALIASES, STDLIB_MODULES, ResolveError)
from .core import (_get, _cache_path, _read_cache, _write_cache, pypi,
                   _central_directory, entry_names, top_level_modules,
                   _pick_wheel, provides)
from .find import (_load_ranked_projects, ranked_project_names, find_provider)
from .fix_import import extract_module_names

__all__ = [
    "__version__",
    "USER_AGENT",
    "EOCD_SIG",
    "CD_SIG",
    "TAIL_BYTES",
    "CODE_EXT",
    "CACHE_DIR",
    "RANKED_CACHE",
    "RANKED_LOCAL",
    "KNOWN_ALIASES",
    "STDLIB_MODULES",
    "ResolveError",
    "_get",
    "_cache_path",
    "_read_cache",
    "_write_cache",
    "pypi",
    "_central_directory",
    "entry_names",
    "top_level_modules",
    "_pick_wheel",
    "provides",
    "_load_ranked_projects",
    "ranked_project_names",
    "find_provider",
    "extract_module_names",
]