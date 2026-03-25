import pytesseract as tess
import cv2 as cv
import numpy as np
from PIL import Image
import pymupdf
from handler.abstract_handler import *


class TextHandler(AbstractHandler):
    def __init__(self):
        super().__init__()

    
    def handle(self, request: Any) -> Any:
        pass

    
    def retrieve_text_from_image(self, img):
        print(tess.image_to_string(img))


    