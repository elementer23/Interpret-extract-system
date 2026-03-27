import cv2 as cv
import numpy as np
from PIL import Image
import pymupdf
from vision.text_handler import TextHandler


class ImageHandler():
    def __init__(self):
        super().__init__()
        self.text_handler = TextHandler()
    
    def process(self, image):

        image = cv.cvtColor(image, cv.COLOR_RGBA2BGR)
        image = cv.cvtColor(image, cv.COLOR_RGB2BGR)
        kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])

        image = cv.filter2D(image, -1, kernel)
        # image = cv.medianBlur(image, 11)

        return image
        

    def pdf_to_image_opencv_numpyarray(self, file):
        doc = pymupdf.open(file)
        for page in doc:
            zoom = 300 / 72
            mat = pymupdf.Matrix(zoom, zoom)
            pix = page.get_pixmap(matrix=mat)

            img = np.frombuffer(pix.samples, dtype=np.uint8)

            if pix.n == 4:
                img = img.reshape(pix.height, pix.width, 4)
                img = cv.cvtColor(img, cv.COLOR_RGBA2BGR)
            else:
                img = img.reshape(pix.height, pix.width, 3)
                img = cv.cvtColor(img, cv.COLOR_RGB2BGR)

            self.text_handler.retrieve_text_from_image(img)
            return img
        doc.close()        

    def pdf_to_image_PIL_show(self, file):
        doc = pymupdf.open(file)
        for page in doc:
            zoom = 3.5
            mat = pymupdf.Matrix(zoom, zoom)
            pix = page.get_pixmap(matrix=mat)
            img = Image.frombytes("RGB", \
                                [pix.width, pix.height], \
                                pix.samples)
            img = img.convert("L")
            page_array = np.array(img)

            cleaned_page_array = cv.adaptiveThreshold(page_array, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY, 27, 20)
            img = Image.fromarray(cleaned_page_array)

            img.show()

        doc.close()




