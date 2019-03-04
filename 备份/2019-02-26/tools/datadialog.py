# -*- coding: utf-8 -*-

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from tools.mysql_conn import myMdb


class DateDialog(QDialog):
    Signal_No = pyqtSignal(str, str)

    def __init__(self, parent=None):
        super(DateDialog, self).__init__(parent)
        self.setWindowTitle('查询子窗口')

        self.verticalLayout = QVBoxLayout(self)
        self.verticalLayout.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setSpacing(6)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        # 修改键
        self.btn_edit = QPushButton()
        icon2 = QIcon()
        icon2.addPixmap(QPixmap(":/png/images/modify_24px.png"), QIcon.Normal, QIcon.Off)
        self.btn_edit.setIcon(icon2)
        self.btn_edit.setObjectName("btn_edit")
        self.btn_edit.setToolTip("修改")
        self.btn_edit.setText("修改")
        self.horizontalLayout_2.addWidget(self.btn_edit)
        # 下拉列表框
        self.cbo_state = QComboBox(self)
        self.cbo_state.setMinimumSize(QSize(0, 26))
        self.cbo_state.setObjectName("cbo_state")
        self.cbo_state.setToolTip("状态")
        self.cbo_state.addItem(QIcon(":/myImage/images/loading.png"), '待审核')
        # self.cbo_state.setStyleSheet("QComboBox{color:red;}")
        self.cbo_state.addItem(QIcon(":/myImage/images/Accept.png"), '审核通过')
        self.cbo_state.addItem(QIcon(":/myImage/images/stop.ico"), '退回修改')
        self.horizontalLayout_2.addWidget(self.cbo_state)
        self.cbo_group = QComboBox()
        self.cbo_group.setMinimumSize(QSize(120, 26))
        self.cbo_group.setObjectName("cbo_group")
        self.cbo_group.setToolTip("公司名称")
        self.horizontalLayout_2.addWidget(self.cbo_group)
        self.cbo_filter = QComboBox()
        self.cbo_filter.setMinimumSize(QSize(100, 26))
        self.cbo_filter.setCurrentText("")
        self.cbo_filter.setObjectName("cbo_filter")
        self.cbo_filter.setToolTip("报价单号")
        self.horizontalLayout_2.addWidget(self.cbo_filter)
        # 查询按钮
        self.btn_query = QPushButton()
        icon3 = QIcon()
        icon3.addPixmap(QPixmap(":/png/images/file_manager.png"), QIcon.Normal, QIcon.Off)
        self.btn_query.setIcon(icon3)
        self.btn_query.setObjectName("btn_query")
        self.btn_query.setToolTip("查询")
        self.btn_query.setText("查询")
        self.horizontalLayout_2.addWidget(self.btn_query)
        # 文本框
        # self.line_search = QLineEdit()
        # self.line_search.setMinimumSize(QSize(50, 28))
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
        self.tablewidget = QTableWidget()
        self.tablewidget.setObjectName("tablewidget")
        self.tablewidget.setColumnCount(0)
        self.tablewidget.setRowCount(0)
        self.verticalLayout.addWidget(self.tablewidget)

        # 使用两个button(ok和cancel)分别连接accept()和reject()槽函数
        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        self.verticalLayout.addWidget(buttons)

        # 信号槽
        self.btn_query.clicked.connect(self.dlg_data)
        self.tablewidget.itemClicked.connect(self.tablewidget_itemClicked)  # 点击清单,显示选择的明细
        # 下拉列表框选择事件连接
        self.cbo_state.currentIndexChanged.connect(self.cbo_state_currentIndexChanged)
        self.cbo_group.currentIndexChanged.connect(self.cbo_group_currentIndexChanged)

    #     self.datetime_emit.dateTimeChanged.connect(self.emit_signal)
    def cbo_state_currentIndexChanged(self):
        """选择审核状态带出公司名称"""
        self.cbo_group.clear()
        # self.clearData()
        m_state = self.cbo_state.currentText()
        res = myMdb().fetchall(field='distinct 公司名称',
                                table='报价基本信息',
                                where='状态='+"'"+m_state+"'")
        no_lst = [tup[0] for tup in res[0]]
        self.cbo_group.insertItem(0, "选择公司名称")
        self.cbo_group.addItems(no_lst)

    def cbo_group_currentIndexChanged(self):
        """选择公司带出报价单号"""
        self.cbo_filter.clear()
        # self.clearData()
        m_state = self.cbo_state.currentText()
        m_group = self.cbo_group.currentText()
        res = myMdb().fetchall(field='报价单号',
                               table='报价基本信息',
                               where='公司名称='+"'"+m_group+"'"+" and 状态="+"'"+m_state+"'")
        no_lst = [tup[0] for tup in res[0]]
        self.cbo_filter.addItems(no_lst)

    def dlg_data(self):
        """点击查询-->查询报价目录"""
        m_state = self.cbo_state.currentText()
        if self.cbo_filter.currentText() == "":
            res = myMdb().fetchall(table='报价基本信息', where="状态='待审核'")
        else:
            m_no = self.cbo_filter.currentText()
            res = myMdb().fetchall(table='报价基本信息',
                                    where="报价单号="+"'"+m_no+"'")
        if res[0] == ():
            return
        # data[1]是cur,data[0]是data数据
        col_lst = [tup[0] for tup in res[1].description]
        data = [tup[0] for tup in res[0]]
        row = len(data)     # 获得data的行数
        vol = len(res[0][0])  # 获得data的列数.cur.description或len(data[0])
        # print(data[0])
        # 插入表格
        # self.tableWidget = QTableWidget(row, vol)             # 设置row行vol列的表格
        self.tablewidget.setColumnCount(vol)
        self.tablewidget.setRowCount(row)
        font = QFont('微软雅黑', 9)
        self.tablewidget.setToolTip("查询")
        self.tablewidget.horizontalHeader().setFont(font)      # 设置行表头字体
        self.tablewidget.verticalHeader().setVisible(False)    # 左垂直表头不显示
        self.tablewidget.setSelectionMode(QAbstractItemView.SingleSelection)  #只能选择单行
        # 设置标题
        self.tablewidget.setHorizontalHeaderLabels(col_lst)
        # 设置表格颜色             
        self.tablewidget.horizontalHeader().setStyleSheet(
                'QHeaderView::section{background:skyblue}')
        self.tablewidget.setEditTriggers(QAbstractItemView.NoEditTriggers)   # 设置表格禁止编辑
        self.tablewidget.setSelectionBehavior(QAbstractItemView.SelectRows)  # 设置整行选中
        self.tablewidget.setFrameStyle(QFrame.Box | QFrame.Plain)
        # 构建表格插入数据
        for i in range(row):                                      # i到row-1的数量
            for j in range(vol):
                temp_data = res[0][i][j]                            # 临时记录，不能直接插入表格
                data1 = QTableWidgetItem(str(temp_data))          # 转换后可插入表格
                self.tablewidget.setItem(i, j, data1)
        # self.tableWidget.resizeColumnsToContents()             # 自适应宽度
        self.tablewidget.resizeRowsToContents()                  # 自适应行高,放最后可以等数据写入后自动适应表格数据宽度
        self.tablewidget.horizontalHeader().setStretchLastSection(True)  # 最后一列对齐边框

    def tablewidget_itemClicked(self):  #还可以考虑全局变量
        h = self.tablewidget.currentIndex().row()
        bjdh = self.tablewidget.item(h, 1).text()
        # 窗口第6列的值
        qte_date = self.tablewidget.item(h, 5).text()
        # print('bjdh='+str(bjdh))
        self.Signal_No.emit(bjdh, qte_date)  # 发射信号
