import sys, os

def get_path_to_pipe():
    if os.name == "nt":
        # WINDOWS
        return "G:\\shrineflow\\y24-pipeline"
    else:
        # LINUX
        return "/groups/shrineflow/y24-pipeline"

def get_path_to_groups_folder():
    if os.name == "nt":
        # WINDOWS
        return "G:\\shrineflow"
    else:
        # LINUX
        return "/groups/shrineflow"
        