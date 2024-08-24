# coding=gbk
import time

import yaml
from wxauto import *

from gengxiang.code.getAll import get_mysql

wx = WeChat()  # ��ȡ��ǰ΢�ſͻ���
who = "G.X"  # Ҫ���͵���
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
        msg = todayStr + "\n" + "���гɽ��" + str(total_amo / 10000) + "��\n" + "���ڹ�ֹͣ���ף�"
        send_wechat(msg)
    if 70000000 <= total_amo <= 75000000:
        msg = todayStr + "\n" + "���гɽ��" + str(total_amo / 10000) + "��\n" + "���ս��! !׼��������"
        send_wechat(msg)
    if 75000000 < total_amo:
        msg = todayStr + "\n" + "���гɽ��" + str(total_amo / 10000) + "��\n" + "������!ץ�����ᣡ"
        send_wechat(msg)


def send_wechat_stock(stop_list, select_list):
    msg = todayStr + "��ͣ������Ϣ��"
    for stop in stop_list:
        info = get_mysql(stop['name'])
        msg = msg + "\n" + str(stop['times']) + " - " + stop['code'] + ' : ' + stop['name'] + \
              "\n " + info[2] + "\n " + info[4] + "\n =================="
    send_wechat(msg)

    if len(select_list) == 0:
        return
    msg2 = todayStr + "���Ƹ�����Ϣ��"
    for select in select_list:
        info = get_mysql(stop['name'])
        msg2 = msg2 + "\n" + str(select['times']) + " -> " + select['code'] + ' : ' + select['name'] + \
               "\n " + info[2] + "\n " + info[4] + "\n =================="
    send_wechat(msg2)


def send_wechat_bk(select_list):
    if len(select_list) == 0:
        return
    wx.ChatWith(who)
    msg = todayStr + "�����Ϣ��"
    for stop in select_list:
        msg = msg + "\n" + stop['code'] + ':' + stop['name'] + " ->" + str(stop['ahs'])
    send_wechat(msg)
    print("���ͽ�����")

# stock_list = []
# ak = {
#     'code': 'sh600187',
#     'name': '����ˮ��',
#     'times': 8
# }
# stock_list.append(ak)
# send_wechat_stock(stock_list, None)
