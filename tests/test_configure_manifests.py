import os
import tempfile
import unittest
from pathlib import Path

from iiif.filesystem_scanner import ManifestsFromDir
from iiif.util import _fix_linux_path


class ManifestsFromDirsTest(unittest.TestCase):
    def setUp(self):
        self._root = Path(tempfile.mkdtemp())
        self.maxDiff = 2000

    def test_recognize_images(self):
        self._create_files(["dir1/dir2/a.tiff", "dir1/dir2/b.tiff",
                            "dir3/c.tiff", "dir3/d.tiff",
                            "dir1/e.tiff", "dir1/dir4/f.tiff"])
        resolver = ManifestsFromDir(self._root, [".tiff", ".tif"])
        dir2images = resolver.find_dirs_with_images()
        expected_dirs = {"dir1": ["e.tiff"], "dir1/dir4": ["f.tiff"],
                         "dir3": ["c.tiff", "d.tiff"], "dir1/dir2": ["a.tiff", "b.tiff"]}
        expected = {self._root / _fix_linux_path(dir_relative):
                        {self._root / _fix_linux_path(dir_relative) / fname
                         for fname in fnames}
                    for dir_relative, fnames in expected_dirs.items()}
        print(expected)
        print(dir2images)
        self.assertDictEqual(expected, dir2images)

    def _create_files(self, relative_fnames):
        for relative_fname in relative_fnames:
            f = self._root / _fix_linux_path(relative_fname)
            f.parent.mkdir(parents=True, exist_ok=True)
            f.write_text(f.stem)
