# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\Users\Administrator\Desktop\Python\ERP\sell\offer.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_offer_Form(object):
    def setupUi(self, offer_Form):
        offer_Form.setObjectName("offer_Form")
        offer_Form.resize(653, 500)
        self.pushButton = QtWidgets.QPushButton(offer_Form)
        self.pushButton.setGeometry(QtCore.QRect(680, 60, 75, 23))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(offer_Form)
        self.pushButton_2.setGeometry(QtCore.QRect(680, 170, 75, 23))
        self.pushButton_2.setObjectName("pushButton_2")
        self.offerwidget = DataTableWidget(offer_Form)
        self.offerwidget.setGeometry(QtCore.QRect(50, 30, 491, 391))
        self.offerwidget.setObjectName("offerwidget")

        self.retranslateUi(offer_Form)
        QtCore.QMetaObject.connectSlotsByName(offer_Form)

    def retranslateUi(self, offer_Form):
        _translate = QtCore.QCoreApplication.translate
        offer_Form.setWindowTitle(_translate("offer_Form", "Form"))
        self.pushButton.setText(_translate("MainWindow", "数据初始化"))
        self.pushButton_2.setText(_translate("MainWindow", "保存数据"))

from qtpandas.views.DataTableView import DataTableWidget
