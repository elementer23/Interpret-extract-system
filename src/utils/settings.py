import json
import os
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
    def retrieve_settings() -> Any:
        try:
            with open('../src/utils/settings.json', 'r') as file:
                data = json.load(file)
                for n in data["settings"]:
                    return n

        except json.JSONDecodeError:
            print("Error: Failed to decode JSON from the file.")

    
    @staticmethod
    def change_chosen_export(chosen_export: str) -> None:
        try:
            with open('../src/utils/settings.json', 'r') as file:
                data = json.load(file)
            if 'chosen_export' in data['settings'][0]:
                data['settings'][0]['chosen_export'] = chosen_export
            with open('../src/utils/settings.json', 'w') as file:
                json.dump(data, file, indent=4)

        except json.JSONDecodeError:
            print("Error: Failed to encode JSON to the file.")


    @staticmethod
    def save_changes() -> str:
        return "changes have been made."