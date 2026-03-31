import pytesseract as tess
from pytesseract import Output

class TextHandler():
    def __init__(self):
        super().__init__()

    def process(self, image):

        data = tess.image_to_data(image, output_type=Output.DICT)

        for i in range(len(data['text'])):
            x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]
            text = data['text'][i]

            if int(float(data['conf'][i])) > 0:
                print(f"Text: {text}, Position: ({x},{y}), Size: {w}x{h}")

        return tess.image_to_string(image)
    


    