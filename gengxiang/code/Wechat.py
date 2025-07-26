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
            cha_value1 / 10000) + "亿\n" + "他来了!抓紧机会！"
        send_wechat(msg)
    if total_amo[0] < total_amo[1]:
        msg = todayStr + "\n" + "两市成交额：" + str(total_amo[0] / 10000) + "亿\n" + "缩量量：" + str(
            cha_value2 / 10000) + "亿\n" + "有内鬼！注意风险！"
        send_wechat(msg)

    # if 70000000 > total_amo:
    #     msg = todayStr + "\n" + "两市成交额：" + str(total_amo / 10000) + "亿\n" + "有内鬼！停止交易！"
    #     send_wechat(msg)
    # if 70000000 <= total_amo <= 75000000:
    #     msg = todayStr + "\n" + "两市成交额：" + str(total_amo / 10000) + "亿\n" + "风险解除! !准备出击！"
    #     send_wechat(msg)
    # if 75000000 < total_amo:
    #     msg = todayStr + "\n" + "两市成交额：" + str(total_amo / 10000) + "亿\n" + "他来了!抓紧机会！"
    #     send_wechat(msg)

    focus = "近5日焦点复盘地址：\n"
    i = 0
    for review in review_url:
        i += 1
        if i < 5:
            focus = focus + review + " \n"
    send_wechat(focus)


def send_wechat_jrj(jrj):
    msg = str(jrj['td']) + " 大盘云图："
    for jr in jrj['hqs']:
        ## + " - 上涨家数:" + jr['bsp']['unum'] + " - 下跌家数:" + jr['bsp']['dnum']
        # " - 总成交额:" + str(round(jr['esp']['amt'] / 100000000, 2)) + "亿" + \
        if float(jr['rval']) < 1000000000:
            continue
        msg = msg + "\n #" + jr['name'] + \
              " - 净流入:" + str(round(float(jr['rval']) / 100000000, 2)) + "亿"
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
        msg = msg + "\n " + str(stop['times']) + " - " + stop['code'] + ' [ ' + stop['limit_times'] + ' ] : #' + stop[
            'name']
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
        msg = msg + "\n" + stop['industry'] + " ->" + str(stop['stop_times']) + "\n  #" + ',#'.join(
            [item for item in stop['stop_details']])
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
