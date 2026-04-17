import re
import py7zr
import zipfile
import tarfile
import warnings
from pathlib import Path
import os

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

    @staticmethod
    def compressed_file_present(val: list) -> bool:
        if not val:
            return None
        
        for c in val:
            if zipfile.is_zipfile(c):
                return True
            elif tarfile.is_tarfile(c):
                return True
            elif py7zr.is_7zfile(c):
                return True
            else:
                return False
            
    @staticmethod        
    def does_file_exist(file: str | None, file_list: list | None, file_dir: str) -> bool:
        if file is None and file_list is None and not file_dir:
            return True
        
        if not file_dir:
            return True
        
        if file_list is None or not file_list:
            source_file = Path(file)
            target_dir = Path(file_dir)
            target_file = target_dir / source_file.name
            
            if target_file.exists():
                return True
            else:
                return False

        if file is None or not file:
            for files in file_list:
                source_file = Path(files)
                target_dir = Path(file_dir)
                target_file = target_dir / source_file.name

                if target_file.exists():
                    return True
                else:
                    return False
                
    @staticmethod
    def strip_all_except_letters(val: str | list) -> str | list:
        arr = []
        if not val:
            return ""

        if isinstance(val, str):
            result = re.sub(r'[^A-Za-z]', '', val)
            result = result.lower()

            return result
        elif isinstance(val, list):
            for n in val:
                result = re.sub(r'[^A-Za-z]', '', n)
                result = result.lower()
                arr.append(result)
            
            return arr
        

    @staticmethod
    def strip_special_characters(val: str | list) -> str | list:
        arr = []
        if not val:
            return ""
        
        if isinstance(val, str):
            result = re.sub(r'[^a-zA-Z0-9]', '', val)
            result = result.lower()

            return result
        elif isinstance(val, list):
            for n in val:
                result = re.sub(r'[^a-zA-Z0-9]', '', n)
                result = result.lower()
                arr.append(result)

            return arr
        
    @staticmethod
    def first_upper_case(s: str) -> str:
        s = BasicUtils.strip_all_except_letters(s[:])
        if not s:
            return ""
        
        arr = []
        for c in s:
            arr.append(c)

        arr[0] = arr[0].upper()
        return ''.join(arr)
    

    @staticmethod
    def is_directory_empty(dir_path: str) -> bool:
        empty = True
        for _ in os.scandir(dir_path):
            empty = False
            break

        return True if empty else False