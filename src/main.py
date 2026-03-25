from PyQt6.QtWidgets import QApplication
from gui.main_window import MainWindow
from handler.handler import Handler
from handler.file_handler import FileHandler
from vision.detection_handler import DetectionHandler
from vision.image_handler import ImageHandler
from vision.text_handler import TextHandler

import sys

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()

def client_code(handler: Handler) -> None:
    pass

if __name__ == "__main__":

    file_handler = FileHandler()
    detection_handler = DetectionHandler()
    image_handler = ImageHandler()
    text_handler = TextHandler()

    file_handler.set_next(image_handler).set_next(detection_handler).set_next(text_handler)