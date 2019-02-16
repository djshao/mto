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

        # 隐藏不需要的控件
        # self.btn_query.hide()
        # self.cmbWork.hide()
        # self.comboBox_2.hide()
        # 设置列表框手动输入生产编号
        # self.cmbNO.setEditable(True)
        # self.cmbDpmt.addItems(['送货清单'])
        # self.label.setText("送 货 清 单")

        # 信号槽
        # self.btn_query.clicked.connect(self.btn_query_clicked)
        # self.tablewidget.itemClicked.connect(self.tablewidget_itemClicked)  # 点击清单,显示选择的明细
        # 下拉列表框选择事件连接

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
        for i in range(1, 11):
            exec("self.lineEdit_{}.setStyleSheet(styleSheet)".format(i))

    def writeParam(self, param):
        """写入查询数据"""
        # self.clearPlanData()
        row = len(param)  # 获得查询窗口选择数据的行数
        m_no = param[0][2]  # 生产编号
        # 找出送货地址,联系方式
        mymdb = myMdb()
        res, cur = mymdb.fetchall(field='{}'.format('交货地点,联系方式'),
                                  table='{}'.format('orders'),
                                  where="生产编号='{}'".format(m_no))
        # 设置标题
        tbl_header = [
            '序号', '名称', '制造标准', '规格型号', '材质', '订单数量', '工作令号',
            '件号', '已发货数', '质保书', '发货数量', '装箱编号', '发货状态'
        ]
        col = len(tbl_header)
        self.tableWidget.setRowCount(row)
        self.tableWidget.setColumnCount(col)
        self.tableWidget.setHorizontalHeaderLabels(tbl_header)
        self.lineEdit_1.setText(param[0][0])
        self.lineEdit_2.setText(str(res[0][0]))
        self.lineEdit_3.setText(str(res[0][1]))
        self.lineEdit_4.setText(time.strftime("%Y-%m-%d", time.localtime()))
        self.lineEdit_5.setText(m_no)
        self.lineEdit_6.setText(param[0][1])
        for i in range(row):
            # 取第4列到第12列
            for j in range(3, 13):
                temp_data = param[i][j]
                if temp_data == 'None':
                    temp_data = 0
                data_1 = QTableWidgetItem(str(temp_data))
                data_1.setFlags(QtCore.Qt.ItemIsEnabled)  # 禁止指定列编辑
                self.tableWidget.setItem(i, j-3, data_1)

            # 把送货单明细第11列到13列None状态设为空值
            for j in range(10, 13):
                data_2 = QTableWidgetItem('')
                self.tableWidget.setItem(i, j, data_2)
        self.tableWidget.resizeColumnsToContents()
        # 开启单元格变更信号
        self.tableWidget.cellChanged.connect(self.input_cellChanged)

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
            if m_all > m_order or m_cmp < 0:
                QMessageBox.warning(self, "警告", "发货数量错误,请检查!")
                self.tableWidget.setItem(row, col, QTableWidgetItem(0))
                # self.tableWidget.setItem(row, 10, QTableWidgetItem(''))
                self.tableWidget.blockSignals(False)  # 开启单元格修改信号
                return

            if m_all == m_order:
                forge_state = '发货完成'
            if m_all < m_order:
                forge_state = '部分发货'

            self.tableWidget.item(row, col).setForeground(QBrush(QColor(255, 0, 0)))
            # 汇总发货数量
            count = plusColumn(self, "tableWidget", 10)
            self.lineEdit_7.setText(str(count))
            # 更新发货状态
            m_st = QTableWidgetItem(forge_state)
            m_st.setFlags(QtCore.Qt.ItemIsEnabled)
            self.tableWidget.setItem(row, 12, m_st)
            self.tableWidget.blockSignals(False)  # 开启单元格修改信号

    def saveDate(self):
        """保存发货清单"""
        rows = self.tableWidget.rowCount()  # 总行数
        cols = self.tableWidget.columnCount()  # 总列数
        for row in range(rows):
            if not self.tableWidget.item(row, 10) or self.tableWidget.item(row, 10).text() == '':
                m_xh = self.tableWidget.item(row, 0).text()
                QMessageBox.warning(self, "警告", "序号{}不能空".format(m_xh))
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
        filed_list = '生产编号,序号,质保书,已发货数,装箱编号,发货状态,发货日期'
        preSql_list = "insert into order_list ({})".format(filed_list)
        subSql_list = "values(%s, %s, %s, %s, %s, %s, %s)"
        sql_list_on = "ON DUPLICATE KEY UPDATE 已发货数=VALUES(已发货数),质保书=VALUES(质保书), \
            装箱编号=VALUES(装箱编号),发货状态=VALUES(发货状态),发货日期=VALUES(发货日期)"
        sql_list = preSql_list+subSql_list+sql_list_on

        # 建发货记录的sql
        filed = '生产编号,收货单位,收货地址,联系方式,发货日期,发货总数,发货人'
        preSql = "insert into 发货记录 ({})".format(filed)
        subSql = "values(%s, %s, %s, %s, %s, %s, %s)"
        sql = preSql+subSql
        param_list = []  # 建传入值的列表
        param = []
        for row in range(rows):
            # 建更新订单明细用列表
            value_list = []
            value_list.append(self.lineEdit_5.text())  # 生产编号
            m_fhsl = self.tableWidget.item(row, 10).text()  # 发货数量
            m_yfhs = self.tableWidget.item(row, 8).text()  # 已发货数
            for col in (0, 9, 10, 11, 12):
                if col == 10:
                    value_list.append(int(m_fhsl)+int(m_yfhs))
                else:
                    value_list.append(self.tableWidget.item(row, col).text())
            value_list.append(self.lineEdit_4.text())  # 发货日期
            param_list.append(value_list)

        # 建发货记录列表
        value = []
        value.append(self.lineEdit_5.text())
        value.append(self.lineEdit_1.text())
        value.append(self.lineEdit_2.text())
        value.append(self.lineEdit_3.text())
        value.append(self.lineEdit_4.text())
        value.append(self.lineEdit_7.text())
        value.append(self.lineEdit_8.text())
        param.append(value)
        # 数据库操作==============================================================
        # 更新order_list发货情况  存在双倍数量,怀疑是ON DUPLICATE KEY UPDATE引起??????
        rowcount = mymdb.insert_many(sql_list, param_list)
        # 发货汇总数据写入发货目录
        mymdb.insert_many(sql, param)
        QMessageBox.about(self, "保存成功", "保存了"+str(int(rowcount/2))+"条发货记录")
        self.clearDeliveryData()

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
        for i in range(1, 11):
            exec("self.lineEdit_{}.setText('')".format(i))


class PackingList(QWidget, Ui_wgtInput):
    """装箱清单类"""
    def __init__(self, parent=None):
        super(PackingList, self).__init__(parent)
        self.setupUi(self)

        # 隐藏不需要的控件
        self.btn_query.hide()
        self.cmbWork.hide()
        self.comboBox_2.hide()
        self.cmbDpmt.addItems(['装箱单'])
        self.label.setText("装箱单")
        self.cmbNO.addItem("1T")


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