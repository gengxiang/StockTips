# coding=gbk

import pymysql


def save_mysql(stock_info):
    print(stock_info)
    if '所属概念' not in stock_info:
        stock_info['所属概念'] = "-"

    mysql = pymysql.connect(host='127.0.0.1', port=3366, user='root', password='gengxiang',
                            database='stock_tips', charset='utf8')
    cursor = mysql.cursor()
    sql = "SELECT * FROM stock_info WHERE stock_code = '%s' limit 1" % \
          (stock_info['股票代码'])
    cursor.execute(sql)
    results = cursor.fetchall()
    if len(results) == 0:
        sql = "INSERT INTO stock_info(stock_code, stock_name, industry, concept,address, scope, market,code)" \
              "VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % \
              (stock_info['股票代码'], stock_info['股票简称'], stock_info['所属同花顺行业'],
               str(stock_info['所属概念']).replace("'", "-"),
               stock_info['注册地址'], str(stock_info['经营范围']).replace("'", "-"), stock_info['market_code'],
               stock_info['code'])
        print(sql)
        cursor.execute(sql)
    else:
        sql = "UPDATE stock_info SET concept = '%s', scope= '%s' WHERE stock_code = '%s'" % \
              (str(stock_info['所属概念']).replace("'", "-"), str(stock_info['经营范围']).replace("'", "-"),
               stock_info['股票代码'])
        print(sql)
        cursor.execute(sql)
    mysql.commit()
    cursor.close()


def get_mysql(name):
    mysql = pymysql.connect(host='127.0.0.1', port=3366, user='root', password='gengxiang',
                            database='stock_tips', charset='utf8')
    cursor = mysql.cursor()

    sql = "SELECT * FROM stock_info WHERE stock_name = '%s' limit 1" % \
          (str(name))
    cursor.execute(sql)
    results = cursor.fetchall()
    return results[0]


stock = get_mysql('众泰汽车')
print(str(stock[2]))

# l_num = 0
#
# while l_num < 45:
#     l_num = l_num + 1
#     with open('../result/all/new ' + str(l_num) + '.txt', 'rb') as file:
#         data_str = file.read()
#         data = json.loads(data_str)
#         for ccs in range(0, len(data)):
#             save_mysql(data[ccs])

#
# {'股票代码': '000790.SZ',
#  '股票简称': '华神科技',
#  '所属同花顺行业': '医药生物-中药-中药Ⅲ',
#  '上市板块': '主板',
#  '所属概念': '抗肝癌;兽药;生物医药;融资融券;抗癌;单抗;转融券标的;仿制药;医保目录;流感;眼科医疗;基建工程;中医药;医美概念;装配式建筑;医疗器械概念;大消费;电子商务;合成生物;西部大开发',
#  '注册地址': '四川省成都市郫都区高新区(西区)蜀新大道1168号2栋1楼101号',
#  '经营范围': '高新技术产品开发生产、经营；中西制剂、原料药的生产（具体经营项目以药品生产许可证核定范围为准，并仅限于分支机构凭药品生产许可证在有效期内从事经营）；药业技术服务和咨询，商品销售（不含国家限制产品和禁止流通产品）；物业管理（凭资质证经营）、咨询及其它服务；农产品自研产品销售；房地产开发（凭资质证经营）。',
#  'market_code': '33',
#  'code': '000790'}
