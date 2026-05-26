from handler.file_handler import FileHandler
from vision.image_handler import ImageHandler
from vision.text_handler import TextHandler
from vision.detection_handler import DetectionHandler
from handler.pipeline import Pipeline
from handler.main_handler import Handler

MOCK_STANDARD_BUILD = (FileHandler(), ImageHandler(), DetectionHandler(), TextHandler())

def test_pipeline_builder():
    assert Handler().pipeline_builder(False, None, ImageHandler()) is None
    assert True if isinstance(Handler().pipeline_builder(False, MOCK_STANDARD_BUILD), Pipeline) else False
    assert Handler().pipeline_builder(True, MOCK_STANDARD_BUILD) is None
    assert True if isinstance(Handler().pipeline_builder(True, None, ImageHandler()), Pipeline) else False