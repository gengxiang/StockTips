# coding=utf-8
# 这段代码能找到你真正的Python路径
import sys

# 打印你正在使用的Python路径
print("你当前运行代码的 Python 路径：")
print(sys.executable)

# 自动生成安装命令
print("\n如果还是报错，请复制下面这行命令去终端运行：")
print(f'"{sys.executable}" -m pip install pandas==1.4.2 numpy==1.21.6')
