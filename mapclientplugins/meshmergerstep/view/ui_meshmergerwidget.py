# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mapclientplugins\meshmergerstep\qt\meshmergerwidget.ui'
#
# Created: Mon Sep 11 16:29:39 2017
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_MeshMergerWidget(object):
    def setupUi(self, MeshMergerWidget):
        MeshMergerWidget.setObjectName("MeshMergerWidget")
        MeshMergerWidget.resize(809, 567)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MeshMergerWidget.sizePolicy().hasHeightForWidth())
        MeshMergerWidget.setSizePolicy(sizePolicy)
        self.horizontalLayout = QtGui.QHBoxLayout(MeshMergerWidget)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.dockWidget = QtGui.QDockWidget(MeshMergerWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dockWidget.sizePolicy().hasHeightForWidth())
        self.dockWidget.setSizePolicy(sizePolicy)
        self.dockWidget.setMinimumSize(QtCore.QSize(353, 197))
        self.dockWidget.setFeatures(QtGui.QDockWidget.DockWidgetFloatable|QtGui.QDockWidget.DockWidgetMovable)
        self.dockWidget.setAllowedAreas(QtCore.Qt.AllDockWidgetAreas)
        self.dockWidget.setObjectName("dockWidget")
        self.dockWidgetContents = QtGui.QWidget()
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dockWidgetContents.sizePolicy().hasHeightForWidth())
        self.dockWidgetContents.setSizePolicy(sizePolicy)
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.verticalLayout = QtGui.QVBoxLayout(self.dockWidgetContents)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.scrollArea = QtGui.QScrollArea(self.dockWidgetContents)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollArea.sizePolicy().hasHeightForWidth())
        self.scrollArea.setSizePolicy(sizePolicy)
        self.scrollArea.setMinimumSize(QtCore.QSize(0, 0))
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents_2 = QtGui.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 351, 503))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollAreaWidgetContents_2.sizePolicy().hasHeightForWidth())
        self.scrollAreaWidgetContents_2.setSizePolicy(sizePolicy)
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.scrollAreaWidgetContents_2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.identifier_frame = QtGui.QFrame(self.scrollAreaWidgetContents_2)
        self.identifier_frame.setMinimumSize(QtCore.QSize(0, 0))
        self.identifier_frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.identifier_frame.setFrameShadow(QtGui.QFrame.Raised)
        self.identifier_frame.setObjectName("identifier_frame")
        self.verticalLayout_5 = QtGui.QVBoxLayout(self.identifier_frame)
        self.verticalLayout_5.setContentsMargins(-1, 5, -1, 3)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.identifier_label = QtGui.QLabel(self.identifier_frame)
        self.identifier_label.setObjectName("identifier_label")
        self.verticalLayout_5.addWidget(self.identifier_label)
        self.line = QtGui.QFrame(self.identifier_frame)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout_5.addWidget(self.line)
        self.verticalLayout_3.addWidget(self.identifier_frame)
        self.mergeOptions_frame = QtGui.QFrame(self.scrollAreaWidgetContents_2)
        self.mergeOptions_frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.mergeOptions_frame.setFrameShadow(QtGui.QFrame.Raised)
        self.mergeOptions_frame.setObjectName("mergeOptions_frame")
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.mergeOptions_frame)
        self.verticalLayout_4.setContentsMargins(-1, 3, -1, -1)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.mergeNodes_label = QtGui.QLabel(self.mergeOptions_frame)
        self.mergeNodes_label.setObjectName("mergeNodes_label")
        self.verticalLayout_4.addWidget(self.mergeNodes_label)
        self.mergeNodesEntry_widget = QtGui.QWidget(self.mergeOptions_frame)
        self.mergeNodesEntry_widget.setObjectName("mergeNodesEntry_widget")
        self.horizontalLayout_4 = QtGui.QHBoxLayout(self.mergeNodesEntry_widget)
        self.horizontalLayout_4.setSpacing(3)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.mergeNodesEntry_lineEdit = QtGui.QLineEdit(self.mergeNodesEntry_widget)
        self.mergeNodesEntry_lineEdit.setObjectName("mergeNodesEntry_lineEdit")
        self.horizontalLayout_4.addWidget(self.mergeNodesEntry_lineEdit)
        self.mergeNodesDelete_pushButton = QtGui.QPushButton(self.mergeNodesEntry_widget)
        self.mergeNodesDelete_pushButton.setObjectName("mergeNodesDelete_pushButton")
        self.horizontalLayout_4.addWidget(self.mergeNodesDelete_pushButton)
        self.verticalLayout_4.addWidget(self.mergeNodesEntry_widget)
        self.mergeNodes_plainTextEdit = QtGui.QPlainTextEdit(self.mergeOptions_frame)
        self.mergeNodes_plainTextEdit.setReadOnly(True)
        self.mergeNodes_plainTextEdit.setObjectName("mergeNodes_plainTextEdit")
        self.verticalLayout_4.addWidget(self.mergeNodes_plainTextEdit)
        self.previewAlign_checkBox = QtGui.QCheckBox(self.mergeOptions_frame)
        self.previewAlign_checkBox.setObjectName("previewAlign_checkBox")
        self.verticalLayout_4.addWidget(self.previewAlign_checkBox)
        self.previewFit_checkBox = QtGui.QCheckBox(self.mergeOptions_frame)
        self.previewFit_checkBox.setObjectName("previewFit_checkBox")
        self.verticalLayout_4.addWidget(self.previewFit_checkBox)
        self.verticalLayout_3.addWidget(self.mergeOptions_frame)
        self.displayOptions_groupBox = QtGui.QGroupBox(self.scrollAreaWidgetContents_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.displayOptions_groupBox.sizePolicy().hasHeightForWidth())
        self.displayOptions_groupBox.setSizePolicy(sizePolicy)
        self.displayOptions_groupBox.setObjectName("displayOptions_groupBox")
        self.verticalLayout_7 = QtGui.QVBoxLayout(self.displayOptions_groupBox)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.displayAxes_checkBox = QtGui.QCheckBox(self.displayOptions_groupBox)
        self.displayAxes_checkBox.setEnabled(True)
        self.displayAxes_checkBox.setObjectName("displayAxes_checkBox")
        self.verticalLayout_7.addWidget(self.displayAxes_checkBox)
        self.displayLines_checkBox = QtGui.QCheckBox(self.displayOptions_groupBox)
        self.displayLines_checkBox.setObjectName("displayLines_checkBox")
        self.verticalLayout_7.addWidget(self.displayLines_checkBox)
        self.displaySurfaces_checkBox = QtGui.QCheckBox(self.displayOptions_groupBox)
        self.displaySurfaces_checkBox.setObjectName("displaySurfaces_checkBox")
        self.verticalLayout_7.addWidget(self.displaySurfaces_checkBox)
        self.displayElementNumbers_checkBox = QtGui.QCheckBox(self.displayOptions_groupBox)
        self.displayElementNumbers_checkBox.setObjectName("displayElementNumbers_checkBox")
        self.verticalLayout_7.addWidget(self.displayElementNumbers_checkBox)
        self.displayNodeNumbers_checkBox = QtGui.QCheckBox(self.displayOptions_groupBox)
        self.displayNodeNumbers_checkBox.setObjectName("displayNodeNumbers_checkBox")
        self.verticalLayout_7.addWidget(self.displayNodeNumbers_checkBox)
        self.displayNodeDerivatives_checkBox = QtGui.QCheckBox(self.displayOptions_groupBox)
        self.displayNodeDerivatives_checkBox.setEnabled(True)
        self.displayNodeDerivatives_checkBox.setObjectName("displayNodeDerivatives_checkBox")
        self.verticalLayout_7.addWidget(self.displayNodeDerivatives_checkBox)
        self.displayXiAxes_checkBox = QtGui.QCheckBox(self.displayOptions_groupBox)
        self.displayXiAxes_checkBox.setEnabled(True)
        self.displayXiAxes_checkBox.setObjectName("displayXiAxes_checkBox")
        self.verticalLayout_7.addWidget(self.displayXiAxes_checkBox)
        self.verticalLayout_3.addWidget(self.displayOptions_groupBox)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem)
        self.verticalLayout_2.addLayout(self.verticalLayout_3)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents_2)
        self.verticalLayout.addWidget(self.scrollArea)
        self.frame = QtGui.QFrame(self.dockWidgetContents)
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.frame)
        self.horizontalLayout_2.setContentsMargins(3, 3, 3, 3)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.viewAll_button = QtGui.QPushButton(self.frame)
        self.viewAll_button.setObjectName("viewAll_button")
        self.horizontalLayout_2.addWidget(self.viewAll_button)
        self.done_button = QtGui.QPushButton(self.frame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.done_button.sizePolicy().hasHeightForWidth())
        self.done_button.setSizePolicy(sizePolicy)
        self.done_button.setObjectName("done_button")
        self.horizontalLayout_2.addWidget(self.done_button)
        self.verticalLayout.addWidget(self.frame)
        self.dockWidget.setWidget(self.dockWidgetContents)
        self.horizontalLayout.addWidget(self.dockWidget)
        self.sceneviewer_frame = QtGui.QFrame(MeshMergerWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sceneviewer_frame.sizePolicy().hasHeightForWidth())
        self.sceneviewer_frame.setSizePolicy(sizePolicy)
        self.sceneviewer_frame.setObjectName("sceneviewer_frame")
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.sceneviewer_frame)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.splitter = QtGui.QSplitter(self.sceneviewer_frame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.splitter.sizePolicy().hasHeightForWidth())
        self.splitter.setSizePolicy(sizePolicy)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.master_sceneviewerWidget = SceneviewerWidget(self.splitter)
        self.master_sceneviewerWidget.setObjectName("master_sceneviewerWidget")
        self.slave_sceneviewerWidget = SceneviewerWidget(self.splitter, self.master_sceneviewerWidget)
        self.slave_sceneviewerWidget.setObjectName("slave_sceneviewerWidget")
        self.horizontalLayout_3.addWidget(self.splitter)
        self.horizontalLayout.addWidget(self.sceneviewer_frame)

        self.retranslateUi(MeshMergerWidget)
        QtCore.QMetaObject.connectSlotsByName(MeshMergerWidget)

    def retranslateUi(self, MeshMergerWidget):
        MeshMergerWidget.setWindowTitle(QtGui.QApplication.translate("MeshMergerWidget", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.dockWidget.setWindowTitle(QtGui.QApplication.translate("MeshMergerWidget", "Mesh Merger Controls", None, QtGui.QApplication.UnicodeUTF8))
        self.identifier_label.setText(QtGui.QApplication.translate("MeshMergerWidget", "Identifier", None, QtGui.QApplication.UnicodeUTF8))
        self.mergeNodes_label.setText(QtGui.QApplication.translate("MeshMergerWidget", "Merge nodes master=slave (e.g. 1=55):", None, QtGui.QApplication.UnicodeUTF8))
        self.mergeNodesDelete_pushButton.setText(QtGui.QApplication.translate("MeshMergerWidget", "Delete", None, QtGui.QApplication.UnicodeUTF8))
        self.previewAlign_checkBox.setText(QtGui.QApplication.translate("MeshMergerWidget", "Preview align", None, QtGui.QApplication.UnicodeUTF8))
        self.previewFit_checkBox.setText(QtGui.QApplication.translate("MeshMergerWidget", "Preview fit", None, QtGui.QApplication.UnicodeUTF8))
        self.displayOptions_groupBox.setTitle(QtGui.QApplication.translate("MeshMergerWidget", "Display options:", None, QtGui.QApplication.UnicodeUTF8))
        self.displayAxes_checkBox.setText(QtGui.QApplication.translate("MeshMergerWidget", "Axes", None, QtGui.QApplication.UnicodeUTF8))
        self.displayLines_checkBox.setText(QtGui.QApplication.translate("MeshMergerWidget", "Lines", None, QtGui.QApplication.UnicodeUTF8))
        self.displaySurfaces_checkBox.setText(QtGui.QApplication.translate("MeshMergerWidget", "Surfaces", None, QtGui.QApplication.UnicodeUTF8))
        self.displayElementNumbers_checkBox.setText(QtGui.QApplication.translate("MeshMergerWidget", "Element numbers", None, QtGui.QApplication.UnicodeUTF8))
        self.displayNodeNumbers_checkBox.setText(QtGui.QApplication.translate("MeshMergerWidget", "Node numbers", None, QtGui.QApplication.UnicodeUTF8))
        self.displayNodeDerivatives_checkBox.setText(QtGui.QApplication.translate("MeshMergerWidget", "Node derivatives", None, QtGui.QApplication.UnicodeUTF8))
        self.displayXiAxes_checkBox.setText(QtGui.QApplication.translate("MeshMergerWidget", "Xi axes", None, QtGui.QApplication.UnicodeUTF8))
        self.viewAll_button.setText(QtGui.QApplication.translate("MeshMergerWidget", "View All", None, QtGui.QApplication.UnicodeUTF8))
        self.done_button.setText(QtGui.QApplication.translate("MeshMergerWidget", "Done", None, QtGui.QApplication.UnicodeUTF8))

from opencmiss.zincwidgets.sceneviewerwidget import SceneviewerWidget
