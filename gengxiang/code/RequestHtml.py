# coding=gbk
from requests_html import HTMLSession

session = HTMLSession()
response = session.get("https://example.com")

# ��Ⱦ JavaScript���״����л��Զ����� Chromium��
response.html.render(timeout=20)

# ��ȡ��Ⱦ�������
print(response.html.html)
