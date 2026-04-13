import pathlib
import os
import shutil

class ZipExporter():
    def __init__(self):
        pass

    def remove_dir(self, dir_path: str) -> None:
        for file in os.listdir(dir_path):
            file_path = os.path.join(dir_path, file)

            if os.path.isfile(file_path):
                os.remove(file_path)

        pathlib.Path(dir_path).rmdir()

    def export_to_zip(self, dir_path: str, dir_name: str) -> None:
        shutil.make_archive(base_name=f"{dir_path}/{dir_name}", format="zip", root_dir=f"{dir_path}/{dir_name}")
        self.remove_dir(f"{dir_path}/{dir_name}")
        