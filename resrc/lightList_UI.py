# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'lightList.ui'
#
# Created: Sat Jul 26 16:18:50 2014
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
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.giCheckBox = QtGui.QCheckBox(Form)
        self.giCheckBox.setMinimumSize(QtCore.QSize(0, 0))
        self.giCheckBox.setMaximumSize(QtCore.QSize(2000, 16))
        self.giCheckBox.setStyleSheet("")
        self.giCheckBox.setChecked(True)
        self.giCheckBox.setObjectName("giCheckBox")
        self.horizontalLayout_2.addWidget(self.giCheckBox)
        spacerItem = QtGui.QSpacerItem(348, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.gridLayout.addLayout(self.horizontalLayout_2, 0, 0, 1, 1)
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
        self.lightList.setDragEnabled(False)
        self.lightList.setDragDropMode(QtGui.QAbstractItemView.NoDragDrop)
        self.lightList.setObjectName("lightList")
        self.gridLayout.addWidget(self.lightList, 1, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.giCheckBox.setText(QtGui.QApplication.translate("Form", "Global Illumination", None, QtGui.QApplication.UnicodeUTF8))

