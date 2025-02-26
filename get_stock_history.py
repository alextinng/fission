import pandas as pd
import akshare as ak

codes = pd.read_csv("D:\\code.text")
codes.head()


start_date = '20250101'
end_date = '20250225'

header=True

for c in codes['code']:
    print("start get data of {}".format(str(c).zfill(6)))
    data = ak.stock_zh_a_hist(symbol=str(c).zfill(6), period="daily", start_date=start_date, end_date=end_date, adjust="qfq")
    if data.empty == False: 
        # 停牌的股票查不到数据
        column = ['日期', '股票代码', '开盘', '收盘', '最高', '最低', '成交量']
        new_df = data[column]
        if header:
            new_df.to_csv("D:\\data.text", mode='a', index=False, header=True, sep=",", encoding="utf-8")
            header = False
        else:
            new_df.to_csv("D:\\data.text", mode='a', index=False, header=False, sep=",", encoding="utf-8")
