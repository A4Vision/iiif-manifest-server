"""
Given a directory -
    create a manifest for each sub directory.
    create a workspace with all the directories.
    listen to filesystem changes inside the directories -
        upon a modification - update the relevant manifest, and optionally the workspace file.

An image is identified by its content AND its suffix - whatever comes after
the last -- in the file name.

The annotations of an image are saved by its hash - hash of image content and possibly -
    part of the image name - whatever comes after the last "--" in its name -
     is part of the hash
"""
import json
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
from iiif import workspace
from iiif.workspace import ManifestSpec


from iiif.canvas_id_calculator import CanvasIDCalc
from iiif.filesystem_scanner import ManifestsFromDir
from iiif.manifest_creator import ManifestBuilder, CanvasBuilder

from pathlib import Path

from iiif.docker_runner import DockerRunner
from iiif.iiif_server import IIIFServer

SUFFIXES = (".tif", ".tiff")


def main(dir_to_serve: Path, port: int):
    server = IIIFServer(dir_to_serve, port, DockerRunner.create())
    from_dir = ManifestsFromDir(dir_to_serve, SUFFIXES)
    cache_path = dir_to_serve / ".mirador_hash_cache.pkl"
    if cache_path.is_file():
        c = CanvasIDCalc.load_from_file(cache_path)
    else:
        c = CanvasIDCalc({})

    manifests = []
    for dir_path, images in from_dir.find_dirs_with_images().items():
        location = dir_to_serve / "other" / "manifests" / (dir_path.name + ".json")
        builder = ManifestBuilder(server, location)
        for image_path in images:
            canvas_id = c.id_of(image_path)
            canvas_builder = CanvasBuilder(Path(canvas_id), image_path, server)
            canvas_builder.set_label(image_path.stem)
            builder.add_canvas(canvas_builder.build())
        manifests.append(ManifestSpec(uri=server.path_to_url(location), location=dir_path.stem))
        builder.save()
    w = workspace.create_workspace(manifests)
    with open(dir_to_serve / "other" / "workspace.json", "w") as f:
        json.dump(w, f)
    c.dump_to_file(cache_path)
    server.run_server()


if __name__ == '__main__':
    main(Path("/home/bugabuga/beni"), 37474)
