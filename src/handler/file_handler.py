import numpy as np
import pymupdf
import os

class FileHandler():
    def __init__(self):
        super().__init__()

    def process(self, context):
        for i in range(len(context.image_s)):
            doc = pymupdf.open(context.image_s[i])
            for page in doc:
                zoom = 300 / 72
                mat = pymupdf.Matrix(zoom, zoom)
                pix = page.get_pixmap(matrix=mat)

                np_buffer = np.frombuffer(pix.samples, dtype=np.uint8)

                if pix.n == 4:
                    np_buffer = np_buffer.reshape(pix.height, pix.width, 4)
                else:
                    np_buffer = np_buffer.reshape(pix.height, pix.width, 3)

                context.image_s[i] = np_buffer
            doc.close()        

    def get_temp_files_dir(self):
        path = "C:/Users/697/Documents/temp_files"
        files = os.listdir(path)

        return files