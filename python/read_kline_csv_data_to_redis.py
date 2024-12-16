import json
import os
import sys

import pandas as pd
import redis


# 读取CSV文件
if len(sys.argv) > 1:
    data_dir = sys.argv[1]
else:
    data_dir = "data"

if not os.path.exists(data_dir):
    print(f"目录{data_dir}不存在")
    exit()
# 为了确保程序正常运行，K线数据文件格式为：DOGEUSDT-1d-2024-09-04.csv
# 由于现在使用list存储k线数据，为了避免后期排序，同时只不留KLINE_KEEP_COUNT = 50条数据，要先进行排序，一次读取改币种所有数据
# 并且保证原来数据+写入数据不超过KLINE_KEEP_COUNT = 50条
file_list = os.listdir(data_dir)
symbols = [f.split('.')[0] for f in file_list]
for symbol in symbols:
    tmp_file_list = filter(lambda x: x.find(symbol) >= 0, file_list)
    tmp_data = []
    kline_key = ""
    for filename in tmp_file_list:
        if filename.endswith('.csv'):
            csv_file_path = os.path.join(data_dir, filename)
            df = pd.read_csv(csv_file_path)
            interval = csv_file_path.split('/')[-1].split('-')[1]
            # 连接到Redis服务器
            redis_host = 'localhost'
            redis_port = 6380
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
                kline_key = f"k_list:{symbol}:{interval}"
                j_data = json.dumps({'t': open_time_ms, 'o': _open, 'h': high, 'l': low, "c": close})
                # 存储close值到Redis
                tmp_data.append(j_data)

                # 打印存储的信息（可选）
    print(kline_key)
    print(f"Stored {tmp_data} to {kline_key}")
    exit()