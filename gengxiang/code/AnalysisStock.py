import time

import pandas as pd

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


def ema_tal(series, n=2):
    k = 2 / (n + 1)
    ema = series.copy()
    for i in range(1, len(ema)):
        ema[i] = series[i] * k + ema[i - 1] * (1 - k)
    return ema


def get_analysis_info(basic_list, ma_min, ma_max):
    llen = len(basic_list)
    if llen < 5:
        return None
    basic_list = sorted(basic_list, key=lambda x: x['date'], reverse=True)
    big_times = 0
    today_big = False
    stop_times = 0
    max_prices = 0
    min_prices = basic_list[0]['price']
    limit_stop_times = 0

    for i in range(0, llen):
        if basic_list[i]['stop_price'] != basic_list[i]['price']:
            break
        else:
            limit_stop_times += 1

    for i in range(0, llen):
        # print(basic_list[i - 1])
        if basic_list[i]['amo'] != 0 and basic_list[i - 1]['amo'] != 0:
            if (i > 0) and (basic_list[i - 1]['amo'] / basic_list[i]['amo'] > 1.35) and (basic_list[i]['amp'] > 0):
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

    # 最近5天 MA3 平均价格、平均金额、平均换手
    three_avg0 = get_avg(basic_list[0: 3 + 0])
    three_avg1 = get_avg(basic_list[1: 3 + 1])
    three_avg2 = get_avg(basic_list[2: 3 + 2])
    three_avg3 = get_avg(basic_list[3: 3 + 3])
    three_avg4 = get_avg(basic_list[4: 3 + 4])

    analysis_info = {
        'date': basic_list[0]['date'],
        'code': basic_list[0]['code'],
        'name': basic_list[0]['name'],
        'price': basic_list[0]['price'],
        # 今日涨停价格
        'stop_price': basic_list[0]['stop_price'],
        # 今日跌停价格
        'b_stop_price': round(basic_list[0]['stop_price'] * 0.9 / 1.1, 2),
        # 今日是否涨停
        'today_stop': basic_list[0]['stop_price'] == basic_list[0]['price'],
        # 今日是否倍量(成交额大于上一日1.5倍)
        'today_big': today_big,
        # 区间涨停次数
        'times': stop_times,
        # 连续涨停次数
        'limit_times': limit_stop_times,
        # 成交额倍量的次数
        'amo_times': big_times,
        # 16日平均换手
        'ahs': max_avg0[2],
        # 近5天 MA3 价格 成交额 换手
        'MA3-0': [three_avg0[0], three_avg0[1], three_avg0[2]],
        'MA3-1': [three_avg1[0], three_avg1[1], three_avg1[2]],
        'MA3-2': [three_avg2[0], three_avg2[1], three_avg2[2]],
        'MA3-3': [three_avg3[0], three_avg3[1], three_avg3[2]],
        'MA3-4': [three_avg4[0], three_avg4[1], three_avg4[2]],
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

    # print(analysis_info, "zhuli : " + calculate_indicator(analysis_info['price'], analysis_info['aprice-0'][0]))

    return analysis_info


def calculate_5day_indicator(analysis_info):
    """
    主力:=EMA( (CLOSE-MA(CLOSE,7))/MA(CLOSE,7)*480,2)*5,colorcyan;
    散户:=EMA( (CLOSE-MA(CLOSE,11))/MA(CLOSE,11)*480,7)*5,colorred;
    合:= MA(主力*1.95+散户*1.45,2);
    XC:= 合 - REF(合,1);
    DRAWTEXT(COND AND 主力 < 200 AND (主力 - REF(主力,1)) > 50 ,LOW*0.95,'加'),colorwhite;
    DRAWTEXT(COND AND CROSS(主力,散户) AND 主力 < 300, LOW*0.92,'买'),colorwhite;
    DRAWICON(HIGH>MA4 AND MA4 > REF(MA4,1) AND XC>0 AND (合+0.85*REF(合,2))>1.85*REF(合,1),LOW*0.89,1);

    从 analysis_info 中提取近5天价格 + MA7，计算近5天指标：
    EMA( (CLOSE-MA7)/MA7*480, 2 )
    返回：近5天指标数组 [最新, 1日前, 2日前, 3日前, 4日前]
    """
    # 1. 提取近5天收盘价（最新 → 5日前）
    price_arr = analysis_info['price_arr']  # [今日, 1日, 2日, 3日, 4日]

    # 2. 提取近5天 MA7 价格
    ma7_arr = [
        analysis_info['MA7-0'][0],  # 今日 MA7
        analysis_info['MA7-1'][0],  # 1日前 MA7
        analysis_info['MA7-2'][0],  # 2日前 MA7
        analysis_info['MA7-3'][0],  # 3日前 MA7
        analysis_info['MA7-4'][0]  # 4日前 MA7
    ]

    # 3. 转成 pandas 序列计算
    # c = pd.Series(price_arr[::-1])
    # m = pd.Series(ma7_arr[::-1])
    c = pd.Series(price_arr[::-1]).reset_index(drop=True)
    m = pd.Series(ma7_arr[::-1]).reset_index(drop=True)

    # 1. 计算中间值
    # 2. 同花顺公式：(C-MA)/MA*480
    x = (c - m) / m * 480

    ema2 = ema_tal(x, 2)  # 标准算法
    result = ema2 * 5

    final = result[::-1].reset_index(drop=True).round(2)

    return final


def analysis_stop_time(analysis_info):
    if 'ST' in analysis_info['name']:
        return
    if analysis_info['today_stop'] and analysis_info['times'] > 1:
        return analysis_info


# 近日有涨停，当天倍量，阳线，ma5小于10 %，ma16向上


def check_strong_start(indicator):
    """
    纯净版：连续2天暴涨（无EMA、无平滑）
    数据顺序：[今天, 昨天, 前天, 大前天, 更早]
    核心条件：
    1. 当天指标  < 200
    2. 今天 - 昨天 >= 50
    3. 昨天 - 前天 >= 50
    """
    # 数据至少要有 今天、昨天、前天 3 个
    if len(indicator) < 3:
        return False

    # 直接取原始数据（不用反转！）
    today = indicator[0]  # 今天
    yesterday = indicator[1]  # 昨天
    b_yesterday = indicator[2]  # 前天
    bb_yesterday = indicator[3]  # 大前天

    # 计算每日涨幅
    diff1 = today - yesterday  # 今日涨幅
    diff2 = yesterday - b_yesterday  # 昨日涨幅
    diff3 = b_yesterday - bb_yesterday  # 前日涨幅

    # ===================== 你的全部条件 =====================
    cond1 = today < 300  # 1. 当天 < 200
    cond2 = diff1 >= 50  # 2. 今天-昨天 >=50
    cond3 = diff2 >= 50  # 3. 昨天-前天 >=50
    cond4 = diff3 >= 50  # 4. 前天-大前天 >=50

    # 5. 单日涨幅不能超过 100（任何一天都不行）
    no_overflow = (diff1 <= 200) and (diff2 <= 200) and (diff3 <= 200)

    # 最终组合条件
    return cond1 and cond2 and (cond3 or cond4) and no_overflow


def analyze_trend_final(indicator):
    """
    终极版：5日指标趋势分析（EMA平滑 + 强势启动捕捉）
    数据格式：[今天, 昨天, 前天, 大前天, 更早]
    核心：找 【刚刚从低位开始强势上涨】 的信号
    """
    # ========== 1. 数据整理 ==========
    arr = indicator[::-1]  # 反转成正序：更早→大前天→前天→昨天→今天

    # days = ["更早", "大前天", "前天", "昨天", "今天"]

    # ========== 2. EMA2 平滑（消除毛刺，更准确） ==========
    def ema2(series):
        if len(series) < 1:
            return series
        res = [series[0]]
        for v in series[1:]:
            res.append(round(v * 2 / 3 + res[-1] * 1 / 3, 2))
        return res

    smooth = ema2(arr)

    # ========== 3. 计算平滑后每日涨跌幅 + 强弱标记 ==========
    changes = []
    trend_text = []
    for i in range(1, len(smooth)):
        prev_val = smooth[i - 1]
        curr_val = smooth[i]
        diff = round(curr_val - prev_val, 2)
        changes.append(diff)

        if diff > 40:
            trend_text.append("强势上涨(>40)")
        elif diff < -40:
            trend_text.append("快速下降(< -40)")
        elif diff > 0:
            trend_text.append("上涨")
        elif diff < 0:
            trend_text.append("下跌")
        else:
            trend_text.append("持平")

    # ========== 4. 核心判断条件 ==========
    today_s = smooth[-1]
    yes_s = smooth[-2]
    bef_s = smooth[-3]

    today_diff = round(today_s - yes_s, 2)
    yes_diff = round(yes_s - bef_s, 2)

    # 关键规则
    is_weak_zone = today_s < -30  # 弱势区
    # has_strong_rise = any(c > 40 for c in changes)  # 旧代码：有一次就行
    strong_rise_count = sum(1 for c in changes if c > 50)  # 统计 >50 的次数
    has_strong_rise = strong_rise_count >= 1  # 🔥 新要求：2次及以上暴涨

    # ======================
    # 新增：近三天平均 > -20
    # ======================
    recent_3_avg = (today_s + yes_s + bef_s) / 3
    is_recent_strong = recent_3_avg > -10  # 平均大于-20才算合格

    # 【刚刚开始强势上涨】核心条件
    is_just_start_strong = (
            has_strong_rise
            and today_diff > 0
            and yes_s < 0
            and today_s > yes_s
            and (today_diff > 20 or yes_diff > 20)
            and is_recent_strong
    )

    return is_just_start_strong


def analysis(analysis_info, ma_min, ma_max):
    if analysis_info is None:
        return

    # 你的 analysis_info 已经存在时，直接调用：
    indicator = calculate_5day_indicator(analysis_info)
    analysis_info['indicator'] = indicator.tolist()
    # final_condition = analyze_trend_final(indicator)
    final_condition = check_strong_start(indicator)

    if 'ST' in analysis_info['name'] or '银行' in analysis_info['name'] or '证券' in analysis_info['name'] or '地产' in \
            analysis_info['name']:
        return
    # 7. 股价偏离均线过滤（核心技术面）
    # 条件1：当前价格 > 16日均线的1.2倍 → 涨幅过大，超买，剔除
    # 条件2：当前价格×1.15 仍小于16日均线 → 股价太弱，严重低于均线，剔除
    elif analysis_info['price_arr'][0] > (analysis_info['MA16-0'][0] * 1.2) or (analysis_info['price_arr'][0] * 1.15) < \
            analysis_info['MA16-0'][0]:
        return

    # 8. 趋势 + 量能过滤
    # 条件1：3日均线 < 16日均线×1.2 → 短期趋势不强，剔除
    # 条件2：今日成交额 < 16日均线价格 → 量能不足，剔除
    elif analysis_info['MA3-0'][0] * 1.1 < (analysis_info['MA16-0'][0]) or (analysis_info['amo_arr'][0]) * 1.1 < \
            analysis_info['MA16-0'][0]:
        return

    # 平均换手率小于1.5,平均成交额小于5000w
    elif analysis_info['ahs'] < 1.5 or analysis_info['aamo-0'][1] < 0.5:
        return

    elif final_condition:
        print(analysis_info['name'], '5日指标：', indicator.tolist())
        print("=" * 70)
        return analysis_info

    return

    #
    # if analysis_info['code'] != 'sh000001' and analysis_info['code'] != 'sz399001':
    #
    #     # 非ST 非银行 非地产
    #     if 'ST' in analysis_info['name'] or '银行' in analysis_info['name'] or '证券' in analysis_info['name'] or '地产' in analysis_info['name']:
    #         return
    #     # 未涨停
    #     elif analysis_info['times'] < 1 or analysis_info['amp'] < 0:
    #         return
    #     elif analysis_info['today_big'] is False:
    #         return
    #     elif analysis_info['today_stop'] is True:
    #         return
    #     # 市净率
    #     elif analysis_info['per'] < 0 or analysis_info['per'] > 100:
    #         return
    #     # 平均换手率小于1.5,平均成交额小于5000w
    #     elif analysis_info['ahs'] < 1.5 or analysis_info['aamo-0'][1] < 0.5:
    #         return
    #
    #     # 7. 股价偏离均线过滤（核心技术面）
    #     # 条件1：当前价格 > 16日均线的1.2倍 → 涨幅过大，超买，剔除
    #     # 条件2：当前价格×1.1 仍小于16日均线 → 股价太弱，严重低于均线，剔除
    #     elif analysis_info['price_arr'][0] > (analysis_info['MA16-0'][0] * 1.2) or (analysis_info['price_arr'][0] * 1.1) < analysis_info['MA16-0'][0]:
    #         return
    #
    #     # 8. 趋势 + 量能过滤
    #     # 条件1：3日均线 < 16日均线×1.2 → 短期趋势不强，剔除
    #     # 条件2：今日成交额 < 16日均线价格 → 量能不足，剔除
    #     elif analysis_info['MA3-0'][0] * 1.1 < (analysis_info['MA16-0'][0]) or (analysis_info['amo_arr'][0])*1.1 < analysis_info['MA16-0'][0]:
    #         return
    #
    #
    #     return analysis_info

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
