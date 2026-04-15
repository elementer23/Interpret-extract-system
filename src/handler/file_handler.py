import numpy as np
import pymupdf
import os
import shutil
from pathlib import Path
from utils.utilities import BasicUtils
import pathlib

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

    def get_temp_files_dir(self):
        path = "C:/Users/697/Documents/temp_files"
        files = os.listdir(path)
        file_context = []

        for file in files:
            full_path = f"C:/Users/697/Documents/temp_files/{file}"
            file_context.append({"file": file, "dir": full_path})

        return file_context
    
    def copy_files(self, file_list: list):
        if not BasicUtils.does_file_exist(file=None, file_list=file_list, file_dir="C:/Users/697/Documents/temp_files/"):
            for file in file_list:
                source_file = Path(file)
                target_dir = Path("C:/Users/697/Documents/temp_files/")

                shutil.copy2(source_file, target_dir)

    def delete_file(self, file: str):
        if BasicUtils.does_file_exist(file=file, file_list=None, file_dir="C:/Users/697/Documents/temp_files/"):
            os.remove(file)
        else:
            print("Bestand bestaat niet")

    def delete_files(self, file_list: list):
        if BasicUtils.does_file_exist(file=None, file_list=file_list, file_dir="C:/Users/697/Documents/temp_files/"):
            for f in file_list:
                os.remove(f)
        else:
            print("Bestand(en) bestaat niet")

    def temp_dir(self, dir_path: str, dir_name: str) -> None:
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

    def conversion(self, file_s: list) -> list:
        arr = []
        for i in range(len(file_s)):
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