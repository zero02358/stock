# coding=utf-8

import MySQLdb
import tushare

try:
    conn= MySQLdb.connect(user='root',passwd='root')  # cennect the database
    cur= conn.cursor()  # get the cur
    cur.execute('create database if not exists Stock')
    conn.select_db('Stock')
    cur.execute('create table if not exists hs300(code varchar(10),weight integer)')
    conn.commit()  # 执行上诉操作
    cur.close()
    conn.close()

except MySQLdb.Error,e: print \
    "Mysql Error %d: %s" % (e.args[0], e.args[1])