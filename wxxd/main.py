# -*- coding: utf-8 -*-

import sys, os
# sys.path.append("..")
# sys.path.append("../lib") 添加上级路径
# from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QFileDialog
from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

# import pymysql
# 天气模块
from urllib.request import urlopen
from bs4 import BeautifulSoup
# 销售
from ui.Ui_mainwindow import Ui_MainWindow
from 查询 import *
from ui.Ui_首页 import Ui_First_Form
from sale.sale import Quote, QuoteExamine, Examine, Order, AdjustPrice
from ui.Ui_quote_check import Ui_Quote_check
# 生产
from produce.produce import *
from quality.qa import *

from tools.datadialog import DateDialog  # 查询子窗口
from tools.mysql_conn import myMdb

class Main(QMainWindow, Ui_MainWindow):
    # Signal_OneParameter = pyqtSignal(str)  # 定义dock窗口信号用

    def __init__(self, parent=None):
        super(Main, self).__init__(parent)
        self.setupUi(self)
        self.machine = Inspection()
        self.setCentralWidget(self.machine)

        # 启动页图像
        # self.imageLabel = QLabel()
        # self.imageLabel.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        # self.image = QImage()
        # if self.image.load("./wxxd/images/20191.jpg"):
        #     self.imageLabel.setPixmap(QPixmap(QPixmap.fromImage(self.image)))
        #     # self.resize(self.image.width(), self.image.height())
        # self.setCentralWidget(self.imageLabel)
        self.statusBar.showMessage('欢迎某某某登录星达ERP') # 屏幕左下状态栏显示提示信息

    # def paintEvent(self, event):
        # """窗口背景图片"""
        # painter = QPainter(self)
        # pixmap = QPixmap("./wxxd/images/2019.jpg")
        # painter.drawPixmap(self.rect(), pixmap)

    @pyqtSlot()
    def on_actionHomepage_triggered(self): # 工作-->首页
        self.firstform = FirstForm()
        self.setCentralWidget(self.firstform)

    @pyqtSlot()
    def on_actionQuote_triggered(self): # 工作-->销售-->报价
        self.quote = Quote()
        self.setCentralWidget(self.quote)

    @pyqtSlot()
    def on_actionAdjust_triggered(self): # 工作-->销售-->调价
        self.adjustprice = AdjustPrice()
        self.setCentralWidget(self.adjustprice)

    @pyqtSlot()
    def on_actionOrder_triggered(self): # 工作-->销售-->订单
        self.order = Order()
        self.setCentralWidget(self.order)

    @pyqtSlot()
    def on_actionCheck_triggered(self): # 工作-->销售-->报价审核
        self.examine = Examine()
        self.setCentralWidget(self.examine)
        # 连接审核修改记录信号到状态栏
        self.examine.Signal_xgjl.connect(self.statusbar_info)

    def statusbar_info(self, record):  # 状态栏信息
        self.statusBar.showMessage(record)

    @pyqtSlot()
    def on_actionziyuan_triggered(self): # 工作-->查询-->生产进度
        """工作-->查询-->生产进度 中间窗口显示多文档界面用法"""
        # print("key=%s ,value=%s" % (item.text(0), item.text(1)))
        # self.mdi = QMdiArea()  #多文档界面
        # self.setCentralWidget(self.mdi)  #创建中央控件多文档界面要self.mdi
        sub_dlg=QMdiSubWindow()
        self.child = OpenDialog()
        sub_dlg.setWidget(self.child)
        sub_dlg.setWindowTitle("查询生产进度")
        self.mdi.addSubWindow(sub_dlg)
        sub_dlg.show()
        # self.mdi.tileSubWindows() # 平铺窗口


    # ==========================工作-->生产===============================
    @pyqtSlot()
    def on_actionPlan_triggered(self):  # 工作-->生产-->计划排产
        self.plan = Plan()
        self.setCentralWidget(self.plan)
        # self.mdiProduce()

    @pyqtSlot()
    def on_actionFgInput_triggered(self):  # 工作-->生产-->锻造-->锻造进度录入
        self.forge = Forge()
        self.setCentralWidget(self.forge)

    @pyqtSlot()
    def on_actionMchInput_triggered(self):  # 工作-->生产-->机加-->机加进度录入
        self.machine = Machine()
        self.setCentralWidget(self.machine)

    # def mdiProduce(self): # 用多窗口法,工作-->计划排产
        """多文档界面"""
        # layout = QHBoxLayout()
        # self.mdi = QMdiArea()
        # # 设置界面tabbar模式
        # self.mdi.setViewMode(QMdiArea.SubWindowView)  # 页切换模式 TabbedView模式
        # self.mdi.setFocusPolicy(Qt.ClickFocus)  # 接收鼠标单击策略
        # self.mdi.setTabPosition(QTabWidget.North)
        # self.mdi.setTabsClosable(True)  # 每个tab上放置红叉关闭某一个tab ，false:没有叉；true:有叉
        # self.mdi.setTabsMovable(True)  # 多个tab可鼠标拖动摆放顺序
        # self.mdi.setTabShape(QTabWidget.Triangular)  # tab的形状，Rounded圆角型；Triangular三角形
        # # 创建框架
        # self.frm = QFrame()
        # self.frm.setFrameStyle(QFrame.StyledPanel | QFrame.Sunken)  # 框架显示外形。
        #                # StylePanel画一个矩形面板，根据当前GUI风格的不同而不同，可被凸起或凹陷
        #                # Sunken画一个3D的凹陷显示效果
        # self.frm.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)  # 大小策略 水平和垂直都可收缩shrunk
        # self.frm.setLayout(layout)  # 设置frm的布局管理 如果此widget(frm)上已有layout,那先删除已有的,再添加新的
        # self.setCentralWidget(self.mdi)

        # # 加入判断是否已经打开?????
        # if self.mdi.subWindowList() == []:
        #     sub = QMdiSubWindow()
        #     # self.child = Produce()
        #     sub.setWidget(self.produce)
        #     sub.setWindowTitle("计划排产")
        #     self.mdi.addSubWindow(sub)
        #     # 关闭之后不会自动释放空间，需要此函数让其在close后自动释放
        #     self.mdi.setAttribute(Qt.WA_DeleteOnClose)
        #     sub.show()
        #     """设置布局来实现几个窗口跟随变化"""
        #     # self.mdi.tileSubWindows() # 平铺窗口
        # else:
        #     for title in self.mdi.subWindowList():
        #         # print(title.windowTitle())
        #         if title.windowTitle() == "计划排产":
        #             title.showMaximized()


    # ==========================工作-->质保===============================
    @pyqtSlot()
    def on_actionInspection_triggered(self):  # 工作-->生产-->机加-->机加进度录入
        self.inspect = Inspection()
        self.setCentralWidget(self.inspect)


    # ==========================任务栏连接区===============================
    @pyqtSlot()
    def on_actionNew_triggered(self):
        """文件-->新建 or 点击任务栏新建"""
        dialog = Query_Form()
        dialog.setWindowTitle("查询")
        dialog.setWindowModality(Qt.ApplicationModal)
        dialog.exec_()

    @pyqtSlot()
    def on_actionOpen_triggered(self):
        """文件-->打开 or 点击任务栏"""
        file, ok = QFileDialog.getOpenFileName(
            self, "打开", "C:/Users/Administrator/Desktop/Python/学习相关/", 
            "All Files (*);;Text Files (*.txt)")
        # 在状态栏显示文件地址  		
        self.statusBar.showMessage(file)

    @pyqtSlot()
    def on_actionSave_triggered(self):
        """文件-->保存 or 点击任务栏保存"""
        name = "TW_order"
        print(self.findChild(QStatusBar, "statusbar"))
        if self.findChild(QTableWidget, "TW_order"):
            # Order().on_PBsave_clicked()  # 运行后还不会找到中心控件,要从中心控件入手??????????????????
            if self.centralWidget().lineEdit_3.text() == "":
                QMessageBox.about(self, "注意", "数据不能为空,返回修改!")
                return
            print(self.centralWidget().lineEdit_4.text())
        if self.findChild(QTableWidget, "TWquote"):
            Quote().on_PBsave_clicked()

    @pyqtSlot()
    def on_action_query_triggered(self):
        """查询-->"""
        dialog = DateDialog(self)
        # '''连接子窗口的自定义信号与主窗口的槽函数'''
        # dialog.Signal_No.connect(self.getcheckNo)
        emn = Examine()
        dialog.Signal_No.connect(emn.quote_detail)
        dialog.show()
        # self.dockmain()

    @pyqtSlot()
    def on_actionTile_triggered(self):  # 平铺mid窗口
        self.mdi.tileSubWindows()

    @pyqtSlot()
    def on_actionCascade_triggered(self):  # 层叠mid窗口
        self.mdi.cascadeSubWindows()

    @pyqtSlot()
    def on_actionCloseAll_triggered(self):  # 关闭所有窗口
        # self.mdi.setViewMode(QMdiArea.TabbedView)
        # self.mdi.closeActiveSubWindow()
        self.mdi.closeAllSubWindows()
        print(self.mdi.subWindowList()[0].windowTitle())


    # ============================Dock窗口区===============================
    def dockmain(self):
        if self.findChild(QDockWidget, "dockWidget"):
            # 把关闭隐藏的控件打开
            self.dockWidget.show()
            # 删除控件重新打开
            # self.dockWidget.deleteLater()
        else:
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
            self.btn_edit = QPushButton(self.dockWidgetContents)
            icon2 = QIcon()
            icon2.addPixmap(QPixmap(":/png/images/modify_24px.png"), QIcon.Normal, QIcon.Off)
            self.btn_edit.setIcon(icon2)
            self.btn_edit.setObjectName("btn_edit")
            self.btn_edit.setToolTip("修改")
            self.btn_edit.setText("修改")
            self.horizontalLayout_2.addWidget(self.btn_edit)
            # 下拉列表框
            self.cbo_state = QComboBox(self.dockWidgetContents)
            self.cbo_state.setMinimumSize(QtCore.QSize(0, 26))
            self.cbo_state.setObjectName("cbo_state")
            self.cbo_state.setToolTip("状态")
            self.cbo_state.addItem(QIcon(":/myImage/images/loading.png"), '待审核')
            # self.cbo_state.setStyleSheet("QComboBox{color:red;}")
            self.cbo_state.addItem(QIcon(":/myImage/images/Accept.png"), '审核通过')
            self.cbo_state.addItem(QIcon(":/myImage/images/stop.ico"), '退回修改')
            self.horizontalLayout_2.addWidget(self.cbo_state)
            self.cbo_group = QComboBox(self.dockWidgetContents)
            self.cbo_group.setMinimumSize(QtCore.QSize(120, 26))
            self.cbo_group.setObjectName("cbo_group")
            self.cbo_group.setToolTip("公司名称")
            self.horizontalLayout_2.addWidget(self.cbo_group)
            self.cbo_filter = QComboBox(self.dockWidgetContents)
            self.cbo_filter.setMinimumSize(QtCore.QSize(100, 26))
            self.cbo_filter.setCurrentText("")
            self.cbo_filter.setObjectName("cbo_filter")
            self.cbo_filter.setToolTip("报价单号")
            self.horizontalLayout_2.addWidget(self.cbo_filter)
            # 查询按钮
            self.btn_query = QPushButton(self.dockWidgetContents)
            icon3 = QIcon()
            icon3.addPixmap(QPixmap(":/png/images/file_manager.png"), QIcon.Normal, QIcon.Off)
            self.btn_query.setIcon(icon3)
            self.btn_query.setObjectName("btn_query")
            self.btn_query.setToolTip("查询")
            self.btn_query.setText("查询")
            self.horizontalLayout_2.addWidget(self.btn_query)
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
            self.tablewidget.setColumnCount(0)
            self.tablewidget.setRowCount(0)
            self.verticalLayout.addWidget(self.tablewidget)
            self.dockWidget.setWidget(self.dockWidgetContents)
            self.addDockWidget(QtCore.Qt.DockWidgetArea(4), self.dockWidget)

            # 信号槽
            self.btn_query.clicked.connect(self.dock_data)
            self.tablewidget.itemClicked.connect(self.tablewidget_itemClicked)  # 点击清单,显示选择的明细
            # 下拉列表框选择事件连接
            self.cbo_state.currentIndexChanged.connect(self.cbo_state_currentIndexChanged)
            self.cbo_group.currentIndexChanged.connect(self.cbo_group_currentIndexChanged)
            # self.tablewidget.itemClicked.connect(self.tablewidget_select)  # 点击清单,显示选择的明细

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

    def dock_data(self):
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
        # 把g_NO设为全局变量,输出查询的报价单号
        global g_NO
        g_NO = self.tablewidget.item(h, 1).text()
        # dock窗口第6列的值
        # qte_data = self.tablewidget.item(h, 5).text()
        print('g_NO='+str(g_NO))
        print(self.centralWidget.objectName)

    def getcheckNo(self, bjdh, qte_date):  # 主窗口开启子窗口,实例化子窗口,传值
        self.check = Examine()
        self.check.quote_detail(bjdh, qte_date)
        # self.gridLayout_2.addWidget(self.tblwgt_quote)
        self.setCentralWidget(self.check)
        # self.Signal_OneParameter.disconnect(self.getcheckNo)  #删除信号

# class QueryForm(QWidget, Ui_Query_Form): # 工作-->查询
#     """查询报表功能"""
#     def __init__(self):
#         super(QueryForm, self).__init__()
#         self.setupUi(self)


class FirstForm(QWidget, Ui_First_Form): # 首页
    """首页"""
    def __init__(self):
        super(FirstForm, self).__init__()
        self.setupUi(self)

        # 判断网络连通,执行天气
        # exit_code = os.system('ping www.baidu.com')
        # if exit_code == 0:
        # raise Exception('connect failed.')
            # 天气模块在断网下会启动失败
        try:
            resp = urlopen('http://www.weather.com.cn/weather/101190201.shtml')
        except:
            self.textWeather.setText("没有连接到网络!")
            return
        soup = BeautifulSoup(resp, 'html.parser')
        tagdate = soup.find('ul', class_="t clearfix")
        dates = tagdate.h1.string
        tagtoday = soup.find('p', class_="tem")
        try:
            temperatureHigh = tagtoday.span.string
        except AttributeError as e:
            temperatureHigh = tagtoday.find_next('p', class_="tem").span.string
        temperatureLow = tagtoday.i.string
        weather = soup.find('p', class_="wea").string
        tagWind = soup.find('p', class_="win")
        winL = tagWind.i.string
        msg1 = '今天是： %s' % dates + '\n'
        msg2 = '风级： %s' % winL + '\n'
        msg3 = '最低温度： %s' % temperatureLow + '\n'
        msg4 = '最高温度： %s' % temperatureHigh + '\n'
        msg5 = '天气： %s' % weather
        result = msg1 + msg2 + msg3 + msg4 + msg5
        self.textWeather.setText(result)


if __name__=="__main__":
    app = QApplication(sys.argv)
    Win = Main()
    Win.show()
    sys.exit(app.exec_())
