from enum import Enum

class PackageType(Enum):
    ZIP = 0
    SEVENZ = 1
    TAR = 2
    DEFAULT = 3
    MULTI_SINGULAR = 4