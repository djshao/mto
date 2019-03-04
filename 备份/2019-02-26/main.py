# -*- coding: utf-8 -*-

import sys, os
# sys.path.append("..")
# sys.path.append("../lib") 添加上级路径
# from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QFileDialog
from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog,QPrintPreviewDialog

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
from delivery.delivery import *

from tools.datadialog import DateDialog  # 查询子窗口
from tools.mysql_conn import myMdb
from tools.dock import DockMain

mymdb = myMdb()

class Main(QMainWindow, Ui_MainWindow):
    # Signal_dockparam = pyqtSignal(list)  # 定义dock窗口信号用

    def __init__(self, parent=None):
        super(Main, self).__init__(parent)
        self.setupUi(self)
        self.firstform = FirstForm()
        self.setCentralWidget(self.firstform)

        self.statusBar.showMessage('欢迎某某某登录星达ERP') # 屏幕左下状态栏显示提示信息

    @pyqtSlot()
    def on_actionHomepage_triggered(self): # 工作-->首页
        # 清除保存/查询变量
        self.clearVar()
        self.firstform = FirstForm()
        self.setCentralWidget(self.firstform)

#===========================工作-->销售===============================
    @pyqtSlot()
    def on_actionQuote_triggered(self): # 工作-->销售-->报价
        # 清除保存/查询变量
        self.clearVar()
        self.quote = Quote()
        self.setCentralWidget(self.quote)

    @pyqtSlot()
    def on_actionAdjust_triggered(self): # 工作-->销售-->调价
        # 清除保存/查询变量
        self.clearVar()
        self.adjustprice = AdjustPrice()
        self.setCentralWidget(self.adjustprice)

    @pyqtSlot()
    def on_actionOrder_triggered(self): # 工作-->销售-->订单
        # 清除保存/查询变量
        self.clearVar()
        self.order = Order()
        self.setCentralWidget(self.order)

    @pyqtSlot()
    def on_actionCheck_triggered(self): # 工作-->销售-->报价审核
        # 清除保存/查询变量
        self.clearVar()
        self.examine = Examine()
        self.setCentralWidget(self.examine)
        # 连接审核修改记录信号到状态栏
        self.examine.Signal_xgjl.connect(self.statusbar_info)

    @pyqtSlot()
    def on_actionDL_triggered(self):  # 工作-->销售-->运输发货-->新建发货清单
        # 清除保存/查询变量
        self.clearVar()
        self.delivery = DeliveryList()
        self.setCentralWidget(self.delivery)
        # 定义dock窗口槽,传递查询选择数据到发货清单
        self.m_slot = self.delivery.writeParam
        # 定义保存函数
        self.m_save = self.delivery.saveData

    @pyqtSlot()
    def on_actionDR_triggered(self):  # 工作-->销售-->运输发货-->修改发货清单
        # 清除保存/查询变量
        self.clearVar()
        self.deliveryrevise = DeliveryRevise()
        self.setCentralWidget(self.deliveryrevise)
        # 定义保存函数变量
        self.m_save = self.deliveryrevise.saveDeliveryRevise

    @pyqtSlot()
    def on_actionPK_triggered(self):  # 工作-->销售-->运输发货-->包装运输
        # 清除保存/查询变量
        self.clearVar()
        self.pack = Packing()
        self.setCentralWidget(self.pack)
        # 定义保存函数变量
        self.m_save = self.pack.savePack

    @pyqtSlot()
    def on_actionTS_triggered(self):  # 工作-->销售-->运输发货-->物流
        # 清除保存/查询变量
        self.clearVar()
        self.transport = Transport()
        self.setCentralWidget(self.transport)
        # 定义dock窗口槽,传递查询选择数据到安排运输
        self.m_slot = self.transport.writeParam
        # 定义dock窗口标题
        
        # 定义保存函数变量
        # self.m_save = self.transport.savetransport


    @pyqtSlot()
    def on_actionWR_triggered(self):  # 工作-->销售-->运输发货-->质保书
        self.warranty = Warranty()
        self.setCentralWidget(self.warranty)

    def statusbar_info(self, record):  # 状态栏信息
        self.statusBar.showMessage(record)

    @pyqtSlot()
    def on_actionziyuan_triggered(self): # 工作-->查询-->生产进度
        """工作-->查询-->生产进度 中间窗口显示多文档界面用法"""
        # print("key={} ,value={}".format(item.text(0), item.text(1)))
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
        # 清除保存/查询变量
        self.clearVar()
        self.forge = Forge()
        self.setCentralWidget(self.forge)

    @pyqtSlot()
    def on_actionMchInput_triggered(self):  # 工作-->生产-->机加-->机加进度录入
        # 清除保存/查询变量
        self.clearVar()
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
    def on_actionInspection_triggered(self):  # 工作-->生产-->出厂检验录入
        # 清除保存/查询变量
        self.clearVar()
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
        # 判断对象self是否name为'm_save'的特性,返回true就执行
        if hasattr(self, 'm_save'):
            self.m_save()
        else:
            return

    @pyqtSlot()
    def on_action_query_triggered(self):
        """查询-->"""
        if hasattr(self, 'm_slot'):
            # 判断是否存在dock窗口
            if self.findChild(QDockWidget, "dockWidget"):
                del self.dock
                # self.dock.dockWidget.show()
                # self.dock.Signal_dockparam.connect(self.m_slot)
            self.dock = DockMain()
            self.addDockWidget(Qt.DockWidgetArea(4), self.dock.dockWidget)
            # 连接子窗口的自定义信号与主窗口的槽函数.m_slot为槽变量,根据工作目录选中而来
            self.dock.Signal_dockparam.connect(self.m_slot)
        else:
            return

#===========================标题栏=====================================
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
        # print(self.mdi.subWindowList()[0].windowTitle())

    # 动作一：打印，无预览
    def on_printAction1_triggered(self):
        printer = QPrinter()
        printDialog = QPrintDialog(printer, self)
        if printDialog.exec_() == QDialog.Accepted:
            self.handlePaintRequest(printer)

    # 动作二：打印，有预览
    @pyqtSlot()
    def on_actionprint_triggered(self):
        dialog = QPrintPreviewDialog()
        dialog.paintRequested.connect(self.handlePaintRequest)
        dialog.exec_()

    # 动作三：直接打印
    def on_printAction3_triggered(self):
        printer = QPrinter()
        self.handlePaintRequest(printer)

    # 动作四：打印到pdf
    # @pyqtSlot()
    # def on_actionprint_triggered(self):
        printer = QPrinter()
        printer.setOutputFormat(QPrinter.PdfFormat)
        printer.setOutputFileName("C:/pdf打印测试.pdf")
        self.handlePaintRequest(printer)

    # 打印函数
    def handlePaintRequest(self, printer):
        document = QTextDocument()
        cursor = QTextCursor(document)
        # cursor.insertText(self.label.text())
        # self.deli = DeliveryList()
        # print(self.deli.lineEdit_5.text())
        cursor.insertText('self.deli.lineEdit_5.text()')
        document.print(printer)

    def clearVar(self):
        """清除保存/查询变量"""
        if hasattr(self, 'm_slot'):
            del self.m_slot
        elif hasattr(self, 'm_save'):
            del self.m_save
        else:
            return



class FirstForm(QWidget, Ui_First_Form): # 首页
    """首页"""
    def __init__(self):
        super(FirstForm, self).__init__()
        self.setupUi(self)

        # 判断网络连通,执行天气
        # exit_code = os.system('ping www.baidu.com')
        # if exit_code == 0:
        # raise Exception('connect failed.')
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
        msg1 = '今天是： {}'.format(dates) + '\n'
        msg2 = '风级： {}'.format(winL) + '\n'
        msg3 = '最低温度： {}'.format(temperatureLow) + '\n'
        msg4 = '最高温度： {}'.format(temperatureHigh) + '\n'
        msg5 = '天气： {}'.format(weather)
        result = msg1 + msg2 + msg3 + msg4 + msg5
        self.textWeather.setText(result)


if __name__=="__main__":
    app = QApplication(sys.argv)
    splash = QSplashScreen()
    splash.setPixmap(QPixmap('./wxxd/images/just do it.jpg'))
    splash.show()
    splash.showMessage('欢迎试用星达ERP',
                       Qt.AlignBottom | Qt.AlignCenter, Qt.white)
    time.sleep(2)

    Win = Main()
    Win.show()
    splash.finish(Win)
    sys.exit(app.exec_())
