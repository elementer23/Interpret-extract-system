from ultralytics import YOLO
from shapely.geometry import Polygon
from shapely.ops import unary_union
import numpy as np
from domain.domain import SymbolDetectionBox
import cv2 as cv

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

        After some changes in the way the ai-model was trained, this function started being a bit different.
        It became far more complex, but it is necessary. The given image or images are procedurally inserted
        into a specific process. An image is split apart into tiles from 640px by 640px, with an overlap of 100px.
        Tiles below a certain size are skipped and tiles with almost nothing on them are skipped as well.
        These tiles and their offsets are then gathered. The gathered tiles are given to the model, 
        to start its prediction process in batches of 16. After the prediction process has finished,
        the coördinates of each piece of a symbol is then allocated on the specific offset of the tile it was found on.
        Each offset is then added to the other (x=x, y=y), so the coördinates that were found on the tile
        can correlate to the corresponding global coördinates of the entire image. 
        After this is done, all the aligning coördinates will be merged by taking one point and deleting
        the points that align with another, until they form one full xyxyxyxy polygon coördinate. 
        Before being send off, as a new original coördinate entry.  

        :type context: PipeContext
        :param context: gives the PipeContext class with all the necessary data. 
        """
        model = YOLO("core_pid_model.pt")
        tile_size = 640
        overlap = 100
        count = 0

        for detection_file in context.image_s:
            grayed_file = cv.cvtColor(detection_file, cv.COLOR_BGR2GRAY)
            file_to_detect = cv.cvtColor(grayed_file, cv.COLOR_GRAY2BGR)

            relevant = []
            merged_results = []
            tiles_to_predict = []
            tile_offsets = []
            
            h, w, _ = file_to_detect.shape
            count += 1

            print(f"Working on file number: {count}")

            tiles_skipped = 0

            for y in range(0, h, tile_size - overlap):
                for x in range(0, w, tile_size - overlap):
                    tile = file_to_detect[y:y+tile_size, x:x+tile_size]

                    if tile.shape[0] < 10 or tile.shape[1] < 10:
                        continue

                    if np.std(tile) < 2:
                        tiles_skipped += 1
                        continue

                    tiles_to_predict.append(tile)
                    tile_offsets.append((x, y))

            print(f"Amount of tiles skipped: {tiles_skipped}")
            print(f"Amount of tiles to check: {len(tiles_to_predict)}")

            if tiles_to_predict:
                stream_on = False if len(tiles_to_predict) < 100 else True
                results = model.predict(tiles_to_predict, imgsz=640, conf=0.15, batch=16, stream=stream_on)
                
                for i, r in enumerate(results):
                    x_off, y_off = tile_offsets[i]

                    if r.obb is not None:
                        boxes = r.obb.xyxyxyxy.cpu().numpy()
                        confidences = r.obb.conf.cpu().numpy()

                        for box, conf in zip(boxes, confidences):
                            offset_box = box.copy()
                            offset_box[:, 0] += x_off
                            offset_box[:, 1] += y_off

                            relevant.append((offset_box, conf))

            if relevant:
                symbol_count = 0
                polygonsWithConf = []
                for box, conf in relevant:
                    poly = Polygon(box)
                    if poly.is_valid:
                        polygonsWithConf.append({"poly": poly, "conf": conf})

                temp_polygons = [p["poly"] for p in polygonsWithConf]
                merged_poly_collection = unary_union(temp_polygons)

                if merged_poly_collection.geom_type == 'Polygon':
                    geoms = [merged_poly_collection]
                else:
                    geoms = list(merged_poly_collection.geoms)

                for final_poly in geoms:
                    symbol_count += 1
                    coords = np.array(final_poly.exterior.coords).astype(np.int32)
                    merged_results.append(SymbolDetectionBox((coords, 0.80), f"{count}-{symbol_count}"))

                print(f"Symbols detected: {len(merged_results)}")

            print("Predicting done! Adding to list of coördinates.")
            
            context.yolo_data.append(merged_results)
                