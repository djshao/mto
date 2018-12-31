# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\Users\Administrator\Desktop\Python\ERP\sell\quote_check.ui'
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
        self.verticalLayout = QtWidgets.QVBoxLayout(Quote_check)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.Button_pass = QtWidgets.QPushButton(Quote_check)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../images/Accept_24px.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Button_pass.setIcon(icon)
        self.Button_pass.setObjectName("Button_pass")
        self.horizontalLayout.addWidget(self.Button_pass)
        self.Button_nopass = QtWidgets.QPushButton(Quote_check)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("../images/stop_32px.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Button_nopass.setIcon(icon1)
        self.Button_nopass.setObjectName("Button_nopass")
        self.horizontalLayout.addWidget(self.Button_nopass)
        self.Button_edit = QtWidgets.QPushButton(Quote_check)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("../images/modify_24px.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Button_edit.setIcon(icon2)
        self.Button_edit.setObjectName("Button_edit")
        self.horizontalLayout.addWidget(self.Button_edit)
        self.Box_group = QtWidgets.QComboBox(Quote_check)
        self.Box_group.setObjectName("Box_group")
        self.horizontalLayout.addWidget(self.Box_group)
        self.Box_filter = QtWidgets.QComboBox(Quote_check)
        self.Box_filter.setCurrentText("")
        self.Box_filter.setObjectName("Box_filter")
        self.horizontalLayout.addWidget(self.Box_filter)
        self.Button_query = QtWidgets.QPushButton(Quote_check)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("../images/find_24px_28620.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Button_query.setIcon(icon3)
        self.Button_query.setObjectName("Button_query")
        self.horizontalLayout.addWidget(self.Button_query)
        self.Line_search = QtWidgets.QLineEdit(Quote_check)
        self.Line_search.setText("")
        self.Line_search.setClearButtonEnabled(True)
        self.Line_search.setObjectName("Line_search")
        self.horizontalLayout.addWidget(self.Line_search)
        self.verticalLayout.addLayout(self.horizontalLayout)
        # self.Quote_list = QtWidgets.QTableWidget(Quote_check)
        # sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        # sizePolicy.setHorizontalStretch(0)
        # sizePolicy.setVerticalStretch(0)
        # sizePolicy.setHeightForWidth(self.Quote_list.sizePolicy().hasHeightForWidth())
        # self.Quote_list.setSizePolicy(sizePolicy)
        # self.Quote_list.setObjectName("Quote_list")
        # self.Quote_list.setColumnCount(0)
        # self.Quote_list.setRowCount(0)
        # self.Quote_list.horizontalHeader().setStretchLastSection(True)
        # self.Quote_list.verticalHeader().setStretchLastSection(False)
        # self.verticalLayout.addWidget(self.Quote_list)
        # self.Quote_detail = QtWidgets.QTableWidget(Quote_check)
        # sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        # sizePolicy.setHorizontalStretch(0)
        # sizePolicy.setVerticalStretch(0)
        # sizePolicy.setHeightForWidth(self.Quote_detail.sizePolicy().hasHeightForWidth())
        # self.Quote_detail.setSizePolicy(sizePolicy)
        # self.Quote_detail.setObjectName("Quote_detail")
        # self.Quote_detail.setColumnCount(0)
        # self.Quote_detail.setRowCount(0)
        # self.verticalLayout.addWidget(self.Quote_detail)
        # self.verticalLayout.setStretch(1, 1)
        # self.verticalLayout.setStretch(2, 2)

        self.retranslateUi(Quote_check)
        QtCore.QMetaObject.connectSlotsByName(Quote_check)

    def retranslateUi(self, Quote_check):
        _translate = QtCore.QCoreApplication.translate
        Quote_check.setWindowTitle(_translate("Quote_check", "报价审核"))
        self.Button_pass.setToolTip(_translate("Quote_check", "审核通过"))
        self.Button_pass.setText(_translate("Quote_check", "通过"))
        self.Button_nopass.setToolTip(_translate("Quote_check", "审核未通过"))
        self.Button_nopass.setText(_translate("Quote_check", "未通过"))
        self.Button_edit.setToolTip(_translate("Quote_check", "修改报价"))
        self.Button_edit.setText(_translate("Quote_check", "修改"))
        self.Box_group.setToolTip(_translate("Quote_check", "分组"))
        self.Box_filter.setToolTip(_translate("Quote_check", "筛选"))
        self.Button_query.setText(_translate("Quote_check", "查询"))
        self.Line_search.setToolTip(_translate("Quote_check", "搜索"))
        self.Line_search.setPlaceholderText(_translate("Quote_check", "搜索...."))
        # self.Quote_list.setToolTip(_translate("Quote_check", "报价清单"))
        # self.Quote_detail.setToolTip(_translate("Quote_check", "报价明细"))

