# -*- coding: utf-8 -*-
"""全局变量管理模块
拼装成字典构造全局变量
import global_demo as gl
    gl._init()  先必须在主模块初始化（只在Main模块需要一次即可）
    gl.set_value('name', 'cc')  设置全局变量
    name = gl.get_value('name')  获取全局变量"""

def _init():  # 初始化
    global _g_dict
    _g_dict = {}

def set_value(key, value):
    """ 定义一个全局变量 """
    _g_dict[key] = value

def del_value(key):
    """删除一个key"""
    try:
        del _g_dict[key]
        return _g_dict
    except KeyError:
        print("key:'{}'不存在".format(key))

def get_value(key, defValue=None):
    """ 获得一个全局变量,不存在则返回默认值 """
    try:
        return _g_dict[key]
    except KeyError:
        return defValue

# def set_value(self, key, value):  # 进阶方法,待研究
    # if(isinstance(value,dict)):
    #     value = json.dumps(value)  # json.dumps()用于将dict类型的数据转成str loads是将str转化成dict格式
    # self.map[key] = value

# def set(self, **keys):  # 进阶方法,待研究
    # try:
    #     for key_, value_ in keys.items():
    #         self.map[key_] = str(value_)
    #         log.debug(key_+":"+str(value_))
    # except BaseException as msg:
    #     log.error(msg)
    #     raise msg

# def get(self, *args):  # 进阶方法,待研究
    # try:
    #     dic = {}
    #     for key in args:
    #         if len(args) == 1:
    #             dic = self.map[key]
    #             log.debug(key+":"+str(dic))
    #         elif len(args) == 1 and args[0] == 'all':
    #             dic = self.map
    #         else:
    #             dic[key] = self.map[key]
    #     return dic
    # except KeyError:
    #     log.warning("key:'" + str(key) + "'  不存在")
    #     return 'Null_'
