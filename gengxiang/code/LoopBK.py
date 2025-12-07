# coding=gbk
import json
import time
import urllib
from urllib import request

import pymysql

all_BK = [
    {
        "f12": "BK1031",
        "f13": 90,
        "f14": "光伏设备",
        "f62": 2103230496
    },
    {
        "f12": "BK1015",
        "f13": 90,
        "f14": "能源金属",
        "f62": 1580268288
    },
    {
        "f12": "BK1027",
        "f13": 90,
        "f14": "小金属",
        "f62": 1509017136
    },
    {
        "f12": "BK0736",
        "f13": 90,
        "f14": "通信服务",
        "f62": 1138455904
    },
    {
        "f12": "BK0732",
        "f13": 90,
        "f14": "贵金属",
        "f62": 493852032
    },
    {
        "f12": "BK1029",
        "f13": 90,
        "f14": "汽车整车",
        "f62": 466498016
    },
    {
        "f12": "BK0428",
        "f13": 90,
        "f14": "电力行业",
        "f62": 454905232
    },
    {
        "f12": "BK0478",
        "f13": 90,
        "f14": "有色金属",
        "f62": 413278816
    },
    {
        "f12": "BK1033",
        "f13": 90,
        "f14": "电池",
        "f62": 378079568
    },
    {
        "f12": "BK0425",
        "f13": 90,
        "f14": "工程建设",
        "f62": 353470704
    },
    {
        "f12": "BK0479",
        "f13": 90,
        "f14": "钢铁行业",
        "f62": 274561632
    },
    {
        "f12": "BK0457",
        "f13": 90,
        "f14": "电网设备",
        "f62": 273380544
    },
    {
        "f12": "BK0433",
        "f13": 90,
        "f14": "农牧饲渔",
        "f62": 194380128
    },
    {
        "f12": "BK0740",
        "f13": 90,
        "f14": "教育",
        "f62": 185108304
    },
    {
        "f12": "BK0451",
        "f13": 90,
        "f14": "房地产开发",
        "f62": 163542480
    },
    {
        "f12": "BK0437",
        "f13": 90,
        "f14": "煤炭行业",
        "f62": 154974080
    },
    {
        "f12": "BK0464",
        "f13": 90,
        "f14": "石油行业",
        "f62": 139236640
    },
    {
        "f12": "BK0910",
        "f13": 90,
        "f14": "专用设备",
        "f62": 131462416
    },
    {
        "f12": "BK0538",
        "f13": 90,
        "f14": "化学制品",
        "f62": 127124528
    },
    {
        "f12": "BK1034",
        "f13": 90,
        "f14": "电源设备",
        "f62": 126577792
    },
    {
        "f12": "BK0475",
        "f13": 90,
        "f14": "银行",
        "f62": 110107600
    },
    {
        "f12": "BK0450",
        "f13": 90,
        "f14": "航运港口",
        "f62": 97392752
    },
    {
        "f12": "BK0731",
        "f13": 90,
        "f14": "化肥行业",
        "f62": 87360000
    },
    {
        "f12": "BK0424",
        "f13": 90,
        "f14": "水泥建材",
        "f62": 77782080
    },
    {
        "f12": "BK1018",
        "f13": 90,
        "f14": "橡胶制品",
        "f62": 67025398
    },
    {
        "f12": "BK1032",
        "f13": 90,
        "f14": "风电设备",
        "f62": 62730516
    },
    {
        "f12": "BK0545",
        "f13": 90,
        "f14": "通用设备",
        "f62": 62657824
    },
    {
        "f12": "BK1043",
        "f13": 90,
        "f14": "专业服务",
        "f62": 58368718
    },
    {
        "f12": "BK0733",
        "f13": 90,
        "f14": "包装材料",
        "f62": 55949342
    },
    {
        "f12": "BK0458",
        "f13": 90,
        "f14": "仪器仪表",
        "f62": 48026145
    },
    {
        "f12": "BK0440",
        "f13": 90,
        "f14": "家用轻工",
        "f62": 41535098
    },
    {
        "f12": "BK1039",
        "f13": 90,
        "f14": "电子化学品",
        "f62": 35798973
    },
    {
        "f12": "BK1042",
        "f13": 90,
        "f14": "医药商业",
        "f62": 35048225
    },
    {
        "f12": "BK0436",
        "f13": 90,
        "f14": "纺织服装",
        "f62": 33321392
    },
    {
        "f12": "BK1017",
        "f13": 90,
        "f14": "采掘行业",
        "f62": 32398538
    },
    {
        "f12": "BK0420",
        "f13": 90,
        "f14": "航空机场",
        "f62": 30673392
    },
    {
        "f12": "BK0725",
        "f13": 90,
        "f14": "装修装饰",
        "f62": 20871694
    },
    {
        "f12": "BK0546",
        "f13": 90,
        "f14": "玻璃玻纤",
        "f62": 17192448
    },
    {
        "f12": "BK0728",
        "f13": 90,
        "f14": "环保行业",
        "f62": 16605997
    },
    {
        "f12": "BK0726",
        "f13": 90,
        "f14": "工程咨询服务",
        "f62": 4605565
    },
    {
        "f12": "BK0456",
        "f13": 90,
        "f14": "家电行业",
        "f62": 2196224
    },
    {
        "f12": "BK0484",
        "f13": 90,
        "f14": "贸易行业",
        "f62": -6384250
    },
    {
        "f12": "BK0429",
        "f13": 90,
        "f14": "交运设备",
        "f62": -9879982
    },
    {
        "f12": "BK0470",
        "f13": 90,
        "f14": "造纸印刷",
        "f62": -16640069
    },
    {
        "f12": "BK0727",
        "f13": 90,
        "f14": "医疗服务",
        "f62": -18357648
    },
    {
        "f12": "BK1045",
        "f13": 90,
        "f14": "房地产服务",
        "f62": -19344204
    },
    {
        "f12": "BK0482",
        "f13": 90,
        "f14": "商业百货",
        "f62": -20402896
    },
    {
        "f12": "BK0739",
        "f13": 90,
        "f14": "工程机械",
        "f62": -20966731
    },
    {
        "f12": "BK1019",
        "f13": 90,
        "f14": "化学原料",
        "f62": -24278528
    },
    {
        "f12": "BK0486",
        "f13": 90,
        "f14": "文化传媒",
        "f62": -24724848
    },
    {
        "f12": "BK0474",
        "f13": 90,
        "f14": "保险",
        "f62": -26921344
    },
    {
        "f12": "BK0735",
        "f13": 90,
        "f14": "计算机设备",
        "f62": -34132288
    },
    {
        "f12": "BK0734",
        "f13": 90,
        "f14": "珠宝首饰",
        "f62": -44780485
    },
    {
        "f12": "BK0485",
        "f13": 90,
        "f14": "旅游酒店",
        "f62": -44862640
    },
    {
        "f12": "BK0427",
        "f13": 90,
        "f14": "公用事业",
        "f62": -48215306
    },
    {
        "f12": "BK1030",
        "f13": 90,
        "f14": "电机",
        "f62": -49291728
    },
    {
        "f12": "BK0476",
        "f13": 90,
        "f14": "装修建材",
        "f62": -50638320
    },
    {
        "f12": "BK0422",
        "f13": 90,
        "f14": "物流行业",
        "f62": -51513520
    },
    {
        "f12": "BK0729",
        "f13": 90,
        "f14": "船舶制造",
        "f62": -56257174
    },
    {
        "f12": "BK0448",
        "f13": 90,
        "f14": "通信设备",
        "f62": -59235440
    },
    {
        "f12": "BK0539",
        "f13": 90,
        "f14": "综合行业",
        "f62": -60713778
    },
    {
        "f12": "BK1028",
        "f13": 90,
        "f14": "燃气",
        "f62": -65575485
    },
    {
        "f12": "BK1016",
        "f13": 90,
        "f14": "汽车服务",
        "f62": -66952142
    },
    {
        "f12": "BK1020",
        "f13": 90,
        "f14": "非金属材料",
        "f62": -80898064
    },
    {
        "f12": "BK0738",
        "f13": 90,
        "f14": "多元金融",
        "f62": -108303040
    },
    {
        "f12": "BK0471",
        "f13": 90,
        "f14": "化纤行业",
        "f62": -111604384
    },
    {
        "f12": "BK0421",
        "f13": 90,
        "f14": "铁路公路",
        "f62": -111906142
    },
    {
        "f12": "BK0454",
        "f13": 90,
        "f14": "塑料制品",
        "f62": -119680192
    },
    {
        "f12": "BK0730",
        "f13": 90,
        "f14": "农药兽药",
        "f62": -131122048
    },
    {
        "f12": "BK1038",
        "f13": 90,
        "f14": "光学光电子",
        "f62": -156417936
    },
    {
        "f12": "BK0481",
        "f13": 90,
        "f14": "汽车零部件",
        "f62": -168013408
    },
    {
        "f12": "BK0447",
        "f13": 90,
        "f14": "互联网服务",
        "f62": -176807168
    },
    {
        "f12": "BK1040",
        "f13": 90,
        "f14": "中药",
        "f62": -191926944
    },
    {
        "f12": "BK0480",
        "f13": 90,
        "f14": "航天航空",
        "f62": -223601920
    },
    {
        "f12": "BK1037",
        "f13": 90,
        "f14": "消费电子",
        "f62": -233917952
    },
    {
        "f12": "BK1046",
        "f13": 90,
        "f14": "游戏",
        "f62": -255573683
    },
    {
        "f12": "BK0465",
        "f13": 90,
        "f14": "化学制药",
        "f62": -260174512
    },
    {
        "f12": "BK0459",
        "f13": 90,
        "f14": "电子元件",
        "f62": -267329632
    },
    {
        "f12": "BK1035",
        "f13": 90,
        "f14": "美容护理",
        "f62": -334691120
    },
    {
        "f12": "BK1044",
        "f13": 90,
        "f14": "生物制品",
        "f62": -337899008
    },
    {
        "f12": "BK0438",
        "f13": 90,
        "f14": "食品饮料",
        "f62": -395324016
    },
    {
        "f12": "BK1036",
        "f13": 90,
        "f14": "半导体",
        "f62": -465186160
    },
    {
        "f12": "BK1041",
        "f13": 90,
        "f14": "医疗器械",
        "f62": -586804928
    },
    {
        "f12": "BK0737",
        "f13": 90,
        "f14": "软件开发",
        "f62": -689905616
    },
    {
        "f12": "BK0477",
        "f13": 90,
        "f14": "酿酒行业",
        "f62": -736655152
    },
    {
        "f12": "BK0473",
        "f13": 90,
        "f14": "证券",
        "f62": -2288416528
    }
]

# 非题材类板块代码集合（按属性分类标注）
non_theme_plate_codes = {
    # 市场交易/资金通道类
    "BK0596", "BK0707", "BK0804", "BK1107", "BK1108",
    # 指数/外资指数关联类
    "BK0701", "BK0867", "BK0879", "BK0612", "BK0611", "BK0821",
    "BK0500", "BK0610", "BK0705", "BK0568", "BK0743", "BK0742",
    "BK0638", "BK0999", "BK1000",
    # 资金持股/机构属性类
    "BK0552", "BK0718", "BK0535", "BK0536", "BK0520", "BK0823",
    # 股价/股权/交易走势类
    "BK1059", "BK1053", "BK1112", "BK1158", "BK0498", "BK0499",
    "BK0636", "BK0511", "BK0501", "BK0971", "BK0528", "BK0816",
    "BK1051", "BK0817", "BK0815", "BK1050",
    # 地域属性类
    "BK0590", "BK0594", "BK0838", "BK0549", "BK0566", "BK0684",
    "BK0534", "BK0926", "BK0677", "BK0643", "BK1193", "BK0813",
    "BK0524", "BK0514", "BK0697", "BK0683", "BK0525", "BK1194"
}


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
            'amo': row[6],  # 成交额（万元）
            'amp': row[5],  # 涨跌幅%
            'qrr': row[7],  # 量比
            'hs': row[8],  # 换手率
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
    print("今天的收盘价:%9s" % analysis_info['price'], "MA", ma_min, ":%9s" % analysis_info['aprice-0'][0], "MA",
          ma_max, ":%9s" % analysis_info['aprice-0'][1])
    print("今天的交易额:%9s" % analysis_info['amo'], "MA", ma_min, ":%9s" % analysis_info['aamo-0'][0], "MA", ma_max,
          ":%9s" % analysis_info['aamo-0'][1])
    print("成交额高于MA", ma_min, ":", analysis_info['amo'] >= analysis_info['aamo-0'][0], "成交额高于MA", ma_max, ":",
          analysis_info['amo'] >= analysis_info['aamo-0'][1],
          "成交额MA", ma_max, "趋势向上:", analysis_info['aamo-0'][1] >= aat_volume)
    print("收盘价高于MA", ma_min, ":", analysis_info['price'] >= analysis_info['aprice-0'][0], "收盘价高于MA", ma_max,
          ":", analysis_info['price'] >= analysis_info['aprice-0'][1],
          "收盘价MA", ma_max, "趋势向上:", analysis_info['aprice-0'][1] >= aa_price)
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
        try:
            current_html = request.urlopen(
                'http://push2.eastmoney.com/api/qt/stock/get?ut=fa5fd1943c7b386f172d6893dbfba10b&invt=2&fltt=2&fields=f60,f43,f47,f48,f50,f58,f168,f170&secid=' + str(
                    bk['f13']) + '.' + bk['f12'], timeout=8.0).read()
        except:
            print("请求异常等待………………")
            time.sleep(5)
            current_html = request.urlopen(
                'http://push2.eastmoney.com/api/qt/stock/get?ut=fa5fd1943c7b386f172d6893dbfba10b&invt=2&fltt=2&fields=f60,f43,f47,f48,f50,f58,f168,f170&secid=' + str(
                    bk['f13']) + '.' + bk['f12'], timeout=9.0).read()

        current_str = json.loads(current_html.decode())['data']
        bk_stock = {
            'date': todayStr,  # 时间
            'name': current_str['f58'],  # 名称
            'code': str(bk['f13']) + '.' + bk['f12'],  # 编码
            'price': float(current_str['f43']),  # 收盘价格
            'amo': int(round(float(current_str['f48']) / 10000, 2)),  # 成交额（万元）
            'amp': float(current_str['f170']),  # 涨跌幅%
            'qrr': float(current_str['f50']),  # 量比
            'hs': float(current_str['f168']),  # 换手率
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
    # 今天日期
    today_str = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    with open("..\data\\" + today_str + "_bk.txt", "w") as file:
        file.write("")
    for bk in all_BK:
        current_html = request.urlopen(
            'http://push2.eastmoney.com/api/qt/stock/get?ut=fa5fd1943c7b386f172d6893dbfba10b&invt=2&fltt=2&fields=f60,f43,f47,f48,f50,f58,f168,f170&secid=' + str(
                bk['f13']) + '.' + bk['f12'], timeout=1.0).read()
        with open("..\data\\" + today_str + "_bk.txt", "a") as file:
            file.write(str(bk['f13']) + '.' + bk['f12'] + "->" + current_html.decode() + "\n")
            print("写入文件->", current_html.decode())


def get_bk_file():
    with open("..\data\\" + todayStr + "_bk.txt", "r") as file:
        line = file.readline()
        while line:
            current_str = json.loads(line[11:len(line) - 1])['data']
            bk_stock = {
                'date': todayStr,  # 时间
                'name': current_str['f58'],  # 名称
                'code': str(line)[:8],  # 编码
                'price': float(current_str['f43']),  # 收盘价格
                'amo': int(round(float(current_str['f48']) / 10000, 2)),  # 成交额（万元）
                'amp': float(current_str['f170']),  # 涨跌幅%
                'qrr': float(current_str['f50']),  # 量比
                'hs': float(current_str['f168']),  # 换手率
            }
            # save_bk_mysql(bk_stock)
            print("保存数据mysql->", bk_stock)
            line = file.readline()


def fetch_and_parse_bk_list():
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "zh-CN,zh;q=0.9",
        "cache-control": "max-age=0",
        "sec-ch-ua": "\"Google Chrome\";v=\"143\", \"Chromium\";v=\"143\", \"Not A(Brand\";v=\"24\"",
        "sec-ch-ua-mobile": "?1",
        "sec-ch-ua-platform": "\"Android\"",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "none",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
    }
    # 1. 获取所有板块列表 https://data.eastmoney.com/bkzj/hy.html
    url = "http://push2.eastmoney.com/api/qt/clist/get?cb=jQuery112308176510448004067_1764860382533&fid=f62&po=1&pz=100&pn=1&np=1&fltt=2&invt=2&ut=8dec03ba335b81bf4ebdf7b29ec27d15&fs=m%3A90+t%3A3&fields=f12%2Cf14%2Cf2%2Cf3%2Cf62%2Cf184%2Cf66%2Cf69%2Cf72%2Cf75%2Cf78%2Cf81%2Cf84%2Cf87%2Cf204%2Cf205%2Cf124%2Cf1%2Cf13"
    req = urllib.request.Request(url, headers=headers)
    response = urllib.request.urlopen(req, timeout=105)
    raw = response.read().decode('utf-8')
    json_str = raw[raw.find('(') + 1: raw.rfind(')')]
    data = json.loads(json_str)
    bk_list = data['data']['diff']

    filtered_bk = [bk for bk in bk_list if
                   (bk.get('f66', 0) > 1000000000) and (bk.get('f12') not in non_theme_plate_codes)]
    filtered_bk = sorted(filtered_bk, key=lambda x: x['f66'], reverse=True)
    stock_dict = {}

    for idx, bk in enumerate(filtered_bk[:10], start=1):
        bk_code = bk.get('f12')
        bk_name = bk.get('f14')
        bk_net_inflow = bk.get('f66', 0) + bk.get('f72', 0)
        # bk_info = f"{bk_name}({bk_net_inflow})"
        bk_info = f"{bk_name}[{idx}]"
        # 构造请求URL，替换BK1090为当前板块code https://data.eastmoney.com/bkzj/BK1090.html
        stock_url = f"http://push2.eastmoney.com/api/qt/clist/get?cb=jQuery112302720680570794537_1764861100324&fid=f62&po=1&pz=20&pn=1&np=1&fltt=2&invt=2&ut=8dec03ba335b81bf4ebdf7b29ec27d15&fs=b%3A{bk_code}&fields=f12%2Cf14%2Cf2%2Cf3%2Cf62%2Cf184%2Cf66%2Cf69%2Cf72%2Cf75%2Cf78%2Cf81%2Cf84%2Cf87%2Cf204%2Cf205%2Cf124%2Cf1%2Cf13"
        try:
            stock_req = urllib.request.Request(stock_url, headers=headers)
            stock_resp = urllib.request.urlopen(stock_req, timeout=105)
            stock_raw = stock_resp.read().decode('utf-8')
            stock_json_str = stock_raw[stock_raw.find('(') + 1: stock_raw.rfind(')')]
            stock_data = json.loads(stock_json_str)
            stock_list = stock_data['data']['diff']
        except Exception as e:
            print(f"板块 {bk_code} {bk_name} 请求失败: {e}")
            continue

        filtered_bst = [bst for bst in stock_list if bst.get('f3', 0) > 8]
        for stock in filtered_bst[:10]:
            code = stock.get('f12')
            if code in stock_dict:
                stock_dict[code]['板块列表'].append(bk_info)
            else:
                stock_dict[code] = {
                    'code': code,
                    'name': stock.get('f14'),
                    # '最新价': stock.get('f2'),
                    '涨跌幅': stock.get('f3'),
                    # '成交额': stock.get('f62'),
                    '主力净流入': stock.get('f184'),
                    # '涨速': stock.get('f66'),
                    # '换手率': stock.get('f169'),
                    '板块列表': [bk_info]
                }

    stock_values = list(stock_dict.values())
    result = sorted(stock_values, key=lambda x: x['主力净流入'], reverse=True)

    # 输出去重后的股票列表，板块信息格式：板块(板块净流入),板块(板块净流入)
    for stock in result:
        # stock['板块'] = ",".join(stock['板块列表'])
        print(stock)
    return result

# 调用函数
# fetch_and_parse_bk_list()
# 今天日期
# todayStr = time.strftime('%Y-%m-%d', time.localtime(time.time()))
