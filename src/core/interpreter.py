from domain.domain import TextDetectionBox, SymbolDetectionBox, InterpretedDetection
import cv2 as cv
from collections import defaultdict
import math

class Interpreter():
    def __init__(self, raw_combo_data: list):
        self.raw_collection = raw_combo_data
        self.collection = []

    def fetch(self) -> list:
        self.read()
        if self.collection:
            return self.collection

    def read(self) -> bool | None:
        if not self.raw_collection:
            return False
        for i in range(len(self.raw_collection)):
            grouped_collection = defaultdict(list)
            symbol_list, ocr_texts = [], []
            for data in self.raw_collection[i]:
                raw_data = data.area_domain()
                symbol = raw_data['symbol']
                x2, y2, w2, h2 = raw_data['symbol_offset']
                symbol_list.append({"symbol_id": symbol, "left": x2, "top": y2, "width": w2, "height": h2})
                x, y, w, h = cv.boundingRect(raw_data['offset'])
                ocr_texts.append({"text": raw_data['text'], "left": x, "top": y, "width": w, "height": h})
                grouped_collection[symbol].append({
                    "symbol_id": symbol,
                    "text": raw_data['text'],
                    "confidence": raw_data['conf'],
                    "left": x,
                    "top": y,
                    "width": w,
                    "height": h,
                    "symbol_left": x2,
                    "symbol_top": y2,
                    "symbol_width": w2,
                    "symbol_height": h2
                })
            result = self.__build(symbol_list, ocr_texts)
            self.collection.append(result)

    def __center(self, bbox):
        x, y, w, h = bbox
        return (x + w / 2, y + h / 2)
    
    def __dst(self, p1, p2):
        return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)
    
    def __build(self, symbol_list: list, text_list: list, max_dst: int = 100) -> list:
        """
        This function initially builds a list with interpreted data.
        It only handles data from a fully build pipeline, so that means 
        a file handler, image handler, detection handler and a text handler. 

        It requires a list of symbols and a list of OCR text. It will try to make
        the connection between the two lists bases on center and distance. It will look
        at the center of a text box and a symbol box, before determining the distance between them.
        It will then sort the possible matches based on distance. And will try to
        see which texts belong to each other. It isn't entirely accurate, if multiple symbols
        are captured in a single area of coordinates. So it will sometimes lose data, if connections
        can't be made. Or it will put two tags with each other and two letter codes, instead of a letter code and tag number.
        
        It will return an empty array, if there were no connections to make or if there were no symbols
        or texts inside the given arrays.

        :type symbol_list: list
        :param symbol_list: a list of symbols, retrieved from the read function
        :type text_list: list
        :param text_list: a list of OCR texts, retrieved from the read function
        :param max_dst: the max distance to check between two coordinates, 100 by default

        :return list: a list of interpreted annotations
        """
        all_possible_matches = []
        for s_idx, symbol in enumerate(symbol_list):
            symbol_bbox = (symbol['left'], symbol['top'], symbol['width'], symbol['height'])
            # center the coordinates of the symbols
            symbol_center = self.__center(symbol_bbox)

            for t_idx, text_item in enumerate(text_list):
                text_bbox = (text_item['left'], text_item['top'], text_item['width'], text_item['height'])
                # center all the coordinates of the text boxes
                text_center = self.__center(text_bbox)

                # calculate the distance between the two coordinates and save all the possible matches
                distance = self.__dst(symbol_center, text_center)
                if distance <= max_dst:
                    all_possible_matches.append({
                        'distance': distance,
                        'symbol_idx': s_idx,
                        'text_idx': t_idx
                    })

        # sort all the possible matches based on the distance
        all_possible_matches.sort(key=lambda x: x['distance'])
        symbol_assigned_texts = defaultdict(list)
        used_text_indices = set()

        for match in all_possible_matches:
            s_idx = match['symbol_idx']
            t_idx = match['text_idx']
            #skip all the unnecessary copies
            if t_idx in used_text_indices:
                continue
            
            #skip all the combinations that already have a connection
            if len(symbol_assigned_texts[s_idx]) >= 2:
                continue

            symbol_assigned_texts[s_idx].append(text_list[t_idx])
            used_text_indices.add(t_idx)

        results = []
        for s_idx, symbol in enumerate(symbol_list):
            symbol_id = symbol['symbol_id']
            symbol_bbox = (symbol['left'], symbol['top'], symbol['width'], symbol['height'])
            
            matched_items = symbol_assigned_texts[s_idx]
            matched_items.sort(key=lambda item: item['top'])

            if len(matched_items) == 2:
                letter_code = matched_items[0]['text']
                tag_number = matched_items[1]['text']
            elif len(matched_items) == 1:
                letter_code = matched_items[0]['text']
                tag_number = None
            else:
                letter_code = None
                tag_number = None

            if letter_code is None and tag_number is None:
                continue

            if letter_code.isdigit() or letter_code is None and isinstance(tag_number, str) and not tag_number.isdigit():
                temp = letter_code
                letter_code = tag_number
                tag_number = temp

            print(f"symbol: {symbol_id} | letter_code: {letter_code}, tagnumber: {tag_number} | x: {symbol_bbox[0]}, y: {symbol_bbox[1]}, w: {symbol_bbox[2]}, h: {symbol_bbox[3]}")

            results.append(InterpretedDetection(
                symbol_id=symbol_id,
                text=letter_code,
                tagnumber=tag_number,
                x=symbol_bbox[0],
                y=symbol_bbox[1],
                w=symbol_bbox[2],
                h=symbol_bbox[3]
            ))
        
        return results if results else []

    

