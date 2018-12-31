# -*- coding: utf-8 -*-

import sys
# from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QFileDialog
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import pymysql
from urllib.request import urlopen
from bs4 import BeautifulSoup
# import re
from Ui_ERPMain import Ui_MainWindow
from Ui_查询 import Ui_Query_Form
from 查询 import *
from Ui_首页 import Ui_First_Form
from sell.sell import QuoteExamine, Quote
# from sell.Ui_quote_check import Ui_Quote_check
# from sell.Ui_quote import Ui_Fquote

class Ui_ERP(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):                         #__init__要两个下划线
        super(Ui_ERP,self).__init__(parent)
        self.setupUi(self)
        self.setCentralWidget(FirstForm())
        # layout = QHBoxLayout()

        self.statusBar().showMessage('准备就绪') # 屏幕左下状态栏显示提示信息

    @pyqtSlot()
    def on_action_home_triggered(self):
        """
        返回首页
        """
        self.setCentralWidget(FirstForm())

    @pyqtSlot()
    def on_action_quote_triggered(self):
        """
        报价
        """
        self.setCentralWidget(Quote())

    @pyqtSlot()
    def on_action_quote_examine_triggered(self):
        """
        报价审核
        """
        self.setCentralWidget(QuoteExamine())

    @pyqtSlot()   
    def on_actionscjd_triggered(self):
        """
        查询生产进度 修改中间窗口为多文档界面显示
        """
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

    @pyqtSlot()
    def on_NewAction_triggered(self):                      #查看弹出对话框
        """
        弹出新建对话框
        """
        dialog = Query_Form()
        dialog.setWindowTitle("查询")
        dialog.setWindowModality(Qt.ApplicationModal)
        dialog.exec_()

    @pyqtSlot()
    def on_OpenAction_triggered(self):
        """
        菜单打开-打开文件对话框
        """
        file,ok= QFileDialog.getOpenFileName(self,"打开","C:/Users/Administrator/Desktop/Python/学习相关/","All Files (*);;Text Files (*.txt)") 
        # 在状态栏显示文件地址  		
        self.statusbar.showMessage(file) 


class QueryForm(QWidget, Ui_Query_Form):#查询
    def __init__(self):
        super(QueryForm, self).__init__()
        self.setupUi(self)


class FirstForm(QWidget, Ui_First_Form):#首页
    """
    首页
    """
    def __init__(self):
        super(FirstForm, self).__init__()
        self.setupUi(self)

        resp=urlopen('http://www.weather.com.cn/weather/101190201.shtml')
        soup=BeautifulSoup(resp,'html.parser')
        tagDate=soup.find('ul', class_="t clearfix")
        dates=tagDate.h1.string
        tagToday=soup.find('p', class_="tem")
        try:
            temperatureHigh=tagToday.span.string
        except AttributeError as e:
            temperatureHigh=tagToday.find_next('p', class_="tem").span.string
        temperatureLow=tagToday.i.string
        weather=soup.find('p', class_="wea").string
        tagWind=soup.find('p',class_="win")
        winL=tagWind.i.string
        msg1 = '今天是： %s' % dates + '\n'
        msg2 = '风级： %s' % winL + '\n'
        msg3 = '最低温度： %s' % temperatureLow + '\n'
        msg4 = '最高温度： %s' % temperatureHigh + '\n'
        msg5 = '天气： %s' % weather
        result = msg1 + msg2 + msg3 + msg4 + msg5
        self.textWeather.setText(result)



if __name__=="__main__":
    app = QApplication(sys.argv)
    Win = Ui_ERP()
    Win.show()
    sys.exit(app.exec_())
