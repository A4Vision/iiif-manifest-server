import copy
import hashlib
import pathlib
import pickle
from pathlib import Path
from typing import Dict, Tuple, List

SUFFIX_NOTATION = "--"
BLOCK_SIZE = 1024
JUMP_SIZE = 1024 * 1024


class CanvasIDCalc:
    """
        Calculate ID - function of content, name suffix: string after the last --
    """

    def __init__(self, known_hashes: Dict[Tuple[float, Path], str]):
        self._known_hashes = copy.deepcopy(known_hashes)

    def _ctime(self, path: Path):
        if path.is_file():
            return float(path.stat().st_ctime)
        return -1

    def hash_of(self, image: Path) -> str:
        size = image.stat().st_size
        h = hashlib.md5()
        h.update(str(size).encode('utf8') + b",")
        with open(image, "rb") as f:
            for offset in self._offsets(size):
                f.seek(offset)
                h.update(f.read(BLOCK_SIZE))
        return h.hexdigest()

    def cached_hash_value(self, path: Path):
        ctime = self._ctime(path)
        key = (ctime, path)
        if key in self._known_hashes:
            return self._known_hashes[key]
        else:
            self._known_hashes[key] = self.hash_of(path)
            if ctime == self._ctime(path):
                return self._known_hashes[key]
            else:
                # File was modified - recalculate the hash
                return self.cached_hash_value(path)

    def id_of(self, image: Path) -> str:
        assert image.is_file()
        hash_value = self.cached_hash_value(image)
        suffix = self._suffix(image.stem)
        return hash_value + suffix

    @classmethod
    def load_from_file(cls, path: Path) -> 'CanvasIDCalc':
        with open(path, "rb") as f:
            known = pickle.load(f)
        return CanvasIDCalc({(ctime, pathlib.Path(p)): hash_value for (ctime, p), hash_value
                             in known.items() if pathlib.Path(p).is_file() and isinstance(ctime, float)
                             and isinstance(hash_value, str)})

    def dump_to_file(self, path: Path):
        with open(path, "wb") as f:
            pickle.dump(self._known_hashes, f)

    def _suffix(self, stem):
        if SUFFIX_NOTATION in stem:
            return stem[stem.rfind(SUFFIX_NOTATION) + 2:]
        else:
            return ""

    def _offsets(self, size: int) -> List[int]:
        offsets = range(0, size, JUMP_SIZE)
        if size > BLOCK_SIZE:
            return list(offsets) + [size - BLOCK_SIZE]
        else:
            return list(offsets)
