# coding=gbk
import yaml
from wxauto import WeChat


def yaml_load():
    f = open('../resource/conf.yaml')
    data = yaml.load(f.read(), Loader=yaml.FullLoader)
    print(type(data))


yaml_load()


def send_wechat_stock(stop_list):
    # �����˷�����Ϣ
    to = "����"  # Ҫ���͵���
    wx = WeChat()  # ��ȡ��ǰ΢�ſͻ���
    wx.Search(to)  # �����촰��
    wx.SendMsg("������Ϣ��")
    for stop in stop_list:
        wx.SendMsg(stop['code'] + ':' + stop['name'] + " ->" + str(stop['times']))  # ������Ϣ
    print("���ͽ�����")


def send_wechat_bk(select_list):
    # �����˷�����Ϣ
    to = "����"  # Ҫ���͵���
    wx = WeChat()  # ��ȡ��ǰ΢�ſͻ���
    wx.Search(to)  # �����촰��
    wx.SendMsg("�����Ϣ��")
    for stop in select_list:
        wx.SendMsg(stop['code'] + ':' + stop['name'] + " ->" + str(stop['ahs']))  # ������Ϣ
    print("���ͽ�����")