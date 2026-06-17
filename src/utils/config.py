import json
from typing import Any
import os
from utils.utilities import BasicUtils

local_appdata = os.environ.get('LOCALAPPDATA')

class Config(object):

    @staticmethod
    def get(name: str | None = None) -> Any:
        """
        Get the config setting that is given.
        Will return a list if no name is given.
        """
        try:
            app_folder = os.path.join(local_appdata, "interpret_extract_system")
            with open(f"{app_folder}\\config.json", 'r') as file:
                data = json.load(file)
                
        except (json.JSONDecodeError, FileNotFoundError):
            print("Error: Failed to decode JSON from the file.")
            if FileNotFoundError:
                Config.create_config()

        else:
            for n in data["config"]:
                return n[name] if name is not None else n


    @staticmethod
    def create_config() -> str:
        """Create the config file if it no longer exists.
        Will require a restart from the application, if used.
        """
        try:
            app_folder = os.path.join(local_appdata, "interpret_extract_system")
            with open(f"{app_folder}\\config.json", "w+") as new_file:
                json.dump(Config.__JSON, new_file, indent=4)

        except json.JSONDecodeError:
            print("Error: Failed to encode JSON to the file.")

    @staticmethod
    def __validate_port(port):
        validated_port = BasicUtils.strip_all_except_numbers(port)
        validated_port = validated_port if validated_port else "8080"
        Config.__write(validated_port, "port")

    @staticmethod
    def __validate_api_key(api_key):
        key = api_key if api_key else "default"
        Config.__write(key, "api_key")

    @staticmethod
    def __validate_cpu_usage(force_cpu):
        cpu = force_cpu if force_cpu else "False"
        Config.__write(cpu, "force_cpu")

    @staticmethod
    def __validate_model(model):
        m = model if model else "default"
        Config.__write(m, "model")

    @staticmethod
    def __write(val: Any, setting_name: str) -> None:
        """This function acts a main hub, to change the values of the config settings.
        It checks whether the setting exists and change the value of the setting.

        :type val: Any
        :param val: the value that will be used to change the setting.
        :type setting_name: string
        :param setting_name: the name of the setting to change the value of.
        """
        try:
            app_folder = os.path.join(local_appdata, "interpret_extract_system")
            with open(f"{app_folder}\\config.json", 'r') as file:
                data = json.load(file)

        except json.JSONDecodeError:
            print("Error: Failed to decode JSON from the file.")
        
        else:
            if setting_name in data['config'][0]:
                data['config'][0][setting_name] = val

            try:
                with open(f"{app_folder}\\config.json", 'w') as file:
                    json.dump(data, file, indent=4)

            except json.JSONDecodeError:
                print("Error: Failed to encode JSON to the file.")

    @staticmethod
    def save(changes: dict):
        """A function to save the changes that were made in the config.
        If a new setting is added, that can be changed by the user. 
        Then it should be added here as well.
        Do keep in mind that if the api-key is changed, that it will be lost.
        So be sure to keep track of a copy somewhere or else a new one has to be requested.

        :type changes: dict
        :param changes: a dictionary full of changes {setting name: value}
        """
        if not changes:
            return "No changes were given."
        
        for k, v in changes.items():
            match k:
                case "port":
                    Config.__validate_port(v)
                case "force_cpu":
                    Config.__validate_cpu_usage(v)
                case "api_key":
                    Config.__validate_api_key(v)
                case "model":
                    Config.__validate_model(v)

    @staticmethod
    def default() -> str:
        """
        Sets the config back to the default.
        If any settings are added, that the user can change.
        Then the default value of that setting, should be added here as well.
        DO keep in mind that the api-key isn't changed back. Will stick to default
        if the api-key hasn't been given before. Else will keep the current api-key.
        """
        Config.__write(7.0, "min_gpu_gb")
        Config.__write("False", "force_cpu")
        Config.__write("8080", "port")
        Config.__write("default", "model")

        return "default applied."

    __JSON = { "config": [{
            "min_gpu_gb": 7.0,
            "force_cpu": "False",
            "port": "8080",
            "api_key": "default",
            "model": "default"
         }]}