from openpyxl import Workbook
import csv
import json
import shutil
from py7zr import pack_7zarchive, unpack_7zarchive
from utils.settings import Settings
from enumeration.package_type import PackageType
from handler.file_handler import FileOsHandler
import cv2 as cv

#Register the package to prevent register and threading problems for later on.
try:
    shutil.register_archive_format('7zip', pack_7zarchive, description='7zip archive')
    shutil.register_unpack_format('7zip', ['.7z'], unpack_7zarchive)
except Exception as e:
    pass

class Exporter():
    """Export class.
    Exports the accumulated data from the text handler and detection handler.
    Exports the data depending on the given preferences in the settings. (Excel etc. and compressed or not.)
    """
    def __init__(self):
        pass

        self.dir_path = Settings.retrieve_settings('directory_path')
        self.dir_name = Settings.retrieve_settings('temp_dir_name')

    def export_to_excel(self, data_to_enter: list, origin_file_s: list, package_type: PackageType = PackageType.DEFAULT) -> None:
        """Exports the given data into an excel file, placing it in seperate files or seperate sheets in the same file.
        Depending on the given settings.

        :type data_to_enter: list
        :param data_to_enter: a list containing several list instances of TextDetectionBox class.
        :type origin_file_s: list
        :param origin_file_s: the list of file names, where the information originates from.
        :type package_type: PackageType class
        :param package_type: type of packing the file(s) should be exported in depending on the settings. (Default is seperate files in a folder.)
        """
        wb = Workbook()

        package_type = package_type.value

        if package_type == 4:
            try:
                for i, entry in enumerate(data_to_enter):
                    if i == 0:
                        ws = wb.active
                        ws.title = f"{origin_file_s[i]}"
                    else:
                        ws = wb.create_sheet(f"{origin_file_s[i]}")

                    headers = ["Type", "Text", "Left", "Top", "Width", "Height"]
                    ws.append(headers)

                    for bbx in entry:
                        dt = bbx.area_domain()

                        row = [dt['type'], dt['text'], dt['left'], dt['top'], dt['width'], dt['height']]

                        ws.append(row)
            except TypeError as tp:
                print(tp)
            else:
                wb.save(f"{self.dir_path}/{self.dir_name}/output.xlsx")

        else:
            for i, entry in enumerate(data_to_enter):
                wb = Workbook()
                ws = wb.active

                headers = ["Type", "Text", "Left", "Top", "Width", "Height"]
                ws.append(headers)

                try:
                    for bbx in entry:
                        dt = bbx.area_domain()

                        row = [dt['type'], dt['text'], dt['left'], dt['top'], dt['width'], dt['height']]

                        ws.append(row)
                except TypeError as tp:
                    print(tp)
                else:
                    wb.save(f"{self.dir_path}/{self.dir_name}/output{i}-{origin_file_s[i]}.xlsx")

    def safe_val(self, val):
        if isinstance(val, str) and val.startswith(('=', '+', '-', '@')):
            return f"'{val}"
        return val

    def adjusted_export_to_excel(self, data_to_enter: list, origin_file_s: list, package_type: PackageType = PackageType.DEFAULT) -> None:
        wb = Workbook()
        sheet1 = wb.active
        sheet1.title = "Tesseract"
        sheet2 = wb.create_sheet("Raw data")
        sheet3 = wb.create_sheet("Interpreted")

        for data in data_to_enter:
            tesseract = data['tesseract']
            raw_data = data['raw_data']
            interpreted = data['interpreted']

            for i, file_name in enumerate(origin_file_s):

                file_header = [f"{self.safe_val(file_name)}"]
                sheet1.append(file_header)
                sheet1.append(["Type", "Text", "Left", "Top", "Width", "Height"])
                for entry in tesseract[i]:
                    dt = entry.area_domain()
                    row = [dt['type'], self.safe_val(dt['text']), dt['left'], dt['top'], dt['width'], dt['height']]
                    sheet1.append(row)

                sheet2.append(file_header)
                sheet2.append(["Text", "Confidence", "Symbol id", "Text offset Left", "Text offset Top", "Text offset Width", "Text offset Height",
                                    "Symbol offset Left", "Symbol offset Top", "Symbol offset Width", "Symbol offset Height"])
                for entry in raw_data[i]:
                    dt = entry.area_domain()
                    x, y, w, h = cv.boundingRect(dt['offset'])
                    x2, y2, w2, h2 = dt['symbol_offset']
                    row = [self.safe_val(dt['text']), dt['conf'], self.safe_val(dt['symbol']), x, y, w, h, x2, y2, w2, h2]
                    sheet2.append(row)

                sheet3.append(file_header)
                sheet3.append(["Symbol id", "Letter code", "Tag number", "Left", "Top", "Width", "Height"])
                for entry in interpreted[i]:
                    dt = entry.area_domain()
                    row = [self.safe_val(dt['symbol']), self.safe_val(dt['text']), self.safe_val(dt['tagnumber']), dt['left'], dt['top'], dt['width'], dt['height']]
                    sheet3.append(row)

        wb.save(f"{self.dir_path}/{self.dir_name}/output.xlsx")

    def export_to_json(self, data_to_enter: list, origin_file_s: list) -> None:
        """Function to export text handler and detection handler data to json files.
        
        :type data_to_enter: list
        :param data_to_enter: the data to enter into the json file(s) (amount depends on how many files are extracted).
        :type origin_file_s: list
        :param origin_file_s: list with the original file names that were used for extraction.
        """
        for i, entry in enumerate(data_to_enter):

            boundaries = []

            for n in entry:
                dt = n.area_domain()
                boundaries.append({"type": dt['type'], "text": dt['text'], "left": dt['left'], "top": dt['top'], "width": dt['width'], "height": dt['height']})

            _json = {"export": [{
                "boundaries": boundaries
            }]}

            file_path = f"{self.dir_path}/{self.dir_name}/output{i}-{origin_file_s[i]}.json"

            try:
                with open(file_path, "w", encoding='utf-8') as file:
                    json.dump(_json, file, ensure_ascii=False, indent=4)
            except FileNotFoundError:
                print("The directory to export too, does not exist. reverting to default, attempting once more.")
                FileOsHandler().create_dir(dir_path=self.dir_path, dir_name=self.dir_name)
                try:
                    with open(file_path, "w", encoding='utf-8') as file:
                        json.dump(_json, file, ensure_ascii=False, indent=4)
                except json.JSONDecodeError as ex:
                    print(ex)


    def export_to_csv(self, data_to_enter: list, origin_file_s: list) -> None:
        """Function to export text handler and detection handler data to csv files.
        
        :type data_to_enter: list
        :param data_to_enter: the data to enter into the csv file(s) (amount depends on how many files are extracted).
        :type origin_file_s: list
        :param origin_file_s: list with the original file names that were used for extraction.
        """
        for i, entry in enumerate(data_to_enter):

            boundaries = []

            for n in entry:
                dt = n.area_domain()
                boundaries.append({"type": dt['type'], "text": dt['text'], "left": dt['left'], "top": dt['top'], "width": dt['width'], "height": dt['height']})
                
            try:
                with open(f"{self.dir_path}/{self.dir_name}/output{i}-{origin_file_s[i]}.csv", "w", newline='') as file:
                    fieldnames = ['type', 'text', 'left', 'top', 'width', 'height']
                    writer = csv.DictWriter(file, fieldnames=fieldnames)
                    writer.writerows(boundaries)
            except FileNotFoundError:
                print("The directory to export too, does not exist. reverting to default, attempting once more.")
                FileOsHandler().create_dir(dir_path=self.dir_path, dir_name=self.dir_name)

                try:
                    with open(f"{self.dir_path}/{self.dir_name}/output{i}-{origin_file_s[i]}.csv", "w", newline='') as file:
                        fieldnames = ['type', 'text', 'left', 'top', 'width', 'height']
                        writer = csv.DictWriter(file, fieldnames=fieldnames)
                        writer.writerows(boundaries)
                except OSError as ex:
                    print(ex)
                

    
    def execute_export(self, data_to_enter: list, origin_file_s: list, package_type: PackageType = PackageType.DEFAULT) -> None:
        """This function is like a main hub for the export options (referring to csv, json and excel).
        If new type is added, it should be added here as well.
        Switches between types depending on the settings of the user.

        :type data_to_enter: list
        :param data_to_enter: the list of data that should be entered inside of the exported files
        :type origin_file_s: list
        :param origin_file_s: the list of original file names, where the data originates from.
        :type package_type: PackageType
        :param package_type: The PackageType referring to the export options from the user settings (is set to DEFAULT when empty)
        """
        FileOsHandler().create_dir(dir_path=self.dir_path, dir_name=self.dir_name)

        self.adjusted_export_to_excel(data_to_enter=data_to_enter, origin_file_s=origin_file_s, package_type=package_type)

        # if len(Settings.retrieve_settings("chosen_export")) == 0:
        #     self.export_to_excel(data_to_enter=data_to_enter, origin_file_s=origin_file_s, package_type=package_type)
        
        # match Settings.retrieve_settings("chosen_export"):
        #     case "excel":
        #         self.export_to_excel(data_to_enter=data_to_enter, origin_file_s=origin_file_s, package_type=package_type)
        #     case "json":
        #         self.export_to_json(data_to_enter=data_to_enter, origin_file_s=origin_file_s)
        #     case "csv":
        #         self.export_to_csv(data_to_enter=data_to_enter, origin_file_s=origin_file_s)

        self.execute_package_export(dir_path=self.dir_path, dir_name=self.dir_name, package_type=package_type)


    def execute_package_export(self, dir_path: str, dir_name: str, package_type: PackageType = PackageType.DEFAULT) -> None:
        """This function is the main hub for compressed export options, placing the exported files into the archives that are created here.
        It currently exports into 'zip', '7zip' and 'tar' but if other options are added, it should be added here as well.
        It creates an archive through the 'shutil' module, do keep in mind that the archive is flat. 
        (Meaning that there is no folder structure, just purely files.)

        dir_path and dir_name differentiate from another, the dir path is the full directory path where you want to export the compressed folder to.
        dir_name is the name of the eventual folder you will be archiving (exporting). So if dir_path is the path to Documents and dir_name 
        is for example called export_container (depending on user settings.). The files inside of the dir_name, will be archived inside of this folder.
        Documents/export_container -> Documents/(archived)export_container.

        Documents/ --(now archived)export_container/ --(flat, no folder structure inside the archive)files

        :type dir_path: string
        :param dir_path: the direct path to where the folder should be packaged.
        :type dir_name: string
        :param dir_name: the name of the folder that will be archived.
        :type package_type: PackageType
        :param package_type: the PackageType or the way of compression (DEFAULT if empty) (0 | ZIP, 1 | SEVENZ, 2 | TAR)
        """
        if isinstance(package_type, PackageType):
            package_type = package_type.value

        directory = f"{dir_path}/{dir_name}"

        match package_type:
            case 0:
                shutil.make_archive(base_name=directory, format="zip", root_dir=directory)
                FileOsHandler().remove_dir(directory)
            case 1:
                shutil.make_archive(base_name=directory, format="7zip", root_dir=directory)
                FileOsHandler().remove_dir(directory)
            case 2: 
                shutil.make_archive(base_name=directory, format="tar", root_dir=directory)
                FileOsHandler().remove_dir(directory)
            case 3:
                pass
            case 4:
                pass