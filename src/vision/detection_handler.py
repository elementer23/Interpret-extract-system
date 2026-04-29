from ultralytics import YOLO

class DetectionHandler():
    """DetectionHandler class.
    
    Used to handle the yolo data and functionalities.
    One of the base handlers, for the pipeline.
    """
    def __init__(self):
        super().__init__()

    def process(self, context):
        """The process function. Mainly used as one of the last handlers in a pipeline build.
        Uses an ai-model and Yolo to detect specific symbols, through the 'obb' task.
        Retrieves the positional arguments of these symbols and returns their:
        positions (x,y,height,width,angle), polygon points, names and confidence score.

        :type context: PipeContext
        :param context: gives the PipeContext class with all the necessary data. 
        """
        model = YOLO("best.pt", task="obb")
        results = model(source=context.image)

        relevant = []

        for result in results:
            xywhr = result.obb.xywhr  # center-x, center-y, width, height, angle (radians)
            xyxyxyxy = result.obb.xyxyxyxy  # polygon format with 4-points
            names = [result.names[cls.item()] for cls in result.obb.cls.int()]  # class name of each box
            confs = result.obb.conf  # confidence score of each box

            relevant.append(xywhr)
            relevant.append(xyxyxyxy)
            relevant.append(names)
            relevant.append(confs)
            result.show()
        return relevant