from enum import Enum

class PackageType(Enum):
    """The PackageType class, inherits from the Enum module.
    Offers PackageTypes to export with, referring to a type of file export or compressing a folder with files.
    If implemented in a function, the correlating integer or PackageType CONSTANT can be called.
    It works both ways. Name Value pairs, basically.
    ZIP = 0, SEVENZ = 1, TAR = 2, DEFAULT = 3.
    """
    ZIP = 0
    SEVENZ = 1
    TAR = 2
    DEFAULT = 3