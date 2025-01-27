# Copyright 2020 by Kurt Rathjen. All Rights Reserved.
#
# This library is free software: you can redistribute it and/or modify it 
# under the terms of the GNU Lesser General Public License as published by 
# the Free Software Foundation, either version 3 of the License, or 
# (at your option) any later version. This library is distributed in the 
# hope that it will be useful, but WITHOUT ANY WARRANTY; without even the 
# implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. 
# See the GNU Lesser General Public License for more details.
# You should have received a copy of the GNU Lesser General Public
# License along with this library. If not, see <http://www.gnu.org/licenses/>.

import os
import logging
from functools import partial

from studiovendor.Qt import QtGui
from studiovendor.Qt import QtWidgets

import studiolibrary

from studiolibrarymaya import setsitem


logger = logging.getLogger(__name__)


DIRNAME = os.path.dirname(__file__)
ARROW_ICON_PATH = os.path.join(DIRNAME, "icons", "arrow.png")


def selectContentAction(item, parent=None):
    """
    :param item: mayabaseitem.MayaBaseItem
    :param parent: QtWidgets.QMenu
    """
    arrowIcon = QtGui.QIcon(ARROW_ICON_PATH)
    action = QtWidgets.QAction(arrowIcon, "Select content", parent)
    action.triggered.connect(item.selectContent)
    return action


def showSetsMenu(path, **kwargs):
    """
    Show the frame range menu at the current cursor position.

    :type path: str
    :rtype: QtWidgets.QAction
    """
    menu = SetsMenu.fromPath(path, **kwargs)
    position = QtGui.QCursor().pos()
    action = menu.exec_(position)
    return action


class SetsMenu(QtWidgets.QMenu):

    @classmethod
    def fromPath(cls, path, parent=None, libraryWindow=None, **kwargs):
        """
        Return a new SetMenu instance from the given path.
        
        :type path: str
        :type parent: QtWidgets.QMenu or None
        :type libraryWindow: studiolibrary.LibraryWindow or None
        :type kwargs: dict
        :rtype: QtWidgets.QAction
        """
        item = setsitem.SetsItem(path, libraryWindow=libraryWindow)
        return cls(item, parent, enableSelectContent=False, **kwargs)

    def __init__(
            self,
            item,
            parent=None,
            namespaces=None,
            enableSelectContent=True,
    ):
        """
        :type item: studiolibrarymaya.BaseItem
        :type parent: QtWidgets.QMenu or None
        :type namespaces: list[str] or None
        :type enableSelectContent: bool
        """
        parent = parent or item.libraryWindow()
        QtWidgets.QMenu.__init__(self, "Selection Sets", parent)

        icon = QtGui.QIcon(setsitem.SetsItem.ICON_PATH)
        self.setIcon(icon)

        self._item = item
        self._namespaces = namespaces
        self._enableSelectContent = enableSelectContent
        self.reload()

    def item(self):
        """
        :rtype: mayabaseitem.MayaBaseItem
        """
        return self._item

    def namespaces(self):
        """
        :rtype: list[str]
        """
        return self._namespaces

    def selectContent(self):
        """
        :rtype: None
        """
        self.item().selectContent(namespaces=self.namespaces())

    def selectionSets(self):
        """
        :rtype: list[setsitem.SetsItem]
        """
        path = self.item().path()

        paths = studiolibrary.walkup(
            path,
            match=lambda path: path.endswith(".set"),
            depth=10,
        )

        items = []
        paths = list(paths)
        libraryWindow = self.item().libraryWindow()

        for path in paths:
            item = setsitem.SetsItem(path)
            item.setLibraryWindow(libraryWindow)
            items.append(item)

        return items

    def reload(self):
        """
        :rtype: None
        """
        self.clear()

        if self._enableSelectContent:
            action = selectContentAction(item=self.item(), parent=self)
            self.addAction(action)
            self.addSeparator()

        selectionSets = self.selectionSets()

        if selectionSets:
            for selectionSet in selectionSets:

                dirname = os.path.basename(os.path.dirname(selectionSet.path()))

                basename = os.path.basename(selectionSet.path())
                basename = basename.replace(selectionSet.EXTENSION, "")

                nicename = dirname + ": " + basename

                action = QtWidgets.QAction(nicename, self)
                callback = partial(selectionSet.load, namespaces=self.namespaces())
                action.triggered.connect(callback)
                self.addAction(action)
        else:
            action = QtWidgets.QAction("No selection sets found!", self)
            action.setEnabled(False)
            self.addAction(action)
