# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\Users\Administrator\Desktop\Python\ERP\首页.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_First_Form(object):
    def setupUi(self, First_Form):
        First_Form.setObjectName("First_Form")
        First_Form.resize(1024, 768)
        self.gridLayout = QtWidgets.QGridLayout(First_Form)
        self.gridLayout.setObjectName("gridLayout")
        self.tableWidget = QtWidgets.QTableWidget(First_Form)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.gridLayout.addWidget(self.tableWidget, 2, 0, 1, 3)
        self.label_2 = QtWidgets.QLabel(First_Form)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 3, 0, 1, 1)
        self.label = QtWidgets.QLabel(First_Form)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(669, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 1, 1, 1)
        self.lineEdit = QtWidgets.QLineEdit(First_Form)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout.addWidget(self.lineEdit, 1, 0, 1, 2)
        self.lineEdit_2 = QtWidgets.QLineEdit(First_Form)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.gridLayout.addWidget(self.lineEdit_2, 4, 0, 1, 2)
        spacerItem1 = QtWidgets.QSpacerItem(932, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 3, 1, 1, 2)
        self.tableWidget_2 = QtWidgets.QTableWidget(First_Form)
        self.tableWidget_2.setObjectName("tableWidget_2")
        self.tableWidget_2.setColumnCount(0)
        self.tableWidget_2.setRowCount(0)
        self.gridLayout.addWidget(self.tableWidget_2, 5, 0, 1, 3)
        self.textWeather = QtWidgets.QTextEdit(First_Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textWeather.sizePolicy().hasHeightForWidth())
        self.textWeather.setSizePolicy(sizePolicy)
        self.textWeather.setMinimumSize(QtCore.QSize(256, 150))
        self.textWeather.setObjectName("textWeather")
        self.gridLayout.addWidget(self.textWeather, 0, 2, 2, 1)

        self.retranslateUi(First_Form)
        QtCore.QMetaObject.connectSlotsByName(First_Form)

    def retranslateUi(self, First_Form):
        _translate = QtCore.QCoreApplication.translate
        First_Form.setWindowTitle(_translate("First_Form", "Form"))
        self.label_2.setText(_translate("First_Form", "消息栏"))
        self.label.setText(_translate("First_Form", "待办事项"))
        self.lineEdit.setText(_translate("First_Form", "你有2条待办事项"))
        self.lineEdit_2.setText(_translate("First_Form", "你有1条消息未读"))
        self.textWeather.setHtml(_translate("First_Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimSun\'; font-size:9.07563pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:9.07563pt;\">天气</span></p></body></html>"))

