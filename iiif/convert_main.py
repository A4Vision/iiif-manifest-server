from tkinter import filedialog
from tkinter import *

import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
from iiif import convert_images
root = Tk()
root.withdraw()
folder_selected = filedialog.askdirectory()
convert_images.main(folder_selected)
