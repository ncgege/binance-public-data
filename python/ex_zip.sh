#!/bin/bash

# 检查参数数量
if [ "$#" -lt 2 ]; then
    # 提示用户输入源目录
    echo -n "请输入要解压的目录: "
    read source_dir

    # 检查源目录是否存在
    if [ ! -d "$source_dir" ]; then
        echo "源目录不存在，请重新运行脚本并提供有效的目录。"
        exit 1
    fi

    # 提示用户输入目标目录
    echo -n "请输入解压到的目录: "
    read desc_dir

    # 检查目标目录是否存在，如果不存在则创建
    if [ ! -d "$desc_dir" ]; then
        echo "目标目录不存在，正在创建..."
        mkdir -p "$desc_dir"
        if [ $? -ne 0 ]; then
            echo "无法创建目标目录，请检查权限。"
            exit 1
        fi
    fi
else
    # 从命令行参数获取源目录和目标目录
    source_dir=$1
    desc_dir=$2

    # 检查源目录是否存在
    if [ ! -d "$source_dir" ]; then
        echo "源目录不存在，请提供有效的目录。"
        exit 1
    fi
fi

# 在这里可以继续添加你的解压逻辑，例如使用unzip、tar等命令
echo "开始解压 $source_dir 到 $desc_dir..."

# 示例解压命令（根据你的实际情况修改）
unzip "$source_dir/*.zip" -d "$desc_dir"
# tar -xvf "$source_dir/*.tar.gz" -C "$desc_dir"
echo "所有文件解压完成！"