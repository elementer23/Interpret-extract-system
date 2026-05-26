from vision.text_handler import TextHandler
from handler.file_handler import FileHandler
from vision.image_handler import ImageHandler
from handler.main_handler import Handler

def test_read_tesseract():

    data = [f"Hello.pdf"]

    builder = Handler().pipeline_builder(True, None, FileHandler(), ImageHandler())
    context = builder.run(builder.handler, data[:])

    TextHandler().read_tesseract(context)

    for i in range(len(context.text_boxes)):
        for bbx in context.text_boxes[i]:
            bbxad = bbx.area_domain()
            assert bbxad['text'] == "HELLO"

