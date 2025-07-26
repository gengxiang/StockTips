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
    big_times = 0
    today_big = False
    stop_times = 0
    max_prices = 0
    min_prices = basic_list[0]['price']
    limit_stop_times = 0

    for i in range(0, llen):
        if basic_list[i - 1]['code'] == "sh600117":
            print(basic_list[i - 1])
        if basic_list[i]['stop_price'] != basic_list[i]['price']:
            break
        else:
            limit_stop_times += 1

    for i in range(0, llen):
        print(basic_list[i - 1])
        if basic_list[i]['amo'] != 0 and basic_list[i - 1]['amo'] != 0:
            if (i > 0) and (basic_list[i - 1]['amo'] / basic_list[i]['amo'] > 1.5) and (basic_list[i]['amp'] > 0):
                big_times += 1
                if i <= 1:
                    today_big = True
        history = basic_list[i]
        if history['stop_price'] == history['price'] or (history['stop_price'] <= 0.0 and history['amp'] > 9.8):
            stop_times = stop_times + 1
        if history['price'] > max_prices:
            max_prices = history['price']
        if history['price'] < min_prices:
            min_prices = history['price']

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
        'price': basic_list[0]['price'],
        'stop_price': basic_list[0]['stop_price'],
        'b_stop_price': round(basic_list[0]['stop_price'] * 0.9 / 1.1, 2),
        # 今日是否涨停
        'today_stop': basic_list[0]['stop_price'] == basic_list[0]['price'],
        # 今日是否倍量
        'today_big': today_big,
        # 区间涨停次数
        'times': stop_times,
        # 连续涨停次数
        'limit_times': limit_stop_times,
        # 增量大于1.5
        'amo_times': big_times,
        # 16日平均换手
        'ahs': max_avg0[2],
        # 近5天 MA7 价格 成交额 换手
        'MA7-0': [min_avg0[0], min_avg0[1], min_avg0[2]],
        'MA7-1': [min_avg1[0], min_avg1[1], min_avg1[2]],
        'MA7-2': [min_avg2[0], min_avg2[1], min_avg2[2]],
        'MA7-3': [min_avg3[0], min_avg3[1], min_avg3[2]],
        'MA7-4': [min_avg4[0], min_avg4[1], min_avg4[2]],
        # 近5天 MA16 价格 成交额 换手
        'MA16-0': [max_avg0[0], max_avg0[1], max_avg0[2]],
        'MA16-1': [max_avg1[0], max_avg1[1], max_avg1[2]],
        'MA16-2': [max_avg2[0], max_avg2[1], max_avg2[2]],
        'MA16-3': [max_avg3[0], max_avg3[1], max_avg3[2]],
        'MA16-4': [max_avg4[0], max_avg4[1], max_avg4[2]],
        # 近5天  价格 成交额 换手
        'price_arr': [basic_list[0]['price'], basic_list[1]['price'], basic_list[2]['price'], basic_list[3]['price'],
                      basic_list[4]['price']],
        'amo_arr': [basic_list[0]['amo'], basic_list[1]['amo'], basic_list[2]['amo'], basic_list[3]['amo'],
                    basic_list[4]['amo'],
                    basic_list[5]['amo'], basic_list[6]['amo'], basic_list[7]['amo'], basic_list[8]['amo'],
                    basic_list[9]['amo']],
        'hs_arr': [basic_list[0]['hs'], basic_list[1]['hs'], basic_list[2]['hs'], basic_list[3]['hs'],
                   basic_list[4]['hs']],
        'max_prices': max_prices,
        'min_prices': min_prices,
        # 涨跌幅
        'amp': basic_list[0]['amp'],
        # 总市值
        'mc': basic_list[0]['mc'],
        # 市盈率
        'per': basic_list[0]['per'],
        # 市净率
        'pb': basic_list[0]['pb'],
        # 换手
        'hs': basic_list[0]['hs'],
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
        'amo-4': round(basic_list[4]['amo'] / 10000, 2)
    }
    return analysis_info


def analysis_stop_time(analysis_info):
    if 'ST' in analysis_info['name']:
        return
    if analysis_info['today_stop'] and analysis_info['times'] > 1:
        return analysis_info


# 近日有涨停，当天倍量，阳线，ma5小于10 %，ma16向上


def analysis(analysis_info, ma_min, ma_max):
    if analysis_info is None:
        return

    if analysis_info['code'] != 'sh000001' and analysis_info['code'] != 'sz399001':
        # 非ST 非银行 非地产
        if 'ST' in analysis_info['name'] or '银行' in analysis_info['name'] or '证券' in analysis_info[
            'name'] or '地产' in analysis_info['name']:
            return
        # 未涨停
        elif analysis_info['times'] < 1 or analysis_info['amp'] < 0:
            return
        elif analysis_info['today_big'] is False:
            return
        # 市净率
        elif analysis_info['per'] < 0 or analysis_info['per'] > 100:
            return
        # 平均换手率小于1.5 或大于8 ,平均成交额小于5000w
        elif analysis_info['ahs'] < 1.5 or analysis_info['hs'] > 8 or analysis_info['aamo-0'][1] < 0.5:
            return

        elif analysis_info['price_arr'][0] > (analysis_info['MA16-0'][0] * 1.1) or analysis_info['price_arr'][0] < \
                analysis_info['MA16-0'][0]:
            return

        return analysis_info

    # if (t_volume > aa_volume) & (analysis_info['aamo-0'][1] >= aa_volume) & (
    #         analysis_info['aamo-0'][1] > analysis_info['aamo-1'][1]):
    #     return analysis_info
    # 当日成交额MA7大于5天前的1.5倍

    # ma7 = analysis_info['MA7-0'][2] / analysis_info['MA7-4'][2] > 1.5
    # # 近三天amo平均值 与前两天amo的比率
    # amo = (3 * (analysis_info['amo_arr'][0] + analysis_info['amo_arr'][1] + analysis_info['amo_arr'][3]) / 2 * (
    #         analysis_info['amo_arr'][4] + analysis_info['amo_arr'][5])) > 1.5
    # price = analysis_info['price_arr'][0] > analysis_info['MA16-0'][1] & analysis_info['MA7-0'][0] > \
    #         analysis_info['MA7-0'][4]
    # if ma7 & amo & price:
    #     return analysis_info
