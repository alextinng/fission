import pandas as pd
import duckdb

df = pd.read_csv("D:\\data.text")
df.head(5)

# 创建一个 DuckDB 连接
conn = duckdb.connect(database=':memory:')  # 使用内存数据库，也可以指定文件路径
# 将 Pandas DataFrame 注册为虚拟表
conn.register('stock_history', df)

# 使用 SQL 查询 DataFrame
# 日期,股票代码,开盘,收盘,最高,最低,成交量
result = conn.execute("""
    COPY (
    WITH price_data AS (
    SELECT
        "日期",
        "股票代码",
        "开盘",
        "收盘",
        "最高",
        "最低",
        "成交量",
        -- 当日涨跌幅计算
        ("收盘" - LAG("收盘") OVER (PARTITION BY "股票代码" ORDER BY "日期")) / LAG("收盘") OVER (PARTITION BY "股票代码" ORDER BY "日期") AS daily_return,
        -- 下一日收盘价
        LEAD("收盘") OVER (PARTITION BY "股票代码" ORDER BY "日期") AS next_day_close_price
    FROM
        stock_history
)
SELECT
    "股票代码",
    "日期",
    "开盘",
    "收盘",
    "最高",
    "最低",
    "成交量",
    daily_return * 100 as "涨跌幅",
    -- 下一日涨跌幅计算
    (next_day_close_price - "收盘") * 100 / "收盘" AS "第二天帐跌幅"
FROM
    price_data
ORDER BY
    "股票代码",
    "日期"
    ) TO 'D:\\stock_history.text' (FORMAT 'csv', HEADER TRUE, DELIMITER ',')
""")

stock_analysis_table_csv = pd.read_csv("D:\\table.text")
conn.register('stock_analysis', stock_analysis_table_csv)
result = conn.execute("""
select "日期","股票代码","涨跌幅","第二天涨跌幅" from stock_analysis where "涨跌幅" > 8 limit 50;
"""
).df()

result.head(100)
