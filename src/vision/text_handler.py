import pytesseract as tess

class TextHandler():
    def __init__(self):
        super().__init__()

    def process(self, image):
        return tess.image_to_string(image)
    


    