import os


def _fix_linux_path(path: str):
    return path.replace("/", os.path.sep)
