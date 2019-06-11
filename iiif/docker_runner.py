import abc
import os
import pathlib
import re
import socket
import subprocess
from contextlib import closing


class DockerRunner(abc.ABC):
    @abc.abstractmethod
    def kill_running_dockers(self):
        pass

    @abc.abstractmethod
    def run_docker(self, image_name: str, port: int, dir_to_serv: pathlib.Path):
        pass

    @abc.abstractmethod
    def kill_image(self, image_name: str):
        pass

    @classmethod
    def create(cls):
        if os.name == 'posix':
            return LinuxDockerRunner()
        else:
            return WindowsDockerRunner()


class WindowsDockerRunner(DockerRunner):
    def _is_port_open(self, port: int):
        with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
            return sock.connect_ex(("localhost", port)) == 0

    def _running_containers(self):
        x = subprocess.run("docker container ls", shell=True, stdout=subprocess.PIPE)
        return re.compile("\n([^ ]+)").findall(x.stdout.decode("utf8"))

    def kill_running_dockers(self):
        for container_id in self._running_containers():
            subprocess.run(f"docker kill {container_id}", shell=True)

    def run_docker(self, image_name: str, port: int, dir_to_serv: pathlib.Path):
        assert not self._is_port_open(port)
        p1 = dir_to_serv / "images"
        p2 = dir_to_serv / "other"
        cmd = f"docker run -d -P --name {image_name} " + \
              f"-v \"{p1}\":/var/www/localhost/images " \
                  f"-v \"{p2}\":/var/www/localhost/other " + \
              f"-p {port}:80 bdlss/iipsrv-openjpeg-docker"
        print("cmd=", cmd)
        subprocess.run(cmd, shell=True)

    def kill_image(self, image_name: str):
        subprocess.run(f"docker stop {image_name}")


class LinuxDockerRunner(DockerRunner):
    def _is_port_open(self, port: int):
        with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
            return sock.connect_ex(("localhost", port)) == 0

    def _running_containers(self):
        x = subprocess.run("docker container ls", shell=True, stdout=subprocess.PIPE)
        return re.compile("\n([^ ]+)").findall(x.stdout.decode("utf8"))

    def kill_running_dockers(self):
        for container_id in self._running_containers():
            subprocess.run(f"docker kill {container_id}", shell=True)

    def run_docker(self, image_name: str, port: int, dir_to_serv: pathlib.Path):
        assert not self._is_port_open(port)
        cmd = f"docker run -d -P --name {image_name} " + \
              f"-v {dir_to_serv}/images:/var/www/localhost/images " \
                  f"-v {dir_to_serv}/other:/var/www/localhost/other " + \
              f"-p {port}:80 bdlss/iipsrv-openjpeg-docker"
        print("cmd=", cmd)
        subprocess.run(cmd, shell=True)

    def kill_image(self, image_name: str):
        subprocess.run(f"docker stop {image_name}")
