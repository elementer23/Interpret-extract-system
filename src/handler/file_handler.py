import numpy as np
import pymupdf
import os
import shutil
from pathlib import Path
from utils.utilities import BasicUtils, FileType
import pathlib
from utils.settings import Settings

class FileHandler():
    """FileHandler class, used for handling the process of pdf to image conversion."""
    def __init__(self):
        super().__init__()

    def process(self, context):
        """The process function. Mainly used in the pipeline to convert pdfs to images,
        using the pymupdf module. (The first step in the usual standard build for the pipeline, but can be used individually.)

        :type context: PipeContext
        :param context: the parameter containing the PipeContext class, consisting out of a list of pdf files.  
        """

        if context.progress_callback:
            context.progress_callback(0)

        amount_of_files = len(context.image_s)

        for i in range(amount_of_files):
            try:
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
                if context.progress_callback:
                    current_file = i + 1
                    percentage = int((current_file / amount_of_files) * 100)
                    context.progress_callback(percentage)
            except Exception as ex:
                print(ex)
                return
            finally:
                doc.close()        

    def conversion(self, file_s: list) -> list:
        """The conversion function, which is essentially the same as the process function in filehandler.
        This one accepts both images and pdfs however, due to having to accept images and pdfs to convert.

        :type file_s: list
        :param file_s: list of files to convert (full paths)

        :return list: a list of converted pdfs and natural images.
        """
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
    """The FileOsHandler class. It's still part of the FileHandler.
    But this class handles Os actions in particular. Such as creating, deleting, scanning, retrieving etc.
    """
    def __init__(self):
        super().__init__()

    def formulate_files_dir(self) -> list:
        """A short function for retrieving the main file container paths, from the settings.
        
        :return list: a list of the path and the name of the folder.
        """
        path = Settings.retrieve_settings('temp_files_path')
        path_name = Settings.retrieve_settings('temp_files_name')

        return [path, path_name]

    def get_temp_files_dir(self):
        """This function retrieves the files, from the main file folder in correlation to the user settings.
        
        :return list | dict: a list made up of dictionaries, containing the original file and the full path towards the file.
        """
        path = self.formulate_files_dir()
        target_path = os.path.join(path[0], path[1])
        self.create_dir(path[0], path[1])

        files = os.listdir(target_path)
        file_context = []

        for file in files:
            full_path = os.path.join(target_path, file)
            if pathlib.Path(full_path).is_dir():
                continue
            
            file_context.append({"file": file, "dir": full_path})

        return file_context
    
    def copy_files(self, file_data: str | list, target_path: str):
        """This function copies the given file(s), to the targeted path. Checking whether they exist or not, before copying them.
        Uses the shutil module.

        :type file_data: string | list
        :param file_data: a string of the file to copy (file path) or a list containing file paths to copy.
        :type target_path: string
        :param target_path: the target path where the files should be copied to.
        """
        if not file_data or not target_path:
            return
        
        try:
            if isinstance(file_data, str):
                if not BasicUtils.does_file_exist(file_data, target_directory=f"{target_path}/"):
                    source_file = Path(file_data)
                    target_dir = Path(f"{target_path}/")

                    shutil.copy2(source_file, target_dir)

            if isinstance(file_data, list):
                for file in file_data:
                    if not BasicUtils.does_file_exist(file, target_directory=f"{target_path}/"):
                        source_file = Path(file)
                        target_dir = Path(f"{target_path}/")

                        shutil.copy2(source_file, target_dir)

        except Exception as ex:
            print("Exception:", ex)

    def delete_file(self, file: str):
        """A function to delete a single file, from the main file container.
        
        :type file: string
        :param file: the file to be deleted (full file path)
        """
        path = self.formulate_files_dir()
        target_path = os.path.join(path[0], path[1])
        if BasicUtils.does_file_exist(file, target_directory=f"{target_path}/"):
            os.remove(file)
        else:
            print("File does not exist")

    def delete_files(self, file_list: list):
        """The exact same function as delete_file, but with one or more file paths in a list.
        
        :type file_list: list
        :param file_list: list of files to be deleted.
        """
        path = self.formulate_files_dir()
        target_path = os.path.join(path[0], path[1])
        for f in file_list:
            if BasicUtils.does_file_exist(f, target_directory=f"{target_path}/"):
                os.remove(f)
        
    def create_dir(self, dir_path: str, dir_name: str) -> None | bool:
        """This functions creater a directory based on the given path (the where) and a name (the folder you want to create.)
        It checks whether the directory already exists or not.
        
        :type dir_path: string
        :param dir_path: the full path where the folder should be created.
        :type dir_name: string
        :param dir_name: the name of the folder you want to create in the directory.
        """
        if not pathlib.Path(f"{dir_path}/{dir_name}").is_dir():
            directory_path = pathlib.Path(f"{dir_path}/{dir_name}")

            try:
                directory_path.mkdir()
                print(f"Directory '{directory_path}' created successfully.")
                return True
            except FileExistsError:
                print(f"Directory '{directory_path}' already exists.")
                return False
            except PermissionError:
                print(f"Permission denied: Unable to create '{directory_path}'.")
                return False
            except Exception as e:
                print(f"An error occurred: {e}")
                return False

    def remove_dir(self, dir_path: str) -> None:
        """This function removes the given directory (full path).
        Do keep in mind that it removes all the files inside of the directory as well.

        (Will halt when the directory does not exist or if the file or directory aren't permitted to be removed.)

        :type dir_path: string
        :param dir_path: the full path to the directory that needs to be removed.
        """
        try:
            for file in os.listdir(dir_path):
                file_path = os.path.join(dir_path, file)

                if os.path.isfile(file_path):
                    try:
                        os.remove(file_path)
                    except PermissionError:
                        print(f"Permission denied: unable to remove {file_path}.")
            
        except FileNotFoundError:
            print(f"Directory {dir_path} does not exist.")
        except PermissionError:
            print(f"Permission denied: Unable to remove {dir_path}.")
        else:
            pathlib.Path(dir_path).rmdir()

    def get_files_from_dir(self, target_path: str) -> list[str] | None:
        """This function retrieves the files from the given path and returns them as a list.
        
        :type target_path: string
        :param target_path: the path toe the directory, to retrieve the files from.

        :return list[str] | None: a list of files or None if there are no files in the list (directory).
        """
        if pathlib.Path(f"{target_path}").is_dir():
            arr = []
            files = os.listdir(target_path)

            for file in files:
                file_path = os.path.join(target_path, file)
                arr.append(file_path)

            return None if not arr else arr
    
    @DeprecationWarning
    def __renew_copies_in_dir(self, target_path: str, files_to_check: list):
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

