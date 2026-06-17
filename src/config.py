import torch
import warnings
import os
import pathlib
from utils.config import Config
from utils.settings import Settings

warnings.filterwarnings(
    "ignore",
    message=".*'pin_memory' argument is set as true but no accelerator is found, then device pinned memory won't be used."
)

def __check_base(file_name: str) -> bool:
    local_appdata = os.environ.get('LOCALAPPDATA')
    app_folder = pathlib.Path(f"{local_appdata}/interpret_extract_system")
    target_file = app_folder / file_name

    return True if target_file.exists() else False

def base():
    """
    Creates the necessary folder structure and files, 
    before the application starts. It won't create any files or folders,
    that are already there. 
    """
    local_appdata = os.environ.get('LOCALAPPDATA')
    if not pathlib.Path(f"{local_appdata}/interpret_extract_system").is_dir():
        app_folder = pathlib.Path(f"{local_appdata}/interpret_extract_system")
        model_folder = pathlib.Path(f"{app_folder}/models")

        try:
            app_folder.mkdir()
            model_folder.mkdir()
            Config.create_config()
            Settings.create_settings_if_not_exist()
            print(f"Directory '{app_folder}' created successfully.")
            print(f"Directory '{model_folder}' created successfully.")
            return True
        except FileExistsError:
            print(f"Directory '{app_folder}' already exists.")
            print(f"Directory '{model_folder}' already exists.")
            return False
        except PermissionError:
            print(f"Permission denied: Unable to create '{app_folder}'.")
            print(f"Permission denied: Unable to create '{model_folder}'.")
            return False
        except Exception as e:
            print(f"An error occurred: {e}")
            return False
        
    if not __check_base("config.json"):
        Config.create_config()

    if not __check_base("settings.json"):
        Settings.create_settings_if_not_exist()

base()

def get_device():
    """
    Gets the corresponding device, depending on whether a gpu is present or not.
    Will force a cpu, if a gpu isn't present or when it is manually selected
    in the config settings. Requires the user to have a gpu which is supported by cuda
    and the gpu needs to have 7 GB of vram by bare minimum. This is used for the ocr and the ai-model
    in case the user decides to make processing everything, faster. (Increases processing by 30 to 50 times) 
    
    The settings for the amount of GB can be manually changed, but isn't recommended due to GPU requirements.
    It can be lowered, but expect performance issues.
    """
    cpu_forced = Config.get("force_cpu").lower()

    if cpu_forced == "true":
        return torch.device("cpu")
    
    min_gb = float(Config.get("min_gpu_gb"))

    if torch.cuda.is_available():
        gpu_memory = torch.cuda.get_device_properties(0).total_memory / 1e9
        if gpu_memory >= min_gb:
            return torch.device("cuda")
    return torch.device("cpu")

DEVICE = get_device()