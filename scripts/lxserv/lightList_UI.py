# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'lightList.ui'
#
# Created: Tue Jan  7 20:39:47 2014
#      by: pyside-uic 0.2.13 running on PySide 1.1.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(295, 215)
        Form.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        Form.setStyleSheet("QWidget\n"
"{\n"
"  dialogbuttonbox-buttons-have-icons: 0;\n"
"  combobox-popup: 1;\n"
"  tabbar-prefer-no-arrows: true;\n"
"  color: #cccccc;\n"
"  background-color: #484848;\n"
"}\n"
"\n"
"")
        self.gridLayout = QtGui.QGridLayout(Form)
        self.gridLayout.setContentsMargins(4, 4, 4, 4)
        self.gridLayout.setVerticalSpacing(3)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setSpacing(8)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtGui.QLabel(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMinimumSize(QtCore.QSize(0, 18))
        self.label.setMaximumSize(QtCore.QSize(16777215, 16))
        font = QtGui.QFont()
        font.setFamily("Geometr415 Md BT")
        font.setPointSize(12)
        font.setWeight(50)
        font.setUnderline(False)
        font.setBold(False)
        self.label.setFont(font)
        self.label.setStyleSheet("QLabel{\n"
"background-color: none;\n"
"color: lightgray;\n"
"}")
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.line = QtGui.QFrame(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.line.sizePolicy().hasHeightForWidth())
        self.line.setSizePolicy(sizePolicy)
        self.line.setMinimumSize(QtCore.QSize(0, 2))
        self.line.setMaximumSize(QtCore.QSize(16777215, 2))
        self.line.setStyleSheet("border: none;\n"
"background-color: rgb(54, 54, 54);")
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName("line")
        self.horizontalLayout.addWidget(self.line)
        self.aboutButton = QtGui.QPushButton(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.aboutButton.sizePolicy().hasHeightForWidth())
        self.aboutButton.setSizePolicy(sizePolicy)
        self.aboutButton.setMinimumSize(QtCore.QSize(16, 16))
        self.aboutButton.setMaximumSize(QtCore.QSize(16, 16))
        self.aboutButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.aboutButton.setStyleSheet("QPushButton\n"
"{\n"
"  icon-size: 12px;\n"
"  background-color: #606060;\n"
"  border-width: 1px;\n"
"  border-color: #353535;\n"
"  border-style: solid;\n"
"  border-radius: 6px;\n"
"  padding: 1px;\n"
"  padding-left: 1px;\n"
"  padding-right: 1px;\n"
"}\n"
"\n"
"QPushButton:pressed\n"
"{\n"
"  icon-size: 12px;\n"
"  background-color: #f49c1c;\n"
"  color: black;\n"
"  border-width: 1px;\n"
"  border-color: #353535;\n"
"  border-style: solid;\n"
"  border-radius: 6px;\n"
"  padding: 1px;\n"
"  padding-left: 1px;\n"
"  padding-right: 1px;\n"
"}")
        self.aboutButton.setObjectName("aboutButton")
        self.horizontalLayout.addWidget(self.aboutButton)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 10, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.gridLayout.addItem(spacerItem, 1, 0, 1, 1)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.giCheckBox = QtGui.QCheckBox(Form)
        self.giCheckBox.setMinimumSize(QtCore.QSize(0, 0))
        self.giCheckBox.setMaximumSize(QtCore.QSize(2000, 16))
        self.giCheckBox.setStyleSheet("")
        self.giCheckBox.setChecked(True)
        self.giCheckBox.setObjectName("giCheckBox")
        self.horizontalLayout_2.addWidget(self.giCheckBox)
        spacerItem1 = QtGui.QSpacerItem(348, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.refreshButton = QtGui.QPushButton(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.refreshButton.sizePolicy().hasHeightForWidth())
        self.refreshButton.setSizePolicy(sizePolicy)
        self.refreshButton.setMinimumSize(QtCore.QSize(20, 20))
        self.refreshButton.setMaximumSize(QtCore.QSize(20, 20))
        self.refreshButton.setStyleSheet("QPushButton{\n"
"background: none;\n"
"border: none;\n"
"}\n"
"\n"
"QPushButton:pressed{\n"
"border: 1px solid #5C5C5C;\n"
"\n"
"}")
        self.refreshButton.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icons/refresh.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.refreshButton.setIcon(icon)
        self.refreshButton.setIconSize(QtCore.QSize(16, 16))
        self.refreshButton.setObjectName("refreshButton")
        self.horizontalLayout_2.addWidget(self.refreshButton)
        self.gridLayout.addLayout(self.horizontalLayout_2, 2, 0, 1, 1)
        self.lightList = QtGui.QListWidget(Form)
        self.lightList.setFocusPolicy(QtCore.Qt.NoFocus)
        self.lightList.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.lightList.setStyleSheet("QListView {\n"
"  color: #000000;\n"
"  background-color: #949ca4;\n"
"  alternate-background-color: #9098a0;\n"
"\n"
"  border-radius: 4px;\n"
"  border-style: solid;\n"
"  border-width: 1px;\n"
"  border-color: #282828;\n"
"}")
        self.lightList.setAutoScroll(False)
        self.lightList.setDragEnabled(True)
        self.lightList.setDragDropMode(QtGui.QAbstractItemView.InternalMove)
        self.lightList.setObjectName("lightList")
        self.gridLayout.addWidget(self.lightList, 3, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Form", "LightBank", None, QtGui.QApplication.UnicodeUTF8))
        self.aboutButton.setText(QtGui.QApplication.translate("Form", "?", None, QtGui.QApplication.UnicodeUTF8))
        self.giCheckBox.setText(QtGui.QApplication.translate("Form", "Global Illumination", None, QtGui.QApplication.UnicodeUTF8))

