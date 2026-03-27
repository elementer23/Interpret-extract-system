from ultralytics import YOLO

class DetectionHandler():
    def __init__(self):
        super().__init__()


    def process(self, image):
        # model = YOLO('yolo26n.pt', task='detect')
        model = YOLO("yolo26n-obb.pt")
        results = model(source=image)
        # results = model(["image1.jpg", "image2.jpg"])  # return a list of Results objects

        relevant = []

        for result in results:
            xywhr = result.obb.xywhr
            names = [result.names[cls.item()] for cls in result.obb.cls.int()]  # class name of each box
            confs = result.obb.conf  # confidence score of each box

            relevant.append(xywhr)
            relevant.append(names)
            relevant.append(confs)
        return relevant