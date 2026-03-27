from vision.image_handler import ImageHandler
import numpy as np
import pymupdf

class FileHandler():
    def __init__(self):
        super().__init__()

        self.image_handler = ImageHandler()

    def process(self, file_path):
        doc = pymupdf.open(file_path)
        for page in doc:
            zoom = 300 / 72
            mat = pymupdf.Matrix(zoom, zoom)
            pix = page.get_pixmap(matrix=mat)

            np_buffer = np.frombuffer(pix.samples, dtype=np.uint8)

            if pix.n == 4:
                np_buffer = np_buffer.reshape(pix.height, pix.width, 4)
            else:
                np_buffer = np_buffer.reshape(pix.height, pix.width, 3)

            return np_buffer
        doc.close()        

    

    def select_file(self, file_name):
        self.image_handler.pdf_to_image_PIL_show(file_name[0])

    def select_multi_file(self, file_names):
        for file in file_names:
            self.image_handler.pdf_to_image_PIL_show(file)