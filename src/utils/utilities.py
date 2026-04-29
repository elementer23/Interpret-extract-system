import re
import py7zr
import zipfile
import tarfile
from enumeration.file_type import FileType
from pathlib import Path
import os

class BasicUtils(object):
    """BasicUtils a 'static' class

    Inherits from the object type and has no initializer as base.

    Contains functionalities that can be generally used in several or specific circumstances,
    but don't belong to any specific module or working structure.

    Only add these types of functionalities to this class (general purpose).
    """

    @staticmethod
    def is_class_present(t: tuple, class_to_check: type) -> bool:
        """Checks whether a class is present inside of the given tuple
        
        :param t: the given tuple to check
        :type t: tuple
        :param class_to_check: the class to check the presence of.
        :type class_to_check: type

        :return bool:
        """
        x = any(isinstance(v, class_to_check) for v in t)
        return x

    @staticmethod
    def is_number_int_float(num) -> bool:
        """Checks whether the given value is a number, int or float. Does not specify what type it is, only returns a boolean.
        
        :param num: the parameter that is checked
        :type num: Any

        :return bool:
        """
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
        """Checks whether the given value only consists out of symbols (special characters).
        
        :type sym: string
        :param sym: the parameter to be checked

        :return bool:
        """
        return re.fullmatch(r"^\W+$", str(sym))
    
    @staticmethod
    def categorize(val) -> str:
        """Categorizes the given value as a number, symbol or line of text.
        
        :type val: Any
        :param val: the value to be categorized.
        
        :return str: 'nummer', 'symbool', 'tekst'
        """
        if BasicUtils.is_number_int_float(val):
            return "nummer"
        elif BasicUtils.is_symbol(val):
            return "symbool"
        else:
            return "tekst"
        
    @staticmethod
    def is_zip_present(val: list) -> bool:
        """Checks whether a zip file type is present inside of the given list.
        
        :type val: list
        :param val: the parameter to be checked

        :return bool | None:
        """
        if not val:
            return None
        
        for zip in val:
            if zipfile.is_zipfile(zip):
                return True

    @staticmethod
    def compressed_file_present(val: list) -> bool:
        """Checks whether a compressed file is present inside of the list.
        Currently checks on 'zip', 'tar' and '7zip' files.

        :type val: list
        :param val: the parameter to be checked

        :return bool | None:
        """
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
    def does_file_exist(file_data: str | None, target_directory: str) -> bool | None:
        """Checks whether the file exists in the given target directory.
        
        :type file_data: string | None
        :param file_data: the file that has to be checked (expects full path to supposed file)
        :type target_directory: string
        :param target_directory: the path to the directory where the file should be.

        :return bool | None:
        """
        if not file_data or file_data is None or not target_directory:
            return None
        
        source_file = Path(file_data)
        target_dir = Path(target_directory)
        target_file = target_dir / source_file.name

        return True if target_file.exists() else False
                
    @staticmethod
    def strip_all_except_letters(val: str | list) -> str | list:
        """Strips all the numbers and special characters, from a singular value or all values in a list and returns in lower case.
        Will return an empty list or str, if all given values only consist out of numbers or special characters.

        :type val: string | list
        :param val: the parameter that will be stripped (add it as a copy [:] if necessary).

        :return str | list:
        """
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
        """Strips all the special characters, from a singular value or all values in a list and returns in lower case.
        Will return an empty list or str, if all given values only consist out of special characters.

        :type val: string | list
        :param val: the parameter that will be stripped (add it as a copy [:] if necessary).

        :return str | list:
        """
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
        """Turns the first letter in the given parameter into an uppercase (if the first character is a letter).
        
        :type s: string
        :param s: the parameter to be changed (add as a copy [:] if necessary)

        :return str:
        """
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
        """Checks whether the given directory is empty or not. Has to be full path.
        Will throw an exception and return false, if permission is denied or the directory does not exist.
        
        :type dir_path: string
        :param dir_path: the given directory to be checked.

        :return bool:
        """
        empty = True
        try:
            for _ in os.scandir(dir_path):
                empty = False
                break
        
        except PermissionError:
            print("Permission to scan this directory is denied.")
            return False
        except FileNotFoundError:
            print("The given directory can't be found or does not exist.")
            return False
        else:
            return True if empty else False
    
    @staticmethod
    def categorize_file_type(file_data: list | str) -> FileType | list[FileType]:
        """Caterogizes the file type(s) of the given value(s).
        Will return UNKNOWN by default if the value is empty.
        Checks by default on 'png', 'webp', 'jpg', 'jpeg', 'json', 'csv', 'xlsx', 'xls', 'docx', 'txt' and 'pdf'.
        New one's have to be added manually. Or else they'll be caterogized as UNKNOWN.

        :type file_data: string | list
        :param file_data: the parameter that has to be checked, either a single file or a list of files (file_path(s)).

        :return FileType | list[FileType]:
        """
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
        """Maintains the given files of given FileType categories.
        Returns a list of files that are compatible with the given arguments. Excluding the rest.
        Returns None if the list is empty or if no Arguments are given.

        :type file_data: list
        :param file_data: the list of files that have to be filtered (add as copy [:] if necessary)
        :type args: FileType(s)
        :param args: Arguments of FileType(s) that will be maintained in the list. Excluding all that isn't specified.

        :return list[str] | None: The list of compatible files
        """
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
