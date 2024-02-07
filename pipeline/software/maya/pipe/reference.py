import maya.cmds as mc
import logging
import pipe
import os
import platform

def logMessage(logName, message):
    logger = logging.getLogger(logName)
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    # create formatter
    formatter = logging.Formatter('%(name)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    # prevent logging from bubbling up to maya's logger
    logger.propagate=0
    # 'application' code
    logger.info(message)

# ninja_rig_name = "Ninja_Rig"
# kitsune_rig_name = "Kitsune_Rig"
rig_path_win = 'G:\\shrineflow\\assets\\Characters\\Rigs\\'
rig_path_lin = '/groups/shrineflow/assets/Characters/Rigs/'


def ref(filePath, namespace):
    mc.file(filePath, r = True, namespace = namespace)

def rig(rig_name):
    if platform.system() == 'Windows':
        filePath = f'{rig_path_win}{rig_name}.mb'
    elif platform.system() == 'Linux':
        filePath = f'{rig_path_lin}{rig_name}.mb'

    # if platform.system() == 'Windows':
    #     # if rig_name == ninja_rig_name:
    #         filePath = f'G:\\shrineflow\\assets\\Characters\\Rigs\\{rig_name}.mb'

    #     # elif rig_name == 'kitsune':
    #         # filePath = 'G:\\shrineflow\\assets\\Characters\\Rigs\\Kitsune_Rig.mb'
            
    # elif platform.system() == 'Linux':
    #     if rig_name == 'ninja':
    #         filePath = '/groups/shrineflow/assets/Characters/Rigs/Ninja_Rig.mb'

    #     elif rig_name == 'kitsune':
    #         filePath = '/groups/shrineflow/assets/Characters/Rigs/Kitsune_Rig.mb'

    self.ref(filePath, rig_name)
    # self.ref(filePath, rig_name)

'''def camera(self):
    env = environment.Environment()
    filePath = mc.file(q=True, sn=True)
    curDir = env.get_file_dir(filePath)[1:]
    if (filePath.find('/groups/unfamiliar/anim_pipeline/production/anim_shots') == -1):
        logMessage('Camera Importer', 'Not in a valid shot file. Please check out a shot and try again.')
        return
    shotName = curDir.split('/')[-1]
    shotsDir = '/groups/unfamiliar/anim_pipeline/production/shots'
    camPath = shotsDir + '/' + shotName + '/camera/camera_main.fbx'
    if os.path.exists(camPath) == False:
        logMessage('Camera Importer', 'No camera has been published for this shot.')
        return
    self.ref(camPath, shotName)'''
