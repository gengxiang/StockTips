import time
import json
import openpyxl
from urllib import request

# 今天日期
today = time.strftime('%Y-%m-%d', time.localtime(time.time()))


# 获取当前行情信息
def get_current(stock_code):
    current = request.urlopen('http://qt.gtimg.cn/q=' + stock_code).read().decode('gbk')
    # print(current)
    cur_arr = str(current).split('~')
    stock = {
        'date': cur_arr[30][0:4] + '-' + cur_arr[30][4:6] + '-' + cur_arr[30][6:8],
        'name': cur_arr[1],
        'code': stock_code,
        'price': float(cur_arr[3]),
        'volume': float(cur_arr[6]),
        't_volume': float(cur_arr[37]),
        'change': float(cur_arr[38])
    }
    return stock


# 获取历史数据
def get_history(stock_code, start_date, end_date):
    history = request.urlopen('https://web.ifzq.gtimg.cn/appstock/app/fqkline/get?param=' + stock_code + ',day,'
                              + start_date + ',' + end_date + ',260,qfq').read().decode('gbk')
    if history.find('"code":0') == -1:
        history = request.urlopen('https://web.ifzq.gtimg.cn/appstock/app/fqkline/get?param=' + stock_code + ',day,'
                                  + start_date + ',' + end_date + ',260,qfq').read().decode('gbk')
    # print(history)
    history_stock = json.loads(history)['data'][stock_code]
    stock_name = history_stock['qt'][stock_code][1]
    result_list = []
    for value in history_stock['day']:
        stock = {
            'date': value[0],
            'name': stock_name,
            'code': stock_code,
            'price': float(value[2]),
            'volume': float(value[5]),
            't_volume': -1,
            'change': -1
        }
        result_list.append(stock)
    return result_list


def get_dict_from_refer(file_name):
    """ 读取xlsx文件，获取xlsx文件中"品牌"、"型号"映射字典
    """
    # 打开Excel表格
    refer_excel = openpyxl.load_workbook(file_name)
    # 获取指定Sheet表单页
    refer_sheet = refer_excel[refer_excel.sheetnames[0]]
    # 创建字典：创建一个以型号为key，以品牌为value的字典
    stock_list = []
    # 行循环：从第二行开始循环，到最后一行截止
    for row in range(2, refer_sheet.max_row + 1):
        # 读取cell单元格中的数据
        stock = {
            'date': str((refer_sheet.cell(row=row, column=1)).value),
            'name': (refer_sheet.cell(row=row, column=2)).value,
            'code': (refer_sheet.cell(row=row, column=3)).value,
            'price': float((refer_sheet.cell(row=row, column=4)).value),
            'volume': float((refer_sheet.cell(row=row, column=5)).value),
            't_volume': float((refer_sheet.cell(row=row, column=6)).value),
            'change': float((refer_sheet.cell(row=row, column=7)).value)
        }
        stock_list.append(stock)
    return stock_list


# 获取基础信息
print(get_current('sh000001'))

excel = openpyxl.load_workbook('E://StockTips//gengxiang//data//sh000001.xlsx')
sheet = excel[excel.sheetnames[0]]
history_list = get_history('sh000001', '2022-09-01', '2022-10-10')
i = 2
for history in history_list:
    sheet.cell(row=i, column=1).value = history['date']
    sheet.cell(row=i, column=2).value = history['name']
    sheet.cell(row=i, column=3).value = history['code']
    sheet.cell(row=i, column=4).value = history['price']
    sheet.cell(row=i, column=5).value = history['volume']
    sheet.cell(row=i, column=6).value = history['t_volume']
    sheet.cell(row=i, column=7).value = history['change']
    i = i + 1
excel.save('E://StockTips//gengxiang//data//sh000001_' + today + '.xlsx')

print(get_dict_from_refer('E://StockTips//gengxiang//data//sh000001_' + today + '.xlsx'))
