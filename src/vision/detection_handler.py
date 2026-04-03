from ultralytics import YOLO

class DetectionHandler():
    def __init__(self):
        super().__init__()


    def process(self, context):
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