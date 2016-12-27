#coding=utf-8

def setting_conver(obj,filter_startswith='__'):
    """将配置文件 k,v 转换为映射
    返回 dict 类型"""
    obj_dict=obj.__dict__
    return {k:obj_dict[k] for k in filter(lambda x:not x.startswith(filter_startswith),obj_dict)}


class Setting(dict):
    pass

