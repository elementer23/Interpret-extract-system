import pytesseract as tess
from pytesseract import Output
from utils.utilities import BasicUtils
import re
from domain.domain import TextDetectionBox
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

    def process(self, context):
        """The process function. This is the process function of the TextHandler, usually one of the last handlers in the build.
        Here the PipeContext is given along, where the pdf or pdf's have been converted to images and have been enhanced.
        The Tesseract OCR is then run over these images, where the text, position and type of each individual annotation is saved.
        Or at least the one's it could find.
         
        For now each finding needs to have a confidence score off 20 or above. Each finding is required to have a value in it,
        it can't be an empty string. And all unnecessary special characters, that aren't connected to a letter, number or special character,
        will be filtered out by regex and skipped. All results will be therefore normalized, turning them into uppercase. 

        :type context: PipeContext
        :param context: the PipeContext instance that is given to the Pipeline build. Contains the necessary information, to extract data from.
        """
        # config = '-c tessedit_char_whitelist=0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ,.()= --psm 3'

        # The list of images will be looped over
        for i in range(len(context.image_s)):
            
            # tesseracts image to data function will then be used on each value
            data = tess.image_to_data(context.image_s[i], output_type=Output.DICT)
            lis = []

            # Each text the OCR could find, will be looped over.
            for i in range(len(data['text'])):
                # Everything unnecessary or invalid, will be filtered out.
                reg_text = self.method_regex(data['text'][i])
                if not len(reg_text) == 0:
                    # The x, y, width and height positions of each item is assigned
                    x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]
                    # The text will be normalized
                    normalized_text = self.normalize_text(data['text'][i])
                    text = data['text'][i]
                    # The confidence score of each item will be checked and has to be over 20
                    if int(float(data['conf'][i])) > 20:
                        # The category of the item, the item itself and the coordinates are added to a class object and added to a list.
                        lis.append(TextDetectionBox(BasicUtils.categorize(text), normalized_text, x, y, w, h))
                        print(f"Text: {text} -> {normalized_text} -> conf score: {int(float(data['conf'][i]))}")

            # append all the data from each individual image, to an all encompassing list. Which is then returned at the end of Pipeline build.
            context.text_boxes.append(lis)

    def method_regex(self, val):
        """This function filters out all unnecessary special characters, turning them into empty spaces.
        This does not mean every single special character, only the one's that aren't connected to anything.

        :type val: Any
        :param val: the value to be filtered.

        :return string: will return the filtered value.
        """
        return re.sub(r"\s+|:+|\\+|\|+|\.+|\++|_+|<+|>+|\*+|\^+|\{+|\}+|\(+|\)+|\[+|\]+|—+|=+|-+|~+|;+|\"+", "", val)
    
    def normalize_text(self, val: str):
        """This function somewhat normalizes the given value. 
        For now it only turns the value into uppercase, but other mods can be added later on.
        (if needed).

        :type val: string
        :param val: the value to be normalized.

        :return string: return the value that is normalized.
        """
        text = val.strip()
        text = text.upper()

        return text
    
    def read_crop(self, image_context, pipeline_context):
        ic = image_context
        pc = pipeline_context

        reader = easyocr.Reader(['en'], gpu=False)

        for i in range(len(pc.yolo_data)):
            for box in pc.yolo_data[i]:
                grayed_image = cv.cvtColor(ic.image_s[i], cv.COLOR_BGR2GRAY)
                bbxad = box.area_domain()
                pts = bbxad['offset'][0].reshape((-1, 1, 2)).astype(np.int32)

                x, y, w, h = cv.boundingRect(pts)
                raw_crop = grayed_image[y:y+h, x:x+w]

                if raw_crop.size > 0:
                    results = reader.readtext(raw_crop, allowlist='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ-+±', paragraph=False)

                    for (bbox, text, prob) in results:
                        if prob > 0.3:  
                            
                            text_pts = np.array(bbox).astype(np.int32).reshape((-1, 1, 2))
                            cv.polylines(raw_crop, [text_pts], True, (0, 255, 0), 2)
                            print(f"Gevonden tekst: {text} (score: {prob:.2f})")

                    cv.imshow("EasyOCR Detectie", raw_crop)
                    cv.waitKey(0)

