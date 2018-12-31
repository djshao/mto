# -*- coding: utf-8 -*-

import sys
# from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QFileDialog
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import pymysql
from Ui_ERPMain import Ui_MainWindow
from Ui_查询 import Ui_Query_Form
from 查询 import *
from Ui_首页 import Ui_First_Form
from sell.quote_check import QuoteExamine
from sell.Ui_quote_check import Ui_Quote_check


class Ui_ERP(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):                         #__init__要两个下划线
        super(Ui_ERP,self).__init__(parent)
        self.setupUi(self)
        # self.homepage()
        # layout = QHBoxLayout()
        # 返回首页    
        self.action_home.triggered.connect(self.homepage)
        # 点击新建时连接槽函数 对话框()     
        self.NewAction.triggered.connect(self.showdialog)  
        # 连接报价审核
        self.action_quote_examine.triggered.connect(self.quotecheck)
        # self.action_quote_examine.triggered.connect(self.sale1)
        # 连接查询生产进度
        self.actionscjd.triggered.connect(self.scjd)
        # 菜单的点击打开事件，当点击打开菜单时连接槽函数 openMsg()     
        self.OpenAction.triggered.connect(self.openMsg)
        #点击报价目录,获取单元格内容
        # self.Widget_catalog.itemClicked.connect(self.handleItemClick)
        # self.setLayout(layout)
        self.statusBar().showMessage('准备就绪')

    # def sale1(self):                                   #调用sell文件夹下报价目录,做窗口停靠
    #     self.items = QDockWidget("报价审核",self)
    #     self.items.setWidget(Bexamine())
    #     self.addDockWidget(Qt.TopDockWidgetArea, self.items)
    #     self.setLayout(QHBoxLayout())                  #设置布局,可以调整窗口,需把分割条弄出来???

        #多文档界面,打开首页
    def homepage(self):
        self.setCentralWidget(FirstForm())

    def quotecheck(self):
        self.setCentralWidget(QuoteExamine())
       
    # def getItem(self, item):
#        print('you selected => ')

    def scjd(self, q):  #(self, qmodelindex):   添加一个多文档界面
        # print("key=%s ,value=%s" % (item.text(0), item.text(1)))
        self.mdi = QMdiArea()                                 #多文档界面
        self.setCentralWidget(self.mdi)                       #创建中央控件多文档界面要self.mdi
        sub=QMdiSubWindow()
        self.child = QueryForm()
        sub.setWidget(self.child)
        sub.setWindowTitle("查询生产进度")
        self.mdi.addSubWindow(sub)
        sub.show()
        
    def sale(self):
        sub=QMdiSubWindow()
        self.child = quote_examine()
        sub.setWidget(self.child)
        sub.setWindowTitle("报价首页")
        self.mdi.addSubWindow(sub)
        sub.show()
        self.mdi.tileSubWindows()#平铺窗口

    def showdialog(self):                      #查看弹出对话框
        dialog = Query_Form()
        dialog.setWindowTitle("查询")
        dialog.setWindowModality(Qt.ApplicationModal)
        dialog.exec_()

    def openMsg(self):
        file,ok= QFileDialog.getOpenFileName(self,"打开","C:/Users/Administrator/Desktop/Python/学习相关/","All Files (*);;Text Files (*.txt)") 
        # 在状态栏显示文件地址  		
        self.statusbar.showMessage(file) 

class QueryForm(QWidget, Ui_Query_Form):#查询
    def __init__(self):
        super(QueryForm, self).__init__()
        self.setupUi(self)

class FirstForm(QWidget, Ui_First_Form):#首页
    def __init__(self):
        super(FirstForm, self).__init__()
        self.setupUi(self)

class Bexamine(QWidget, Ui_Quote_check):#报价审核
    def __init__(self):
        super(Bexamine, self).__init__()
        self.setupUi(self)
        
        


#class OfferHome(QWidget, Ui_Offer_Home):#报价首页
#    def __init__(self):
#        super(OfferHome, self).__init__()
#        self.setupUi(self)

if __name__=="__main__":
    app = QApplication(sys.argv)
    Win = Ui_ERP()
    Win.show()
    sys.exit(app.exec_())
