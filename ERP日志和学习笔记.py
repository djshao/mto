2018-12-29
    print(type(date)) 打印date的数据类型
    增加数字为空时设为0,其他类型会自动识别为空
2018-12-28
    1/ 自动报价单号
    2/ fetchone元祖,最大值判断和当天日期值判断,None就用日期值加01,有就用查询值+1
    3/ self.TWquote.setRowCount(rows + rownum)
    4/ 删除行修改为只清除数据,不删行.取消插入多行的方法,用启动就建500行表格的方法,防止Nano单元格

2018-12-26
    mysql重复插入insert时更新on duplicate key update

2018-12-25
    实现用executemany批量导入数据库
    def __new__(self, *args, **kwargs): #通常用于控制生成一个新实例的过程。它是类级别的方法
    def __del__(self):#析构函数，数据库连接模块退出时释放对象时使用
        self.__db.close()
        print('关闭数据库连接')

2018-12-24
    用字典加数组方式改进批量插入.
    建字典的方法
    value_list = [] # 建数组
    for k in range(h): 
        value_dict = {} # 建字典 要放列循环前,行循环内才不出错
        for i in range(cols):
            value_dict['公司名称'] = self.CBcorporate.currentText() #结果是{'公司名称':镇海炼化,...}
        value_list.append(value_dict)

2018-12-23
    py文件若含有from . import 导包或导入函数的情况，无法在该文件下正常执行，而父模块被外部加载时可以正常被使用。
    当一个包里的 __init__ 定义了 __all__ 那么当以 * 方式引入包中的模块的时候 在列表外的模块不会被引入
2018-12-22
    *args：
        （表示的就是将实参中按照位置传值，多出来的值都给args，且以元祖的方式呈现）
    **kwargs：
        （表示的就是形参中按照关键字传值把多余的传值以字典的方式呈现）
    三者的顺序必须是位置参数、*args、**kwargs，不然就会报错：

2018-12-21
    mysql_conn
        转化操作sql类,遇到问题:1/查询返回结果要不要字典问题.字典转列表待研究????????????
    rstrip() 删除 string 字符串末尾的指定字符（默认为空格）

2018-12-19
    修复item缺失时导出问题,self.TWquote.setItem(i, 0, QTableWidgetItem(xh))
    两位小数，字符串形式的：'%.2f' % a 方式最好，其次用Decimal。
        可以传递给Decimal整型或者字符串参数，但不能是浮点数据，因为浮点数据本身就不准确
    # 文件名用变量
    lineedit_dic = {}
    for i in range(5):
        lineedit_dic["lineedit_"+str(i)] = QLineEdit(self)
        lineedit_dic["lineedit_"+str(i)].setText("lineedit_"+str(i))

2018-12-18
    设置lineEdit当前时间
        self.quotedate.setText(time.strftime("%Y-%m-%d", time.localtime()))
    设置timeEdit当前时间
        self.quotedate.setText(QDate.currentDate())

2018-12-17
    global 修饰符 当做全局变量使用
        函数定义了本地作用域，而模块定义的是全局作用域。
        在模块层面定义的变量（无需global修饰），如果在函数中没有再定义同名变量，可以在函数中当做全局变量使用：
        但如果在函数中有再赋值/定义（因为python是弱类型语言，赋值语句和其定义变量的语句一样），则会产生引用了未定义变量的错误：
        如果想要在函数内定义全局作用域，需要加上global修饰符
        hehe=6
        def f():
            global hehe
            print(hehe)
            hehe=3
        f()
        print(hehe)

    pandas
        是基于numpy构建的，使得数据分析工作变得更快更简单的高级数据结构和操作工具
    NumPy
        它是一个由多维数组对象和用于处理数组的例程集合组成的库
        使用NumPy，开发人员可以执行以下操作：
        数组的算数和逻辑运算。
        傅立叶变换和用于图形操作的例程。
        与线性代数有关的操作。 NumPy 拥有线性代数和随机数生成的内置函数。

2018-12-16
    空值问题:
        pandas中空值nan
        tablewidget中空值,未选择时为none,选择后为"",需考虑转换数据类型?????
        转换数据类型参考学习参考源码中pandas
        返回原来数据可参考<学点编程8>的mbook on_TWquote_currentCellChanged
        修改数量和总价列后自动计算总数量和总价.
    decimal模块
    #研究金额大写
        1.可以传递给Decimal整型或者字符串参数，但不能是浮点数据，因为浮点数据本身就不准确。
            对于浮点数需要先将其转换为字符串.Decimal()的构造中如果是小数或字符的话，需要加上单引号；如果为整数，则不需要
        2.要从浮点数据转换为Decimal类型
            from decimal import *  # 浮点数据转换为Decimal类型
            Decimal.from_float(12.222)
            # 结果为Decimal('12.2219999999999995310417943983338773250579833984375')
        3.通过设定有效数字，限定结果样式：
            getcontext().prec = 6
            Decimal(1)/Decimal(7)
            # 结果为Decimal('0.142857')，六个有效数字
        4.四舍五入，保留几位小数
            from decimal import *
            Decimal('50.5679').quantize(Decimal('0.00'))
            # 结果为Decimal('50.57')，结果四舍五入保留了两位小数
        5.Decimal 结果转化为string
            from decimal import *
            str(Decimal('3.40').quantize(Decimal('0.0')))
            # 结果为'3.40'，字符串类型


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
    #一条INSERT语句插入批量数据的写法：
    INSERT INTO [表名]([列名],[列名]) VALUES
        ([列值],[列值])),
        ([列值],[列值])),
        ([列值],[列值]));
    判断空值的两种方法:if self.TWquote.item(0,i)==None:                      #item没输过为None,输过后是NULL
                    if not self.TWquote.item(0,i):                         #没修改过是没有item,用None或not,不用带text()
                    if self.TWquote.item(0, i).text() == "":               #修改过就有item用"",要加text()
    INSERT INTO #数据库必须字段数量相同才能插入.
    QTableWidget::scrollToItem                 #显示最后一行
    myTable->setRowCount(myTable->rowCount()+1)# 随着数据增加动态添加行 
    num->setCheckState(Qt::Unchecked);         #加入复选框
    if(NULL != TWquote.item(i, 0)) ????#判断某一列最大行数,用于取最后一行行号

2018-12-10
def getRow(self):      #获取QTableWidget中所有已选行的行号
        self.selectedRow = list()
        item = self.qtablewidget.selectedItems()
        for i in item:
            if self.qtablewidget.indexFromItem(i).row() not in self.selectedRow:
                self.selectedRow.append(self.qtablewidget.indexFromItem(i).row())
--------------------- 

2018-12-09  学习命名规范
    \版本注记：定义一个变量version = "Revision: 1.4"
    运算符除 * 外，两边空1格分隔，函数参数=周围不用空格
    每行长度限制在79字符内，使用行末反斜杠折叠长行
    与None之类的单值比较，永远用:'is'或'is not'来做：if x is not None
    在模块和包内定义基异常类(base exception class)
    使用字符串方法(methods)代替字符串模块。
    在检查前缀或后缀时避免对字符串进行切片，用startswith()和endswith()代替，如：No: if foo[:3] == 'bar':Yes: if foo.startswith('bar'):
    只用isinstance()进行对象类型的比较，如：No: if type(obj) is type(1):Yes: if isinstance(obj, int)
    判断True或False不要用 ==，如：No: if greeting == True:Yes: if greeting:

    1、模块
        不含下划线、简短、全小写;
    2、类名、异常名：
        类名使用驼峰(CamelCase)命名风格，首字母大写，私有类可用一个下划线开头.连续写,中间不用_.
        将相关的类和顶级函数放在同一个模块里;
    3、函数
        函数名一律小写，如有多个单词，用下划线隔开.私有函数在函数前加一个下划线_.规划在两单词间用_.
    4、变量名
        变量名尽量小写, 如有多个单词，用下划线隔开
    5、常量
        常量使用以下划线分隔的大写命名



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
    self.mdi.tileSubWindows()  # 多文档界面平铺窗口
    row = self.tableWidget.row(item)        #根据单元格对象取得其在表格中的行和列号
    column = self.tableWidget.column(item)  
    totalrow = self.tableWidget.rowCount()  #totalrow为表格中的行数
    # 取查询后的表头列表
    col_lst_3 = [tup[0] for tup in cur_3.description]
    ()tup元组,[]数组,{}dict字典

\获取单元格内容
    self.Quote_list.itemClicked.connect(self.querydetail)  #单元格点击事件
    def querydt(self, item):
        print('you selected => '+ item.text())             #打印单元格内容
        self.Line_search.setText(item.text())              #设置搜索框等于单元格的内容
    def querydetail(self):
        h = self.Quote_list.currentIndex().row()            #找到所选行的行数h
        bjdh = self.Quote_list.item(h, 0).text()            #找到所选h行的0位报价单号

\消息框（QMessageBox）
    # 信息框
    QMessageBox.information(self, '框名', '内容', 按钮s, 默认按钮) 
    # 问答框
    QMessageBox.question(self, '框名', '内容', 按钮s, 默认按钮)
    # 警告框
    QMessageBox.warning(self, '框名', '内容', 按钮s, 默认按钮) 
    # 危险框
    QMessageBox.ctitical(self, '框名', '内容', 按钮s, 默认按钮)
    # 关于框
    QMessageBox.about(self, '框名', '内容') 
