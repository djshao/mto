# -*- coding: utf-8 -*-

import sys
#from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QFileDialog
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from Ui_ERPMain import Ui_MainWindow
from Ui_查询 import Ui_Query_Form
from 查询 import *
from Ui_首页 import Ui_First_Form
from Ui_Offer_Home import Ui_Offer_Home


class Ui_ERP(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):                         #__init__要两个下划线
        super(Ui_ERP,self).__init__(parent)
        self.setupUi(self)
#        layout = QHBoxLayout()

#        self.first = FirstForm()
#        self.setCentralWidget(self.first)                   #创建中央控件,默认显示首页,单文档界面用

        #多文档界面
        self.mdi = QMdiArea()                                #多文档界面
        self.setCentralWidget(self.mdi)                      #创建中央控件多文档界面要self.mdi
        sub=QMdiSubWindow()
        self.first = FirstForm()                             #添加Ui_首页模块Ui_First_Form类____窗口要初始化后使用
        sub.setWidget(self.first)
        sub.setWindowTitle("首页")
        self.mdi.addSubWindow(sub)
       
        # 菜单的点击事件，当点击新建菜单时连接槽函数 对话框()     
        self.NewAction.triggered.connect(self.showdialog)  
        # self.NewAction.triggered.connect(self.windowaction)
        self.Taskbar.clicked.connect(self.windowaction)
        # 菜单的点击事件，当点击打开菜单时连接槽函数 openMsg()     
        self.OpenAction.triggered.connect(self.openMsg)
        #点击报价目录,获取单元格内容
        # self.Widget_catalog.itemClicked.connect(self.handleItemClick)
        
#        self.setLayout(layout)
        self.statusBar().showMessage('准备就绪')

    # def getItem(self, item):
    #     print('you selected => '+ item.text)

    def windowaction(self, q):  #(self, qmodelindex):   添加一个多文档界面
        item = self.Taskbar.currentItem()
        print("key=%s ,value=%s" % (item.text(0), item.text(1)))
        if item.text(0) == "生产进度":
            sub=QMdiSubWindow()
            self.child = QueryForm()
            sub.setWidget(self.child)
            sub.setWindowTitle("查询生产进度")
            self.mdi.addSubWindow(sub)
            sub.show()
        
        if item.text(0) == "报价":
            sub=QMdiSubWindow()
            self.child = OfferHome()
            sub.setWidget(self.child)
            sub.setWindowTitle("报价首页")
            self.mdi.addSubWindow(sub)
            sub.show()
#            self.mdi.tileSubWindows()#平铺窗口

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

class OfferHome(QWidget, Ui_Offer_Home):#报价首页
    def __init__(self):
        super(OfferHome, self).__init__()
        self.setupUi(self)

if __name__=="__main__":
    app = QApplication(sys.argv)
    Win = Ui_ERP()
    Win.show()
    sys.exit(app.exec_())
