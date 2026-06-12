from src.config import DEVICE
from ultralytics import YOLO
from shapely.geometry import Polygon
from shapely.ops import unary_union
from shapely.strtree import STRtree
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
        self.model = YOLO("core_pid_model.pt").to(DEVICE)

    def _tile_generator(self, file_to_predict, tile_size, overlap):

        h, w = file_to_predict.shape[:2]

        for y in range(0, h, tile_size - overlap):
            for x in range(0, w, tile_size - overlap):
                tile = file_to_predict[y:y+tile_size, x:x+tile_size]

                if tile.shape[0] < 10 or tile.shape[1] < 10 or np.std(tile) < 2:
                    continue

                if len(tile.shape) > 2:
                    grayed_tile = cv.cvtColor(tile, cv.COLOR_BGR2GRAY)
                    converted_tile = cv.cvtColor(grayed_tile, cv.COLOR_GRAY2BGR)
                else: 
                    converted_tile = cv.cvtColor(tile, cv.COLOR_GRAY2BGR)

                yield converted_tile, (x, y)


    def _predict_batch(self, tiles, offsets, relevant_list):
        results = self.model.predict(tiles, imgsz=640, conf=0.15, batch=len(tiles), verbose=False, device="cpu")

        for i, r in enumerate(results):
            if r.obb is not None:
                x_off, y_off = offsets[i]
                boxes = r.obb.xyxyxyxy.cpu().numpy()
                confidences = r.obb.conf.cpu().numpy()

                for box, conf in zip(boxes, confidences):
                    offset_box = box + np.array([x_off, y_off])
                    relevant_list.append((offset_box, conf))


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
        tile_size = 640
        overlap = 100
        cpu_batch_size = 4

        if context.progress_callback:
            context.progress_callback(0)

        amount_of_files = len(context.image_s)

        for count, detection_file in enumerate(context.image_s, start=1):
            print(f"Working on file number: {count}")

            file_to_predict = detection_file

            relevant = []
            merged_results = []

            tiles_generator = self._tile_generator(file_to_predict, tile_size, overlap)

            current_batch_tiles = []
            current_batch_offsets = []

            for tile, (x_off, y_off) in tiles_generator:
                current_batch_tiles.append(tile)
                current_batch_offsets.append((x_off, y_off))

                if len(current_batch_tiles) == cpu_batch_size:
                    self._predict_batch(current_batch_tiles, current_batch_offsets, relevant)

                    current_batch_tiles.clear()
                    current_batch_offsets.clear()

            if current_batch_tiles:
                self._predict_batch(current_batch_tiles, current_batch_offsets, relevant)

            if relevant:
                polygons = [Polygon(box) for box, conf in relevant if Polygon(box).is_valid]

                tree = STRtree(polygons)
                merged_polygons = []
                visited = set()

                for i, poly in enumerate(polygons):
                    if i in visited:
                        continue

                    indices = tree.query(poly)
                    cluster = [polygons[idx] for idx in indices if idx not in visited]

                    if cluster:
                        merged_cluster = unary_union(cluster)

                        if merged_cluster.geom_type == 'Polygon':
                            merged_polygons.append(merged_cluster)
                        else:
                            merged_polygons.extend(list(merged_cluster.geoms))

                        for idx in indices:
                            visited.add(idx)

                for symbol_count, final_poly in enumerate(merged_polygons, start=1):
                    coords = np.array(final_poly.exterior.coords).astype(np.int32)
                    grid_pos = self.__get_grid_position(coords, file_to_predict.shape[0], file_to_predict.shape[1])
                    merged_results.append(SymbolDetectionBox((coords, 0.80), f"{count}-{symbol_count}"))

                print(f"Symbols detected: {len(merged_results)}")

            print("Predicting done! Adding to list of coördinates.")

            if context.progress_callback:
                percentage = int((count / amount_of_files) * 100)
                context.progress_callback(percentage)
            
            context.yolo_data.append(merged_results)

    
    def __get_grid_position(self, coords, height, width):
        """
        determines the position of the symbol coordinates through a grid structure of 3x3

        Args:
            coords (numpy array): the coordinates of the symbols in polygon format  
            height (int): the pixel height of the converted file
            width (int): the pixel width of the converted file

        Yields:
            str: yields a string with the position in a basic format 'links-boven', 'midden', 'rechts-onder', etc.
        """
        positions = [["links-boven", "midden-boven", "rechts-boven"],
                     ["links-midden", "midden", "rechts-midden"],
                     ["links-onder", "midden-onder", "rechts-onder"]]
        
        center_x = np.mean(coords[:, 0])
        center_y = np.mean(coords[:, 1])

        col_idx = min(int(center_x / (width / 3)), 2)
        row_idx = min(int(center_y / (height / 3)), 2)

        yield positions[row_idx][col_idx]
                