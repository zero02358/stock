# coding=utf-8
import tushare as ts
from sqlalchemy import create_engine
tm = ts.get_hist_data('600000',start="2000-12-12",end="2016-12-12")
count=1
for i in tm.ix.date:
    tm.ix.id = count
    count = count + 1
print tm
HOST = '127.0.0.1'
database = "stock"
username = 'root'
password = 'root'
# 非第一次运行标志
flag = "runflag"

mysql_url = 'mysql://' + username + ':' + \
                    password + '@' +HOST + '/' + database + '?charset=utf8'
engin = create_engine(mysql_url)


tm.to_sql("600000",engin)