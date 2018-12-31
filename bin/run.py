from mbook import Mbook
from createbook import CreateBook
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtSql import QSqlDatabase
import sys

def connectDB():         #db = pymysql.connect(host='127.0.0.1', port=3308, user='root', password='root', db='mrp',charset='utf8',)
    db = QSqlDatabase.addDatabase('QMYSQL')
    db.setDatabaseName('mrp')
    db.setHostName('127.0.0.1')
    db.setUserName('root')
    db.setPassword('root')
    db.setPort(3308)  #('')会提示str错误,不加''就可以了

    if not db.open():
        QMessageBox.critical(None, "严重错误", "数据连接失败，程序无法使用，请按取消键退出", QMessageBox.Cancel)
        return False
    else:
        return db

if __name__ == "__main__":
    app = QApplication(sys.argv)
    db = connectDB()
    if db:
        mb = Mbook(db)
        mb.show()
        sys.exit(app.exec_())