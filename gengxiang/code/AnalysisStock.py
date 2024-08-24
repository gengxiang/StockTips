import time

# 今天日期
from gengxiang.code.Wechat import send_wechat

todayStr = time.strftime('%Y-%m-%d', time.localtime(time.time()))


def get_total(basic_list):
    total_price = 0
    total_amo = 0
    total_hs = 0
    for per in basic_list:
        total_price = total_price + per['price']
        total_amo = total_amo + per['amo']
        total_hs = total_hs + per['hs']
    return total_price, total_amo, total_hs


def get_analysis_info(basic_list, ma_min, ma_max):
    llen = len(basic_list)
    if llen < 5:
        return None
    stop_times = 0
    for history in basic_list:
        if history['stop_price'] == history['price'] or (history['stop_price'] <= 0.0 and history['amp'] > 9.8):
            stop_times = stop_times + 1

    tuple_min0 = get_total(basic_list[0: ma_min + 0])
    tuple_max0 = get_total(basic_list[0: ma_max + 0])
    tuple_min1 = get_total(basic_list[1: ma_min + 1])
    tuple_max1 = get_total(basic_list[1: ma_max + 1])
    tuple_min2 = get_total(basic_list[2: ma_min + 2])
    tuple_max2 = get_total(basic_list[2: ma_max + 2])
    tuple_min3 = get_total(basic_list[3: ma_min + 3])
    tuple_max3 = get_total(basic_list[3: ma_max + 3])
    tuple_min4 = get_total(basic_list[4: ma_min + 4])
    tuple_max4 = get_total(basic_list[4: ma_max + 4])

    analysis_info = {
        'date': basic_list[0]['date'],
        'code': basic_list[0]['code'],
        'name': basic_list[0]['name'],
        'times': stop_times,
        'today_stop': basic_list[0]['stop_price'] == basic_list[0]['price'],
        'hs': basic_list[0]['hs'],
        'ahs': round(tuple_max0[2] / ma_max, 2),
        'price': basic_list[0]['price'],
        'aprice-0': [round(tuple_min0[0] / ma_min, 2), round(tuple_max0[0] / ma_max, 2)],
        'aprice-1': [round(tuple_min1[0] / ma_min, 2), round(tuple_max1[0] / ma_max, 2)],
        'aprice-2': [round(tuple_min2[0] / ma_min, 2), round(tuple_max2[0] / ma_max, 2)],
        'aprice-3': [round(tuple_min3[0] / ma_min, 2), round(tuple_max3[0] / ma_max, 2)],
        'aprice-4': [round(tuple_min4[0] / ma_min, 2), round(tuple_max4[0] / ma_max, 2)],
        'amo': round(basic_list[0]['amo'] / 10000, 2),
        'aamo-0': [round(tuple_min0[1] / ma_min / 10000, 2), round(tuple_max0[1] / ma_max / 10000, 2)],
        'aamo-1': [round(tuple_min1[1] / ma_min / 10000, 2), round(tuple_max1[1] / ma_max / 10000, 2)],
        'aamo-2': [round(tuple_min2[1] / ma_min / 10000, 2), round(tuple_max2[1] / ma_max / 10000, 2)],
        'aamo-3': [round(tuple_min3[1] / ma_min / 10000, 2), round(tuple_max3[1] / ma_max / 10000, 2)],
        'aamo-4': [round(tuple_min4[1] / ma_min / 10000, 2), round(tuple_max4[1] / ma_max / 10000, 2)],
        'amp': basic_list[0]['amp'],
        'mc': basic_list[0]['mc'],
        'per': basic_list[0]['per'],
        'pb': basic_list[0]['pb']
    }
    return analysis_info


def analysis_stop_time(analysis_info):
    if 'ST' in analysis_info['name']:
        return
    if analysis_info['today_stop'] and analysis_info['times'] > 1:
        return analysis_info


def analysis(analysis_info, ma_min, ma_max):
    if analysis_info is None:
        return

    if analysis_info['code'] != 'sh000001' and analysis_info['code'] != 'sz399001':
        # 非ST 非银行 非地产
        if 'ST' in analysis_info['name'] or '银行' in analysis_info['name'] or '证券' in analysis_info[
            'name'] or '地产' in analysis_info['name']:
            return
        # 未涨停
        elif analysis_info['times'] < 1 or analysis_info['amp'] > 9.8:
            return
        # 市净率
        elif analysis_info['per'] < 0 or analysis_info['per'] > 100:
            return
        # 平均换手率小于1.5 或大于8 ,平均成交额小于5000w, ma_min < ma_max
        elif analysis_info['ahs'] < 1.9 or analysis_info['hs'] > 8 or analysis_info['aamo-0'][1] < 0.5 or \
                analysis_info['aprice-0'][0] < analysis_info['aprice-0'][1]:
            return

    aa_price = round((analysis_info['aprice-0'][1] + analysis_info['aprice-1'][1] + analysis_info['aprice-2'][1] +
                      analysis_info['aprice-3'][1] + analysis_info['aprice-4'][1]) / 5, 2)
    aat_volume = round((analysis_info['aamo-0'][1] + analysis_info['aamo-1'][1] + analysis_info['aamo-2'][1] +
                        analysis_info['aamo-3'][1] + analysis_info['aamo-4'][1]) / 5, 2)

    print(analysis_info['date'], "---->", analysis_info['name'], analysis_info['code'])
    print("今天的收盘价:%9s" % analysis_info['price'], "MA", ma_min, ":%9s" % analysis_info['aprice-0'][0], "MA",
          ma_max, ":%9s" % analysis_info['aprice-0'][1])
    print("今天的交易额:%9s" % analysis_info['amo'], "MA", ma_min, ":%9s" % analysis_info['aamo-0'][0], "MA", ma_max,
          ":%9s" % analysis_info['aamo-0'][1])
    print("成交额高于MA", ma_min, ":", analysis_info['amo'] >= analysis_info['aamo-0'][0], "成交额高于MA", ma_max, ":",
          analysis_info['amo'] >= analysis_info['aamo-0'][1],
          "成交额MA", ma_max, "趋势向上:", analysis_info['aamo-0'][1] >= aat_volume)
    print("收盘价高于MA", ma_min, ":", analysis_info['price'] >= analysis_info['aprice-0'][0], "收盘价高于MA", ma_max,
          ":", analysis_info['price'] >= analysis_info['aprice-0'][1],
          "收盘价MA", ma_max, "趋势向上:", analysis_info['aprice-0'][1] >= aa_price)
    if analysis_info['code'] == 'sh000001' or analysis_info['code'] == 'sz399001':
        send_wechat(analysis_info['date'] + "---->" + analysis_info['name'] + analysis_info['code']
                    + "\n 收盘价: " + str(analysis_info['price'])
                    + "   MA" + str(ma_min) + ": " + str(analysis_info['aprice-0'][0])
                    + "   MA" + str(ma_max) + ": " + str(analysis_info['aprice-0'][1])
                    + "\n 交易额: " + str(analysis_info['amo'])
                    + "   MA" + str(ma_max) + ": " + str(analysis_info['aamo-0'][1])
                    + "\n 价高于MA" + str(ma_min) + ": " + str(analysis_info['price'] >= analysis_info['aprice-0'][0])
                    + " 价高于MA" + str(ma_max) + ": " + str(analysis_info['price'] >= analysis_info['aprice-0'][1])
                    + "\n 额高于MA" + str(ma_min) + ": " + str(analysis_info['amo'] >= analysis_info['aamo-0'][0])
                    + " 额高于MA" + str(ma_max) + ": " + str(analysis_info['amo'] >= analysis_info['aamo-0'][1])
                    + "\n 成交价MA" + str(ma_max) + "趋势向上: " + str(analysis_info['aprice-0'][1] >= aa_price)
                    + "\n 成交额MA" + str(ma_max) + "趋势向上: " + str(analysis_info['aamo-0'][1] >= aat_volume))
    print("========================================================================================")
    if (analysis_info['aamo-0'][1] >= aat_volume) & (analysis_info['aprice-0'][1] >= aa_price) \
            & (analysis_info['amo'] >= analysis_info['aamo-0'][1]) & (
            analysis_info['amo'] <= analysis_info['aamo-0'][0]) \
            & (analysis_info['price'] >= analysis_info['aprice-0'][0]) & (analysis_info['aprice-0'][1] >= aa_price):
        return analysis_info
