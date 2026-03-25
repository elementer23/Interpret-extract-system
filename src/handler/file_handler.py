from PyQt6.QtWidgets import QFileDialog
from handler.abstract_handler import *

class FileHandler(AbstractHandler):
    def __init__(self):
        super().__init__()

    def handle(self, request: Any) -> Any:
        pass

    def select_file_from_explorer(self, file_names):
        print(file_names)