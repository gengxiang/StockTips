# coding=gbk
import time

import yaml
from wxauto import *

from gengxiang.code.getAll import get_mysql

wx = WeChat()  # 获取当前微信客户端
who = "G.X"  # 要发送的人
todayStr = time.strftime('%Y-%m-%d', time.localtime(time.time()))


def yaml_load():
    f = open('../resource/conf.yaml')
    data = yaml.load(f.read(), Loader=yaml.FullLoader)
    print(type(data))


def send_wechat(msg):
    WxUtils.SetClipboard(msg)
    wx.ChatWith(who)
    wx.SendClipboard(who)
    # wx.ChatWith(who)
    # wx.SendMsg(msg, who)


def send_wechat_thsbks(thsBsk_list):
    if len(thsBsk_list) == 0:
        return
    wx.ChatWith(who)
    msg = todayStr + "同花顺板块信息："
    for bsk in thsBsk_list:
        msg = msg + "\n " + '#' + bsk['行业名称'] + "  +>领涨股: '#'" + str(
            bsk['领涨股']) + " ->净流入资金(亿): " + str(bsk['净流入资金(亿)'])
    send_wechat(msg)
    print("发送结束！")


def send_wechat_bks(bsk_list):
    if len(bsk_list) == 0:
        return
    wx.ChatWith(who)
    msg = todayStr + "东方财富板块信息："
    for bsk in bsk_list:
        msg = msg + "\n " + '#' + bsk['name'] + " ->" + str(bsk['板块列表'])
    send_wechat(msg)
    print("发送结束！")


def send_wechat_tips(total_amo, review_url):
    dot = calc_reasonable_position(total_amo)
    cha_value1 = total_amo[0] - total_amo[1]
    cha_value2 = total_amo[1] - total_amo[0]
    if total_amo[0] >= total_amo[1]:
        msg = todayStr + "\n" + "两市成交额：" + str(total_amo[0] / 10000) + "亿\n" + "放量：" + str(
            cha_value1 / 10000) + "亿\n" \
              + "操作建议：" + dot[2]["操作建议"] + "\n" + "最大仓位：" + dot[2]["建议仓位区间"]
        send_wechat(msg)
    if total_amo[0] < total_amo[1]:
        msg = todayStr + "\n" + "两市成交额：" + str(total_amo[0] / 10000) + "亿\n" + "缩量量：" + str(
            cha_value2 / 10000) + "亿\n" \
              + "操作建议：" + dot[2]["操作建议"] + "\n" + "最大仓位：" + str(dot[2]["建议仓位区间"])
        send_wechat(msg)

    focus = "近5日焦点复盘地址：\n"
    i = 0
    for review in review_url:
        i += 1
        if i < 5:
            focus = focus + review + " \n"
    send_wechat(focus)


def calc_reasonable_position(total_amo):
    """
    优化仓位分布：结合今日成交额与各均值的比值，分段提升灵敏度
    :param total_amo: [今日成交额, 昨日成交额, 5日均值, 16日均值, 30日均值]
    :return: 仓位层数（int, 1~8）
    """

    price_result = volume_based_position_analysis(total_amo[5], total_amo[6], total_amo[7], total_amo[8])
    print(price_result)
    volume_result = volume_based_position_analysis(total_amo[0], total_amo[1], total_amo[2], total_amo[3])
    print(volume_result)

    # 取出两个维度的综合评分
    price_score = price_result["综合评分"]
    volume_score = volume_result["综合评分"]

    # ======================
    # 最终综合评分（价格40% + 量能60%，最科学的权重）
    # ======================
    final_score = round(price_score * 0.4 + volume_score * 0.6, 1)

    # ======================
    # 最终仓位等级
    # ======================
    if final_score >= 90:
        final_level = "重仓"
        final_position = "80%~100%"
    elif final_score >= 70:
        final_level = "中高仓"
        final_position = "60%~80%"
    elif final_score >= 50:
        final_level = "中等仓"
        final_position = "40%~60%"
    elif final_score >= 30:
        final_level = "轻仓"
        final_position = "20%~40%"
    else:
        final_level = "空仓/观望"
        final_position = "0%~20%"

    # ======================
    # 操作信号（双维度共振判断）
    # ======================
    if price_score >= 50 and volume_score >= 50:
        operation = "买入/持有信号（价量共振走强）,想想赚钱的感觉！"
    elif price_score >= 50 and volume_score < 50:
        operation = "观望信号（价强量弱，谨慎）"
    elif price_score < 50 and volume_score >= 50:
        operation = "观望信号（量强价弱，反弹减仓）"
    else:
        operation = "卖出/空仓信号（价量双弱）, 想想亏钱的日子！"

    # ======================
    # 最终返回结果
    # ======================
    return price_result, volume_result, {
        "最终综合评分": final_score,
        "最终仓位等级": final_level,
        "建议仓位区间": final_position,
        "操作建议": operation,
        "价格评分": price_score,
        "成交量评分": volume_score,
        "价格维度详情": price_result,
        "成交量维度详情": volume_result
    }


def volume_based_position_analysis(today_volume, yesterday_volume, ma5, ma16):
    # 数据校验（已删除 ma30）
    if any(not isinstance(v, (int, float)) or v <= 0 for v in [today_volume, yesterday_volume, ma5, ma16]):
        return {"error": "所有输入必须为大于0的数字"}

    # ---------------------
    # 1. 短期动能评分（不变）
    # ---------------------
    day_growth = (today_volume - yesterday_volume) / yesterday_volume
    vs_ma5_ratio = today_volume / ma5
    short_score = 50 + (day_growth * 150) + ((vs_ma5_ratio - 1) * 120)
    short_score = max(0, min(100, short_score))

    # ---------------------
    # 2. 中期趋势评分（已删除 ma30）
    # ---------------------
    ma_trend = 0
    if ma5 > ma16:
        ma_trend = 1
    elif ma5 < ma16:
        ma_trend = -1

    # 原基于ma30 → 替换为 ma16（最合理等价替换）
    vol_strength = max(-30, min(30, (today_volume / ma16 - 1) * 100))
    mid_score = 50 + (ma_trend * 25) + vol_strength
    mid_score = max(0, min(100, mid_score))

    # ---------------------
    # 3. 市场热度评分（已删除 ma30）
    # ---------------------
    health_ratio = ma5 / ma16
    heat_score = 50 + ((health_ratio - 1) * 80) + ((today_volume / ma16 - 1) * 40)
    heat_score = max(0, min(100, heat_score))

    # ---------------------
    # 4. 综合评分（不变）
    # ---------------------
    total = short_score * 0.40 + mid_score * 0.35 + heat_score * 0.25
    total = round(total, 2)

    # ---------------------
    # 5. 仓位建议（不变）
    # ---------------------
    if total >= 80:
        level = "重仓"
        pos = 80 + (total - 80) / 20 * 20
    elif total >= 60:
        level = "中高仓"
        pos = 60 + (total - 60) / 20 * 20
    elif total >= 40:
        level = "中等仓"
        pos = 40 + (total - 40) / 20 * 20
    elif total >= 20:
        level = "轻仓"
        pos = 20 + (total - 20) / 20 * 20
    else:
        level = "空仓"
        pos = total / 20 * 20

    pos = round(max(0, min(100, pos)), 1)

    # ---------------------
    # 返回结果（已删除 ma30 相关）
    # ---------------------
    return {
        "综合评分": total,
        "仓位等级": level,
        "建议仓位": f"{pos}%",
        "分项评分": {
            "短期动能": round(short_score, 1),
            "中期趋势": round(mid_score, 1),
            "市场热度": round(heat_score, 1),
        },
        "成交量状态": {
            "日环比": f"{day_growth:.1%}",
            "vs5日均": f"{vs_ma5_ratio - 1:.1%}",
            "均线排列": "多头" if ma_trend == 1 else "空头" if ma_trend == -1 else "震荡",
            "量能强度": f"{vol_strength:.1f}分"
        }
    }


def send_wechat_jrj(jrj):
    total_inflow = 0
    msg = str(jrj['td']) + " 大盘云图："
    for jr in jrj['hqs']:
        if float(jr['rval']) < 1000000000:
            continue
        total_inflow += float(jr['rval'])
        msg = msg + "\n #" + jr['name'] + \
              " - 净流入:" + str(round(float(jr['rval']) / 100000000, 2)) + "亿"
    total_inflow_亿 = round(total_inflow / 100000000, 2)
    msg = msg + "\n总净流入金额：" + str(total_inflow_亿) + "亿"
    wx.ChatWith(who)
    send_wechat(msg)


def send_wechat_stock(stop_list, select_list):
    # if len(stop_list) > 2:
    #     msg = "搞短线！！！ \n"
    #
    # if len(stop_list) < 3:
    #     msg = "弃短线！！！ \n"

    msg = todayStr + "涨停个股信息："
    for stop in stop_list:
        info = get_mysql(stop['code'])
        msg = msg + "\n " + " - " + stop['code'] + ' [ ' + str(stop['times']) + ' / ' + str(
            stop['limit_times']) + ' ] : #' + \
              stop['name'] + "\n " + ", ".join(str(x) for x in stop['indicator'])
        if info is not None:
            msg = msg + "\n " + info[4]
    send_wechat(msg)

    if len(select_list) == 0:
        return

    select_list_sorted = sorted(select_list, key=lambda x: (x['amo_times'] + x['times'] + x['limit_times']),
                                reverse=True)[:25]
    select_list_sorted = sorted(select_list_sorted, key=lambda x: (x['MA3-0'][1] / x['MA16-0'][1]), reverse=True)
    msg2 = todayStr + "趋势个股信息："
    for select in select_list_sorted[:15]:
        info = get_mysql(select['code'])
        msg2 = msg2 + "\n " + str(select['times']) + " -> " + select['code'] + ' : #' + select[
            'name'] + "\n " + ", ".join(str(x) for x in select['indicator'])
        if info is not None:
            msg2 = msg2 + "\n " + info[2] + "\n " + info[4]
    send_wechat(msg2)


def send_wechat_bk(select_list):
    if len(select_list) == 0:
        return
    wx.ChatWith(who)
    msg = todayStr + "板块信息："
    for stop in select_list:
        msg = msg + "\n " + stop['code'] + ':#' + stop['name'] + " ->" + str(stop['ahs'])
    send_wechat(msg)
    print("发送结束！")


def send_wechat_ind(select_list, title):
    if len(select_list) == 0:
        return
    wx.ChatWith(who)
    msg = todayStr + " " + title
    i = 0
    for stop in select_list:
        msg = msg + "\n" + stop['industry'] + " ->" + str(stop['stop_times']) \
              + "\n  #" + ',#'.join([item for item in stop['stop_details']])
        i += 1
        if stop['stop_times'] < 4:
            break
        if i >= 8:
            break
        # if i < 5 and i % 8 == 0:
        #     send_wechat(msg)
        #     msg = todayStr + " " + title

    send_wechat(msg)
    print(title + "发送结束！")


def send_wechat_rank(select):
    if len(select) == 0:
        return
    wx.ChatWith(who)
    msg = todayStr + " 今日涨停榜"
    i = 0
    for stop in select[:10]:
        if stop['times'] < 3:
            break
        msg = msg + "\n#" + stop['name'] + " -> " + str(stop['times']) + "\n || " + stop['industry']
        # + "\n || " + '*'.join([item for item in stop['concept']])
        i += 1
        # if i < 5 and i % 9 == 0:
        #     send_wechat(msg)
        #     msg = todayStr + " 今日涨停榜"

    send_wechat(msg)
    print("发送结束！")

# stock = {
#     'code': row[0],
#     'name': row[1],
#     'industry': row[2],
#     'address': row[3],
#     'times': row[5],
#     'concept': row[4].split(',')
# }
# stock_list = []
# ak = {
#     'code': 'sh600187',
#     'name': '国中水务',
#     'times': 8
# }
# stock_list.append(ak)
# send_wechat_stock(stock_list, None)
