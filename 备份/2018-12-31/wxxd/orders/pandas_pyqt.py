# -*- coding: utf-8 -*-

"""
Module implementing MainWindow.
"""

from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtWidgets import QMainWindow, QApplication

import pymysql
from qtpandas.models.DataFrameModel import DataFrameModel
import pandas as pd
from sqlalchemy import create_engine

from orders.Ui_pandas_pyqt import Ui_MainWindow


class OrderWindow(QMainWindow, Ui_MainWindow):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(OrderWindow, self).__init__(parent)
        self.setupUi(self)
        
        '''初始化pandasqt'''
        widget = self.pandastablewidget
        widget.resize(600, 500) # 如果对部件尺寸大小不满意可以在这里设置
        
        
        self.model = DataFrameModel() # 设置新的模型
        widget.setViewModel(self.model)
        
        # conn = pymysql.connect(host='localhost', port=3308,user='root',password='root',db='mrp',charset='utf8')
        # # 通过sqlalchemy.create_engine建立连接引擎
        # engine = create_engine('mysql+pymysql://root:root@localhost:3308/mrp')
        # sql = 'select * from user'
        # self.df = pd.read_sql(sql, con=conn)#MySQL法连接数据库,读取数据需要转换
        # self.df = pd.read_sql(sql, engine)#SQLAlchemy法可以直接创建dataframe
        # self.df.to_sql(name='user',con=engine,if_exists='append',index=False)  写入数据库
        # df.to_sql(目标表名,con=engine, schema=数据库名, index=False, index_label=False, if_exists='append', chunksize=1000)
        # pd.io.sql.to_sql(df,table_name,con=conn,schema='w_analysis',if_exists='append') 两个语句???

        self.df = pd.read_excel(r'C:/Users/Administrator/Desktop/报价模板.xlsx',encoding='utf-8')
        # self.df_original = self.df.copy() # 备份原始数据
        self.model.setDataFrame(self.df)
        
        d = self.df.loc[:,'num'].sum()
        print('d' +str(d))
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

    # 定义函数，自动输出DataFrme数据写入mysql的数类型字典表,配合to_sql方法使用(注意，其类型只能是SQLAlchemy type )
    def mapping_df_types(df):
        """自动获取DataFrme各列的数据类型，生成字典。"""
        dtypedict = {}
        for i, j in zip(df.columns, df.dtypes):
            if "object" in str(j):
                dtypedict.update({i: VARCHAR(256)})
            if "float" in str(j):
                dtypedict.update({i: NUMBER(19,8)})
            if "int" in str(j):
                dtypedict.update({i: VARCHAR(19)})
        return dtypedict

        #data_base.to_sql('stock_class',engine,index=False,if_exists='append',dtype=dtypedict,chunksize=100)参考


    
    @pyqtSlot()
    def on_pushButton_clicked(self):
        """
        初始化pandas
        """
        self.model.setDataFrame(self.df_original)
    
    @pyqtSlot()
    def on_pushButton_2_clicked(self):
        """
        保存数据
        """
        # self.df.to_excel(r'./data/fund_data_new.xlsx')
        engine = create_engine('mysql+pymysql://root:root@localhost:3308/mrp')
        self.df.to_sql(name='test',con=engine,if_exists='append',index=False)#index=False自增型关键字用false默认为True，指定DataFrame的index是否一同写入数据库
        # con.dispose() # engine.dispose()
       

if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    ui = OrderWindow()
    ui.show()
    sys.exit(app.exec_())
