# coding=gbk
import yaml
from wxauto import WeChat


def yaml_load():
    f = open('../resource/conf.yaml')
    data = yaml.load(f.read(), Loader=yaml.FullLoader)
    print(type(data))


yaml_load()


def send_wechat_stock(stop_list):
    # 给单人发送消息
    to = "耿翔"  # 要发送的人
    wx = WeChat()  # 获取当前微信客户端
    wx.Search(to)  # 打开聊天窗口
    wx.SendMsg("个股信息：")
    for stop in stop_list:
        wx.SendMsg(stop['code'] + ':' + stop['name'] + " ->" + str(stop['times']))  # 发送消息
    print("发送结束！")


def send_wechat_bk(select_list):
    # 给单人发送消息
    to = "耿翔"  # 要发送的人
    wx = WeChat()  # 获取当前微信客户端
    wx.Search(to)  # 打开聊天窗口
    wx.SendMsg("板块信息：")
    for stop in select_list:
        wx.SendMsg(stop['code'] + ':' + stop['name'] + " ->" + str(stop['ahs']))  # 发送消息
    print("发送结束！")
