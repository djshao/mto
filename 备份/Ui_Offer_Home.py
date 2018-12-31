# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Administrator\Desktop\Python\ERP\Offer_Home.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import pymysql
from functools import partial
from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSignal, QObject, Qt, pyqtSlot

class Ui_Offer_Home(object):
    def setupUi(self, Offer_Home):
        Offer_Home.setObjectName("Offer_Home")
        Offer_Home.resize(1024, 768)
        Offer_Home.setToolTip("")
        self.verticalLayout = QtWidgets.QVBoxLayout(Offer_Home)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.Button_offernew = QtWidgets.QPushButton(Offer_Home)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("images/Add_16px_528841_easyicon.net.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Button_offernew.setIcon(icon)
        self.Button_offernew.setObjectName("Button_offernew")
        self.horizontalLayout.addWidget(self.Button_offernew)
        self.Button_audit = QtWidgets.QPushButton(Offer_Home)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("images/Accept_16px_528836_easyicon.net.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Button_audit.setIcon(icon1)
        self.Button_audit.setObjectName("Button_audit")
        self.horizontalLayout.addWidget(self.Button_audit)
        self.Box_group = QtWidgets.QComboBox(Offer_Home)
        self.Box_group.setObjectName("Box_group")
        self.horizontalLayout.addWidget(self.Box_group)
        self.Box_filter = QtWidgets.QComboBox(Offer_Home)
        self.Box_filter.setObjectName("Box_filter")
        self.horizontalLayout.addWidget(self.Box_filter)
        self.Line_search = QtWidgets.QLineEdit(Offer_Home)
        self.Line_search.setText("")
        self.Line_search.setObjectName("Line_search")
        self.horizontalLayout.addWidget(self.Line_search)
        self.verticalLayout.addLayout(self.horizontalLayout)

        #连接数据库
        db = pymysql.connect(host='127.0.0.1', port=3308, user='root', password='root', db='mrp',charset='utf8',)
        cur = db.cursor()
        cur.execute("SELECT * FROM 报价基本信息")
        data = cur.fetchall()                                     #接收全部的返回结果行
        col_lst = [tup[0] for tup in cur.description]             #数据列字段名 tup:数组 #description:种类
        #数据的大小
        row = len(data)                                           #获得data的行数
        vol = len(data[0])                                        #获得data的卷数.第一行的数量(列数)
        #插入表格
        self.Widget_catalog = QTableWidget(row,vol)               #目录表
        self.Widget_details = QTableWidget(row,vol)               #明细表
        font = QtGui.QFont('微软雅黑',9)
        #设置字体、表头
        self.Widget_catalog.horizontalHeader().setFont(font)      #设置行表头字体
        self.Widget_catalog.setHorizontalHeaderLabels(col_lst)    #设置标题
        #设置竖直方向表头不可见
#        self.Widget_catalog.verticalHeader().setVisible(False)
        self.Widget_catalog.setFrameShape(QFrame.NoFrame)         #设置无边框
        #设置表格颜色             
        self.Widget_catalog.horizontalHeader().setStyleSheet('QHeaderView::section{background:skyblue}')
        
        self.Widget_catalog.setContextMenuPolicy(Qt.CustomContextMenu)#允许右键产生菜单
        self.Widget_catalog.customContextMenuRequested.connect(self.generateMenu)#将右键绑定到槽
        
#        self.Widget_catalog.setEditTriggers(QAbstractItemView.NoEditTriggers)#设置表格禁止编辑
        self.Widget_catalog.setSelectionBehavior(QAbstractItemView.SelectRows)#设置整行选中
        self.verticalLayout.addWidget(self.Widget_catalog)
        
        #构建表格插入数据
        for i in range(row):                                      #i到row-1的数量
            for j in range(vol):
                temp_data = data[i][j]                            # 临时记录，不能直接插入表格
                data1 = QTableWidgetItem(str(temp_data))          # 转换后可插入表格
                self.Widget_catalog.setItem(i, j, data1)
        self.Widget_catalog.resizeColumnsToContents()             #自适应宽度
        self.Widget_catalog.resizeRowsToContents()                #自适应行高,这两句放最后可以等数据写入后自动适应表格数据宽度
        db.close
        cur.close

        #报价明细区域
#        db = pymysql.connect(host='127.0.0.1', port=3308, user='root', password='root', db='mrp',charset='utf8',)
        conn = db.cursor()
        sql = "SELECT * FROM 报价明细 WHERE 报价单号 LIKE 'BJ18011516'"   #'%"+bjdh+"%'"
        conn.execute(sql)
        col_lst_1 = [tup[0] for tup in conn.description]             #数据列字段名 tup:数组 #description:种类
        vol_1 = len(conn.description)                                #获得data的卷数.第一行的数量(列数)cur.description  len(data[0]) 
        self.Widget_details = QTableWidget(100,vol_1)
        self.Widget_details.setHorizontalHeaderLabels(col_lst_1)
#        self.Widget_details.verticalHeader().setVisible(False)
        self.Widget_details.setFrameShape(QFrame.NoFrame)             #设置无边框
        self.Widget_details.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.Widget_details.horizontalHeader().setStyleSheet('QHeaderView::section{background:skyblue}')
        self.Widget_details.setObjectName("报价明细")
        self.verticalLayout.addWidget(self.Widget_details)
        self.Widget_details.resizeColumnsToContents()                 #自适应字段宽度
        
        db.close
        conn.close
        
        self.retranslateUi(Offer_Home)
        QtCore.QMetaObject.connectSlotsByName(Offer_Home)

        #测试显示报价明细
#        self.Button_offernew.clicked.connect(self.querycl)
        self.Widget_catalog.itemClicked.connect(self.querydt)
        self.Button_offernew.clicked.connect(partial(self.up_data, cur, db))  #更新实现  #partialial传递db
#        self.Button_offernew.clicked.connect(self.msg)

    def generateMenu(self, pos):
        row_num = -1
        for i in self.Widget_catalog.selectionModel().selection().indexes():
            row_num = i.row()
        if row_num < 2 :
            menu = QMenu()
            item1 = menu.addAction(u"通过")
            item2 = menu.addAction(u"未通过")
            action = menu.exec_(self.Widget_catalog.mapToGlobal(pos))
            if action == item1:
                print('你选了通过')
            elif action == item2:
                print('你选了未通过')
            else:
                return

    def querycl(self, db):#查询报价目录
        lsearch = self.Line_search.text()                    #搜索框
        db = pymysql.connect(host='127.0.0.1', port=3308, user='root', password='root', db='mrp',charset='utf8',)
        curr = db.cursor()
        print('you search=> '+ lsearch)
        sql = "SELECT * FROM 报价基本信息 WHERE 公司名称 LIKE '%"+lsearch+"%'"   #'%"+bjdh+"%'"
        curr.execute(sql)
        self.Widget_catalog.clearContents()
        data_2 = curr.fetchall()
        row_2 = len(data_2)                                 #获得data的行数
        vol_2 = len(curr.description)                       #获得data的列数.cur.description  len(data[0]) 
        #构建表格插入数据
        for i in range(row_2):                              #i到row-1的数量
            for j in range(vol_2):
                temp_data = data_2[i][j]                    # 临时记录，不能直接插入表格
                data2 = QTableWidgetItem(str(temp_data))    # 转换后可插入表格
                self.Widget_catalog.setItem(i, j, data2)
        self.Widget_catalog.resizeColumnsToContents()       #自适应宽度
        self.Widget_catalog.resizeRowsToContents()          #自适应行高

    def querydt(self):#查询报价明细querydt(self, item)
#        print('you selected => '+ item.text())
#        self.Line_search.setText(item.text())               #搜索框等于点击表格的值
        h = self.Widget_catalog.currentIndex().row()         #找到所选行的行数h
        bjdh = self.Widget_catalog.item(h, 0).text()         #找到所选h行的0位报价单号
        db = pymysql.connect(host='127.0.0.1', port=3308, user='root', password='root', db='mrp',charset='utf8',)
        cur_3 = db.cursor()
        sql = "SELECT * FROM 报价明细 WHERE 报价单号 LIKE '%"+bjdh+"%'"   #'%"+bjdh+"%'"
        cur_3.execute(sql)
        self.Widget_details.clearContents()
        data_3 = cur_3.fetchall()
        row_3 = len(data_3)                                   #获得data的行数
        vol_3 = len(cur_3.description)                        #获得data的列数.cur.description  len(data[0]) 
        #构建表格插入数据
        for i in range(row_3):                                #i到row-1的数量
            for j in range(vol_3):
                temp_data = data_3[i][j]                      # 临时记录，不能直接插入表格
                data3 = QTableWidgetItem(str(temp_data))      # 转换后可插入表格
                self.Widget_details.setItem(i, j, data3)
        self.Widget_details.resizeColumnsToContents()          #自适应宽度
        self.Widget_details.resizeRowsToContents()             #自适应行高
        
        
    #更新数据
    def up_data(self,cur,db):
        h = self.Widget_catalog.currentIndex().row()          #找到所选行的行数h
        bjdh = self.Widget_catalog.item(h, 0).text()          #找到所选h行的0位报价单号
        print('you bjdh=> '+ bjdh)
        cur.execute("UPDATE 报价基本信息 SET 状态='通过' WHERE 报价单号 = '"+bjdh+"'")
        db.commit()
        reply = QMessageBox.information(QWidget(), "标题", "审核成功" )  
        print( reply )
        
#    def msg(self): 
#        reply = QMessageBox.information(QWidget(), "标题", "对话框消息正文", QMessageBox.Yes | QMessageBox.No ,  QMessageBox.Yes )  
#        print( reply )

    def retranslateUi(self, Offer_Home):
        _translate = QtCore.QCoreApplication.translate
        Offer_Home.setWindowTitle(_translate("Offer_Home", "报价首页"))
        self.Button_offernew.setText(_translate("Offer_Home", "新建"))
        self.Button_audit.setText(_translate("Offer_Home", "审核"))
        self.Box_group.setToolTip(_translate("Offer_Home", "分组"))
        self.Box_filter.setToolTip(_translate("Offer_Home", "筛选"))
        self.Line_search.setToolTip(_translate("Offer_Home", "搜索"))
        self.Line_search.setPlaceholderText(_translate("Offer_Home", "搜索...."))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Offer_Home = QtWidgets.QWidget()
    ui = Ui_Offer_Home()
    ui.setupUi(Offer_Home)
    Offer_Home.show()
    sys.exit(app.exec_())

