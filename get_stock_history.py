import pandas as pd
import akshare as ak

import requests
import pandas as pd
url = "https://raw.githubusercontent.com/alextinng/fission/refs/heads/master/code.text"

# 下载文件并保存到本地
response = requests.get(url)
response.raise_for_status()  # 确保请求成功

# 将文件内容保存到本地
file_path = "data.csv"
with open(file_path, "w", encoding="utf-8") as file:
    file.write(response.text)

# 使用 pandas 读取本地文件
codes = pd.read_csv(file_path)
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
