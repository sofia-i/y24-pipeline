import sys
import os
from . import utils

studio_library_path = os.path.join(utils.get_path_to_pipe(), "pipeline", "lib", "studiolibrary")
assets_path = os.path.join(utils.get_path_to_groups_folder(), "working_files", "Animation", "StudioLibrary_files")

def run():
    if studio_library_path not in sys.path:
        sys.path.insert(0, studio_library_path)
    import studiolibrary

    studiolibrary.setLibraries([
        {'name': 'Pose Library', 'path': assets_path, 'default': True, 'theme': {'accentColor': 'rgb(3,252,211)',},},
        ])
    studiolibrary.main()

