#!/usr/bin/python
# coding=utf-8
from sqlalchemy import create_engine
import tushare as ts
import time
import os
import MySQLdb

def print_log(log_content):
    print 5*'-' + log_content

class DataStore:
    HOST = '127.0.0.1'
    database = "stockinfo"
    username = 'root'
    password = 'root'
    # 非第一次运行标志
    flag = "runflag"
    sql_engin = ""

    all_stock_info = ts.get_stock_basics()

    def __init__(self):
        """
        创建数据库引擎
        """
        # self.sql_engin = create_engine(self.get_sql_url())

        self.crate_database()

    def crate_database(self):
        conn = MySQLdb.connect(host = self.HOST,port = 3306,
            user = self.username,passwd = self.password)

        # cennect the database
        cur = conn.cursor()  # get the cur
        cur.execute('create database if not exists ' + self.database)
        conn.select_db(self.database)
        cur.close()
        conn.close()
        print_log('create database end')

    def get_sql_url(self):
        """
        获取mysql的链接
        :return:
        """
        mysql_url = 'mysql://' + self.username + ':' + \
                    self.password + '@' +self.HOST + '/' + self.database + '?charset=utf8'
        return mysql_url

    @staticmethod
    def get_today_date():
        """
        获取今天的日期，格式指定'%Y-%m-%d'
        :return:
        """
        today_date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        return today_date

    @staticmethod
    def get_years_before_today_date():
        """
        获取若干年前的今天，用于提供获取时间段的股票数据
        :return:
        """
        oneYear = 365 * 24 * 3600
        # 指定时间间隔是10年
        number = 10
        temp = time.strftime('%Y-%m-%d', time.localtime(time.time() - oneYear*number))
        return temp

    def create_run_flag(self):
        """
        创建非第一次运行标志
        :return:
        """
        os.mkdir(self.flag)
        pass

    def is_first_run(self):
        """
        如果文件存在则非第一次运行
        :return:
        """
        if os.path.exists(self.flag):
            return False
        else:
            return True

    def get_stock_ids(self):
        """
        获取需要的股票id，这里主要排除新股、ST股票
        :return: 股票id列表
        """
        stock_ids = []
        for stockid in self.all_stock_info.index:
            stockname = self.all_stock_info.ix[stockid]['name'].decode('utf-8')
            # 如果是ST或者新股，不在处理范围
            if stockname.find("ST") >= 0 or stockname.find("N") >= 0:
                pass
            else:
                stock_ids.append(stockid)
        return stock_ids

    def create_init_data(self):
        """
        数据初始化,
        :return:
        """
        enddate = self.get_today_date()
        # 十年前的今天
        startdate = self.get_years_before_today_date()

        try:
            conn = MySQLdb.connect(host=self.HOST, port=3306,
                                   user=self.username, passwd=self.password)
            # cennect the database
            cur = conn.cursor()  # get the cur
            conn.select_db(self.database)
            for stockid in self.get_stock_ids():
                # 根据股票id创建一个表;stockid_6000000,如果直接为数字，创建表失败，数据库语法错误
                initsql = 'CREATE TABLE IF NOT EXISTS stockid_'+ stockid +'(open FLOAT,high FLOAT,' \
                          'close FLOAT,low FLOAT,volume FLOAT,p_change FLOAT,ma5 FLOAT,' \
                          'ma10 FLOAT,ma20 FLOAT,v_ma5 FLOAT,v_ma10 FLOAT,v_ma20 FLOAT,' \
                          'turnover FLOAT)'
                cur.execute(initsql)
                conn.commit()

                # 获取该股票的历史数据
                stockinfo = ts.get_hist_data(stockid, startdate, enddate)
                for date in stockinfo.index: # 索引就是时间
                    print_log('start write stockinfo for id ' + stockid)
                    stockDayInfo = stockinfo.ix[date]
                    """
                    >>> info = ts.get_hist_data("600000","2012-12-12","2014-12-12")
                    >>> info.ix['2013-11-26']
                    open                  9.900
                    high                 10.030
                    close                 9.900
                    low                   9.880
                    volume           728576.880
                    price_change         -0.030
                    p_change             -0.300
                    ma5                  10.002
                    ma10                  9.889
                    ma20                 10.044
                    v_ma5           1198138.050
                    v_ma10          1517251.630
                    v_ma20          1540624.400
                    turnover              0.490
                    Name: 2013-11-26, dtype: float64
                    """
                    # 为每个参数赋值
                    (
                        stock_open,
                        stock_high,
                        stock_close,
                        stock_low,
                        stock_volume,
                        stock_price_change,
                        stock_p_change,
                        stock_ma5,
                        stock_ma10,
                        stock_ma20,
                        stock_v_ma5,
                        stock_v_ma10,
                        stock_v_ma20,
                        stock_turnover
                    ) = stockDayInfo

                    insertdata = 'INSERT INTO stockid_' + stockid + ' (open,high,close,' \
                              'low,volume,p_change,ma5,ma10,ma20,v_ma5,v_ma10,' \
                              'v_ma20,turnover) VALUES ' \
                                '(%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f)' % \
                            (
                                float(stock_open),
                                float(stock_high),
                                float(stock_close),
                                float(stock_low),
                                float(stock_volume),
                                float(stock_p_change),
                                float(stock_ma5),
                                float(stock_ma10),
                                float(stock_ma20),
                                float(stock_v_ma5),
                                float(stock_v_ma10),
                                float(stock_v_ma10),
                                float(stock_turnover)
                            )

                    cur.execute(insertdata)
                    conn.commit()
                    print_log(insertdata + 10*"-" + "successfully")
            cur.close()
            conn.close()

        except MySQLdb.Error, e:
            print_log("Mysql Error %d: %s" % (e.args[0], e.args[1]))

    def append_new_data(self):
        """
        追加今日数据
        :return:
        """
        # 遍历所有股票，以id为索引
        for stockid in self.all_stock_info.index:
            stockname = self.all_stock_info.ix[stockid]['name'].decode('utf-8')
            # 如果是ST或者新股，不在处理范围
            if stockname.find("ST") >= 0 or stockname.find("N") >= 0:
                pass
            else:
                today = self.get_today_date()
                stockinfo = ts.get_tick_data(stockid, date=today)
                try:
                    stockinfo.to_sql(stockid, self.sql_engin, if_exists='append')
                except:
                    print_log("Error huppend, append stock info failed.")

    def run(self):
        """
        第一次执行则初始化
        非首次执行则追加数据
        :return:
        """
        if self.is_first_run :
            self.create_init_data()
            self.create_run_flag()
        else:
            pass
            # self.append_new_data()


if __name__ == '__main__':
    # todo 待填入run方法
    dts = DataStore()
    dts.run()
"""
tmp = ts.get_today_all()
tmp.to_sql('today_all', engine)"""
# # 存  入数据库
# df.to_sql('tick_data',engine)
# all_stock_info.to_sql('stockinfo', engine)