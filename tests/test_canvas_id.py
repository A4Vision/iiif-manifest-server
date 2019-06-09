import random
import tempfile
import time
import unittest
from pathlib import Path

from iiif.canvas_id_calculator import CanvasIDCalc


class CanvasIdTest(unittest.TestCase):
    def _create_temp_file(self):
        res = Path(tempfile.mktemp(suffix=".tiff"))
        res.touch()
        return res

    def test_canvas_hash_is_consistent(self):
        generator = random.Random(1234)

        calc = CanvasIDCalc({})
        image_file = Path(tempfile.mktemp(suffix=".tiff"))
        image_file.touch()
        h1 = calc.hash_of(image_file)
        image_file.touch()
        self.assertEqual(h1, calc.hash_of(image_file))
        image_file.write_bytes(b"abcd" + str(generator.randint(0, 1000)).encode("utf8"))
        h3 = calc.hash_of(image_file)
        self.assertNotEqual(h1, h3)
        self.assertEqual(h3, calc.hash_of(image_file))

    def _delayed_write_bytes(self, path: Path, b: bytes):
        time.sleep(0.05)
        path.write_bytes(b)

    def test_canvas_id(self):
        im1 = self._create_temp_file()
        calc2 = CanvasIDCalc({})
        self._delayed_write_bytes(im1, b"abcd")
        abcd_id = calc2.id_of(im1)
        self._delayed_write_bytes(im1, b"1234")
        self.assertNotEqual(abcd_id, calc2.id_of(im1))
        self._delayed_write_bytes(im1, b"abcd")
        self.assertEqual(abcd_id, calc2.id_of(im1))

        new_path = Path(str(im1) + "--other.tif")
        im2 = Path(str(im1) + "other.tif")

        im1.rename(new_path)
        self.assertNotEqual(abcd_id, calc2.id_of(new_path))

        new_path.rename(im2)
        self.assertEqual(abcd_id, calc2.id_of(im2))

        im2.rename(im1)
        self.assertEqual(abcd_id, calc2.id_of(im1))

    def test_reusing_dump_load(self):
        im1 = self._create_temp_file()
        calc = CanvasIDCalc({})
        before = calc.id_of(im1)
        temp = self._create_temp_file()
        calc.dump_to_file(temp)
        calc2 = CanvasIDCalc.load_from_file(temp)
        self.assertEqual(before, calc2.id_of(im1))
