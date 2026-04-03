import cv2 as cv
import numpy as np
from PIL import Image
import pymupdf
import matplotlib.pyplot as plt


class ImageHandler():
    def __init__(self):
        super().__init__()
    
    def process(self, context):

        context.image = cv.cvtColor(context.image, cv.COLOR_RGBA2BGR)
        context.image = cv.cvtColor(context.image, cv.COLOR_RGB2BGR)

        if context.text_handler_present:

            context.image = cv.cvtColor(context.image, cv.COLOR_BGR2GRAY)

            cv.medianBlur(context.image, 3)
            context.image = cv.adaptiveThreshold(context.image, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY, 27, 20)

            kernel = np.ones((1,1), np.uint8)
            context.image = cv.morphologyEx(context.image, cv.MORPH_OPEN, kernel)


    def draw_bounding_box(self, image, bounding_boxes: list):
        for bbx in bounding_boxes:
            bbxad = bbx.area_domain()
            cv.rectangle(image, (bbxad['left'], bbxad['top']), (bbxad['left'] + bbxad['width'], bbxad['top'] + bbxad['height']), (0, 255, 0), 2)

        plt.figure(figsize=(10, 10))
        plt.imshow(cv.cvtColor(image, cv.COLOR_BGR2RGB))
        plt.axis('off')
        plt.show()

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




