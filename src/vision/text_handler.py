from src.config import DEVICE
import pytesseract as tess
from pytesseract import Output
from utils.utilities import BasicUtils
import re
from domain.domain import TextDetectionBox, RawData
import numpy as np
import cv2 as cv 
import easyocr

class TextHandler():
    """TextHandler class.
    
    One of the base handlers to build a Pipeline. TextHandler is usually one of the last in the Pipeline order.
    This is where the pdf has been converted and has been enhanced beforehand, before it's pushed in the 'OCR'.
    Where the data of the 'OCR' is extracted for each individual image, before it's saved and appended to the text_box list.
    The TextHandler can be used as a stand-alone handler, if the text, positions etc. have to be exported out of an image.
    """
    def __init__(self):
        super().__init__()
        use_gpu_boolean = (DEVICE.type == "cuda")
        self.reader = easyocr.Reader(['en'], gpu=use_gpu_boolean)
        self.clean_regex = re.compile(r"[\s:\\|.+\_<>\^*{}()\[\]—=\-~;\"]+")

    def process(self, context):
        """The process function. This is the process function of the TextHandler, usually one of the last handlers in the build.
        Here the PipeContext is given along, where the pdf or pdf's have been converted to images, have been enhanced and have been
        cropped, depending on symbol coördinates.
        The EasyOCR OCR is then run over these crops, where the text, position and type of each individual annotation is saved.
        Or at least the one's it could find.
         
        For now each finding needs to have a confidence score off 30 or above.

        :type context: PipeContext
        :param context: the PipeContext instance that is given to the Pipeline build. Contains the necessary information, to extract data from.
        """
        if context.progress_callback:
            context.progress_callback(0)

        amount_of_files = len(context.yolo_data)

        for i, yolo_box in enumerate(context.yolo_data):
            data = []

            current_image = context.image_s[i]
            grayed_image = cv.cvtColor(current_image, cv.COLOR_BGR2GRAY) if len(current_image.shape) > 2 else current_image

            for box in yolo_box:
                pts = box.offset_box[0].reshape((-1, 1, 2)).astype(np.int32)
                x, y, w, h = cv.boundingRect(pts)
                raw_crop = grayed_image[y:y+h, x:x+w]
                
                if raw_crop.size > 0:
                    results = self.reader.readtext(raw_crop, allowlist='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ-+±', paragraph=False, workers=0)

                    for (bbox, text, prob) in results:
                        if prob > 0.3:  

                            local_pts = np.array(bbox).astype(np.int32)
                            offset = np.array([x, y])
                            global_pts = local_pts + offset
                            text_pts_global = global_pts.reshape((-1, 1, 2))

                            grid_pos = next(self.__get_grid_position(text_pts_global, current_image.shape[0], current_image.shape[1]))
                            safe_global_pts = text_pts_global.copy()
                            
                            text_pts = np.array(bbox).astype(np.int32).reshape((-1, 1, 2))
                            # cv.polylines(raw_crop, [text_pts], True, (0, 255, 0), 2)
                            data.append(RawData(text, prob, box.symbol_id, safe_global_pts, (x, y, w, h), grid_pos))
                            
            if context.progress_callback:
                current_file = i + 1
                percentage = int((current_file / amount_of_files) * 100)
                context.progress_callback(percentage)

            context.combo_data.append(data)

    def __get_grid_position(self, coords, height, width):
        """
        determines the position of the symbol coordinates through a grid structure of 3x3

        Args:
            coords (numpy array): the coordinates of the symbols in polygon format  
            height (int): the pixel height of the converted file
            width (int): the pixel width of the converted file

        Yields:
            str: yields a string with the position in a basic format 'links-boven', 'midden', 'rechts-onder', etc.
        """
        positions = [["links-boven", "midden-boven", "rechts-boven"],
                     ["links-midden", "midden", "rechts-midden"],
                     ["links-onder", "midden-onder", "rechts-onder"]]
        
        x, y, w, h = cv.boundingRect(coords)
        center_x = (x + w / 2)
        center_y = (y + h / 2)

        col_idx = min(int(center_x / (width / 3)), 2)
        row_idx = min(int(center_y / (height / 3)), 2)

        yield positions[row_idx][col_idx]
    
    def read_tesseract(self, context):
        """
        Tesseract OCR, this function will not work if the pipeline hasn't been build beforehand. Has to consist out of the
        filehandler and imagehandler at least. Since the files have to be processed first. Before finally giving the context
        of the pipeline to this function.

        For now each finding needs to have a confidence score off 20 or above. Each finding is required to have a value in it,
        it can't be an empty string. And all unnecessary special characters, that aren't connected to a letter, number or special character,
        will be filtered out by regex and skipped. All results will be therefore normalized, turning them into uppercase. 

        :type context: PipeContext
        :param context: the PipeContext instance that is given to the Pipeline build. Contains the necessary information, to extract data from.
        """

        if context.progress_callback:
            context.progress_callback(0)

        amount_of_files = len(context.image_s)

        # The list of images will be looped over
        for i in range(amount_of_files):
            
            # tesseracts image to data function will then be used on each value
            data = tess.image_to_data(context.image_s[i], output_type=Output.DICT)
            lis = []

            # Each text the OCR could find, will be looped over.
            # for j in range(len(data['text'])):
            for text, conf, left, top, width, height in zip(
                data['text'], data['conf'], data['left'], data['top'], data['width'], data['height']
            ):
                # Everything unnecessary or invalid, will be filtered out.
                if text is None or not text.strip():
                    continue
                    # The x, y, width and height positions of each item is assigned
                try:
                    conf_score = int(float(conf))
                except (ValueError, TypeError):
                    continue
                
                # The confidence score of each item will be checked and has to be over 20
                if conf_score > 20:
                    reg_text = self.method_regex(text)
                    if len(reg_text) > 0:
                        # The text will be normalized
                        normalized_text = self.normalize_text(text)
                        
                        # The category of the item, the item itself and the coordinates are added to a class object and added to a list.
                        lis.append(TextDetectionBox(
                            type=BasicUtils.categorize(text), 
                            text=normalized_text, 
                            x=left, y=top, w=width, h=height
                        ))

            if context.progress_callback:
                current_file = i + 1
                percentage = int((current_file / amount_of_files) * 100)
                context.progress_callback(percentage)

            # append all the data from each individual image, to an all encompassing list. Which is then returned at the end of Pipeline build.
            context.text_boxes.append(lis)

    def method_regex(self, val):
        """This function filters out all unnecessary special characters, turning them into empty spaces.
        This does not mean every single special character, only the one's that aren't connected to anything.

        :type val: Any
        :param val: the value to be filtered.

        :return string: will return the filtered value.
        """
        return self.clean_regex.sub("", val)
    
    def normalize_text(self, val: str):
        """This function somewhat normalizes the given value. 
        For now it only turns the value into uppercase, but other mods can be added later on.
        (if needed).

        :type val: string
        :param val: the value to be normalized.

        :return string: return the value that is normalized.
        """
        return val.strip().upper()


