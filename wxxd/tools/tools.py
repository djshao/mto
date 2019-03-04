# -*- coding: utf-8 -*-
"""工具函数模块"""

from PyQt5.QtWidgets import *

from decimal import Decimal



# 计算列值总数函数plus 加,和
def plusColumn(self, name, l):
    """计算所选列的总数,l为列数;plus 加,和
    name:tablewidget的objectname
    l:要计算的列
    """
    count = 0
    m_child = self.findChild(QTableWidget, name)
    rows = m_child.rowCount()
    for i in range(rows):
        if not m_child.item(i, l) or m_child.item(i, l).text() == "":
            return count
        else:
            count += Decimal(m_child.item(i, l).text())
    return count

    #     # 判断不存在和空值,并设为0值
    #     if not m_child.item(i, l):
    #         count += 0
    #     elif m_child.item(i, l).text() == "":
    #         count += 0
    #     else:
    #         count += int(m_child.item(i, l).text())
    # return count

def computePrice(self, name, row):
    """修改后重新计算单价/总价"""
    m_child = self.findChild(QTableWidget, name)
    m_child.blockSignals(True)  # 暂停单元格修改信号

    # 数量quantity
    quantity = int(m_child.item(row, 7).text())
    # 单重unit weight                  
    if m_child.item(row, 12).text() == "":
        weight = 0
    else:
        weight = Decimal(str(m_child.item(row, 12).text()))
    # 公斤价weight price
    if m_child.item(row, 13).text() == "":
        weight_price = 0
    else:
        weight_price = Decimal(str(m_child.item(row, 13).text()))
    # 加工费cost
    if m_child.item(row, 14).text() == "":
        cost = 0
    else:
        cost = Decimal(str(m_child.item(row, 14).text()))
    # 其他费用expenses
    if m_child.item(row, 15).text() == "":
        expenses = 0
    else:
        expenses = Decimal(str(m_child.item(row, 15).text()))
    # 计算单价    公斤价="0.00或0时直接用单价,需要转化字符类型再==
    m_price = m_child.item(row, 10).text()
    if float(m_price) == float(0.00) or float(m_price) == float(0):
        price = Decimal(str(m_price))
    else:
        # 单价=单重*公斤价+加工费+其他费用
        price = weight*weight_price+cost+expenses
    # 更新单价,小数点2位
    m_child.setItem(row, 10, QTableWidgetItem(str('%.2f' % price)))
    # 更新总价amount=数量*单价
    amount = Decimal(quantity*price)
    m_child.setItem(row, 11, QTableWidgetItem(str('%.2f' % amount)))

    m_child.blockSignals(False)  # 恢复单元格修改信号