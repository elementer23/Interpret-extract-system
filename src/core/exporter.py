from openpyxl import Workbook
import csv
import json
import shutil
from py7zr import pack_7zarchive, unpack_7zarchive
from utils.settings import Settings
from enumeration.package_type import PackageType
from handler.file_handler import FileHandler


class Exporter():
    def __init__(self):
        pass

        self.dir_path = Settings.retrieve_settings()['directory_path'] 
        self.dir_name = Settings.retrieve_settings()['temp_dir_name']

    def export_to_excel(self, data_to_enter: list, package_type: PackageType = PackageType.DEFAULT) -> None:
        wb = Workbook()

        package_type = package_type.value

        if package_type == 4:
            for i, entry in enumerate(data_to_enter):
                if i == 0:
                    ws = wb.active
                else:
                    ws = wb.create_sheet()

                headers = ["Type", "Text", "Left", "Top", "Width", "Height"]
                ws.append(headers)

                for bbx in entry:
                    dt = bbx.area_domain()

                    row = [dt['type'], dt['text'], dt['left'], dt['top'], dt['width'], dt['height']]

                    ws.append(row)

            wb.save(f"{self.dir_path}/{self.dir_name}/output.xlsx")

        else:

            for i, entry in enumerate(data_to_enter):
                wb = Workbook()
                ws = wb.active

                headers = ["Type", "Text", "Left", "Top", "Width", "Height"]
                ws.append(headers)

                for bbx in entry:
                    dt = bbx.area_domain()

                    row = [dt['type'], dt['text'], dt['left'], dt['top'], dt['width'], dt['height']]

                    ws.append(row)

                wb.save(f"{self.dir_path}/{self.dir_name}/output{i}.xlsx")


    def export_to_json(self, data_to_enter: list) -> None:

        for i, entry in enumerate(data_to_enter):

            boundaries = []

            for n in entry:
                dt = n.area_domain()
                boundaries.append({"type": dt['type'], "text": dt['text'], "left": dt['left'], "top": dt['top'], "width": dt['width'], "height": dt['height']})

            _json = {"export": [{
                "boundaries": boundaries
            }]}

            file_path = f"{self.dir_path}/{self.dir_name}/output{i}.json"

            with open(file_path, "w", encoding='utf-8') as file:
                json.dump(_json, file, ensure_ascii=False, indent=4)


    def export_to_csv(self, data_to_enter: list) -> None:

        for i, entry in enumerate(data_to_enter):

            boundaries = []

            for n in entry:
                dt = n.area_domain()
                boundaries.append({"type": dt['type'], "text": dt['text'], "left": dt['left'], "top": dt['top'], "width": dt['width'], "height": dt['height']})
                
            with open(f"{self.dir_path}/{self.dir_name}/output{i}.csv", "w", newline='') as file:
                fieldnames = ['type', 'text', 'left', 'top', 'width', 'height']
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writerows(boundaries)

    
    def execute_export(self, data_to_enter: list, package_type: PackageType = PackageType.DEFAULT) -> None:
        FileHandler().temp_dir(dir_path=self.dir_path, dir_name=self.dir_name)

        if len(Settings.retrieve_settings()["chosen_export"]) == 0:
            self.export_to_excel(data_to_enter=data_to_enter, package_type=package_type)
        
        match Settings.retrieve_settings()["chosen_export"]:
            case "excel":
                self.export_to_excel(data_to_enter=data_to_enter, package_type=package_type)
            case "json":
                self.export_to_json(data_to_enter=data_to_enter)
            case "csv":
                self.export_to_csv(data_to_enter=data_to_enter)

        self.execute_package_export(package_type=package_type)


    def execute_package_export(self, package_type: PackageType = PackageType.DEFAULT) -> None:
        shutil.register_archive_format('7zip', pack_7zarchive, description='7zip archive')
        shutil.register_unpack_format('7zip', ['.7z'], unpack_7zarchive)

        if isinstance(package_type, PackageType):
            package_type = package_type.value

        match package_type:
            case 0:
                shutil.make_archive(base_name=f"{self.dir_path}/{self.dir_name}", format="zip", root_dir=f"{self.dir_path}/{self.dir_name}")
                FileHandler().remove_dir(f"{self.dir_path}/{self.dir_name}")
            case 1:
                shutil.make_archive(base_name=f"{self.dir_path}/{self.dir_name}", format="7zip", root_dir=f"{self.dir_path}/{self.dir_name}")
                FileHandler().remove_dir(f"{self.dir_path}/{self.dir_name}")
            case 2: 
                shutil.make_archive(base_name=f"{self.dir_path}/{self.dir_name}", format="tar", root_dir=f"{self.dir_path}/{self.dir_name}")
                FileHandler().remove_dir(f"{self.dir_path}/{self.dir_name}")
            case 3:
                pass
            case 4:
                pass