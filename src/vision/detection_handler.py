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
        model = YOLO("core_pid_model.pt")
        # relevant = []
        # for detection_file in context.image_s:
        #     results = model(detection_file)

        #     for result in results:

        #         xywhr = result.obb.xywhr  # center-x, center-y, width, height, angle (radians)
        #         xyxyxyxy = result.obb.xyxyxyxy  # polygon format with 4-points
        #         names = [result.names[cls.item()] for cls in result.obb.cls.int()]  # class name of each box
        #         confs = result.obb.conf  # confidence score of each box

        #         relevant.append(xywhr)
        #         relevant.append(xyxyxyxy)
        #         relevant.append(names)
        #         relevant.append(confs)
        #         result.show()

            
        tile_size = 640
        overlap = 100
        # # coor = []

        for detection_file in context.image_s:

            relevant = []
            
            h, w, _ = detection_file.shape

            for y in range(0, h, tile_size - overlap):
                for x in range(0, w, tile_size - overlap):
                    tile = detection_file[y:y+tile_size, x:x+tile_size]

                    if tile.shape[0] < 10 or tile.shape[1] < 10:
                        continue

                    results = model.predict(tile, imgsz=640, conf=0.15)
                    for r in results:
                        if r.obb is not None:
                            boxes = r.obb.xyxyxyxy.cpu().numpy()
                            confidences = r.obb.conf.cpu().numpy()

                        for box, conf in zip(boxes, confidences):
                            offset_box = box.copy()
                            offset_box[:, 0] += x
                            offset_box[:, 1] += y

                            relevant.append((offset_box, conf))
            
            context.yolo_data.append(relevant)
                # print(result)
        #         for box in result.boxes:
        #             x1, y1, x2, y2 = map(int, box.xyxy[0])

        #             coor.append(x1)
        #             coor.append(y1)
        #             coor.append(x2)
        #             coor.append(y2)
        # #         xywhr = result.obb.xywhr  # center-x, center-y, width, height, angle (radians)
        # #         x, y, w, h, r = result.obb.xywhr
        # #         xyxyxyxy = result.obb.xyxyxyxy  # polygon format with 4-points
        # #         names = [result.names[cls.item()] for cls in result.obb.cls.int()]  # class name of each box
        # #         confs = result.obb.conf  # confidence score of each box

        # #         relevant.append(xywhr)
        # #         relevant.append(xyxyxyxy)
        # #         relevant.append(names)
        # #         relevant.append(confs)
        # #         coor.append(x)
        # #         coor.append(y)
        # #         coor.append(w)
        # #         coor.append(h)
        # #         coor.append(r)
        # #         result.show()

        # print(coor)
        # print(relevant)
        # return relevant