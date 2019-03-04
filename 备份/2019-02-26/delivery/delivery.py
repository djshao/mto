# -*- coding: utf-8 -*-
"""
发货功能模块
"""
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QColor, QBrush, QPixmap, QIcon, QFont
from PyQt5.QtCore import pyqtSignal, QObject, Qt, pyqtSlot, QDate, QDateTime
from PyQt5.QtWidgets import *

import pymysql
import time

from ui.Ui_input import Ui_wgtInput
from ui.Ui_delivery import Ui_Form
from tools.mysql_conn import myMdb
from tools.tools import *


class DeliveryList(QWidget, Ui_Form):
    """送货清单类"""
    def __init__(self, parent=None):
        super(DeliveryList, self).__init__(parent)
        self.setupUi(self)
        self.inittableWidget()

        # 信号槽
        # self.btn_query.clicked.connect(self.btn_query_clicked)
        # self.tablewidget.itemClicked.connect(self.tablewidget_itemClicked)  # 点击清单,显示选择的明细
        # 下拉列表框选择事件连接
        # 开启单元格变更信号
        self.tableWidget.cellChanged.connect(self.input_cellChanged)

    def inittableWidget(self):
        """初始化tablewidget"""
        # 设置行表头字体
        font = QtGui.QFont('微软雅黑', 9)
        self.tableWidget.horizontalHeader().setFont(font)
        # 左垂直表头不显示
        self.tableWidget.verticalHeader().setVisible(False)
        # 只能选择单行
        self.tableWidget.setSelectionMode(QAbstractItemView.SingleSelection)
        # 设置表格颜色             
        self.tableWidget.horizontalHeader().setStyleSheet('QHeaderView::section{background:skyblue}')
        self.tableWidget.setFrameStyle(QtWidgets.QFrame.Box | QtWidgets.QFrame.Plain)
        # 设置文本框无边框
        styleSheet = "background:transparent;border-width:0;border-style:outset"
        for i in range(1, 8):
            exec("self.lineEdit_{}.setStyleSheet(styleSheet)".format(i))
        # 设置当前日期
        self.dateEdit.setDate(QDate.currentDate())

    def writeParam(self, param):
        """写入查询数据"""
        self.tableWidget.blockSignals(True)  # 暂停单元格修改信号
        # if param[0][13] == '清点装箱':
        #     self.label.setText("修改送货清单")
        #     self.label.setStyleSheet("color:#ff6600;")
        row = len(param)  # 获得查询窗口选择数据的行数
        # 找出送货地址,联系方式
        mymdb = myMdb()
        res, cur = mymdb.fetchall(field='{}'.format('交货地点,联系方式'),
                                  table='{}'.format('orders'),
                                  where="生产编号='{}'".format(param[0][2]))
        # 设置标题
        tbl_header = [
            '序号', '名称', '制造标准', '规格型号', '材质', '订单数量',
            '工作令号', '件号', '已发货数', '质保书', '发货数量'
        ]
        col = len(tbl_header)
        self.tableWidget.setRowCount(row)
        self.tableWidget.setColumnCount(col)
        self.tableWidget.setHorizontalHeaderLabels(tbl_header)
        self.lineEdit_1.setText(param[0][0])
        self.lineEdit_2.setText(str(res[0][0]))
        self.lineEdit_3.setText(str(res[0][1]))
        self.lineEdit_4.setText(param[0][2])
        # 一生产编号有多合同号的情况,考虑用筛选法选出合同号加到cmb,再选择显示同一合同号
        self.lineEdit_5.setText(param[0][1])
        for i in range(row):
            # 取第4列到第12列
            for j in range(3, 13):
                temp_data = param[i][j]
                if temp_data == 'None':
                    temp_data = 0
                data_1 = QTableWidgetItem(str(temp_data))
                # j=12质保书列可编辑
                if j != 12:
                    data_1.setFlags(QtCore.Qt.ItemIsEnabled)  # 禁止指定列编辑
                self.tableWidget.setItem(i, j-3, data_1)
            # 把送货单明细第11列None状态设为空值
            self.tableWidget.setItem(i, 10, QTableWidgetItem(''))
        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.blockSignals(False)  # 启动单元格修改信号

    def input_cellChanged(self, row, col):
        """输入完成数量后计算判断数量是否正确
            判断发货状态"""
        if col == 10:
            if self.tableWidget.item(row, col).text() == '':  # 发货数=空时退出
                self.tableWidget.setItem(row, 10, QTableWidgetItem(''))
                return

            self.tableWidget.blockSignals(True)  # 暂停单元格修改信号
            m_order = int(self.tableWidget.item(row, 5).text())  # 订单数量
            if self.tableWidget.item(row, 8).text() == 'None':  # 已完成数'None'时设为0
                m_cmpt = 0
            else:
                m_cmpt = int(self.tableWidget.item(row, 8).text())  # 已完成数

            m_cmp = int(self.tableWidget.item(row, 10).text())  # 发货数量
            m_all = m_cmpt + m_cmp  # 完成总数
            # if m_all > m_order or m_cmp < 0:
            #     QMessageBox.warning(self, "警告", "发货数量错误,请检查!")
            #     self.tableWidget.setItem(row, col, QTableWidgetItem(0))
            #     # self.tableWidget.setItem(row, 10, QTableWidgetItem(''))
            #     self.tableWidget.blockSignals(False)  # 开启单元格修改信号
            #     return

            self.tableWidget.item(row, col).setForeground(QBrush(QColor(255, 0, 0)))
            # 汇总发货数量
            count = plusColumn(self, "tableWidget", 10)
            self.lineEdit_6.setText(str(count))
            # 更新发货状态
            # if m_all == m_order:
            #     forge_state = '发货完成'
            # if m_all < m_order:
            #     forge_state = '部分发货'
            # m_st = QTableWidgetItem(forge_state)
            # m_st.setFlags(QtCore.Qt.ItemIsEnabled)
            # self.tableWidget.setItem(row, 12, m_st)
            self.tableWidget.blockSignals(False)  # 开启单元格修改信号

    def saveData(self):
        """保存发货清单"""
        rows = self.tableWidget.rowCount()  # 总行数
        cols = self.tableWidget.columnCount()  # 总列数
        for row in range(rows):
            if not self.tableWidget.item(row, 10) or self.tableWidget.item(row, 10).text() == '':
                m_xh = self.tableWidget.item(row, 0).text()
                QMessageBox.warning(self, "警告", "序号{}发货数量不能空".format(m_xh))
                return

        if self.lineEdit_2 == '' or self.lineEdit_3 == '':
            QMessageBox.about(self, "警告", "发货地址/联系方式不能空")
            return
        button = QMessageBox.question(self, "注意", "请确认无误再保存发货清单,\n按OK继续,按Cancel退出",
                                      QMessageBox.Ok|QMessageBox.Cancel, QMessageBox.Ok)
        if button == QMessageBox.Cancel:
            return

        m_no = self.lineEdit_5.text()  # 生产编号
        mymdb = myMdb()
        # 建更新订单明细的发货清单明细sql
        field_list = '生产编号,序号,质保书,已发货数,发货日期,发货状态'
        preSql_list = "insert into order_list ({})".format(field_list)
        subSql_list = " values(%s, %s, %s, %s, %s, %s)"
        sql_list_on = " ON DUPLICATE KEY UPDATE 质保书=VALUES(质保书),已发货数=VALUES(已发货数),发货日期=VALUES(发货日期),发货状态=VALUES(发货状态)"
        sql_list = preSql_list+subSql_list+sql_list_on

        # 建发货记录的sql  考虑移到选择物流后再保存?????
        fields = '收货单位,收货地址,联系方式,生产编号,合同编号,序号,质保书,发货数量,发货日期'
        preSql = "insert into 发货记录 ({}) ".format(fields)
        subSql = " values(%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        sql = preSql + subSql

        # 建更新订单明细用列表
        param_list = []  # 建传入值的列表
        param = []
        for row in range(rows):
            value_list = []
            value_list.append(self.lineEdit_5.text())  # 生产编号
            m_fhsl = self.tableWidget.item(row, 10).text()  # 发货数量
            m_yfhs = self.tableWidget.item(row, 8).text()  # 已发货数
            for col in (0, 9, 10):
                if col == 10:
                    value_list.append(int(m_fhsl)+int(m_yfhs))
                else:
                    value_list.append(self.tableWidget.item(row, col).text())
            value_list.append(self.dateEdit.date().toString("yyyy-MM-dd"))  # 发货日期
            value_list.append('清点装箱')  # 发货状态
            param_list.append(value_list)

            # 循环执行静态字符串方式把文本框内容加入发货记录value列表
            value = []
            for i in range(1, 6):
                exec("value.append(self.lineEdit_{}.text())".format(i))
            for col in (0, 9, 10):
                value.append(self.tableWidget.item(row, col).text())
            value.append(self.dateEdit.date().toString("yyyy-MM-dd"))
            param.append(value)
        # 数据库操作==============================================================
        # 更新order_list发货情况  存在双倍数量,怀疑是ON DUPLICATE KEY UPDATE引起??????
        rowcount = mymdb.insert_many(sql_list, param_list)
        # 发货汇总数据写入发货记录
        mymdb.insert_many(sql, param)
        QMessageBox.about(self, "保存成功", "保存了"+str(int(rowcount/2))+"条发货记录")
        self.clearDeliveryData()

    def printDelivery(self):
        """打印发货清单"""

    def clearDeliveryData(self):
        """清除发货清单窗口数据"""
        # try:
            # 关闭单元格变化信号
        self.tableWidget.cellChanged.disconnect(self.input_cellChanged)
        # except:
        #     pass
        # finally:
        self.tableWidget.clearContents()
        # 静态法清除lineEdit控件数据
        for i in range(1, 7):
            exec("self.lineEdit_{}.setText('')".format(i))


class Packing(QWidget, Ui_Form):
    """包装运输类"""
    def __init__(self, parent=None):
        super(Packing, self).__init__(parent)
        self.setupUi(self)

        self.label.setText("包 装 运 输 安 排")
        self.label.setStyleSheet("color:#ff6600;")
        # 加入生产编号列表框
        self.cmbNO = QtWidgets.QComboBox()
        self.cmbNO.setMinimumSize(QtCore.QSize(100, 26))
        self.cmbNO.setEditable(False)
        self.cmbNO.setObjectName("生产编号")
        self.gridLayout.addWidget(self.cmbNO, 1, 5)
        # 加入车牌号列表框
        self.cmbPN = QtWidgets.QComboBox()
        self.cmbPN.setMinimumSize(QtCore.QSize(100, 26))
        self.cmbPN.setEditable(False)
        self.cmbPN.setObjectName("车牌号")
        self.gridLayout.addWidget(self.cmbPN, 2, 5)
        self.label_2.setText('物流公司:')
        self.label_7.setText('车牌号:')
        self.label_9.setText('发货重量:')
        # 设置行表头字体
        font = QtGui.QFont('微软雅黑', 9)
        self.tableWidget.horizontalHeader().setFont(font)
        # 左垂直表头不显示
        self.tableWidget.verticalHeader().setVisible(False)
        # 只能选择单行
        # self.tableWidget.setSelectionMode(QAbstractItemView.SingleSelection)
        # 设置表格颜色             
        self.tableWidget.horizontalHeader().setStyleSheet('QHeaderView::section{background:skyblue}')
        self.tableWidget.setFrameStyle(QtWidgets.QFrame.Box | QtWidgets.QFrame.Plain)
        # 设置文本框无边框
        styleSheet = "background:transparent;border-width:0;border-style:outset"
        for i in range(1, 8):
            exec("self.lineEdit_{}.setStyleSheet(styleSheet)".format(i))
        # 发货日期默认当前日期
        self.dateEdit.setDate(QDate.currentDate())

        # 日期控件信号连接槽函数
        self.dateEdit.dateChanged.connect(self.date_dateChanged)
        self.cmbNO.activated.connect(self.cmbNO_activated)

    def date_dateChanged(self):
        """查询指定发货日期的生产编号"""
        self.cmbNO.clear()
        mymdb = myMdb()
        m_date = self.dateEdit.date().toString("yyyy-MM-dd")
        res, cur = mymdb.fetchall(field='{}'.format('distinct 生产编号'),
                                  table='{}'.format('发货记录'),
                                  where="发货日期='{}'".format(m_date))
        no_lst = [tup[0] for tup in res]
        self.cmbNO.addItems(no_lst)

    def cmbNO_activated(self):
        """根据生产编号和发货状态等于'清单装箱'完成查询"""
        self.tableWidget.clearContents()
        if self.cmbNO.currentText() == "":
            return
        mymdb = myMdb()
        m_date = self.dateEdit.date().toString("yyyy-MM-dd")  # 发货日期
        m_no = self.cmbNO.currentText()  # 编号

        field = 'b.合同编号,b.序号,b.名称,b.制造标准,b.规格型号,b.材质,a.发货数量,a.装箱编号, a.物流公司,a.车牌号'
        table = '发货记录 a inner join order_list b on a.生产编号=b.生产编号 and a.序号=b.序号 and a.发货日期=b.发货日期'
        where = "a.生产编号='{}' and a.发货日期='{}'".format(m_no, m_date)
        res, cur = mymdb.fetchall(field='{}'.format(field), table='{}'.format(table), where=where)

        tbl_header = [tup[0] for tup in cur.description]
        data = [tup[0] for tup in res]
        row = len(data)     # 获得data的行数
        vol = len(tbl_header)
        # 插入表格
        self.tableWidget.setColumnCount(vol)
        self.tableWidget.setRowCount(row)
        # 设置标题
        self.tableWidget.setHorizontalHeaderLabels(tbl_header)
        # 构建表格插入数据
        for i in range(row):
            for j in range(vol):
                temp_data = res[i][j]
                data1 = QTableWidgetItem(str(temp_data))
                if j in range(7):  # 第0-6列禁止编辑
                    data1.setFlags(QtCore.Qt.ItemIsEnabled)
                self.tableWidget.setItem(i, j, data1)
        self.tableWidget.resizeColumnsToContents()
        # self.tableWidget.resizeRowsToContents()
        # self.tableWidget.horizontalHeader().setStretchLastSection(True)
        # 汇总发货数量
        count = plusColumn(self, "tableWidget", 6)
        self.lineEdit_6.setText(str(count))
        # 带出车牌号
        self.plateNumber()

    def plateNumber(self):
        """查询指定生产编号中的车牌号"""
        self.cmbPN.clear()
        mymdb = myMdb()
        m_no = self.cmbNO.currentText()
        m_date = self.dateEdit.date().toString("yyyy-MM-dd")
        res, cur = mymdb.fetchall(field='{}'.format('distinct 车牌号'),
                                  table='{}'.format('发货记录'),
                                  where="生产编号='{}' and 发货日期='{}'".format(m_no, m_date))
        m_lst = [tup[0] for tup in res]
        self.cmbPN.addItems(m_lst)

    def savePack(self):
        """保存包装运输"""
        rows = self.tableWidget.rowCount()  # 总行数
        cols = self.tableWidget.columnCount()  # 总列数
        for row in range(rows):
            if not self.tableWidget.item(row, 7) or self.tableWidget.item(row, 7).text() == '':
                m_xh = self.tableWidget.item(row, 1).text()
                QMessageBox.warning(self, "警告", "序号{}装箱编号不能空".format(m_xh))
                return
        button = QMessageBox.question(self, "注意", "请确认无误再保存,\n按OK继续,按Cancel退出",
                                      QMessageBox.Ok|QMessageBox.Cancel, QMessageBox.Ok)
        if button == QMessageBox.Cancel:
            return

        mymdb = myMdb()
        fields = '{}'.format('生产编号,序号,发货数量,装箱编号,物流公司,车牌号,发货日期')
        preSql = "insert into {} ({})".format('发货记录', fields)
        subSql = " values(%s, %s, %s, %s, %s, %s, %s)"
        sql_on = " ON DUPLICATE KEY UPDATE 装箱编号=VALUES(装箱编号),物流公司=VALUES(物流公司),车牌号=VALUES(车牌号)"
        sql = preSql+subSql+sql_on

        # 建更新订单明细用列表
        param = []
        for row in range(rows):
            value = []
            value.append(self.cmbNO.currentText())
            for col in (1, 6, 7, 8, 9):
                value.append(self.tableWidget.item(row, col).text())
            value.append(self.dateEdit.date().toString("yyyy-MM-dd"))  # 发货日期
            param.append(value)

        # 数据库操作=====================================================================================
        mymdb.insert_many(sql, param)
        QMessageBox.about(self, "保存成功", "装箱运输记录已保存")
        self.tableWidget.clearContents()

    def printPacking(self):
        """打印装车清单"""


# class Packing(QWidget, Ui_wgtInput):
    # """包装运输类"""
    # def __init__(self, parent=None):
    #     super(Packing, self).__init__(parent)
    #     self.setupUi(self)

    #     # 隐藏不需要的控件
    #     self.cmbWork.hide()
    #     self.comboBox_2.hide()
    #     # self.cmbDpmt.hide()
    #     self.cmbDpmt.setToolTip("车牌号")
    #     self.cmbNO.setToolTip("生产编号")
    #     self.label.setText("包 装 运 输 安 排")
    #     # 发货日期默认当前日期
    #     self.dateEdit.setDate(QDate.currentDate())
    #     # 日期控件信号连接槽函数
    #     self.dateEdit.dateChanged.connect(self.date_dateChanged)
    #     self.cmbNO.activated.connect(self.cmbNO_activated)

    # def date_dateChanged(self):
    #     """查询指定发货日期的生产编号"""
    #     self.cmbNO.clear()
    #     mymdb = myMdb()
    #     m_date = self.dateEdit.date().toString("yyyy-MM-dd")
    #     res, cur = mymdb.fetchall(field='{}'.format('distinct 生产编号'),
    #                               table='{}'.format('发货记录'),
    #                               where="发货日期='{}'".format(m_date))
    #     no_lst = [tup[0] for tup in res]
    #     self.cmbNO.addItems(no_lst)

    # def cmbNO_activated(self):
    #     """根据生产编号和发货状态等于'清单装箱'完成查询"""
    #     self.tblwgtInput.clearContents()
    #     if self.cmbNO.currentText() == "":
    #         return
    #     mymdb = myMdb()
    #     m_date = self.dateEdit.date().toString("yyyy-MM-dd")  # 发货日期
    #     m_no = self.cmbNO.currentText()  # 编号

    #     field = 'b.合同编号,b.序号,b.名称,b.制造标准,b.规格型号,b.材质,a.发货数量,a.装箱编号, a.物流公司,a.车牌号'
    #     table = '发货记录 a inner join order_list b on a.生产编号=b.生产编号 and a.序号=b.序号 and a.发货日期=b.发货日期'
    #     res, cur = mymdb.fetchall(field='{}'.format(field),
    #                               table='{}'.format(table),
    #                               where="a.生产编号='{}' and a.发货日期='{}'".format(m_no, m_date))
    #     tbl_header = [
    #         '合同编号', '序号', '名称', '制造标准', '规格型号', '材质', '发货数量', '装箱编号', '物流公司', '车牌号'
    #     ]


    #     # field = '{}'.format('合同编号,序号,发货数量,装箱编号,物流公司,车牌号')
    #     # table = '{}'.format('发货记录')
    #     # where = "生产编号='{}' and 发货日期='{}'".format(m_no, m_date)
    #     # res, cur = mymdb.fetchall(field=field, table=table, where=where)

    #     tbl_header = [tup[0] for tup in cur.description]
    #     # tbl_header = ['合同编号', '序号', '发货数量', '装箱编号', '物流公司', '车牌号']
    #     data = [tup[0] for tup in res]
    #     row = len(data)     # 获得data的行数
    #     vol = len(tbl_header)
    #     # 插入表格
    #     self.tblwgtInput.setColumnCount(vol)
    #     self.tblwgtInput.setRowCount(row)
    #     font = QFont('微软雅黑', 9)
    #     self.tblwgtInput.setToolTip("装箱运输")
    #     self.tblwgtInput.horizontalHeader().setFont(font)  # 设置行表头字体
    #     self.tblwgtInput.verticalHeader().setVisible(False)  # 左垂直表头不显示
    #     # self.tblwgtInput.setSelectionMode(QAbstractItemView.SingleSelection)  # 只能选择单行
    #     # 设置标题
    #     self.tblwgtInput.setHorizontalHeaderLabels(tbl_header)
    #     # 设置表格样式             
    #     self.tblwgtInput.horizontalHeader().setStyleSheet(
    #         'QHeaderView::section{background:skyblue}')
    #     self.tblwgtInput.setFrameStyle(QFrame.Box | QFrame.Plain)
    #     # 构建表格插入数据
    #     for i in range(row):
    #         for j in range(vol):
    #             temp_data = res[i][j]
    #             data1 = QTableWidgetItem(str(temp_data))
    #             if j in range(7):  # 第0-6列禁止编辑
    #                 data1.setFlags(QtCore.Qt.ItemIsEnabled)
    #             self.tblwgtInput.setItem(i, j, data1)
    #     self.tblwgtInput.resizeColumnsToContents()
    #     # self.tblwgtInput.resizeRowsToContents()
    #     # self.tblwgtInput.horizontalHeader().setStretchLastSection(True)
    #     self.plateNumber()

    # def plateNumber(self):
    #     """查询指定生产编号中的车牌号"""
    #     self.cmbDpmt.clear()
    #     mymdb = myMdb()
    #     m_no = self.cmbNO.currentText()
    #     m_date = self.dateEdit.date().toString("yyyy-MM-dd")
    #     res, cur = mymdb.fetchall(field='{}'.format('distinct 车牌号'),
    #                               table='{}'.format('发货记录'),
    #                               where="生产编号='{}' and 发货日期='{}'".format(m_no, m_date))
    #     m_lst = [tup[0] for tup in res]
    #     self.cmbDpmt.addItems(m_lst)

    # def savePack(self):
    #     """保存包装运输"""
    #     rows = self.tblwgtInput.rowCount()  # 总行数
    #     cols = self.tblwgtInput.columnCount()  # 总列数
    #     for row in range(rows):
    #         if not self.tblwgtInput.item(row, 3) or self.tblwgtInput.item(row, 3).text() == '':
    #             m_xh = self.tblwgtInput.item(row, 1).text()
    #             QMessageBox.warning(self, "警告", "序号{}装箱编号不能空".format(m_xh))
    #             return
    #     button = QMessageBox.question(self, "注意", "请确认无误再保存,\n按OK继续,按Cancel退出",
    #                                   QMessageBox.Ok|QMessageBox.Cancel, QMessageBox.Ok)
    #     if button == QMessageBox.Cancel:
    #         return

    #     mymdb = myMdb()
    #     fields = '{}'.format('生产编号,合同编号,序号,发货数量,装箱编号,物流公司,车牌号,发货日期')
    #     preSql = "insert into {} ({})".format('发货记录', fields)
    #     subSql = " values(%s, %s, %s, %s, %s, %s, %s, %s)"
    #     sql_on = " ON DUPLICATE KEY UPDATE 装箱编号=VALUES(装箱编号),物流公司=VALUES(物流公司),车牌号=VALUES(车牌号)"
    #     sql = preSql+subSql+sql_on

    #     # 建更新订单明细用列表
    #     param = []
    #     for row in range(rows):
    #         value = []
    #         value.append(self.cmbNO.currentText())
    #         for col in range(6):
    #             value.append(self.tblwgtInput.item(row, col).text())
    #         value.append(self.dateEdit.date().toString("yyyy-MM-dd"))  # 发货日期
    #         param.append(value)

    #     # 数据库操作=====================================================================================
    #     mymdb.insert_many(sql, param)
    #     QMessageBox.about(self, "保存成功", "装箱运输记录已保存")
    #     self.tblwgtInput.clearContents()

    # def printPacking(self):
    #     """打印装车清单"""


class DeliveryRevise(QWidget, Ui_Form):
    """修改送货清单类"""
    def __init__(self, parent=None):
        super(DeliveryRevise, self).__init__(parent)
        self.setupUi(self)
        self.initTableWidget()

        self.cmbNO = QtWidgets.QComboBox()
        self.cmbNO.setMinimumSize(QtCore.QSize(100, 26))
        self.cmbNO.setEditable(False)
        self.cmbNO.setObjectName("生产编号")
        self.gridLayout.addWidget(self.cmbNO, 1, 5)

        self.tableWidget.cellChanged.connect(self.input_cellChanged)
        # 日期控件信号连接槽函数
        self.dateEdit.dateChanged.connect(self.date_dateChanged)
        self.cmbNO.activated.connect(self.cmbNO_activated)
        # 单元格点击事件,记录前值
        self.tableWidget.itemClicked.connect(self.outSelect)

    def initTableWidget(self):
        """初始化tablewidget"""
        self.label.setText("修 改 送 货 清 单")
        self.label.setStyleSheet("color:#ff6600;")

        # 设置行表头字体
        font = QtGui.QFont('微软雅黑', 9)
        self.tableWidget.horizontalHeader().setFont(font)
        # 左垂直表头不显示
        self.tableWidget.verticalHeader().setVisible(False)
        # 只能选择单行
        self.tableWidget.setSelectionMode(QAbstractItemView.SingleSelection)
        # 设置表格颜色             
        self.tableWidget.horizontalHeader().setStyleSheet('QHeaderView::section{background:skyblue}')
        self.tableWidget.setFrameStyle(QtWidgets.QFrame.Box | QtWidgets.QFrame.Plain)
        # 设置文本框无边框
        styleSheet = "background:transparent;border-width:0;border-style:outset"
        for i in range(1, 8):
            exec("self.lineEdit_{}.setStyleSheet(styleSheet)".format(i))
        # 设置当前日期
        self.dateEdit.setDate(QDate.currentDate())

    def date_dateChanged(self):
        """查询指定发货日期的生产编号"""
        self.cmbNO.clear()
        mymdb = myMdb()
        m_date = self.dateEdit.date().toString("yyyy-MM-dd")
        res, cur = mymdb.fetchall(field='{}'.format('distinct 生产编号'),
                                  table='{}'.format('发货记录'),
                                  where="发货日期='{}'".format(m_date))
        no_lst = [tup[0] for tup in res]
        self.cmbNO.addItems(no_lst)

    def cmbNO_activated(self):
        """选择生产编号查询数据"""
        self.tableWidget.blockSignals(True)  # 暂停单元格修改信号
        self.tableWidget.clearContents()
        mymdb = myMdb()
        m_date = self.dateEdit.date().toString("yyyy-MM-dd")  # 发货日期
        m_no = self.cmbNO.currentText()  # 编号
        field = 'b.合同编号,b.序号,b.名称,b.制造标准,b.规格型号,b.材质,b.数量,b.已发货数,a.质保书,a.发货数量,a.装箱编号, \
            a.收货单位,a.收货地址,a.联系方式'
        table = '发货记录 a inner join order_list b on a.生产编号=b.生产编号 and a.序号=b.序号 and a.发货日期=b.发货日期'
        res, cur = mymdb.fetchall(field='{}'.format(field),
                                  table='{}'.format(table),
                                  where="a.生产编号='{}' and a.发货日期='{}'".format(m_no, m_date))
        tbl_header = [
            '合同编号', '序号', '名称', '制造标准', '规格型号', '材质', '订单数量', '已发货数', '质保书', '发货数量', '装箱编号'
        ]
        data = [tup[0] for tup in res]
        row = len(data)     # 获得data的行数
        vol = len(tbl_header)  # 获得data的列数
        # 插入表格
        self.tableWidget.setColumnCount(vol)
        self.tableWidget.setRowCount(row)
        # 设置标题
        self.tableWidget.setHorizontalHeaderLabels(tbl_header)
        # 构建表格插入数据
        for i in range(row):
            for j in range(vol):
                temp_data = res[i][j]
                data1 = QTableWidgetItem(str(temp_data))
                if j in range(8):  # 第0-7列禁止编辑
                    data1.setFlags(QtCore.Qt.ItemIsEnabled)
                self.tableWidget.setItem(i, j, data1)
        self.lineEdit_1.setText(res[0][11])
        self.lineEdit_2.setText(res[0][12])
        self.lineEdit_3.setText(res[0][13])
        self.tableWidget.resizeColumnsToContents()
        # self.tableWidget.resizeRowsToContents()
        # self.tableWidget.horizontalHeader().setStretchLastSection(True)
        # 汇总发货数量
        count = plusColumn(self, "tableWidget", 9)
        self.lineEdit_6.setText(str(count))
        self.tableWidget.blockSignals(False)  # 启动单元格修改信号

        # 点击单元格取单元格值

    def outSelect(self, Item=None):
        """获得点击单元格的值"""
        if Item == None:
            return
        if Item == '':
            Item = 0
        # 把table_value设为全局变量,给添加修改记录用
        global g_TXT
        g_TXT = Item.text()
        # return m_txt

    def input_cellChanged(self, row, col):
        """输入完成数量后计算判断数量是否正确"""
        self.tableWidget.blockSignals(True)  # 暂停单元格修改信号
        if col == 9:
            if self.tableWidget.item(row, col).text() == '':  # 发货数=空时退出
                self.tableWidget.setItem(row, col, QTableWidgetItem('0'))

            m_order = int(self.tableWidget.item(row, 6).text())  # 订单数量
            m_cmpt = int(self.tableWidget.item(row, 7).text())  # 已发货数
            m_cmp = int(self.tableWidget.item(row, 9).text())  # 发货数量
            # 发货数量和前值对比,修改已发货数
            if int(g_TXT) > m_cmp:
                m_cmpt = m_cmpt - (int(g_TXT) - m_cmp)
            elif int(g_TXT) < m_cmp:
                m_cmpt = m_cmpt + (m_cmp - int(g_TXT))

            if m_cmpt > m_order or m_cmp < 0:
                QMessageBox.warning(self, "警告", "发货数量有误,请检查修改!")
                self.tableWidget.setItem(row, 9, QTableWidgetItem(g_TXT))
                self.tableWidget.blockSignals(False)  # 开启单元格修改信号
                return
            elif m_cmp == 0:
                self.tableWidget.setItem(row, 10, QTableWidgetItem(''))

            # 修改已发货数
            m_dlv = QTableWidgetItem(str(m_cmpt))
            m_dlv.setFlags(QtCore.Qt.ItemIsEnabled)
            self.tableWidget.setItem(row, 7, m_dlv)

        self.tableWidget.item(row, col).setForeground(QBrush(QColor(255, 0, 0)))
        # 汇总发货数量
        count = plusColumn(self, "tableWidget", 9)
        self.lineEdit_6.setText(str(count))
        self.tableWidget.blockSignals(False)  # 开启单元格修改信号

    def saveDeliveryRevise(self):
        """保存修改的发货清单"""
        rows = self.tableWidget.rowCount()  # 总行数
        cols = self.tableWidget.columnCount()  # 总列数

        if self.lineEdit_2 == '' or self.lineEdit_3 == '':
            QMessageBox.about(self, "警告", "发货地址/联系方式不能空")
            return
        button = QMessageBox.question(self, "注意", "请确认无误再保存发货清单,\n按OK继续,按Cancel退出",
                                      QMessageBox.Ok|QMessageBox.Cancel, QMessageBox.Ok)
        if button == QMessageBox.Cancel:
            return

        mymdb = myMdb()
        # 建更新订单明细的发货清单明细sql 需加质保书/发货日期/发货状态判断有无发过
        field_list = '{}'.format('生产编号,序号,已发货数,质保书,发货日期,发货状态')
        preSql_list = "insert into {} ({})".format('order_list', field_list)
        subSql_list = " values(%s, %s, %s, %s, %s, %s)"
        sql_list_on = " ON DUPLICATE KEY UPDATE 已发货数=VALUES(已发货数),质保书=VALUES(质保书),发货状态=VALUES(发货状态)"
        sql_list = preSql_list+subSql_list+sql_list_on

        fields = '{}'.format('收货单位,收货地址,联系方式,生产编号,序号,质保书,发货数量,装箱单号,发货日期')
        preSql = "insert into {} ({})".format('发货记录', fields)
        subSql = " values(%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        sql_on = " ON DUPLICATE KEY UPDATE 收货单位=VALUES(收货单位),收货地址=VALUES(收货地址), \
                   联系方式=VALUES(联系方式),质保书=VALUES(质保书),发货数量=VALUES(发货数量),装箱单号=VALUES(装箱单号)"
        sql = preSql+subSql+sql_on

        # 建更新订单明细用列表
        param_list = []  # 建传入值的列表
        param = []
        for row in range(rows):
            value_list = []
            value_list.append(self.cmbNO.currentText())  # 生产编号
            for col in (1, 7, 8):
                value_list.append(self.tableWidget.item(row, col).text())
            value_list.append(self.dateEdit.date().toString("yyyy-MM-dd"))  # 发货日期
            # 判断发货状态
            if int(self.tableWidget.item(row, 9).text()) == 0 and int(self.tableWidget.item(row, 7).text()) > 0:
                value_list.append('部分发货')
            elif int(self.tableWidget.item(row, 7).text()) == 0:
                value_list.append('')
            elif int(self.tableWidget.item(row, 9).text()) > 0:
                value_list.append('清点装箱')
            param_list.append(value_list)

            # 发货记录value列表
            value = []
            value.append(self.lineEdit_1.text())
            value.append(self.lineEdit_2.text())
            value.append(self.lineEdit_3.text())
            value.append(self.cmbNO.currentText())
            for col in (1, 8, 9, 10):
                value.append(self.tableWidget.item(row, col).text())
            value.append(self.dateEdit.date().toString("yyyy-MM-dd"))
            param.append(value)
        # 数据库操作==============================================================
        rowcount = mymdb.insert_many(sql_list, param_list)
        # 发货汇总数据写入发货记录
        mymdb.insert_many(sql, param)
        QMessageBox.about(self, "修改成功", "成功修改发货清单")
        self.clearDeliveryData()

    def clearDeliveryData(self):
        """清除发货清单窗口数据"""
        self.tableWidget.clearContents()
        # 静态法清除lineEdit控件数据
        for i in range(1, 7):
            exec("self.lineEdit_{}.setText('')".format(i))
        self.cmbNO.clear()


class Transport(QWidget, Ui_Form):
    """运输类"""
    def __init__(self, parent=None):
        super(Transport, self).__init__(parent)
        self.setupUi(self)
        self.initTableWidget()

        # 设置列表框手动输入生产编号
        self.cmbNO = QtWidgets.QComboBox()
        self.cmbNO.setMinimumSize(QtCore.QSize(100, 26))
        self.cmbNO.setEditable(False)
        self.cmbNO.setObjectName("生产编号")
        self.gridLayout.addWidget(self.cmbNO, 1, 5)

        self.dateEdit.setDate(QDate.currentDate())

        # 显示清点装箱状态的生产编号
        mymdb = myMdb()
        res, cur = mymdb.fetchall(field='{}'.format('distinct 生产编号'),
                                  table='{}'.format('order_list'),
                                  where="发货状态='{}'".format('清点装箱'))
        no_lst = [tup[0] for tup in res]
        self.cmbNO.addItems(no_lst)

        # 日期控件信号连接槽函数
        self.cmbNO.activated.connect(self.cmbNO_activated)

    def initTableWidget(self):
        """初始化tablewidget"""
        self.label.setText("物 流 记 录")
        self.label.setStyleSheet("color:#ff6600;")
        self.label_8.setText('发货重量:')
        self.label_4.setText('运费:')
        # 设置行表头字体
        font = QtGui.QFont('微软雅黑', 9)
        self.tableWidget.horizontalHeader().setFont(font)
        # 左垂直表头不显示
        self.tableWidget.verticalHeader().setVisible(False)
        # 只能选择单行
        self.tableWidget.setSelectionMode(QAbstractItemView.SingleSelection)
        # 设置表格颜色             
        self.tableWidget.horizontalHeader().setStyleSheet('QHeaderView::section{background:skyblue}')
        self.tableWidget.setFrameStyle(QtWidgets.QFrame.Box | QtWidgets.QFrame.Plain)
        # 设置文本框无边框
        styleSheet = "background:transparent;border-width:0;border-style:outset"
        for i in range(1, 8):
            exec("self.lineEdit_{}.setStyleSheet(styleSheet)".format(i))
        # 设置当前日期
        self.dateEdit.setDate(QDate.currentDate())

    def cmbNO_activated(self, param):
        """选择生产编号查询数据"""
        self.tableWidget.blockSignals(True)  # 暂停单元格修改信号
        self.tableWidget.clearContents()
        mymdb = myMdb()
        m_no = self.cmbNO.currentText()  # 编号
        field = '序号,数量,装箱编号'
        table = 'order_list'
        res, cur = mymdb.fetchall(field='{}'.format(field),
                                  table='{}'.format(table),
                                  where="生产编号='{}' and 发货状态='{}'".format(m_no, '清点装箱'))
        tbl_header = ['序号', '数量', '装箱单号', '物流公司', '车牌号']
        data = [tup[0] for tup in res]
        row = len(data)     # 获得data的行数
        vol = len(tbl_header)  # 获得data的列数
        # 插入表格
        self.tableWidget.setColumnCount(vol)
        self.tableWidget.setRowCount(row)
        # 设置标题
        self.tableWidget.setHorizontalHeaderLabels(tbl_header)
        # 构建表格插入数据
        for i in range(row):
            for j in range(3):
                temp_data = res[i][j]
                data1 = QTableWidgetItem(str(temp_data))
                if j in range(3):  # 第0-7列禁止编辑
                    data1.setFlags(QtCore.Qt.ItemIsEnabled)
                self.tableWidget.setItem(i, j, data1)
        # self.lineEdit_1.setText(res[0][11])
        # self.lineEdit_2.setText(res[0][12])
        # self.lineEdit_3.setText(res[0][13])
        self.tableWidget.resizeColumnsToContents()
        # self.tableWidget.resizeRowsToContents()
        # self.tableWidget.horizontalHeader().setStretchLastSection(True)
        # 汇总发货数量
        # count = plusColumn(self, "tableWidget", 9)
        # self.lineEdit_6.setText(str(count))
        self.tableWidget.blockSignals(False)  # 启动单元格修改信号

        # 点击单元格取单元格值

    def writeParam(self, param):
        """写入查询数据"""
        self.tableWidget.blockSignals(True)  # 暂停单元格修改信号
        row = len(param)  # 获得查询窗口选择数据的行数
        # 找出送货地址,联系方式
        mymdb = myMdb()
        res, cur = mymdb.fetchall(field='{}'.format('交货地点,联系方式'),
                                  table='{}'.format('orders'),
                                  where="生产编号='{}'".format(param[0][2]))
        # 设置标题
        tbl_header = [
            '序号', '名称', '制造标准', '规格型号', '材质', '订单数量',
            '工作令号', '件号', '已发货数', '质保书', '发货数量'
        ]
        col = len(tbl_header)
        self.tableWidget.setRowCount(row)
        self.tableWidget.setColumnCount(col)
        self.tableWidget.setHorizontalHeaderLabels(tbl_header)
        self.lineEdit_1.setText(param[0][0])
        self.lineEdit_2.setText(str(res[0][0]))
        self.lineEdit_3.setText(str(res[0][1]))
        self.lineEdit_4.setText(param[0][2])
        # 一生产编号有多合同号的情况,考虑用筛选法选出合同号加到cmb,再选择显示同一合同号
        self.lineEdit_5.setText(param[0][1])
        for i in range(row):
            # 取第4列到第12列
            for j in range(3, 13):
                temp_data = param[i][j]
                if temp_data == 'None':
                    temp_data = 0
                data_1 = QTableWidgetItem(str(temp_data))
                # j=12质保书列可编辑
                if j != 12:
                    data_1.setFlags(QtCore.Qt.ItemIsEnabled)  # 禁止指定列编辑
                self.tableWidget.setItem(i, j-3, data_1)
            # 把送货单明细第11列None状态设为空值
            self.tableWidget.setItem(i, 10, QTableWidgetItem(''))
        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.blockSignals(False)  # 启动单元格修改信号


class Warranty(QWidget, Ui_wgtInput):
    """质保书类"""
    def __init__(self, parent=None):
        super(Warranty, self).__init__(parent)
        self.setupUi(self)

        # 隐藏不需要的控件
        self.btn_query.hide()
        self.cmbWork.hide()
        self.comboBox_2.hide()
        # 设置列表框手动输入生产编号
        # self.cmbNO.setEditable(True)
        self.cmbDpmt.addItems(['发货'])
        self.label.setText("质保书")
        # self.addcmbNO()