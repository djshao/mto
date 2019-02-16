# -*- coding: utf-8 -*-
"""
质保功能模块
"""
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QColor, QBrush, QPixmap, QIcon, QFont
from PyQt5.QtCore import pyqtSignal, QObject, Qt, pyqtSlot, QDate, QDateTime
from PyQt5.QtWidgets import *

import pymysql
import time

from ui.Ui_input import Ui_wgtInput
from tools.mysql_conn import myMdb
from tools.tools import *

mymdb = myMdb()  # 常用的实例和变量可以放最前


class Inspection(QWidget, Ui_wgtInput):
    """出厂检验类"""
    def __init__(self, parent=None):
        super(Inspection, self).__init__(parent)
        self.setupUi(self)

        # 隐藏不需要的控件
        self.btn_query.hide()
        self.cmbWork.hide()
        self.comboBox_2.hide()
        # 设置列表框手动输入生产编号
        # self.cmbNO.setEditable(True)
        self.cmbDpmt.addItems(['质检'])
        self.label.setText("出 厂 检 验 录 入")
        self.addcmbNO()

        # 生产编号列表框回车激活信号就连接
        self.cmbNO.activated.connect(self.cmbNO_activated)
        # 生产编号列表框选择变动信号连接
        # self.cmbNO.currentIndexChanged.connect(self.cmbDpmt_currentIndexChanged)
        self.tblwgtInput.itemClicked.connect(self.addItemsCmb)  # 明细区点击事件,加入cmb控件

    def cmbNO_activated(self):
        """查询未检验完成的明细"""
        self.clearEntryData()
        m_no = self.cmbNO.currentText()
        res = mymdb.fetchall(
            table='order_list',
            field='序号,名称,制造标准,规格型号,材质,数量,已检验数,检验人员',
            # where="生产状态 in ('部分机加','机加完成,'部分检验')")
            where='生产编号='+"'"+m_no+"'"+" and (生产状态='部分机加' or 生产状态='机加完成' or 生产状态='部分检验')")
        if res[0] == ():
            return
        # data = [tup[0] for tup in res[0]]
        # 取游标的标题列表
        # col_lst = [tup[0] for tup in res[1].description]
        row = len([tup[0] for tup in res[0]])  # 获得的行数
        col = len(res[0][0])
        self.tblwgtInput.setColumnCount(11)
        self.tblwgtInput.setRowCount(row)
        font = QtGui.QFont('微软雅黑', 9)
        self.tblwgtInput.horizontalHeader().setFont(font)  # 设置行表头字体
        col_lst = [
            '序号', '名称', '制造标准', '规格型号', '材质', '订单数量', '已检验数', '检验人员', '检验数量', '检验日期', '生产状态'
        ]
        self.tblwgtInput.setHorizontalHeaderLabels(col_lst)  # 设置标题
        self.tblwgtInput.setToolTip("生产明细")
        self.tblwgtInput.horizontalHeader().setStyleSheet(
            'QHeaderView::section{background:skyblue}')
        self.tblwgtInput.setFrameStyle(QtWidgets.QFrame.Box | QtWidgets.QFrame.Plain)
        #构建表格插入数据
        for i in range(row):
            for j in range(col-1):
                temp_data = res[0][i][j]
                data = QTableWidgetItem(str(temp_data))
                data.setFlags(QtCore.Qt.ItemIsEnabled)  # 禁止指定列编辑
                self.tblwgtInput.setItem(i, j, data)
            self.tblwgtInput.setItem(i, 7, QTableWidgetItem(''))
            # 加入当天日期为完成日期
            m_date = QTableWidgetItem(time.strftime("%Y-%m-%d", time.localtime()))
            m_date.setFlags(QtCore.Qt.ItemIsEnabled)
            self.tblwgtInput.setItem(i, 9, m_date)
            item0 = QTableWidgetItem()
            item0.setFlags(QtCore.Qt.ItemIsEnabled)
            self.tblwgtInput.setItem(i, 10, item0)
        # 适应列宽/行高/最后一列对齐边框
        self.tblwgtInput.horizontalHeader().setStretchLastSection(True)
        # self.tblwgtInput.resizeRowsToContents()
        self.tblwgtInput.resizeColumnsToContents()

        # 开启单元格变更信号
        self.tblwgtInput.cellChanged.connect(self.input_cellChanged)

    def addcmbNO(self):
        """筛选生产编号"""
        self.cmbNO.clear()
        res = mymdb.fetchall(
            field='distinct 生产编号',
            table='order_list',
            where="生产状态='机加完成' or 生产状态='部分机加' or 生产状态='部分检验'")
        # print(res)
        if res is None:
            return
        no_lst = [tup[0] for tup in res[0]]
        self.cmbNO.addItems(no_lst)

    def addItemsCmb(self):
        """点击单元格显示cmb列表框事件,有全屏退出问题"""
        # 尝试删除列表框,用于再次点击事件
        # QTableWidget.removeCellWidget(int row,int column)
        #删除第row行第column列的窗口部件
        try:
            self.cmb.deleteLater()
        except:
            pass
        finally:
            if self.tblwgtInput.currentItem().column() == 7:
                # 加单元格下拉列表框
                self.cmb = QComboBox()
                result = mymdb.fetchall(field='姓名', table='employee', where="职务='检验员'")
                # 循环取元祖数据,转为列表
                self.cmb.insertItem(0, "选择人员")
                self.cmb.addItems([tup[0] for tup in result[0]])
                # 设置字体颜色
                h = self.tblwgtInput.currentItem().row()
                self.tblwgtInput.setCellWidget(h, 7, self.cmb)
                self.tblwgtInput.resizeColumnsToContents()

                # self.gLayout = QtWidgets.QGridLayout(self.tblwgtInput)
                # self.gLayout.addWidget(self.cmb)
                # 列表框点击事件
                self.cmb.currentIndexChanged.connect(self.cmb_currentIndexChanged)

    def cmb_currentIndexChanged(self):
        """cmb控件选择后写入单元格"""
        m_txt = self.cmb.currentText()
        m_row = self.tblwgtInput.currentItem().row()
        m_col = self.tblwgtInput.currentItem().column()
        self.tblwgtInput.setItem(m_row, m_col, QTableWidgetItem(str(m_txt)))
        # 删除cmb
        self.tblwgtInput.removeCellWidget(m_row, m_col)
        # self.tblwgtInput.resizeColumnsToContents()

    @pyqtSlot()
    def on_pbtnSave_clicked(self):
        """保存出厂进度录入"""
        rows = self.tblwgtInput.rowCount()  # 总行数
        cols = self.tblwgtInput.columnCount()  # 总列数
        filed = '生产编号,序号,检验人员,检验数量,检验日期'
        preSql = "insert into 出厂检验 ("+filed+")"
        subSql = "values(%s, %s, %s, %s, %s)"
        sql = preSql+subSql  # 前后相加成一个完整的sql
        sql_1 = "INSERT INTO order_list (生产编号,序号,检验人员,已检验数,生产状态) VALUES(%s, %s, %s, %s, %s)  \
                ON DUPLICATE KEY UPDATE 检验人员=VALUES(检验人员),已检验数=VALUES(已检验数),生产状态=VALUES(生产状态)"
        # print(sql)
        param = []  # 建传入值的列表
        param_1 = []
        for row in range(rows):
            # 判断序号None或空值时退出循环
            if self.tblwgtInput.item(row, 0) is None or self.tblwgtInput.item(row, 0).text() == "":
                break
            # 判断检验数量None或空值时pass
            if self.tblwgtInput.item(row, 8) is None or self.tblwgtInput.item(row, 8).text() == "":
                continue
            else:
                value_list = []
                m_NO = self.cmbNO.currentText()
                value_list.append(m_NO)
                value_list.append(self.tblwgtInput.item(row, 0).text())
                value_list.append(self.tblwgtInput.item(row, 7).text())
                value_list.append(self.tblwgtInput.item(row, 8).text())
                value_list.append(self.tblwgtInput.item(row, 9).text())
                param.append(value_list)
                # 已完成数
                value_list_1 = []
                m_xh = self.tblwgtInput.item(row, 0).text()  # 序号
                m_state = self.tblwgtInput.item(row, 10).text()  # 检验状态

                if self.tblwgtInput.item(row, 6).text() == 'None':  # 已检验数=none时设为0
                    m_cmpt = 0
                else:
                    m_cmpt = int(self.tblwgtInput.item(row, 6).text())
                m_cmp = int(self.tblwgtInput.item(row, 8).text())  # 检验数量
                m_all = m_cmpt + m_cmp  # 完成总数
                value_list_1.append(m_NO)
                value_list_1.append(m_xh)
                value_list_1.append(self.tblwgtInput.item(row, 7).text())
                value_list_1.append(m_all)
                value_list_1.append(m_state)
                param_1.append(value_list_1)

        # 数据库操作-->写入检验完成数据==============================================================
        rowcount = mymdb.insert_many(sql, param)
        # 更新-->检验状态
        mymdb.updateAll(sql_1, param_1)
        QMessageBox.about(self, "保存成功", "保存了"+str(rowcount)+"条检验记录")
        self.clearEntryData()
        # self.queryProductionNumber()

    # 输入完成数量后判断数值是否超过订单数量
    def input_cellChanged(self, row, col):
        """输入完成数量后计算判断数量是否正确"""
        if col == 8:
            if self.tblwgtInput.item(row, col).text() == '':  # 完成数=空时退出
                self.tblwgtInput.setItem(row, 10, QTableWidgetItem(''))
                return

            self.tblwgtInput.blockSignals(True)  # 暂停单元格修改信号
            m_order = int(self.tblwgtInput.item(row, 5).text())  # 订单数量
            if self.tblwgtInput.item(row, 6).text() == 'None':  # 已完成数=none时设为0
                m_cmpt = 0
            else:
                m_cmpt = int(self.tblwgtInput.item(row, 6).text())  # 已完成数

            m_cmp = int(self.tblwgtInput.item(row, 8).text())  # 完成数量
            m_all = m_cmpt + m_cmp  # 完成总数
            if m_all > m_order or m_cmp < 0:
                QMessageBox.warning(self, "警告", "锻造数量错误,请检查!")
                self.tblwgtInput.setItem(row, col, QTableWidgetItem(0))
                self.tblwgtInput.setItem(row, 10, QTableWidgetItem(''))
                self.tblwgtInput.blockSignals(False)  # 开启单元格修改信号
                return

            if m_all == m_order:
                forge_state = '检验完成'
            if m_all < m_order:
                forge_state = '部分检验'
            self.tblwgtInput.item(row, col).setForeground(QBrush(QColor(255, 0, 0)))
            # 更新锻造状态
            m_st = QTableWidgetItem(forge_state)
            m_st.setFlags(QtCore.Qt.ItemIsEnabled)
            self.tblwgtInput.setItem(row, 10, m_st)
            self.tblwgtInput.blockSignals(False)  # 开启单元格修改信号

    def clearEntryData(self):
        try:
            # 关闭单元格变化信号
            self.tblwgtInput.cellChanged.disconnect(self.input_cellChanged)
        except:
            pass
        finally:
            self.tblwgtInput.clearContents()
