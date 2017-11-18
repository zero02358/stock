# -*- coding:utf-8 -*-
# 获取各个行业最近十天涨幅最大的股票
import tushare as ts
stock_info = ts.get_stock_basics()

# 取得所有的行业
all_industry = []
all_stock_industry = []
for xx in range(len(stock_info)):
    all_industry.append(stock_info.industry[xx])
    all_stock_industry.append([stock_info.index[xx], stock_info.industry[xx]])

# 删除行业list中的重复数据
all_industry = list(set(all_industry))
# 去除创业板
buy_stock_id = [x for x in stock_info.index if not x.startswith('300')]

# 开始计算
strongest_stock_id = ''
strongest_stock_percent = 0
for i in range(len(all_industry)):
    for j in range(len(all_stock_industry)):
        if all_stock_industry[j][1] == all_industry[i] and buy_stock_id.count(all_stock_industry[j][0]) > 0:
            # 获取涨幅最大的股票
            df = ts.get_hist_data(all_stock_industry[j][0])
            if not df is None and df.close.count() > 260:  # 去除上市时间不到一年的股票
                close_todaylist = df.close.head(10)[0]
                close_10daylists_ago = df.close.head(10)[9]
                percentage_10daylists = (
                    close_todaylist - close_10daylists_ago) / close_10daylists_ago

                if percentage_10daylists > strongest_stock_percent:
                    strongest_stock_id = all_stock_industry[j][0]
                    strongest_stock_percent = percentage_10daylists
                else:
                    pass
            else:
                pass
        else:
            pass
    print 'the strongest stock in', all_industry[i], 'is:', strongest_stock_id
    strongest_stock_id = ''
    strongest_stock_percent = 0
