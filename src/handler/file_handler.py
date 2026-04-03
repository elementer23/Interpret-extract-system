import numpy as np
import pymupdf

class FileHandler():
    def __init__(self):
        super().__init__()

    def process(self, context):
        doc = pymupdf.open(context.image)
        for page in doc:
            zoom = 300 / 72
            mat = pymupdf.Matrix(zoom, zoom)
            pix = page.get_pixmap(matrix=mat)

            np_buffer = np.frombuffer(pix.samples, dtype=np.uint8)

            if pix.n == 4:
                np_buffer = np_buffer.reshape(pix.height, pix.width, 4)
            else:
                np_buffer = np_buffer.reshape(pix.height, pix.width, 3)

            context.image = np_buffer
        doc.close()        
