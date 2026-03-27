class Pipeline():
    def __init__(self, *args):
        super().__init__()
        if args is not None:
            self.handler = args

    def run(self, class_handlers, data):
        if data is None:
            return

        for handler in class_handlers:
            data = handler.process(data)
        return data