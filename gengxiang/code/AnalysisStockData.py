import time

import GetAndSaveStockData

# 今天日期
todayStr = time.strftime('%Y-%m-%d', time.localtime(time.time()))


def get_analysis_info(basic_list):
    """
    跟进近20日交易数据
    获取16日平均价格&平均成交额
    获取前4天16日平均价格&平均成交额
    :rtype: object
    """
    total_price = 0
    total_t_volume = 0
    for history in basic_list:
        total_price = total_price + history['price']
        total_t_volume = total_t_volume + history['t_volume']

    p1 = total_price - basic_list[19]['price'] - basic_list[18]['price'] - basic_list[17]['price'] - basic_list[16][
        'price']
    p2 = total_price - basic_list[19]['price'] - basic_list[18]['price'] - basic_list[17]['price'] - basic_list[0][
        'price']
    p3 = total_price - basic_list[19]['price'] - basic_list[18]['price'] - basic_list[0]['price'] - basic_list[1][
        'price']
    p4 = total_price - basic_list[19]['price'] - basic_list[0]['price'] - basic_list[1]['price'] - basic_list[2][
        'price']
    p5 = total_price - basic_list[0]['price'] - basic_list[1]['price'] - basic_list[2]['price'] - basic_list[3]['price']
    # print(round(p5 / 16), "->", round(p4 / 16), "->", round(p3 / 16), "->", round(p2 / 16), "->", round(p1 / 16))

    t1 = total_t_volume - basic_list[19]['t_volume'] - basic_list[18]['t_volume'] - basic_list[17]['t_volume'] - \
         basic_list[16]['t_volume']
    t2 = total_t_volume - basic_list[19]['t_volume'] - basic_list[18]['t_volume'] - basic_list[17]['t_volume'] - \
         basic_list[0]['t_volume']
    t3 = total_t_volume - basic_list[19]['t_volume'] - basic_list[18]['t_volume'] - basic_list[0]['t_volume'] - \
         basic_list[1]['t_volume']
    t4 = total_t_volume - basic_list[19]['t_volume'] - basic_list[0]['t_volume'] - basic_list[1]['t_volume'] - \
         basic_list[2]['t_volume']
    t5 = total_t_volume - basic_list[0]['t_volume'] - basic_list[1]['t_volume'] - basic_list[2]['t_volume'] - \
         basic_list[3]['t_volume']
    # print(round(t5 / 16), "->", round(t4 / 16), "->", round(t3 / 16), "->", round(t2 / 16), "->", round(t1 / 16))

    analysis_info = {
        'date': basic_list[0]['t_date'],
        'code': basic_list[0]['code'],
        'name': basic_list[0]['name'],
        'price': basic_list[0]['price'],
        'a_price': round(p1 / 16, 2),
        'a_price_1': round(p2 / 16, 2),
        'a_price_2': round(p3 / 16, 2),
        'a_price_3': round(p4 / 16, 2),
        'a_price_4': round(p5 / 16, 2),
        't_volume': round(basic_list[0]['t_volume'] / 10000, 2),
        'at_volume': round(t1 / 160000, 2),
        'at_volume_1': round(t2 / 160000, 2),
        'at_volume_2': round(t3 / 160000, 2),
        'at_volume_3': round(t4 / 160000, 2),
        'at_volume_4': round(t5 / 160000, 2)
    }

    return analysis_info


def analysis(analysis_info):
    aa_price = round((analysis_info['a_price'] + analysis_info['a_price_1'] + analysis_info['a_price_2'] +
                      analysis_info['a_price_3'] + analysis_info['a_price_4']) / 5, 2)
    aat_volume = round((analysis_info['at_volume'] + analysis_info['at_volume_1'] + analysis_info['at_volume_2'] +
                        analysis_info['at_volume_3'] + analysis_info['at_volume_4']) / 5, 2)
    print(analysis_info['date'], "---->", analysis_info['name'], analysis_info['code'])
    print("今天的收盘价:", analysis_info['price'], "MA16:", analysis_info['a_price'])
    print("今天的交易额:", analysis_info['t_volume'], "MA16:", analysis_info['at_volume'])
    print("成交额高于MA16", analysis_info['t_volume'] > analysis_info['at_volume'],
          "成交额MA16趋势向上:", analysis_info['at_volume'] > aat_volume)
    print("收盘价高于MA16", analysis_info['price'] > analysis_info['a_price'],
          "收盘价MA16趋势向上:", analysis_info['a_price'] > aa_price)


# history_list = GetAndSaveStockData.get_mysql('sh000001')
# print(history_list)
history_list = GetAndSaveStockData.get_excel('E://StockTips//gengxiang//data//sh000001.xlsx')
print(history_list)
info = get_analysis_info(history_list)
analysis(info)
