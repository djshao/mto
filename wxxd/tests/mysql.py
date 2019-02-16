#coding=utf-8
import pymysql
conn= pymysql.connect(
        host='localhost',
        port = 3308,
        user='root',
        passwd='root',
        db ='mrp',
        )
cur = conn.cursor()
#jsonArray：传入的json数组，每个字段名后面跟值，不一定要填全。例：
# jsonArray = [{'sid':'1', 'sname':'xuteng','gender':'hello','birthday':'1995-08-31','address':'hubei'},
#              {'sid':'2', 'sname':'xuteng','birthday':'1995-08-31','address':'hubei'},
#              {'sid':'3', 'sname':'xuteng','gender':'hello','birthday':'1995-08-31'}]
def insertMap(jsonArray,tableName):
        for json in jsonArray:#遍历每一个子json 下面是为每一个json拼接sql 并执行
                preSql = "insert into "+tableName+" ("  #前一段拼接字段
                subSql ="values("                       #后一段拼接字段
                exc = ()   #作为execute的参数值，这是一个tuble类型
                for x in json:# 取出每一个子json的key和value值
                    preSql += x + "," #拼接前面sql的key值
                    subSql += "%s,"   #拼接后面sql的value数量
                    exc = exc + (json[x],)#每次 给exc添加新的值tuble，注意后面的“，”号不能少，否则不能识别为一个tuble
                preSql = preSql[0:preSql.__len__()-1] + ")"#去掉后面的“，”再添加“）”
                subSql = subSql[0:subSql.__len__()-1] + ")"#去掉后面的“，”再添加“）”
                sql = preSql+subSql  #前后相加成一个完整的sql
                print(sql)
                print(exc)
                cur.execute(sql,exc) #将拼接好的sql和exc作为传入参数 执行
        cur.close()
        conn.commit()
        conn.close()
#测试代码见图片 模块名.insertMap(jsonArray, "students")
