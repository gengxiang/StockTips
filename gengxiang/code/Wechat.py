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


def send_wechat_tips(total_amo):
    if 70000000 > total_amo:
        msg = todayStr + "\n" + "两市成交额：" + str(total_amo / 10000) + "亿\n" + "有内鬼！停止交易！"
        send_wechat(msg)
    if 70000000 <= total_amo <= 75000000:
        msg = todayStr + "\n" + "两市成交额：" + str(total_amo / 10000) + "亿\n" + "风险解除! !准备出击！"
        send_wechat(msg)
    if 75000000 < total_amo:
        msg = todayStr + "\n" + "两市成交额：" + str(total_amo / 10000) + "亿\n" + "他来了!抓紧机会！"
        send_wechat(msg)


def send_wechat_stock(stop_list, select_list):
    msg = todayStr + "涨停个股信息："
    for stop in stop_list:
        info = get_mysql(stop['name'])
        msg = msg + "\n" + str(stop['times']) + " - " + stop['code'] + ' : ' + stop['name'] + \
              "\n " + info[2] + "\n " + info[4] + "\n =================="
    send_wechat(msg)

    if len(select_list) == 0:
        return
    msg2 = todayStr + "趋势个股信息："
    for select in select_list:
        info = get_mysql(stop['name'])
        msg2 = msg2 + "\n" + str(select['times']) + " -> " + select['code'] + ' : ' + select['name'] + \
               "\n " + info[2] + "\n " + info[4] + "\n =================="
    send_wechat(msg2)


def send_wechat_bk(select_list):
    if len(select_list) == 0:
        return
    wx.ChatWith(who)
    msg = todayStr + "板块信息："
    for stop in select_list:
        msg = msg + "\n" + stop['code'] + ':' + stop['name'] + " ->" + str(stop['ahs'])
    send_wechat(msg)
    print("发送结束！")

# stock_list = []
# ak = {
#     'code': 'sh600187',
#     'name': '国中水务',
#     'times': 8
# }
# stock_list.append(ak)
# send_wechat_stock(stock_list, None)
