import sys, os

def run():
    shrineflow_path_prefix = ""
    file_delin = ""
    if os.name == "nt":
        # we're in windows
        shrineflow_path_prefix = 'G:\\shrineflow'
        file_delin = '\\'
    else:
        shrineflow_path_prefix = '/groups/shrineflow'
        file_delin = '/'

    lib_path = f'{shrineflow_path_prefix}{file_delin}y24-pipeline{file_delin}pipeline{file_delin}lib'
    if lib_path not in sys.path:
        sys.path.insert(0, lib_path)
    
    import dwpicker
    dwpicker.show()