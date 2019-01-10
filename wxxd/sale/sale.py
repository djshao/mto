# -*- coding: utf-8 -*-
"""
销售功能模块
"""
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QColor, QBrush, QPixmap, QIcon
from PyQt5.QtCore import pyqtSignal, QObject, Qt, pyqtSlot, QDate, QDateTime
from PyQt5.QtWidgets import *
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel  # 数据库模型视图

import pymysql
from qtpandas.models.DataFrameModel import DataFrameModel
from qtpandas.views.DataTableView import DataTableWidget
import pandas as pd
from sqlalchemy import create_engine
import numpy as np
from decimal import Decimal
import time

from sale.Ui_quote_check import Ui_Quote_check
from sale.Ui_quote import Ui_Fquote
from sale.Ui_offer import Ui_offer_Form
from sale.Ui_order import Ui_WidgetOrder

from tools.mysql_conn import myMdb
from tools.tools import *
# from lib.RMB import * #人民币大写转换
# sys.path.append("..")  # 调用上级目录
# from Ui_Main import Ui_MainWindow

class Order(QWidget, Ui_WidgetOrder):
    """订单模块"""
    def __init__(self, parent=None):
        super(Order, self).__init__(parent)
        self.setupUi(self)
        self.open_order()

        self.comboBox.addItem('请选择销售代表')
        self.comboBox.setStyleSheet("QComboBox{color:red;}")
        self.comboBox.addItem(QIcon(":/png/images/Accept.png"), '吴丹')
        self.comboBox.addItem(QIcon(":/png/images/Accept.png"), '费舟亮')
        # 列表框变色
        self.comboBox.currentIndexChanged.connect(self.comboBox_currentIndexChanged)

    # 保存订单
    @pyqtSlot()
    def on_PBsave_clicked(self):
        """保存合同和订单明细"""
        if self.lineEdit_3.text() == "" or self.lineEdit_4.text() == "" or \
           self.comboBox.currentText() == "请选择销售代表":
            QMessageBox.about(self, "注意", "数据不能为空,返回修改!")
            return
        button = QMessageBox.question(self, "注意", "将要保存订单,确定无误按OK继续,按Cancel退出",
                                      QMessageBox.Ok|QMessageBox.Cancel, QMessageBox.Ok)
        if button == QMessageBox.Cancel:
            return
        rows = self.TW_order.rowCount()  # 总行数
        cols = self.TW_order.columnCount()  # 总列数
        filed = '生产编号,合同编号,买方,序号,名称,制造标准,规格型号,材质,数量,工作令号,件号,单价,小计,单重,交货期,备注,材料编码'
        preSql = "insert into order_list ("+filed+")"
        subSql = "values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        sql = preSql+subSql  # 前后相加成一个完整的sql
        param = []  # 建传入值的列表
        for row in range(rows):
            # if not self.TW_order.item(row, 0):  # 从0行开始找出空值所在行
            #     break # 跳出循环
            # elif self.TW_order.item(row, 0).text() == "":  #从0行开始找出空值所在行
            #     break
            if self.TW_order.item(row, 0).text() != "":
                # for k in range(row):
                value_list = []
                value_list.append(self.lineEdit_3.text())  # 生产编号加入数组
                value_list.append(self.lineEdit_4.text())  # 合同编号
                value_list.append(self.lineEdit_2.text())  # 买方
                for i in range(cols):
                    # 把None和空值的数字格设为0值
                    if not self.TW_order.item(row, i):
                        value_list.append("0")
                    elif self.TW_order.item(row, i).text() == "":
                        value_list.append("0")
                    else:
                        value_list.append(self.TW_order.item(row, i).text())
                param.append(value_list)
            else:
                pass
        rowcount = myMdb().insert_many(sql, param)
        # 保存订单汇总==============================================================
        myMdb().insert(
                        table='orders',
                        买方=self.lineEdit_2.text(),
                        生产编号=self.lineEdit_3.text(),
                        合同编号=self.lineEdit_4.text(),
                        签订日期=self.lineEdit_5.text(),
                        总数量=self.lineEdit_6.text(),
                        总金额=self.lineEdit_7.text(),
                        销售代表=self.comboBox.currentText(),
                        交货地点=self.lineEdit.text())
        QMessageBox.about(self, "保存成功", "保存了"+str(rowcount)+"条订单记录")

    def open_order(self):
        """打开订单-->初始化订单表格"""
        self.TW_order.blockSignals(True)
        #设置表格设置初始500行
        self.TW_order.setRowCount(500)
        # 设置标题
        # self.TWquote.setHorizontalHeaderLabels(input_table_header)
        # 设置每格为空值
        for i in range(500):
            for j in range(14):
                new_item = QTableWidgetItem("")
                new_item.setTextAlignment(Qt.AlignHCenter|Qt.AlignVCenter)
                self.TW_order.setItem(i, j, new_item)
        # 设置行表头字体
        font = QtGui.QFont('微软雅黑', 9)
        self.TW_order.horizontalHeader().setFont(font)
        # 左垂直表头不显示
        self.TW_order.verticalHeader().setVisible(False)
        # 只能选择单行
        self.TW_order.setSelectionMode(QAbstractItemView.SingleSelection)
        # 设置表格颜色             
        self.TW_order.horizontalHeader().setStyleSheet('QHeaderView::section{background:skyblue}')
        self.TW_order.setFrameStyle(QtWidgets.QFrame.Box | QtWidgets.QFrame.Plain)
        # 设置订单lneedit文本框显示当前日期
        self.lineEdit_5.setText(time.strftime("%Y-%m-%d", time.localtime()))
        # 设置文本框无边框
        styleSheet = "background:transparent;border-width:0;border-style:outset"
        self.lineEdit_1.setStyleSheet(styleSheet)
        self.lineEdit_2.setStyleSheet(styleSheet)
        self.lineEdit_3.setStyleSheet(styleSheet)
        self.lineEdit_4.setStyleSheet(styleSheet)
        self.lineEdit_5.setStyleSheet(styleSheet)
        self.lineEdit_6.setStyleSheet(styleSheet)
        self.TW_order.blockSignals(False)

    #点击查询按钮事件
    @pyqtSlot()
    def on_PBquery_clicked(self):
        """查询报价单-->生成生产合同明细"""
        self.TW_order.blockSignals(True)  # 暂停单元格修改信号
        bjdh = self.Line_search.text()
        if bjdh == "":
            data = myMdb().fetchall(table='quote')
        else:
            data = myMdb().fetchall(table='quote', where='报价单号='+bjdh)
        if len(data) == 0:
            QMessageBox.warning(self, '查询出错', '没有查到报价记录')
            return
        row = len(data)
        vol = len(data[0])
        # 构建表格插入数据
        self.lineEdit_2.setText(str(data[0][0]))
        for i in range(row):
            for j in range(1, vol-5):
                temp_data = data[i][j]
                data1 = QTableWidgetItem(str(temp_data))
                self.TW_order.setItem(i, j-2, data1)
        self.TW_order.resizeColumnsToContents()             # 自适应宽度
        self.TW_order.resizeRowsToContents()                  # 自适应行高
        self.TW_order.horizontalHeader().setStretchLastSection(True)  # 最后一列对齐边框
        # 汇总数量金额--总金额栏2位小数
        count_1 = plusColumn(self, "TW_order", 5).quantize(Decimal('0'))
        self.lineEdit_6.setText(str(count_1))
        count_2 = plusColumn(self, "TW_order", 9).quantize(Decimal('0.00'))
        self.lineEdit_7.setText(str(count_2))
        self.TW_order.blockSignals(False)  # 恢复单元格修改信号
        # 导入后开启单元格变更事件,比暂停信号要好.  但传参数错误,待研究??????????
        # self.TW_order.cellChanged.connect(lambda: self.TW_order_cellChanged(int, int))

    # 右键菜单
    def contextMenuEvent(self, event):
        """系统自带右键菜单事件:"""
        pmenu = QMenu(self)
        insertAct = QAction(u"插入行", self.TW_order)
        # deleteAct = QAction(u"删除行", self.TWquote)
        pmenu.addAction(insertAct)
        # pmenu.addAction(deleteAct)
        pmenu.popup(QtGui.QCursor.pos())  #在鼠标光标位置显示pmenu.popup(self.mapToGlobal(event.pos()))
        insertAct.triggered.connect(self.add_onerow)
        # deleteAct.triggered.connect(self.ondelselect)

    def add_onerow(self):
        """当前位置插入一行"""
        r = self.TWquote.currentIndex().row()
        # 在r位置插入一空行
        self.TW_order.insertRow(r)
        # 给插入的行设置空值
        for j in range(15):
            newItem = QTableWidgetItem(0)
            newItem.setTextAlignment(Qt.AlignHCenter|Qt.AlignVCenter)
            self.TW_order.setItem(r, j, newItem)

    # @pyqtSlot()
    def comboBox_currentIndexChanged(self):
        """列表框变色"""
        if self.comboBox.currentText() != "请选择销售代表":
            self.comboBox.setStyleSheet("QComboBox{color:black;}")
        else:
            self.comboBox.setStyleSheet("QComboBox{color:red;}")

    @pyqtSlot(int, int)
    def on_TW_order_cellChanged(self, row, col):
        """订单明细修改变更事件-->红色显示修改\重新计算数量价格"""
        items = self.TW_order.item(row, col)
        txt = items.text()
        self.TW_order.blockSignals(True)  # 暂停单元格修改信号
        # 字体颜色（红色）
        # item.setForeground(QBrush(QColor(255, 0, 0)))
        # 背景颜色（红色）
        self.TW_order.item(row, col).setBackground(QBrush(QColor(255, 0, 0)))
        self.TW_order.blockSignals(False)  # 启动单元格修改信号
        # 重新计算
        if col == 5 or col == 8:
            number = int(self.TW_order.item(row, 5).text())
            price = Decimal(str(self.TW_order.item(row, 8).text()))
            amount = Decimal(number*price)
            self.TW_order.setItem(row, 9, QTableWidgetItem(str('%.2f' % amount)))
            # 汇总列总数量/总金额,更新到lineEdit
            count_1 = plusColumn(self, "TW_order", 5).quantize(Decimal('0'))
            self.lineEdit_6.setText(str(count_1))
            # 添加计算结果到总金额栏,2位小数
            count_2 = plusColumn(self, "TW_order", 9).quantize(Decimal('0.00'))
            self.lineEdit_7.setText(str(count_2))
        # 被修改单元格的列标题
        # lie = self.TW_order.horizontalHeaderItem(col).text()
        # record = '%s:%s修改为%s,'%(lie, table_value, txt)
        # xgjl = 'concat(修改记录,'+"'"+record+"'"+')'

    def offer(self): # pandas
        # self.offerwidget = DataTableWidget()
        # widget = self.offerwidget
        # widget.resize(600, 500) # 如果对部件尺寸大小不满意可以在这里设置

        # self.model = DataFrameModel() # 设置新的模型
        # widget.setViewModel(self.model)

        # #测试插入时间
        # start = time.clock()
        # # MySQL法连接数据库,读取数据需要转换
        # conn = pymysql.connect(host='localhost', port=3308,user='root',password='root',db='mrp',charset='utf8')
        # sql = 'select * from PP'
        # self.df = pd.read_sql(sql, con=conn)

        # 通过SQLAlchemy法.create_engine建立连接引擎,可以直接创建dataframe
        # engine = create_engine('mysql+pymysql://root:root@localhost:3308/mrp')
        # sql = 'select * from PP'
        # self.df = pd.read_sql(sql, engine)
        # self.df.to_sql(name='user',con=engine,if_exists='append',index=False)  写入数据库
        # df.to_sql(目标表名,con=engine, schema=数据库名, index=False, index_label=False, if_exists='append', chunksize=1000)
        # pd.io.sql.to_sql(df,table_name,con=conn,schema='w_analysis',if_exists='append') 两个语句???

        # self.df = pd.read_excel(r'C:/Users/Administrator/Desktop/报价模板.xlsx',encoding='utf-8')
        # self.df_original = self.df.copy() # 备份原始数据
        # self.model.setDataFrame(self.df)
        # end = time.clock()
        # print('[insert_many executemany] Time Usage:',end-start)

        # d = self.df.loc[:,'num'].sum()
        # d = sum(self.df['单重'])
        # print('d' +str(d))
        # self.df.apply(sum)
        # column_sum = self.df.iloc[:,j].sum()

        """
        # 查询数据并转为pandas.DataFrame，指定DataFrame的index为数据库中的id字段
        df = pd.read_sql('SELECT * FROM students', engine, index_col='id')
        print(df)
        # 修改DataFrame中的数据（移除age列）
        dft = df.drop(['age'], axis=1)
        # 将修改后的数据追加至原表,index=False代表不插入索引，因为数据库中id字段为自增字段
        dft.to_sql('students', engine, index=False, if_exists='append')
        """

        #定义函数，自动输出DataFrme数据写入mysql的数类型字典表,配合to_sql方法使用(注意，其类型只能是SQLAlchemy type )
        # @pyqtSlot()
        # def on_pushButton_2_clicked(self):
        # def mapping_df_types(df):
        """自动获取DataFrme各列的数据类型，生成字典。"""
        # dtypedict = {}
        # for i, j in zip(df.columns, df.dtypes):
        #     if "object" in str(j):
        #         dtypedict.update({i: VARCHAR(256)})
        #     if "float" in str(j):
        #         dtypedict.update({i: NUMBER(19,8)})
        #     if "int" in str(j):
        #         dtypedict.update({i: VARCHAR(19)})
        # return dtypedict
        # print(dtypedict)

        #data_base.to_sql('stock_class',engine,index=False,if_exists='append',dtype=dtypedict,chunksize=100)参考

        # @pyqtSlot()
        # def on_pushButton_clicked(self):
        #     """
        #     初始化pandas
        #     """
        #     self.model.setDataFrame(self.df_original)
        
        # @pyqtSlot()
        # def on_pushButton_2_clicked(self):
        #     """
        #     保存数据
        #     """
        #     # self.df.to_excel(r'./data/fund_data_new.xlsx')
        #     engine = create_engine('mysql+pymysql://root:root@localhost:3308/mrp')
        #     self.df.to_sql(name='test',con=engine,if_exists='append',index=False)#index=False自增型关键字用false默认为True，指定DataFrame的index是否一同写入数据库
        #     # con.dispose() # engine.dispose()


class Quote(QWidget, Ui_Fquote):
    """报价类"""
    def __init__(self, parent=None):
        super(Quote, self).__init__(parent)
        self.setupUi(self)
        #设置报价lneedit文本框显示当前日期
        self.quotedate.setText(time.strftime("%Y-%m-%d", time.localtime()))

        #公司名称下拉列表框
        result = myMdb().fetchall(field='公司名称', table='客户资料表')
        # vol = len(result[0])
        # 循环取元祖数据,转为列表
        col_lst = [tup[0] for tup in result]
        self.CBcorporate.insertItem(0, "请选择公司名称")
        self.CBcorporate.addItems(col_lst)

        #设置表格设置初始11行
        self.TWquote.setRowCount(500)
        # 设置标题
        # self.TWquote.setHorizontalHeaderLabels(input_table_header)
        # 设置每格为空值
        for i in range(500):
            for j in range(15):
                new_item = QTableWidgetItem("")
                new_item.setTextAlignment(Qt.AlignHCenter|Qt.AlignVCenter)
                self.TWquote.setItem(i, j, new_item)
        #表格格式设置
        self.TWquote.horizontalHeader().setStyleSheet('QHeaderView::section{background:skyblue}')
        self.TWquote.setContextMenuPolicy(Qt.CustomContextMenu)            # 允许右键产生菜单
        self.TWquote.customContextMenuRequested.connect(self.right_menu)    # 将右键绑定到槽
        # self.TWquote.setSelectionBehavior(QAbstractItemView.SelectRows)  # 设置整行选中
        self.TWquote.verticalHeader().setVisible(False)                    # 左垂直表头不显示
        # self.TWquote.setEditTriggers(QAbstractItemView.AnyKeyPressed)    # 设置表格任何时候都能修改
        self.TWquote.horizontalHeader().setStretchLastSection(True)        #最后一列对齐边框
        # self.TWquote.horizontalHeader().setResizeMode(QHeaderView.Stretch)
        # self.TWquote.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch) #占满屏幕,平均分配列宽
        self.TWquote.resizeColumnsToContents()                             # 自适应列宽度
        # self.TWquote.resizeRowsToContents()                              # 自适应行高
        # self.autoadd()                                                   # 自动编序号
        # self.TWquote.hideColumn(0)                                       # 隐藏第一列
        # self.TWquote.showColumn(0)                                       # 显示第一列
        #设置文本框无边框
        styleSheet = "background:transparent;border-width:0;border-style:outset"
        self.quotationNo.setStyleSheet(styleSheet)
        self.contact.setStyleSheet(styleSheet)
        self.lineEdit_5.setStyleSheet(styleSheet)
        self.lineEdit_6.setStyleSheet(styleSheet)
        self.lineEdit_8.setStyleSheet(styleSheet)
        self.lineEdit_9.setStyleSheet(styleSheet)
        self.quotedate.setStyleSheet(styleSheet)
        self.total_price.setStyleSheet(styleSheet)
        self.total_quantity.setStyleSheet(styleSheet)
        self.add_quote_No()
        # self.TWquote.cellChanged.connect(self.cell_changed)

    #点击查询按钮事件
    @pyqtSlot()
    def on_PBquery_clicked(self):
        # 点击查询后计算单价总价
        self.calculate()

    # 单价/总价计算
    def calculate(self):
        rows = self.TWquote.rowCount()                                       # 保存时有空行的情况用总行数.
        # 判断有数据的行数h,空值就退出循环
        for h in range(rows):
            if not self.TWquote.item(h, 0):
                break #跳出循环
            elif self.TWquote.item(h, 0).text() == "":
                break
        for i in range(h+1):
            quantity = int(self.TWquote.item(i, 5).text())                     # 数量quantity
            if self.TWquote.item(i, 10).text() == "":
                weight = 0
            else:
                weight = Decimal(str(self.TWquote.item(i, 10).text()))        # 单重unit weight
            if self.TWquote.item(i, 11).text() == "":
                weight_price = 0
            else:
                weight_price = Decimal(str(self.TWquote.item(i, 11).text()))   # 公斤价weight price
            if self.TWquote.item(i, 12).text() == "":
                cost = 0
            else:
                cost = Decimal(str(self.TWquote.item(i, 12).text()))            # 加工费cost
            if self.TWquote.item(i, 13).text() == "":
                expenses = 0
            else:
                expenses = Decimal(str(self.TWquote.item(i, 13).text()))        # 其他费用expenses
            # 计算单价    单价=单重*公斤价+加工费+其他费用
            if self.TWquote.item(i, 11).text() == "":
                price = Decimal(str(self.TWquote.item(i, 8).text()))
            else:
                price = weight*weight_price+cost+expenses
            self.TWquote.setItem(i, 8, QTableWidgetItem(str('%.2f' % price)))    #设置单价小数点2位
            amount = Decimal(quantity*price)                                     #总价amount=数量*单价
            self.TWquote.setItem(i, 9, QTableWidgetItem(str('%.2f' % amount))) 
            count_1 = self.sum_amount(5)
            self.total_quantity.setText(str(count_1.quantize(Decimal('0'))))   # 添加计算结果到总数量栏,0位小数
            count_2 = self.sum_amount(9)
            self.total_price.setText(str(count_2.quantize(Decimal('0.00'))))    # 添加计算结果到总价栏,2位小数

    # 计算列值总数函数
    def sum_amount(self, l):
        """计算所选列的总数,l为列数"""
        count = 0
        # 获取表格中的总行数,考虑到保存时有空行的情况用总行数.
        rows = self.TWquote.rowCount()
        for i in range(rows):
            # 判断不存在和空值,并设为0值
            if not self.TWquote.item(i, l):
                count += 0
            elif self.TWquote.item(i, l).text() == "":
                count += 0
            else:
                count += Decimal(self.TWquote.item(i, l).text())
            print(i)
        return count

    def cell_changed(self, row, col):  # 参考后删除
        """单元格变更后事件"""
        item = self.TWquote.item(row, col)
        txt = item.text()
        item.setForeground(QBrush(QColor(255, 0, 0)))
        # self.settext('第%s行，第%s列 , 数据改变为:%s'%(row,col,txt))
        print('第%s行，第%s列 , 数据改变为:%s'%(row,col,txt))

    # 当单元格的焦点变化时，重新计算数量和总价
    # @pyqtSlot(int, int, int, int)
    # def on_TWquote_currentCellChanged(self, currentRow, currentColumn, previousRow, previousColumn):
        # if previousColumn == 5:                                                #改动后的列索引=数量列
        #     count_1 = self.sum_amount(5)                                       #计算第5列数量
        #     self.total_quantity.setText(str(count_1.quantize(Decimal('0'))))   # 添加计算结果到总数量栏,0位小数
        #     # self.money.setText(str(cncurrency(int(count_2))))                # 添加人民币大写

    # 自动增加序号
    def autoadd(self):
        """序号自动编号"""
        rows = self.TWquote.rowCount()  # 获取表格中的总行数
        for i in range(rows):
            xh = '%d'% (i+1)
            self.TWquote.setItem(i, 0, QTableWidgetItem(xh))

    # 右键菜单
    def right_menu(self, pos):
        """右键菜单def contextMenuEvent(self, event):"""
        pmenu = QMenu(self)
        pInsertAct = QAction(u"插入行", self.TWquote)
        pInsertsAct = QAction(u"插入多行", self.TWquote)
        pDeleteAct = QAction(u"删除行", self.TWquote)
        pHideAct = QAction(u"隐藏列", self.TWquote)
        pMergeAct = QAction(u"合并单元格", self.TWquote)
        pmenu.addAction(pInsertAct)
        pmenu.addAction(pInsertsAct)
        pmenu.addAction(pDeleteAct)
        pmenu.addAction(pHideAct)
        pmenu.addAction(pMergeAct)
        pmenu.popup(QtGui.QCursor.pos())  #在鼠标光标位置显示pmenu.popup(self.mapToGlobal(event.pos()))
        pInsertAct.triggered.connect(self.add_onerow)
        pInsertsAct.triggered.connect(self.add_rows)
        pDeleteAct.triggered.connect(self.ondelselect)
        pHideAct.triggered.connect(self.onhide)
        pMergeAct.triggered.connect(self.onmergecolumn)

    # 当前位置插入一行
    def add_onerow(self):
        r = self.TWquote.currentIndex().row()
        # print('r=' +str(r))
        self.TWquote.insertRow(r) #在r位置插入一空行
        for j in range(15):# 给插入的行设置空值
            newItem = QTableWidgetItem(0)
            newItem.setTextAlignment(Qt.AlignHCenter|Qt.AlignVCenter)
            self.TWquote.setItem(r, j, newItem)

    # 插入多行=======??????
    def add_rows(self):
        """清除数据"""
        rows = self.TWquote.rowCount()# 获取表格中的总行数
        for i in self.TWquote.selectionModel().selection().indexes():
            rownum = i.row()
        #在末尾插入空行
        self.TWquote.setRowCount(rows + rownum)

    # 清除所选的数据,现在是连行都删除,考虑只清除数据的情况是否合适???????????
    def del_select(self):
        """清除数据"""
        ret = QMessageBox.warning(self.TWquote, u'警告', u'是否删除所选行?', QMessageBox.Yes|QMessageBox.No)
        if ret == QMessageBox.Yes:
            for rg in self.TWquote.selectedRanges():
                new_item = QTableWidgetItem("")
                for i in range(rg.topRow(), rg.bottomRow()+1):
                    # print('top' +str(rg.topRow()))
                    # print(rg.bottomRow())
                    self.TWquote.setItem(i, 3, new_item)

    # 删除所选行
    def ondelselect(self):
        """删除所选行及数据"""
        ret = QMessageBox.warning(self.TWquote, u'警告', u'是否删除所选行?', QMessageBox.Yes|QMessageBox.No)
        if ret == QMessageBox.Yes:
            select_rows = set()
            for rg in self.TWquote.selectedRanges():
                for i in range(rg.topRow(), rg.bottomRow()+1):
                    select_rows.add(i)
            select_rows = list(select_rows)
            # print('r' +str(select_rows))
            select_rows.sort(reverse=True)  # 分类反转
            for index in select_rows:
                self.TWquote.removeRow(index)
        else:
            return

    # 隐藏列 还要增加还原隐藏的功能==================================????
    def onhide(self):
        """隐藏列"""
        c = self.TWquote.currentIndex().column()
        print('隐藏' +str(c) +'列')
        self.TWquote.hideColumn(c) #隐藏c列

    # 合并单元格
    def onmergecolumn(self):
        """合并单元格"""
        print('合并' +'单元格')

    # 生成报价单号
    def add_quote_No(self):
        """自动生成报价单号"""
        # 格式化当前日期+后两位
        date = time.strftime("%y%m%d", time.localtime()) + "00"
        bj = myMdb().fetchone(field='max(报价单号)', table='quote', where="报价单号>"+date)
        if bj[0] is None:
            bjdh = int(date) + 1
        else:
            bjdh = bj[0] + 1
        self.quotationNo.setText(str(bjdh))

    # 保存报价
    @pyqtSlot()
    def on_PBsave_clicked(self):  # save_quote
        """保存报价明细和汇总"""
        if self.CBcorporate.currentText() == "请选择公司名称":
            QMessageBox.warning(self, '警告', '公司名称未选择')
            return
        # 保存报价明细
        rows = self.TWquote.rowCount()  # 总行数
        cols = self.TWquote.columnCount()  # 总列数
        for h in range(rows+1):
            if not self.TWquote.item(h, 0):  # 从0行开始找出空值所在行
                break # 跳出循环
            elif self.TWquote.item(h, 0).text() == "":  #从0行开始找出空值所在行
                break
        preSql = "insert into quote ("  # 前一段拼接字段
        subSql = "values("              # 后一段拼接字段
        # exc = ()   # 作为execute的参数值，这是一个tuble类型
        preSql += "公司名称" + ","
        subSql += "%s,"
        preSql += "报价单号" + ","
        subSql += "%s,"
        for i in range(cols):  # 取出每一个子json的key和value值
            x = self.TWquote.horizontalHeaderItem(i).text()  # 列表头值
            preSql += x + ","  # 拼接前面sql的key值
            subSql += "%s,"   # 拼接后面sql的value数量
        preSql = preSql[0:preSql.__len__()-1] + ")"  # 去掉后面的“，”再添加“）”
        subSql = subSql[0:subSql.__len__()-1] + ")"  # 去掉后面的“，”再添加“）”
        sql = preSql+subSql  # 前后相加成一个完整的sql
        param = []  # 建传入值的列表
        for k in range(h):
            value_list = []
            value_list.append(self.CBcorporate.currentText())  # 公司名称加入数组
            value_list.append(self.quotationNo.text())
            for i in range(cols):
                if i in (10, 11, 12, 13) and self.TWquote.item(k, i).text() == "":
                    value_list.append("0")  # 把空值的数字格设为0值
                else:
                    value_list.append(self.TWquote.item(k, i).text())
                print(value_list)
            param.append(value_list)
        rowcount = myMdb().insert_many(sql, param)  # 执行SQL,返回插入的条数
        # 保存报价汇总==============================================================
        myMdb().insert(
            table='报价基本信息',
            公司名称=self.CBcorporate.currentText(),
            报价单号=self.quotationNo.text(),
            总数量=self.total_quantity.text(),
            总价=self.total_price.text(),
            业务员=self.contact.text(),
            报价日期=self.quotedate.text(),
            状态='待审核')
        QMessageBox.about(self, "保存成功", "保存了"+str(rowcount)+"条报价记录")

    # 导入excel文件
    @pyqtSlot()
    def on_PBnew_clicked(self):
        """打开Excel文件,导入到报价明细表中"""
        self.TWquote.clear
        #需要增加先清除原来数据代码
        openfile_name = QFileDialog.getOpenFileName(
            self, '选择文件', 'C:/Users/Administrator/Desktop/', 'Excel files(*.xlsx , *.xls)')
        global path_openfile_name                      # 把打开的文件名当全局变量,传导给读取表格用
        path_openfile_name = openfile_name[0]
        ###===========读取表格，转换表格，===========================================
        if len(path_openfile_name) > 0:
            df = pd.read_excel(path_openfile_name)
            input_table = df
            # input_table = df.fillna(0)                  # pandas将NaN替换为0
            # input_table = df.where(df.notnull(), None)# 将NaN替换为None
            input_table_rows = input_table.shape[0]     # numpy函数中shape函数读取矩阵第一维度的长度
            input_table_colunms = input_table.shape[1]
            # input_table_header = input_table.columns.values.tolist() # 读取标题
        ###======================给tablewidget设置行列表头============================
            # self.TWquote.setColumnCount(input_table_colunms)
            self.TWquote.setRowCount(input_table_rows)            #设置和导入数据相同行数
            # self.TWquote.setHorizontalHeaderLabels(input_table_header) # 设置标题
        ###================遍历表格每个元素，同时添加到tablewidget中========================
            for i in range(input_table_rows):
                input_table_rows_values = input_table.iloc[[i]]   # iloc：通过行和列的下标来访问数据
                input_table_rows_values_array = np.array(input_table_rows_values)
                input_table_rows_values_list = input_table_rows_values_array.tolist()[0]
                for j in range(input_table_colunms):
                    input_table_items_list = input_table_rows_values_list[j]
        ###==============将遍历的元素添加到tablewidget中并显示=======================
                    input_table_items = str(input_table_items_list)
                    if input_table_items == 'nan':
                        input_table_items = 0
                    newItem = QTableWidgetItem(input_table_items)
                    newItem.setTextAlignment(Qt.AlignHCenter|Qt.AlignVCenter)
                    # print('newitem=' +input_table_items)
                    self.TWquote.setItem(i, j, newItem)  
        else:
            self.centralWidget.show()
        self.TWquote.resizeColumnsToContents()#根据内容自动调整所有列的列宽


class QuoteExamine(QWidget, Ui_Quote_check):
    """报价审核类"""
    def __init__(self, parent=None):
        super(QuoteExamine, self).__init__(parent)
        self.setupUi(self)
        self.quote_list()

        #连接槽
        self.Quote_list.itemClicked.connect(self.query_detail)  # 点击报价清单,显示选择的报价明细
        self.Button_query.clicked.connect(self.query_list)    # 点击查询查报价清单
        self.Quote_detail.itemClicked.connect(self.outSelect)  # 报价明细区点击事件,记录前值
        self.Box_filter.currentIndexChanged.connect(self.Box_filter_currentIndexChanged)  # 报价明细区单元格变更事件

    def quote_list(self):  # 默认显示报价清单
        """审核报价清单"""
        data = myMdb().fetchall(table='报价基本信息', where="状态='待审核'")
        row = len(data)     # 获得data的行数
        vol = len(data[0])  # 获得data的列数.cur.description或len(data[0]) 
        # 插入表格
        # self.Quote_list = QTableWidget(row, vol)             # 设置row行vol列的表格
        self.Quote_list.setRowCount(row)
        font = QtGui.QFont('微软雅黑', 9)
        self.Quote_list.horizontalHeader().setFont(font)      # 设置行表头字体
        self.Quote_list.verticalHeader().setVisible(False)    # 左垂直表头不显示
        self.Quote_list.setSelectionMode(QAbstractItemView.SingleSelection)  #只能选择单行

        # 设置表格颜色             
        self.Quote_list.horizontalHeader().setStyleSheet('QHeaderView::section{background:skyblue}')
        # self.Quote_list.setContextMenuPolicy(Qt.CustomContextMenu)  # 允许右键产生菜单
        # self.Quote_list.customContextMenuRequested.connect(self.generateMenu)  # 将右键绑定到槽
        self.Quote_list.setEditTriggers(QAbstractItemView.NoEditTriggers)   # 设置表格禁止编辑
        self.Quote_list.setSelectionBehavior(QAbstractItemView.SelectRows)  # 设置整行选中
        splitter = QtWidgets.QSplitter(QtCore.Qt.Vertical)                  # 设置分割条
        self.Quote_list.setFrameStyle(QtWidgets.QFrame.Box | QtWidgets.QFrame.Plain)
        # 构建表格插入数据
        for i in range(row):                                      # i到row-1的数量
            for j in range(vol):
                temp_data = data[i][j]                            # 临时记录，不能直接插入表格
                data1 = QTableWidgetItem(str(temp_data))          # 转换后可插入表格
                self.Quote_list.setItem(i, j, data1)
        # self.Quote_list.resizeColumnsToContents()             # 自适应宽度
        self.Quote_list.resizeRowsToContents()                  # 自适应行高,放最后可以等数据写入后自动适应表格数据宽度
        self.Quote_list.horizontalHeader().setStretchLastSection(True)  # 最后一列对齐边框
        splitter.addWidget(self.Quote_list)
        self.verticalLayout.addWidget(splitter)

        # 明细区域========================================
        font = QtGui.QFont('微软雅黑', 9)
        self.Quote_detail.horizontalHeader().setFont(font)         # 设置行表头字体
        # self.Quote_detail.setHorizontalHeaderLabels(col_lst_3)     # 设置标题
        self.Quote_detail.verticalHeader().setVisible(False)       # 左垂直表头不显示
        self.Quote_detail.setObjectName("报价明细")
        self.Quote_detail.horizontalHeader().setStyleSheet(
            'QHeaderView::section{background:skyblue}')
        self.Quote_detail.setFrameStyle(QtWidgets.QFrame.Box | QtWidgets.QFrame.Plain)
        self.Quote_detail.resizeColumnsToContents()                # 自适应宽度
        # self.Quote_detail.horizontalHeader().setStretchLastSection(True)  # 最后一列对齐边框
        self.Quote_detail.setFrameStyle(QtWidgets.QFrame.Box | QtWidgets.QFrame.Plain)
        # splitter = QtWidgets.QSplitter(QtCore.Qt.Vertical)
        splitter.addWidget(self.Quote_detail)
        self.verticalLayout.addWidget(splitter)
        # self.setLayout(self.verticalLayout)           # 设置布局 加这行后查询后可以更新,不用再addwidget,待搞明白?

    def query_list(self):  # 查询报价清单
        """查询报价清单"""
        self.Quote_list.clearContents                    # clearContents清除内容,clear清空表格中所有内容（包含表头）
        lsearch = self.Line_search.text()                    # 搜索框
        # sql = "SELECT * FROM 报价基本信息 WHERE 公司名称 LIKE '%"+lsearch+"%'"   #'%"+bjdh+"%'"
        if lsearch == "":
            data_2 = myMdb().fetchall(table='报价基本信息', where="状态='待审核'")
        else:
            data_2 = myMdb().fetchall(
                table='报价基本信息',
                where="公司名称 like '%"+lsearch+"%'" + " and 状态='待审核'")
                # where="公司名称="+"'"+lsearch+"'" + "and 状态!='审核通过'")
        # print(data_2)
        if not data_2:
            QMessageBox.warning(self, '查询出错', '没有查到报价记录')
            return
        # col_lst_2 = [tup[0] for tup in curr.description]
        # print(data_2)
        row_2 = len(data_2)                                 #获得data的行数
        vol_2 = len(data_2[0])                      #获得data的列数.cur.description  len(data[0]) 
        self.Quote_list.setRowCount(row_2)                  #取查询到数据的行数,设表格行数
        for i in range(row_2):                              #i到row-2的数量
            for j in range(vol_2):
                temp_data = data_2[i][j]                    # 临时记录，不能直接插入表格
                data2 = QTableWidgetItem(str(temp_data))    # 转换后可插入表格
                self.Quote_list.setItem(i, j, data2)

    def query_detail(self):
        """查询报价明细"""
        # 暂停事件信号
        self.Quote_detail.blockSignals(True)
        # 设置下拉列表框
        self.add_combobox()
        h = self.Quote_list.currentIndex().row()       # 找到所选行的行数h
        bjdh = self.Quote_list.item(h, 1).text()       # 找到所选h行的第2列报价单号
        self.Quote_detail.clearContents()  # 清除报价明细表内数据
        data_3 = myMdb().fetchall(table='quote', where="报价单号=" +bjdh)
        row_3 = len(data_3)                            # 获得data的行数
        vol_3 = len(data_3[0])                         # 获得data的列数.cur.description len(data[0])
        self.Quote_detail.setRowCount(row_3)
        #构建表格插入数据
        for i in range(row_3):                                     # i到row-1的数量
            for j in range(vol_3):
                temp_data = data_3[i][j]                           # 临时记录，不能直接插入表格
                data3 = QTableWidgetItem(str(temp_data))           # 转换后可插入表格
                if j in (0, 1, 2, 3, 4, 5, 6, 8, 9, 11, 16):
                    data3.setFlags(QtCore.Qt.NoItemFlags)  # 禁止指定列编辑
                self.Quote_detail.setItem(i, j, data3)
        # 适应列宽/行高/最后一列对齐边框
        self.Quote_detail.resizeColumnsToContents()
        self.Quote_detail.resizeRowsToContents()
        self.Quote_detail.horizontalHeader().setStretchLastSection(True)
        # 启用事件信号
        self.Quote_detail.blockSignals(False)

    def quote_list_select(self):
        """报价清单点击显示列表框事件,有全屏退出问题"""
        # 尝试删除列表框,用于再次点击事件
        # try:
        #     self.comBox.deleteLater()
        # except:
        #     pass
        # finally:
        #     # 加单元格下拉列表框
        #     self.comBox = QComboBox()
        #     self.comBox.addItem('请选择审核结果')
        #     # 设置字体颜色
        #     self.comBox.setStyleSheet("QComboBox{color:red;}")
        #     self.comBox.addItem(QIcon(":/png/images/Accept.png"),'审核通过')
        #     self.comBox.addItem(QIcon(":/png/images/stop_32px.ico"),'退回重报')
        #     h = self.Quote_list.currentItem().row()
        #     self.Quote_list.setCellWidget(h, 6, self.comBox)

            # self.verticalLayout.addWidget(self.comBox)
            # self.setLayout(self.verticalLayout)
            # 列表框点击事件
            # self.comBox.currentIndexChanged.connect(self.combox_changed)

    # 单击一个单元格，即可获得其中的字符
    def outSelect(self, Item=None):
        """单击一个单元格，即可获得其中的字符"""
        if Item == None:
            return
        # 把table_value设为全局变量,给添加修改记录用
        global table_value
        table_value = Item.text()

    # 修改报价明细区域单元格后，设置颜色打印变更值
    @pyqtSlot(int, int)
    def on_Quote_detail_cellChanged(self, row, col):
        """报价明细修改后的变更事件-->写入变更记录"""
        # if item == None:
        #     return
        # if col == 11:
        #     return
        item = self.Quote_detail.item(row, col)
        txt = item.text()
        self.Quote_detail.blockSignals(True)  # 暂停单元格修改信号
        # 字体颜色（红色）
        # item.setForeground(QBrush(QColor(255, 0, 0)))
        # 背景颜色（红色）
        self.Quote_detail.item(row, col).setBackground(QBrush(QColor(255, 0, 0)))
        self.Quote_detail.blockSignals(False)  # 启动单元格修改信号
        # 报价单号/序号
        bjdh = self.Quote_detail.item(row, 1).text()
        xh = self.Quote_detail.item(row, 2).text()
        # 屏幕左下状态栏显示提示信息??????????????????????
        # self.statusBar().showMessage('序号%s数据改变为:%s'%(txt, xh)) 
        # 被修改单元格的列标题
        lie = self.Quote_detail.horizontalHeaderItem(col).text()
        record = '%s:%s修改为%s,'%(lie, table_value, txt)
        xgjl = 'concat(修改记录,'+"'"+record+"'"+')'
        # 重新计算汇总
        self.Quote_detail_calculate(row)
        # 更新-数据库-->
        myMdb().update(table='quote',
                        数量=self.Quote_detail.item(row, 7).text(),
                        单价=self.Quote_detail.item(row, 10).text(),
                        总价=self.Quote_detail.item(row, 11).text(),
                        单重=self.Quote_detail.item(row, 12).text(),
                        公斤价=self.Quote_detail.item(row, 13).text(),
                        加工费=self.Quote_detail.item(row, 14).text(),
                        其他费用=self.Quote_detail.item(row, 15).text(),
                        修改记录=xgjl,
                        where="报价单号="+bjdh+ " and 序号="+xh)
        # 汇总总数量/总价,更新到数据库表中
        count_1 = self.sum_amount_1(7).quantize(Decimal('0'))
        count_2 = self.sum_amount_1(11).quantize(Decimal('0'))
        myMdb().update(table='报价基本信息', 总数量=count_1, 总价=count_2, where="报价单号="+bjdh)

    def Quote_detail_calculate(self, row):
        """修改后重新计算单价/总价"""
        self.Quote_detail.blockSignals(True)  # 暂停单元格修改信号
        # 数量quantity
        quantity = int(self.Quote_detail.item(row, 7).text())
        # 单重unit weight                  
        if self.Quote_detail.item(row, 12).text() == "":
            weight = 0
        else:
            weight = Decimal(str(self.Quote_detail.item(row, 12).text()))
        # 公斤价weight price
        if self.Quote_detail.item(row, 13).text() == "":
            weight_price = 0
        else:
            weight_price = Decimal(str(self.Quote_detail.item(row, 13).text()))
        # 加工费cost
        if self.Quote_detail.item(row, 14).text() == "":
            cost = 0
        else:
            cost = Decimal(str(self.Quote_detail.item(row, 14).text()))
        # 其他费用expenses
        if self.Quote_detail.item(row, 15).text() == "":
            expenses = 0
        else:
            expenses = Decimal(str(self.Quote_detail.item(row, 15).text()))
        # 计算单价    公斤价="0.00或0时直接用单价,需要转化字符类型再==
        if float(self.Quote_detail.item(row, 13).text()) == float(0.00):
            price = Decimal(str(self.Quote_detail.item(row, 10).text()))
        elif float(self.Quote_detail.item(row, 13).text()) == float(0):
            price = Decimal(str(self.Quote_detail.item(row, 10).text()))
        else:
            # 单价=单重*公斤价+加工费+其他费用
            price = weight*weight_price+cost+expenses
        # 更新单价,小数点2位
        self.Quote_detail.setItem(row, 10, QTableWidgetItem(str('%.2f' % price)))
        # 更新总价amount=数量*单价
        amount = Decimal(quantity*price)
        self.Quote_detail.setItem(row, 11, QTableWidgetItem(str('%.2f' % amount))) 
        self.Quote_detail.blockSignals(False)  # 恢复单元格修改信号

    # 计算列值总数函数
    def sum_amount_1(self, l):
        """计算所选列的总数,l为列数"""
        count = 0
        # 获取表格中的总行数,考虑到保存时有空行的情况用总行数.
        rows = self.Quote_detail.rowCount()
        for i in range(rows):
            # 判断不存在和空值,并设为0值
            if not self.Quote_detail.item(i, l):
                count += 0
            elif self.Quote_detail.item(i, l).text() == "":
                count += 0
            else:
                count += Decimal(self.Quote_detail.item(i, l).text())
        return count

    def add_combobox(self):
        """设置下拉列表框控件参数"""
        if self.Box_filter.count() > 0:
            return
        self.Box_filter.addItem('请选择审核结果')
        # 设置字体颜色+图标
        self.Box_filter.setStyleSheet("QComboBox{color:red;}")
        self.Box_filter.addItem(QIcon(":/png/images/Accept.png"), '审核通过')
        self.Box_filter.addItem(QIcon(":/png/images/stop_32px.ico"), '退回重报')

    # @pyqtSlot()  # 报价审核通过
    def Box_filter_currentIndexChanged(self):
        """列表框选择变更事件-->更新数据库审核状态"""
        if self.Box_filter.currentText() == '请选择审核结果':
            return
        if self.Box_filter.currentText() == '':
            return
        h = self.Quote_list.currentIndex().row()          # 找到所选行的行数h
        bjdh = self.Quote_list.item(h, 1).text()          # 找到所选h行的1位报价单号
        zt = self.Box_filter.currentText()
        button = QMessageBox.question(self, "提醒", "将要保存审核状态为:"+zt+"？",
                                      QMessageBox.Ok|QMessageBox.Cancel,QMessageBox.Ok)
        if button == QMessageBox.Ok:
            myMdb().update(table='报价基本信息', 状态="'"+zt+"'", where="报价单号="+bjdh)
            QMessageBox.information(QWidget(), "报价审核", "审核结果:"+zt)
            self.Box_filter.blockSignals(True)
            # 防止再次选择下拉框引起再次写状态,要清空
            self.Box_filter.clear()
            self.Box_filter.blockSignals(False)
            self.query_list()
        else:
            return