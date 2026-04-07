from utils.utilities import BasicUtils as u
from vision.text_handler import TextHandler

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
            return

        context = PipeContext(data)
        context.text_handler_present = u.is_class_present(class_handlers, TextHandler)

        for handler in class_handlers:
            handler.process(context)
        return context