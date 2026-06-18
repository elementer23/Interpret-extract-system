from utils.utilities import BasicUtils as u
from vision.text_handler import TextHandler
from enumeration.file_type import FileType
from error.error_hub import ErrorHub

class PipeContext():
    """PipeContext class. 
    
    Acts as an un-inherited connection to the Pipeline class.
    Used as a storage for data to be passed back and forward in the Pipeline.
    If new data has to be added, apply it here, before creating any extra unnecessary parameters in the run function.
    (It's a preference not a must.)

    The progress_callback parameter isn't necessarily required, but once threading is used. It's definitely a must.
    Keeps track of the progress of a function in the pipeline. 

    :type data: Any
    :param data: a parameter to pass any type of data through, mainly used for pdf files. (Main purpose, other behavior has to be implemented seperately).
    """
    def __init__(self, data, progress_callback=None):
        self.image_s = data
        self.text_boxes = []
        self.yolo_data = []
        self.combo_data = []
        self.text_handler_present = False
        self.progress_callback = progress_callback

class Pipeline():
    """Pipeline class.
    
    Acts as the Pipeline for the handlers. Performing sequential actions depending on the order of the added handlers.
    Each official handler is required to have the process function implemented, whom also have to work with the PipeContext class.
    There are no checks to see, whether this rule is applied. But the Pipeline will not work otherwise.
    Can be called as a stand-alone class, without the use of the Handler class. But the arguments still have to be passed.

    :type args: tuple
    :param args: the required handlers given as arguments.
    """
    def __init__(self, *args):
        super().__init__()
        if args is not None:
            self.handler = args

    def run(self, class_handlers, data, progress_callback=None) -> PipeContext | None:
        """This function runs or starts the pipeline.
        This function will essentially accept any type of data, but it will not run on any type of data.
        If no class_handlers are present, it will fail and return None. If the data isn't a list containing file paths
        it will fail and return None. Only Pdf files can be passed through here, any other file type will be filtered out.
        It will return None, if no pdfs were present inside the data.

        Will automatically convert the pdf to an image, but will generate it in a gray format, due to the 'OCR' performance.
        (Which is best on Grayscaling.) Will sharpen the given pdf-turned-to-image and will scale it to 300 dpi. 
        This will cause the positions of certain items, texts etc. to lose it's original position (mainly for consistency.)
        Will turn the single pdf or list of pdfs into MatLike data (opencv). Allowing positions and text etc. to be exported.
        Or used to open as a canvas image. Any other purposes or functionalities have to be added seperately (due to it's single purpose nature).
        
        :type class_handlers: tuple
        :param class_handlers: the tuple of handlers that have to be run.
        :type data: Any
        :param data: the data that has to be processed in the handlers (apply as a copy [:] if necessary)
        :type progress_callback: fn | None
        :param progress_callback: usually a progression function that keeps track of the 'progress' of a function in the pipeline.

        :return PipeContext | None: Will return the given PipeContext instance with the processed data or None if conditions aren't met.
        """
        try:

            if data is None:
                raise Exception
            
            pdf_arr = []
            file_type_list = u.categorize_file_type(data)

            for i in range(len(file_type_list)):
                if file_type_list[i] is FileType.PDF:
                    pdf_arr.append(data[i])

            if not pdf_arr:
                raise Exception
            
            context = PipeContext(pdf_arr[:], progress_callback=progress_callback)
            context.text_handler_present = u.is_class_present(class_handlers, TextHandler)

        except Exception:
            print("The file or files weren't compatible extensions, choose a pdf instead.")
            ErrorHub.error_msg("The file or files weren't compatible extensions, choose a pdf instead.", "information")
            return None
        else:
            for handler in class_handlers:
                handler.process(context)
            return context

        