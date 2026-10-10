#!/usr/bin/env python3
"""Constants for pyprovides: known aliases, stdlib modules, and configuration."""

import os

__version__ = "0.1.0"

USER_AGENT = "pyprovides/%s" % __version__
EOCD_SIG = b"PK\x05\x06"
CD_SIG = b"PK\x01\x02"
TAIL_BYTES = 65536
CODE_EXT = (".py", ".pyi", ".pyd", ".so", ".dll", ".dylib")
CACHE_DIR = os.environ.get("PYPROVIDES_CACHE", ".pyprovides-cache")
RANKED_CACHE = os.environ.get("PYPROVIDES_RANKED_CACHE", ".pyprovides-ranked.json")
# Local copy from EXPERIMENTS/090-reverse-index/top-pypi-packages.min.json
RANKED_LOCAL = os.path.join(os.path.dirname(__file__), "..", "EXPERIMENTS", "090-reverse-index", "top-pypi-packages.min.json")

# Known aliases for cross-name mappings (module -> distribution)
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

# Standard library modules (top-level names)
STDLIB_MODULES = frozenset([
    "ctypes", "xml", "collections", "html", "http", "urllib", "sqlite3", "json", "re", "math", "random",
    "datetime", "decimal", "fractions", "itertools", "functools", "operator",
    "os", "sys", "subprocess", "threading", "multiprocessing", "asyncio",
    "uuid", "hashlib", "hmac", "secrets", "base64", "binascii", "struct",
    "pickle", "shelve", "csv", "configparser", "logging", "traceback",
    "warnings", "contextlib", "abc", "inspect", "textwrap", "string", "time",
    "calendar", "locale", "gettext", "copy", "pprint", "reprlib", "numbers",
    "heapq", "bisect", "array", "weakref", "types", "importlib",
    "pkgutil", "modulefinder", "runpy", "pathlib", "typing", "dataclasses",
    "enum", "argparse", "unittest", "doctest", "pdb", "profile", "pstats",
    "timeit", "trace", "gc", "sysconfig", "platform", "errno", "signal",
    "select", "fcntl", "termios", "tty", "pty", "resource", "grp", "pwd",
    "crypt", "spwd", "ossaudiodev", "audioop", "wave", "aifc", "sunau",
    "sndhdr", "colorsys", "imghdr", "tarfile", "zipfile", "gzip", "bz2",
    "lzma", "zlib", "md5", "sha", "sha1", "sha224", "sha256", "sha384",
    "sha512", "binhex", "uu", "quopri", "email", "mailbox", "mimetypes",
    "toml", "getopt", "optparse", "shlex", "cmd", "readline", "rlcompleter",
    "code", "codeop", "site", "user", "builtins", "__main__", "__future__",
    "difflib", "unicodedata", "stringprep", "getpass", "curses",
    "zoneinfo", "schedule", "concurrent", "contextvars", "sched", "queue",
])

class ResolveError(Exception):
    """The distribution could not be resolved. Never means 'provides nothing'."""