import time
import re

import pandas as pd
import requests
import re

from lxml import etree

"""
url='https://hrss.ah.gov.cn/content/column/6791574?pageIndex'
通过第一页，可以获得整个公开招聘有多少页，返回页数

开始每页爬取url链接，文案名字，保存至list中
得到list，访问每个链接，爬取文案，以及邮箱值，若不能获得，则返回无邮箱联系方式
url='https://hrss.ah.gov.cn/content/column/6791574?pageIndex=1'

"""

proxies = {
    "http": "121.40.98.50:80",  # HTTP 代理
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36'
}

url = 'https://hrss.ah.gov.cn/zxzx/ztzl/ahsszsydwgkzpzl/ssgxgkzp/index.html'
page_url = 'https://hrss.ah.gov.cn/content/column/6791574?pageIndex='


def get_page_num(url) -> int:
    response = requests.get(url=url, headers=headers, proxies=proxies)
    if response.status_code==200:
        res = re.search(r'pageCount:(\d+)', response.text, re.S)
        if res:
            print(f'一共有{res.group(1)}页数据')
        else:
            print('找不到页码')
        response.close()
        return res.group(1)
    else:
        print('访问失败')
        response.close()


# url='https://hrss.ah.gov.cn/content/column/6791574?pageIndex='
def get_page_recruit_href(page_num: int) -> list:
    content_list = []
    total_page_url = page_url + str(page_num)
    response = requests.get(url=total_page_url, headers=headers, proxies=proxies)
    html = etree.HTML(response.text, etree.HTMLParser())
    lis = html.xpath('/html/body/div[1]/div[2]/div/div/div[2]/div[2]/div[3]/ul/li')
    for li in lis:
        # a
        try:
            href = li.xpath('./a/@href')[0]
            title = li.xpath('./a/span/text()')[0]
            content_time=li.xpath('./span/text()')[0]
            content_list.append({'title': title, 'href': href,'time':content_time})
        except:
            print('这是分割线')
    response.close()
    time.sleep(3)
    return content_list


def get_recruit_content_email(content_time,title,url):
    time.sleep(3)
    response = requests.get(url, headers=headers, proxies=proxies)
    if response.status_code==200:
        print(f'{title}访问成功，正在获取')
        response.encoding = 'utf-8'  # 中文网页常用编码
        html = etree.HTML(response.text, etree.HTMLParser())
        elements = html.xpath('/html/body/div[1]/div[2]/div/div/div[2]/div/div[2]//text()')
        content=''
        for element in elements:
            content += element.replace('\u00A0', ' ')

        res = re.findall(r'\b([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,})\b', response.text, re.S)
        if res:
            email =list(dict.fromkeys(res))
            content_list = {'title': title, 'time': content_time, 'content': content, 'all_email': email,
                            'last_email': email[-1]}
        else:
            email='没有email'
            content_list = {'title': title, 'time': content_time, 'content': content, 'all_email': email,
                            'last_email': '没有email'}

        response.close()
        return content_list
    else:
        print('访问失败')
        response.close()



if __name__=='__main__':
    # 获取一共要爬取多少页
    page_number=get_page_num(url)
    # 爬一页，休息十秒钟
    time.sleep(2)
    for page in range(1,int(page_number)+1):
        print(f'正在获取第{page}页')
        lists=get_page_recruit_href(page_num=page)
        # 开始一页一页地取
        content_emails=[]
        for li in lists:
            content_email=get_recruit_content_email(url=li['href'], content_time=li['time'], title=li['title'])
            content_emails.append(content_email)

        content_emails_pd=pd.DataFrame(data=content_emails)
        content_emails_pd.to_csv('content_emails1.csv',encoding='utf-8-sig',mode="a",index=False)


