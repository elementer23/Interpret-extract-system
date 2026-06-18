import numpy as np
import pymupdf
import os
import shutil
from pathlib import Path
from utils.utilities import BasicUtils, FileType
import pathlib
from utils.settings import Settings
from collections import defaultdict
import re
from error.error_hub import ErrorHub

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
                ErrorHub.error_msg(f"Something went wrong: '{ex}'", "warning")
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
    

    def __generate_detected_connections(self, data):
        """
        Generates a dictionary and lists the texts that belong to a symbol.
        Creating a single batch for a file.
        """
        grouped_batch = defaultdict(list)

        rows = len(data)
        for i in range(rows):
            for box in data[i]:
                bbxad = box.area_domain()
                grouped_batch[bbxad['symbol']].append(bbxad["text"])
        return grouped_batch
    
    def __generate_symbol_indications(self, page, scale_factor, data):
        """
        generates the indications in the form of a rectangle, 
        showing which symbols have been found and are marked.
        """
        rows = len(data)
        for i in range(rows):
            for box in data[i]:
                bbxad = box.area_domain()
                x, y, w, h = bbxad["symbol_offset"]

                pdf_x1 = x * scale_factor
                pdf_y1 = y * scale_factor
                pdf_x2 = (x + w) * scale_factor
                pdf_y2 = (y + h) * scale_factor

                rect = pymupdf.Rect(pdf_x1, pdf_y1, pdf_x2, pdf_y2)
                page.draw_rect(rect, color=(1, 0, 0), width=2)
    
    def draw_contextdata_on_pdf(self, pipeline_context, filepath, name):
        """
        This function draws the data that originates from the pipeline, onto 
        a copy of the given pdf. 
        """
        if BasicUtils.categorize_file_type(filepath) is not FileType.PDF: return None
        pc = pipeline_context
        if not pc: return None
        name = "generated_pdf" if not name else name

        save_location = Path.home() / "Downloads"
        save_as = save_location / name
        save_as = FileOsHandler().get_unique_file(save_as, "pdf")

        doc = pymupdf.open(filepath)
        page = doc[0]

        cv_image_width = pc.image_s[0].shape[1]
        scale_factoring = page.rect.width / cv_image_width

        batch = self.__generate_detected_connections(pc.combo_data)
        batch_found = [(k, v) for k, v in batch.items()]

        self.__generate_symbol_indications(page, scale_factoring, pc.combo_data)

        cols, start_x, start_y, gap_x, gap_y = 4, 40, 60, 200, 20

        total_items = len(batch_found)
        if total_items > 0:
            num_rows = ((total_items - 1) // cols) + 1
            grid_width = cols * gap_x
            grid_height = num_rows * gap_y
            background_rect = pymupdf.Rect(start_x - 10, start_y - 15, start_x + grid_width + 10, start_y + grid_height + 20)
            page.draw_rect(background_rect, color=(0, 0, 0), fill=(1, 1, 1), fill_opacity=0.9, width=1)

            for index, item in enumerate(batch_found):
                symbol_id, text_list = item
                filtered_text = f"{symbol_id}: {', '.join(text_list)}"
                row = index // cols
                col = index % cols
                item_x = start_x + (col * gap_x)
                item_y = start_y + (row * gap_y)

                page.insert_text(pymupdf.Point(item_x, item_y), filtered_text, fontsize=11, color=(1, 0, 0))

        doc.save(save_as, garbage=4, deflate=True)
        doc.close()
    
    def image_to_pdf(self, image, name: str):
        """
        This function simply converts an image to a pdf.
        """
        if BasicUtils.categorize_file_type(image) is not FileType.IMAGE: return None
        re.sub(r'[^\w\-_\. ]', '_', name)
        name = "image_to_pdf" if not name else name
        doc = pymupdf.open(image)
        pdfbytes = doc.convert_to_pdf()
        pdf = pymupdf.open("pdf", pdfbytes)
        save_location = Path.home() / "Downloads"
        save_as = save_location / name
        save_as = FileOsHandler().get_unique_file(save_as, "pdf")
        pdf.save(save_as)
        pdf.close()
        doc.close()

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
            ErrorHub.error_msg(f"Something went wrong, while trying to copy files: '{ex}'", "warning")

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
        
    def get_unique_file(self, filepath: str, extension_type: str = None):
        """
        This function acts like the file_name (1).extension from windows.
        Checking whether a given name is already present within the directory.
        Checks for the same extension, once the 'extension_type' parameter is left empty.
        Will check for a file of the same name and the same extension type, when trying to convert
        from one extension to another.
         
        Will check for a file of the same name and the given 'extension_type' if an extension is given.
        """
        directory, filename = os.path.split(filepath)
        name, original_ext = os.path.splitext(filename)

        if extension_type and not extension_type.startswith('.'):
            extension_type = f".{extension_type}"

        extensions_to_check = {original_ext}
        if extension_type:
            extensions_to_check.add(extension_type)

        if not any(os.path.exists(os.path.join(directory, f"{name}{ext}")) for ext in extensions_to_check):
            final_ext = extension_type if extension_type else original_ext
            return os.path.join(directory, f"{name}{final_ext}")

        counter = 1
        while True:
            new_name_base = f"{name} ({counter})"
            
            conflict = False
            for ext in extensions_to_check:
                check_path = os.path.join(directory, f"{new_name_base}{ext}")
                if os.path.exists(check_path):
                    conflict = True
                    break
            
            if not conflict:
                final_ext = extension_type if extension_type else original_ext
                return os.path.join(directory, f"{new_name_base}{final_ext}")
                
            counter += 1

