# -*- coding: utf-8 -*-

"""工具函数模块"""

# 计算列值总数函数
def sum_columns(table, l):
    """计算所选列的总数,table为tablewidget表名,l为列数"""
    count = 0
    # 获取表格中的总行数,考虑到保存时有空行的情况用总行数.
    rows = self.table.rowCount()
    for i in range(rows):
        # 判断不存在和空值,并设为0值
        if not self.table.item(i, l):
            count += 0
        elif self.table.item(i, l).text() == "":
            count += 0
        else:
            count += Decimal(self.table.item(i, l).text())
        print('整列值='+str(count))
    return count