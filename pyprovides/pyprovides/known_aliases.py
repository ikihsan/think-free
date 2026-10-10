#!/usr/bin/env python3
"""Known module -> distribution aliases for common cross-name cases.

These are module names that don't match their distribution name (e.g., 
import sklearn comes from pip install scikit-learn).
"""

# Module name -> distribution name (as it appears on PyPI)
KNOWN_ALIASES = {
    "sklearn": "scikit-learn",
    "yaml": "PyYAML",
    "cv2": "opencv-python",
    "PIL": "Pillow",
    "dateutil": "python-dateutil",
    "MySQLdb": "mysqlclient",
    "psycopg2": "psycopg2-binary",
    "bs4": "beautifulsoup4",
    "Crypto": "pycryptodome",
    "skimage": "scikit-image",
    "jwt": "PyJWT",
    "serial": "pyserial",
    "dotenv": "python-dotenv",
    "OpenSSL": "pyOpenSSL",
    "magic": "python-magic",
    "ldap": "python-ldap",
    "google.protobuf": "protobuf",
    "pkg_resources": "setuptools",
}

# Standard library modules (no distribution needed)
STDLIB_MODULES = frozenset([
    "ctypes", "ctypes.wintypes", "xml.etree.ElementTree", "collections.abc",
    "html", "http", "urllib", "sqlite3", "json", "re", "math", "random",
    "datetime", "decimal", "fractions", "itertools", "functools", "operator",
    "os", "sys", "subprocess", "threading", "multiprocessing", "asyncio",
    "uuid", "hashlib", "hmac", "secrets", "base64", "binascii", "struct",
    "pickle", "shelve", "csv", "configparser", "logging", "traceback",
    "warnings", "contextlib", "abc", "inspect", "textwrap", "string", "time",
    "calendar", "locale", "gettext", "copy", "pprint", "reprlib", "numbers",
    "collections", "heapq", "bisect", "array", "weakref", "types", "importlib",
    "pkgutil", "modulefinder", "runpy", "importlib.util", "importlib.machinery",
    "pathlib", "typing", "dataclasses", "enum", "argparse", "unittest",
    "doctest", "pdb", "profile", "pstats", "timeit", "trace", "gc", "sysconfig",
    "platform", "errno", "signal", "select", "fcntl", "termios", "tty", "pty",
    "resource", "grp", "pwd", "crypt", "spwd", "ossaudiodev", "audioop",
    "wave", "aifc", "sunau", "au", "sndhdr", "colorsys", "imghdr", "sndhdr",
    "tarfile", "zipfile", "gzip", "bz2", "lzma", "zlib", "hashlib", "hmac",
    "md5", "sha", "sha1", "sha224", "sha256", "sha384", "sha512",
    "binascii", "base64", "binhex", "uu", "quopri", "email", "mailbox",
    "mimetypes", "base64", "binascii", "html", "xml", "json", "csv", "toml",
    "configparser", "argparse", "getopt", "optparse", "shlex", "cmd", "readline",
    "rlcompleter", "code", "codeop", "site", "user", "builtins", "__main__",
    "__future__", "warnings", "contextlib", "abc", "typing", "dataclasses",
    "enum", "numbers", "collections", "heapq", "bisect", "array", "weakref",
    "types", "copy", "pprint", "reprlib", "string", "textwrap", "difflib",
    "unicodedata", "stringprep", "readline", "rlcompleter", "getpass", "curses",
    "curses.textpad", "curses.ascii", "curses.panel", "time", "calendar",
    "datetime", "zoneinfo", "timeit", "schedule", "threading", "multiprocessing",
    "concurrent", "concurrent.futures", "subprocess", "sched", "queue",
    "contextvars", "asyncio", "asyncio.events", "asyncio.coroutines",
    "asyncio.tasks", "asyncio.streams", "asyncio.protocols", "asyncio.transports",
    "asyncio.base_events", "asyncio.base_subprocess", "asyncio.base_tasks",
    "asyncio.constants", "asyncio.coroutines", "asyncio.events", "asyncio.exceptions",
    "asyncio.format_helpers", "asyncio.futures", "asyncio.locks", "asyncio.log",
    "asyncio.proactor_events", "asyncio.protocols", "asyncio.queues",
    "asyncio.runners", "asyncio.selector_events", "asyncio.sslproto",
    "asyncio.staggered", "asyncio.streams", "asyncio.subprocess", "asyncio.tasks",
    "asyncio.timeouts", "asyncio.transports", "asyncio.trsock", "asyncio.unix_events",
    "asyncio.windows_events", "asyncio.windows_utils",
])


def is_stdlib(module_name: str) -> bool:
    """Check if a module is in the standard library."""
    top = module_name.split(".")[0]
    return top in STDLIB_MODULES


def get_alias(module_name: str) -> str | None:
    """Get the distribution name for a known alias, or None if not known."""
    return KNOWN_ALIASES.get(module_name)


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        for mod in sys.argv[1:]:
            alias = get_alias(mod)
            if alias:
                print(f"{mod} -> {alias}")
            elif is_stdlib(mod):
                print(f"{mod} -> (stdlib)")
            else:
                print(f"{mod} -> unknown")