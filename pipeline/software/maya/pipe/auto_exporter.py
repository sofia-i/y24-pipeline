import os
from . import utils
import maya.cmds as cmds
from . import fbx_exporter as ex


# import pyautogui
# from PIL import ImageGrab
# from functools import partial
# ImageGrab.grab = partial(ImageGrab.grab, all_screens=True)
import time


base_file_path = os.path.join(utils.get_path_to_groups_folder(), "working_files","Animation","used_files")

character_options = ["Kitsune", "Ninja","Barrel","Lantern"]
destination_path_elements = ["assets", "Animation"]
destination_path = os.path.join(utils.get_path_to_groups_folder(), *destination_path_elements)
character_destination_paths = {
    "Kitsune": os.path.join(destination_path, "Kitsune"),
    "Ninja": os.path.join(destination_path, "Ninja"),
    "Barrel": os.path.join(destination_path, "Props", "Barrel"),
    "Lantern": os.path.join(destination_path, "Props", "Lantern")
}

file_types = ["ANIM","TPOSE"]


def run():

    # Get all original file path(s) in maya scene file =================================================
    # Gets correct ref to groups folder
    import maya.OpenMaya as om
    import platform

    def callbackFunction(retCode, fileObject, clientData):

        
        original_path = fileObject.rawFullName()
        
        currentOS = platform.system()
        
        find = ''
        replace = ''
        
        if currentOS == 'Windows':
            find = r"/groups/"
            replace = "G:/"
        elif currentOS == 'Linux':
            find = "G:/"
            replace = r"/groups/"
        
        newFilePath = original_path.replace(find, replace)
        
        # Set the new file path
        fileObject.setRawFullName(newFilePath)
        
        print("***Original Path: "+original_path)
        print("***Replaced Path: "+newFilePath)
        
        # Allow the file to be loaded
        om.MScriptUtil.setBool(retCode, True)

    # Add the callback for file referencing and store the callback ID
    callback_id = om.MSceneMessage.addCheckFileCallback(om.MSceneMessage.kBeforeCreateReferenceCheck, callbackFunction)

    # To delete the callback run this or close and re-open Maya:
    # om.MMessage.removeCallback(callback_id)
    # ==================================================================================================


    # Exports all .mb files in base_file_path
    exported_files = []
    tpose_files = []
    failed_files = []
    for root, dirs, files in os.walk(base_file_path, topdown=False):
        for file in files:
            character = "None"
            for char in character_options:
                if char in root:
                    character = char
                    break
            # character = "Ninja" if "Ninja" in root elif "Kitsune" if "Kitsune" in root elif "Barrel" if "Barrel" in root else "Lantern"
            path = root.replace(base_file_path + f"\\{character}\\","").split("\\")
            path = [] if not path else path
            file_path = os.path.join(root,file)
            print(file_path)


            file_type = "TPOSE" if "TPOSE" in file_path else "ANIM"
            # for ftype in file_types:
            #     if ftype in file_path:
            #         file_type = ftype
            #         break
            


            # Delete the existing file
            anim_path = os.path.join(character_destination_paths[character],*path,file.split('.')[0]+"_" + file_type + ".fbx")
            print(anim_path)
            if os.path.exists(anim_path):
                print("removing " + anim_path)
                os.remove(anim_path)

            if "\\." not in file_path:
                try:
                    cmds.file(file_path, open=True, force=True)
                    print("Export")
                    if file_type == "TPOSE":
                        ex.export(character, tpose=True, anim=False,path=path,close=True)
                        tpose_files.append(file_path)
                    elif file_type == "ANIM":
                        ex.export(character, tpose=False, anim=True,path=path,close=True)
                        exported_files.append(file_path)
                    else:
                        print("Error exporting " + file_path)
                except:
                    print("Failed to export " + file_path)
                    failed_files.append(file_path)

            first = False

    if failed_files:
        print("These Anims Failed to Export:")
        for file in failed_files:
            print(file)
    else: 
        print("All anims exported!")
    print("Exported Anims")
    for file in exported_files:
        print(file)
    for file in tpose_files:
        print(file)

        


 
# run()