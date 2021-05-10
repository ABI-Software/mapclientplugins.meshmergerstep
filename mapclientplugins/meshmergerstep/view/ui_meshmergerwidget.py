# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'meshmergerwidget.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from opencmiss.zincwidgets.sceneviewerwidget import SceneviewerWidget


class Ui_MeshMergerWidget(object):
    def setupUi(self, MeshMergerWidget):
        if not MeshMergerWidget.objectName():
            MeshMergerWidget.setObjectName(u"MeshMergerWidget")
        MeshMergerWidget.resize(809, 649)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MeshMergerWidget.sizePolicy().hasHeightForWidth())
        MeshMergerWidget.setSizePolicy(sizePolicy)
        self.horizontalLayout = QHBoxLayout(MeshMergerWidget)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.dockWidget = QDockWidget(MeshMergerWidget)
        self.dockWidget.setObjectName(u"dockWidget")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(1)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.dockWidget.sizePolicy().hasHeightForWidth())
        self.dockWidget.setSizePolicy(sizePolicy1)
        self.dockWidget.setMinimumSize(QSize(353, 197))
        self.dockWidget.setFeatures(QDockWidget.DockWidgetFloatable|QDockWidget.DockWidgetMovable)
        self.dockWidget.setAllowedAreas(Qt.AllDockWidgetAreas)
        self.dockWidgetContents = QWidget()
        self.dockWidgetContents.setObjectName(u"dockWidgetContents")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.dockWidgetContents.sizePolicy().hasHeightForWidth())
        self.dockWidgetContents.setSizePolicy(sizePolicy2)
        self.verticalLayout = QVBoxLayout(self.dockWidgetContents)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.scrollArea = QScrollArea(self.dockWidgetContents)
        self.scrollArea.setObjectName(u"scrollArea")
        sizePolicy2.setHeightForWidth(self.scrollArea.sizePolicy().hasHeightForWidth())
        self.scrollArea.setSizePolicy(sizePolicy2)
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents_2 = QWidget()
        self.scrollAreaWidgetContents_2.setObjectName(u"scrollAreaWidgetContents_2")
        self.scrollAreaWidgetContents_2.setGeometry(QRect(0, 0, 365, 564))
        sizePolicy2.setHeightForWidth(self.scrollAreaWidgetContents_2.sizePolicy().hasHeightForWidth())
        self.scrollAreaWidgetContents_2.setSizePolicy(sizePolicy2)
        self.verticalLayout_2 = QVBoxLayout(self.scrollAreaWidgetContents_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.identifier_frame = QFrame(self.scrollAreaWidgetContents_2)
        self.identifier_frame.setObjectName(u"identifier_frame")
        self.identifier_frame.setMinimumSize(QSize(0, 0))
        self.identifier_frame.setFrameShape(QFrame.StyledPanel)
        self.identifier_frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_5 = QVBoxLayout(self.identifier_frame)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(-1, 5, -1, 3)
        self.identifier_label = QLabel(self.identifier_frame)
        self.identifier_label.setObjectName(u"identifier_label")

        self.verticalLayout_5.addWidget(self.identifier_label)

        self.line = QFrame(self.identifier_frame)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_5.addWidget(self.line)


        self.verticalLayout_3.addWidget(self.identifier_frame)

        self.mergeNodes_frame = QFrame(self.scrollAreaWidgetContents_2)
        self.mergeNodes_frame.setObjectName(u"mergeNodes_frame")
        self.mergeNodes_frame.setFrameShape(QFrame.StyledPanel)
        self.mergeNodes_frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_4 = QVBoxLayout(self.mergeNodes_frame)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(-1, 3, -1, -1)
        self.mergeNodes_label = QLabel(self.mergeNodes_frame)
        self.mergeNodes_label.setObjectName(u"mergeNodes_label")

        self.verticalLayout_4.addWidget(self.mergeNodes_label)

        self.mergeNodesEntry_widget = QWidget(self.mergeNodes_frame)
        self.mergeNodesEntry_widget.setObjectName(u"mergeNodesEntry_widget")
        self.horizontalLayout_4 = QHBoxLayout(self.mergeNodesEntry_widget)
        self.horizontalLayout_4.setSpacing(3)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.mergeNodesEntry_lineEdit = QLineEdit(self.mergeNodesEntry_widget)
        self.mergeNodesEntry_lineEdit.setObjectName(u"mergeNodesEntry_lineEdit")

        self.horizontalLayout_4.addWidget(self.mergeNodesEntry_lineEdit)

        self.mergeNodesDelete_pushButton = QPushButton(self.mergeNodesEntry_widget)
        self.mergeNodesDelete_pushButton.setObjectName(u"mergeNodesDelete_pushButton")

        self.horizontalLayout_4.addWidget(self.mergeNodesDelete_pushButton)

        self.mergeNodesApply_pushButton = QPushButton(self.mergeNodesEntry_widget)
        self.mergeNodesApply_pushButton.setObjectName(u"mergeNodesApply_pushButton")

        self.horizontalLayout_4.addWidget(self.mergeNodesApply_pushButton)


        self.verticalLayout_4.addWidget(self.mergeNodesEntry_widget)

        self.mergeNodesList_plainTextEdit = QPlainTextEdit(self.mergeNodes_frame)
        self.mergeNodesList_plainTextEdit.setObjectName(u"mergeNodesList_plainTextEdit")
        self.mergeNodesList_plainTextEdit.setReadOnly(False)

        self.verticalLayout_4.addWidget(self.mergeNodesList_plainTextEdit)


        self.verticalLayout_3.addWidget(self.mergeNodes_frame)

        self.mergeOptions_groupBox = QGroupBox(self.scrollAreaWidgetContents_2)
        self.mergeOptions_groupBox.setObjectName(u"mergeOptions_groupBox")
        self.gridLayout = QGridLayout(self.mergeOptions_groupBox)
        self.gridLayout.setObjectName(u"gridLayout")
        self.previewMerge_checkBox = QCheckBox(self.mergeOptions_groupBox)
        self.previewMerge_checkBox.setObjectName(u"previewMerge_checkBox")

        self.gridLayout.addWidget(self.previewMerge_checkBox, 0, 0, 1, 1)

        self.fit_frame = QFrame(self.mergeOptions_groupBox)
        self.fit_frame.setObjectName(u"fit_frame")
        self.fit_frame.setFrameShape(QFrame.StyledPanel)
        self.fit_frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_6 = QHBoxLayout(self.fit_frame)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.fit_checkBox = QCheckBox(self.fit_frame)
        self.fit_checkBox.setObjectName(u"fit_checkBox")

        self.horizontalLayout_6.addWidget(self.fit_checkBox)

        self.previewFit_checkBox = QCheckBox(self.fit_frame)
        self.previewFit_checkBox.setObjectName(u"previewFit_checkBox")

        self.horizontalLayout_6.addWidget(self.previewFit_checkBox)


        self.gridLayout.addWidget(self.fit_frame, 1, 0, 1, 1)


        self.verticalLayout_3.addWidget(self.mergeOptions_groupBox)

        self.displayOptions_groupBox = QGroupBox(self.scrollAreaWidgetContents_2)
        self.displayOptions_groupBox.setObjectName(u"displayOptions_groupBox")
        sizePolicy.setHeightForWidth(self.displayOptions_groupBox.sizePolicy().hasHeightForWidth())
        self.displayOptions_groupBox.setSizePolicy(sizePolicy)
        self.verticalLayout_7 = QVBoxLayout(self.displayOptions_groupBox)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.displayAxes_checkBox = QCheckBox(self.displayOptions_groupBox)
        self.displayAxes_checkBox.setObjectName(u"displayAxes_checkBox")
        self.displayAxes_checkBox.setEnabled(True)

        self.verticalLayout_7.addWidget(self.displayAxes_checkBox)

        self.displayLines_checkBox = QCheckBox(self.displayOptions_groupBox)
        self.displayLines_checkBox.setObjectName(u"displayLines_checkBox")

        self.verticalLayout_7.addWidget(self.displayLines_checkBox)

        self.displaySurfaces_frame = QFrame(self.displayOptions_groupBox)
        self.displaySurfaces_frame.setObjectName(u"displaySurfaces_frame")
        self.displaySurfaces_frame.setFrameShape(QFrame.StyledPanel)
        self.displaySurfaces_frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_5 = QHBoxLayout(self.displaySurfaces_frame)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.displaySurfaces_checkBox = QCheckBox(self.displaySurfaces_frame)
        self.displaySurfaces_checkBox.setObjectName(u"displaySurfaces_checkBox")

        self.horizontalLayout_5.addWidget(self.displaySurfaces_checkBox)

        self.displaySurfacesExterior_checkBox = QCheckBox(self.displaySurfaces_frame)
        self.displaySurfacesExterior_checkBox.setObjectName(u"displaySurfacesExterior_checkBox")

        self.horizontalLayout_5.addWidget(self.displaySurfacesExterior_checkBox)

        self.displaySurfacesTranslucent_checkBox = QCheckBox(self.displaySurfaces_frame)
        self.displaySurfacesTranslucent_checkBox.setObjectName(u"displaySurfacesTranslucent_checkBox")

        self.horizontalLayout_5.addWidget(self.displaySurfacesTranslucent_checkBox)

        self.displaySurfacesWireframe_checkBox = QCheckBox(self.displaySurfaces_frame)
        self.displaySurfacesWireframe_checkBox.setObjectName(u"displaySurfacesWireframe_checkBox")

        self.horizontalLayout_5.addWidget(self.displaySurfacesWireframe_checkBox)


        self.verticalLayout_7.addWidget(self.displaySurfaces_frame)

        self.displayElementNumbers_checkBox = QCheckBox(self.displayOptions_groupBox)
        self.displayElementNumbers_checkBox.setObjectName(u"displayElementNumbers_checkBox")

        self.verticalLayout_7.addWidget(self.displayElementNumbers_checkBox)

        self.displayNodeNumbers_checkBox = QCheckBox(self.displayOptions_groupBox)
        self.displayNodeNumbers_checkBox.setObjectName(u"displayNodeNumbers_checkBox")

        self.verticalLayout_7.addWidget(self.displayNodeNumbers_checkBox)

        self.displayNodeDerivatives_checkBox = QCheckBox(self.displayOptions_groupBox)
        self.displayNodeDerivatives_checkBox.setObjectName(u"displayNodeDerivatives_checkBox")
        self.displayNodeDerivatives_checkBox.setEnabled(True)

        self.verticalLayout_7.addWidget(self.displayNodeDerivatives_checkBox)

        self.displayXiAxes_checkBox = QCheckBox(self.displayOptions_groupBox)
        self.displayXiAxes_checkBox.setObjectName(u"displayXiAxes_checkBox")
        self.displayXiAxes_checkBox.setEnabled(True)

        self.verticalLayout_7.addWidget(self.displayXiAxes_checkBox)


        self.verticalLayout_3.addWidget(self.displayOptions_groupBox)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer)


        self.verticalLayout_2.addLayout(self.verticalLayout_3)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents_2)

        self.verticalLayout.addWidget(self.scrollArea)

        self.frame = QFrame(self.dockWidgetContents)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.frame)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(3, 3, 3, 3)
        self.viewAll_button = QPushButton(self.frame)
        self.viewAll_button.setObjectName(u"viewAll_button")

        self.horizontalLayout_2.addWidget(self.viewAll_button)

        self.done_button = QPushButton(self.frame)
        self.done_button.setObjectName(u"done_button")
        sizePolicy3 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.done_button.sizePolicy().hasHeightForWidth())
        self.done_button.setSizePolicy(sizePolicy3)

        self.horizontalLayout_2.addWidget(self.done_button)


        self.verticalLayout.addWidget(self.frame)

        self.dockWidget.setWidget(self.dockWidgetContents)

        self.horizontalLayout.addWidget(self.dockWidget)

        self.sceneviewer_frame = QFrame(MeshMergerWidget)
        self.sceneviewer_frame.setObjectName(u"sceneviewer_frame")
        sizePolicy4 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy4.setHorizontalStretch(4)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.sceneviewer_frame.sizePolicy().hasHeightForWidth())
        self.sceneviewer_frame.setSizePolicy(sizePolicy4)
        self.sceneviewer_frame.setFrameShape(QFrame.NoFrame)
        self.sceneviewer_frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.sceneviewer_frame)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.splitter = QSplitter(self.sceneviewer_frame)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Horizontal)
        self.master_sceneviewerWidget = SceneviewerWidget(self.splitter)
        self.master_sceneviewerWidget.setObjectName(u"master_sceneviewerWidget")
        sizePolicy5 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.master_sceneviewerWidget.sizePolicy().hasHeightForWidth())
        self.master_sceneviewerWidget.setSizePolicy(sizePolicy5)
        self.splitter.addWidget(self.master_sceneviewerWidget)
        self.slave_sceneviewerWidget = SceneviewerWidget(self.splitter)
        self.slave_sceneviewerWidget.setObjectName(u"slave_sceneviewerWidget")
        sizePolicy5.setHeightForWidth(self.slave_sceneviewerWidget.sizePolicy().hasHeightForWidth())
        self.slave_sceneviewerWidget.setSizePolicy(sizePolicy5)
        self.splitter.addWidget(self.slave_sceneviewerWidget)

        self.horizontalLayout_3.addWidget(self.splitter)


        self.horizontalLayout.addWidget(self.sceneviewer_frame)


        self.retranslateUi(MeshMergerWidget)

        QMetaObject.connectSlotsByName(MeshMergerWidget)
    # setupUi

    def retranslateUi(self, MeshMergerWidget):
        MeshMergerWidget.setWindowTitle(QCoreApplication.translate("MeshMergerWidget", u"Form", None))
        self.dockWidget.setWindowTitle(QCoreApplication.translate("MeshMergerWidget", u"Mesh Merger Controls", None))
        self.identifier_label.setText(QCoreApplication.translate("MeshMergerWidget", u"Identifier", None))
        self.mergeNodes_label.setText(QCoreApplication.translate("MeshMergerWidget", u"Merge nodes master=slave (e.g. 1=55):", None))
#if QT_CONFIG(tooltip)
        self.mergeNodesEntry_lineEdit.setToolTip(QCoreApplication.translate("MeshMergerWidget", u"<html><head/><body><p>Enter a master node, or master=slave pair.</p><p>Or hold down S-key and click nodes in the 3D view.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.mergeNodesDelete_pushButton.setToolTip(QCoreApplication.translate("MeshMergerWidget", u"<html><head/><body><p>Delete map for currently selected node</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.mergeNodesDelete_pushButton.setText(QCoreApplication.translate("MeshMergerWidget", u"Delete", None))
#if QT_CONFIG(tooltip)
        self.mergeNodesApply_pushButton.setToolTip(QCoreApplication.translate("MeshMergerWidget", u"<html><head/><body><p>Apply edits in merge nodes list text edit</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.mergeNodesApply_pushButton.setText(QCoreApplication.translate("MeshMergerWidget", u"Apply", None))
#if QT_CONFIG(tooltip)
        self.mergeNodesList_plainTextEdit.setToolTip(QCoreApplication.translate("MeshMergerWidget", u"<html><head/><body><p>List of master=slave nodes to merge.</p><p>After editing click 'Apply' to apply them.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.mergeOptions_groupBox.setTitle(QCoreApplication.translate("MeshMergerWidget", u"Merge options:", None))
        self.previewMerge_checkBox.setText(QCoreApplication.translate("MeshMergerWidget", u"Preview merge", None))
        self.fit_checkBox.setText(QCoreApplication.translate("MeshMergerWidget", u"Fit", None))
        self.previewFit_checkBox.setText(QCoreApplication.translate("MeshMergerWidget", u"Preview fit", None))
        self.displayOptions_groupBox.setTitle(QCoreApplication.translate("MeshMergerWidget", u"Display options:", None))
        self.displayAxes_checkBox.setText(QCoreApplication.translate("MeshMergerWidget", u"Axes", None))
        self.displayLines_checkBox.setText(QCoreApplication.translate("MeshMergerWidget", u"Lines", None))
        self.displaySurfaces_checkBox.setText(QCoreApplication.translate("MeshMergerWidget", u"Surfaces", None))
        self.displaySurfacesExterior_checkBox.setText(QCoreApplication.translate("MeshMergerWidget", u"Exterior", None))
        self.displaySurfacesTranslucent_checkBox.setText(QCoreApplication.translate("MeshMergerWidget", u"Transluc.", None))
        self.displaySurfacesWireframe_checkBox.setText(QCoreApplication.translate("MeshMergerWidget", u"Wireframe", None))
        self.displayElementNumbers_checkBox.setText(QCoreApplication.translate("MeshMergerWidget", u"Element numbers", None))
        self.displayNodeNumbers_checkBox.setText(QCoreApplication.translate("MeshMergerWidget", u"Node numbers", None))
        self.displayNodeDerivatives_checkBox.setText(QCoreApplication.translate("MeshMergerWidget", u"Node derivatives", None))
        self.displayXiAxes_checkBox.setText(QCoreApplication.translate("MeshMergerWidget", u"Xi axes", None))
        self.viewAll_button.setText(QCoreApplication.translate("MeshMergerWidget", u"View All", None))
        self.done_button.setText(QCoreApplication.translate("MeshMergerWidget", u"Done", None))
    # retranslateUi

