import cv2 as cv
import numpy as np
from PIL import Image
import pymupdf
import matplotlib.pyplot as plt
from core.exporter import Exporter
from utils.settings import PackageSettings

MAX_KERNEL_LENGTH = 31

class ImageHandler():
    def __init__(self):
        super().__init__()
    
    def process(self, context):

        for i in range(len(context.image_s)):
            if context.image_s[i].shape[2] == 4:
                context.image_s[i] = cv.cvtColor(context.image_s[i], cv.COLOR_RGBA2BGR)
            else:
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


class ImageExportHandler():
    def __init__(self):
        super().__init__()

    def read_to_color(self, file: np.ndarray | str):
        if isinstance(file, str):
            image_color = cv.imread(file, cv.IMREAD_COLOR)
            return image_color
        
        if isinstance(file, np.ndarray):
            if file.shape[2] == 4:
                return cv.cvtColor(file, cv.COLOR_RGBA2BGR)
            else:
                return cv.cvtColor(file, cv.COLOR_RGB2BGR)
            

    def read_to_gray(self, file: np.ndarray | str):
        if isinstance(file, str):
            image_gray = cv.imread(file, cv.IMREAD_GRAYSCALE)
            return image_gray
        
        if isinstance(file, np.ndarray):
            if file.shape[2] == 4:
                image_gray = cv.cvtColor(file, cv.COLOR_RGBA2BGR)
            else:
                image_gray = cv.cvtColor(file, cv.COLOR_RGB2BGR)

            return cv.cvtColor(image_gray, cv.COLOR_BGR2GRAY)
            

    def read_to_inverted(self, file: np.ndarray | str):
        gray_image = self.read_to_gray(file)
        negative_image = 255 - gray_image
        return negative_image
    
    
    def apply_color_type(self, file: np.ndarray | str, config: dict):

        match config['color_type']:
            case "gray":
                return self.read_to_gray(file)
            case "color":
                return self.read_to_color(file)
            case "inverted":
                return self.read_to_inverted(file)


    def grid_effect(self, file: np.ndarray | str, config: dict, count: int = 0):

        if isinstance(file, str):
            image = cv.imread(file)

        if isinstance(file, np.ndarray):
            image = file

        num_rows = 6
        num_cols = 3

        image_height, image_width = image.shape[0], image.shape[1]
        sub_image_height = image_height // num_rows
        sub_image_width = image_width // num_cols

        for row in range(num_rows):
            for col in range(num_cols):
                start_x = col * sub_image_width
                start_y = row * sub_image_height
                end_x = (col + 1) * sub_image_width
                end_y = (row + 1) * sub_image_height

                sub_image = image[start_y:end_y, start_x:end_x]

                cv.imwrite(f"{config['save_location']}/{config['archive_name']}/piece_{row}_{col}-{count}{config['image_type']}", sub_image)


    def gaussian_blur_effect(self, file: np.ndarray | str, config: dict):
        if isinstance(file, str):
            image = cv.imread(file)

        if isinstance(file, np.ndarray):
            image = file

        for i in range(1, MAX_KERNEL_LENGTH, 2):
            dst = cv.GaussianBlur(image, (i, i), 0)

            return dst
        
    def median_blur_effect(self, file: np.ndarray | str, config: dict):
        if isinstance(file, str):
            image = cv.imread(file)

        if isinstance(file, np.ndarray):
            image = file

        for i in range(1, MAX_KERNEL_LENGTH, 2):
            dst = cv.medianBlur(image, i)

            return dst


    def apply_effect_type(self, file: np.ndarray | str, config: dict, count: int = 0):

        match config['effect_type']:
            case "default":
                return file
            case "grid":
                self.grid_effect(file[:], config, count)
                return file
            case "gaussianblur":
                return self.gaussian_blur_effect(file, config)
            case "medianblur":
                return self.median_blur_effect(file, config)


    def conversion(self, file: np.ndarray | str | list, config: dict) -> None:

        if isinstance(file, np.ndarray):
            image = self.apply_color_type(file[:], config)
            image = self.apply_effect_type(image, config)
            cv.imwrite(f"{config['save_location']}/{config['archive_name']}/{config['file_name']}{config['image_type']}", image)

        if isinstance(file, str):
            image = self.apply_color_type(file[:], config)
            image = self.apply_effect_type(image, config)
            cv.imwrite(f"{config['save_location']}/{config['archive_name']}/{config['file_name']}{config['image_type']}", image)

        if isinstance(file, list):
            for i in range(len(file)):
                image = self.apply_color_type(file[i], config)
                image = self.apply_effect_type(image, config, i)
                cv.imwrite(f"{config['save_location']}/{config['archive_name']}/{config['file_name']}-{i}{config['image_type']}", image)

        
        Exporter().execute_package_export(config['save_location'], config['archive_name'], PackageSettings.manage_package(config['export_type']))