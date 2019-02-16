# -*- coding: utf-8 -*-

import sys
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import (QIcon, QPixmap, QFont)
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QWidget, QMenu, QApplication
from PyQt5.QtCore import (Qt, pyqtSignal, QEvent)

from tools.mysql_conn import myMdb


class DockMain(QWidget):
    """窗口停靠功能"""
    Signal_dockparam = pyqtSignal(list)  # 定义dock窗口信号用

    def __init__(self):
        super(DockMain, self).__init__()
        self.initdockmain()
        self.add_cmb_state()

        # 右键菜单
        self.tablewidget.setContextMenuPolicy(Qt.ActionsContextMenu)
        self.tablewidget.addAction(QAction("全选", self, triggered=self.checkAll))
        self.tablewidget.addAction(QAction("反选", self, triggered=self.invert))

        # 信号槽
        self.cmb_NO.activated.connect(self.cmb_NO_activated)
        self.btn_ok.clicked.connect(self.btn_ok_clicked)  # 确认选择并导出
        # 下拉列表框选择事件连接
        self.cmb_state.activated.connect(self.cmb_state_activated)
        self.cmb_group.activated.connect(self.cmb_group_activated)
        # 选中行,选中复选框
        self.tablewidget.cellClicked.connect(self.tablewidget_select)

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
        self.cmb_state = QComboBox(self.dockWidgetContents)
        self.cmb_state.setMinimumSize(QtCore.QSize(0, 26))
        self.cmb_state.setObjectName("cmb_state")
        self.cmb_state.setToolTip("生产状态")
        self.horizontalLayout_2.addWidget(self.cmb_state)
        self.cmb_group = QComboBox(self.dockWidgetContents)
        self.cmb_group.setMinimumSize(QtCore.QSize(120, 26))
        self.cmb_group.setObjectName("cmb_group")
        self.cmb_group.setToolTip("公司名称")
        self.horizontalLayout_2.addWidget(self.cmb_group)
        self.cmb_NO = QComboBox(self.dockWidgetContents)
        self.cmb_NO.setMinimumSize(QtCore.QSize(100, 26))
        self.cmb_NO.setCurrentText("")
        self.cmb_NO.setObjectName("cmb_NO")
        self.cmb_NO.setToolTip("编号")
        self.horizontalLayout_2.addWidget(self.cmb_NO)
        # ok按钮
        self.btn_ok = QPushButton(self.dockWidgetContents)
        icon3 = QIcon()
        icon3.addPixmap(QPixmap(":/myImage/images/Accept.png"), QIcon.Normal, QIcon.Off)
        self.btn_ok.setIcon(icon3)
        self.btn_ok.setObjectName("btn_ok")
        self.btn_ok.setToolTip("OK")
        self.btn_ok.setText("OK")
        self.horizontalLayout_2.addWidget(self.btn_ok)
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

    def add_cmb_state(self):
        """列表框添加生产状态"""
        self.cmb_NO.clear()
        # self.clearData()
        mymdb = myMdb()
        res, cur = mymdb.fetchall(field='distinct {}'.format('生产状态'),
                                  table='{}'.format('order_list'))
        m_st = [tup[0] for tup in res]
        self.cmb_state.insertItem(0, "选择生产状态")
        self.cmb_state.addItems(m_st)

    def cmb_state_activated(self):
        """选择状态带出公司代码"""
        self.cmb_group.clear()
        # self.cmb_NO.clear()
        mymdb = myMdb()
        m_state = self.cmb_state.currentText()
        res, cur = mymdb.fetchall(field='distinct {}'.format('买方'),
                                  table='{}'.format('order_list'),
                                  where="生产状态='{}'".format(m_state))
        m_st = [tup[0] for tup in res]
        self.cmb_group.addItems(m_st)

    def cmb_group_activated(self):
        """选择代码带出编号"""
        self.cmb_NO.clear()
        mymdb = myMdb()
        m_state = self.cmb_state.currentText()
        m_group = self.cmb_group.currentText()
        res, cur = mymdb.fetchall(field='distinct {}'.format('生产编号'),
                                  table='{}'.format('order_list'),
                                  where="买方='{}' and 生产状态='{}'".format(m_group, m_state))
        m_gp = [tup[0] for tup in res]
        self.cmb_NO.addItems(m_gp)

    def cmb_NO_activated(self):
        """选中编号根据生产编号/发货状态不等于发货完成查询"""
        self.tablewidget.clearContents()
        mymdb = myMdb()
        m_state = self.cmb_state.currentText()  # 状态
        m_no = self.cmb_NO.currentText()  # 编号
        field = '{}'.format('买方,合同编号,生产编号,序号,名称,制造标准,规格型号,材质,数量,工作令号,件号,已发货数,质保书,生产状态')
        table = '{}'.format('order_list')
        where = "生产编号='{}' and (发货状态!='{}' or 发货状态 is Null)".format(m_no, '发货完成')
        if self.cmb_NO.currentText() == "":
            return
        else:
            res, cur = mymdb.fetchall(field=field, table=table, where=where)
        col_lst = [tup[0] for tup in cur.description]
        data = [tup[0] for tup in res]
        row = len(data)     # 获得data的行数
        vol = len(res[0])  # 获得data的列数
        # 插入表格
        self.tablewidget.setColumnCount(vol)
        self.tablewidget.setRowCount(row)
        font = QFont('微软雅黑', 9)
        self.tablewidget.setToolTip("查询")
        self.tablewidget.horizontalHeader().setFont(font)  # 设置行表头字体
        self.tablewidget.verticalHeader().setVisible(False)  # 左垂直表头不显示
        self.tablewidget.setSelectionMode(QAbstractItemView.SingleSelection)  # 只能选择单行
        # 设置标题
        self.tablewidget.setHorizontalHeaderLabels(col_lst)
        # 设置表格颜色             
        self.tablewidget.horizontalHeader().setStyleSheet(
            'QHeaderView::section{background:skyblue}')
        self.tablewidget.setEditTriggers(QAbstractItemView.NoEditTriggers)   # 设置表格禁止编辑
        self.tablewidget.setSelectionBehavior(QAbstractItemView.SelectRows)  # 设置整行选中
        self.tablewidget.setFrameStyle(QFrame.Box | QFrame.Plain)
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
        存在点击复选框,选中行不变化,选中状态变化的情况"""
        h = self.tablewidget.currentIndex().row()
        m_data = self.tablewidget.item(h, 0).text()
        data = QTableWidgetItem(str(m_data))
        if self.tablewidget.item(h, 0).checkState() == Qt.Checked:
            data.setCheckState(Qt.Unchecked)
        else:
            data.setCheckState(Qt.Checked)
        self.tablewidget.setItem(h, 0, data)

    def btn_ok_clicked(self):
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
