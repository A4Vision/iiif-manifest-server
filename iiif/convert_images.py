import sys
import os
import subprocess
import pathlib

def command(src_image, target_image):
    return f'vips tiffsave "{src_image}" "{target_image}" --compression deflate --pyramid --tile --tile-height 256 --tile-width 256'


def main(d):
    d = pathlib.Path(d)
    l_files = list(d.iterdir())
    for f in l_files:
        if f.is_file():
            if f.suffix.lower() in ['.tiff', '.tif'] and 'editted' not in f.stem:
                target = f.parent / (f.stem + '_editted' + f.suffix)
                if target not in l_files:
                    cmd = command(str(f), str(target))
                    print(cmd)
                    try:
                        subprocess.check_call(cmd, shell=True)
                    except Exception as e:
                        print("error with file", f)
                        print("keeping running...")


if __name__ == '__main__':
    main(sys.argv[1])
