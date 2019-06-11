from tkinter import filedialog
from tkinter import *
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
from iiif import main
root = Tk()
root.withdraw()
folder_selected = filedialog.askdirectory()
main.main(folder_selected)
