import numpy as np
import pymupdf
import os
import shutil
from pathlib import Path
from utils.utilities import BasicUtils, FileType
import pathlib
from utils.settings import Settings

class FileHandler():
    def __init__(self):
        super().__init__()

    def process(self, context):
        for i in range(len(context.image_s)):
            doc = pymupdf.open(context.image_s[i])
            for page in doc:
                zoom = 300 / 72
                mat = pymupdf.Matrix(zoom, zoom)
                pix = page.get_pixmap(matrix=mat)

                np_buffer = np.frombuffer(pix.samples, dtype=np.uint8)

                if pix.n == 4:
                    np_buffer = np_buffer.reshape(pix.height, pix.width, 4)
                else:
                    np_buffer = np_buffer.reshape(pix.height, pix.width, 3)

                context.image_s[i] = np_buffer
            doc.close()        

    def conversion(self, file_s: list) -> list:
        arr = []
        for i in range(len(file_s)):
            if BasicUtils.categorize_file_type(file_s[i]) is FileType.IMAGE:
                arr.append(file_s[i])
                continue

            doc = pymupdf.open(file_s[i])
            for page in doc:
                zoom = 300 / 72
                mat = pymupdf.Matrix(zoom, zoom)
                pix = page.get_pixmap(matrix=mat)

                np_buffer = np.frombuffer(pix.samples, dtype=np.uint8)

                if pix.n == 4:
                    np_buffer = np_buffer.reshape(pix.height, pix.width, 4)
                else:
                    np_buffer = np_buffer.reshape(pix.height, pix.width, 3)

                arr.append(np_buffer)

            doc.close()

        return arr        
    

class FileOsHandler():
    def __init__(self):
        super().__init__()

    def formulate_files_dir(self) -> list:
        path = Settings.retrieve_settings('temp_files_path')
        path_name = Settings.retrieve_settings('temp_files_name')

        return [path, path_name]

    def get_temp_files_dir(self):

        path = self.formulate_files_dir()
        target_path = os.path.join(path[0], path[1])
        self.create_dir(path[0], path[1])

        files = os.listdir(target_path)
        file_context = []

        for file in files:
            full_path = os.path.join(target_path, file)
            file_context.append({"file": file, "dir": full_path})

        return file_context
    
    def copy_files(self, file_data: str | list):
        if not file_data:
            return
        
        path = self.formulate_files_dir()
        target_path = os.path.join(path[0], path[1])
        try:
            if isinstance(file_data, str):
                if not BasicUtils.does_file_exist(file_data, target_directory=f"{target_path}/"):
                    source_file = Path(file_data)
                    target_dir = Path(f"{path[0]}/{path[1]}/")

                    shutil.copy2(source_file, target_dir)

            if isinstance(file_data, list):
                for file in file_data:
                    if not BasicUtils.does_file_exist(file, target_directory=f"{target_path}/"):
                        source_file = Path(file)
                        target_dir = Path(f"{path[0]}/{path[1]}/")

                        shutil.copy2(source_file, target_dir)

        except Exception as ex:
            print("Exception:", ex)

    def delete_file(self, file: str):
        path = self.formulate_files_dir()
        target_path = os.path.join(path[0], path[1])
        if BasicUtils.does_file_exist(file, target_directory=f"{target_path}/"):
            os.remove(file)
        else:
            print("Bestand bestaat niet")

    def delete_files(self, file_list: list):
        path = self.formulate_files_dir()
        target_path = os.path.join(path[0], path[1])
        for f in file_list:
            if BasicUtils.does_file_exist(f, target_directory=f"{target_path}/"):
                os.remove(f)
        
    def create_dir(self, dir_path: str, dir_name: str) -> None:
        if not pathlib.Path(f"{dir_path}/{dir_name}").is_dir():
            directory_path = pathlib.Path(f"{dir_path}/{dir_name}")

            try:
                directory_path.mkdir()
                print(f"Directory '{directory_path}' created successfully.")
            except FileExistsError:
                print(f"Directory '{directory_path}' already exists.")
            except PermissionError:
                print(f"Permission denied: Unable to create '{directory_path}'.")
            except Exception as e:
                print(f"An error occurred: {e}")

    def remove_dir(self, dir_path: str) -> None:
        for file in os.listdir(dir_path):
            file_path = os.path.join(dir_path, file)

            if os.path.isfile(file_path):
                os.remove(file_path)

        pathlib.Path(dir_path).rmdir()

    def get_files_from_dir(self, target_path: str) -> list[str]:
        if pathlib.Path(f"{target_path}").is_dir():
            arr = []
            files = os.listdir(target_path)

            for file in files:
                file_path = os.path.join(target_path, file)
                arr.append(file_path)

            return None if not arr else arr
        

    def renew_copies_in_dir(self, target_path: str, files_to_check: list):
        try:
            messages = []
            count = 0
            currently_in_dir = self.get_files_from_dir(target_path=target_path)

            if not files_to_check:
                messages.append("There were no files to check.")
                raise Exception

            if currently_in_dir is None:
                self.copy_files(files_to_check)

            file_names_in_dir = [os.path.basename(file) for file in currently_in_dir]
            file_names_in_given_list = [os.path.basename(file) for file in files_to_check]

            print(file_names_in_dir)
            print(file_names_in_given_list)
            for file in file_names_in_given_list:
                if file in file_names_in_dir:
                    count = count + 1

            print(count)

        except Exception:
            print(messages)

