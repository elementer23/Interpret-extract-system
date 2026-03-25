from PyQt6.QtWidgets import QFileDialog
from handler.abstract_handler import *
from vision.image_handler import ImageHandler

class FileHandler(AbstractHandler):
    def __init__(self):
        super().__init__()

        self.image_handler = ImageHandler()

    def handle(self, request: Any) -> Any:
        pass

    def select_file(self, file_name):
        self.image_handler.pdf_to_image_PIL_show(file_name[0])

    def select_multi_file(self, file_names):
        self.image_handler.pdf_to_image_PIL_multi_show(file_names)

    def select_file_for_text_extraction(self, file_name):
        self.image_handler.pdf_to_image_opencv_numpyarray(file_name[0])