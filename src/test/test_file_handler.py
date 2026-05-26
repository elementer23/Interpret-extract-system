from handler.file_handler import FileOsHandler
from test.test_settings import mock_retrieve_settings
import os
from utils.utilities import BasicUtils
import pathlib

def mock_formulate_files_dir():
    path = mock_retrieve_settings('temp_files_path')
    path_name = mock_retrieve_settings('temp_files_name')

    return [path, path_name]

def test_formulate_files_dir():
    path = mock_retrieve_settings('temp_files_path')
    path_name = mock_retrieve_settings('temp_files_name')

    assert path == "C:/Users/697/Documents"
    assert path_name == "test_container"

def test_copy_files():
    path = mock_formulate_files_dir()
    target_path = os.path.join(path[0], path[1])
    FileOsHandler().create_dir(path[0], path[1])

    files_to_copy = ["Hello.pdf", "mock_settings.json"]

    FileOsHandler().copy_files(files_to_copy, target_path)

    base_names = []

    files = os.listdir(target_path)
    for file in files:
        base_names.append(os.path.basename(file))

    assert True if base_names[0] and base_names[1] in files_to_copy else False

    # FileOsHandler().remove_dir(target_path)

def test_get_temp_files_dir():
    path = mock_formulate_files_dir()
    target_path = os.path.join(path[0], path[1])

    files = os.listdir(target_path)
    file_context = []

    for file in files:
        full_path = os.path.join(target_path, file)
        if pathlib.Path(full_path).is_dir():
            continue
        
        file_context.append({"file": file, "dir": full_path})

    for output in file_context:
        assert True if output['file'] == "Hello.pdf" or output['file'] == "mock_settings.json" else False

    # FileOsHandler().remove_dir(target_path)

def test_delete_files():
    path = mock_formulate_files_dir()
    target_path = os.path.join(path[0], path[1])

    file_list = []
    files = os.listdir(target_path)
    for file in files:
        full_path = os.path.join(target_path, file)
        file_list.append(full_path)

    for f in file_list:
        if BasicUtils.does_file_exist(f, target_directory=f"{target_path}/"):
            os.remove(f)

    assert True if BasicUtils.is_directory_empty(f"{target_path}") else False

    FileOsHandler().remove_dir(target_path)