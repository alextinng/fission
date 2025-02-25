import requests
import json
import re
import pandas as pd
import sys


# 请求的URL
url = "https://push2ex.eastmoney.com/getTopicZTPool?cb=callbackdata7401790&ut=7eea3edcaed734bea9cbfc24409ed989&dpt=wz.ztzt&Pageindex=0&pagesize=170&sort=fbt%3Aasc&date=20250225&_=1740485445738"

# 请求头
headers = {
    "Accept": "*/*",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "Connection": "keep-alive",
    "Cookie": "HAList=ty-1-688316-%u9752%u4E91%u79D1%u6280-U; qgqp_b_id=f70986967149bbef4e715da199108eda; fullscreengg=1; fullscreengg2=1; websitepoptg_api_time=1740484998815; st_si=50616904875236; st_asi=delete; st_pvi=11933472320548; st_sp=2024-12-21%2009%3A33%3A30; st_inirUrl=https%3A%2F%2Fwww.bing.com%2F; st_sn=8; st_psi=20250225201045826-113200304537-7725154704",
    "Referer": "https://quote.eastmoney.com/ztb/detail",
    "Sec-Fetch-Dest": "script",
    "Sec-Fetch-Mode": "no-cors",
    "Sec-Fetch-Site": "same-site",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 Edg/132.0.0.0",
    "sec-ch-ua": '"Not A(Brand";v="8", "Chromium";v="132", "Microsoft Edge";v="132"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"'
}

# 发送请求
response = requests.get(url, headers=headers)

# 检查请求是否成功
if response.status_code == 200:
    # 去掉回调函数部分，提取JSON数据
    json_data = re.search(r"callbackdata7401790\((.*)\);", response.text).group(1)
    data = json.loads(json_data)

    # print(data)
    df = pd.DataFrame(data['data']['pool'])
    
    df.rename(columns={
        "c": "股票代码",
        "n": "股票名称",
        "zdp": "涨跌幅度",
        "amount": "成交额"
    }, inplace=True)
    df["日期"] = pd.Timestamp.today().normalize()

    columns_to_keep = ["股票代码", "股票名称","涨跌幅度","成交额","日期"]
    new_df = df[columns_to_keep]

    # print(new_df)
    new_df.to_csv(sys.stdout, index=False, header=True, sep=",", encoding="utf-8")

else:
    print(f"请求失败，状态码：{response.status_code}")
