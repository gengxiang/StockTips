# coding=utf-8
import requests
from bs4 import BeautifulSoup


# http获取当前行情信息
def get_focus_review():
    review_url = []
    url = 'https://www.cls.cn/subject/1135'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        html_content = response.text
        # 用BeautifulSoup解析HTML
        soup = BeautifulSoup(html_content, 'html.parser')
        # 查找所有的链接
        for link in soup.find_all('a', attrs='f-l subject-interest-list-illustration'):
            review_url.append('https://www.cls.cn' + link.get('href'))
    else:
        print(f"Failed to retrieve the webpage: {response.status_code}")

    return review_url


# 金融界大盘云图
def get_jrj_view():
    url = 'https://gateway.jrj.com/quot-feed/category_hqs'
    # 请求头（可选）
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "zh-CN,zh;q=0.9",
        "content-type": "application/json",
        "deviceinfo": "{\"productId\":\"6000021\",\"version\":\"1.0.0\",\"device\":\"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36\",\"sysName\":\"Chrome\",\"sysVersion\":[\"chrome/127.0.0.0\"]}",
        "priority": "u=1, i",
        "productid": "6000021",
        "sec-ch-ua": "\"Not)A;Brand\";v=\"99\", \"Google Chrome\";v=\"127\", \"Chromium\";v=\"127\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "Windows",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "cross-site"
    }
    data = {
        "env": [1, 2, 4, 5],
        "cat": 11,
        "start": 0,
        "num": 10,
        "column": 10,
        "sort": 2}

    # 发送POST请求
    response = requests.post(url, headers=headers, json=data)  # 使用json参数发送JSON数据
    # 或者使用 data 参数发送表单数据：
    # response = requests.post(url, headers=headers, data=data)

    # 检查请求是否成功
    if response.status_code == 200:
        print(response.json()['data'])
        return response.json()['data']
    else:
        print(f"请求失败，状态码: {response.status_code}")
        print("错误信息:", response.text)

# get_jrj_view()
