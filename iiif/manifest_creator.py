import copy
import json
import pathlib
from typing import Union, List, Dict, Tuple

from iiif.iiif_server import IIIFServer

SAMPLES_CANVAS = {
    "@type": "sc:Canvas",
    "@id": "http://localhost:80/canvas1",
    "label": "",
    "width": 100,
    "height": 100,
    "images": [
        {
            "@type": "oa:Annotation",
            "motivation": "sc:painting",
            "on": "http://localhost:80/canvas1",
            "resource": {
                "@type": "dctypes:Image",
                "@id": "http://localhost/fcgi-bin/iipsrv.fcgi?IIIF=PalaisDuLouvre.tif/full/200,/0/default.jpg",
                "service": {
                    "@context": "http://iiif.io/api/image/2/context.json",
                    "@id": "http://localhost:80/fcgi-bin/iipsrv.fcgi?IIIF=PalaisDuLouvre.tif",
                    "profile": "http://iiif.io/api/image/2/level2.json"
                }
            }
        }
    ]
}

SAMPLE_MANIFEST = {
    "@context": "http://iiif.io/api/presentation/2/context.json",
    "@type": "sc:Manifest",
    "@id": "http://localhost:80/manifests/manifest.json",
    "label": "",
    "description": "",
    "attribution": "",
    "sequences": [
        {
            "@type": "sc:Sequence",
            "canvases": [

            ]
        }
    ]
}

ATTRIBUTION, DESCRIPTION, LABEL = "attribution", "description", "label"


class CanvasBuilder:
    def __init__(self, canvas_id: pathlib.Path, image: pathlib.Path, server: IIIFServer):
        self._canvas_dict = copy.deepcopy(SAMPLES_CANVAS)
        self._server = server
        assert image.is_file()
        self._canvas_dict["@id"] = self._image_dict()["on"] = self._server.url_to(canvas_id)
        suffix = "/full/100,/0/default.jpg"
        self._image_dict()["resource"]["@id"] = self._server.image_path_to_url(image) + suffix
        self._set_service_value("@id", self._server.image_path_to_url(image))

    def _image_dict(self):
        return self._canvas_dict["images"][0]

    def set_service_context(self, url: str):
        self._set_service_value("@context", url)

    def set_service_profile(self, url: str):
        self._set_service_value("profile", url)

    def _set_service_value(self, key: str, url: str):
        self._image_dict()["resource"]["service"][key] = url

    def build(self):
        return copy.deepcopy(self._canvas_dict)

    def set_label(self, label: str):
        self._canvas_dict[LABEL] = label


class ManifestBuilder:
    def __init__(self, server: IIIFServer, location: pathlib.Path):
        self._server = server
        self._manifest_dict = copy.deepcopy(SAMPLE_MANIFEST)
        self._location = location
        assert location.suffix == ".json", f"json suffix Expected, actual={location.suffix}"
        self._manifest_dict["@id"] = self._server.path_to_url(location)
        self._canvases_ids = set()

    def save(self):
        manifest = self.build()
        self._location.parent.mkdir(parents=True, exist_ok=True)
        with self._location.open("w") as f:
            json.dump(manifest, f, indent=4, sort_keys=True)

    def __setitem__(self, key: str, value: str):
        assert key in [ATTRIBUTION, DESCRIPTION, LABEL]
        self._manifest_dict[key] = value

    def build(self):
        return copy.deepcopy(self._manifest_dict)

    def add_canvas(self, canvas):
        if canvas["@id"] in self._canvases_ids:
            return
        assert canvas["@id"] not in self._canvases_ids
        self._canvases_ids.add(canvas["@id"])
        self._manifest_dict["sequences"][0]["canvases"].append(canvas)

    def canvas_count(self):
        return len(self._canvases_ids)

    def set_local_context_path(self, context_path: pathlib.Path):
        assert context_path.suffix == ".json", f"json suffix expected, actual={context_path.suffix}"
        if not context_path.is_file():
            raise FileNotFoundError
        self._manifest_dict["@context"] = self._server.path_to_url(context_path)


def get(obj: Union[List, Dict], key: Tuple):
    current = obj
    for k in key:
        current = current[k]
    return current


def is_reachable(url):
    try:
        import requests
        response = requests.get(url)
        return response.ok
    except:
        return True


def validate_many_reachable(obj, keys):
    for url in [get(obj, k) for k in keys]:
        assert is_reachable(url)


def validate_manifest_files_are_reachable(manifest_dict):
    validate_many_reachable(manifest_dict, [("@id",), ("@context",)])

    for canvas in manifest_dict["sequences"][0]["canvases"]:
        image = canvas["images"][0]
        validate_many_reachable(image, [("resource", "@id",),
                                        ("resource", "service", "profile"),
                                        ("resource", "service", "@id"),
                                        ("resource", "service", "@context"),
                                        ])
