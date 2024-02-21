# Adopted from Student Accomplice
# https://github.com/Student-Accomplice-Pipeline-Team/accomplice_pipe/blob/prod/pipe/accomplice/software/maya/pipe/animation/playblastExporter.py

import os
import re
from PySide2 import QtWidgets, QtCore, QtGui
import maya.cmds as mc
from .constants import GAME_CAMERA_NAME
from . import utils

review_folder_path_elements = ["working_files", "Animation", "Review"]
path_to_review_folder = os.path.join(utils.get_path_to_groups_folder(), *review_folder_path_elements)

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
        return [name for name in os.listdir(path_to_review_folder) if os.path.isdir(os.path.join(path_to_review_folder, name))]

    def setupUI(self):
        self.setWindowTitle("Playblast Exporter")
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.setFixedSize(325, 400)

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

        self.viewCheckBoxes = [self.gameViewCheckBox, self.frontViewCheckBox, self.backViewCheckBox, self.leftViewCheckBox, 
                                self.rightViewCheckBox]

        for viewCheckBox in self.viewCheckBoxes:
            viewCheckBox.setChecked(True)
            self.viewSelectionLayout.addWidget(viewCheckBox)

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
            game_view = View(name="GameCamView", cameraName=self.cameraComboBox.currentText())
            views.append(game_view)

        # Front view
        if(self.frontViewCheckBox.isChecked()):
            front_view = View(name="FrontView", cameraName="front")
            views.append(front_view)

        # Back view
        if(self.backViewCheckBox.isChecked()):
            back_view_camera = mc.duplicate("front", name="back")[0]
            mc.select(back_view_camera)
            mc.rotate(0, 180, 0, relative=True, objectSpace=True)
            mc.move(0, 0, 2*-1000.1, relative=True)
            
            back_view = View(name="BackView", cameraName=back_view_camera)
            self.createdCameras.append(back_view_camera)

            views.append(back_view)
        
        # Right view
        if(self.rightViewCheckBox.isChecked()):
            right_view = View(name="RightView", cameraName="side")
            views.append(right_view)
        
        # Left view
        if(self.leftViewCheckBox.isChecked()):
            left_view_camera = mc.duplicate("side", name="left")[0]
            mc.select(left_view_camera)
            mc.rotate(0, 180, 0, relative=True, objectSpace=True)
            mc.move(2*-1000.1, 0, 0, relative=True)

            left_view = View(name="LeftView", cameraName=left_view_camera)
            self.createdCameras.append(left_view_camera)

            views.append(left_view)

        return views

    def discard_cameras(self):
        for camera in self.createdCameras:
            if mc.objExists(camera):
                mc.delete(camera)

    def playblast(self):
        """Exports a playblast of the current animation to ??."""
        currentReview = f"{self.reviewListWidget.currentItem().text()}"
        filepath_folder = os.path.join(path_to_review_folder, currentReview)
        filepath_base = os.path.join(filepath_folder, self.filename)

        print(filepath_base)

        previous_lookthru = mc.lookThru(q=True)
        
        views = self.setup_views()
        try:
            for view in views:
                filepath = f'{filepath_base}_{view.name}'
                mc.lookThru(view.cameraName)
                # mc.playblast(f=filepath, forceOverwrite=True, viewer=False, percent=self.videoScalePct,
                #          format=self.videoFormat, compression=self.videoCompression, widthHeight = [self.width, self.height])
                mc.playblast(f=filepath, forceOverwrite=True, viewer=False, percent=self.videoScalePct,
                                widthHeight = [self.width, self.height])
            
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error",
                                           "Error exporting playblasts. See the script editor for details.")
            print(e)
            return

        # Cleanup
        mc.lookThru(previous_lookthru)
        self.discard_cameras()

        messageBox = QtWidgets.QMessageBox(self)
        messageBox.setText("Playblasts exported successfully!")
        openOutputFolderButton = messageBox.addButton("Open Output Folder", QtWidgets.QMessageBox.AcceptRole)
        openOutputFolderButton.clicked.connect(lambda: os.system('xdg-open "%s"' % os.path.dirname(filepath_folder)))
        openOutputFolderButton.clicked.connect(self.close)
        closeButton = messageBox.addButton("Close", QtWidgets.QMessageBox.RejectRole)
        closeButton.clicked.connect(self.close)
        messageBox.exec_()

    def run(self):
        self.show()
