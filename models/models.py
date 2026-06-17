from src.utils.config import Config
import pathlib
import os

LOCAL_APPDATA = os.environ.get('LOCALAPPDATA')

class Models():
    """
    This class handles the ai-models
    """
    def __init__(self):
        self.model = Config.get("model")
        self.path_to_model = None

    def get(self):
        """
        This function returns the model that has been selected in the config settings.
        """
        self.set_model()

        return self.path_to_model 

    def set_model(self):
        """
        This function sets the ai-model depending on which one is chosen.
        Will automatically set the default model, given along with the system installation.
        """
        if self.model == "default":
            self.path_to_model = pathlib.Path("models") / "core_pid_model.pt"
            self.path_to_model = self.path_to_model.resolve()
        else:
            self.path_to_model = self.__get_path() / f"{self.model}.pt"

    def __get_path(self):
        app_folder = pathlib.Path(LOCAL_APPDATA) / "interpret_extract_system"
        folder = app_folder / "models"
        if folder.is_dir():
            return folder
        
    def get_models(self):
        """
        This function returns all the models that are present inside of the models folder,
        within the interpret_extract_system folder in the appdata local.
        """
        directory = self.__get_path()
        if not directory:
            return []
       
        return [f.stem for f in directory.iterdir() if f.is_file() and f.suffix == ".pt"]
            




