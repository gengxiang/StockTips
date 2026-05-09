# coding=gbk
import re

import requests
from bs4 import BeautifulSoup

# # from playwright.sync_api import sync_playwright
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.chrome.service import Service
# from webdriver.chrome import ChromeDriverManager

# 2. 同花顺概念资金流接口（AJAX 请求）
url = "https://data.10jqka.com.cn/funds/gnzjl/field/je/order/DESC/ajax/1/free/1/"

FILTER_KEYWORDS = [
    # 交易通道类
    "沪股通", "深股通", "融资融券", "北交所概念", "富时罗素",
    # 政策/改革类（宏观，非具体题材）
    "国企改革", "央企国企改革", "一带一路", "西部大开发", "福建自贸区", "海峡两岸",
    # 市场指数/工具类
    "同花顺漂亮100", "同花顺中特估100",
    # 资金/持股类
    "证金持股", "国家队持股", "回购增持再贷款概念",
    # 其他非题材类
    "专精特新", "中字头", "地方国资", "央企改革"
]


def get_cookie():
    return ""


def fetch_and_parse_bk_list():
    # https://data.eastmoney.com/bkzj/hy.html
    # 1. 修正请求头变量名（统一用 headers，避免拼写错误） https://data.10jqka.com.cn/funds/gnzjl/###
    cookie = "_ga=GA1.1.966233084.1764860120; __utma=156575163.966233084.1764860120.1765545861.1765545861.1; __utmz=156575163.1765545861.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); Hm_lvt_69929b9dce4c22a060bd22d703b2a280=1768737610; _ga_H2RK0R0681=GS2.1.s1768737611$o2$g0$t1768739056$j60$l0$h0; Hm_lvt_a333197d2292e40ca3f2321a61ddfa64=1776431492,1776955844,1777549735,1778077813; HMACCOUNT=8DBD565843D4A92C; Hm_lvt_9d25c03aef06fec6abea265b79509ba4=1776431492,1776955844,1777549735,1778077813; Hm_lvt_60bad21af9c824a4a0530d5dbf4357ca=1776431493,1776955844,1777549735,1778077813; Hm_lvt_78c58f01938e4d85eaf619eae71b4ed1=1776431493,1776955844,1777549735,1778077813; Hm_lvt_f79b64788a4e377c608617fba4c736e2=1776431493,1776955844,1777549735,1778077813; _tea_utm_cache_10000007=undefined; Hm_lpvt_a333197d2292e40ca3f2321a61ddfa64=1778328272; Hm_lpvt_9d25c03aef06fec6abea265b79509ba4=1778328272; Hm_lpvt_78c58f01938e4d85eaf619eae71b4ed1=1778328272; Hm_lpvt_60bad21af9c824a4a0530d5dbf4357ca=1778328272; Hm_lpvt_f79b64788a4e377c608617fba4c736e2=1778328272; v=A54LguqOezYGQq9SWkqC6TjS7z_lX2Pr9CEWvUgnC7fekTChsO-y6cSzZsob" \
             ""
    headers = {
        "Accept": "text/html, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cookie": cookie,
        # "Cookie": "_ga=GA1.1.966233084.1764860120; __utma=156575163.966233084.1764860120.1765545861.1765545861.1; __utmz=156575163.1765545861.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); Hm_lvt_69929b9dce4c22a060bd22d703b2a280=1768737610; _ga_H2RK0R0681=GS2.1.s1768737611$o2$g0$t1768739056$j60$l0$h0; Hm_lvt_a333197d2292e40ca3f2321a61ddfa64=1775236318,1775571426,1776088490,1776351902; HMACCOUNT=8DBD565843D4A92C; Hm_lvt_9d25c03aef06fec6abea265b79509ba4=1775236318,1775571426,1776088490,1776351902; Hm_lvt_78c58f01938e4d85eaf619eae71b4ed1=1775236318,1775571426,1776088491,1776351902; Hm_lvt_60bad21af9c824a4a0530d5dbf4357ca=1775236318,1775571426,1776088491,1776351902; Hm_lvt_f79b64788a4e377c608617fba4c736e2=1775236318,1775571426,1776088491,1776351902; _tea_utm_cache_10000007=undefined; Hm_lpvt_a333197d2292e40ca3f2321a61ddfa64=1776430695; Hm_lpvt_60bad21af9c824a4a0530d5dbf4357ca=1776430695; Hm_lpvt_f79b64788a4e377c608617fba4c736e2=1776430695; Hm_lpvt_78c58f01938e4d85eaf619eae71b4ed1=1776430695; Hm_lpvt_9d25c03aef06fec6abea265b79509ba4=1776430695; v=A5wJjAREGU1cyu2RCALz6CQ5bbFLFUDdwrtUA3adqitoOzKvniUQzxLJJJvF",
        "Dnt": "1",
        "Hexin-V": re.search(r'v=([^;]+)', cookie).group(1),
        "Priority": "u=1, i",
        "Referer": "https://data.10jqka.com.cn/funds/gnzjl/",
        "Sec-Ch-Ua": "\"Google Chrome\";v=\"143\", \"Chromium\";v=\"143\", \"Not A(Brand\";v=\"24\"",
        "Sec-Ch-Ua-Mobile": "?1",
        "Sec-Ch-Ua-Platform": "\"Android\"",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Mobile Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"
    }
    # 3. 发送 GET 请求（修正 headers 变量名，删除多余的 headers=header, 行）
    response = requests.get(
        url=url,
        headers=headers,  # 正确引用定义的 headers 变量
        timeout=100
    )
    # 检查请求是否成功
    response.raise_for_status()

    # 4. 解析响应（同花顺该接口返回 HTML，不是 JSON）
    print("响应状态码：", response.status_code)
    soup = BeautifulSoup(response.text, 'html.parser')
    tbody = soup.find('tbody')
    tr_list = tbody.find_all('tr') if tbody else []

    result = []
    for tr in tr_list:
        tds = tr.find_all('td')
        if len(tds) < 7:
            continue  # 跳过无效行

        # 核心字段提取
        industry_name = tds[1].find('a').text.strip()  # 行业名称
        industry_index = tds[2].text.strip()  # 行业指数

        inflow = float(tds[4].text.strip()) if tds[4].text.strip() else None  # 流入资金(亿)
        outflow = float(tds[5].text.strip()) if tds[5].text.strip() else None  # 流出资金(亿)
        net_flow = float(tds[6].text.strip()) if tds[6].text.strip() else None  # 净额(亿)
        company_count = int(tds[7].text.strip()) if tds[7].text.strip() else None  # 公司家数
        leading_stock = tds[8].find('a').text.strip()  # 领涨股名称
        leading_price = float(tds[10].text.strip()) if tds[10].text.strip() else None  # 领涨股当前价(元)

        result.append({'行业名称': industry_name, '净流入资金(亿)': net_flow, '领涨股': leading_stock})

    filtered_out = [item for item in result if item['行业名称'] not in FILTER_KEYWORDS]
    filtered_result = [item for item in filtered_out if item['净流入资金(亿)'] > 50][:10]
    return filtered_result

# fetch_and_parse_bk_list();
# print(get_10jqka_cookie_playwright())
# get_10jqka_cookie()
# 调用示例
# print(get_10jqka_cookie_selenium())
