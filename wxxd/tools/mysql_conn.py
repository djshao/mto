#安装PyMySQL：pip3 install PyMySQL  
#!/usr/bin/python3  
#coding=utf-8  
#数据库操作类

from PyQt5.QtSql import QSqlDatabase
from datetime import *
import pymysql as mdb
import hashlib
import time


def connectDB():
    """ db = pymysql.connect(host='127.0.0.1', port=3308, user='root', password='root', db='mrp',charset='utf8',)"""
    db = QSqlDatabase.addDatabase('QMYSQL')
    db.setDatabaseName('mrp')
    db.setHostName('localhost')
    db.setUserName('root')
    db.setPassword('root')
    db.setPort(3308)


class myMdb(object):
    #数据库连接对象
    __db = None
    #游标对象
    __cursor = None
    def __new__(self, *args, **kwargs): #__new__ 通常用于控制生成一个新实例的过程。它是类级别的方法
        if not hasattr(self, '_instance'): # 参数是一个对象和一个字符串，如果字符串是对象属性之一的命名，则返回True，否则False
            self._instance = super().__new__(self)
            #主机
            host = 'host' in kwargs and kwargs['host'] or 'localhost'
            #端口
            port = 'port' in kwargs and kwargs['port'] or '3308'
            #用户名
            user = 'user' in kwargs and kwargs['user'] or 'root'
            #密码
            passwd = 'passwd' in kwargs and kwargs['passwd'] or 'root'
            #数据库
            db = 'db' in kwargs and kwargs['db'] or 'mrp'
            #编码
            charset = 'charset' in kwargs and kwargs['charset'] or 'utf8'
            # 打开数据库连接  
            # print('连接数据库')
            self.__db = mdb.connect(host=host,port=int(port),user=user,passwd=passwd,db=db,charset=charset)
            #创建一个游标对象 cursor
            self.__cursor = self.__db.cursor()
            # self.__cursor = self.__db.cursor(cursor=mdb.cursors.DictCursor) # 游标类型为字典类型
        return self._instance

    #返回执行execute()方法后影响的行数 
    def execute(self, sql):
        self.__cursor.execute(sql)
        rowcount = self.__cursor.rowcount
        return rowcount

    # 增->返回新增ID
    def insert(self, **kwargs):
        table = kwargs['table'] # 取字典中的table值
        del kwargs['table']
        sql = 'insert into %s set '%table
        for k, v in kwargs.items():
            sql += "`%s`='%s',"%(k, v)
        sql = sql.rstrip(',') # rstrip() 删除 string 字符串末尾的指定的','字符.（默认为空格）
        # a = "on duplicate key update"
        # sql = sql +" " +a
        # print(sql)
        try:
            # 执行SQL语句
            self.__cursor.execute(sql)
            # 提交到数据库执行
            self.__db.commit()
            #获取自增id
            res = self.__cursor.lastrowid
        except Exception as e:
            # 发生错误时回滚
            print(e)
            self.__db.rollback()
        else:
            return res

    def insert_many(self, sql, param): # 批量插入executemany
        """executemany批量插入数据库"""
        a = "ON DUPLICATE KEY UPDATE"  # 自动判断是否有记录,待研究??????
        try:
            self.__cursor.executemany(sql,param)
            self.__db.commit()
            rowcount = self.__cursor.rowcount
        except Exception as e:
            print(e)
            self.__db.rollback()
        else:
            return rowcount
        # print(rowcount)

        #测试插入时间
        # start = time.clock()
        # insert_many(table)
        # end = time.clock()
        # print('[insert_many executemany] Time Usage:',end-start)

    # 批量插入->返回影响的行数
    def insertMap(jsonArray, tableName):
        """批量插入,返回影响行数rowcount"""
        for json in jsonArray:#遍历每一个子json 下面是为每一个json拼接sql 并执行
            preSql = "insert into "+tableName+" ("  #前一段拼接字段
            subSql = "values("                       #后一段拼接字段
            exc = ()   # 作为execute的参数值，这是一个tuble类型
            for x in json:  # 取出每一个子json的key和value值
                preSql += x + ","  # 拼接前面sql的key值
                subSql += "%s,"   # 拼接后面sql的value数量
                exc = exc + (json[x],)  # 每次 给exc添加新的值tuble，注意后面的“，”号不能少，否则不能识别为一个tuble
            preSql = preSql[0:preSql.__len__()-1] + ")"  # 去掉后面的“，”再添加“）”
            subSql = subSql[0:subSql.__len__()-1] + ")"  # 去掉后面的“，”再添加“）”
            sql = preSql+subSql  # 前后相加成一个完整的sql
            # print(sql)
            # print(exc)
            try:
                self.__cursor.execute(sql, exc)  # 将拼接好的sql和exc作为传入参数 执行
                # self.__db.commit()
                # 影响的行数
                rowcount = self.__cursor.rowcount
            except:
                self.__db.rollback()
            else:
                return rowcount
        self.__db.commit()
    #测试代码见图片 模块名.insertMap(jsonArray, "students")

    #删->返回影响的行数
    def delete(self, **kwargs):
        table = kwargs['table']
        where = kwargs['where']
        sql = 'DELETE FROM %s where %s'%(table,where)
        print(sql)
        try:
            # 执行SQL语句
            self.__cursor.execute(sql)
            # 提交到数据库执行
            self.__db.commit()
            #影响的行数
            rowcount = self.__cursor.rowcount
        except:
            # 发生错误时回滚
            self.__db.rollback()
        else:
            return rowcount

    #改->返回影响的行数
    def update(self, **kwargs):
        flag = False
        table = kwargs['table']
        #del kwargs['table']
        kwargs.pop('table')  # 如果键值table在字典中存在，删除dict[table]，返回 dict[table]的value值。

        where = kwargs['where']
        kwargs.pop('where')

        sql = 'update %s set '%table
        for k, v in kwargs.items():  # 待研究'是否合理问题,是否需要去除.1月3日去除',待看后面是否出问题????
            sql += "%s=%s,"%(k, v)
        sql = sql.rstrip(',')
        sql += ' where %s'%where
        print(sql)
        try:
            # 执行SQL语句
            self.__cursor.execute(sql)
            # 提交到数据库执行
            self.__db.commit()
            flag = True
            #影响的行数
            rowcount = self.__cursor.rowcount
        except:
            # 发生错误时回滚
            flag = False
            self.__db.rollback()
            print("执行失败, %s" % err)
        else:
            return rowcount
            # return flag

    #查->单条数据
    def fetchone(self, **kwargs):
        table = kwargs['table']
        #字段
        field = 'field' in kwargs and kwargs['field'] or '*'
        #where
        where = 'where' in kwargs and 'where '+kwargs['where'] or ''
        #order
        order = 'order' in kwargs and 'order by '+ kwargs['order'] or ''
        sql = 'select %s from %s %s %s limit 1'%(field,table,where,order)
        # print(sql)
        try:
            # 执行SQL语句
            self.__cursor.execute(sql)
            # 使用 fetchone() 方法获取单条数据.
            data = self.__cursor.fetchone()
        except:
            # 发生错误时回滚
            self.__db.rollback()
        else:
            return data

    #查->多条数据
    def fetchall(self, **kwargs):
        data = ""
        table = kwargs['table']
        #字段
        field = 'field' in kwargs and kwargs['field'] or '*'
        #where
        where = 'where' in kwargs and 'where '+kwargs['where'] or ''
        #order
        order = 'order' in kwargs and 'order by '+ kwargs['order'] or ''
        #limit
        limit = 'limit' in kwargs and 'limit '+ kwargs['limit'] or ''
        sql = 'select %s from %s %s %s %s'%(field,table,where,order,limit)
        # print(sql)
        try:
            # 执行SQL语句
            self.__cursor.execute(sql)
            # 使用 fetchone() 方法获取单条数据.
            data = self.__cursor.fetchall()
            # print('data' +str(data))
        except:
            # 发生错误时回滚
            self.__db.rollback()
        else:
            return data

    #析构函数，释放对象时使用
    def __del__(self):
        # 关闭数据库连接
        # self.__cursor.close()
        self.__db.close()
        # print('关闭数据库连接')


#生成md5
def makeMd5(mstr):
    hmd5 = hashlib.md5()
    hmd5.update(mstr.encode("utf-8"))
    return hmd5.hexdigest()


#获取unix时间戳
def getTime():
    return round(time.time())


#时间格式化
def timeFormat(timestamp):
    #return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timestamp))
    #return datetime.fromtimestamp(timestamp)
    return datetime.utcfromtimestamp(timestamp)


# if __name__ == '__main__':
 
 
    # dbObject = myMdb(host='localhost',port=3308,user='root',passwd='root',db='mrp',charset='utf8')
 
 
#     #创建表
#     print('创建表:')
#     sql = "DROP TABLE IF EXISTS `user`;"
#     dbObject.execute(sql)
#     sql = '''
#     CREATE TABLE `user` (
#     `id` int(11) NOT NULL AUTO_INCREMENT,
#     `name` varchar(50) NOT NULL,
#     `pwd` char(32) NOT NULL,
#     `insert_time` int(11) NOT NULL,
#     PRIMARY KEY (`id`)
#     ) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COMMENT='用户表';
#     '''
#     print(sql)
#     res = dbObject.execute(sql)
#     print(res)
 
 
    #写入数据
    # print('\n写入数据:')
    # pwd = makeMd5('root')
    # insert_time = getTime()
    # res = dbObject.insert(table='user',name='aaaa',pwd=pwd,insert_time=insert_time)
    # print(res)
 
 
#     time.sleep(1)
#     pwd = makeMd5('root')
#     insert_time = getTime()
#     res = dbObject.insert(table='user',name='bbbb',pwd=pwd,insert_time=insert_time)
#     print(res)
 
 
#     time.sleep(1)
#     pwd = makeMd5('111111')
#     insert_time = getTime()
#     res = dbObject.insert(table='user',name='cccc',pwd=pwd,insert_time=insert_time)
#     print(res)
 
 
#     #查询数据-单条
#     print('\n查询数据-单条:')
#     res = dbObject.fetchone(table='user',where="name='cccc'")
#     print(res)
 
 
#     #修改数据
#     print('\n修改数据:')
#     res = dbObject.update(table='user',where="id=1",name='dddd')
#     print(res)
 
 
#     #删除数据
#     print('\n删除数据:')
#     res = dbObject.delete(table='user',where="id=2")
#     print(res)
 
 
#     #查询数据-多条
#     print('\n查询数据-多条:')
#     res = dbObject.fetchall(table='user',order="id desc")  #  cursor.fetchmany(3)取3行
#     print(res,type(res))
#     if res:
#         for value in res:
#             print('name:%s,date:%s'%(value['name'],timeFormat(value['insert_time'])))
