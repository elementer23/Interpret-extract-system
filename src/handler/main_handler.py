from handler.file_handler import FileHandler
from vision.image_handler import ImageHandler
from vision.text_handler import TextHandler
from vision.detection_handler import DetectionHandler
from handler.pipeline import Pipeline
from typing import Any

class Handler():
    """Handler class. 
    
    Used to build the pipeline with, consists of standard builds. But allows custom.
    """
    def __init__(self):
        super().__init__()

    STANDARD_TEXT_BUILD = (FileHandler(), ImageHandler(), TextHandler())
    STANDARD_DETECTION_BUILD = (FileHandler(), ImageHandler(), DetectionHandler())
    STANDARD_BUILD = (FileHandler(), ImageHandler(), DetectionHandler(), TextHandler())

    def pipeline_builder(self, custom: bool, build_type: Any | None, *args):
        """This function is used to build the pipeline.
        Requiring a boolean to indicate whether it's custom or not. 
        Requiring for the build type to be applied with a pre-created build or None (once the build is custom).
        The pipeline_builder is mainly used for the main handlers: 'detection', 'image', 'text' and 'file' handlers.
        When creating a new handler, it has to be manually added and needs the process functionality.

        :type custom: boolean
        :param custom: a boolean to indicate whether the build will be custom or not.
        :type build_type: Any | None
        :param build_type: a parameter to place a standard build (apply None type when custom).
        :type args: tuple
        :param args: arguments that are used to build the pipeline with, if custom. (Not required when using build_type.)

        :return Pipeline | None: will return a built pipeline or None if one of the conditions isn't met.
        """
        if custom:
            if build_type is None:
                return Pipeline(*args)
            else:
                print("build type has to be none when building custom pipeline")
                return None
        else:
            if build_type is not None:
                return Pipeline(*build_type)
            else:
                print("build type can't be none when using a standard pipeline")
                return None

    