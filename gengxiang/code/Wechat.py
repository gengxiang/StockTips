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


def send_wechat_tips(total_amo, review_url):
    cha_value1 = total_amo[0] - total_amo[1]
    cha_value2 = total_amo[1] - total_amo[0]
    if total_amo[0] >= total_amo[1]:
        msg = todayStr + "\n" + "两市成交额：" + str(total_amo[0] / 10000) + "亿\n" + "放量：" + str(
            cha_value1 / 10000) + "亿\n" + "最大仓位：" + str(calc_reasonable_position(total_amo)) + "层\n" + "他来了!抓紧机会！"
        send_wechat(msg)
    if total_amo[0] < total_amo[1]:
        msg = todayStr + "\n" + "两市成交额：" + str(total_amo[0] / 10000) + "亿\n" + "缩量量：" + str(
            cha_value2 / 10000) + "亿\n" + "最大仓位：" + str(calc_reasonable_position(total_amo)) + "层\n" + "有内鬼！注意风险！"
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
    today_amo = total_amo[0]
    avg_amo_5 = total_amo[2]
    avg_amo_16 = total_amo[3]
    avg_amo_30 = total_amo[4]
    max_position = 10

    # 防止除零
    ratio_5 = today_amo / avg_amo_5 if avg_amo_5 > 0 else 1
    ratio_16 = today_amo / avg_amo_16 if avg_amo_16 > 0 else 1
    ratio_30 = today_amo / avg_amo_30 if avg_amo_30 > 0 else 1

    # 仓位分布优化：加权平均
    weighted_ratio = (0.3 * ratio_5 + 0.3 * ratio_16 + 0.4 * ratio_30)

    # 分段提升灵敏度
    if today_amo > avg_amo_5 and today_amo > avg_amo_16 and today_amo > avg_amo_30:
        position = max_position
    elif weighted_ratio >= 1.2:
        position = int(max_position * 0.8)
    elif weighted_ratio >= 1.0:
        position = int(max_position * 0.6)
    elif weighted_ratio >= 0.8:
        position = int(max_position * 0.4)
    else:
        position = int(max_position * 0.2)

    # 限定仓位范围
    position = max(1, min(max_position, position))
    return position


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
    if len(stop_list) > 2:
        msg = "搞短线！！！ \n"

    if len(stop_list) < 3:
        msg = "弃短线！！！ \n"

    msg = msg + todayStr + "涨停个股信息："
    for stop in stop_list:
        info = get_mysql(stop['code'])
        msg = msg + "\n " + " - " + stop['code'] + ' [ ' + str(stop['times']) + ' / ' + str(
            stop['limit_times']) + ' ] : #' + \
              stop['name']
        if info is not None:
            msg = msg + "\n " + info[4]
    send_wechat(msg)

    if len(select_list) == 0:
        return
    # msg2 = todayStr + "趋势个股信息："
    # for select in select_list:
    #     info = get_mysql(select['code'])
    #     msg2 = msg2 + "\n " + str(select['times']) + " -> " + select['code'] + ' : #' + select['name']
    #     if info is not None:
    #         msg2 = msg2 + "\n " + info[2] + "\n " + info[4]
    # send_wechat(msg2)


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
    for stop in select:
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
