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

from ui.Ui_quote_check import Ui_Quote_check
from ui.Ui_quote import Ui_wgt_quote
from ui.Ui_check import Ui_Quote_check
from ui.Ui_order import Ui_WidgetOrder

from tools.mysql_conn import myMdb
from tools.tools import *
from tools.datadialog import DateDialog  # 查询子窗口
# from lib.RMB import * #人民币大写转换


class AdjustPrice(QWidget, Ui_wgt_quote):
    """调价类"""
    def __init__(self, parent=None):
        super(AdjustPrice, self).__init__(parent)
        self.setupUi(self)

        self.label.setText("调价管理")
        # 隐藏不需要的选择控件
        self.cbo_state.hide()
        self.btn_check.hide()
        self.PBnew.hide()
        self.quotedate.setText(time.strftime("%Y-%m-%d", time.localtime()))

        # 自定义标题
        self.tblwgt_quote.setColumnCount(12)
        filed = ['序号','名称','制造标准','规格型号','材质','数量','工作令号','件号','单价','金额',' 折扣%','折扣价']
        self.tblwgt_quote.setHorizontalHeaderLabels(filed)  # 设置标题
        font = QtGui.QFont('微软雅黑', 9)
        self.tblwgt_quote.horizontalHeader().setFont(font)  # 设置行表头字体
        self.tblwgt_quote.horizontalHeader().setStyleSheet('QHeaderView::section{background:skyblue}')
        self.tblwgt_quote.verticalHeader().setVisible(False)                    # 左垂直表头不显示
        # self.tblwgt_quote.setEditTriggers(QAbstractItemView.AnyKeyPressed)    # 设置表格任何时候都能修改
        self.tblwgt_quote.horizontalHeader().setStretchLastSection(True)        #最后一列对齐边框
        # self.tblwgt_quote.horizontalHeader().setResizeMode(QHeaderView.Stretch)
        # self.tblwgt_quote.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch) #占满屏幕,平均分配列宽
        self.tblwgt_quote.setFrameStyle(QtWidgets.QFrame.Box | QtWidgets.QFrame.Plain)
        # self.tblwgt_quote.resizeColumnsToContents()                             # 自适应列宽度
        #设置文本框无边框
        styleSheet = "background:transparent;border-width:0;border-style:outset"
        # self.quotationNo.setStyleSheet(styleSheet)
        self.contact.setStyleSheet(styleSheet)
        self.lineEdit_5.setStyleSheet(styleSheet)
        self.lineEdit_6.setStyleSheet(styleSheet)
        self.lineEdit_8.setStyleSheet(styleSheet)
        self.lineEdit_9.setStyleSheet(styleSheet)
        self.quotedate.setStyleSheet(styleSheet)
        self.total_price.setStyleSheet(styleSheet)
        self.total_quantity.setStyleSheet(styleSheet)
        # 信号连接槽
        self.btn_query.clicked.connect(self.opendiolog)
        self.tblwgt_quote.cellChanged.connect(self.adjust_calculate)

    def opendiolog(self):
        dialog = DateDialog(self)
        # '''连接子窗口的自定义信号与主窗口的槽函数'''
        dialog.Signal_No.connect(self.query_adjust_detail)
        dialog.show()

    def adjust_calculate(self, row):
        """ 调整折扣率后重新计算单价/总价   函数中不能有信号,有就进四死循环"""
        self.tblwgt_quote.cellChanged.disconnect(self.adjust_calculate)  # 删除信号
        # 数量quantity
        quantity = int(self.tblwgt_quote.item(row, 5).text())
        # 折扣
        zk = float(self.tblwgt_quote.item(row, 10).text())
        # 计算单价 原价*折扣率%
        prc = float(self.tblwgt_quote.item(row, 8).text())
        price = Decimal(prc*zk*0.01)
        # 更新单价,小数点2位
        self.tblwgt_quote.setItem(row, 8, QTableWidgetItem(str('%.2f' % price)))
        # 更新总价amount=数量*单价
        amount = Decimal(quantity*price)
        self.tblwgt_quote.setItem(row, 9, QTableWidgetItem(str('%.2f' % amount)))
        count_1 = plusColumn(self, "tblwgt_quote", 5).quantize(Decimal('0'))
        self.total_quantity.setText(str(count_1))
        count_2 = plusColumn(self, "tblwgt_quote", 9).quantize(Decimal('0.00'))
        self.total_price.setText(str(count_2))
        # self.tblwgt_quote.blockSignals(False)  # 恢复单元格修改信号
        self.tblwgt_quote.cellChanged.connect(self.adjust_calculate)

    def query_adjust_detail(self, bjdh, qte_date):
        """查询报价"""
        # 清除数据删除cellchang信号
        self.clearAdjustData()
        mdb = myMdb()
        res = mdb.fetchall(table='quote', where="报价单号="+"'"+bjdh+"'")
        if not res:
            QMessageBox.warning(self, '查询出错', '没有查到报价记录')
            return
        data = [tup[0] for tup in res[0]]
        row = len(data)     # 获得data的行数
        vol = len(res[0][0])  # 获得data的列数.cur.description或len(data[0])
        # self.tblwgt_quote.setColumnCount(vol-8)
        self.tblwgt_quote.setRowCount(row)
        #构建表格插入数据
        self.CBcorporate.addItem(str(res[0][0][0]))
        self.quotationNo.setText(str(res[0][0][1]))
        self.quotedate.setText(qte_date)  # 报价制单日期
        for i in range(row):  # i到row-1的数量
            for j in range(2, vol-7):  # 第3列开始
                temp_data = res[0][i][j]
                data3 = QTableWidgetItem(str(temp_data))
                if j in (0, 1, 2, 3, 4, 5, 6, 8, 9, 11):
                    data3.setFlags(QtCore.Qt.NoItemFlags)  # 禁止指定列编辑
                self.tblwgt_quote.setItem(i, j-2, data3)
            # 折扣率默认设100%
            self.tblwgt_quote.setItem(i, 10, QTableWidgetItem(str(100)))
            self.tblwgt_quote.setItem(i, 11, QTableWidgetItem(str(res[0][i][11])))
        # 适应列宽/行高/最后一列对齐边框
        self.tblwgt_quote.resizeColumnsToContents()
        self.tblwgt_quote.resizeRowsToContents()
        self.tblwgt_quote.horizontalHeader().setStretchLastSection(True)
        # 计算总数量总价
        count_1 = plusColumn(self, "tblwgt_quote", 5).quantize(Decimal('0'))
        self.total_quantity.setText(str(count_1))
        count_2 = plusColumn(self, "tblwgt_quote", 9).quantize(Decimal('0.00'))
        self.total_price.setText(str(count_2))
        # 连接被关闭的单元格变更信号
        self.tblwgt_quote.cellChanged.connect(self.adjust_calculate)

    # 变更查询和保存后清空数据
    def clearAdjustData(self):
        # 存在信号连接就删除
        try:
            self.tblwgt_quote.cellChanged.disconnect()
        except:
            pass
        finally:
            self.tblwgt_quote.clearContents()
            self.CBcorporate.clear()
            self.quotationNo.setText('')
            self.total_quantity.setText('')
            self.total_price.setText('')
            # for i in (2, 3, 4, 6, 7, 8):
            #     # 控件名是变量的两种方法
            #     # self.findChild(QLineEdit, "lineEdit_"+str(i)).setText("")
            #     exec("self.lineEdit_"+str(i)+".setText('')")


class Order(QWidget, Ui_WidgetOrder):
    """订单类"""
    def __init__(self, parent=None):
        super(Order, self).__init__(parent)
        self.setupUi(self)
        self.initOrder()
        self.dateEdit()

        # 公司名称下拉列表框
        mdb = myMdb()
        result = mdb.fetchall(field='{}'.format('distinct 公司名称'), table='{}'.format('报价基本信息'))
        # 循环取元祖数据,转为列表
        col_lst = [tup[0] for tup in result[0]]
        # self.cmbCO.insertItem(0, "公司名称")
        # self.cmbCO.addItems(col_lst)
        # 销售代表下拉列表框
        self.comboBox.addItem('请选择销售代表')
        self.comboBox.setStyleSheet("QComboBox{color:red;}")
        self.comboBox.addItem(QIcon(":/png/images/Accept.png"), '公司')
        self.comboBox.addItem(QIcon(":/png/images/Accept.png"), '吴丹')
        self.comboBox.addItem(QIcon(":/png/images/Accept.png"), '费舟亮')

        self.TW_order.setContextMenuPolicy(Qt.ActionsContextMenu)
        self.TW_order.addAction(QAction("插入一行", self, triggered=self.add_onerow))
        self.TW_order.addAction(QAction("插入多行", self, triggered=self.add_rows))
        self.TW_order.addAction(QAction("删除行", self, triggered=self.delselect))
        self.TW_order.addAction(QAction("复制", self, triggered=self.add_rows))
        self.TW_order.addAction(QAction("粘贴", self, triggered=self.delselect))

        # 修改单元格信号
        self.TW_order.cellChanged.connect(self.TW_order_cellChanged)

    def dateEdit(self):
        """tablewidget单元格加入交货期dateedit控件"""
        self.dateedit = QDateEdit(QDate.currentDate(), self)
        self.dateedit.setCalendarPopup(True)
        # row = self.TW_order.currentItem().row()
        self.TW_order.setCellWidget(0, 12, self.dateedit)
        # 日期控件信号连接槽函数
        self.dateedit.dateChanged.connect(self.date_changed)

    def date_changed(self, date):
        """日期控件发生改变时执行"""
        # 把选择日期转换为文本
        row = self.TW_order.rowCount()
        for i in range(row):
            if self.TW_order.item(i, 0) is None:
                break
            if self.TW_order.item(i, 0).text() != "":
                txt = QTableWidgetItem(date.toString("yyyy-MM-dd"))
                self.TW_order.setItem(i, 12, txt)

    def initOrder(self):
        """打开订单-->初始化订单表格"""
        # 设置订单lineedit文本框显示当前日期
        self.lineEdit_5.setText(time.strftime("%Y-%m-%d", time.localtime()))
        #设置表格设置初始100行
        self.TW_order.setRowCount(100)
        self.TW_order.setColumnCount(13)
        # 设置标题
        tbl_header = ['序号','名称','制造标准','规格型号','材质','数量', \
                        '工作令号','件号','单价','金额','备注','净重','交货日期']
        vol = len(tbl_header)
        self.TW_order.setHorizontalHeaderLabels(tbl_header)
        # 设置每格为空值
        for m_row in range(100):
            for m_col in range(vol):
                items = QTableWidgetItem("")
                self.TW_order.setItem(m_row, m_col, items)
        # 设置行表头字体
        font = QtGui.QFont('微软雅黑', 9)
        self.TW_order.horizontalHeader().setFont(font)
        # 左垂直表头不显示
        self.TW_order.verticalHeader().setVisible(False)
        # 只能选择单行
        # self.TW_order.setSelectionMode(QAbstractItemView.SingleSelection)
        # 设置表格颜色             
        self.TW_order.horizontalHeader().setStyleSheet('QHeaderView::section{background:skyblue}')
        self.TW_order.setFrameStyle(QtWidgets.QFrame.Box | QtWidgets.QFrame.Plain)
        # 设置文本框无边框
        styleSheet = "background:transparent;border-width:0;border-style:outset"
        for i in range(1, 7):
            exec("self.lineEdit_{}.setStyleSheet(styleSheet)".format(i))

    def writeParam(self, param):
        """写入查询数据"""
        self.TW_order.blockSignals(True)  # 暂停单元格修改信号
        row = len(param)  # 获得查询窗口选择数据的行数
        col = self.TW_order.columnCount()
        m_name = param[0][0]
        self.TW_order.setRowCount(row)
        self.lineEdit_2.setText(m_name)
        for i in range(row):
            # 取第4列到第12列
            for j in range(1, col):
                temp_data = param[i][j]
                # if temp_data == 'None':
                #     temp_data = 0
                data_1 = QTableWidgetItem(str(temp_data))
                self.TW_order.setItem(i, j-1, data_1)
            # 把送货单明细第11列None状态设为空值
            self.TW_order.setItem(i, col, QTableWidgetItem(''))
        self.TW_order.resizeColumnsToContents()
        # 汇总数量金额
        count_1 = plusColumn(self, "TW_order", 5)
        self.lineEdit_6.setText(str(count_1))
        count_2 = plusColumn(self, "TW_order", 9)
        self.lineEdit_7.setText(str(count_2))
        self.TW_order.blockSignals(False)  # 启动单元格修改信号

    def sumColumn(self):
        """汇总数量金额 已整合,待取消"""
        # count_1 = plusColumn(self, "TW_order", 5)
        # self.lineEdit_6.setText(str(count_1))
        # count_2 = plusColumn(self, "TW_order", 9)
        # self.lineEdit_7.setText(str(count_2))

    # def contextMenuEvent(self, event):
    #     """系统自带右键菜单事件:"""
    #     self.TW_order.setContextMenuPolicy(Qt.ActionsContextMenu)
    #     self.TW_order.addAction(QAction("插入行", self, triggered=self.add_onerow))
    #     self.TW_order.addAction(QAction("删除行", self, triggered=self.delselect))

    def add_onerow(self):
        """当前位置插入一行"""
        self.TW_order.blockSignals(True)  # 暂停单元格修改信号
        row = self.TW_order.currentIndex().row()
        cols = self.TW_order.columnCount()
        # print(cols)
        # 在row行位置插入一空行
        self.TW_order.insertRow(row)
        # 给插入的行设置空值
        for m_col in range(cols):
            new_item = QTableWidgetItem("")
            new_item.setTextAlignment(Qt.AlignHCenter|Qt.AlignVCenter)
            self.TW_order.setItem(row, m_col, new_item)
        self.TW_order.blockSignals(False)  # 暂停单元格修改信号

    def add_rows(self):  # 暂未加入
        """尾行插入多行数据"""
        rows = self.TW_order.rowCount()# 获取表格中的总行数
        for i in self.TW_order.selectionModel().selection().indexes():
            rownum = i.row()
        #在末尾插入空行
        self.TW_order.setRowCount(rows + rownum)

    def delselect(self):
        """删除所选行及数据,可以多行,可以自选"""
        ret = QMessageBox.warning(self.TW_order, u'警告', u'是否删除所选行?',
                                  QMessageBox.Yes|QMessageBox.No)
        if ret == QMessageBox.Yes:
            select_rows = set()
            for rg in self.TW_order.selectedRanges():
                for i in range(rg.topRow(), rg.bottomRow()+1):
                    select_rows.add(i)
            select_rows = list(select_rows)
            # print('r' +str(select_rows))
            select_rows.sort(reverse=True)  # 分类反转
            for index in select_rows:
                self.TW_order.removeRow(index)
        else:
            return
        self.sumColumn()

    def TW_order_cellChanged(self, row, col):
        """订单明细修改变更事件-->红色显示修改,重新计算数量价格"""
        self.TW_order.blockSignals(True)  # 暂停单元格修改信号
        items = self.TW_order.item(row, col)  # currentIndex()可以考虑
        txt = items.text()
        # 字体颜色（红色）
        # item.setForeground(QBrush(QColor(255, 0, 0)))
        # 背景颜色（红色）
        self.TW_order.item(row, col).setBackground(QBrush(QColor(255, 0, 0)))
        # 重新计算
        if col in (5, 8):
            if self.TW_order.item(row, 5).text() == '':
                number = 0
            else:
                number = int(self.TW_order.item(row, 5).text())

            if self.TW_order.item(row, 8).text() == '':
                price = 0
            else:
                price = Decimal(str(self.TW_order.item(row, 8).text()))

            amount = Decimal(number*price)
            self.TW_order.setItem(row, 9, QTableWidgetItem(str(amount)))
            # 汇总列总数量/总金额,更新到lineEdit
            count_1 = plusColumn(self, "TW_order", 5)
            self.lineEdit_6.setText(str(count_1))
            # 添加计算结果到总金额栏,2位小数
            money = plusColumn(self, "TW_order", 9)
            self.lineEdit_7.setText(str(money))
        self.TW_order.blockSignals(False)  # 启动单元格修改信号

    # 保存订单
    def save(self):
        """保存合同和订单明细"""
        if self.lineEdit_3.text() == "":
            QMessageBox.about(self, "注意", "生产编号未输入,请检查添加!")
            return

        if self.lineEdit_4.text() == "":
            QMessageBox.about(self, "注意", "合同编号未输入,请检查添加!")
            return
        
        if self.TW_order.item(0, 0).text() == "":
            QMessageBox.about(self, "注意", "订单数据未输入,请检查添加!")
            return
        
        if self.comboBox.currentText() == "请选择销售代表":
            QMessageBox.about(self, "注意", "销售代表未输入,请检查添加!")
            return

        # 交货日期不能为空
        if self.TW_order.item(0, 12) is None or self.TW_order.item(0, 11).text() == "":
            QMessageBox.about(self, "注意", "交货日期未选,请返回输入!")
            return

        button = QMessageBox.question(self, "注意", "请确认无误再保存订单,\n按OK继续,按Cancel退出",
                                      QMessageBox.Ok|QMessageBox.Cancel, QMessageBox.Ok)
        if button == QMessageBox.Cancel:
            return

        # 找出对应客户代码
        mdb = myMdb()
        company = self.lineEdit_2.text()
        # print(param)
        m_code = mdb.fetchone(field='{}'.format('客户代码'),
                              table='{}'.format('客户资料表'),
                              where="{}='{}'".format('公司名称', company))
                              # where="公司名称 like '{}'".format(m_name))

        rows = self.TW_order.rowCount()  # 总行数
        cols = self.TW_order.columnCount()  # 总列数
        filed = '生产编号,合同编号,公司名称,客户代码,序号,名称,制造标准,规格型号,材质,数量,工作令号,件号,单价,金额,备注,净重,交货日期,生产状态'
        preSql = "insert into {} ({})".format('order_list', filed)
        subSql = "values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        sql = preSql+subSql  # 前后相加成一个完整的sql
        param = []  # 建传入值的列表
        for row in range(rows):  # 还要验证none的情况是否出错???????????????????????????????????????
            # if self.TW_order.item(row, 0) is None:
            #     break
            if self.TW_order.item(row, 0).text() != "" or self.TW_order.item(row, 0) is None:
                value_list = []
                value_list.append(self.lineEdit_3.text())  # 生产编号加入数组
                value_list.append(self.lineEdit_4.text())  # 合同编号
                value_list.append(self.lineEdit_2.text())  # 买方
                value_list.append(m_code[0])  # 客户代码
                for col in range(cols):
                    # 把None和空值的数字格设为0值
                    if not self.TW_order.item(row, col) or self.TW_order.item(row, col).text() == "":
                        value_list.append("")
                    else:
                        value_list.append(self.TW_order.item(row, col).text())
                value_list.append('签订合同')
                param.append(value_list)
            else:
                break
        # 保存订单==============================================================
        rowcount = mdb.insert_many(sql, param)
        m_r = self.textEdit.toPlainText().replace("\n", ";")
        mdb.insert(table='orders',
                   公司名称=self.lineEdit_2.text(),
                   生产编号=self.lineEdit_3.text(),
                   合同编号=self.lineEdit_4.text(),
                   签订日期=self.lineEdit_5.text(),
                   总数量=self.lineEdit_6.text(),
                   总金额=self.lineEdit_7.text(),
                   销售代表=self.comboBox.currentText(),
                   交货地点=self.lineEdit_8.text(),
                   技术要求=m_r,
                   订单状态='签订合同')
        QMessageBox.about(self, "保存成功", "保存了"+str(rowcount)+"条订单记录")

        # bjdh = self.cmbNO.currentText()
        # mdb.update(table='报价基本信息', 状态="'签订合同'", where="报价单号="+bjdh)
        self.clearData()

    def clearData(self):
        # 存在信号连接就删除
        try:
            self.TW_order.cellChanged.disconnect()
        except:
            pass
        finally:
            self.textEdit.clear()
            self.TW_order.clearContents()
            self.comboBox.setCurrentText("请选择销售代表")
            for i in (2, 3, 4, 6, 7, 8):
                exec("self.lineEdit_{}.setText('{}')".format(i, ''))

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


class Quote(QWidget, Ui_wgt_quote):
    """报价类"""
    def __init__(self, parent=None):
        super(Quote, self).__init__(parent)
        self.setupUi(self)

        # 隐藏不需要的选择控件
        self.cbo_state.hide()
        self.btn_check.setText('计算')
        #设置报价lneedit文本框显示当前日期
        self.quotedate.setText(time.strftime("%Y-%m-%d", time.localtime()))

        # col_lst = [tup[0] for tup in res[1].description]
        # data = [tup[0] for tup in res[0]]
        # row = len(data)     # 获得data的行数
        # vol = len(res[0][0])  # 获得data的列数.cur.description或len(data[0])

        #公司名称下拉列表框
        self.mymdb = myMdb()
        result = self.mymdb.fetchall(field='公司名称', table='客户资料表')
        # 循环取元祖数据,转为列表
        cl_lst = [tup[0] for tup in result[0]]
        self.CBcorporate.insertItem(0, "请选择公司名称")
        self.CBcorporate.addItems(cl_lst)

        #设置表格设置初始100行
        self.tblwgt_quote.setRowCount(100)
        self.tblwgt_quote.setColumnCount(24)
        # 设置标题
        table_header = ['序号','名称','制造标准','规格型号','材质','数量','工作令号', \
                        '件号','单价','金额','备注','净重','净重价','毛重','毛重价','加工费', \
                        '其他费用','外径','内径','高度','外径余量','内径余量','高度余量','火耗']
        self.tblwgt_quote.setHorizontalHeaderLabels(table_header)
        # 设置每格为空值
        for i in range(100):
            for j in range(22):
                new_item = QTableWidgetItem("")
                # new_item.setTextAlignment(Qt.AlignHCenter|Qt.AlignVCenter)
                self.tblwgt_quote.setItem(i, j, new_item)
        #表格格式设置
        self.tblwgt_quote.horizontalHeader().setStyleSheet('QHeaderView::section{background:skyblue}')
        self.tblwgt_quote.setContextMenuPolicy(Qt.CustomContextMenu)            # 允许右键产生菜单
        self.tblwgt_quote.customContextMenuRequested.connect(self.right_menu)    # 将右键绑定到槽
        # self.tblwgt_quote.setSelectionBehavior(QAbstractItemView.SelectRows)  # 设置整行选中
        self.tblwgt_quote.verticalHeader().setVisible(False)                    # 左垂直表头不显示
        # self.tblwgt_quote.setEditTriggers(QAbstractItemView.AnyKeyPressed)    # 设置表格任何时候都能修改
        self.tblwgt_quote.horizontalHeader().setStretchLastSection(True)        #最后一列对齐边框
        # self.tblwgt_quote.horizontalHeader().setResizeMode(QHeaderView.Stretch)
        # self.tblwgt_quote.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch) #占满屏幕,平均分配列宽
        self.tblwgt_quote.resizeColumnsToContents()                             # 自适应列宽度
        # self.tblwgt_quote.resizeRowsToContents()                              # 自适应行高
        # self.autoadd()                                                   # 自动编序号
        # self.tblwgt_quote.hideColumn(0)                                       # 隐藏第一列
        # self.tblwgt_quote.showColumn(0)                                       # 显示第一列
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
        # self.tblwgt_quote.cellChanged.connect(self.cell_changed)

    #点击计算按钮事件
    @pyqtSlot()
    def on_btn_check_clicked(self):
        self.calculate()

    # dock窗口导入查询数据
    def writeParam(self):
        # 点击查询后计算单价总价
        self.calculate()

    # 单价/总价计算
    def calculate(self):
        rows = self.tblwgt_quote.rowCount()  # 保存时有空行的情况用总行数.
        # 判断有数据的行数h,空值就退出循环
        for h in range(rows):
            if not self.tblwgt_quote.item(h, 0):
                break  #跳出循环
            elif self.tblwgt_quote.item(h, 0).text() == "":
                break
        for i in range(h+1):
            quantity = int(self.tblwgt_quote.item(i, 5).text())  # 数量quantity
            if self.tblwgt_quote.item(i, 10).text() == "":
                weight = 0
            else:
                weight = Decimal(str(self.tblwgt_quote.item(i, 10).text()))  # 单重unit weight
            if self.tblwgt_quote.item(i, 11).text() == "":
                weight_price = 0
            else:
                weight_price = Decimal(str(self.tblwgt_quote.item(i, 11).text()))  # 公斤价weight price
            if self.tblwgt_quote.item(i, 12).text() == "":
                cost = 0
            else:
                cost = Decimal(str(self.tblwgt_quote.item(i, 12).text()))  # 加工费cost
            if self.tblwgt_quote.item(i, 13).text() == "":
                expenses = 0
            else:
                expenses = Decimal(str(self.tblwgt_quote.item(i, 13).text()))  # 其他费用expenses
            # 计算单价    单价=单重*公斤价+加工费+其他费用
            if self.tblwgt_quote.item(i, 11).text() == "":
                price = Decimal(str(self.tblwgt_quote.item(i, 8).text()))
            else:
                price = round(weight*weight_price+cost+expenses)
            self.tblwgt_quote.setItem(i, 8, QTableWidgetItem(str(price)))
            amount = quantity*price  # 总价amount=数量*单价
            self.tblwgt_quote.setItem(i, 9, QTableWidgetItem(str(amount)))
            count_1 = plusColumn(self, 'tblwgt_quote', 5)
            self.total_quantity.setText(str(count_1))
            count_2 = plusColumn(self, 'tblwgt_quote', 9)
            self.total_price.setText(str(count_2))  # 添加计算结果到总价栏,2位小数

    # 计算列值总数函数
    def sum_amount(self, l):
        """计算所选列的总数,l为列数"""
        count = 0
        # 获取表格中的总行数,考虑到保存时有空行的情况用总行数.
        rows = self.tblwgt_quote.rowCount()
        for i in range(rows):
            # 判断不存在和空值,并设为0值
            if not self.tblwgt_quote.item(i, l):
                count += 0
            elif self.tblwgt_quote.item(i, l).text() == "":
                count += 0
            else:
                count += Decimal(self.tblwgt_quote.item(i, l).text())
            print(i)
        return count

    def cell_changed(self, row, col):  # 参考后删除
        """单元格变更后事件"""
        item = self.tblwgt_quote.item(row, col)
        txt = item.text()
        item.setForeground(QBrush(QColor(255, 0, 0)))
        # self.settext('第%s行，第%s列 , 数据改变为:%s'%(row,col,txt))
        print('第{}行，第{}列 , 数据改变为:{}'.format(row, col, txt))

    # 当单元格的焦点变化时，重新计算数量和总价
    # @pyqtSlot(int, int, int, int)
    # def on_tblwgt_quote_currentCellChanged(self, currentRow, currentColumn, previousRow, previousColumn):
        # if previousColumn == 5:                                                #改动后的列索引=数量列
        #     count_1 = self.sum_amount(5)                                       #计算第5列数量
        #     self.total_quantity.setText(str(count_1.quantize(Decimal('0'))))   # 添加计算结果到总数量栏,0位小数
        #     # self.money.setText(str(cncurrency(int(count_2))))                # 添加人民币大写

    # 自动增加序号
    def autoadd(self):
        """序号自动编号"""
        rows = self.tblwgt_quote.rowCount()  # 获取表格中的总行数
        for i in range(rows):
            xh = '%d'% (i+1)
            self.tblwgt_quote.setItem(i, 0, QTableWidgetItem(xh))

    # 右键菜单
    def right_menu(self, pos):
        """右键菜单def contextMenuEvent(self, event):"""
        pmenu = QMenu(self)
        pInsertAct = QAction(u"插入行", self.tblwgt_quote)
        pInsertsAct = QAction(u"插入多行", self.tblwgt_quote)
        pDeleteAct = QAction(u"删除行", self.tblwgt_quote)
        pHideAct = QAction(u"隐藏列", self.tblwgt_quote)
        pMergeAct = QAction(u"合并单元格", self.tblwgt_quote)
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
        r = self.tblwgt_quote.currentIndex().row()
        # print('r=' +str(r))
        self.tblwgt_quote.insertRow(r) #在r位置插入一空行
        for j in range(15):# 给插入的行设置空值
            newItem = QTableWidgetItem(0)
            newItem.setTextAlignment(Qt.AlignHCenter|Qt.AlignVCenter)
            self.tblwgt_quote.setItem(r, j, newItem)

    # 插入多行=======??????
    def add_rows(self):
        """清除数据"""
        rows = self.tblwgt_quote.rowCount()# 获取表格中的总行数
        for i in self.tblwgt_quote.selectionModel().selection().indexes():
            rownum = i.row()
        #在末尾插入空行
        self.tblwgt_quote.setRowCount(rows + rownum)

    # 清除所选的数据,现在是连行都删除,考虑只清除数据的情况是否合适???????????
    def del_select(self):
        """清除数据"""
        ret = QMessageBox.warning(self.tblwgt_quote, u'警告', u'是否删除所选行?',
                                    QMessageBox.Yes|QMessageBox.No)
        if ret == QMessageBox.Yes:
            for rg in self.tblwgt_quote.selectedRanges():
                new_item = QTableWidgetItem("")
                # 选择行的最顶行到最底行
                for i in range(rg.topRow(), rg.bottomRow()+1):
                    self.tblwgt_quote.setItem(i, 3, new_item)

    # 删除所选行
    def ondelselect(self):
        """删除所选行及数据"""
        ret = QMessageBox.warning(self.tblwgt_quote, u'警告', u'是否删除所选行?',
                                    QMessageBox.Yes|QMessageBox.No)
        if ret == QMessageBox.Yes:
            select_rows = set()
            for rg in self.tblwgt_quote.selectedRanges():
                for i in range(rg.topRow(), rg.bottomRow()+1):
                    select_rows.add(i)
            select_rows = list(select_rows)
            # print('r' +str(select_rows))
            select_rows.sort(reverse=True)  # 分类反转
            for index in select_rows:
                self.tblwgt_quote.removeRow(index)
        else:
            return

    # 隐藏列 还要增加还原隐藏的功能==================================????
    def onhide(self):
        """隐藏列"""
        c = self.tblwgt_quote.currentIndex().column()
        print('隐藏' +str(c) +'列')
        self.tblwgt_quote.hideColumn(c) #隐藏c列

    # 合并单元格
    def onmergecolumn(self):
        """合并单元格"""
        print('合并' +'单元格')

    # 生成报价单号
    def add_quote_No(self):
        """自动生成报价单号"""
        # 格式化当前日期+后两位
        # date = time.strftime("%y%m%d", time.localtime()) + "00"
        date = time.strftime("%y%m%d", time.localtime()) + "00"
        bj = myMdb().fetchone(field='max(报价单号)', table='quote', where="报价单号>"+date)
        if bj[0] is None:
            bjdh = int(date) + 1
        else:
            bjdh = int(bj[0]) + 1
        self.quotationNo.setText(str(bjdh))

    # 保存报价
    @pyqtSlot()
    def on_PBsave_clicked(self):  # save_quote
        """保存报价明细和汇总"""
        if self.CBcorporate.currentText() == "请选择公司名称":
            QMessageBox.warning(self, '警告', '公司名称未选择')
            return
        # 保存报价明细
        rows = self.tblwgt_quote.rowCount()  # 总行数
        cols = self.tblwgt_quote.columnCount()  # 总列数
        for h in range(rows+1):
            if not self.tblwgt_quote.item(h, 0):  # 从0行开始找出空值所在行
                break # 跳出循环
            elif self.tblwgt_quote.item(h, 0).text() == "":  #从0行开始找出空值所在行
                break
        preSql = "insert into quote ("  # 前一段拼接字段
        subSql = "values("              # 后一段拼接字段
        # exc = ()   # 作为execute的参数值，这是一个tuble类型
        preSql += "公司名称" + ","
        subSql += "%s,"
        preSql += "报价单号" + ","
        subSql += "%s,"
        for i in range(cols):  # 取出每一个子json的key和value值
            x = self.tblwgt_quote.horizontalHeaderItem(i).text()  # 列表头值
            preSql += x + ","  # 拼接前面sql的key值
            subSql += "%s,"   # 拼接后面sql的value数量
        preSql = preSql[0:preSql.__len__()-1] + ")"  # 去掉后面的“，”再添加“）”
        subSql = subSql[0:subSql.__len__()-1] + ")"  # 去掉后面的“，”再添加“）”
        sql = preSql+subSql  # 前后相加成一个完整的sql
        # print(sql)
        param = []  # 建传入值的列表
        for k in range(h):
            value_list = []
            value_list.append(self.CBcorporate.currentText())  # 公司名称加入数组
            value_list.append(self.quotationNo.text())
            for i in range(cols):
                if i in (10, 11, 12, 13) and self.tblwgt_quote.item(k, i).text() == "":
                    value_list.append("0")  # 把空值的数字格设为0值
                else:
                    value_list.append(self.tblwgt_quote.item(k, i).text())
            param.append(value_list)
            print(value_list)
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
        self.tblwgt_quote.clear
        #需要增加先清除原来数据代码
        openfile_name = QFileDialog.getOpenFileName(
            self, '选择文件', 'C:/Users/Administrator/Desktop/', 'Excel files(*.xlsx , *.xls)')
        global path_openfile_name                      # 把打开的文件名当全局变量,传导给读取表格用
        path_openfile_name = openfile_name[0]
        ###===========读取表格，转换表格，===========================================
        if len(path_openfile_name) > 0:
            df = pd.read_excel(path_openfile_name)
            # 转化为list,待研究?????????????????????????????????????????????????
            # train_data = np.array(df)  # np.ndarray()
            # train_x_list=train_data.tolist()  # list

            # print(train_x_list)
            input_table = df
            # input_table = df.fillna(0)                  # pandas将NaN替换为0
            # input_table = df.where(df.notnull(), None)# 将NaN替换为None
            input_table_rows = input_table.shape[0]     # numpy函数中shape函数读取矩阵第一维度的长度
            input_table_colunms = input_table.shape[1]
            # input_table_header = input_table.columns.values.tolist() # 读取标题
            # filed = ['生产编号','合同编号','买方','序号','名称','制造标准','规格型号',
            #     '材质','数量','工作令号','件号','单价','金额','单重','交货期','备注','材料编码']
        ###======================给tablewidget设置行列表头============================
            # self.tblwgt_quote.setColumnCount(input_table_colunms)
            self.tblwgt_quote.setRowCount(input_table_rows)            #设置和导入数据相同行数
            # self.tblwgt_quote.setHorizontalHeaderLabels(filed) # 设置标题
            # self.tblwgt_quote.setHorizontalHeaderLabels(input_table_header) # 设置标题
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
                    self.tblwgt_quote.setItem(i, j, newItem)
        else:
            self.centralWidget.show()
        self.tblwgt_quote.resizeColumnsToContents()#根据内容自动调整所有列的列宽


class QuoteExamine(QWidget, Ui_Quote_check):
    """报价审核类-->目录和明细同一中间控件法"""
    def __init__(self, parent=None):
        super(QuoteExamine, self).__init__(parent)
        self.setupUi(self)
        self.quote_list()

        #连接槽
        self.Quote_list.itemClicked.connect(self.query_detail)  # 点击报价清单,显示选择的报价明细
        self.btn_query.clicked.connect(self.query_list)    # 点击查询查报价清单
        self.Quote_detail.itemClicked.connect(self.outSelect)  # 报价明细区点击事件,记录前值
        self.cbo_filter.currentIndexChanged.connect(self.cbo_filter_currentIndexChanged)  # 报价明细区单元格变更事件

    def quote_list(self):  # 默认显示报价清单
        """显示审核报价清单"""
        res = myMdb().fetchall(table='报价基本信息', where="状态='待审核'")
        data = [tup[0] for tup in res[0]]
        row = len(data)     # 获得data的行数
        vol = len(res[0][0])  # 获得data的列数.cur.description或len(data[0])
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
                temp_data = res[0][i][j]                            # 临时记录，不能直接插入表格
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
        # QTableWidget.removeCellWidget(int row,int column)
        #删除第row行第column列的窗口部件
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
        # 屏幕左下状态栏显示提示信息,调用父类
        # super(main,self).statusBar().showMessage('序号%s数据改变为:%s'%(txt, xh))
        print(self.findChild(QMainWindow, "statusbar"))
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
        self.quote_list()

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
        if self.cbo_filter.count() > 0:
            return
        self.cbo_filter.addItem('请选择审核结果')
        # 设置字体颜色+图标
        self.cbo_filter.setStyleSheet("QComboBox{color:red;}")
        self.cbo_filter.addItem(QIcon(":/png/images/Accept.png"), '审核通过')
        self.cbo_filter.addItem(QIcon(":/png/images/stop_32px.ico"), '退回修改')

    # @pyqtSlot()  # 报价审核通过
    def cbo_filter_currentIndexChanged(self):
        """列表框选择变更事件-->更新数据库审核状态"""
        if self.cbo_filter.currentText() == '请选择审核结果':
            return
        if self.cbo_filter.currentText() == '':
            return
        h = self.Quote_list.currentIndex().row()          # 找到所选行的行数h
        bjdh = self.Quote_list.item(h, 1).text()          # 找到所选h行的1位报价单号
        zt = self.cbo_filter.currentText()
        button = QMessageBox.question(self, "提醒", "将要保存审核状态为:"+zt+"？",
                                      QMessageBox.Ok|QMessageBox.Cancel,QMessageBox.Ok)
        if button == QMessageBox.Ok:
            myMdb().update(table='报价基本信息', 状态="'"+zt+"'", where="报价单号="+bjdh)
            QMessageBox.information(QWidget(), "报价审核", "审核结果:"+zt)
            self.cbo_filter.blockSignals(True)
            # 防止再次选择下拉框引起再次写状态,要清空
            self.cbo_filter.clear()
            self.cbo_filter.blockSignals(False)
            self.query_list()
        else:
            return


class Examine(QWidget, Ui_wgt_quote):
    """报价审核类-->Dock窗口法"""
    Signal_xgjl = pyqtSignal(str)  #定义修改记录信号
    def __init__(self, parent=None):
        super(Examine, self).__init__(parent)
        self.setupUi(self)

        self.label.setText("报价审核")
        # # 增加审核状态和审核按钮
        # self.cbo_state = QtWidgets.QComboBox()
        # self.cbo_state.setMinimumSize(QtCore.QSize(0, 26))
        # self.cbo_state.setCurrentText("")
        # self.cbo_state.setObjectName("cbo_state")
        # self.cbo_state.setToolTip("审核情况")
        # self.horizontalLayout.addWidget(self.cbo_state)
        # self.btn_check = QtWidgets.QPushButton()
        # icon = QtGui.QIcon()
        # icon.addPixmap(QtGui.QPixmap(":/myImage/images/check.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        # self.btn_check.setIcon(icon)
        # self.btn_check.setObjectName("btn_check")
        # self.btn_check.setToolTip("审核")
        # self.btn_check.setText("审核")
        # self.horizontalLayout.addWidget(self.btn_check)

        # 下拉列表框加数据
        self.cbo_state.addItem('请选择审核结果')
        # self.cbo_state.setStyleSheet("QComboBox{color:red;}")
        self.cbo_state.addItem(QIcon(":/png/images/Accept.png"), '审核通过')
        self.cbo_state.addItem(QIcon(":/png/images/stop_32px.ico"), '退回修改')

        # 报价明细区点击事件,记录前值
        self.tblwgt_quote.itemClicked.connect(self.outSelect)
        # dialog.Signal_No.connect(self.quote_detail)  # 点击清单,显示选择的明细
        self.btn_query.clicked.connect(self.opendiolog)

    def opendiolog(self):
        dialog = DateDialog(self)
        '''连接子窗口的自定义信号与主窗口的槽函数'''
        dialog.Signal_No.connect(self.quote_detail)
        # dialog.show()
        dialog.exec_()

    # 显示报价明细
    def quote_detail(self, bjdh, qte_date):
        """显示报价明细"""
        # 暂停事件信号
        self.tblwgt_quote.blockSignals(True)
        # self.layout = QHBoxLayout()
        # 设置下拉列表框
        # self.add_combobox()
        mymdb = myMdb()
        self.tblwgt_quote.clearContents()  # 清除报价明细表内数据
        res = mymdb.fetchall(table='{}'.format('quote'), where="报价单号='{}'".format(bjdh))
        col_lst = [tup[0] for tup in res[1].description]
        del col_lst[0:2]
        data = [tup[0] for tup in res[0]]
        row = len(data)     # 获得data的行数
        vol = len(res[0][0])  # 获得data的列数.cur.description或len(data[0])
        # self.tblwgt_quote = QTableWidget(row, vol)
        self.tblwgt_quote.setColumnCount(vol-2)
        self.tblwgt_quote.setRowCount(row)
        font = QtGui.QFont('微软雅黑', 9)
        self.tblwgt_quote.horizontalHeader().setFont(font)  # 设置行表头字体
        self.tblwgt_quote.setHorizontalHeaderLabels(col_lst)  # 设置标题
        self.tblwgt_quote.verticalHeader().setVisible(False)  # 左垂直表头不显示
        self.tblwgt_quote.setObjectName("tblwgt_quote")
        self.tblwgt_quote.setToolTip("报价明细")
        self.tblwgt_quote.horizontalHeader().setStyleSheet(
            'QHeaderView::section{background:skyblue}')
        self.tblwgt_quote.setFrameStyle(QtWidgets.QFrame.Box | QtWidgets.QFrame.Plain)
        #构建表格插入数据
        self.CBcorporate.addItem(str(res[0][0][0]))
        self.quotationNo.setText(str(res[0][0][1]))
        self.quotedate.setText(qte_date)  # 报价制单日期
        for i in range(row):  # i到row-1的数量
            for j in range(2, vol-2):  # 第3列开始
                temp_data = res[0][i][j]
                data3 = QTableWidgetItem(str(temp_data))
                if j in (0, 1, 2, 3, 4, 5, 6, 8, 9, 11, 16):
                    data3.setFlags(QtCore.Qt.NoItemFlags)  # 禁止指定列编辑
                self.tblwgt_quote.setItem(i, j-2, data3)
        # 适应列宽/行高/最后一列对齐边框
        self.tblwgt_quote.resizeColumnsToContents()
        self.tblwgt_quote.resizeRowsToContents()
        self.tblwgt_quote.horizontalHeader().setStretchLastSection(True)
        count_1 = plusColumn(self, "tblwgt_quote", 5)
        self.total_quantity.setText(str(count_1))
        count_2 = plusColumn(self, "tblwgt_quote", 9)
        self.total_price.setText(str(count_2))
        # 启用事件信号
        self.tblwgt_quote.blockSignals(False)

    # 点击单元格取单元格值
    def outSelect(self, Item=None):  # 需改进,不用全局,用return值的方法????????????????????????????????
        """获得点击单元格的值"""
        if Item == None:
            return
        # 把table_value设为全局变量,给添加修改记录用
        # global g_TXT
        g_TXT = Item.text()
        return g_TXT

    # 修改报价明细区域单元格后，设置颜色打印变更值
    @pyqtSlot(int, int)
    def on_tblwgt_quote_cellChanged(self, row, col):
        """报价明细修改后的变更事件-->写入变更记录"""
        # if item == None:
        #     return
        # if col == 11:
        #     return
        mymdb = myMdb()
        item = self.tblwgt_quote.item(row, col)
        txt = item.text()
        self.tblwgt_quote.blockSignals(True)  # 暂停单元格修改信号
        # 字体颜色（红色）
        # item.setForeground(QBrush(QColor(255, 0, 0)))
        # 背景颜色（红色）
        self.tblwgt_quote.item(row, col).setBackground(QBrush(QColor(255, 0, 0)))
        self.tblwgt_quote.blockSignals(False)  # 启动单元格修改信号
        # 报价单号/序号
        bjdh = self.quotationNo.text()
        xh = self.tblwgt_quote.item(row, 0).text()
        # 被修改单元格的列标题
        g_TXT = self.outSelect()
        lie = self.tblwgt_quote.horizontalHeaderItem(col).text()
        record = '{}:{}修改为{},'.format(lie, g_TXT, txt)
        # xgjl = 'concat(修改记录,'+"'"+record+"'"+')'
        xgjl = "concat(修改记录,'{}')".format(record)
        # 重新计算汇总
        self.tblwgt_quote_calculate(row)
        # 更新-数据库-->
        mymdb.update(table='{}'.format('quote'),
                     数量=self.tblwgt_quote.item(row, 5).text(),
                     单价=self.tblwgt_quote.item(row, 8).text(),
                     金额=self.tblwgt_quote.item(row, 9).text(),
                     单重=self.tblwgt_quote.item(row, 10).text(),
                     公斤价=self.tblwgt_quote.item(row, 11).text(),
                     加工费=self.tblwgt_quote.item(row, 12).text(),
                     其他费用=self.tblwgt_quote.item(row, 13).text(),
                     修改记录=xgjl,
                     where="报价单号='{}' and 序号='{}'".format(bjdh, xh))
                     #  where="报价单号="+bjdh+ " and 序号="+xh)
        # 汇总总数量/总价,更新到数据库表中
        count_1 = plusColumn(self, "tblwgt_quote", 5).quantize(Decimal('0'))
        self.total_quantity.setText(str(count_1))
        count_2 = plusColumn(self, "tblwgt_quote", 9).quantize(Decimal('0.00'))
        self.total_price.setText(str(count_2))
        # 更新数据库
        mymdb.update(table='{}'.format('报价基本信息'),
                     总数量=count_1,
                     总价=count_2,
                     where="报价单号='{}'".format(bjdh))
        self.Signal_xgjl.emit(record)  # 发射修改记录数据信号

    def tblwgt_quote_calculate(self, row):
        """修改后重新计算单价/总价"""
        self.tblwgt_quote.blockSignals(True)  # 暂停单元格修改信号
        # 数量quantity
        quantity = int(self.tblwgt_quote.item(row, 5).text())
        # 单重unit weight                  
        if self.tblwgt_quote.item(row, 10).text() == "":
            weight = 0
        else:
            weight = Decimal(str(self.tblwgt_quote.item(row, 10).text()))
        # 公斤价weight price
        if self.tblwgt_quote.item(row, 11).text() == "":
            weight_price = 0
        else:
            weight_price = Decimal(str(self.tblwgt_quote.item(row, 11).text()))
        # 加工费cost
        if self.tblwgt_quote.item(row, 12).text() == "":
            cost = 0
        else:
            cost = self.tblwgt_quote.item(row, 12).text()
        # 其他费用expenses
        if self.tblwgt_quote.item(row, 13).text() == "":
            expenses = 0
        else:
            expenses = self.tblwgt_quote.item(row, 13).text()
        # 计算单价    公斤价="0.00或0时直接用单价,需要转化字符类型再==
        if float(self.tblwgt_quote.item(row, 11).text()) == float(0.00):
            price = Decimal(str(self.tblwgt_quote.item(row, 8).text()))
        elif float(self.tblwgt_quote.item(row, 11).text()) == float(0):
            price = Decimal(str(self.tblwgt_quote.item(row, 8).text()))
        else:
            # 单价=单重*公斤价+加工费+其他费用
            price = weight*weight_price+cost+expenses
        # 更新单价,小数点2位
        self.tblwgt_quote.setItem(row, 8, QTableWidgetItem(str('%.2f' % price)))
        # 更新总价amount=数量*单价
        amount = Decimal(quantity*price)
        self.tblwgt_quote.setItem(row, 9, QTableWidgetItem(str('%.2f' % amount))) 
        self.tblwgt_quote.blockSignals(False)  # 恢复单元格修改信号

    # 报价审核
    @pyqtSlot()
    def on_btn_check_clicked(self):
        """列表框选择变更事件-->更新数据库审核状态"""
        if self.cbo_state.currentText() == '请选择审核结果':
            return
        if self.cbo_state.currentText() == '':
            return
        bjdh = self.quotationNo.text()  # 报价单号
        state = self.cbo_state.currentText()  # 审核状态
        button = QMessageBox.question(self, "提醒", "将要保存审核状态为:"+state+"？",
                                      QMessageBox.Ok|QMessageBox.Cancel, QMessageBox.Ok)
        if button == QMessageBox.Ok:
            mymdb = myMdb()
            mymdb.update(table='{}'.format('报价基本信息'), 状态='{}'.format(state), where="报价单号='{}'".format(bjdh))
            QMessageBox.information(QWidget(), "报价审核", "审核结果:"+state)
            # self.cbo_state.blockSignals(True)
            # 防止再次选择下拉框引起再次写状态,要清空
            # self.cbo_state.clear()
            # self.cbo_state.blockSignals(False)
            # self.query_list()
        else:
            return

    # 审核保存后清空数据
    def clearData(self):
        # 暂停信号
        self.tblwgt_quote.blockSignals(True)
        self.CBcorporate.addItem("")
        self.quotationNo.setText("")
        self.total_quantity.setText("")
        self.total_price.setText("")
        self.tblwgt_quote.clearContents()
        # for i in range(2, 9):
        #     self.findChild(QLineEdit, "lineEdit_"+str(i)).setText("")
        # 启动信号
        self.tblwgt_quote.blockSignals(False)