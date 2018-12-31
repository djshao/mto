# -*- coding: utf-8 -*-


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal, QObject, Qt, pyqtSlot
import pymysql
from functools import partial
from PyQt5.QtWidgets import *
from Ui_Sale_Home import *
from sell.Ui_examine_bar import Ui_Bar_examine

class quote_examine(QWidget, Ui_Offer_Home):#继承销售首页
    def __init__(self, parent=None):
        super(quote_examine, self).__init__(parent)
        self.setupUi(self)
        self.viewcatalog() 
        # self.bar()      
        #连接槽
        self.Widget_catalog.itemClicked.connect(self.querydt) #点击报价目录,显示选择的报价单
        self.Button_query.clicked.connect(self.querycl)    #  #partial(self.querycl,db)传递db

    def viewcatalog(self):#默认显示报价基本信息
        #连接数据库
        db = pymysql.connect(host='127.0.0.1', port=3308, user='root', password='root', db='mrp',charset='utf8',)
        cur = db.cursor()
        cur.execute("SELECT * FROM 报价基本信息")
        data = cur.fetchall()                                     #接收全部的返回结果行
        col_lst = [tup[0] for tup in cur.description]             #数据列字段名 tup:数组 #description:种类
        #数据的大小
        row = len(data)                                           #获得data的行数
        vol = len(data[0])                                        #获得data的列数.cur.description或len(data[0]) 
        #插入表格
        self.Widget_catalog = QTableWidget(row,vol)               #目录表
        font = QtGui.QFont('微软雅黑',9)
        self.Widget_catalog.horizontalHeader().setFont(font)      #设置行表头字体
        self.Widget_catalog.setHorizontalHeaderLabels(col_lst)    #设置标题
        self.Widget_catalog.verticalHeader().setVisible(False)    #左垂直表头不显示
        #设置表格颜色             
        self.Widget_catalog.horizontalHeader().setStyleSheet('QHeaderView::section{background:skyblue}')
        self.Widget_catalog.setContextMenuPolicy(Qt.CustomContextMenu)#允许右键产生菜单
        self.Widget_catalog.customContextMenuRequested.connect(self.generateMenu)#将右键绑定到槽
        self.Widget_catalog.setEditTriggers(QAbstractItemView.NoEditTriggers)#设置表格禁止编辑
        self.Widget_catalog.setSelectionBehavior(QAbstractItemView.SelectRows)#设置整行选中
        splitter = QtWidgets.QSplitter(QtCore.Qt.Vertical)                    #设置分割条
        self.Widget_catalog.setFrameStyle(QtWidgets.QFrame.Box | QtWidgets.QFrame.Plain)
        #构建表格插入数据
        for i in range(row):                                      #i到row-1的数量
            for j in range(vol):
                temp_data = data[i][j]                            # 临时记录，不能直接插入表格
                data1 = QTableWidgetItem(str(temp_data))          # 转换后可插入表格
                self.Widget_catalog.setItem(i, j, data1)
        # self.Widget_catalog.resizeColumnsToContents()             #自适应宽度
        # self.Widget_catalog.resizeRowsToContents()                #自适应行高,这两句放最后可以等数据写入后自动适应表格数据宽度
        self.Widget_catalog.horizontalHeader().setStretchLastSection(True)#最后一列对齐边框
        splitter.addWidget(self.Widget_catalog)
        # self.verticalLayout.addWidget(splitter)                   #加入布局需要最后加,不然出错.

        # 报价明细区域
        cur_3 = db.cursor()
        sql = "SELECT * FROM 报价明细"
        cur_3.execute(sql)
        data_3 = cur_3.fetchall()
        col_lst_3 = [tup[0] for tup in cur_3.description]
        vol_3 = len(data_3[0])                                       #获得data的列数.cur.description  len(data[0]) 
        self.Widget_details = QTableWidget(0,vol_3)                  #初始界面显示标题不用显示明细数据,所以QTableWidget(0,vol_3) 
        font = QtGui.QFont('微软雅黑',9)
        self.Widget_details.horizontalHeader().setFont(font)         #设置行表头字体
        self.Widget_details.setHorizontalHeaderLabels(col_lst_3)     #设置标题
        self.Widget_details.verticalHeader().setVisible(False)       #左垂直表头不显示
        self.Widget_details.setObjectName("报价明细")
        self.Widget_details.horizontalHeader().setStyleSheet('QHeaderView::section{background:skyblue}')
        self.Widget_details.setFrameStyle(QtWidgets.QFrame.Box | QtWidgets.QFrame.Plain)
        self.Widget_details.resizeColumnsToContents()                #自适应宽度
        # self.Widget_details.horizontalHeader().setStretchLastSection(True)#最后一列对齐边框
        self.Widget_details.setFrameStyle(QtWidgets.QFrame.Box | QtWidgets.QFrame.Plain)
        splitter.addWidget(self.Widget_details)
        self.verticalLayout.addWidget(splitter)
        # self.setLayout(self.verticalLayout)                      ##加这行后查询后可以更新,不用再addwidget,待搞明白?

    def generateMenu(self, pos):#右键菜单
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

    def querycl(self):#查询报价基本信息目录
        self.Widget_catalog.clearContents                    #clearContents清除内容,clear清空表格中所有内容（包含表头）
        # QTableWidget.clear()
        lsearch = self.Line_search.text()                    #搜索框
        db = pymysql.connect(host='127.0.0.1', port=3308, user='root', password='root', db='mrp',charset='utf8',)
        curr = db.cursor()
        print('you search=> '+lsearch)
        sql = "SELECT * FROM 报价基本信息 WHERE 公司名称 LIKE '%"+lsearch+"%'"   #'%"+bjdh+"%'"
        curr.execute(sql)
        data_2 = curr.fetchall()
        col_lst_2 = [tup[0] for tup in curr.description]
        row_2 = len(data_2)                                 #获得data的行数
        vol_2 = len(curr.description)                       #获得data的列数.cur.description  len(data[0]) 
        self.Widget_catalog.setRowCount(row_2)              #取查询到数据的行数,设表格行数
        # self.Widget_catalog = QTableWidget(row_2,vol_2)
        # self.Widget_catalog.setHorizontalHeaderLabels(col_lst_2)
        for i in range(row_2):                              #i到row-1的数量
            for j in range(vol_2):
                temp_data = data_2[i][j]                    # 临时记录，不能直接插入表格
                data2 = QTableWidgetItem(str(temp_data))    # 转换后可插入表格
                self.Widget_catalog.setItem(i, j, data2)
        # self.verticalLayout.addWidget(self.Widget_catalog)
        # self.setLayout(self.verticalLayout)

    def querydt(self):#查询报价明细    querydt(self, item)
        # print('you selected => '+ item.text())
        # self.Line_search.setText(item.text())                    #搜索框等于点击表格的值
        h = self.Widget_catalog.currentIndex().row()               #找到所选行的行数h
        bjdh = self.Widget_catalog.item(h, 0).text()               #找到所选h行的0位报价单号
        db = pymysql.connect(host='127.0.0.1', port=3308, user='root', password='root', db='mrp',charset='utf8',)
        cur_3 = db.cursor()
        sql = "SELECT * FROM 报价明细 WHERE 报价单号 LIKE '%"+bjdh+"%'"   #'%"+bjdh+"%'"
        cur_3.execute(sql)
        self.Widget_details.clearContents()                         #清除表内数据
        data_3 = cur_3.fetchall()
        col_lst_3 = [tup[0] for tup in cur_3.description]
        row_3 = len(data_3)                                          #获得data的行数
        vol_3 = len(data_3[0])                                       #获得data的列数.cur.description  len(data[0]) 
        self.Widget_details.setRowCount(row_3)
        # self.Widget_catalog.setColumnCount(0)
        #构建表格插入数据
        for i in range(row_3):                                       #i到row-1的数量
            for j in range(vol_3):
                temp_data = data_3[i][j]                           # 临时记录，不能直接插入表格
                data3 = QTableWidgetItem(str(temp_data))           # 转换后可插入表格
                self.Widget_details.setItem(i, j, data3)
        self.Widget_details.resizeColumnsToContents()              #自适应宽度
        # self.Widget_details.resizeRowsToContents()                 #自适应行高
        self.Widget_details.horizontalHeader().setStretchLastSection(True)#最后一列对齐边框
        
    def up_data(self):#审核通过
        h = self.Widget_catalog.currentIndex().row()          #找到所选行的行数h
        bjdh = self.Widget_catalog.item(h, 0).text()          #找到所选h行的0位报价单号
        print('you bjdh=> '+ bjdh)
        db = pymysql.connect(host='127.0.0.1', port=3308, user='root', password='root', db='mrp',charset='utf8',)
        cur_4 = db.cursor()
        cur_4.execute("UPDATE 报价基本信息 SET 状态='通过' WHERE 报价单号 = '"+bjdh+"'")
        db.commit()
        reply = QMessageBox.information(QWidget(), "标题", "审核成功" )  
        print( reply )
        cur_4.close
        db.close

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    #    Offer_Home = QtWidgets.QWidget()          
    ui = quote_examine()
#    ui.setupUi(Offer_Home)
    ui.show()
    sys.exit(app.exec_())

