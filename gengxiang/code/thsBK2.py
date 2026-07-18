# coding=gbk
import requests
from playwright.sync_api import sync_playwright

# 配置
BASE_URL = "https://data.10jqka.com.cn/funds/gnzjl/"
# 两个目标接口
API_BUY = "https://data.10jqka.com.cn/funds/gnzjl/field/buy/order/DESC/ajax/1/free/1/"
API_ZDF = "https://data.10jqka.com.cn/funds/gnzjl/field/tradezdf/order/DESC/ajax/1/free/1/"


def get_valid_hexin_v():
    """启动无头浏览器，访问页面自动生成hexin-v"""
    with sync_playwright() as p:
        # 无头模式，后台运行无窗口
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36"
        )
        # 访问资金概念首页，加载ths.js并自动生成v
        page.goto(BASE_URL, timeout=15000)
        page.wait_for_timeout(2000)  # 等待JS执行完成，写入Cookie v

        # 提取Cookie中的v值 = hexin-v
        cookies = page.context.cookies()
        hexin_v = ""
        for ck in cookies:
            if ck["name"] == "v":
                hexin_v = ck["value"]
                break
        browser.close()
        return hexin_v


def fetch_fund_data(api_url):
    """携带实时hexin-v请求接口，返回表格html"""
    hv = get_valid_hexin_v()
    headers = {
        "accept": "text/html, */*; q=0.01",
        "accept-language": "zh-CN,zh;q=0.9",
        "hexin-v": hv,
        "sec-ch-ua": '"Google Chrome";v="147", "Not.A/Brand";v="8", "Chromium";v="147"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "x-requested-with": "XMLHttpRequest",
        "referer": BASE_URL
    }
    resp = requests.get(api_url, headers=headers, timeout=10)
    return resp.text


if __name__ == "__main__":
    # 1. 获取按净流入排序榜单
    html_buy = fetch_fund_data(API_BUY)
    print("=== 板块净流入榜单HTML ===")
    print(html_buy[:1000])

    # 2. 获取按涨幅排序榜单
    html_zdf = fetch_fund_data(API_ZDF)
    print("\n=== 板块涨幅榜单HTML ===")
    print(html_zdf[:1000])
