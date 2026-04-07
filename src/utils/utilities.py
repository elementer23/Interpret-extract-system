import re
import zipfile
import warnings

class BasicUtils(object):

    @staticmethod
    def is_class_present(t: tuple, class_to_check: type) -> bool:
        x = any(isinstance(v, class_to_check) for v in t)
        return x

    @staticmethod
    def is_number_int_float(num) -> bool:
        if isinstance(num, int):
            return True
        elif isinstance(num, float):
            return True
        elif num.isdigit():
            return True
        else:
            return False
        
    @staticmethod
    def is_symbol(sym: str) -> bool:
        return re.fullmatch(r"^\W+$", str(sym))
    
    @staticmethod
    def categorize(val) -> str:
        if BasicUtils.is_number_int_float(val):
            return "nummer"
        elif BasicUtils.is_symbol(val):
            return "symbool"
        else:
            return "tekst"
        
    @staticmethod
    def is_zip_present(val: list) -> bool:
        if not val:
            return None
        
        for zip in val:
            if zipfile.is_zipfile(zip):
                return True