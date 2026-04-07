import pytesseract as tess
from pytesseract import Output
from utils.utilities import BasicUtils
import re
from domain.domain import TextDetectionBox

class TextHandler():
    def __init__(self):
        super().__init__()

    def process(self, context):
        # config = '-c tessedit_char_whitelist=0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ,.()= --psm 3'

        for i in range(len(context.image_s)):

            data = tess.image_to_data(context.image_s[i], output_type=Output.DICT)
            lis = []

            for i in range(len(data['text'])):
                reg_text = self.method_regex(data['text'][i])
                if not len(reg_text) == 0:
                    x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]
                    normalized_text = self.normalize_text(data['text'][i])
                    text = data['text'][i]

                    if int(float(data['conf'][i])) > 20:
                        lis.append(TextDetectionBox(BasicUtils.categorize(text), normalized_text, x, y, w, h))
                        print(f"Text: {text} -> {normalized_text} -> conf score: {int(float(data['conf'][i]))}")

            # return tess.image_to_string(image)
            context.text_boxes.append(lis)

    def method_regex(self, val):
        return re.sub(r"\s+|:+|\\+|\|+|\.+|\++|_+|<+|>+|\*+|\^+|\{+|\}+|\(+|\)+|\[+|\]+|—+|=+|-+|~+|;+|\"+", "", val)
    
    def normalize_text(self, val: str):
        text = val.strip()
        text = text.upper()

        return text
    