# -*- coding: utf-8 -*-

import sys
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import (QIcon, QPixmap, QFont)
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QWidget, QMenu, QApplication
from PyQt5.QtCore import (Qt, pyqtSignal, QEvent)

from tools.mysql_conn import myMdb
import tools.globaldict as gl


class DockMain(QWidget):
    """窗口停靠功能"""
    Signal_dockparam = pyqtSignal(list)  # 定义dock窗口信号用

    def __init__(self, parent=None):
        super(DockMain, self).__init__(parent)
        self.initdockmain()

        # 全局变量
        self.tbl = gl.get_value('tbl')  # 表名tbl=table
        self.tag = gl.get_value('tag')  # tag标签,报价单号or生产编号
        self.field = gl.get_value('field')  # 查询字段
        self.header = gl.get_value('header')  # 表头
        self.company = gl.get_value('company')
        # print(self.table)
        if self.tbl == 'quote':
            self.state = '状态'
        else:
            self.state = '生产状态'
        self.add_cmbState()

        # 右键菜单
        self.tablewidget.setContextMenuPolicy(Qt.ActionsContextMenu)
        self.tablewidget.addAction(QAction("全选", self, triggered=self.checkAll))
        self.tablewidget.addAction(QAction("反选", self, triggered=self.invert))

        # 信号槽
        self.btnOk.clicked.connect(self.btnOk_clicked)  # 确认选择并导出
        # 下拉列表框选择事件连接
        self.cmbNO.activated.connect(self.cmbNO_activated)
        self.cmbState.activated.connect(self.cmbState_activated)
        self.cmbGroup.activated.connect(self.cmbGroup_activated)
        # 选中行,选中复选框  信号触发要考虑,cellclicked不合理,点复选框不触发选择行,但能发射信号
        # self.tablewidget.cellClicked.connect(self.tablewidget_select)
        self.tablewidget.clicked.connect(self.tablewidget_select)

    def initdockmain(self):
        """初始化dock窗口"""
        self.dockWidget = QDockWidget(self)
        self.dockWidget.setObjectName("dockWidget")
        self.dockWidgetContents = QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.verticalLayout = QVBoxLayout(self.dockWidgetContents)
        self.verticalLayout.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setSpacing(6)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        # 修改键
        # self.btn_edit = QPushButton(self.dockWidgetContents)
        # icon2 = QIcon()
        # icon2.addPixmap(QPixmap(":/png/images/modify_24px.png"), QIcon.Normal, QIcon.Off)
        # self.btn_edit.setIcon(icon2)
        # self.btn_edit.setObjectName("btn_edit")
        # self.btn_edit.setToolTip("修改")
        # self.btn_edit.setText("修改")
        # self.horizontalLayout_2.addWidget(self.btn_edit)
        # 下拉列表框
        self.cmbState = QComboBox(self.dockWidgetContents)
        self.cmbState.setMinimumSize(QtCore.QSize(0, 26))
        self.cmbState.setObjectName("cmbState")
        self.cmbState.setToolTip("状态")
        self.horizontalLayout_2.addWidget(self.cmbState)
        self.cmbGroup = QComboBox(self.dockWidgetContents)
        self.cmbGroup.setMinimumSize(QtCore.QSize(120, 26))
        self.cmbGroup.setObjectName("cmbGroup")
        self.cmbGroup.setToolTip("公司名称")
        self.horizontalLayout_2.addWidget(self.cmbGroup)
        self.cmbNO = QComboBox(self.dockWidgetContents)
        self.cmbNO.setMinimumSize(QtCore.QSize(100, 26))
        self.cmbNO.setCurrentText("")
        self.cmbNO.setObjectName("cmbNO")
        self.cmbNO.setToolTip("编号")
        self.horizontalLayout_2.addWidget(self.cmbNO)
        # ok按钮
        self.btnOk = QPushButton(self.dockWidgetContents)
        icon3 = QIcon()
        icon3.addPixmap(QPixmap(":/myImage/images/Accept.png"), QIcon.Normal, QIcon.Off)
        self.btnOk.setIcon(icon3)
        self.btnOk.setObjectName("btnOk")
        self.btnOk.setToolTip("OK")
        self.btnOk.setText("OK")
        self.horizontalLayout_2.addWidget(self.btnOk)
        # 文本框
        # self.line_search = QLineEdit(self.dockWidgetContents)
        # self.line_search.setMinimumSize(QtCore.QSize(50, 28))
        # self.line_search.setText("")
        # self.line_search.setClearButtonEnabled(True)
        # self.line_search.setObjectName("line_search")
        # self.line_search.setToolTip("报价单号")
        # self.line_search.setPlaceholderText("输入报价单号")
        # self.horizontalLayout_2.addWidget(self.line_search)
        spacerItem1 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.horizontalLayout_2.setStretch(0, 1)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.tablewidget = QTableWidget(self.dockWidgetContents)
        self.tablewidget.setObjectName("tablewidget")
        # self.tablewidget.setColumnCount(0)
        # self.tablewidget.setRowCount(0)
        self.verticalLayout.addWidget(self.tablewidget)
        self.dockWidget.setWidget(self.dockWidgetContents)
        # self.addDockWidget(QtCore.Qt.DockWidgetArea(4), self.dockWidget)

        font = QFont('微软雅黑', 9)
        self.tablewidget.setToolTip("查询")
        self.tablewidget.horizontalHeader().setFont(font)  # 设置行表头字体
        self.tablewidget.verticalHeader().setVisible(False)  # 左垂直表头不显示
        self.tablewidget.setSelectionBehavior(QAbstractItemView.SelectRows)  # 设置选择行为，以行为单位
        self.tablewidget.setSelectionMode(QAbstractItemView.SingleSelection)  # 设置选择模式，选择单行
        # 设置表格颜色             
        self.tablewidget.horizontalHeader().setStyleSheet(
            'QHeaderView::section{background:skyblue}')
        self.tablewidget.setEditTriggers(QAbstractItemView.NoEditTriggers)   # 设置表格禁止编辑
        self.tablewidget.setFrameStyle(QFrame.Box | QFrame.Plain)

    def add_cmbState(self):
        """列表框添加生产状态"""
        self.cmbNO.clear()
        # self.clearData()
        mymdb = myMdb()
        res = mymdb.fetchall(field='distinct {}'.format(self.state), table='{}'.format(self.tbl))
        m_st = [tup[0] for tup in res[0]]
        try:
            m_st.remove(None)  # 删除空值
        finally:
            self.cmbState.insertItem(0, "选择状态")
            self.cmbState.addItems(m_st)

    def cmbState_activated(self):
        """选择状态带出公司代码"""
        self.cmbGroup.clear()
        # self.cmb_NO.clear()
        mdb = myMdb()
        m_stt = self.cmbState.currentText()
        if m_stt == '':
            return
        else:
            res = mdb.fetchall(field='distinct {}'.format(self.company),
                               table='{}'.format(self.tbl),
                               where="{}='{}'".format(self.state, m_stt))
        m_st = [tup[0] for tup in res[0]]
        self.cmbGroup.addItems(m_st)

    def cmbGroup_activated(self):
        """选择代码带出编号"""
        self.cmbNO.clear()
        mdb = myMdb()
        m_stt = self.cmbState.currentText()
        m_cmpn = self.cmbGroup.currentText()
        res = mdb.fetchall(field='distinct {}'.format(self.tag),
                           table='{}'.format(self.tbl),
                           where="{}='{}' and {}='{}'".format(self.company, m_cmpn, self.state, m_stt))
        m_no = [tup[0] for tup in res[0]]
        self.cmbNO.addItems(m_no)

    def cmbNO_activated(self):
        """选中编号根据生产编号/发货状态不等于发货完成查询"""
        self.tablewidget.clearContents()
        m_stt = self.cmbState.currentText()  # 状态
        m_no = self.cmbNO.currentText()  # 编号
        where = '{}={}'.format(self.tag, m_no)
        # where = "生产编号='{}' and (发货状态!='{}' or 发货状态 is Null)".format(m_no, '发货完成')
        if self.cmbNO.currentText() == "":
            return
        else:
            mymdb = myMdb()
            res, cur = mymdb.fetchall(field=self.field, table=self.tbl, where=where)
        col_lst = [tup[0] for tup in cur.description]
        data = [tup[0] for tup in res]
        row = len(data)     # 获得data的行数
        vol = len(res[0])  # 获得data的列数
        # 插入表格
        self.tablewidget.setColumnCount(vol)
        self.tablewidget.setRowCount(row)
        # 设置标题
        self.tablewidget.setHorizontalHeaderLabels(col_lst)

        # 构建表格插入数据
        for i in range(row):
            for j in range(vol):
                temp_data = res[i][j]
                data1 = QTableWidgetItem(str(temp_data))
                if j == 0:
                    data1.setCheckState(Qt.Unchecked)
                self.tablewidget.setItem(i, j, data1)
        # 适应宽度/高度/对齐边框
        self.tablewidget.resizeColumnsToContents()
        # self.tablewidget.resizeRowsToContents()
        self.tablewidget.horizontalHeader().setStretchLastSection(True)

    def checkAll(self):
        """右键菜单全选"""
        m_row = self.tablewidget.rowCount()
        for row in range(m_row):
            m_data = self.tablewidget.item(row, 0).text()
            data = QTableWidgetItem(str(m_data))
            data.setCheckState(Qt.Checked)
            self.tablewidget.setItem(row, 0, data)

    def invert(self):
        """右键菜单反选"""
        m_row = self.tablewidget.rowCount()
        for row in range(m_row):
            m_data = self.tablewidget.item(row, 0).text()
            data = QTableWidgetItem(str(m_data))
            if self.tablewidget.item(row, 0).checkState() == Qt.Checked:
                data.setCheckState(Qt.Unchecked)
            else:
                data.setCheckState(Qt.Checked)
            self.tablewidget.setItem(row, 0, data)

    def tablewidget_select(self):  #???????????????????????
        """点击表格选中复选框,已选中状态改不选
        存在点击复选框,选中行不变化,选中状态变化的情况.行选和框选不协同
        信号触发存在问题"""
        # row = self.tablewidget.currentIndex().row()
        row = self.tablewidget.currentRow()
        # col = self.tablewidget.currentColumn()
        if row == -1:  # 防止第一次没选择中行时,h是-1的问题.
            return
        m_data = self.tablewidget.item(row, 0).text()
        data = QTableWidgetItem(str(m_data))
        if self.tablewidget.item(row, 0).checkState() == Qt.Checked:
            data.setCheckState(Qt.Unchecked)
        else:
            data.setCheckState(Qt.Checked)
        self.tablewidget.setItem(row, 0, data)

    def btnOk_clicked(self):
        """选择编号发射信号 1自定义信号,2设全局变量"""
        # 创建导出列表
        param = []
        rows = self.tablewidget.rowCount()
        cols = self.tablewidget.columnCount()
        # 判断复选框的选中状态
        for m_j in range(rows):
            if self.tablewidget.item(m_j, 0).checkState() == Qt.Checked:  # 或者== 2
                m_list = []
                for m_i in range(cols):
                    m_list.append(self.tablewidget.item(m_j, m_i).text())
                param.append(m_list)
        if param == []:
            QMessageBox.about(self, "注意", "数据未选择,请检查!")
            return
        # 发射信号
        self.Signal_dockparam.emit(param)
        self.tablewidget.clearContents()
        self.dockWidget.close()

        # items = self.tablewidget.selectedItems()通过item选出行号法
            # m_rows = []
            # value_list.append(items[i].text())  # items[i]根据i的位置(0,1)取
            # 循环取单元格,i.row()单元格的行号,i.text()单元格的文本
            # for i in items:
            #     if i.row() not in m_rows:
            #         m_rows.append(i.row())
            # for m_row in m_rows:
            #     value_list = []
            #     for m_col in range(m_cols):
            #         value_list.append(self.tablewidget.item(m_row, m_col).text())
            #     param.append(value_list)
