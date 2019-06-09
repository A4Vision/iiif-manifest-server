import json
import tempfile
import unittest
from pathlib import Path

from iiif.docker_runner import LinuxDockerRunner, DockerRunner
from iiif.manifest_creator import CanvasBuilder, ManifestBuilder
from iiif.iiif_server import IIIFServer


class TestCaseWithRoot(unittest.TestCase):
    def setUp(self):
        super(TestCaseWithRoot, self).setUp()
        self._root = Path(tempfile.mkdtemp())
        self._server = IIIFServer(self._root, 1234, DockerRunner.create())
        self._image1 = Path(self._root) / "images" / "image1.tiff"
        self._image1.parent.mkdir()
        self._image1.touch()



class TestCanvasBuilder(TestCaseWithRoot):
    def test_build_canvas(self):
        builder = CanvasBuilder(Path("canvas1"), self._image1, self._server)
        builder.set_service_context("context1.json")
        builder.set_service_profile("profile.json")

        canvas1 = builder.build()
        builder.set_service_context("context2.json")
        canvas2 = builder.build()
        self.assertEqual("context1.json", canvas1["images"][0]["resource"]["service"]["@context"])
        self.assertEqual("context2.json", canvas2["images"][0]["resource"]["service"]["@context"])

    def test_profile(self):
        builder = CanvasBuilder(Path("canvas1"), self._image1, self._server)
        builder.set_service_context("context1")


class ManifestBuilderTest(TestCaseWithRoot):
    def _create_builder(self):
        self._location = self._root / "manifest.json"
        return ManifestBuilder(self._server, self._location)

    def test_save(self):
        builder = self._create_builder()
        built_manifest = builder.build()
        builder.save()
        loaded = json.load(open(self._location, "r"))
        self.assertDictEqual(loaded, built_manifest)

    def test_set_context(self):
        builder = self._create_builder()
        (self._root / "context1").touch()
        with self.assertRaisesRegex(AssertionError, ".*json.*"):
            builder.set_local_context_path(self._root / "context1")
        with self.assertRaises(FileNotFoundError):
            builder.set_local_context_path(self._root / "context1.json")
        (self._root / "context1.json").touch()
        builder.set_local_context_path(self._root / "context1.json")
        builder.build()

    def test_adding_canvases(self):
        builder = self._create_builder()
        canvas_builder1 = CanvasBuilder(Path("canvas1"), self._image1, self._server)
        canvas_builder2 = CanvasBuilder(Path("canvas2"), self._image1, self._server)
        builder.add_canvas(canvas_builder1.build())
        builder.add_canvas(canvas_builder1.build())
        builder.add_canvas(canvas_builder2.build())
        assert builder.canvas_count() == 2
