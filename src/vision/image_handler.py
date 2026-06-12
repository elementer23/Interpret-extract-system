import cv2 as cv
import numpy as np
from PIL import Image
import pymupdf
import matplotlib.pyplot as plt
from core.exporter import Exporter
from utils.settings import PackageSettings
from collections import defaultdict

MAX_KERNEL_LENGTH = 31

class ImageHandler():
    """ImageHandler class.
    
    One of the base handlers for the pipeline.
    Used to handle proper sharpening and color conversions,
    for incoming image data.
    """
    def __init__(self):
        super().__init__()
    
    def process(self, context):
        """The process function. Mainly used to handle the converted data, from the FileHandler.
        Smoothing the image out, sharpening it where necessary and grayscaling or colorscaling it, if necessary.
        Uses 'opencv' to handle the image data, before sending it through in the pipeline.
        Usually the second step in a standard pipeline build, right after the FileHandler.

        :type context: PipeContext
        :param context: the PipeContext instance, that contains the data from the converted pdf's.
        """
        if context.progress_callback:
            context.progress_callback(0)

        amount_of_files = len(context.image_s)

        for i in range(amount_of_files):
            if context.image_s[i].shape[2] == 4:
                context.image_s[i] = cv.cvtColor(context.image_s[i], cv.COLOR_RGBA2BGR)
            else:
                context.image_s[i] = cv.cvtColor(context.image_s[i], cv.COLOR_RGB2BGR)

            if context.progress_callback:
                current_file = i + 1
                percentage = int((current_file / amount_of_files) * 100)
                context.progress_callback(percentage)


    def draw_bounding_box(self, pipeline_context):
        """This function uses the original text box coordinates, obtained from applying 'OCR' on the converted pdf's.
        And draws them as rectangles using the original coordinates, of the given image. Before returning them in a list.

        pipeline context would be all fully converted files, after OCR. Just to apply the text box coordinates from that image.

        :type pipeline_context: PipeContext
        :param pipeline_context: the converted image, after applied effects and OCR, for text box information.

        :return list: a list of converted images, with drawing coordinates applied to them.
        """
        pc = pipeline_context

        arr = []

        for i in range(len(pc.text_boxes)):
            for bbx in pc.text_boxes[i]:
                bbxad = bbx.area_domain()
                cv.rectangle(pc.image_s[i], (bbxad['left'], bbxad['top']), (bbxad['left'] + bbxad['width'], bbxad['top'] + bbxad['height']), (0, 0, 255), 2)

            arr.append(cv.cvtColor(pc.image_s[i], cv.COLOR_BGR2RGB))
        return arr
    

    def __generate_symbol_connection(self, data):
        batch = []
        
        rows = len(data)
        for i in range(rows):
            grouped_batch = defaultdict(list)
            for box in data[i]:
                bbxad = box.area_domain()
                grouped_batch[bbxad['symbol']].append(bbxad["text"])
            batch.append(grouped_batch)
        return batch    
    
    def __generate_flat_space(self, start_y, gap_y, cols, total_items, image):
         if total_items > 0:
            num_rows = ((total_items - 1) // cols) + 1
            flat_height = start_y + (num_rows * gap_y) + 20
            cv.rectangle(image, (0, 0), (image.shape[1], int(flat_height)), (255, 255, 255), cv.FILLED)
            
    def draw_detection_box(self, pipeline_context):
        pc = pipeline_context
        arr = []

        batch = self.__generate_symbol_connection(pc.combo_data)
        batch_per_file = []
        for it in batch:
            batch_per_file.append([(k, v) for k, v in it.items()])

        # x2, y2, w2, h2 = cv.boundingRect(bbxad["offset"])
        # pts = bbxad['offset'][0].reshape((-1, 1, 2)).astype(np.int32)
        # cv.polylines(pc.image_s[i], [pts], isClosed=True, color=(0, 255, 0), thickness=3)

        rows = len(pc.combo_data)
        cols, start_x, start_y, gap_x, gap_y = 4, 40, 60, 500, 40
  
        for i in range(rows):
            for box in pc.combo_data[i]:
                bbxad = box.area_domain()
                x, y, w, h = bbxad["symbol_offset"]
                cv.rectangle(pc.image_s[i], (x, y), (x + w, y + h), (0, 255, 0), 3)

            total_items = len(batch_per_file[i])
            self.__generate_flat_space(start_y, gap_y, cols, total_items, pc.image_s[i])
            for idx, item in enumerate(batch_per_file[i]):
                symbol_id, text_list = item
                filtered_text = f"{symbol_id}: {', '.join(text_list)}"
                grid_col = idx % cols
                grid_row = idx // cols
                text_x = start_x + (grid_col * gap_x)
                text_y = start_y + (grid_row * gap_y)
                cv.putText(pc.image_s[i], filtered_text, (int(text_x), int(text_y)), cv.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2, cv.LINE_AA)

            arr.append(cv.cvtColor(pc.image_s[i], cv.COLOR_BGR2RGB))
        return arr
        
    def pdf_to_image_PIL_show(self, file):
        """A function to instantly convert and show a pdf, as an image. (unused).
        
        :type file: file path - string
        :param file: the path to the file that has to be converted and shown.
        """
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
    """ImageExportHandler class.
    
    Used to save converted pdf's, as images. Applied with corresponding effects, 
    colorscaling and chosen extension. Before saving them in a folder or exporting them
    entirely. Mainly to create a new dataset to train with, if necessary. 
    Can be used to apply effects on images as well, converting image to image.
    Applying effects on the given images. 
    """
    def __init__(self):
        super().__init__()

    def read_to_color(self, file: np.ndarray | str):
        """This functions reads a regular image or numpy array to a color version of itself.
        Keeping it's original color. Do keep in mind, that it's not natural to turn a grayscaled image,
        to a colorscaled image. This will not work for that reason. A grayscaled image, does not retain it's original
        color pallete after all. 

        :type file: np.ndarray | string
        :param file: a file object in the form of it's path string or a numpy array.

        :return MatLike: returns opencv's natural MatLike module, containing the image in a MatLike format.
        """
        if isinstance(file, str):
            image_color = cv.imread(file, cv.IMREAD_COLOR)
            return image_color
        
        if isinstance(file, np.ndarray):
            if file.shape[2] == 4:
                return cv.cvtColor(file, cv.COLOR_RGBA2BGR)
            else:
                return cv.cvtColor(file, cv.COLOR_RGB2BGR)
            

    def read_to_gray(self, file: np.ndarray | str):
        """This functions reads a regular image or a numpy array version of it, to a grayscaled version.
        
        :type file: np.ndarray | string
        :param file: a file object in the form of it's path string or a numpy array.

        :return MatLike: returns opencv's natural MatLike module, containing the image in a MatLike format.
        """
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
        """This functions reads a regular image or a numpy array version of it, to an inverted version.
        Meaning it will first turn it gray and then invert the color, from black to white and white to black.

        :type file: np.ndarray | string
        :param file: a file object in the form of it's path string or a numpy array.

        :return MatLike: returns opencv's natural MatLike module, containing the image in a MatLike format.
        """
        gray_image = self.read_to_gray(file)
        negative_image = 255 - gray_image
        return negative_image
    
    
    def apply_color_type(self, file: np.ndarray | str, config: dict):
        """The main hub to apply the color, according to the choice of the user.
        
        :type file: np.ndarray | string
        :param file: a file object in the form of it's path string or a numpy array.
        :type config: dict
        :param config: a dictionary containing the chosen color type of the user.

        :return MatLike: returns opencv's natural MatLike module, containing the image in a MatLike format.
        """

        match config['color_type']:
            case "gray":
                return self.read_to_gray(file)
            case "color":
                return self.read_to_color(file)
            case "inverted":
                return self.read_to_inverted(file)
            
    def grid_effect(self, file: np.ndarray | str, config: dict, count: int = 0):
        """This function applies a grid effect to the regular image or to the numpy array version of it.
        It does not essentially apply a grid, a literal grid. But it cuts the image into a grid and
        saves each piece as an individual image.

        :type file: np.ndarray | string
        :param file: a file object in the form of it's path string or a numpy array.
        :type config: dict
        :param config: the dictionary containing the necessary file paths, to save each image with.
        :type count: integer
        :param count: an extra parameter to create the connection between the original image and which grid pieces belong to it.
        """

        if isinstance(file, str):
            image = cv.imread(file)

        if isinstance(file, np.ndarray):
            image = file

        tile_size, overlap = config['tile_size'], config['tile_overlap']

        h, w = image.shape[0], image.shape[1]
        count_tiles = 0

        for y in range(0, h, tile_size - overlap):
            for x in range(0, w, tile_size - overlap):
                tile = image[y:y+tile_size, x:x+tile_size]

                if tile.shape[0] < 10 or tile.shape[1] < 10:
                    continue

                if np.std(tile) < 2:
                    continue

                count_tiles += 1

                cv.imwrite(f"{config['save_location']}/{config['archive_name']}/tile-{count_tiles}_image-{count}{config['image_type']}", tile)


    def gaussian_blur_effect(self, file: np.ndarray | str, config: dict):
        """This function applies the Gaussian blur effect on a regular image or the numpy array version.
        Will return the MatLike from opencv, with the effect applied.

        :type file: np.ndarray | string
        :param file: a file object in the form of it's path string or a numpy array.
        :type config: dict
        :param config: unused

        :return MatLike: returns opencv's natural MatLike module, containing the image in a MatLike format.
        """
        if isinstance(file, str):
            image = cv.imread(file)

        if isinstance(file, np.ndarray):
            image = file

        for i in range(1, MAX_KERNEL_LENGTH, 2):
            dst = cv.GaussianBlur(image, (i, i), 0)

            return dst
        
    def median_blur_effect(self, file: np.ndarray | str, config: dict):
        """This function applies the Median blur effect on a regular image or the numpy array version.
        Will return the MatLike from opencv, with the effect applied.

        :type file: np.ndarray | string
        :param file: a file object in the form of it's path string or a numpy array.
        :type config: dict
        :param config: unused

        :return MatLike: returns opencv's natural MatLike module, containing the image in a MatLike format.
        """
        if isinstance(file, str):
            image = cv.imread(file)

        if isinstance(file, np.ndarray):
            image = file

        for i in range(1, MAX_KERNEL_LENGTH, 2):
            dst = cv.medianBlur(image, i)

            return dst


    def apply_effect_type(self, file: np.ndarray | str, config: dict, count: int = 0):
        """The main hub, to apply the effect type on the regular image or the numpy array version.
        
        :type file: np.ndarray | string
        :param file: a file object in the form of it's path string or a numpy array.
        :type config: dict
        :param config: the dictionary containing the corresponding effect type.
        :type count: integer
        :param count: the count to give along, to connect the image and grid. (0 by default)

        :return MatLike: returns opencv's natural MatLike module, containing the image in a MatLike format.
        """

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
        """This function is the main hub of conversion. Applying the colors and effects,
        before saving the image. Accepts a regular image, array of images or numpy array versions.
        Will export the folder afterwards, if that setting has been selected.
        
        :type file: np.ndarray | string | list
        :param file: a file object in the form of it's path string, list or a numpy array.
        :type config: dict
        :param config: the dictionary containing all the settings, before saving the images.
        """

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