# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\Users\Administrator\erp\wxxd\tools\input.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_wgtInput(object):
    def setupUi(self, wgtInput):
        wgtInput.setObjectName("wgtInput")
        wgtInput.resize(1024, 768)
        self.gridLayout_2 = QtWidgets.QGridLayout(wgtInput)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.pbtnSave = QtWidgets.QPushButton(wgtInput)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/myImage/images/save.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pbtnSave.setIcon(icon)
        self.pbtnSave.setObjectName("pbtnSave")
        self.gridLayout_2.addWidget(self.pbtnSave, 0, 0, 1, 1)
        self.btn_query = QtWidgets.QPushButton(wgtInput)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/myImage/images/file_manager.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_query.setIcon(icon1)
        self.btn_query.setObjectName("btn_query")
        self.gridLayout_2.addWidget(self.btn_query, 0, 1, 1, 1)
        self.cmbWork = QtWidgets.QComboBox(wgtInput)
        self.cmbWork.setMinimumSize(QtCore.QSize(90, 26))
        self.cmbWork.setObjectName("cmbWork")
        self.cmbWork.addItem("")
        self.cmbWork.addItem("")
        self.cmbWork.addItem("")
        self.cmbWork.addItem("")
        self.gridLayout_2.addWidget(self.cmbWork, 0, 2, 1, 1)
        self.cmbDpmt = QtWidgets.QComboBox(wgtInput)
        self.cmbDpmt.setMinimumSize(QtCore.QSize(90, 26))
        self.cmbDpmt.setObjectName("cmbDpmt")
        self.gridLayout_2.addWidget(self.cmbDpmt, 0, 3, 1, 1)
        self.cmbNO = QtWidgets.QComboBox(wgtInput)
        self.cmbNO.setMinimumSize(QtCore.QSize(90, 26))
        self.cmbNO.setEditable(False)
        self.cmbNO.setCurrentText("")
        self.cmbNO.setObjectName("cmbNO")
        self.gridLayout_2.addWidget(self.cmbNO, 0, 4, 1, 1)
        self.comboBox_2 = QtWidgets.QComboBox(wgtInput)
        self.comboBox_2.setMinimumSize(QtCore.QSize(90, 26))
        self.comboBox_2.setObjectName("comboBox_2")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.gridLayout_2.addWidget(self.comboBox_2, 0, 5, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem, 0, 6, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(393, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem1, 0, 7, 1, 1)
        self.label = QtWidgets.QLabel(wgtInput)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(18)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 1, 0, 1, 8)
        self.frame = QtWidgets.QFrame(wgtInput)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout = QtWidgets.QGridLayout(self.frame)
        self.gridLayout.setObjectName("gridLayout")
        self.tblwgtInput = QtWidgets.QTableWidget(self.frame)
        self.tblwgtInput.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectItems)
        self.tblwgtInput.setObjectName("tblwgtInput")
        self.tblwgtInput.setColumnCount(0)
        self.tblwgtInput.setRowCount(0)
        self.tblwgtInput.verticalHeader().setVisible(False)
        self.gridLayout.addWidget(self.tblwgtInput, 0, 0, 1, 1)
        self.gridLayout_2.addWidget(self.frame, 2, 0, 1, 8)

        self.retranslateUi(wgtInput)
        QtCore.QMetaObject.connectSlotsByName(wgtInput)

    def retranslateUi(self, wgtInput):
        _translate = QtCore.QCoreApplication.translate
        wgtInput.setWindowTitle(_translate("wgtInput", "Form"))
        self.pbtnSave.setText(_translate("wgtInput", "保存"))
        self.btn_query.setText(_translate("wgtInput", "查询"))
        self.cmbWork.setCurrentText(_translate("wgtInput", "工艺环节"))
        self.cmbWork.setItemText(0, _translate("wgtInput", "工艺环节"))
        self.cmbWork.setItemText(1, _translate("wgtInput", "锻造"))
        self.cmbWork.setItemText(2, _translate("wgtInput", "机加"))
        self.cmbWork.setItemText(3, _translate("wgtInput", "终检"))
        self.cmbDpmt.setToolTip(_translate("wgtInput", "生产部门"))
        self.comboBox_2.setItemText(0, _translate("wgtInput", "生产状态"))
        self.comboBox_2.setItemText(1, _translate("wgtInput", "全部完成"))
        self.comboBox_2.setItemText(2, _translate("wgtInput", "部分完成"))
        self.label.setText(_translate("wgtInput", "锻 造 进 度 录 入"))

import myImage_rc
