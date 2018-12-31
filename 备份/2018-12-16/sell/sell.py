# -*- coding: utf-8 -*-
"""
销售功能模块
"""
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal, QObject, Qt, pyqtSlot, QDate, QDateTime
import pymysql
from PyQt5.QtWidgets import *
from sell.Ui_quote_check import Ui_Quote_check
from sell.Ui_quote import Ui_Fquote
import pandas as pd
import numpy as np


class Quote(QWidget,Ui_Fquote):
    """
    报价类
    """
    def __init__(self, parent=None):
        super(Quote, self).__init__(parent)
        self.setupUi(self)
        self.quotedate.setDate(QDate.currentDate())

        #公司名称下拉列表框
        db = pymysql.connect(host='localhost', port=3308, user='root', password='root', db='mrp',charset='utf8')
        cur = db.cursor()
        sql = "select 公司名称 from 客户资料表"
        cur.execute(sql)
        result = cur.fetchall()
        col_lst = [tup[0] for tup in result]             #循环取元祖数据,转为列表
        self.CBcorporate.addItem("")
        self.CBcorporate.addItems(col_lst)

        self.TWquote.setRowCount(11)                                       # 打开时设置11行
        self.TWquote.horizontalHeader().setStyleSheet('QHeaderView::section{background:skyblue}')
        self.TWquote.setContextMenuPolicy(Qt.CustomContextMenu)            # 允许右键产生菜单
        self.TWquote.customContextMenuRequested.connect(self.right_menu)    # 将右键绑定到槽
        # self.TWquote.setSelectionBehavior(QAbstractItemView.SelectRows)  # 设置整行选中
        # self.TWquote.verticalHeader().setVisible(False)                  # 左垂直表头不显示
        # self.TWquote.setEditTriggers(QAbstractItemView.AnyKeyPressed)    # 设置表格任何时候都能修改
        self.TWquote.horizontalHeader().setStretchLastSection(True)        #最后一列对齐边框
        # self.TWquote.horizontalHeader().setResizeMode(QHeaderView.Stretch)
        # self.TWquote.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch) #占满屏幕,平均分配列宽
        self.TWquote.resizeColumnsToContents()                             # 自适应列宽度
        # self.TWquote.resizeRowsToContents()                              # 自适应行高,这两句放最后可以等数据写入后自动适应表格数据宽度
        # self.autoadd()                                                   # 自动编序号
        # self.TWquote.hideColumn(0)                                       # 隐藏第一列
        # self.TWquote.showColumn(0)                                       #显示列
        # self.sum_amount(9)

    def sum_amount(self, l):
        """计算报价总数量,总价函数"""
        count = 0
        rows = self.TWquote.rowCount()                                    # 获取表格中的总行数,考虑到保存时有空行的情况用总行数.
        for i in range(rows):
            if not self.TWquote.item(i,l):                                #把缺省值和空值设为0 
                count += 0
            elif self.TWquote.item(i,l).text()=="":
                count += 0
            else:
                count += int(self.TWquote.item(i,l).text())
        print('sum_count=' +str(count))
        return count

    # def sum_amount(self):
    # @pyqtSlot()
    # def on_PBquery_clicked(self):
    #     """计算报价总数量,总价"""
    #     count_1 = self.sum_amount(5)                                       #计算第5列数量
    #     print('count_1=' +str(self.sum_amount(5)))
    #     self.lineEdit_2.setText(str(count_1))                              # 添加计算结果到总数量框
    #     count_2 = self.sum_amount(9)
    #     print('count_2=' +str(self.sum_amount(9)))                          #计算第9列总价
    #     self.lineEdit_3.setText(str(count_2))                               # 添加计算结果到总价框

        # count = 0
        # rows = self.TWquote.rowCount()                                    # 获取表格中的总行数,考虑到保存时有空行的情况用总行数.
        # for i in range(rows):
        #     if not self.TWquote.item(i,5):                                #把缺省值和空值设为0 
        #         count += 0
        #     elif self.TWquote.item(i,5).text()=="":
        #         count += 0
        #     else:
        #         count += int(self.TWquote.item(i,5).text())
        # print('s=' +str(count))
        # self.lineEdit_2.setText(str(count)) # 添加计算结果到总数量框

    @pyqtSlot(int, int, int, int)
    def on_TWquote_currentCellChanged(self, currentRow, currentColumn, previousRow, previousColumn):
        """变更指定列值重新计算数量和总价"""    
        print('列=' +str(previousColumn))
        if previousColumn == 5:                                                #改动后的列索引=数量列
            count_1 = self.sum_amount(5)                                       #计算第5列数量
            print('count_1=' +str(self.sum_amount(5)))
            self.lineEdit_2.setText(str(count_1))                              # 添加计算结果到总数量框
        if previousColumn == 9:                                                #改动后的列索引=总价列
            count_2 = self.sum_amount(9)
            print('count_2=' +str(self.sum_amount(9)))                          #计算第9列总价
            self.lineEdit_3.setText(str(count_2))                               # 添加计算结果到总价框


    def autoadd(self):
        """
        序号自动编号
        """
        rows = self.TWquote.rowCount()                                    # 获取表格中的总行数
        for i in range(rows):
            xh = '%d'% (i+1)
            self.TWquote.setItem(i, 0, QTableWidgetItem(xh))

    def right_menu(self, pos):#右键菜单
        """
        右键菜单2
        """
        pmenu = QMenu(self)
        pInsertAct = QAction(u"插入行",self.TWquote)
        pDeleteAct = QAction(u"删除行",self.TWquote)
        pHideAct = QAction(u"隐藏列",self.TWquote)
        pMergeAct = QAction(u"合并单元格",self.TWquote)
        pmenu.addAction(pInsertAct)
        pmenu.addAction(pDeleteAct)
        pmenu.addAction(pHideAct)
        pmenu.addAction(pMergeAct)
        pmenu.popup(QtGui.QCursor.pos())                     #在鼠标光标位置显示
        pInsertAct.triggered.connect(self.add_onerow)
        pDeleteAct.triggered.connect(self.ondelselect)
        pHideAct.triggered.connect(self.onhide)
        pMergeAct.triggered.connect(self.onmergecolumn)
    
    def add_onerow(self): # 当前插入一行
        """
        插入一行
        """
        r = self.TWquote.currentIndex().row()
        # print('r=' +str(r))
        self.TWquote.insertRow(r) #在h位置插入一空行

    def add_rows(self): # 插入多行???
        """
        插入多行========================存在序号就会按光标所在行的序号插入行数,待解决(可以考虑光标焦点)?????
        """
        rows = self.TWquote.rowCount()# 获取表格中的总行数
        for i in self.TWquote.selectionModel().selection().indexes():
            rownum = i.row()
        print('i=' +str(rownum))
        #在末尾插入空行
        self.TWquote.setRowCount(rows + rownum)

    def ondelselect(self): # 删除所选行数据
        """
        删除所选行
        """
        ret = QMessageBox.warning(self.TWquote, u'警告', u'是否删除所选行?', QMessageBox.Yes|QMessageBox.No)
        if ret == QMessageBox.Yes:
            select_rows = set()
            for rg in self.TWquote.selectedRanges():
                for i in range(rg.topRow(),rg.bottomRow()+1):
                    select_rows.add(i)
            select_rows = list(select_rows)
            print('r' +str(select_rows))
            select_rows.sort(reverse=True) # 分类反转
            for index in select_rows:
                self.TWquote.removeRow(index)
            pass
        else:
            return

    def onhide(self):
        """隐藏列"""
        c = self.TWquote.currentIndex().column()
        print('隐藏' +str(c) +'列')
        self.TWquote.hideColumn(c) #隐藏c列

    def onmergecolumn(self):
        """合并单元格"""
        print('合并' +'单元格')

    @pyqtSlot()
    def on_PBsave_clicked(self): #保存(self,cur,db,col_lst)
        """
        保存报价数据
        """
        db = pymysql.connect(host='127.0.0.1', port=3308, user='root', password='root', db='mrp',charset='utf8',)
        cur = db.cursor()
        row_1 = self.TWquote.rowCount()                                  #表格行数
        value_lst = [] 
        for h in range(row_1):                                        
            if not self.TWquote.item(h,0):                                   #从0行开始找出空值所在行
                print('h=' +str(h))
                break                                                        #跳出循环
        try:
            for k in range(h):                                                   #从0行到最大数据行循环
                value_lst.append(self.CBcorporate.currentText())                      #公司名称加入数组
                value_lst.append(self.quotationNo.text())                        #报价单号加入数组
                for i in range(15):                                              #从i到15个字段数量的循环range(len(col_lst))
                    if self.TWquote.item(k,i) == None:                           #把空值设为NULL
                        value_lst.append(None)
                    else:
                        value_lst.append(self.TWquote.item(k,i).text())
                print('value_lst2=' +str(value_lst))
                cur.execute(
                    "INSERT INTO quote VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",value_lst)
                del value_lst[:]                                                 #删除原数组的所有元素
            print('成功修改', cur.rowcount, '条数据')
            cur.close()
            db.commit()
            QMessageBox.about(self,"保存成功","报价保存成功!")
        except:
            db.rollback()
        db.close()                                                 

    @pyqtSlot()
    def on_PBnew_clicked(self): #导入Excel
        """打开Excel文件,导入报价明细表中"""

        #需要增加先清除原来数据代码
        openfile_name = QFileDialog.getOpenFileName(self,'选择文件','C:/Users/Administrator/Desktop/','Excel files(*.xlsx , *.xls)')
        global path_openfile_name
        path_openfile_name = openfile_name[0]
        ###===========读取表格，转换表格，===========================================
        if len(path_openfile_name) > 0:
            df = pd.read_excel(path_openfile_name)
            input_table = df.fillna(0)# 将NaN替换为0
            # input_table = df.where(df.notnull(), None)# 将NaN替换为None
            input_table_rows = input_table.shape[0]
            input_table_colunms = input_table.shape[1]
            # input_table_header = input_table.columns.values.tolist()
        ###======================给tablewidget设置行列表头============================
            # self.TWquote.setColumnCount(input_table_colunms)
            # self.TWquote.setRowCount(input_table_rows)
            # self.TWquote.setHorizontalHeaderLabels(input_table_header)
        ###================遍历表格每个元素，同时添加到tablewidget中========================
            for i in range(input_table_rows):
                input_table_rows_values = input_table.iloc[[i]]   # iloc：通过行和列的下标来访问数据
                input_table_rows_values_array = np.array(input_table_rows_values)
                input_table_rows_values_list = input_table_rows_values_array.tolist()[0]
                for j in range(input_table_colunms):
                    input_table_items_list = input_table_rows_values_list[j]
        ###==============将遍历的元素添加到tablewidget中并显示=======================
                    input_table_items = str(input_table_items_list)
                    newItem = QTableWidgetItem(input_table_items) 
                    newItem.setTextAlignment(Qt.AlignHCenter|Qt.AlignVCenter)
                    self.TWquote.setItem(i, j, newItem)  
        else:
            self.centralWidget.show()
        self.TWquote.resizeColumnsToContents()

class QuoteExamine(QWidget, Ui_Quote_check):
    """
    报价审核类
    """
    def __init__(self, parent=None):
        super(QuoteExamine, self).__init__(parent)
        self.setupUi(self)
        self.quotelist() 
   
        #连接槽
        self.Quote_list.itemClicked.connect(self.querydetail)  #点击报价目录,显示选择的报价明细
        self.Button_query.clicked.connect(self.querylist)    #  #partial(self.querycl,db)传递db

    def quotelist(self):#默认显示报价清单
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
        self.Quote_list = QTableWidget(row,vol)               #目录表
        font = QtGui.QFont('微软雅黑',9)
        self.Quote_list.horizontalHeader().setFont(font)      #设置行表头字体
        self.Quote_list.setHorizontalHeaderLabels(col_lst)    #设置标题
        self.Quote_list.verticalHeader().setVisible(False)    #左垂直表头不显示
        #设置表格颜色             
        self.Quote_list.horizontalHeader().setStyleSheet('QHeaderView::section{background:skyblue}')
        # self.Quote_list.setContextMenuPolicy(Qt.CustomContextMenu)#允许右键产生菜单
        # self.Quote_list.customContextMenuRequested.connect(self.generateMenu)#将右键绑定到槽
        self.Quote_list.setEditTriggers(QAbstractItemView.NoEditTriggers)#设置表格禁止编辑
        self.Quote_list.setSelectionBehavior(QAbstractItemView.SelectRows)#设置整行选中
        splitter = QtWidgets.QSplitter(QtCore.Qt.Vertical)                    #设置分割条
        self.Quote_list.setFrameStyle(QtWidgets.QFrame.Box | QtWidgets.QFrame.Plain)
        #构建表格插入数据
        for i in range(row):                                      #i到row-1的数量
            for j in range(vol):
                temp_data = data[i][j]                            # 临时记录，不能直接插入表格
                data1 = QTableWidgetItem(str(temp_data))          # 转换后可插入表格
                self.Quote_list.setItem(i, j, data1)
        # self.Quote_list.resizeColumnsToContents()             #自适应宽度
        self.Quote_list.resizeRowsToContents()                #自适应行高,这两句放最后可以等数据写入后自动适应表格数据宽度
        self.Quote_list.horizontalHeader().setStretchLastSection(True)#最后一列对齐边框
        splitter.addWidget(self.Quote_list)
        self.verticalLayout.addWidget(splitter)                 

        # 报价明细区域
        cur_3 = db.cursor()
        sql = "SELECT * FROM 报价明细"
        cur_3.execute(sql)
        data_3 = cur_3.fetchall()
        col_lst_3 = [tup[0] for tup in cur_3.description]
        vol_3 = len(data_3[0])                                       #获得data的列数.cur.description  len(data[0]) 
        self.Quote_detail = QTableWidget(0,vol_3)                  #初始界面显示标题不用显示明细数据,所以QTableWidget(0,vol_3) 
        font = QtGui.QFont('微软雅黑',9)
        self.Quote_detail.horizontalHeader().setFont(font)         #设置行表头字体
        self.Quote_detail.setHorizontalHeaderLabels(col_lst_3)     #设置标题
        self.Quote_detail.verticalHeader().setVisible(False)       #左垂直表头不显示
        self.Quote_detail.setObjectName("报价明细")
        self.Quote_detail.horizontalHeader().setStyleSheet('QHeaderView::section{background:skyblue}')
        self.Quote_detail.setFrameStyle(QtWidgets.QFrame.Box | QtWidgets.QFrame.Plain)
        self.Quote_detail.resizeColumnsToContents()                #自适应宽度
        self.Quote_list.resizeRowsToContents()
        # self.Quote_detail.horizontalHeader().setStretchLastSection(True)#最后一列对齐边框
        self.Quote_detail.setFrameStyle(QtWidgets.QFrame.Box | QtWidgets.QFrame.Plain)
        splitter.addWidget(self.Quote_detail)
        self.verticalLayout.addWidget(splitter)
        # self.setLayout(self.verticalLayout)                      ##加这行后查询后可以更新,不用再addwidget,待搞明白?


    def querylist(self):#查询报价单明细
        self.Quote_list.clearContents                    #clearContents清除内容,clear清空表格中所有内容（包含表头）
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
        self.Quote_list.setRowCount(row_2)              #取查询到数据的行数,设表格行数
        for i in range(row_2):                              #i到row-1的数量
            for j in range(vol_2):
                temp_data = data_2[i][j]                    # 临时记录，不能直接插入表格
                data2 = QTableWidgetItem(str(temp_data))    # 转换后可插入表格
                self.Quote_list.setItem(i, j, data2)

    def querydetail(self):#查询报价明细    querydt(self, item)
        # print('you selected => '+ item.text())
        # self.Line_search.setText(item.text())                    #搜索框等于点击表格的值
        h = self.Quote_list.currentIndex().row()               #找到所选行的行数h
        bjdh = self.Quote_list.item(h, 0).text()               #找到所选h行的0位报价单号
        db = pymysql.connect(host='127.0.0.1', port=3308, user='root', password='root', db='mrp',charset='utf8',)
        cur_3 = db.cursor()
        sql = "SELECT * FROM 报价明细 WHERE 报价单号 LIKE '%"+bjdh+"%'"   #'%"+bjdh+"%'"
        cur_3.execute(sql)
        self.Quote_detail.clearContents()                         #清除表内数据
        data_3 = cur_3.fetchall()
        col_lst_3 = [tup[0] for tup in cur_3.description]
        row_3 = len(data_3)                                          #获得data的行数
        vol_3 = len(data_3[0])                                       #获得data的列数.cur.description  len(data[0]) 
        self.Quote_detail.setRowCount(row_3)
        # self.Quote_list.setColumnCount(0)
        #构建表格插入数据
        for i in range(row_3):                                       #i到row-1的数量
            for j in range(vol_3):
                temp_data = data_3[i][j]                           # 临时记录，不能直接插入表格
                data3 = QTableWidgetItem(str(temp_data))           # 转换后可插入表格
                self.Quote_detail.setItem(i, j, data3)
        self.Quote_detail.resizeColumnsToContents()              #自适应宽度
        # self.Quote_detail.resizeRowsToContents()                 #自适应行高
        self.Quote_detail.horizontalHeader().setStretchLastSection(True)#最后一列对齐边框
        
    def up_data(self):#审核通过
        h = self.Quote_list.currentIndex().row()          #找到所选行的行数h
        bjdh = self.Quote_list.item(h, 0).text()          #找到所选h行的0位报价单号
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
    ui = QuoteExamine()
#    ui.setupUi(Offer_Home)
    ui.show()
    sys.exit(app.exec_())

