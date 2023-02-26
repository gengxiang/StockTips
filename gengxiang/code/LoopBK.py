# coding=gbk
import json
import time
from urllib import request

import pymysql

all_BK = [
    {
        "f12": "BK1031",
        "f13": 90,
        "f14": "����豸",
        "f62": 2103230496
    },
    {
        "f12": "BK1015",
        "f13": 90,
        "f14": "��Դ����",
        "f62": 1580268288
    },
    {
        "f12": "BK1027",
        "f13": 90,
        "f14": "С����",
        "f62": 1509017136
    },
    {
        "f12": "BK0736",
        "f13": 90,
        "f14": "ͨ�ŷ���",
        "f62": 1138455904
    },
    {
        "f12": "BK0732",
        "f13": 90,
        "f14": "�����",
        "f62": 493852032
    },
    {
        "f12": "BK1029",
        "f13": 90,
        "f14": "��������",
        "f62": 466498016
    },
    {
        "f12": "BK0428",
        "f13": 90,
        "f14": "������ҵ",
        "f62": 454905232
    },
    {
        "f12": "BK0478",
        "f13": 90,
        "f14": "��ɫ����",
        "f62": 413278816
    },
    {
        "f12": "BK1033",
        "f13": 90,
        "f14": "���",
        "f62": 378079568
    },
    {
        "f12": "BK0425",
        "f13": 90,
        "f14": "���̽���",
        "f62": 353470704
    },
    {
        "f12": "BK0479",
        "f13": 90,
        "f14": "������ҵ",
        "f62": 274561632
    },
    {
        "f12": "BK0457",
        "f13": 90,
        "f14": "�����豸",
        "f62": 273380544
    },
    {
        "f12": "BK0433",
        "f13": 90,
        "f14": "ũ������",
        "f62": 194380128
    },
    {
        "f12": "BK0740",
        "f13": 90,
        "f14": "����",
        "f62": 185108304
    },
    {
        "f12": "BK0451",
        "f13": 90,
        "f14": "���ز�����",
        "f62": 163542480
    },
    {
        "f12": "BK0437",
        "f13": 90,
        "f14": "ú̿��ҵ",
        "f62": 154974080
    },
    {
        "f12": "BK0464",
        "f13": 90,
        "f14": "ʯ����ҵ",
        "f62": 139236640
    },
    {
        "f12": "BK0910",
        "f13": 90,
        "f14": "ר���豸",
        "f62": 131462416
    },
    {
        "f12": "BK0538",
        "f13": 90,
        "f14": "��ѧ��Ʒ",
        "f62": 127124528
    },
    {
        "f12": "BK1034",
        "f13": 90,
        "f14": "��Դ�豸",
        "f62": 126577792
    },
    {
        "f12": "BK0475",
        "f13": 90,
        "f14": "����",
        "f62": 110107600
    },
    {
        "f12": "BK0450",
        "f13": 90,
        "f14": "���˸ۿ�",
        "f62": 97392752
    },
    {
        "f12": "BK0731",
        "f13": 90,
        "f14": "������ҵ",
        "f62": 87360000
    },
    {
        "f12": "BK0424",
        "f13": 90,
        "f14": "ˮ�ཨ��",
        "f62": 77782080
    },
    {
        "f12": "BK1018",
        "f13": 90,
        "f14": "����Ʒ",
        "f62": 67025398
    },
    {
        "f12": "BK1032",
        "f13": 90,
        "f14": "����豸",
        "f62": 62730516
    },
    {
        "f12": "BK0545",
        "f13": 90,
        "f14": "ͨ���豸",
        "f62": 62657824
    },
    {
        "f12": "BK1043",
        "f13": 90,
        "f14": "רҵ����",
        "f62": 58368718
    },
    {
        "f12": "BK0733",
        "f13": 90,
        "f14": "��װ����",
        "f62": 55949342
    },
    {
        "f12": "BK0458",
        "f13": 90,
        "f14": "�����Ǳ�",
        "f62": 48026145
    },
    {
        "f12": "BK0440",
        "f13": 90,
        "f14": "�����Ṥ",
        "f62": 41535098
    },
    {
        "f12": "BK1039",
        "f13": 90,
        "f14": "���ӻ�ѧƷ",
        "f62": 35798973
    },
    {
        "f12": "BK1042",
        "f13": 90,
        "f14": "ҽҩ��ҵ",
        "f62": 35048225
    },
    {
        "f12": "BK0436",
        "f13": 90,
        "f14": "��֯��װ",
        "f62": 33321392
    },
    {
        "f12": "BK1017",
        "f13": 90,
        "f14": "�ɾ���ҵ",
        "f62": 32398538
    },
    {
        "f12": "BK0420",
        "f13": 90,
        "f14": "���ջ���",
        "f62": 30673392
    },
    {
        "f12": "BK0725",
        "f13": 90,
        "f14": "װ��װ��",
        "f62": 20871694
    },
    {
        "f12": "BK0546",
        "f13": 90,
        "f14": "��������",
        "f62": 17192448
    },
    {
        "f12": "BK0728",
        "f13": 90,
        "f14": "������ҵ",
        "f62": 16605997
    },
    {
        "f12": "BK0726",
        "f13": 90,
        "f14": "������ѯ����",
        "f62": 4605565
    },
    {
        "f12": "BK0456",
        "f13": 90,
        "f14": "�ҵ���ҵ",
        "f62": 2196224
    },
    {
        "f12": "BK0484",
        "f13": 90,
        "f14": "ó����ҵ",
        "f62": -6384250
    },
    {
        "f12": "BK0429",
        "f13": 90,
        "f14": "�����豸",
        "f62": -9879982
    },
    {
        "f12": "BK0470",
        "f13": 90,
        "f14": "��ֽӡˢ",
        "f62": -16640069
    },
    {
        "f12": "BK0727",
        "f13": 90,
        "f14": "ҽ�Ʒ���",
        "f62": -18357648
    },
    {
        "f12": "BK1045",
        "f13": 90,
        "f14": "���ز�����",
        "f62": -19344204
    },
    {
        "f12": "BK0482",
        "f13": 90,
        "f14": "��ҵ�ٻ�",
        "f62": -20402896
    },
    {
        "f12": "BK0739",
        "f13": 90,
        "f14": "���̻�е",
        "f62": -20966731
    },
    {
        "f12": "BK1019",
        "f13": 90,
        "f14": "��ѧԭ��",
        "f62": -24278528
    },
    {
        "f12": "BK0486",
        "f13": 90,
        "f14": "�Ļ���ý",
        "f62": -24724848
    },
    {
        "f12": "BK0474",
        "f13": 90,
        "f14": "����",
        "f62": -26921344
    },
    {
        "f12": "BK0735",
        "f13": 90,
        "f14": "������豸",
        "f62": -34132288
    },
    {
        "f12": "BK0734",
        "f13": 90,
        "f14": "�鱦����",
        "f62": -44780485
    },
    {
        "f12": "BK0485",
        "f13": 90,
        "f14": "���ξƵ�",
        "f62": -44862640
    },
    {
        "f12": "BK0427",
        "f13": 90,
        "f14": "������ҵ",
        "f62": -48215306
    },
    {
        "f12": "BK1030",
        "f13": 90,
        "f14": "���",
        "f62": -49291728
    },
    {
        "f12": "BK0476",
        "f13": 90,
        "f14": "װ�޽���",
        "f62": -50638320
    },
    {
        "f12": "BK0422",
        "f13": 90,
        "f14": "������ҵ",
        "f62": -51513520
    },
    {
        "f12": "BK0729",
        "f13": 90,
        "f14": "��������",
        "f62": -56257174
    },
    {
        "f12": "BK0448",
        "f13": 90,
        "f14": "ͨ���豸",
        "f62": -59235440
    },
    {
        "f12": "BK0539",
        "f13": 90,
        "f14": "�ۺ���ҵ",
        "f62": -60713778
    },
    {
        "f12": "BK1028",
        "f13": 90,
        "f14": "ȼ��",
        "f62": -65575485
    },
    {
        "f12": "BK1016",
        "f13": 90,
        "f14": "��������",
        "f62": -66952142
    },
    {
        "f12": "BK1020",
        "f13": 90,
        "f14": "�ǽ�������",
        "f62": -80898064
    },
    {
        "f12": "BK0738",
        "f13": 90,
        "f14": "��Ԫ����",
        "f62": -108303040
    },
    {
        "f12": "BK0471",
        "f13": 90,
        "f14": "������ҵ",
        "f62": -111604384
    },
    {
        "f12": "BK0421",
        "f13": 90,
        "f14": "��·��·",
        "f62": -111906142
    },
    {
        "f12": "BK0454",
        "f13": 90,
        "f14": "������Ʒ",
        "f62": -119680192
    },
    {
        "f12": "BK0730",
        "f13": 90,
        "f14": "ũҩ��ҩ",
        "f62": -131122048
    },
    {
        "f12": "BK1038",
        "f13": 90,
        "f14": "��ѧ�����",
        "f62": -156417936
    },
    {
        "f12": "BK0481",
        "f13": 90,
        "f14": "�����㲿��",
        "f62": -168013408
    },
    {
        "f12": "BK0447",
        "f13": 90,
        "f14": "����������",
        "f62": -176807168
    },
    {
        "f12": "BK1040",
        "f13": 90,
        "f14": "��ҩ",
        "f62": -191926944
    },
    {
        "f12": "BK0480",
        "f13": 90,
        "f14": "���캽��",
        "f62": -223601920
    },
    {
        "f12": "BK1037",
        "f13": 90,
        "f14": "���ѵ���",
        "f62": -233917952
    },
    {
        "f12": "BK1046",
        "f13": 90,
        "f14": "��Ϸ",
        "f62": -255573683
    },
    {
        "f12": "BK0465",
        "f13": 90,
        "f14": "��ѧ��ҩ",
        "f62": -260174512
    },
    {
        "f12": "BK0459",
        "f13": 90,
        "f14": "����Ԫ��",
        "f62": -267329632
    },
    {
        "f12": "BK1035",
        "f13": 90,
        "f14": "���ݻ���",
        "f62": -334691120
    },
    {
        "f12": "BK1044",
        "f13": 90,
        "f14": "������Ʒ",
        "f62": -337899008
    },
    {
        "f12": "BK0438",
        "f13": 90,
        "f14": "ʳƷ����",
        "f62": -395324016
    },
    {
        "f12": "BK1036",
        "f13": 90,
        "f14": "�뵼��",
        "f62": -465186160
    },
    {
        "f12": "BK1041",
        "f13": 90,
        "f14": "ҽ����е",
        "f62": -586804928
    },
    {
        "f12": "BK0737",
        "f13": 90,
        "f14": "�������",
        "f62": -689905616
    },
    {
        "f12": "BK0477",
        "f13": 90,
        "f14": "�����ҵ",
        "f62": -736655152
    },
    {
        "f12": "BK0473",
        "f13": 90,
        "f14": "֤ȯ",
        "f62": -2288416528
    }
]


def get_mysql(block_code):
    b_k_list = []
    mysql = pymysql.connect(host='127.0.0.1', port=3366, user='root', password='gengxiang',
                            database='stock_tips', charset='utf8')
    cursor = mysql.cursor()
    sql = "SELECT * FROM block_data_detail WHERE code = '%s' order by id desc limit 20" % block_code
    cursor.execute(sql)
    results = cursor.fetchall()
    for row in results:
        stock = {
            'date': row[3],
            'name': row[2],
            'code': row[1],
            'price': row[4],
            'amo': row[6],  # �ɽ����Ԫ��
            'amp': row[5],  # �ǵ���%
            'qrr': row[7],  # ����
            'hs': row[8],  # ������
        }
        b_k_list.append(stock)
    return b_k_list


def save_bk_mysql(b_k_stock):
    mysql = pymysql.connect(host='127.0.0.1', port=3366, user='root', password='gengxiang',
                            database='stock_tips', charset='utf8')
    cursor = mysql.cursor()

    sql = "SELECT * FROM block_data_detail WHERE code = '%s' and date = '%s' limit 1" % \
          (b_k_stock['code'], b_k_stock['date'])
    cursor.execute(sql)
    results = cursor.fetchall()
    if len(results) == 0:
        sql = "INSERT INTO block_data_detail(code, name, date, price, amo, amp, qrr, hs)" \
              "VALUES ('%s', '%s', '%s', %s, %s, %s, %s, %s)" % \
              (b_k_stock['code'], b_k_stock['name'], b_k_stock['date'], b_k_stock['price'],
               b_k_stock['amo'], b_k_stock['amp'], b_k_stock['qrr'], b_k_stock['hs'])
        cursor.execute(sql)
    else:
        sql = "UPDATE block_data_detail SET price = %s, amo= %s, amp= %s, qrr = %s, hs = %s" \
              "WHERE code = '%s' and date = '%s'" % \
              (b_k_stock['price'], b_k_stock['amo'], b_k_stock['amp'],
               b_k_stock['qrr'], b_k_stock['hs'], b_k_stock['code'], b_k_stock['date'])
        cursor.execute(sql)
    mysql.commit()
    cursor.close()


def get_block_total(basic_list):
    total_b_price = 0
    total_b_amo = 0
    total_b_hs = 0
    for per in basic_list:
        total_b_price = total_b_price + per['price']
        total_b_amo = total_b_amo + per['amo']
        total_b_hs = total_b_hs + per['hs']
    return total_b_price, total_b_amo, total_b_hs


def get_analysis_info(basic_block_list, ma_min, ma_max):
    if len(basic_block_list) < 5:
        return None
    tuple_min0 = get_block_total(basic_block_list[0: ma_min + 0])
    tuple_max0 = get_block_total(basic_block_list[0: ma_max + 0])
    tuple_min1 = get_block_total(basic_block_list[1: ma_min + 1])
    tuple_max1 = get_block_total(basic_block_list[1: ma_max + 1])
    tuple_min2 = get_block_total(basic_block_list[2: ma_min + 2])
    tuple_max2 = get_block_total(basic_block_list[2: ma_max + 2])
    tuple_min3 = get_block_total(basic_block_list[3: ma_min + 3])
    tuple_max3 = get_block_total(basic_block_list[3: ma_max + 3])
    tuple_min4 = get_block_total(basic_block_list[4: ma_min + 4])
    tuple_max4 = get_block_total(basic_block_list[4: ma_max + 4])

    analysis_info = {
        'date': basic_block_list[0]['date'],
        'code': basic_block_list[0]['code'],
        'name': basic_block_list[0]['name'],
        'hs': basic_block_list[0]['hs'],
        'ahs': round(tuple_max0[2] / ma_max, 2),
        'price': basic_block_list[0]['price'],
        'aprice-0': [round(tuple_min0[0] / ma_min, 2), round(tuple_max0[0] / ma_max, 2)],
        'aprice-1': [round(tuple_min1[0] / ma_min, 2), round(tuple_max1[0] / ma_max, 2)],
        'aprice-2': [round(tuple_min2[0] / ma_min, 2), round(tuple_max2[0] / ma_max, 2)],
        'aprice-3': [round(tuple_min3[0] / ma_min, 2), round(tuple_max3[0] / ma_max, 2)],
        'aprice-4': [round(tuple_min4[0] / ma_min, 2), round(tuple_max4[0] / ma_max, 2)],
        'amo': round(basic_block_list[0]['amo'] / 10000, 2),
        'aamo-0': [round(tuple_min0[1] / ma_min / 10000, 2), round(tuple_max0[1] / ma_max / 10000, 2)],
        'aamo-1': [round(tuple_min1[1] / ma_min / 10000, 2), round(tuple_max1[1] / ma_max / 10000, 2)],
        'aamo-2': [round(tuple_min2[1] / ma_min / 10000, 2), round(tuple_max2[1] / ma_max / 10000, 2)],
        'aamo-3': [round(tuple_min3[1] / ma_min / 10000, 2), round(tuple_max3[1] / ma_max / 10000, 2)],
        'aamo-4': [round(tuple_min4[1] / ma_min / 10000, 2), round(tuple_max4[1] / ma_max / 10000, 2)],
        'amp': basic_block_list[0]['amp'],
        'qrr': basic_block_list[0]['qrr'],
    }
    return analysis_info


def analysis(analysis_info, ma_min, ma_max):
    if analysis_info is None:
        return
    if analysis_info['aprice-0'][0] < analysis_info['aprice-0'][1]:
        return

    aa_price = round((analysis_info['aprice-0'][1] + analysis_info['aprice-1'][1] + analysis_info['aprice-2'][1] +
                      analysis_info['aprice-3'][1] + analysis_info['aprice-4'][1]) / 5, 2)
    aat_volume = round((analysis_info['aamo-0'][1] + analysis_info['aamo-1'][1] + analysis_info['aamo-2'][1] +
                        analysis_info['aamo-3'][1] + analysis_info['aamo-4'][1]) / 5, 2)
    print(analysis_info['date'], "---->", analysis_info['name'], analysis_info['code'])
    print("��������̼�:%9s" % analysis_info['price'], "MA", ma_min, ":%9s" % analysis_info['aprice-0'][0], "MA",
          ma_max, ":%9s" % analysis_info['aprice-0'][1])
    print("����Ľ��׶�:%9s" % analysis_info['amo'], "MA", ma_min, ":%9s" % analysis_info['aamo-0'][0], "MA", ma_max,
          ":%9s" % analysis_info['aamo-0'][1])
    print("�ɽ������MA", ma_min, ":", analysis_info['amo'] >= analysis_info['aamo-0'][0], "�ɽ������MA", ma_max, ":",
          analysis_info['amo'] >= analysis_info['aamo-0'][1],
          "�ɽ���MA", ma_max, "��������:", analysis_info['aamo-0'][1] >= aat_volume)
    print("���̼۸���MA", ma_min, ":", analysis_info['price'] >= analysis_info['aprice-0'][0], "���̼۸���MA", ma_max,
          ":", analysis_info['price'] >= analysis_info['aprice-0'][1],
          "���̼�MA", ma_max, "��������:", analysis_info['aprice-0'][1] >= aa_price)
    print("========================================================================================")
    if (analysis_info['aamo-0'][1] >= aat_volume) & (analysis_info['aprice-0'][1] >= aa_price) \
            & (analysis_info['amo'] >= analysis_info['aamo-0'][1]) & (
            analysis_info['amo'] <= analysis_info['aamo-0'][0]) \
            & (analysis_info['price'] >= analysis_info['aprice-0'][0]) & (analysis_info['aprice-0'][1] >= aa_price):
        return analysis_info


def loop_bk():
    selects = []
    for bk in all_BK:
        # print(bk['f12'], "--->", bk['f14'])
        current_html = request.urlopen(
            'http://push2.eastmoney.com/api/qt/stock/get?ut=fa5fd1943c7b386f172d6893dbfba10b&invt=2&fltt=2&fields=f60,f43,f47,f48,f50,f58,f168,f170&secid=' + str(
                bk['f13']) + '.' + bk['f12'], timeout=1.0).read()

        current_str = json.loads(current_html.decode())['data']
        bk_stock = {
            'date': todayStr,  # ʱ��
            'name': current_str['f58'],  # ����
            'code': str(bk['f13']) + '.' + bk['f12'],  # ����
            'price': float(current_str['f43']),  # ���̼۸�
            'amo': int(round(float(current_str['f48']) / 10000, 2)),  # �ɽ����Ԫ��
            'amp': float(current_str['f170']),  # �ǵ���%
            'qrr': float(current_str['f50']),  # ����
            'hs': float(current_str['f168']),  # ������
        }
        save_bk_mysql(bk_stock)
        total_block_list = get_mysql(str(bk['f13']) + '.' + bk['f12'])
        # print(total_block_list)

        if len(total_block_list) >= 20:
            nn = analysis(get_analysis_info(total_block_list, 7, 16), 7, 16)
            if nn is not None:
                selects.append(nn)
        else:
            nn = analysis(get_analysis_info(total_block_list, 1, len(total_block_list) - 4), 1,
                          len(total_block_list) - 4)
            if nn is not None:
                selects.append(nn)
    return selects


def write_bk_file():
    # ��������
    today_str = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    with open("..\data\\" + today_str + "_bk.txt", "w") as file:
        file.write("")
    for bk in all_BK:
        current_html = request.urlopen(
            'http://push2.eastmoney.com/api/qt/stock/get?ut=fa5fd1943c7b386f172d6893dbfba10b&invt=2&fltt=2&fields=f60,f43,f47,f48,f50,f58,f168,f170&secid=' + str(
                bk['f13']) + '.' + bk['f12'], timeout=1.0).read()
        with open("..\data\\" + today_str + "_bk.txt", "a") as file:
            file.write(str(bk['f13']) + '.' + bk['f12'] + "->" + current_html.decode() + "\n")
            print("д���ļ�->", current_html.decode())


def get_bk_file():
    with open("..\data\\" + todayStr + "_bk.txt", "r") as file:
        line = file.readline()
        while line:
            current_str = json.loads(str(line)[11:])['data']
            bk_stock = {
                'date': todayStr,  # ʱ��
                'name': current_str['f58'],  # ����
                'code': str(line)[:8],  # ����
                'price': float(current_str['f43']),  # ���̼۸�
                'amo': int(round(float(current_str['f48']) / 10000, 2)),  # �ɽ����Ԫ��
                'amp': float(current_str['f170']),  # �ǵ���%
                'qrr': float(current_str['f50']),  # ����
                'hs': float(current_str['f168']),  # ������
            }
            # save_bk_mysql(bk_stock)
            print("��������mysql->", bk_stock)
            line = file.readline()


# ��������
todayStr = time.strftime('%Y-%m-%d', time.localtime(time.time()))

# write_bk_file()
# get_bk_file()
