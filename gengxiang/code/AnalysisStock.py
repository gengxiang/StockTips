import time

# 今天日期

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


def get_avg(basic_list):
    total_price = 0
    total_amo = 0
    total_hs = 0
    for per in basic_list:
        total_price = total_price + per['price']
        total_amo = total_amo + per['amo']
        total_hs = total_hs + per['hs']
    avg_price = round(total_price / len(basic_list), 2)
    avg_amo = round(total_amo / len(basic_list), 2)
    avg_hs = round(total_hs / len(basic_list), 2)
    return avg_price, avg_amo, avg_hs


def get_analysis_info(basic_list, ma_min, ma_max):
    llen = len(basic_list)
    if llen < 5:
        return None
    stop_times = 0
    max_prices = 0
    for history in basic_list:
        if history['stop_price'] == history['price'] or (history['stop_price'] <= 0.0 and history['amp'] > 9.8):
            stop_times = stop_times + 1
        if history['price'] > max_prices:
            max_prices = history['price']

    # 价格、金额、换手的平均值 MA7，MA16
    # 最近5天 MA16平均价格、平均金额、平均换手
    max_avg0 = get_avg(basic_list[0: ma_max + 0])
    max_avg1 = get_avg(basic_list[1: ma_max + 1])
    max_avg2 = get_avg(basic_list[2: ma_max + 2])
    max_avg3 = get_avg(basic_list[3: ma_max + 3])
    max_avg4 = get_avg(basic_list[4: ma_max + 4])
    # 最近5天 MA7 平均价格、平均金额、平均换手
    min_avg0 = get_avg(basic_list[0: ma_min + 0])
    min_avg1 = get_avg(basic_list[1: ma_min + 1])
    min_avg2 = get_avg(basic_list[2: ma_min + 2])
    min_avg3 = get_avg(basic_list[3: ma_min + 3])
    min_avg4 = get_avg(basic_list[4: ma_min + 4])

    analysis_info = {
        'date': basic_list[0]['date'],
        'code': basic_list[0]['code'],
        'name': basic_list[0]['name'],
        'times': stop_times,
        'max_prices': max_prices,
        'today_stop': basic_list[0]['stop_price'] == basic_list[0]['price'],
        'hs': basic_list[0]['hs'],
        'ahs': max_avg0[2],
        'price': basic_list[0]['price'],
        # 近5日价格 MA7,, MA16
        'aprice-0': [min_avg0[0], max_avg0[0]],
        'aprice-1': [min_avg1[0], max_avg1[0]],
        'aprice-2': [min_avg2[0], max_avg2[0]],
        'aprice-3': [min_avg3[0], max_avg3[0]],
        'aprice-4': [min_avg4[0], max_avg4[0]],
        # 近5日成交额 MA7,, MA16
        'aamo-0': [min_avg0[1], max_avg0[1]],
        'aamo-1': [min_avg1[1], max_avg1[1]],
        'aamo-2': [min_avg2[1], max_avg2[1]],
        'aamo-3': [min_avg3[1], max_avg3[1]],
        'aamo-4': [min_avg4[1], max_avg4[1]],
        # 近5日成交额
        'amo': round(basic_list[0]['amo'] / 10000, 2),
        'amo-1': round(basic_list[1]['amo'] / 10000, 2),
        'amo-2': round(basic_list[2]['amo'] / 10000, 2),
        'amo-3': round(basic_list[3]['amo'] / 10000, 2),
        'amo-4': round(basic_list[4]['amo'] / 10000, 2),
        # 20日内涨跌幅
        'amp': round((max_prices - basic_list[0]['price']) / max_prices, 2),
        # 总市值
        'mc': basic_list[0]['mc'],
        # 市盈率
        'per': basic_list[0]['per'],
        # 市净率
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
        elif analysis_info['times'] < 1 or analysis_info['amp'] > 0.25:
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

    aa_volume = round((analysis_info['aamo-0'][1] + analysis_info['aamo-1'][1] + analysis_info['aamo-2'][1] +
                       analysis_info['aamo-3'][1] + analysis_info['aamo-4'][1]) / 5, 2)
    t_volume = round((analysis_info['amo'] + analysis_info['amo-1'] + analysis_info['amo-2'] + analysis_info['amo-3'] +
                      analysis_info['amo-4']) / 5, 2)

    if (t_volume > aa_volume) & (analysis_info['aamo-0'][1] >= aa_volume) & (
            analysis_info['aamo-0'][1] > analysis_info['aamo-1'][1]):
        return analysis_info

    # if (analysis_info['aamo-0'][1] >= aa_volume) \
    #         & (analysis_info['aprice-0'][1] >= aa_price) \
    #         & (analysis_info['amo'] >= analysis_info['aamo-0'][1]) \
    #         & (analysis_info['amo'] <= analysis_info['aamo-0'][0]) \
    #         & (analysis_info['price'] >= analysis_info['aprice-0'][0]) \
    #         & (analysis_info['aprice-0'][1] >= aa_price):
    #     return analysis_info
