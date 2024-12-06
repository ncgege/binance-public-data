import json
import os
import sys

import pandas as pd
import redis


# 读取CSV文件
if len(sys.argv[1]) > 1:
    data_dir = sys.argv[1]
else:
    data_dir = "data"

if not os.path.exists(data_dir):
    print(f"目录{data_dir}不存在")
    exit()
# 为了确保程序正常运行，K线数据文件格式为：DOGEUSDT-1d-2024-09-04.csv

for filename in os.listdir(data_dir):
    if filename.endswith('.csv'):
        csv_file_path = os.path.join(data_dir, filename)
        df = pd.read_csv(csv_file_path)
        symbol = csv_file_path.split('/')[-1].split('-')[0]
        interval = csv_file_path.split('/')[-1].split('-')[1]
        # 连接到Redis服务器
        redis_host = 'localhost'
        redis_port = 6379
        redis_db = 0
        r = redis.StrictRedis(host=redis_host, port=redis_port, db=redis_db, decode_responses=True)

        # 遍历DataFrame并存储数据到Redis
        for index, row in df.iterrows():
            open_time = row['open_time']
            # 将open_time转换为毫秒时间戳（假设原始数据是秒时间戳）
            open_time_ms = int(float(open_time))
            close = float(row['close'])
            _open = float(row['open'])
            high = float(row['high'])
            low = float(row['low'])

            # 构造Redis键名
            redis_key = f"kline_data:{symbol}:{interval}:{open_time_ms}"
            j_data = json.dumps({'t': open_time_ms, 'o': _open, 'h': high, 'l': low, "c": close})
            # 存储close值到Redis
            print(redis_key)
            r.set(redis_key, j_data)
            # 打印存储的信息（可选）
            print(f"Stored {close} to {redis_key}")
