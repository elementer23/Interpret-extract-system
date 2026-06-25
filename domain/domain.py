from abc import ABC, abstractmethod

class Domain(ABC):
    __slots__ = ()
    @abstractmethod
    def area_domain(self) -> dict:
        pass

class TextDetectionBox(Domain):
    """
    A class to store the data from tesseract
    """
    __slots__=('type', 'text', 'x', 'y', 'w', 'h')

    def __init__(self, type: str, text: str, x: int, y: int, w: int, h: int):
        self.type = type
        self.text = text
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def area_domain(self) -> dict:
        return {"type": self.type, "text": self.text, "left": self.x, "top": self.y, "width": self.w, "height": self.h}
    

class SymbolDetectionBox(Domain):
    """
    A class to store the data that YOLO has found
    """
    __slots__=('offset_box', 'symbol_id')

    def __init__(self, offset_box, symbol_id):
        self.offset_box = offset_box
        self.symbol_id = symbol_id

    def area_domain(self) -> dict:
        return {"offset": self.offset_box, "symbol_id": self.symbol_id}
       

class RawData(Domain):
    """
    A class to store the raw data from symbols and easyOCR data
    """
    __slots__ = ('text', 'conf', 'symbol_id', 'offset', 'symbol_offset', 'grid_position')

    def __init__(self, text, conf, symbol_id, offset, symbol_offset, grid_position):
        self.text = text
        self.conf = conf
        self.symbol_id = symbol_id
        self.offset = offset
        self.symbol_offset = symbol_offset
        self.grid_position = grid_position

    def area_domain(self) -> dict:
        return {"text": self.text, "conf": self.conf, "symbol": self.symbol_id, "offset": self.offset, "symbol_offset": self.symbol_offset, "grid_position": self.grid_position}        

class InterpretedDetection(Domain):
    """
    A class to store the interpreted data from YOLO and EasyOCR
    """
    __slots__ = ('symbol_id', 'text', 'tagnumber', 'x', 'y', 'w', 'h')

    def __init__(self, symbol_id: str | int, text: str, tagnumber: str, x: int, y: int, w: int, h: int):
        self.symbol_id = symbol_id
        self.text = text
        self.tagnumber = tagnumber
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def area_domain(self) -> dict:
        return {"symbol": self.symbol_id, "text": self.text, "tagnumber": self.tagnumber, "left": self.x, "top": self.y, "width": self.w, "height": self.h}