2018-12-16
    空值问题:
    pandas中空值nan
    tablewidget中空值,未选择时为none,选择后为"",需考虑转换数据类型?????
    转换数据类型参考学习参考源码中pandas
    返回原来数据可参考<学点编程8>的mbook on_TWquote_currentCellChanged
    修改数量和总价列后自动计算总数量和总价.
    研究金额大写


201812-15
    lambda匿名函数
    lambda argument_list: expression  #argument_list是参数列表。它的结构与Python中函数(function)的参数列表是一样的
                                       #expression是一个关于参数的表达式。表达式中出现的参数需要在argument_list中有定义
        lambda x, y: x*y；函数输入是x和y，输出是它们的积x*y
        lambda:None；函数没有输入参数，输出是None
        lambda *args: sum(args); 输入是任意个数的参数，输出是它们的和(隐性要求是输入参数必须能够进行加法运算)
        lambda **kwargs: 1；输入是任意键值对参数，输出是1
    setattr(object, name, values) # 给对象的属性赋值，若属性不存在，先创建再赋值
    修改combobox附加数据库查询的公司名称记录,用循环赋值添加到列表中的方法
    修改报价时间为当前时间,修改为弹出日历的方式.
    
2018-12-14
    增加报价导入Excel表功能
    QSqlTableModel 类为单个数据库表提供了一个可编辑的数据模型
    pyqt5用QSqlTableModel
    ORM框架采用SQLAlchemy+pandas
    pandas两个操作符:
        loc：通过行和列的索引来访问数据
        iloc：通过行和列的下标来访问数据
    修改右键菜单,参考mbook模块
    
2018-12-12
    """ 一条INSERT语句插入批量数据的写法：
    INSERT INTO [表名]([列名],[列名]) VALUES
    ([列值],[列值])),
    ([列值],[列值])),
    ([列值],[列值]));"""
    判断空值的两种方法:if self.TWquote.item(0,i)==None: ??????#tablewidget格子中没输过为None,输过后有变化,出错||
                    if not self.TWquote.item(0,i):没修改过是没有item,用None或not
                    if self.TWquote.item(0,i)=='':修改过就有item用''
    INSERT INTO #数据库必须字段数量相同才能插入.
    QTableWidget::scrollToItem #显示最后一行
    myTable->setRowCount(myTable->rowCount()+1)# 随着数据增加动态添加行 
    num->setCheckState(Qt::Unchecked);   #加入复选框
    if(NULL != m_pTrainTable.item(i, 0)) ????#判断某一列最大行数,用于取最后一行行号

2018-12-10
def getRow(self):      #获取QTableWidget中所有已选行的行号
        self.selectedRow = list()
        item = self.qtablewidget.selectedItems()
        for i in item:
            if self.qtablewidget.indexFromItem(i).row() not in self.selectedRow:
                self.selectedRow.append(self.qtablewidget.indexFromItem(i).row())
--------------------- 

2018-12-09  学习命名规范
    1、模块
    模块尽量使用小写命名，首字母保持小写，尽量不要用下划线(除非多个单词，且数量不多的情况)
    2、类名
    类名使用驼峰(CamelCase)命名风格，首字母大写，私有类可用一个下划线开头.连续写,中间不用_.
    将相关的类和顶级函数放在同一个模块里. 不像Java, 没必要限制一个类一个模块.
    3、函数
    函数名一律小写，如有多个单词，用下划线隔开.私有函数在函数前加一个下划线_.规划在两单词间用_.
    4、变量名
    变量名尽量小写, 如有多个单词，用下划线隔开
    常量采用全大写，如有多个单词，使用下划线隔开
    5、常量
    常量使用以下划线分隔的大写命名

self.mdi.tileSubWindows()#多文档界面平铺窗口

12-06
    关闭窗口btn.clicked.connect(QCoreApplication.instance().quit)  instance()方法为我们提供了其当前实例
    addStrtch()，拉伸因子,它的作用是在布局中添加空白，并把非空白内容顶到布局的尾部
    grid.addWidget(reviewEdit, 3, 1, 5, 1) 网格布局并且设置了组件之间的间距,让reviewEdit组件跨了5行。
    .clearContents清除内容,.clear清空表格中所有内容（包含表头）

12-05
    考虑窗口分割问题,是选分割条还是用两个窗口?

2018-12-04
    考虑放弃工作任务栏,还是用工作菜单栏进入各工作目录
    多窗口可以用多文档界面,或者Qtabwidget,加关闭功能(缺点是不能同时显示)
    优化报价审核
    self.Widget_details.horizontalHeader().setStretchLastSection(True)#最后一列对齐边框

2018-11-29
    学习多文档界面,对比打开子窗口,选择了用多文档界面,可以打开多个窗口,可以多种排列.
    row = self.tableWidget.row(item)        #根据单元格对象取得其在表格中的行和列号
    column = self.tableWidget.column(item)  
    totalrow = self.tableWidget.rowCount()  #totalrow为表格中的行数