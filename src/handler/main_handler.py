from handler.file_handler import FileHandler
from vision.image_handler import ImageHandler
from vision.text_handler import TextHandler
from vision.detection_handler import DetectionHandler
from handler.pipeline import Pipeline
from typing import Any

class Handler():
    def __init__(self):
        super().__init__()


    STANDARD_TEXT_BUILD = (FileHandler(), ImageHandler(), TextHandler())
    STANDARD_DETECTION_BUILD = (FileHandler(), ImageHandler(), DetectionHandler())

    def pipeline_builder(self, custom: bool, build_type: Any | None, *args):
        if custom:
            if build_type is None:
                return Pipeline(*args)
            else:
                return "build type has to be none when building custom pipeline"
        else:
            if build_type is not None:
                return Pipeline(*build_type)
            else:
                return "build type can't be none when using a standard pipeline"

    