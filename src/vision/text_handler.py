import pytesseract as tess
import numpy as np


class TextHandler():
    def __init__(self):
        super().__init__()

    def process(self, image):
        return tess.image_to_string(image)
    
    def retrieve_text_from_image(self, img):
        print(tess.image_to_string(img))


    