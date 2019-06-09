import time
import os
import pathlib
import shutil

from iiif.docker_runner import LinuxDockerRunner, DockerRunner


class IIIFServer:
    """
    An HTTP + IIIF image server
    """
    DATA_FILE2CREATE = ("context.json", "level2.json", "service_context.json")

    def __init__(self, root_dir: pathlib.Path, port: int, docker_runner: DockerRunner):
        assert root_dir.is_dir()
        self._root = root_dir
        self._iiif_root = self._root
        self._port = port
        self._docker_runner = docker_runner

    def _base_url(self):
        return f"http://localhost:{self._port}"

    def path_to_url(self, local_path: pathlib.Path):
        return self.url_to(local_path.relative_to(self._root))

    def image_path_to_url(self, local_path: pathlib.Path):
        without_images_prefix = local_path.relative_to(self._iiif_root / "images")
        return self.url_to(f"fcgi-bin/iipsrv.fcgi?IIIF={without_images_prefix}")

    def url_to(self, relative_url):
        return f"{self._base_url()}/{str(relative_url).replace(os.path.sep, '/')}"

    def run_server(self):
        self._create_data_files()
        self._image_name = f'iiipimage{int(time.time()) % 10000000}'
        self._docker_runner.kill_running_dockers()
        self._docker_runner.run_docker(self._image_name, self._port, self._root)

    def stop_server(self):
        self._docker_runner.kill_image(self._image_name)

    def _create_data_files(self):
        data_dir = self._root / "other" / "data"
        data_dir.mkdir(parents=True, exist_ok=True)
        for fname in self.DATA_FILE2CREATE:
            import iiif.data
            src = pathlib.Path(iiif.data.__file__).parent / fname
            assert src.is_file()
            shutil.copyfile(src, data_dir / fname)
