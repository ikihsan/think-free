#!/usr/bin/env python3
"""pyprovides tests.

The zip-parsing tests build a real zip with zipfile and read it back through
the same entry_names/top_level_modules the tool uses; there is no mock of the
code under test. The network test is real too, and is skipped when PyPI is
unreachable rather than being faked.

Run: python3 -m unittest discover -s pyprovides
"""

import io
import os
import sys
import tempfile
import unittest
import zipfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pyprovides import (entry_names, provides, top_level_modules,  # noqa: E402
                         _central_directory, _pick_wheel)

try:
    import urllib.error
    from pyprovides import pypi
    ONLINE = pypi("numpy")[0]
except Exception:
    ONLINE = False


def central_directory_of(files):
    """Build a real zip in memory and return (whole file, central directory)."""
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as z:
        for name in files:
            z.writestr(name, b"# test payload\n")
    whole = buf.getvalue()
    with zipfile.ZipFile(io.BytesIO(whole)) as z:
        cd = z.comment  # unused; central directory is read from raw bytes
    idx = whole.rfind(b"PK\x05\x06")
    import struct
    cd_size, cd_off = struct.unpack("<II", whole[idx + 12:idx + 20])
    return whole, whole[cd_off:cd_off + cd_size]


class TestTopLevelModules(unittest.TestCase):
    def test_package_directory(self):
        _, cd = central_directory_of(["sklearn/__init__.py", "sklearn/base.py"])
        self.assertEqual(entry_names(cd),
                         ["sklearn/__init__.py", "sklearn/base.py"])
        self.assertEqual(top_level_modules(entry_names(cd)), {"sklearn"})

    def test_single_module_at_root(self):
        _, cd = central_directory_of(["yaml.py", "pkg-1.0.dist-info/METADATA"])
        self.assertEqual(top_level_modules(entry_names(cd)), {"yaml"})

    def test_type_stub_and_compiled_extension(self):
        _, cd = central_directory_of(["cv2.pyi", "_ssl.so", "x.pyd"])
        self.assertEqual(top_level_modules(entry_names(cd)),
                         {"cv2", "_ssl", "x"})

    def test_dist_info_is_never_a_module(self):
        _, cd = central_directory_of(
            ["pkg-1.0.dist-info/METADATA", "pkg-1.0.dist-info/top_level.txt",
             "pkg/__init__.py"])
        self.assertEqual(top_level_modules(entry_names(cd)), {"pkg"})

    def test_data_scripts_are_not_modules(self):
        _, cd = central_directory_of(
            ["pkg-1.0.data/scripts/mytool", "pkg/__init__.py"])
        self.assertEqual(top_level_modules(entry_names(cd)), {"pkg"})

    def test_data_purelib_prefix_is_stripped(self):
        _, cd = central_directory_of(
            ["pkg-1.0.data/purelib/reallib/__init__.py"])
        self.assertEqual(top_level_modules(entry_names(cd)), {"reallib"})

    def test_dotted_directory_is_not_a_module(self):
        _, cd = central_directory_of(["some.data/x.py", "real/__init__.py"])
        self.assertNotIn("some.data", top_level_modules(entry_names(cd)))


class TestEntryNames(unittest.TestCase):
    def test_roundtrip_over_many_entries(self):
        names = ["pkg/mod%d.py" % i for i in range(200)]
        _, cd = central_directory_of(names)
        self.assertEqual(sorted(entry_names(cd)), sorted(names))

    def test_large_directory_spans_the_tail_window(self):
        # A central directory bigger than the 64 KiB window must still parse,
        # because the EOCD is read first and the exact range is then fetched.
        names = ["pkg/%s/mod%d.py" % ("x" * 40, i) for i in range(3000)]
        _, cd = central_directory_of(names)
        self.assertGreater(len(cd), 65536)
        self.assertEqual(len(entry_names(cd)), 3000)


class TestPickWheel(unittest.TestCase):
    def test_prefers_pure_python_wheel(self):
        payload = {"urls": [
            {"packagetype": "bdist_wheel", "filename": "p-1-cp311-cp311-linux_x86_64.whl", "size": 99},
            {"packagetype": "bdist_wheel", "filename": "p-1-py3-none-any.whl", "size": 999},
            {"packagetype": "sdist", "filename": "p-1.tar.gz", "size": 1},
        ]}
        self.assertEqual(_pick_wheel(payload)["filename"], "p-1-py3-none-any.whl")

    def test_smallest_when_no_pure_wheel(self):
        payload = {"urls": [
            {"packagetype": "bdist_wheel", "filename": "p-1-cp311-win_amd64.whl", "size": 99},
            {"packagetype": "bdist_wheel", "filename": "p-1-cp311-manylinux.whl", "size": 5},
        ]}
        self.assertEqual(_pick_wheel(payload)["filename"], "p-1-cp311-manylinux.whl")

    def test_no_wheel_is_none(self):
        self.assertIsNone(_pick_wheel({"urls": [{"packagetype": "sdist"}]}))


@unittest.skipUnless(ONLINE, "PyPI unreachable; network tests skipped, not faked")
class TestAgainstPyPI(unittest.TestCase):
    """These are the arm C negative controls: a name that provides itself."""

    def setUp(self):
        self.tmp = tempfile.mkdtemp()

    def test_self_providing(self):
        for name in ("numpy", "requests", "click"):
            status, mods, detail = provides(name, cache_dir=self.tmp)
            self.assertEqual(status, "ok", name)
            self.assertIn(name, mods, "%s should provide itself; got %s"
                          % (name, sorted(mods)[:5]))
            self.assertLess(detail["bytes_fetched"], detail["wheel_bytes"] + 1)

    def test_shadow_name_is_reported_as_not_providing(self):
        # The measured silent case, restated as an assertion.
        status, mods, detail = provides("Crypto", cache_dir=self.tmp)
        self.assertEqual(status, "ok")
        self.assertNotIn("Crypto", mods)
        self.assertEqual(detail["canonical"], "crypto")

    def test_absent_name_is_not_a_registry_answer_about_modules(self):
        status, mods, _ = provides("reqests", cache_dir=self.tmp)
        self.assertEqual(status, "no-such-project")
        self.assertEqual(mods, set())

    def test_sdist_only_is_its_own_status(self):
        status, _, detail = provides("sklearn", cache_dir=self.tmp)
        self.assertEqual(status, "no-wheel")
        self.assertIn("wheel", detail["why"])

    def test_cache_is_a_pure_acceleration(self):
        a = provides("tqdm", cache_dir=self.tmp)
        second = os.path.getmtime(os.path.join(self.tmp, "tqdm.json"))
        b = provides("tqdm", cache_dir=self.tmp)
        self.assertEqual(a[0], b[0])
        self.assertEqual(a[1], b[1])
        self.assertEqual(second, os.path.getmtime(os.path.join(self.tmp, "tqdm.json")))


if __name__ == "__main__":
    unittest.main()