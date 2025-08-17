# coding=gbk
from requests_html import HTMLSession

session = HTMLSession()
response = session.get("https://example.com")

# 渲染 JavaScript（首次运行会自动下载 Chromium）
response.html.render(timeout=20)

# 获取渲染后的内容
print(response.html.html)
