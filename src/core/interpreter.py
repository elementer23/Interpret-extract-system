from domain.domain import InterpretedDetection
import cv2 as cv
from collections import defaultdict
import math

class Interpreter():
    """
    The interpreter class.
    Interpretes the connection between symbol, lettercode and tagnumber.
    Is Rather complex, but also rather basic. It checks which coordinates
    are closest to one another, based from top to bottom.
    This interpreter isn't flawless and could potentially skip connections, once the amount of
    symbols exceeds more than 3, within a quadrant of coordinates. 

    The connections haven't been made within the raw data, but the information is far more reliable.
    It simply connects a symbol id to a text that has been found, within the quadrant of coordinates.
    Allowing a better view of what has been found and where it is.

    This class and it's functions could become far more potent and precise, but this progress is put to a halt.
    Due to the current understanding of coordinates and calculations. (Also due to the lack of time while currently writing this.)

    This Interpreter only works with raw combo data. Which is created when using a full pipeline build. 
    (The raw combo data is the raw data that is being talked about)
    """
    def __init__(self, raw_combo_data: list):
        self.raw_collection = raw_combo_data
        self.collection = []

    def fetch(self) -> list:
        """
        This function fetches the interpreted data
        """
        self.read()
        if self.collection:
            return self.collection

    def read(self) -> bool | None:
        """
        This function reads the raw data and assigns the data into groups
        of symbols and texts. 
        """
        if not self.raw_collection:
            return False
        for raw_page in self.raw_collection:
            symbol_list, ocr_texts = [], []
            for data in raw_page:
                # raw_data = data.area_domain()
                # symbol = data.symbol_id
                # x2, y2, w2, h2 = data.symbol_offset
                symbol_list.append((data.symbol_id, data.symbol_offset))
                x, y, w, h = cv.boundingRect(data.offset)
                ocr_texts.append((data.text, x, y, w, h))
            result = self.__build(symbol_list, ocr_texts)
            self.collection.append(result)

    def __center(self, x, y, w, h):
        """
        This function calculates the center of a bounding box
        """
        return (x + w / 2, y + h / 2)
    
    def __dst(self, p1, p2):
        """
        This function calculates the distance between two points
        """
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
        for s_idx, (symbol_id, symbol_bbox) in enumerate(symbol_list):
            # center the coordinates of the symbols
            symbol_center = self.__center(*symbol_bbox)

            for t_idx, (text, tx, ty, tw, th) in enumerate(text_list):
                # center all the coordinates of the text boxes
                text_center = self.__center(tx, ty, tw, th)

                # calculate the distance between the two coordinates and save all the possible matches
                distance = self.__dst(symbol_center, text_center)
                if distance <= max_dst:
                    all_possible_matches.append((distance, s_idx, t_idx))

        # sort all the possible matches based on the distance
        all_possible_matches.sort()
        symbol_assigned_texts = defaultdict(list)
        used_text_indices = set()

        for distance, s_idx, t_idx in all_possible_matches:
            #skip all the unnecessary copies
            if t_idx in used_text_indices:
                continue
            
            #skip all the combinations that already have a connection
            if len(symbol_assigned_texts[s_idx]) >= 2:
                continue

            symbol_assigned_texts[s_idx].append(text_list[t_idx])
            used_text_indices.add(t_idx)

        results = []
        for s_idx, (symbol_id, symbol_bbox) in enumerate(symbol_list):
            matched_items = symbol_assigned_texts[s_idx]
            matched_items.sort(key=lambda item: item[2])

            if len(matched_items) == 2:
                letter_code = matched_items[0][0]
                tag_number = matched_items[1][0]
            elif len(matched_items) == 1:
                letter_code = matched_items[0][0]
                tag_number = None
            else:
                continue

            if (letter_code and letter_code.isdigit()) or (letter_code is None and isinstance(tag_number, str) and not tag_number.isdigit()):
                letter_code, tag_number = tag_number, letter_code

            print(f"symbol: {symbol_id} | letter_code: {letter_code}, tagnumber: {tag_number} | x: {symbol_bbox[0]}, y: {symbol_bbox[1]}, w: {symbol_bbox[2]}, h: {symbol_bbox[3]}")

            results.append(InterpretedDetection(
                symbol_id=symbol_id,
                text=letter_code if letter_code else "",
                tagnumber=tag_number if tag_number else "",
                x=symbol_bbox[0],
                y=symbol_bbox[1],
                w=symbol_bbox[2],
                h=symbol_bbox[3]
            ))
        
        return results if results else []

    

