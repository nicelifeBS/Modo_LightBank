# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'lightPanel.ui'
#
# Created: Wed Jul 30 11:05:16 2014
#      by: pyside-uic 0.2.13 running on PySide 1.1.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(487, 117)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        Form.setStyleSheet("QWidget\n"
"{\n"
"  dialogbuttonbox-buttons-have-icons: 0;\n"
"  combobox-popup: 1;\n"
"  tabbar-prefer-no-arrows: true;\n"
"  color: #cccccc;\n"
"  background-color: #484848;\n"
"}\n"
"\n"
"\n"
"\n"
"\n"
"\n"
"\n"
"\n"
"\n"
"\n"
"\n"
"")
        self.gridLayout_3 = QtGui.QGridLayout(Form)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setVerticalSpacing(2)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.groupBox = QtGui.QGroupBox(Form)
        self.groupBox.setStyleSheet("QGroupBox{\n"
"background-color: #484848;\n"
"border: none;\n"
"}\n"
"\n"
"QSpinBox, QDoubleSpinBox\n"
"{\n"
"  spinbox-click-autorepeat-rate: 100000;\n"
"  background-color: #9098a0;\n"
"  color: #000000;\n"
"  padding: 1px;\n"
"  padding-right: 12px;\n"
"  border-style: solid;\n"
"  border: 1px solid #353535;\n"
"  border-radius: 6px;\n"
"}\n"
"\n"
"QSpinBox:disabled, QDoubleSpinBox:disabled\n"
"{\n"
"  background-color: #414141;\n"
"  color: #666666;\n"
"}\n"
"\n"
"QSpinBox::up-button, QDoubleSpinBox::up-button {\n"
"  subcontrol-origin: border;\n"
"  subcontrol-position: center right;\n"
"\n"
"  height: 18px;\n"
"  width: 6px;\n"
"  left: -3px;\n"
"  border-width: 0px;\n"
"}\n"
"\n"
"QSpinBox::down-button, QDoubleSpinBox::down-button {\n"
"  subcontrol-origin: border;\n"
"  subcontrol-position: center right;\n"
"\n"
"  height: 18px;\n"
"  width: 6px;\n"
"  left: -9px;\n"
"  border-width: 0px;\n"
"  border-left: 1px solid #6c7176;\n"
"}\n"
"\n"
"QSpinBox::up-arrow, QDoubleSpinBox::up-arrow {\n"
"  image: url(SpinBoxRightArrow.png) 1;\n"
"  width: 6px;\n"
"  height: 9px;\n"
"}\n"
"\n"
"QSpinBox::down-arrow, QDoubleSpinBox::down-arrow {\n"
"  image: url(SpinBoxLeftArrow.png) 1;\n"
"  width: 4px;\n"
"  height: 7px;\n"
"}\n"
"")
        self.groupBox.setTitle("")
        self.groupBox.setCheckable(False)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_2 = QtGui.QGridLayout(self.groupBox)
        self.gridLayout_2.setContentsMargins(3, 3, 3, 12)
        self.gridLayout_2.setVerticalSpacing(3)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.optionsWidget = QtGui.QWidget(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.optionsWidget.sizePolicy().hasHeightForWidth())
        self.optionsWidget.setSizePolicy(sizePolicy)
        self.optionsWidget.setStyleSheet("")
        self.optionsWidget.setObjectName("optionsWidget")
        self.gridLayout = QtGui.QGridLayout(self.optionsWidget)
        self.gridLayout.setContentsMargins(3, 4, 4, 4)
        self.gridLayout.setHorizontalSpacing(5)
        self.gridLayout.setVerticalSpacing(3)
        self.gridLayout.setObjectName("gridLayout")
        self.diffuseSlider = QtGui.QSlider(self.optionsWidget)
        self.diffuseSlider.setFocusPolicy(QtCore.Qt.NoFocus)
        self.diffuseSlider.setStyleSheet("background: none;")
        self.diffuseSlider.setMaximum(1000)
        self.diffuseSlider.setProperty("value", 0)
        self.diffuseSlider.setOrientation(QtCore.Qt.Horizontal)
        self.diffuseSlider.setObjectName("diffuseSlider")
        self.gridLayout.addWidget(self.diffuseSlider, 0, 1, 1, 1)
        self.specularSlider = QtGui.QSlider(self.optionsWidget)
        self.specularSlider.setFocusPolicy(QtCore.Qt.NoFocus)
        self.specularSlider.setStyleSheet("background: none;")
        self.specularSlider.setMaximum(1000)
        self.specularSlider.setProperty("value", 0)
        self.specularSlider.setOrientation(QtCore.Qt.Horizontal)
        self.specularSlider.setObjectName("specularSlider")
        self.gridLayout.addWidget(self.specularSlider, 1, 1, 1, 1)
        self.specularLabel = QtGui.QLabel(self.optionsWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.specularLabel.sizePolicy().hasHeightForWidth())
        self.specularLabel.setSizePolicy(sizePolicy)
        self.specularLabel.setMinimumSize(QtCore.QSize(137, 0))
        self.specularLabel.setMaximumSize(QtCore.QSize(137, 16777215))
        self.specularLabel.setStyleSheet("background: none;")
        self.specularLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.specularLabel.setObjectName("specularLabel")
        self.gridLayout.addWidget(self.specularLabel, 1, 0, 1, 1)
        self.diffuseLabel = QtGui.QLabel(self.optionsWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.diffuseLabel.sizePolicy().hasHeightForWidth())
        self.diffuseLabel.setSizePolicy(sizePolicy)
        self.diffuseLabel.setMinimumSize(QtCore.QSize(137, 0))
        self.diffuseLabel.setMaximumSize(QtCore.QSize(137, 16777215))
        self.diffuseLabel.setStyleSheet("background: none;")
        self.diffuseLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.diffuseLabel.setObjectName("diffuseLabel")
        self.gridLayout.addWidget(self.diffuseLabel, 0, 0, 1, 1)
        self.specularSpinBox = QtGui.QDoubleSpinBox(self.optionsWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.specularSpinBox.sizePolicy().hasHeightForWidth())
        self.specularSpinBox.setSizePolicy(sizePolicy)
        self.specularSpinBox.setMinimumSize(QtCore.QSize(80, 0))
        self.specularSpinBox.setMaximumSize(QtCore.QSize(80, 16777215))
        self.specularSpinBox.setMaximum(1000.0)
        self.specularSpinBox.setObjectName("specularSpinBox")
        self.gridLayout.addWidget(self.specularSpinBox, 1, 2, 1, 1)
        self.diffuseSpinBox = QtGui.QDoubleSpinBox(self.optionsWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.diffuseSpinBox.sizePolicy().hasHeightForWidth())
        self.diffuseSpinBox.setSizePolicy(sizePolicy)
        self.diffuseSpinBox.setMinimumSize(QtCore.QSize(80, 0))
        self.diffuseSpinBox.setMaximumSize(QtCore.QSize(80, 16777215))
        self.diffuseSpinBox.setMaximum(1000.0)
        self.diffuseSpinBox.setObjectName("diffuseSpinBox")
        self.gridLayout.addWidget(self.diffuseSpinBox, 0, 2, 1, 1)
        self.gridLayout_2.addWidget(self.optionsWidget, 2, 0, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setSpacing(5)
        self.horizontalLayout.setContentsMargins(5, -1, 4, -1)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.optionsCheckbox = QtGui.QCheckBox(self.groupBox)
        self.optionsCheckbox.setText("")
        self.optionsCheckbox.setObjectName("optionsCheckbox")
        self.horizontalLayout.addWidget(self.optionsCheckbox)
        self.lightEnabledCheckbox = QtGui.QCheckBox(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lightEnabledCheckbox.sizePolicy().hasHeightForWidth())
        self.lightEnabledCheckbox.setSizePolicy(sizePolicy)
        self.lightEnabledCheckbox.setMinimumSize(QtCore.QSize(16, 0))
        self.lightEnabledCheckbox.setMaximumSize(QtCore.QSize(16, 16777215))
        self.lightEnabledCheckbox.setFocusPolicy(QtCore.Qt.NoFocus)
        self.lightEnabledCheckbox.setText("")
        self.lightEnabledCheckbox.setChecked(True)
        self.lightEnabledCheckbox.setTristate(False)
        self.lightEnabledCheckbox.setObjectName("lightEnabledCheckbox")
        self.horizontalLayout.addWidget(self.lightEnabledCheckbox)
        self.lightSoloButton = QtGui.QPushButton(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lightSoloButton.sizePolicy().hasHeightForWidth())
        self.lightSoloButton.setSizePolicy(sizePolicy)
        self.lightSoloButton.setMinimumSize(QtCore.QSize(18, 18))
        self.lightSoloButton.setMaximumSize(QtCore.QSize(18, 18))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(10)
        self.lightSoloButton.setFont(font)
        self.lightSoloButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.lightSoloButton.setStyleSheet("QPushButton\n"
"{\n"
"  icon-size: 12px;\n"
"  background-color: #606060;\n"
"  border-width: 1px;\n"
"  border-color: #353535;\n"
"  border-style: solid;\n"
"  border-radius: 6px;\n"
"  padding: 1px;\n"
"  padding-left: 12px;\n"
"  padding-right: 12px;\n"
"}\n"
"\n"
"\n"
"\n"
"QPushButton:checked\n"
"{\n"
"  icon-size: 12px;\n"
"  background-color: #f49c1c;\n"
"  color: black;\n"
"\n"
"}")
        self.lightSoloButton.setIconSize(QtCore.QSize(18, 18))
        self.lightSoloButton.setCheckable(True)
        self.lightSoloButton.setChecked(False)
        self.lightSoloButton.setObjectName("lightSoloButton")
        self.horizontalLayout.addWidget(self.lightSoloButton)
        self.colorPickButton = QtGui.QPushButton(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.colorPickButton.sizePolicy().hasHeightForWidth())
        self.colorPickButton.setSizePolicy(sizePolicy)
        self.colorPickButton.setMinimumSize(QtCore.QSize(18, 18))
        self.colorPickButton.setMaximumSize(QtCore.QSize(18, 18))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(10)
        self.colorPickButton.setFont(font)
        self.colorPickButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.colorPickButton.setStyleSheet("QPushButton\n"
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
"QPushButton:checked\n"
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
        self.colorPickButton.setText("")
        self.colorPickButton.setIconSize(QtCore.QSize(18, 18))
        self.colorPickButton.setCheckable(False)
        self.colorPickButton.setChecked(False)
        self.colorPickButton.setObjectName("colorPickButton")
        self.horizontalLayout.addWidget(self.colorPickButton)
        self.intensityLabel = QtGui.QLabel(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.intensityLabel.sizePolicy().hasHeightForWidth())
        self.intensityLabel.setSizePolicy(sizePolicy)
        self.intensityLabel.setMinimumSize(QtCore.QSize(50, 0))
        self.intensityLabel.setMaximumSize(QtCore.QSize(50, 16777215))
        self.intensityLabel.setStyleSheet("background: none;")
        self.intensityLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.intensityLabel.setObjectName("intensityLabel")
        self.horizontalLayout.addWidget(self.intensityLabel)
        self.intensitySlider = QtGui.QSlider(self.groupBox)
        self.intensitySlider.setFocusPolicy(QtCore.Qt.NoFocus)
        self.intensitySlider.setStyleSheet("background: none;")
        self.intensitySlider.setMaximum(100)
        self.intensitySlider.setProperty("value", 0)
        self.intensitySlider.setOrientation(QtCore.Qt.Horizontal)
        self.intensitySlider.setInvertedAppearance(False)
        self.intensitySlider.setInvertedControls(False)
        self.intensitySlider.setTickPosition(QtGui.QSlider.NoTicks)
        self.intensitySlider.setTickInterval(0)
        self.intensitySlider.setObjectName("intensitySlider")
        self.horizontalLayout.addWidget(self.intensitySlider)
        self.intensitySpinBox = QtGui.QDoubleSpinBox(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.intensitySpinBox.sizePolicy().hasHeightForWidth())
        self.intensitySpinBox.setSizePolicy(sizePolicy)
        self.intensitySpinBox.setMinimumSize(QtCore.QSize(80, 0))
        self.intensitySpinBox.setMaximumSize(QtCore.QSize(80, 16777215))
        self.intensitySpinBox.setMaximum(100000.0)
        self.intensitySpinBox.setObjectName("intensitySpinBox")
        self.horizontalLayout.addWidget(self.intensitySpinBox)
        self.gridLayout_2.addLayout(self.horizontalLayout, 1, 0, 1, 1)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.lightNameLineEdit = QtGui.QLineEdit(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lightNameLineEdit.sizePolicy().hasHeightForWidth())
        self.lightNameLineEdit.setSizePolicy(sizePolicy)
        self.lightNameLineEdit.setMinimumSize(QtCore.QSize(0, 20))
        self.lightNameLineEdit.setMaximumSize(QtCore.QSize(16777215, 20))
        self.lightNameLineEdit.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.lightNameLineEdit.setStyleSheet("QLineEdit{\n"
"background-color: #606060;\n"
"color: white;\n"
"border-top-left-radius: 3px;\n"
"border-top-right-radius: 0px;\n"
"border-bottom-right-radius: 0px;\n"
"border-bottom-left-radius: 0px;\n"
"border: none;\n"
"padding-left: 10px;\n"
"}")
        self.lightNameLineEdit.setInputMethodHints(QtCore.Qt.ImhNone)
        self.lightNameLineEdit.setReadOnly(False)
        self.lightNameLineEdit.setObjectName("lightNameLineEdit")
        self.horizontalLayout_2.addWidget(self.lightNameLineEdit)
        self.identContainer = QtGui.QLabel(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.identContainer.sizePolicy().hasHeightForWidth())
        self.identContainer.setSizePolicy(sizePolicy)
        self.identContainer.setMinimumSize(QtCore.QSize(0, 20))
        self.identContainer.setMaximumSize(QtCore.QSize(16777215, 20))
        font = QtGui.QFont()
        font.setPointSize(7)
        font.setItalic(True)
        self.identContainer.setFont(font)
        self.identContainer.setStyleSheet("QLabel{\n"
"background-color: #606060;\n"
"color: #606060;\n"
"border-radius: 0px;\n"
"padding-right: 10px;\n"
"}")
        self.identContainer.setObjectName("identContainer")
        self.horizontalLayout_2.addWidget(self.identContainer)
        self.rowContainer = QtGui.QLabel(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.rowContainer.sizePolicy().hasHeightForWidth())
        self.rowContainer.setSizePolicy(sizePolicy)
        self.rowContainer.setMinimumSize(QtCore.QSize(0, 20))
        self.rowContainer.setMaximumSize(QtCore.QSize(16777215, 20))
        font = QtGui.QFont()
        font.setPointSize(7)
        font.setItalic(True)
        self.rowContainer.setFont(font)
        self.rowContainer.setStyleSheet("QLabel{\n"
"background-color: #606060;\n"
"color: #606060;\n"
"border-radius: 0px;\n"
"padding-right: 10px;\n"
"}")
        self.rowContainer.setObjectName("rowContainer")
        self.horizontalLayout_2.addWidget(self.rowContainer)
        self.lightTypeLabel = QtGui.QLabel(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lightTypeLabel.sizePolicy().hasHeightForWidth())
        self.lightTypeLabel.setSizePolicy(sizePolicy)
        self.lightTypeLabel.setMinimumSize(QtCore.QSize(0, 20))
        self.lightTypeLabel.setMaximumSize(QtCore.QSize(16777215, 20))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(8)
        font.setItalic(True)
        self.lightTypeLabel.setFont(font)
        self.lightTypeLabel.setStyleSheet("QLabel{\n"
"background-color: #606060;\n"
"color: #B5B5B5;\n"
"border-top-right-radius:3px;\n"
"border-top-left-radius: 0px;\n"
"border-bottom-right-radius: 0px;\n"
"border-bottom-left-radius: 0px;\n"
"padding-right: 10px;\n"
"}")
        self.lightTypeLabel.setObjectName("lightTypeLabel")
        self.horizontalLayout_2.addWidget(self.lightTypeLabel)
        self.gridLayout_2.addLayout(self.horizontalLayout_2, 0, 0, 1, 1)
        self.gridLayout_3.addWidget(self.groupBox, 0, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.specularLabel.setText(QtGui.QApplication.translate("Form", "Affect Specular", None, QtGui.QApplication.UnicodeUTF8))
        self.diffuseLabel.setText(QtGui.QApplication.translate("Form", "Affect Diffuse", None, QtGui.QApplication.UnicodeUTF8))
        self.specularSpinBox.setSuffix(QtGui.QApplication.translate("Form", "%", None, QtGui.QApplication.UnicodeUTF8))
        self.diffuseSpinBox.setSuffix(QtGui.QApplication.translate("Form", "%", None, QtGui.QApplication.UnicodeUTF8))
        self.lightSoloButton.setText(QtGui.QApplication.translate("Form", "S", None, QtGui.QApplication.UnicodeUTF8))
        self.intensityLabel.setText(QtGui.QApplication.translate("Form", "Intensity", None, QtGui.QApplication.UnicodeUTF8))
        self.lightNameLineEdit.setText(QtGui.QApplication.translate("Form", "LightName", None, QtGui.QApplication.UnicodeUTF8))
        self.identContainer.setText(QtGui.QApplication.translate("Form", ".", None, QtGui.QApplication.UnicodeUTF8))
        self.rowContainer.setText(QtGui.QApplication.translate("Form", ".", None, QtGui.QApplication.UnicodeUTF8))
        self.lightTypeLabel.setText(QtGui.QApplication.translate("Form", "Directional", None, QtGui.QApplication.UnicodeUTF8))

