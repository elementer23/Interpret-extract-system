from abc import ABC, abstractmethod

class Domain(ABC):
    @abstractmethod
    def area_domain(self) -> dict:
        pass

class TextDetectionBox(Domain):
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
    def __init__(self, offset_box, confidence, name):
        self.offset_box = offset_box
        self.confidence = confidence
        self.name = name

    def area_domain(self) -> dict:
        return {"offset": self.offset_box, "conf": self.confidence, "name": self.name}
        
    