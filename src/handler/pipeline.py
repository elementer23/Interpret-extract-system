from utils.utilities import BasicUtils as u
from vision.text_handler import TextHandler
from enumeration.file_type import FileType

class PipeContext():
    def __init__(self, data):
        self.image_s = data
        self.text_boxes = []
        self.yolo_data = {}
        self.text_handler_present = False

class Pipeline():
    def __init__(self, *args):
        super().__init__()
        if args is not None:
            self.handler = args

    def run(self, class_handlers, data):
        if data is None:
            return "A list of files wasn't given."
        
        pdf_arr = []
        file_type_list = u.categorize_file_type(data)

        for i in range(len(file_type_list)):
            if file_type_list[i] is FileType.PDF:
                pdf_arr.append(data[i])

        if not pdf_arr:
            return "There were no pdf's present inside of the list."

        context = PipeContext(pdf_arr[:])
        context.text_handler_present = u.is_class_present(class_handlers, TextHandler)

        for handler in class_handlers:
            handler.process(context)
        return context