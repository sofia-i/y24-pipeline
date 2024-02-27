# Adopted from Student Accomplice
# https://github.com/Student-Accomplice-Pipeline-Team/accomplice_pipe/blob/prod/pipe/accomplice/software/maya/pipe/animation/playblastExporter.py

import os, sys
import subprocess
import re
from PySide2 import QtWidgets, QtCore, QtGui
import maya.cmds as mc
from .constants import GAME_CAMERA_NAME
from . import utils

GAME_CAM_VIEW_NAME = "GameCamView"
FRONT_VIEW_NAME = "FrontView"
BACK_VIEW_NAME = "BackView"
LEFT_VIEW_NAME = "LeftView"
RIGHT_VIEW_NAME = "RightView"
COMPOSITE_VIEW_NAME = "Grid"

review_folder_path_elements = ["working_files", "Animation", "Review"]
path_to_review_folder = os.path.join(utils.get_path_to_groups_folder(), *review_folder_path_elements)

FFMPEG_PATH = ""
VIDEO_EXTENSION = ""
if os.name == "nt":
    # WINDOWS
    VIDEO_EXTENSION = ".avi"
    ffmpeg_path_elements = ["pipeline", "lib", "ffmpeg_exe", "ffmpeg"]
else:
    # LINUX
    VIDEO_EXTENSION = ".mov"
    ffmpeg_path_elements = ["pipeline", "lib", "ffmpeg", "ffmpeg"]
FFMPEG_PATH = os.path.join(utils.get_path_to_pipe(), *ffmpeg_path_elements)

class View():
    def __init__(self, name, cameraName):
        self.name = name
        self.cameraName = cameraName

class PlayblastExporter(QtWidgets.QMainWindow):
    def __init__(self):
        super(PlayblastExporter, self).__init__()

        self.filename = ""
        self.videoFormat = "qt"
        self.videoScalePct = 100
        self.videoCompression = "Animation"
        self.videoOutputType = "movie"
        self.width = 1920
        self.height = 1080
        
        self.createdCameras = []

        self.reviews = self.getReviews()
        self.filename = self.getFilename()

        self.setupUI()

    def getFilename(self):
        current_filepath = mc.file(q=True, sn=True)
        current_filename = os.path.basename(current_filepath)
        raw_name, extension = os.path.splitext(current_filename)
        return raw_name

    def getReviews(self):
        reviews = [name for name in os.listdir(path_to_review_folder) if os.path.isdir(os.path.join(path_to_review_folder, name))]
        reviews.sort(reverse=True)
        return reviews
    
    def updateGridAvailable(self, value):
        if(not value):
            self.compositeViewCheckBox.setEnabled(False)
        elif(self.gameViewCheckBox.isChecked() and self.frontViewCheckBox.isChecked() and self.leftViewCheckBox.isChecked() and self.rightViewCheckBox.isChecked()):
            self.compositeViewCheckBox.setEnabled(True)

    def setupUI(self):
        self.setWindowTitle("Playblast Exporter")
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.setFixedSize(325, 425)

        self.mainWidget = QtWidgets.QWidget()
        self.mainLayout = QtWidgets.QVBoxLayout(self.mainWidget)
        self.setCentralWidget(self.mainWidget)

        # LISTS
        self.listLayout = QtWidgets.QHBoxLayout()
        self.mainLayout.addLayout(self.listLayout)

        self.reviewLayout = QtWidgets.QVBoxLayout()
        self.listLayout.addLayout(self.reviewLayout)

        self.reviewLabel = QtWidgets.QLabel("Reviews")
        self.reviewLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.reviewLayout.addWidget(self.reviewLabel)

        self.reviewListWidget = QtWidgets.QListWidget()
        self.reviewListWidget.setFixedWidth(150)
        self.reviewListWidget.addItems(self.reviews)
        self.reviewLayout.addWidget(self.reviewListWidget)

        # CAMERA SELECT
        self.cameraSelectLayout = QtWidgets.QHBoxLayout()
        self.mainLayout.addLayout(self.cameraSelectLayout)

        self.cameraLabel = QtWidgets.QLabel("Game Camera")
        self.cameraSelectLayout.addWidget(self.cameraLabel)

        # add all the scene cameras to the combo box
        self.cameraComboBox = QtWidgets.QComboBox()
        all_cameras = mc.ls(type=('camera'))
        # remove the default cameras
        custom_cameras = [camera for camera in all_cameras if (not mc.camera(mc.listRelatives(camera,parent=True)[0], startupCamera=True, q=True) or camera=="perspShape")]
        self.cameraComboBox.addItems(custom_cameras)

        # select one that matches the game camera name, if there is one
        r = re.compile(f'{GAME_CAMERA_NAME}\w*')
        game_cameras = list(filter(r.match, custom_cameras))
        if len(game_cameras) > 0:
            try:
                self.cameraComboBox.setCurrentText(game_cameras[0])
            except:
                print("Exception when trying to pull game camera. Select game camera manually.")
        
        self.cameraSelectLayout.addWidget(self.cameraComboBox)
        
        # VIEW SELECT
        self.viewSelectionLayout = QtWidgets.QVBoxLayout()
        self.mainLayout.addLayout(self.viewSelectionLayout)

        self.gameViewCheckBox = QtWidgets.QCheckBox("Game Cam View")
        self.frontViewCheckBox = QtWidgets.QCheckBox("Front View")
        self.backViewCheckBox = QtWidgets.QCheckBox("Back View")
        self.leftViewCheckBox = QtWidgets.QCheckBox("Left View")
        self.rightViewCheckBox = QtWidgets.QCheckBox("Right View")
        self.compositeViewCheckBox = QtWidgets.QCheckBox("Combined Grid")

        for checkBox in [self.gameViewCheckBox, self.frontViewCheckBox, self.rightViewCheckBox, self.leftViewCheckBox]:
            checkBox.stateChanged.connect(self.updateGridAvailable)

        self.viewCheckBoxes = [self.gameViewCheckBox, self.frontViewCheckBox, self.backViewCheckBox, self.leftViewCheckBox, 
                                self.rightViewCheckBox]

        for viewCheckBox in self.viewCheckBoxes:
            viewCheckBox.setChecked(True)
            self.viewSelectionLayout.addWidget(viewCheckBox)

        # Composite menu
        self.compositeSelectLayout = QtWidgets.QVBoxLayout()
        self.mainLayout.addLayout(self.compositeSelectLayout)
        self.compositeLabel = QtWidgets.QLabel("Combine views into grid (must have Game, Front, Right, and Left checked)")
        self.compositeLabel.setWordWrap(True)
        self.compositeSelectLayout.addWidget(self.compositeLabel)
        self.compositeViewCheckBox.setChecked(True)
        self.compositeSelectLayout.addWidget(self.compositeViewCheckBox)

        # BUTTONS
        self.buttonLayout = QtWidgets.QHBoxLayout()
        self.mainLayout.addLayout(self.buttonLayout)

        self.exportButton = QtWidgets.QPushButton("Playblast")
        self.exportButton.clicked.connect(self.playblast)
        self.buttonLayout.addWidget(self.exportButton)

        self.cancelButton = QtWidgets.QPushButton("Cancel")
        self.buttonLayout.addWidget(self.cancelButton)
        
        self.cancelButton.clicked.connect(self.close)

    def setup_views(self):
        views = []

        # Game Camera view
        if(self.gameViewCheckBox.isChecked()):
            game_view = View(name=GAME_CAM_VIEW_NAME, cameraName=self.cameraComboBox.currentText())
            views.append(game_view)

        # Front view
        if(self.frontViewCheckBox.isChecked()):
            front_view = View(name=FRONT_VIEW_NAME, cameraName="front")
            views.append(front_view)

        # Back view
        if(self.backViewCheckBox.isChecked()):
            back_view_camera = mc.duplicate("front", name="back")[0]
            mc.select(back_view_camera)
            mc.rotate(0, 180, 0, relative=True, objectSpace=True)
            mc.move(0, 0, 2*-1000.1, relative=True)
            
            back_view = View(name=BACK_VIEW_NAME, cameraName=back_view_camera)
            self.createdCameras.append(back_view_camera)

            views.append(back_view)
        
        # Right view
        if(self.rightViewCheckBox.isChecked()):
            right_view = View(name=RIGHT_VIEW_NAME, cameraName="side")
            views.append(right_view)
        
        # Left view
        if(self.leftViewCheckBox.isChecked()):
            left_view_camera = mc.duplicate("side", name="left")[0]
            mc.select(left_view_camera)
            mc.rotate(0, 180, 0, relative=True, objectSpace=True)
            mc.move(2*-1000.1, 0, 0, relative=True)

            left_view = View(name=LEFT_VIEW_NAME, cameraName=left_view_camera)
            self.createdCameras.append(left_view_camera)

            views.append(left_view)

        return views

    def discard_cameras(self):
        for camera in self.createdCameras:
            if mc.objExists(camera):
                mc.delete(camera)

    def setup_progress_ui(self, num_tasks):
        self.progressWindow = mc.window(title="Playblast Progress")
        mc.columnLayout()
        self.progressTextLabel = mc.text(label='Playblasting...', width=300)
        self.progressControl = mc.progressBar(maxValue=num_tasks, width=300)
        mc.showWindow(self.progressWindow)

        return self.progressControl

    def playblast(self):
        """Exports a playblast of the current animation to ??."""
        currentReview = f"{self.reviewListWidget.currentItem().text()}"
        filepath_folder = os.path.join(path_to_review_folder, currentReview)
        filepath_base = os.path.join(filepath_folder, self.filename)

        do_composite = self.compositeViewCheckBox.isEnabled() and self.compositeViewCheckBox.isChecked()

        # print(filepath_base)

        previous_lookthru = mc.lookThru(q=True)
        
        views = self.setup_views()

        num_tasks = len(views)
        if do_composite: 
            num_tasks += 1
        progressControl = self.setup_progress_ui(num_tasks)

        result_files = {}
        try:
            for view in views:
                filepath = f'{filepath_base}_{view.name}'
                mc.lookThru(view.cameraName)
                # mc.playblast(f=filepath, forceOverwrite=True, viewer=False, percent=self.videoScalePct,
                #          format=self.videoFormat, compression=self.videoCompression, widthHeight = [self.width, self.height])
                result = mc.playblast(f=filepath, forceOverwrite=True, viewer=False, percent=self.videoScalePct,
                                widthHeight = [self.width, self.height])
                result_files[view.name] = result
                # Progress UI
                mc.progressBar(progressControl, edit=True, step=1)
            
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error",
                                           "Error exporting playblasts. See the script editor for details.")
            mc.error(f"Error while playblasting: {e}")
            return

        # Cleanup
        mc.lookThru(previous_lookthru)
        self.discard_cameras()

        # Composite a grid video
        if do_composite:
            try:
                self.composite(filepath_base, result_files)

                mc.progressBar(progressControl, edit=True, step=1)
            except Exception as e:
                print(f"Composite failed, exception: {e}")

        mc.deleteUI(self.progressWindow)

        messageBox = QtWidgets.QMessageBox(self)
        messageBox.setText("Playblasts exported successfully!")
        openOutputFolderButton = messageBox.addButton("Open Output Folder", QtWidgets.QMessageBox.AcceptRole)
        openOutputFolderButton.clicked.connect(lambda: os.system('xdg-open "%s"' % os.path.dirname(filepath_folder)))
        openOutputFolderButton.clicked.connect(self.close)
        closeButton = messageBox.addButton("Close", QtWidgets.QMessageBox.RejectRole)
        closeButton.clicked.connect(self.close)
        messageBox.exec_()

    def construct_ffmpeg_cmd(self, input_video_paths, output_path, 
                             width=1920, height=1080, grid_width=2, grid_height=2):
        # Taken from https://stackoverflow.com/questions/63993922/how-to-merge-several-videos-in-a-grid-in-one-video
        input_videos = ""
        input_setpts = "nullsrc=size={}x{} [base];".format(width, height)
        input_overlays = "[base][video0] overlay=shortest=1 [tmp0];"
        for index, path_video in enumerate(input_video_paths):
                input_videos += " -i " + path_video
                input_setpts += "[{}:v] setpts=PTS-STARTPTS, scale={}x{} [video{}];".format(index, width//grid_width, height//grid_height, index)
                if index > 0 and index < len(input_video_paths) - 1:
                    input_overlays += "[tmp{}][video{}] overlay=shortest=1:x={}:y={} [tmp{}];".format(index-1, index, width//grid_width * (index%grid_width), height//grid_height * (index//grid_width), index)
                if index == len(input_video_paths) - 1:
                    input_overlays += "[tmp{}][video{}] overlay=shortest=1:x={}:y={}".format(index-1, index, width//grid_width * (index%grid_width), height//grid_height * (index//grid_width))

        complete_command = FFMPEG_PATH + " " + input_videos + " -filter_complex \"" + input_setpts + input_overlays + "\" -c:v libx264 " + output_path

        return complete_command

    def composite(self, filepath_base: str, files: dict):
        if GAME_CAM_VIEW_NAME not in files:
            raise Exception("Game cam not found")
        elif FRONT_VIEW_NAME not in files:
            raise Exception("Front not found")
        elif RIGHT_VIEW_NAME not in files:
            raise Exception("Right not found")
        elif LEFT_VIEW_NAME not in files:
            raise Exception("Left not found")
        
        video_paths = [f'{path}{VIDEO_EXTENSION}' for path in [files[GAME_CAM_VIEW_NAME], files[FRONT_VIEW_NAME], files[RIGHT_VIEW_NAME], files[LEFT_VIEW_NAME]]]
        output_path = f"{filepath_base}_{COMPOSITE_VIEW_NAME}.mp4"
        ffmpeg_command = self.construct_ffmpeg_cmd(video_paths, output_path)
        # if not os.name == "nt":
            # linux
        #     ffmpeg_command = ffmpeg_command.split()

        try:
            process = subprocess.Popen(ffmpeg_command, shell=True)
            process.communicate()
            process.wait()
        except Exception as e:
            mc.confirmDialog(icon = 'critical', title = 'Error', message = 'Following error occurred while compiling video \n{}'.format(e))

    def run(self):
        self.show()
