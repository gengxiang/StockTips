import time

# 今天日期
todayStr = time.strftime('%Y-%m-%d', time.localtime(time.time()))


def get_analysis_info(basic_list, ma, llen):
    """
    跟进近20日交易数据
    获取16日平均价格&平均成交额
    获取前4天16日平均价格&平均成交额
    :rtype: object
    """
    if ma < llen - 4:
        return None

    total_price = 0
    total_t_volume = 0
    total_change = 0
    stop_times = 0
    print(basic_list)
    for history in basic_list:
        total_price = total_price + history['price']
        total_t_volume = total_t_volume + history['amo']
        total_change = total_change + history['hs']
        if history['stop_price'] == history['price'] or (history['stop_price'] == 0.0 and history['amp'] > 9.8):
            stop_times = stop_times + 1

    p1 = total_price - basic_list[llen - 1]['price'] - basic_list[llen - 2]['price'] - basic_list[llen - 3]['price'] - \
         basic_list[llen - 4]['price']
    p2 = total_price - basic_list[llen - 1]['price'] - basic_list[llen - 2]['price'] - basic_list[llen - 3]['price'] - \
         basic_list[llen - ma - 4]['price']
    p3 = total_price - basic_list[llen - 1]['price'] - basic_list[llen - 2]['price'] - basic_list[llen - ma - 4][
        'price'] - basic_list[llen - ma - 3]['price']
    p4 = total_price - basic_list[llen - 1]['price'] - basic_list[llen - ma - 4]['price'] - basic_list[llen - ma - 3][
        'price'] - basic_list[llen - ma - 2]['price']
    p5 = total_price - basic_list[llen - ma - 4]['price'] - basic_list[llen - ma - 3]['price'] - \
         basic_list[llen - ma - 2]['price'] - basic_list[llen - ma - 1]['price']
    t1 = total_t_volume - basic_list[llen - 1]['amo'] - basic_list[llen - 2]['amo'] - basic_list[llen - 3]['amo'] - \
         basic_list[llen - 4]['amo']
    t2 = total_t_volume - basic_list[llen - 1]['amo'] - basic_list[llen - 2]['amo'] - basic_list[llen - 3]['amo'] - \
         basic_list[llen - ma - 4]['amo']
    t3 = total_t_volume - basic_list[llen - 1]['amo'] - basic_list[llen - 2]['amo'] - basic_list[llen - ma - 4]['amo'] - \
         basic_list[llen - ma - 3]['amo']
    t4 = total_t_volume - basic_list[llen - 1]['amo'] - basic_list[llen - ma - 4]['amo'] - basic_list[llen - ma - 3][
        'amo'] - basic_list[llen - ma - 2]['amo']
    t5 = total_t_volume - basic_list[llen - ma - 4]['amo'] - basic_list[llen - ma - 3]['amo'] - \
         basic_list[llen - ma - 2]['amo'] - basic_list[llen - ma - 1]['amo']

    analysis_info = {
        'date': basic_list[0]['date'],
        'code': basic_list[0]['code'],
        'name': basic_list[0]['name'],
        'amp': basic_list[0]['amp'],
        'mc': basic_list[0]['mc'],
        'hs': basic_list[0]['hs'],
        'per': basic_list[0]['per'],
        'pb': basic_list[0]['pb'],
        'price': basic_list[0]['price'],
        'times': stop_times,
        'ahs': round(total_change / len(basic_list), 2),
        'aprice-0': round(p1 / ma, 2),
        'aprice-1': round(p2 / ma, 2),
        'aprice-2': round(p3 / ma, 2),
        'aprice-3': round(p4 / ma, 2),
        'aprice-4': round(p5 / ma, 2),
        'amo': round(basic_list[0]['amo'] / 10000, 2),
        'aamo-0': round(t1 / 10000 / ma, 2),
        'aamo-1': round(t2 / 10000 / ma, 2),
        'aamo-2': round(t3 / 10000 / ma, 2),
        'aamo-3': round(t4 / 10000 / ma, 2),
        'aamo-4': round(t5 / 10000 / ma, 2)
    }
    return analysis_info


def analysis(analysis_info, ma):
    if analysis_info['code'] != 'sh000001' and analysis_info['code'] != 'sz399001':
        # 非ST 非银行 非地产
        if 'ST' in analysis_info['name'] or '银行' in analysis_info['name'] or '地产' in analysis_info['name']:
            return
        # 平均换手率小于1.2 或大于7 ,平均成交额小于5000w
        elif 1.5 > analysis_info['ahs'] or analysis_info['hs'] > 8 or analysis_info['aamo-0'] < 0.5:
            return
        # 未涨停
        elif analysis_info['times'] < 1 or analysis_info['amp'] > 9.8:
            return

    aa_price = round((analysis_info['aprice-0'] + analysis_info['aprice-1'] + analysis_info['aprice-2'] +
                      analysis_info['aprice-3'] + analysis_info['aprice-4']) / 5, 2)
    aat_volume = round((analysis_info['aamo-0'] + analysis_info['aamo-1'] + analysis_info['aamo-2'] +
                        analysis_info['aamo-3'] + analysis_info['aamo-4']) / 5, 2)
    print(analysis_info['date'], "---->", analysis_info['name'], analysis_info['code'])
    print("今天的收盘价:", analysis_info['price'], "MA:", analysis_info['aprice-0'])
    print("今天的交易额:", analysis_info['amo'], "(亿)", "MA:", analysis_info['aamo-0'], "(亿)")
    print("成交额高于MA", ma, ":", analysis_info['amo'] >= analysis_info['aamo-0'],
          "成交额MA", ma, "趋势向上:", analysis_info['aamo-0'] >= aat_volume)
    print("收盘价高于MA", ma, ":", analysis_info['price'] >= analysis_info['aprice-0'],
          "收盘价MA", ma, "趋势向上:", analysis_info['aprice-0'] >= aa_price)
    print("====================================================")
    if (analysis_info['amo'] >= 1.2 * analysis_info['aamo-0']) & (analysis_info['aamo-0'] >= 1.1 * aat_volume) & (
            analysis_info['price'] >= analysis_info['aprice-0']) & (analysis_info['aprice-0'] >= aa_price):
        return analysis_info
