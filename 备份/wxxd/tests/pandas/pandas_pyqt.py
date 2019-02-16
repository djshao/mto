# -*- coding: utf-8 -*-

"""
Module implementing MainWindow.
"""

from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidget, QTableWidgetItem, QTableView, QHeaderView

import pymysql
from qtpandas.models.DataFrameModel import DataFrameModel
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import time

from Ui_pandasmain import Ui_MainWindow


class PandasWindow(QMainWindow, Ui_MainWindow):
    """
    pandas_pyqt.
    """
    def __init__(self, parent=None):
        """
        Constructor构造函数

        @父控件的参数父引用
        @type QWidget
        """
        super(PandasWindow, self).__init__(parent)
        self.setupUi(self)

        # 初始化pandasqt
        # widget = self.pandastablewidget
        # self.widget.resize(600, 500) # 如果对部件尺寸大小不满意可以在这里设置

        self.model = DataFrameModel() # 设置新的模型
        self.widget.setViewModel(self.model)

        # MySQL法连接数据库,读取数据需要转换
        # conn = pymysql.connect(
        #     host='localhost', port=3308, user='root', password='root', db='mrp', charset='utf8')
        sql = 'select * from ht'
        # self.df = pd.read_sql(sql, conn)

        # 通过sqlalchemy.create_engine建立连接引擎.echo=True，会显示在加载数据库所执行的SQL语句，可不选此参数，默认为False
        # engine = create_engine("mysql+pymysql://root:root@127.0.0.1:3308/mrp?charset=utf8")
        # engine = create_engine('mysql+pymysql://root:root@127.0.0.1:3308/mrp', encoding='utf-8', echo=True)
        # engine = create_engine(
        #     "mysql+pymysql://{}:{}@{}/{}".format('root', 'root', 'localhost:3308', 'mrp'), encoding='utf-8')

        # engine = create_engine(
        #     "mysql+mysqlconnector://{}:{}@{}/{}".format
        #     ('root', 'root', 'localhost:3308', 'mrp'), encoding='utf-8')
        engine = create_engine("mysql+mysqlconnector://root:root@localhost:3308/mrp?charset=utf8")
        # con = engine.connect()  # 创建连接


        # SQLAlchemy法,查询数据并转为pandas.DataFrame，指定DataFrame的index为数据库中的生产编号字段
        self.df = pd.read_sql(sql, engine)
        # self.df.head()
        # print(self.df.head())
        # self.new_df = self.df[["生产编号", "序号", "名称", "制造标准", "规格型号", "材质", "数量", "已机加数", "机加部门", "机加日期", "生产状态"]]
        # print(self.df)
        # 读取excel表格数据
        # self.df = pd.read_excel(r'C:/Users/Administrator/Desktop/报价模板1.xlsx', encoding='utf-8')
        # self.df_original = self.df.copy() # 备份原始数据

        #创建与数据库的会话session class ,注意,这里返回给session的是个class类,不是实例
        self.session = sessionmaker(bind=engine)()  # 另一种方法
        # DBSession = sessionmaker(bind=engine)       #创建用于数据库session对象
        # self.session = DBSession()                  #这里才是生成session实例可以理解为cursor

        self.model.setDataFrame(self.df)
        self.widget.tableView.horizontalHeader().setStretchLastSection(True)
        # self.widget.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.widget.tableView.resizeColumnsToContents()
        self.widget.tableView.resizeRowsToContents()

    # ==============将mysql数据库中文件查询生成dataframe格式文件，写入tableWidget文件=====================================
        # if self.new_df.empty==False:
        #     row_num3=self.new_df.shape[0]  # 取行数
        #     col_num3=self.new_df.shape[1]  # 取列数
        #     self.tableWidget.setRowCount(row_num3)
        #     self.tableWidget.setColumnCount(col_num3)
        #     for i in range(row_num3):
        #         for j in range(col_num3):
        #             temp_db_a2=self.new_df.iloc[i, j]
        #             db_a2=QTableWidgetItem(str(temp_db_a2))
        #             self.tableWidget.setItem(i, j, db_a2)
        #     # 取列名称,设为列表
        #     col_name3=list(self.new_df.columns)
        #     # print(col_name3)
        #     self.tableWidget.setHorizontalHeaderLabels(col_name3)  # 设置标题列名

    # =========================常用pandas代码==============================
        # 测试插入时间
        # start = time.clock()
        # end = time.clock()
        # print('[插入多个执行] 使用时间:', end-start)
        # print(self.df.describe())  # 基础数据集统计结果
        # self.df.info()  # 基础数据集特征信息
        #替换丢失的数据 用“value”的值替换“to_replace”中给出的值。
        # self.df.replace(to_replace=None, value=None)
        # 将对象类型转换为 float  将对象类型转换为数字型以便计算（如果它们是字符串的话）
        # self.pd.to_numeric(self.df["feature_name"], errors='coerce')
        # 将数据转换为 Numpy 数组
        # self.df.as_matrix()
        # 获取数据的头“n”行
        # self.df.head(n)
        # 按特征名称获取数据
        # self.df.loc[feature_name]
        # 这个函数将数据里“height”一列中的所有值乘以2
        # self.df["height"].apply(*lambda* height: 2 * height)
        # 重命名数据列  将数据的第3列重命名为“size”
        # self.df.rename(columns = {self.df.columns[2]:'size'}, inplace=True)
        # 单独提取某一列
        # self.df["name"].unique()
        # 访问子数据 从数据中选择“name”和“size”两列
        # new_df = self.df[["name", "size"]]

        # self.df.columns  # 列出列名称
        # 数据之和df.sum()
        # 数据中的最小值df.min()
        # 数据中的最大值df.max()
        # 最小值的索引df.idxmin()
        # 最大值的索引df.idxmax()
        # 数据统计信息，有四分位数，中位数等df.describe()
        # 平均值df.mean()
        # 中位数值df.median() 
        # '数量'列之和df.sum()
        # d = self.df.loc[:, '数量'].sum()
        # print('d' +str(d))
        # self.df.apply(sum)
        # column_sum = self.df.iloc[:,j].sum()

        # 对数据进行排序
        # self.df.sort_values(ascending = False)
        # 布尔索引 过滤“size”的数据列，以显示等于5的值：
        # self.df[self.df["size"] == 5]
        # 选择某值 选择“size”列的第一行：
        # self.df.loc([0], ['size'])


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

        # data_base.to_sql('stock_class',engine,index=False,if_exists='append',dtype=dtypedict,chunksize=100)参考


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
        # print(self.df)
        engine = create_engine("mysql+pymysql://root:root@127.0.0.1:3308/mrp?charset=utf8")
        # index=False自增型关键字用false默认为True，指定DataFrame的index是否一同写入数据库
        self.new_df = self.df[["生产编号", "序号", "处理数量", "处理工艺"]]
        print(self.new_df)
        # 去掉ID主键,因ID是自增型
        # self.new_df.to_sql(name='ht', con=engine, if_exists='fail', index=False)
        # sql_1 = "INSERT INTO ht (生产编号,序号,处理日期,处理数量,处理工艺) VALUES(%s, %s, %s, %s, %s)  \
        #         ON DUPLICATE KEY UPDATE 处理日期=VALUES(处理日期),处理数量=VALUES(处理数量),处理工艺=VALUES(处理工艺)"

        for row in range(0, len(self.new_df)):
            row_data = table_class(column_1=self.new_df.ix[i]['生产编号'],
                                    column_2=self.new_df.ix[i]['序号'],
                                )
            self.session.merge(row_data)
            self.session.commit()

        # pd.io.sql.to_sql(df1,tablename,con=conn,if_exists='repalce')
        # sql法写入数据库
        # self.df.to_sql(name='order_list',con=engine,if_exists='append',index=False)
        # sqlalchemy法写入数据库
        # df.to_sql(目标表名,con=engine, schema=数据库名, index=False, index_label=False, if_exists='append', chunksize=1000)
        # con.dispose() # engine.dispose()


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    ui = PandasWindow()
    ui.show()
    sys.exit(app.exec_())
