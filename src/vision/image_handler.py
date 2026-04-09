import cv2 as cv
import numpy as np
from PIL import Image
import pymupdf
import matplotlib.pyplot as plt


class ImageHandler():
    def __init__(self):
        super().__init__()
    
    def process(self, context):

        for i in range(len(context.image_s)):
            context.image_s[i] = cv.cvtColor(context.image_s[i], cv.COLOR_RGBA2BGR)
            context.image_s[i] = cv.cvtColor(context.image_s[i], cv.COLOR_RGB2BGR)

            if context.text_handler_present:

                context.image_s[i] = cv.cvtColor(context.image_s[i], cv.COLOR_BGR2GRAY)

                cv.medianBlur(context.image_s[i], 3)
                context.image_s[i] = cv.adaptiveThreshold(context.image_s[i], 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY, 27, 20)

                kernel = np.ones((1,1), np.uint8)
                context.image_s[i] = cv.morphologyEx(context.image_s[i], cv.MORPH_OPEN, kernel)


    def draw_bounding_box(self, image_context, pipeline_context):
        pc = pipeline_context
        ic = image_context

        for i in range(len(pc.text_boxes)):
            for bbx in pc.text_boxes[i]:
                bbxad = bbx.area_domain()
                cv.rectangle(ic.image_s[i], (bbxad['left'], bbxad['top']), (bbxad['left'] + bbxad['width'], bbxad['top'] + bbxad['height']), (0, 255, 0), 2)

            plt.figure(figsize=(10, 10))
            plt.imshow(cv.cvtColor(ic.image_s[i], cv.COLOR_BGR2RGB))
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




