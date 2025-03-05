import pandas as pd
import duckdb

df = pd.read_csv("D:\\Private\\fission\\stock_market_data.text")
df["下一天开盘"] = df["开盘"].shift(-1)
df["下一天收盘"] = df["收盘"].shift(-1)
df["下一天最高"] = df["最高"].shift(-1)
df["下一天最低"] = df["最低"].shift(-1)
df["下一天成交量"] = df["成交量"].shift(-1)

df = df.sort_values(by=['股票代码','日期'])
df["下一天涨跌幅"] = ( df["下一天收盘"] - df['收盘'] ) * 100 / df['收盘']
df['涨跌幅'] = df['下一天涨跌幅'].shift(1)

df['下一天最大涨跌幅'] = (df['下一天最高'] - df['收盘']) * 100 / df['收盘']
df['下一天最小涨跌幅'] = (df['下一天最低'] - df['收盘']) * 100 / df['收盘']
df['下一天成交量变化幅度'] = (df['下一天成交量'] - df['成交量']) * 100 / df['成交量']

df.to_csv("D:\\Private\\fission\\dwd_stock_market_data.text", index=False, header=True, sep=",", encoding="utf-8")
