import json
from utils.utilities import BasicUtils
from enumeration.package_type import PackageType
import re
from typing import Any

class Settings(object):
    
    @staticmethod
    def read_settings() -> None:
        try:
            with open('../src/utils/settings.json', 'r') as file:
                data = json.load(file)
                for n in data["settings"]:
                    print(n)
            
        except json.JSONDecodeError:
            print("Error: Failed to decode JSON from the file.")


    @staticmethod
    def retrieve_settings(name: str | None = None) -> Any:
        try:
            with open('../src/utils/settings.json', 'r') as file:
                data = json.load(file)
                for n in data["settings"]:
                    return n[name] if name is not None else n

        except json.JSONDecodeError:
            print("Error: Failed to decode JSON from the file.")

    
    @staticmethod
    def change_chosen_export(chosen_export: str) -> None:
        Settings.write_to_settings(chosen_export, "chosen_export")

    @staticmethod
    def change_custom_file_selection(val: str) -> None:
        if not val:
            Settings.write_to_settings("", "custom_file_selection")

            return
        
        arr = []
        s = val.split()
        s = BasicUtils.strip_special_characters(s)

        if Settings.is_applicable_file_type(s[:]):
            for n in s:
                arr.append(f"*.{n}")

            result = re.sub(r"[\[\]\'\,]", '', str(f"{arr}"))
            Settings.write_to_settings(str(f"({result})"), "custom_file_selection")

    @staticmethod
    def change_custom_file_selection_name(chosen_name: str) -> None:
        if not chosen_name:
            Settings.write_to_settings("", "custom_file_selection_name")

            return
        
        s = BasicUtils.first_upper_case(chosen_name)

        if not s:
            return
        
        Settings.write_to_settings(s, "custom_file_selection_name")

    @staticmethod
    def change_export_options_order(chosen_export: str) -> None:
        try:
            with open('../src/utils/settings.json', 'r') as file:
                data = json.load(file)
            if 'export_options' in data['settings'][0]:
                l = data['settings'][0]['export_options']
                arr = []
                for i in range(len(l)):
                    arr.append(l[i])
                    
                temp = arr[0]
                arr[arr.index(chosen_export)] = temp
                arr[0] = chosen_export
                data['settings'][0]['export_options'] = arr

            with open('../src/utils/settings.json', 'w') as file:
                json.dump(data, file, indent=4)

        except json.JSONDecodeError:
            print("Error: Failed to encode JSON to the file.")

    @staticmethod
    def change_directory_path(chosen_path: str) -> None:
        Settings.write_to_settings(chosen_path, "directory_path")

    @staticmethod
    def change_temp_dir_name(chosen_name: str) -> None:
        if not chosen_name:
            return
        
        Settings.write_to_settings(chosen_name, "temp_dir_name")


    @staticmethod
    def change_chosen_package(chosen_package: str) -> None:
        Settings.write_to_settings(chosen_package, "chosen_package")

    
    @staticmethod
    def change_package_type_s(chosen_package: str) -> None:
        try:
            with open('../src/utils/settings.json', 'r') as file:
                data = json.load(file)
            if 'package_type_s' in data['settings'][0]:
                l = data['settings'][0]['package_type_s']
                arr = []
                for i in range(len(l)):
                    arr.append(l[i])
                    
                temp = arr[0]
                arr[arr.index(chosen_package)] = temp
                arr[0] = chosen_package
                data['settings'][0]['package_type_s'] = arr

            with open('../src/utils/settings.json', 'w') as file:
                json.dump(data, file, indent=4)

        except json.JSONDecodeError:
            print("Error: Failed to encode JSON to the file.")

    
    @staticmethod
    def change_temp_files_path(chosen_files_path: str) -> None:
        Settings.write_to_settings(chosen_files_path, "temp_files_path")

    @staticmethod
    def change_temp_files_name(chosen_files_name: str) -> None:
        if not chosen_files_name:
            return
        
        Settings.write_to_settings(chosen_files_name, "temp_files_name")

    @staticmethod
    def is_applicable_file_type(file_type_s: str | list) -> bool:
        n = file_type_s
        arr = ["png", "jpg", "jpeg", "webp", "pdf", "dwg", "zip", "tar", "7z"]

        if not n:
            return False
        
        if isinstance(n, str):
            s = BasicUtils.strip_special_characters(n[:])
            
            return True if s in arr else False
        
        elif isinstance(n, list):
            l = BasicUtils.strip_special_characters(n[:])
            for f in l:
                if f not in arr:
                    return False
                
        return True

    @staticmethod
    def write_to_settings(val: str, setting_name: str) -> None:
        try:
            with open('../src/utils/settings.json', 'r') as file:
                data = json.load(file)
            if setting_name in data['settings'][0]:
                data['settings'][0][setting_name] = val
            with open('../src/utils/settings.json', 'w') as file:
                json.dump(data, file, indent=4)

        except json.JSONDecodeError:
            print("Error: Failed to encode JSON to the file.")

    @staticmethod
    def save_changes(changes: dict) -> str:

        if not changes:
            return "no changes to make."
        
        for key, value in changes.items():
            match key:
                case "chosen_export":
                    Settings.change_chosen_export(value)
                    Settings.change_export_options_order(value)
                case "custom_file_selection":
                    Settings.change_custom_file_selection(value)
                case "custom_file_selection_name":
                    Settings.change_custom_file_selection_name(value)
                case "directory_path":
                    Settings.change_directory_path(value)   
                case "temp_dir_name":
                    Settings.change_temp_dir_name(value)
                case "chosen_package":
                    Settings.change_chosen_package(value)
                    Settings.change_package_type_s(value)
                case "temp_files_path":
                    Settings.change_temp_files_path(value)
                case "temp_files_name":
                    Settings.change_temp_files_name(value)

        return "changes have been made."
    
    @staticmethod
    def apply_default() -> str:
        Settings.write_to_settings(["excel", "json", "csv"], "export_options")
        Settings.write_to_settings("", "chosen_export")
        Settings.write_to_settings("", "custom_file_selection")
        Settings.write_to_settings("", "custom_file_selection_name")
        Settings.write_to_settings("C:/Users/697/Documents", "directory_path")
        Settings.write_to_settings("temp_dir", "temp_dir_name")
        Settings.write_to_settings(["default", "multi_sheet", "zip", "7zip", "tar"], "package_type_s")
        Settings.write_to_settings("default", "chosen_package")
        Settings.write_to_settings("C:/Users/697/Documents", "temp_files_path")
        Settings.write_to_settings("temp_files", "temp_files_name")

        return "default applied"
    

class PackageSettings(object):

    @staticmethod
    def manage_package(packaging: str = None) -> PackageType:

        if packaging is None:
            packaging = Settings.retrieve_settings('chosen_package')

        match packaging:
            case "default":
                return PackageType.DEFAULT
            case "multi_sheet":
                return PackageType.MULTI_SINGULAR
            case "zip":
                return PackageType.ZIP
            case "tar":
                return PackageType.TAR
            case "7zip":
                return PackageType.SEVENZ