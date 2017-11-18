#coding:utf-8

"""
负责实现获取stock的方法，
获取stockid：
上市时间在2017年以前的，非停盘的
"""
import tushare as ts
import datetime
import log,logging

def issuspension(stockid):
    """
    判断是否停盘
    :param stockid:
    :return:
    """
    # todo

def isdateok(date):
    """
    判断上市时间是否在规则内，date格式
    :param stockid:
    :return:
    """
    # todo


def getstockid():
    """
    获取所有满足条件的股票代码，目的是搜索到一个股票列表，持久化到文本中，便于后续使用
    条件1 2017年以前上市的
    条件2 市盈率低于100
    条件3 市值低于500亿（可选）
    条件4 非停盘股票

    获取后存入文本
    :return:
    """
    # todo，实现各个条件后获得代码列表：stocklist
    stocklist = ["600000","600001"]
    stockfile = "stockcode.csv"
    for id in stocklist:
        with open(stockfile,'w+') as f:
            for id in stocklist:
                f.write(str(id) + ",")
                logging.debug("write id %s" % str(id))

if __name__ == '__main__':
    getstockid()