from enum import Enum

class FileType(Enum):
    """The FileType class, inherits from the Enum module.
    Offers summarized FileTypes to correlate file extensions with.
    If implemented in a function, the correlating integer or FileType CONSTANT can be called.
    It works both ways. Name Value pairs, basically.
    PDF = 0, IMAGE = 1, TEMPLATE_EXTENSION = 2, TEXT_EXTENSION = 3, UNKNOWN = 4 (unsupported in the code basically.)
    """
    PDF = 0
    IMAGE = 1
    TEMPLATE_EXTENSION = 2
    TEXT_EXTENSION = 3
    UNKNOWN = 4
    