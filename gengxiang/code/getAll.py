# coding=gbk

import pymysql


def save_mysql(stock_info):
    print(stock_info)
    if '��������' not in stock_info:
        stock_info['��������'] = "-"

    mysql = pymysql.connect(host='127.0.0.1', port=3366, user='root', password='gengxiang',
                            database='stock_tips', charset='utf8')
    cursor = mysql.cursor()
    sql = "SELECT * FROM stock_info WHERE stock_code = '%s' limit 1" % \
          (stock_info['��Ʊ����'])
    cursor.execute(sql)
    results = cursor.fetchall()
    if len(results) == 0:
        sql = "INSERT INTO stock_info(stock_code, stock_name, industry, concept,address, scope, market,code)" \
              "VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % \
              (stock_info['��Ʊ����'], stock_info['��Ʊ���'], stock_info['����ͬ��˳��ҵ'],
               str(stock_info['��������']).replace("'", "-"),
               stock_info['ע���ַ'], str(stock_info['��Ӫ��Χ']).replace("'", "-"), stock_info['market_code'],
               stock_info['code'])
        print(sql)
        cursor.execute(sql)
    else:
        sql = "UPDATE stock_info SET concept = '%s', scope= '%s' WHERE stock_code = '%s'" % \
              (str(stock_info['��������']).replace("'", "-"), str(stock_info['��Ӫ��Χ']).replace("'", "-"),
               stock_info['��Ʊ����'])
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


stock = get_mysql('��̩����')
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
# {'��Ʊ����': '000790.SZ',
#  '��Ʊ���': '����Ƽ�',
#  '����ͬ��˳��ҵ': 'ҽҩ����-��ҩ-��ҩ��',
#  '���а��': '����',
#  '��������': '���ΰ�;��ҩ;����ҽҩ;������ȯ;����;����;ת��ȯ���;����ҩ;ҽ��Ŀ¼;����;�ۿ�ҽ��;��������;��ҽҩ;ҽ������;װ��ʽ����;ҽ����е����;������;��������;�ϳ�����;�����󿪷�',
#  'ע���ַ': '�Ĵ�ʡ�ɶ���ۯ����������(����)���´��1168��2��1¥101��',
#  '��Ӫ��Χ': '���¼�����Ʒ������������Ӫ�������Ƽ���ԭ��ҩ�����������徭Ӫ��Ŀ��ҩƷ�������֤�˶���ΧΪ׼���������ڷ�֧����ƾҩƷ�������֤����Ч���ڴ��¾�Ӫ����ҩҵ�����������ѯ����Ʒ���ۣ������������Ʋ�Ʒ�ͽ�ֹ��ͨ��Ʒ������ҵ����ƾ����֤��Ӫ������ѯ����������ũ��Ʒ���в�Ʒ���ۣ����ز�������ƾ����֤��Ӫ����',
#  'market_code': '33',
#  'code': '000790'}
