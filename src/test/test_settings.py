import json
import os

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
            "directory_path": "C:/Users/697/Documents",
            "temp_dir_name": "export_container",
            "package_type_s": [
                "default",
                "zip",
                "7zip",
                "tar"
            ],
            "chosen_package": "default",
            "temp_files_path": "C:/Users/697/Documents",
            "temp_files_name": "test_container"
        }]}

path = f"mock_settings.json"

def test_create_settings_if_not_exists():
    try:
        with open(path, "w+") as new_file:
            json.dump(__JSON, new_file, indent=4)

    except json.JSONDecodeError:
        print("Error: Failed to encode JSON to the file.")

    assert True if os.path.isfile(path) else False


def test_read_settings():
    try:
        with open(path, 'r') as file:
            data = json.load(file)
        
    except json.JSONDecodeError:
        print("Error: Failed to decode JSON from the file.")

    else:
        for n in data["settings"]:
            assert n == __JSON['settings'][0]


def mock_retrieve_settings(setting: str):
  
    try:
        with open(path, 'r') as file:
            data = json.load(file)
            
    except (json.JSONDecodeError, FileNotFoundError):
        print("Error: Failed to decode JSON from the file.")

    else:
        for n in data["settings"]:
            return n[setting]

def test_retrieve_settings():

    name = "default_export"

    try:
        with open(path, 'r') as file:
            data = json.load(file)
            
    except (json.JSONDecodeError, FileNotFoundError):
        print("Error: Failed to decode JSON from the file.")

    else:
        for n in data["settings"]:
            assert n[name] == "excel"
