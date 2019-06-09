import os
import pathlib
from typing import List, Dict, Set, Iterable


class ManifestsFromDir:
    def __init__(self, root: pathlib.Path, suffixes: Iterable[str]):
        self._root = root
        assert self._root.is_dir()
        self._suffixes = suffixes

    def find_dirs_with_images(self) -> Dict[pathlib.Path, Set[pathlib.Path]]:
        res = {}
        for dirname, dirs, files in os.walk(str(self._root)):
            paths = {pathlib.Path(dirname) / fname for fname in files
                     if self._has_legal_suffix(fname)}
            if len(paths) > 0:
                res[pathlib.Path(dirname)] = paths
        return res

    def _has_legal_suffix(self, fname: str):
        return any(fname.endswith(suffix) for suffix in self._suffixes)



