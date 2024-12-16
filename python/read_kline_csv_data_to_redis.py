import json
import os
import sys

import pandas as pd
import redis
from settings import KLINE_KEEP_COUNT


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
symbols = [f.split('-')[0] for f in file_list]
symbols = list(set(symbols))
redis_host = 'localhost'
redis_port = 6380
redis_db = 0
r = redis.StrictRedis(host=redis_host, port=redis_port, db=redis_db, decode_responses=True)
r2 = redis.StrictRedis(host=redis_host, port=6379, db=redis_db, decode_responses=True)
total = len(symbols)
cur_count = 0
for symbol in symbols:
    tmp_file_list = [f for f in file_list if f.find(symbol) >= 0]
    interval = tmp_file_list[-1].split('-')[1]
    # 构造Redis键名
    kline_key = f"k_list:{symbol}:{interval}"
    cur_kline_list = r.lrange(kline_key, 0, -1)
    cur_kline_list = [json.loads(kd) for kd in cur_kline_list]
    cur_timestamp_list = [t.get('t') for t in cur_kline_list]
    min_timestamp = min(cur_timestamp_list)
    read_data = []
    for filename in tmp_file_list:
        if filename.endswith('.csv'):
            csv_file_path = os.path.join(data_dir, filename)
            df = pd.read_csv(csv_file_path)
            # 连接到Redis服务器

            # 遍历DataFrame并存储数据到Redis
            for index, row in df.iterrows():
                open_time = row['open_time']
                # 将open_time转换为毫秒时间戳（假设原始数据是秒时间戳）
                open_time_ms = int(float(open_time))
                close = float(row['close'])
                _open = float(row['open'])
                high = float(row['high'])
                low = float(row['low'])
                if open_time_ms < min_timestamp:
                    j_data = {'t': open_time_ms, 'o': _open, 'h': high, 'l': low, "c": close}
                    # 存储close值到Redis
                    read_data.append(j_data)

                # 打印存储的信息（可选）
    print(f"当前键：{kline_key}， 数据最小时间戳：{min_timestamp}")
    read_data = sorted(read_data, key=lambda x: x['t'], reverse=True)
    if len(read_data) + len(cur_kline_list) >= KLINE_KEEP_COUNT:
        read_data = read_data[:KLINE_KEEP_COUNT - len(cur_kline_list)]

    read_data = [json.dumps(td) for td in read_data]
    cur_count += 1
    print(f"完成进度{cur_count}/{total}.")
    if read_data:
        r2.lpush(kline_key, *read_data)
        print(f"数据写入{kline_key}完成")
