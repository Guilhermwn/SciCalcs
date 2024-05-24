# ------------------------------------------------
# IMPORTAÇÕES

import os
from pathlib import Path

class Detector():
    def __init__(self, pages_folder:str):
        self.pages_folder = pages_folder

    def list_pages(self):
        pages_path = Path(os.getcwd())/self.pages_folder
        pages = os.listdir(pages_path)
        list = []
        for page in pages:
            name = page.split('.')[0]
            list.append(name.capitalize())
        return list