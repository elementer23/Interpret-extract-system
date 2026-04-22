import re
import py7zr
import zipfile
import tarfile
from enumeration.file_type import FileType
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
    
    @staticmethod
    def categorize_file_type(file_data: list | str) -> FileType | list[FileType]:
        if not file_data:
            return FileType.UNKNOWN
        
        file_arr = []
        image_arr = [".png", ".webp", ".jpg", ".jpeg"]
        template_arr = [".json", ".csv", ".xlsx", ".xls"]
        txt_arr = [".docx", ".txt"]
        pdf = ".pdf"

        if isinstance(file_data, str):
            file_path = Path(file_data)
            extension = file_path.suffix

            if extension in image_arr:
                return FileType.IMAGE
            elif extension in template_arr:
                return FileType.TEMPLATE_EXTENSION
            elif extension in txt_arr:
                return FileType.TEXT_EXTENSION
            elif extension == pdf:
                return FileType.PDF
            else:
                return FileType.UNKNOWN

        if isinstance(file_data, list):
            for file in file_data:
                file_path = Path(file)
                extension = file_path.suffix

                if extension in image_arr:
                    file_arr.append(FileType.IMAGE)
                elif extension in template_arr:
                    file_arr.append(FileType.TEMPLATE_EXTENSION)
                elif extension in txt_arr:
                    file_arr.append(FileType.TEXT_EXTENSION)
                elif extension == pdf:
                    file_arr.append(FileType.PDF)
                else:
                    file_arr.append(FileType.UNKNOWN)
            
        return file_arr
    
    @staticmethod
    def maintain_compatible_extensions(file_data: list, *args) -> list[str] | None:
        if not file_data or not args:
            return None

        file_types = BasicUtils.categorize_file_type(file_data)
        extensions = [val for val in args]
        compatible_extensions = []

        for i in range(len(file_types)):
            if file_types[i] not in extensions:
                continue

            compatible_extensions.append(file_data[i])

        if not compatible_extensions:
            return None
        
        return compatible_extensions
