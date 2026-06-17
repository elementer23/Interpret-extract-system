import json
from utils.utilities import BasicUtils
from enumeration.package_type import PackageType
import re
from typing import Any
import os
import pathlib

local_appdata = os.environ.get('LOCALAPPDATA')
base_folder = pathlib.Path(f"{local_appdata}/interpret_extract_system")

class Settings(object):
    """Settings class.
    
    Inherits the 'object' type. Used as a 'static' class and
    implements static functions that apply to the Settings.
    (Settings that the user can change).
    Any new functions added should relate to settings that the user can change.
    """
    
    @staticmethod
    def read_settings() -> None:
        """This function simply prints the settings to the terminal."""
        try:
            app_folder = os.path.join(local_appdata, "interpret_extract_system")
            with open(f'{app_folder}\\settings.json', 'r') as file:
                data = json.load(file)
            
        except json.JSONDecodeError:
            print("Error: Failed to decode JSON from the file.")

        else:
            for n in data["settings"]:
                print(n)


    @staticmethod
    def retrieve_settings(name: str | None = None) -> Any:
        """This function retrieves the settings, from the file.
        Retrieves a specific setting once the correct name is given.
        Will return all the settings if the name is left blank.
        Will create an entirely new settings file, at the location the user has given,
        once the file no longer exists. Requiring the application to be restarted after creation.

        :type name: string | None = None
        :param name: the name of the setting to retrieve.
        
        :return Any: will return the value of the given setting or all settings, if intentionally left blank.
        """
        try:
            app_folder = os.path.join(local_appdata, "interpret_extract_system")
            with open(f'{app_folder}\\settings.json', 'r') as file:
                data = json.load(file)
                
        except (json.JSONDecodeError, FileNotFoundError):
            print("Error: Failed to decode JSON from the file.")
            if FileNotFoundError:
                Settings.create_settings_if_not_exist()

        else:
            for n in data["settings"]:
                return n[name] if name is not None else n
    
    @staticmethod
    def change_chosen_export(chosen_export: str) -> None:
        """Change the chosen export setting in the file."""
        Settings.write_to_settings(chosen_export, "chosen_export")

    @staticmethod
    def change_custom_file_selection(val: str) -> None:
        """Change the custom file selection setting, if the standard file selection isn't needed.
        Will deny file extensions that aren't supported.
        """
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
        """Change the name of the file selection (extra functionality)"""
        if not chosen_name:
            Settings.write_to_settings("", "custom_file_selection_name")

            return
        
        s = BasicUtils.first_upper_case(chosen_name)

        if not s:
            return
        
        Settings.write_to_settings(s, "custom_file_selection_name")

    @staticmethod
    def change_export_options_order(chosen_export: str) -> None:
        """This function changes the export order, in the dropdown.
        Mainly due to the current code structure.
        """
        try:
            app_folder = os.path.join(local_appdata, "interpret_extract_system")
            with open(f'{app_folder}\\settings.json', 'r') as file:
                data = json.load(file)

        except json.JSONDecodeError:
            print("Error: Failed to decode JSON from the file.")

        else:
            if 'export_options' in data['settings'][0]:
                l = data['settings'][0]['export_options']
                arr = []
                for i in range(len(l)):
                    arr.append(l[i])
                    
                temp = arr[0]
                arr[arr.index(chosen_export)] = temp
                arr[0] = chosen_export
                data['settings'][0]['export_options'] = arr

            try:
                with open(f'{app_folder}\\settings.json', 'w') as file:
                    json.dump(data, file, indent=4)
            
            except json.JSONDecodeError:
                print("Error: Failed to encode JSON to the file.")

    @staticmethod
    def change_directory_path(chosen_path: str) -> None:
        """Changes the base path where the files will be exported to."""
        Settings.write_to_settings(chosen_path, "directory_path")

    @staticmethod
    def change_temp_dir_name(chosen_name: str) -> None:
        """Changes the base name of the folder where the exported files will reside."""
        if not chosen_name:
            return
        
        Settings.write_to_settings(chosen_name, "temp_dir_name")

    @staticmethod
    def change_chosen_package(chosen_package: str) -> None:
        """Changes the packaging type setting. Default as base, but can be zip, 7zip, tar, multisheet etc."""
        Settings.write_to_settings(chosen_package, "chosen_package")

    @staticmethod
    def change_package_type_s(chosen_package: str) -> None:
        """Changes the order of the dropdown of the package settings.
        Mainly due to the current structure of the code.
        """
        try:
            app_folder = os.path.join(local_appdata, "interpret_extract_system")
            with open(f'{app_folder}\\settings.json', 'r') as file:
                data = json.load(file)

        except json.JSONDecodeError:
            print("Error: Failed to decode JSON from the file.")
        
        else:
            if 'package_type_s' in data['settings'][0]:
                l = data['settings'][0]['package_type_s']
                arr = []
                for i in range(len(l)):
                    arr.append(l[i])
                    
                temp = arr[0]
                arr[arr.index(chosen_package)] = temp
                arr[0] = chosen_package
                data['settings'][0]['package_type_s'] = arr

            try:
                with open(f'{app_folder}\\settings.json', 'w') as file:
                    json.dump(data, file, indent=4)

            except json.JSONDecodeError:
                print("Error: Failed to encode JSON to the file.")
    
    @staticmethod
    def change_temp_files_path(chosen_files_path: str) -> None:
        """Change the path, where the main file container will be created."""
        Settings.write_to_settings(chosen_files_path, "temp_files_path")

    @staticmethod
    def change_temp_files_name(chosen_files_name: str) -> None:
        """Change the name of the main file container.
        Do keep in mind that this can be used differently as well.
        Lets say, that you got hundreds of folders in a certain path.
        And you have to switch between these folders, to see their content 
        inside of the application. Then you could simply change the name, to the 
        required folder in the settings. And it should load in, all the files inside of that directory.
        Do keep in mind, that folders inside of another folder will be ignored, along with the files in there.
        """
        if not chosen_files_name:
            return
        
        Settings.write_to_settings(chosen_files_name, "temp_files_name")

    @staticmethod
    def is_applicable_file_type(file_type_s: str | list) -> bool:
        """Checks whether the chosen file extensions are supported (see change_custom_file_selection).
        returns True or False whether all chosen extensions are applicable. 
        Will return False, if one extension isn't suppported.

        :type file_type_s: string | list
        :param file_type_s: a single file extension or a list of file extensions to check.

        :return bool: True or False depending on the outcome.
        """
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
        """This function acts a main hub, to change the values of the settings.
        It checks whether the setting exists and change the value of the setting.

        :type val: string
        :param val: the value that will be used to change the setting.
        :type setting_name: string
        :param setting_name: the name of the setting to change the value of.
        """
        try:
            app_folder = os.path.join(local_appdata, "interpret_extract_system")
            with open(f'{app_folder}\\settings.json', 'r') as file:
                data = json.load(file)

        except json.JSONDecodeError:
            print("Error: Failed to decode JSON from the file.")
        
        else:
            if setting_name in data['settings'][0]:
                data['settings'][0][setting_name] = val

            try:
                with open(f'{app_folder}\\settings.json', 'w') as file:
                    json.dump(data, file, indent=4)

            except json.JSONDecodeError:
                print("Error: Failed to encode JSON to the file.")


    @staticmethod
    def save_changes(changes: dict) -> str:
        """A function to save the changes that were made in the settings.
        If a new setting is added, that can be changed by the user. 
        Then it should be added here as well.

        :type changes: dict
        :param changes: a dictionary full of changes {setting name: value}
        """

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
        """Sets the settings back to the default.
        If any settings are added, that the user can change.
        Then the default value of that setting, should be added here as well.
        """

        Settings.write_to_settings(["excel", "json", "csv"], "export_options")
        Settings.write_to_settings("", "chosen_export")
        Settings.write_to_settings("", "custom_file_selection")
        Settings.write_to_settings("", "custom_file_selection_name")
        Settings.write_to_settings(f"{base_folder}", "directory_path")
        Settings.write_to_settings("export_container", "temp_dir_name")
        Settings.write_to_settings(["default", "zip", "7zip", "tar"], "package_type_s")
        Settings.write_to_settings("default", "chosen_package")
        Settings.write_to_settings(f"{base_folder}", "temp_files_path")
        Settings.write_to_settings("file_container", "temp_files_name")

        return "default applied"
    
    @staticmethod
    def create_settings_if_not_exist() -> str:
        """Create the settings file if it no longer exists.
        Will require a restart from the application, if used.
        """
        try:
            app_folder = os.path.join(local_appdata, "interpret_extract_system")
            with open(f"{app_folder}\\settings.json", "w+") as new_file:
                json.dump(Settings.__JSON, new_file, indent=4)

        except json.JSONDecodeError:
            print("Error: Failed to encode JSON to the file.")


    __JSON = { "settings": [{
            "default_export": "excel",
            "export_options": [
                "excel",
                "json",
                "csv"
            ],
            "chosen_export": "",
            "file_selection_options": [
                "(*.png)",
                "(*.jpg)",
                "(*.jpeg)",
                "(*.webp)",
                "(*.pdf)",
                "(*.dwg)",
                "(*.zip)",
                "(*.tar)",
                "(*.7z)"
            ],
            "default_file_selection": "(*.png *.jpg *.jpeg *.webp *.pdf *.dwg *.zip *.tar *.7z)",
            "custom_file_selection": "",
            "file_selection_name": "Default",
            "custom_file_selection_name": "",
            "directory_path": f"{base_folder}",
            "temp_dir_name": "export_container",
            "package_type_s": [
                "default",
                "zip",
                "7zip",
                "tar"
            ],
            "chosen_package": "default",
            "temp_files_path": f"{base_folder}",
            "temp_files_name": "file_container"
        }]}

        
class PackageSettings(object):
    """PackageSettings class.
    
    Inherits from the object type. Used as a 'static' class,
    in regards to Package Settings.
    """

    @staticmethod
    def manage_package(packaging: str = None) -> PackageType:
        """This function manages the packaging options and returns them.
        Returning a certain PackageType, depending on the chosen setting.
        Can also be used seperately, for other uses if necessary.
        Will grab the chosen package setting by default, if empty.
        Or will return the package type, depending on the given packaging request.
        Will return the corresponding package type.
        Will return Default if the chosen packaging option does not exist.

        :type packaging: string = None
        :param packaging: the requested packaging option, can be left empty and will return the PackageType from the settings as base.

        :return PackageType: will return a corresponding PackageType enum constant.
        """
        try:
            if packaging is None:
                packaging = Settings.retrieve_settings('chosen_package')

        except ValueError: 
            print("The given value does not exist as a packaging type.")
            return PackageType.DEFAULT

        else:
            match packaging:
                case "default":
                    return PackageType.DEFAULT
                case "zip":
                    return PackageType.ZIP
                case "tar":
                    return PackageType.TAR
                case "7zip":
                    return PackageType.SEVENZ