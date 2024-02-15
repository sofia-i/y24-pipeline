import maya.cmds as mc
import logging
import os
from . import utils

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


def ref(filePath, namespace):
    mc.file(filePath, r = True, namespace = namespace)

def rig(rig_name):
    filePath = os.path.join(utils.get_path_to_groups_folder(), "assets", "Characters", "Rigs", f'{rig_name}.mb')

    ref(filePath, rig_name)
