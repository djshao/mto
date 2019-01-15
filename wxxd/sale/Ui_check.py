# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\Users\Administrator\erp\wxxd\sale\check.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Quote_check(object):
    def setupUi(self, Quote_check):
        Quote_check.setObjectName("Quote_check")
        Quote_check.resize(1024, 768)
        Quote_check.setToolTip("")
        self.gridLayout = QtWidgets.QGridLayout(Quote_check)
        self.gridLayout.setObjectName("gridLayout")
        self.Box_filter = QtWidgets.QComboBox(Quote_check)
        self.Box_filter.setMinimumSize(QtCore.QSize(0, 26))
        self.Box_filter.setCurrentText("")
        self.Box_filter.setObjectName("Box_filter")
        self.gridLayout.addWidget(self.Box_filter, 0, 0, 1, 1)
        self.Button_edit = QtWidgets.QPushButton(Quote_check)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/myImage/images/Accept.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Button_edit.setIcon(icon)
        self.Button_edit.setObjectName("Button_edit")
        self.gridLayout.addWidget(self.Button_edit, 0, 1, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(806, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 2, 1, 1)
        self.tblwgt_quote = QtWidgets.QTableWidget(Quote_check)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tblwgt_quote.sizePolicy().hasHeightForWidth())
        self.tblwgt_quote.setSizePolicy(sizePolicy)
        self.tblwgt_quote.setObjectName("tblwgt_quote")
        self.tblwgt_quote.setColumnCount(0)
        self.tblwgt_quote.setRowCount(0)
        self.tblwgt_quote.horizontalHeader().setStretchLastSection(True)
        self.tblwgt_quote.verticalHeader().setStretchLastSection(False)
        self.gridLayout.addWidget(self.tblwgt_quote, 1, 0, 1, 3)

        self.retranslateUi(Quote_check)
        QtCore.QMetaObject.connectSlotsByName(Quote_check)

    def retranslateUi(self, Quote_check):
        _translate = QtCore.QCoreApplication.translate
        Quote_check.setWindowTitle(_translate("Quote_check", "报价审核"))
        self.Box_filter.setToolTip(_translate("Quote_check", "审核情况"))
        self.Button_edit.setToolTip(_translate("Quote_check", "审核"))
        self.Button_edit.setText(_translate("Quote_check", "审核"))
        self.tblwgt_quote.setToolTip(_translate("Quote_check", "报价清单"))

import myImage_rc
