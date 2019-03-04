# -*- coding: utf-8 -*-
"""
生产功能模块
"""
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QColor, QBrush, QPixmap, QIcon, QFont
from PyQt5.QtCore import pyqtSignal, QObject, Qt, pyqtSlot, QDate, QDateTime
from PyQt5.QtWidgets import *

import pymysql
import time

from ui.Ui_plan import Ui_wgt_plan
from ui.Ui_orderlist import Ui_Dialog  # 查询订单明细子窗口

from ui.Ui_input import Ui_wgtInput
from tools.mysql_conn import myMdb
from tools.tools import *

mymdb = myMdb()

class Machine(QWidget, Ui_wgtInput):
    """机加类"""
    def __init__(self, parent=None):
        super(Machine, self).__init__(parent)
        self.setupUi(self)
        # self.mymdb = myMdb()

        # 隐藏不需要的控件
        # self.btn_query.hide()
        self.cmbWork.hide()
        self.comboBox_2.hide()
        self.cmbNO.setEditable(True)
        self.cmbDpmt.addItems(['金工车间', '机加外协'])
        self.label.setText("机 加 进 度 录 入")

        # 列表框变动信号连接
        self.cmbNO.activated.connect(self.cmbNO_activated)
        self.cmbDpmt.activated.connect(self.cmbDpmt_activated)
        self.tblwgtInput.itemClicked.connect(self.selectItemsDpmt)  # 明细区点击事件,加入cmb控件

    def cmbNO_activated(self):
        """查询未机加完成的明细"""
        self.clearEntryData()
        m_no = self.cmbNO.currentText()
        # if m_no == '':
        #     return
        res, cur = mymdb.fetchall(
            table='{}'.format('order_list'),
            field='{}'.format('序号,名称,制造标准,规格型号,材质,数量,已机加数,机加部门'),
            where="生产编号='{}' and 机加状态!='{}'".format(m_no,'机加完成'))
        if res == ():
            return
        # 取游标的标题列表
        # col_lst = [tup[0] for tup in cur.description]
        row = len([tup[0] for tup in res])  # 获得data的行数
        col = len(res[0])
        self.tblwgtInput.setColumnCount(11)
        self.tblwgtInput.setRowCount(row)
        font = QtGui.QFont('微软雅黑', 9)
        self.tblwgtInput.horizontalHeader().setFont(font)  # 设置行表头字体
        col_lst = [
            '序号', '名称', '制造标准', '规格型号', '材质', '订单数量', '已机加数', '机加部门', '机加数量', '机加日期', '机加状态'
        ]
        self.tblwgtInput.setHorizontalHeaderLabels(col_lst)  # 设置标题
        self.tblwgtInput.setToolTip("机加明细")
        self.tblwgtInput.horizontalHeader().setStyleSheet(
            'QHeaderView::section{background:skyblue}')
        self.tblwgtInput.setFrameStyle(QtWidgets.QFrame.Box | QtWidgets.QFrame.Plain)
        #构建表格插入数据
        for i in range(row):
            for j in range(col-1):
                temp_data = res[i][j]
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

    def cmbDpmt_activated(self):
        """筛选生产编号"""
        self.cmbNO.clear()
        m_dm = self.cmbDpmt.currentText()
        if m_dm == '金工车间':
            m_where = "(机加部门 is Null or 机加部门 = '金工车间') \
                and 锻造状态 is not Null and (机加状态 is Null or 机加状态 = '部分机加')"
        else:
            m_where = "机加部门 = '%s' and 锻造状态 is not Null and (机加状态 is Null or 机加状态 = '部分机加')"%m_dm
        res, cur = mymdb.fetchall(field='distinct 生产编号', table='order_list', where=m_where)
        # print(res)
        if res is None:
            return
        no_lst = [tup[0] for tup in res]
        self.cmbNO.addItems(no_lst)

    def selectItemsDpmt(self):
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
                # self.mymdb = myMdb()
                result = mymdb.fetchall(field='姓名', table='employee', where="职务='车工'")
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
        """保存机加进度录入"""
        rows = self.tblwgtInput.rowCount()  # 总行数
        cols = self.tblwgtInput.columnCount()  # 总列数
        filed = '生产编号,序号,机加部门,机加数量,机加日期'
        preSql = "insert into 机加记录 ({})".format(filed)
        subSql = "values(%s, %s, %s, %s, %s)"
        sql = preSql+subSql  # 前后相加成一个完整的sql
        sql_1 = "INSERT INTO order_list (生产编号,序号,机加部门,已机加数,机加状态) VALUES(%s, %s, %s, %s, %s)  \
                ON DUPLICATE KEY UPDATE 机加部门=VALUES(机加部门),已机加数=VALUES(已机加数),机加状态=VALUES(机加状态)"
        # print(sql)
        param = []  # 建传入值的列表
        param_1 = []
        for row in range(rows):
            # 判断序号None或空值时退出循环
            if self.tblwgtInput.item(row, 0) is None or self.tblwgtInput.item(row, 0).text() == "":
                break
            # 判断机加数量None或空值时pass
            if self.tblwgtInput.item(row, 8) is None or self.tblwgtInput.item(row, 8).text() == "":
                continue
            else:
                value_list = []
                m_NO = self.cmbNO.currentText()
                value_list.append(m_NO)
                value_list.append(self.tblwgtInput.item(row, 0).text())
                value_list.append(self.cmbDpmt.currentText())
                value_list.append(self.tblwgtInput.item(row, 8).text())
                value_list.append(self.tblwgtInput.item(row, 9).text())
                param.append(value_list)

                # 已完成数
                value_list_1 = []
                m_xh = self.tblwgtInput.item(row, 0).text()  # 序号
                m_state = self.tblwgtInput.item(row, 10).text()  # 机加状态

                if self.tblwgtInput.item(row, 6).text() == 'None':  # 已机加数=none时设为0
                    m_cmpt = 0
                else:
                    m_cmpt = int(self.tblwgtInput.item(row, 6).text())
                m_cmp = int(self.tblwgtInput.item(row, 8).text())  # 机加数量
                m_all = m_cmpt + m_cmp  # 完成总数
                value_list_1.append(m_NO)
                value_list_1.append(m_xh)
                value_list_1.append(self.cmbDpmt.currentText())
                value_list_1.append(m_all)
                value_list_1.append(m_state)
                param_1.append(value_list_1)
                # 更新-->订单生产状态
                # mymdb.update(
                #     table='order_list',
                #     生产状态="'"+m_state+"'",
                #     where="生产编号="+m_NO+" and 序号="+m_xh)

        # 数据库操作-->写入机加完成数据==============================================================
        rowcount = mymdb.insert_many(sql, param)
        # 更新-->机加状态
        mymdb.updateAll(sql_1, param_1)
        QMessageBox.about(self, "保存成功", "保存了"+str(rowcount)+"条机加记录")
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
                forge_state = '机加完成'
            if m_all < m_order:
                forge_state = '部分机加'
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


class Forge(QWidget, Ui_wgtInput):
    """锻造类"""
    def __init__(self, parent=None):
        super(Forge, self).__init__(parent)
        self.setupUi(self)
        # self.mymdb = myMdb()
        # self.queryProductionNumber()

        # 隐藏不需要的控件
        self.btn_query.hide()
        self.cmbWork.hide()
        self.comboBox_2.hide()
        self.cmbDpmt.addItems(['1T','2T','压机','锻造外协'])
        # 生产编号列表框变动信号连接
        self.cmbNO.currentIndexChanged.connect(self.cmbNO_currentIndexChanged)
        self.cmbDpmt.currentIndexChanged.connect(self.cmbDpmt_currentIndexChanged)

    def cmbNO_currentIndexChanged(self):
        """查询未锻造完成的锻造明细"""
        self.clearEntryData()
        m_no = self.cmbNO.currentText()
        if m_no == '':
            return
        res = mymdb.fetchall(
            table='锻造', 
            field='序号,名称,制造标准,锻造规格,材质,数量,已锻造数,锻造部门',
            where='生产编号={}'.format(m_no))
        # col_lst = [tup[0] for tup in res[1].description]
        # 删除列表中不需要的数据
        # del col_lst[0:2]
        data = [tup[0] for tup in res[0]]
        row = len(data)  # 获得data的行数
        vol = len(res[0][0])
        # self.tblwgtInput = Qtblwgt(row, vol)
        self.tblwgtInput.setColumnCount(11)
        self.tblwgtInput.setRowCount(row)
        font = QtGui.QFont('微软雅黑', 9)
        self.tblwgtInput.horizontalHeader().setFont(font)  # 设置行表头字体
        col_lst = ['序号','名称','制造标准','锻造规格','材质','订单数量','已锻造数','锻造部门','锻造数量','锻造日期','锻造状态']
        self.tblwgtInput.setHorizontalHeaderLabels(col_lst)  # 设置标题
        self.tblwgtInput.setToolTip("锻造明细")
        self.tblwgtInput.horizontalHeader().setStyleSheet(
            'QHeaderView::section{background:skyblue}')
        self.tblwgtInput.setFrameStyle(QtWidgets.QFrame.Box | QtWidgets.QFrame.Plain)
        #构建表格插入数据
        for i in range(row):  # i到row-1的数量
            for j in range(vol):  # 第2列开始
                temp_data = res[0][i][j]
                data3 = QTableWidgetItem(str(temp_data))
                data3.setFlags(QtCore.Qt.NoItemFlags)  # 禁止指定列编辑
                self.tblwgtInput.setItem(i, j, data3)
            # 加入当天日期为完成日期
            m_date = QTableWidgetItem(time.strftime("%Y-%m-%d", time.localtime()))
            m_date.setFlags(QtCore.Qt.NoItemFlags)
            self.tblwgtInput.setItem(i, 9, m_date)
        # 适应列宽/行高/最后一列对齐边框
        self.tblwgtInput.resizeColumnsToContents()
        self.tblwgtInput.resizeRowsToContents()
        self.tblwgtInput.horizontalHeader().setStretchLastSection(True)
        # 开启单元格变更信号
        self.tblwgtInput.cellChanged.connect(self.input_cellChanged)

    def cmbDpmt_currentIndexChanged(self):
        """筛选未锻造完成的生产编号"""
        self.cmbNO.clear()
        m_dpmt = self.cmbDpmt.currentText()
        res = mymdb.fetchall(
            field='distinct 生产编号', table='锻造', where="锻造状态!='全部完成' and 锻造部门='{}'".format(m_dpmt))
        if res is None:
            return
        no_lst = [tup[0] for tup in res[0]]
        self.cmbNO.addItems(no_lst)

    @pyqtSlot()
    def on_pbtnSave_clicked(self):
        """保存锻造完工录入"""
        if self.tblwgtInput.item(0, 7) is None or self.tblwgtInput.item(0, 7).text() == "":
            QMessageBox.warning(self, "警告", "锻件交期不能空")
            return

        rows = self.tblwgtInput.rowCount()  # 总行数
        cols = self.tblwgtInput.columnCount()  # 总列数
        filed = '生产编号,序号,锻造部门,锻造数量,锻造日期'
        preSql = "insert into 锻造记录 ({})".format(filed)
        subSql = "values(%s, %s, %s, %s, %s)"
        sql = preSql+subSql  # 前后相加成一个完整的sql
        sql_1 = "INSERT INTO 锻造 (生产编号,序号,已锻造数,锻造日期,锻造状态) VALUES(%s, %s, %s, %s, %s)  \
                ON DUPLICATE KEY UPDATE 已锻造数=VALUES(已锻造数),锻造日期=VALUES(锻造日期),锻造状态=VALUES(锻造状态)"
        # print(sql)
        param = []  # 建传入值的列表
        param_1 = []
        for row in range(rows):
            # 判断序号None或空值时退出循环
            if self.tblwgtInput.item(row, 0) is None or self.tblwgtInput.item(row, 0).text() == "":
                break
            # 判断锻造数量None或空值时pass
            if self.tblwgtInput.item(row, 8) is None or self.tblwgtInput.item(row, 8).text() == "":
                continue
            else:
                value_list = []
                m_bjdh = self.cmbNO.currentText()  # 报价单号
                value_list.append(m_bjdh)
                for col in (0, 7, 8, 9):
                    value_list.append(self.tblwgtInput.item(row, col).text())
                param.append(value_list)
                # 计算已锻造数,建列表批量更新数据库
                value_list_1 = []
                m_xh = self.tblwgtInput.item(row, 0).text()  # 序号
                m_state = self.tblwgtInput.item(row, 10).text()  # 锻造状态
                if self.tblwgtInput.item(row, 6).text() == 'None':  # 已锻造数=none时设为0
                    m_cmpt = 0
                else:
                    m_cmpt = int(self.tblwgtInput.item(row, 6).text())
                m_cmp = int(self.tblwgtInput.item(row, 8).text())  # 锻造数量
                m_all = m_cmpt + m_cmp  # 完成总数
                value_list_1.append(m_bjdh)
                value_list_1.append(m_xh)
                value_list_1.append(m_all)
                value_list_1.append(self.tblwgtInput.item(row, 9).text())
                value_list_1.append(m_state)
                param_1.append(value_list_1)
                # 更新-->订单生产状态
                # mymdb.update(
                #     table='order_list',
                #     生产状态="'"+m_state+"'",
                #     where="生产编号="+m_bjdh+" and 序号="+m_xh)
                mymdb.update(
                    table='order_list',
                    生产状态="{}",
                    where="生产编号={} and 序号={}").format(m_state, m_bjdh, m_xh)

        # 数据库操作==============================================================
        rowcount = mymdb.insert_many(sql, param)
        # 更新-->锻造状态
        mymdb.updateAll(sql_1, param_1)
        QMessageBox.about(self, "保存成功", "保存了"+str(rowcount)+"条锻造记录")
        self.clearEntryData()
        # self.queryProductionNumber()

    # 输入完成数量后判断数值是否超过订单数量
    def input_cellChanged(self, row):
        """输入完成数量后计算判断数量是否正确"""
        self.tblwgtInput.blockSignals(True)  # 暂停单元格修改信号
        m_order = int(self.tblwgtInput.item(row, 5).text())  # 订单数量
        if self.tblwgtInput.item(row, 6).text() == 'None':  # 已完成数=none时设为0
            m_cmpt = 0
        else:
            m_cmpt = int(self.tblwgtInput.item(row, 6).text())
        m_cmp = int(self.tblwgtInput.item(row, 8).text())  # 完成数量
        m_all = m_cmpt + m_cmp  # 完成总数
        if m_all > m_order or m_cmp < 0:
            QMessageBox.warning(self, "警告", "锻造数量错误,请检查!")
            self.tblwgtInput.setItem(row, 8, QTableWidgetItem(0))
            self.tblwgtInput.blockSignals(False)  # 开启单元格修改信号
            return
        if m_all == m_order:
            forge_state = '锻造完成'
        if m_all < m_order:
            forge_state = '部分锻造'
        self.tblwgtInput.item(row, 8).setForeground(QBrush(QColor(255, 0, 0)))
        # 更新锻造状态
        self.tblwgtInput.setItem(row, 10, QTableWidgetItem(forge_state))
        self.tblwgtInput.blockSignals(False)  # 开启单元格修改信号

    def clearEntryData(self):
        try:
            self.tblwgtInput.cellChanged.disconnect()
        except:
            pass
        finally:
            self.tblwgtInput.clearContents()


class Plan(QWidget, Ui_wgt_plan):
    """计划排产类"""
    def __init__(self, parent=None):
        super(Plan, self).__init__(parent)
        self.setupUi(self)
        self.initPlan()

        # 锻造部门下拉列表框
        self.cmbCO.insertItem(0, "选择锻造部门")
        self.cmbCO.addItem("1T")
        self.cmbCO.addItem("2T")
        self.cmbCO.addItem("压机")
        self.cmbCO.addItem("外协")
        # 加入交货日期控件
        self.dateedit = QDateEdit(QDate.currentDate(), self)
        self.dateedit.setMinimumSize(QtCore.QSize(100, 26))
        self.dateedit.setCalendarPopup(True)
        self.dateedit.setToolTip("交货日期")
        self.horizontalLayout.addWidget(self.dateedit)
        # 日期控件信号连接槽函数
        self.dateedit.dateChanged.connect(self.date_changed)
        # 列表框变色
        self.cmbCO.currentIndexChanged.connect(self.cmbCO_currentIndexChanged)
        # 查询弹窗
        # self.pbtnQuery.clicked.connect(self.opendiolog)

    def initPlan(self):
        """初始化计划排产表格"""
        # 设置订单lineedit文本框显示当前日期
        self.lineEdit_5.setText(time.strftime("%Y-%m-%d", time.localtime()))
        #设置表格设置初始100行
        self.tblwgt.setRowCount(25)
        self.tblwgt.setColumnCount(9)
        # 设置标题
        tbl_header = ['序号','名称','制造标准','锻造规格','材质','数量','备注','锻件交期','锻造部门']
        self.tblwgt.setHorizontalHeaderLabels(tbl_header)
        # 设置每格为空值
        for m_row in range(100):
            for m_col in range(9):
                item = QTableWidgetItem("")
                item.setTextAlignment(Qt.AlignHCenter|Qt.AlignVCenter)
                self.tblwgt.setItem(m_row, m_col, item)
        # self.tblwgt.resizeColumnsToContents()
        self.tblwgt.resizeRowsToContents()
        # 设置行表头字体
        font = QtGui.QFont('微软雅黑', 9)
        self.tblwgt.horizontalHeader().setFont(font)
        # 左垂直表头不显示
        self.tblwgt.verticalHeader().setVisible(False)
        # 选择多行
        self.tblwgt.setSelectionMode(QAbstractItemView.ExtendedSelection)
        # 设置表格颜色             
        self.tblwgt.horizontalHeader().setStyleSheet('QHeaderView::section{background:skyblue}')
        self.tblwgt.setFrameStyle(QtWidgets.QFrame.Box | QtWidgets.QFrame.Plain)
        # 设置文本框无边框
        styleSheet = "background:transparent;border-width:0;border-style:outset"
        self.lineEdit_1.setStyleSheet(styleSheet)
        self.lineEdit_2.setStyleSheet(styleSheet)
        self.lineEdit_3.setStyleSheet(styleSheet)
        self.lineEdit_4.setStyleSheet(styleSheet)
        self.lineEdit_5.setStyleSheet(styleSheet)

    def openPlanList(self, param):
        self.clearPlanData()
        row = len(param)  # 获得查询窗口选择数据的行数
        # 转换客户公司名称为公司代码
        # self.mymdb = myMdb()
        name = param[0][2]
        m_code = mymdb.fetchone(field='{}'.format('客户代码'),
                                table='{}'.format('客户资料表'),
                                where="公司名称 like '{}'".format(name))
        self.lineEdit_1.setText(m_code[0])
        self.lineEdit_2.setText(param[0][0])
        for i in range(row):
            for j in range(3, 10):
                temp_data = param[i][j]
                data1 = QTableWidgetItem(str(temp_data))
                self.tblwgt.setItem(i, j-3, data1)
        self.tblwgt.resizeColumnsToContents()
        count = plusColumn(self, "tblwgt", 5)
        self.lineEdit_3.setText(str(count))
        # 导入技术要求
        m_jsyq = mymdb.fetchone(field='{}'.format('技术要求'),
                                table='{}'.format('orders'),
                                where="生产编号='{}'".format(param[0][0]))
        self.textEdit.setPlainText(m_jsyq[0].replace(";", "\n"))
        # 开启单元格变更变色
        self.tblwgt.cellChanged.connect(self.tblwgt_chang)

    # 单元格加入交货期dateedit控件,已选用菜单直选法
    # def dateEdit(self):
        # self.dateedit = QDateEdit(QDate.currentDate(), self)
        # self.dateedit.setCalendarPopup(True)
        # # row = self.tblwgt.currentItem().row()
        # self.horizontalLayout.addWidget(self.dateedit)
        # self.tblwgt.setCellWidget(0, 9, self.dateedit)
        # # 日期控件信号连接槽函数
        # self.dateedit.dateChanged.connect(self.date_changed)

    # 交货日期发生改变时执行
    def date_changed(self, date):
        # 把选择日期转换为文本
        row = self.tblwgt.rowCount()
        for i in range(row):
            if self.tblwgt.item(i, 0) is None:
                break
            if self.tblwgt.item(i, 0).text() != "":
            # if self.tblwgt.item(i, 0) is None:
                txt = QTableWidgetItem(date.toString("yyyy-MM-dd"))
                self.tblwgt.setItem(i, 7, txt)

    # 保存锻造排单  还未加锻造要求??????????????????
    @pyqtSlot()
    def on_pbtnSave_clicked(self):
        """保存锻造排单"""
        if self.tblwgt.item(0, 7) is None or self.tblwgt.item(0, 7).text() == "":
            QMessageBox.warning(self, "警告", "锻件交期不能空")
            return
        if self.tblwgt.item(0, 8) is None or self.tblwgt.item(0, 8).text() == "":
            QMessageBox.about(self, "警告", "锻造部门不能空")
            return
        button = QMessageBox.question(self, "注意", "请确认无误再保存订单,\n按OK继续,按Cancel退出",
                                      QMessageBox.Ok|QMessageBox.Cancel, QMessageBox.Ok)
        if button == QMessageBox.Cancel:
            return

        # mymdb = myMdb()
        rows = self.tblwgt.rowCount()  # 总行数
        cols = self.tblwgt.columnCount()  # 总列数
        m_scbh = self.lineEdit_2.text()  # 生产编号
        filed = '客户代码,生产编号,序号,名称,制造标准,锻造规格,材质,数量,锻造备注,锻件交期,锻造部门,下单日期,锻造状态'
        preSql = "insert into 锻造 ({})".format(filed)
        subSql = "values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        sql = preSql+subSql  # 前后相加成一个完整的sql
        param = []  # 建传入值的列表
        for row in range(rows):
            if self.tblwgt.item(row, 0) is None or self.tblwgt.item(row, 0).text() == "":
                break
            else:
                m_xh = self.tblwgt.item(row, 0).text()
                # 更新订单明细-->生产状态=锻造排产
                mymdb.update(table='{}'.format('order_list'),
                             生产状态='{}'.format('锻造排产'),
                             where="生产编号='{}' and 序号='{}'".format(m_scbh, m_xh))
                value_list = []
                value_list.append(self.lineEdit_1.text())  # 客户代码
                value_list.append(self.lineEdit_2.text())  # 生产编号
                for col in range(cols):
                    # 把None和空值的数字格设为0值
                    if not self.tblwgt.item(row, col) or self.tblwgt.item(row, col).text() == "":
                        value_list.append("0")
                    else:
                        value_list.append(self.tblwgt.item(row, col).text())
                value_list.append(self.lineEdit_5.text())  # 下单日期
                value_list.append('锻造排产')  # 锻造状态
                param.append(value_list)
        # 数据库操作==============================================================
        rowcount = mymdb.insert_many(sql, param)
        if rowcount is None:
            QMessageBox.about(self, "警告", "输入数据错误,请检查")
            return
        # 更新订单-->订单状态
        # mymdb.update(table='orders', 订单状态="'锻造排单'", where="生产编号="+m_scbh)# 分批锻造保存时变更状态后,影响再次查询未排产的编号??????
        QMessageBox.about(self, "保存成功", "保存了"+str(rowcount)+"条订单记录")
        self.clearPlanData()

    #点击查询按钮事件
    @pyqtSlot()
    def on_pbtnQuery_clicked(self):
        # dialog = OpenDialog(self)
        # # '''连接子窗口的自定义信号与主窗口的槽函数'''
        # dialog.Signal_param.connect(self.openPlanList)
        # dialog.show()

        dockmain = DockMain(self)
        # '''连接子窗口的自定义信号与主窗口的槽函数'''
        dockmain.Signal_param.connect(self.openPlanList)
        dockmain.show()

    # def on_pbtnQuery_clicked(self):  # 直接查询法
        # """查询报价单-->生成生产合同明细"""
        # if self.cmbNO.currentText() in ("", "生产编号"):
        #     return
        # self.clearData()
        # self.mymdb = myMdb()
        # m_no = self.cmbNO.currentText()
        # m_co = self.cmbCO.currentText()
        # res = self.mymdb.fetchall(table='order_list', where='生产编号='+m_no)
        # data = [tup[0] for tup in res[0]]
        # row = len(data)
        # # vol = len(res[0][0])
        # self.tblwgt.setRowCount(row)
        # # 构建表格插入数据
        # gsmc = mymdb.fetchone(field='客户代码', table='客户资料表', where="公司名称 like '%"+m_co+"%'")
        # self.lineEdit_1.setText(gsmc[0])
        # self.lineEdit_2.setText(str(data[0]))
        # for i in range(row):
        #     for j in range(3, 10):
        #         temp_data = res[0][i][j]
        #         data1 = QTableWidgetItem(str(temp_data))
        #         self.tblwgt.setItem(i, j-3, data1)
        #     # 交货日期和备注
        #     self.tblwgt.setItem(i, 8, QTableWidgetItem(str(res[0][i][14])))
        #     self.tblwgt.setItem(i, 9, QTableWidgetItem(str(res[0][i][15])))
        # # 导入技术要求
        # m_jsyq = mymdb.fetchone(field='技术要求', table='orders', where='生产编号='+m_no)
        # self.textEdit.setPlainText(m_jsyq[0].replace(";", "\n"))
        # # 表格插入日期控件
        # self.dateEdit()
        # # 调整表格
        # self.tblwgt.resizeColumnsToContents()
        # self.tblwgt.resizeRowsToContents()
        # # 汇总数量
        # count_1 = plusColumn(self, "tblwgt", 5)
        # self.lineEdit_3.setText(str(count_1))
        # # 启动单元格变更事件信号
        # # 再次查询打开时,用clearData时删信号解决
        # self.tblwgt.cellChanged.connect(self.tblwgt_chang)

    # 右键菜单
    def contextMenuEvent(self, event):
        """系统自带右键菜单事件:"""
        pmenu = QMenu(self)
        insertAct = QAction(u"插入行", self.tblwgt)
        # deleteAct = QAction(u"删除行", self.TWquote)
        pmenu.addAction(insertAct)
        # pmenu.addAction(deleteAct)
        # 在鼠标光标位置显示
        pmenu.popup(QtGui.QCursor.pos())
        # pmenu.popup(self.mapToGlobal(event.pos()))
        insertAct.triggered.connect(self.add_onerow)
        # deleteAct.triggered.connect(self.ondelselect)

    def add_onerow(self):
        """当前位置插入一行"""
        self.tblwgt.blockSignals(True)  # 暂停单元格修改信号
        row = self.tblwgt.currentIndex().row()
        cols = self.tblwgt.columnCount()
        # print(cols)
        # 在row行位置插入一空行
        self.tblwgt.insertRow(row)
        # 给插入的行设置空值
        for m_col in range(cols):
            new_item = QTableWidgetItem("")
            new_item.setTextAlignment(Qt.AlignHCenter|Qt.AlignVCenter)
            self.tblwgt.setItem(row, m_col, new_item)
        self.tblwgt.blockSignals(False)  # 暂停单元格修改信号

    def cmbCO_currentIndexChanged(self):
        """选择锻造部门"""
        self.cmbCO.currentText()
        row = self.tblwgt.rowCount()
        for i in range(row):
            if self.tblwgt.item(i, 0) is None:
                break
            if self.tblwgt.item(i, 0).text() != "":
                txt = QTableWidgetItem(self.cmbCO.currentText())
                self.tblwgt.setItem(i, 8, txt)

    def tblwgt_chang(self, row, col):
        """明细修改变更事件-->红色显示修改,重新计算数量"""
        self.tblwgt.blockSignals(True)  # 暂停单元格修改信号
        txt = self.tblwgt.item(row, col).text()  # currentIndex()可以考虑
        # 字体颜色（红色）
        self.tblwgt.item(row, col).setForeground(QBrush(QColor(255, 0, 0)))
        # 背景颜色（红色）
        # self.tblwgt.item(row, col).setBackground(QBrush(QColor(255, 0, 0)))
        # 重新计算
        if col == 5:
            # 汇总列总数量,更新到lineEdit
            count_1 = plusColumn(self, "tblwgt", 5)
            self.lineEdit_3.setText(str(count_1))
        self.tblwgt.blockSignals(False)  # 启动单元格修改信号
    
    # 保存后清空数据
    def clearPlanData(self):
        # 存在信号连接就删除
        try:
            self.tblwgt.cellChanged.disconnect()
        except:
            pass
        finally:
            self.textEdit.clear()
            self.tblwgt.clearContents()
            for i in (1, 2, 3):
                exec("self.lineEdit_"+str(i)+".setText('')")


class OpenDialog(QDialog, Ui_Dialog): # 订单明细查询弹窗
    """订单明细查询弹窗"""
    Signal_param = pyqtSignal(list)

    def __init__(self, parent=None):
        super(OpenDialog, self).__init__(parent)
        self.setupUi(self)

        self.cmbState.addItem('订单状态')
        self.cmbState.addItem('签订合同')
        self.cmbState.addItem('锻造排单')
        self.cmbState.addItem('锻造完成')
        # 信号槽
        self.btnQuery.clicked.connect(self.openData)  # 按生产编号查询订单明细
        # 下拉列表框选择事件连接
        self.cmbState.currentIndexChanged.connect(self.cmbState_currentIndexChanged)
        self.cmbCO.currentIndexChanged.connect(self.cmbCO_currentIndexChanged)

    def cmbState_currentIndexChanged(self):
        """选择订单状态带出公司名称"""
        self.cmbCO.clear()
        # self.clearData()
        m_state = self.cmbState.currentText()
        res, cur = mymdb.fetchall(field='{}'.format('distinct 买方'),
                                  table='{}'.format('orders'),
                                  where="订单状态='{}'".format(m_state))
        no_lst = [tup[0] for tup in res]
        self.cmbCO.addItems(no_lst)

    def cmbCO_currentIndexChanged(self):
        """选择公司带出生产编号"""
        self.cmbNO.clear()
        # self.clearData()
        m_state = self.cmbState.currentText()
        m_group = self.cmbCO.currentText()
        res = mymdb.fetchall(field='生产编号',
                               table='orders',
                               where='买方='+"'"+m_group+"'"+" and 订单状态="+"'"+m_state+"'")
        no_lst = [tup[0] for tup in res[0]]
        self.cmbNO.addItems(no_lst)

    def openData(self):
        """点击查询订单明细"""
        if self.cmbNO.currentText() == "":
            return
        else:
            m_no = self.cmbNO.currentText()
            res = mymdb.fetchall(table='order_list', where="生产编号="+"'"+m_no+"'"+" and 生产状态='签订合同'")
        # data[1]是cur,data[0]是data数据
        data = [tup[0] for tup in res[0]]
        row = len(data)     # 获得data的行数
        # 插入表格
        self.tblwgtOrderList.setColumnCount(12)
        self.tblwgtOrderList.setRowCount(row)
        font = QFont('微软雅黑', 9)
        self.tblwgtOrderList.setToolTip("订单明细")
        self.tblwgtOrderList.horizontalHeader().setFont(font)  # 设置行表头字体
        self.tblwgtOrderList.setSelectionBehavior(QAbstractItemView.SelectRows)  # 设置整行选中
        self.tblwgtOrderList.setEditTriggers(QAbstractItemView.NoEditTriggers)   # 设置表格禁止编辑
        # 设置标题
        col_lst = ['生产编号','合同编号','公司名称','序号','名称','制造标准','规格型号','材质','数量','备注','交货日期','生产状态']
        self.tblwgtOrderList.setHorizontalHeaderLabels(col_lst)
        # 设置表格颜色             
        self.tblwgtOrderList.horizontalHeader().setStyleSheet(
                'QHeaderView::section{background:skyblue}')
        self.tblwgtOrderList.setFrameStyle(QFrame.Box | QFrame.Plain)
        # 构建表格插入数据
        for i in range(row):
            for j in range(9):
                temp_data = res[0][i][j]
                data1 = QTableWidgetItem(str(temp_data))
                self.tblwgtOrderList.setItem(i, j, data1)
                self.tblwgtOrderList.setItem(i, 9, QTableWidgetItem(str(res[0][i][13])))
                self.tblwgtOrderList.setItem(i, 10, QTableWidgetItem(str(res[0][i][15])))
                self.tblwgtOrderList.setItem(i, 11, QTableWidgetItem(str(res[0][i][16])))
        self.tblwgtOrderList.resizeColumnsToContents()  # 自适应宽度
        self.tblwgtOrderList.resizeRowsToContents()  # 自适应行高
        self.tblwgtOrderList.horizontalHeader().setStretchLastSection(True)  # 最后一列对齐边框
        # 导入技术要求
        m_jsyq = mymdb.fetchone(field='技术要求', table='orders', where='生产编号='+m_no)
        self.textEdit.setPlainText(m_jsyq[0].replace(";", "\n"))

    @pyqtSlot()
    def on_btnExport_clicked(self):
        # 创建传入值的列表
        param = []
        # 判断选择数据空就退出
        if self.tblwgtOrderList.selectedRanges() == []:
            return
        m_cols = self.tblwgtOrderList.columnCount()
        for rg in self.tblwgtOrderList.selectedRanges():
            for m_k in range(rg.topRow(), rg.bottomRow()+1):
                value_list = []
                for m_i in range(m_cols):
                    value_list.append(self.tblwgtOrderList.item(m_k, m_i).text())
                param.append(value_list)
        self.Signal_param.emit(param)  # 发射信号

        # items = self.tblwgtOrderList.selectedItems()通过item选出行号法
            # m_rows = []
            # value_list.append(items[i].text())  # items[i]根据i的位置(0,1)取
            # 循环取单元格,i.row()单元格的行号,i.text()单元格的文本
            # for i in items:
            #     if i.row() not in m_rows:
            #         m_rows.append(i.row())
            # for m_row in m_rows:
            #     value_list = []
            #     for m_col in range(m_cols):
            #         value_list.append(self.tblwgtOrderList.item(m_row, m_col).text())
            #     param.append(value_list)
