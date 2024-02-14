import sys, os
from . import utils

path_to_picker = ["working_files", "Animation", "Picker_files"]

picker_filenames = [
    "Ninja_Picker.json",
    "Kitsune_Picker.json"
]

def run():
    pipeline_path = utils.get_path_to_pipe()
    lib_path = os.path.join(pipeline_path, "pipeline", "lib")

    if lib_path not in sys.path:
        sys.path.insert(0, lib_path)
    
    import dwpicker

    picker_folder_path = os.path.join(utils.get_path_to_groups_folder(), *path_to_picker)
    picker_filepaths = [os.path.join(picker_folder_path, picker_filename) for picker_filename in picker_filenames]
    print("Picker filepaths", picker_filepaths)

    dwpicker.show(pickers=picker_filepaths)
