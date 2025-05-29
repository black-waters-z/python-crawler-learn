# requests.session():维持会话,可以让我们在跨请求时保存某些参数
import time

import pandas as pd
import requests
from lxml import etree
import re

proxies = {
    "http": "121.40.98.50:80",  # HTTP 代理
}

# 开始封装：
# 目标url
form_data = {
    'form_email': '',
    'form_password': '',
}
# 设置请求头
req_header = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
}


def getlist(loginurl, infourl, session) -> list[str]:
    # 使用session发起请求
    response = session.post(loginurl, headers=req_header, data=form_data,proxies=proxies)

    if response.status_code == 200:
        url = infourl
        # 访问主页：
        response = session.get(url, headers=req_header,proxies=proxies)
        print(response.text)
        list = []
        if response.status_code == 200:
            print(response.text)
            # 开始获取其中数据，对数据进行xpath
            html = etree.HTML(response.text, etree.HTMLParser())
            uls = html.xpath('//*[@id="content"]/div/div[1]/div[1]/div[2]/div[1]/div/ul')

            for ul in uls:
                lis = ul.xpath('./li')
                for li in lis:
                    name = li.xpath('./div[2]/div[1]/a/text()')[0]
                    href = li.xpath('./div[2]/div[1]/a/@href')[0]
                    list.append({"name": name, "href": href})

            return list
        else:
            print("请求失败")
    else:
        print('登录失败')
    response.close()


# 进入到评论页面
def get_comments(info, session) -> list:
    url = info['href']
    pattern = r"(https:\/\/book\.douban\.com\/subject\/\d+\/)"
    match = re.search(pattern, url)
    book = []
    book_name = info['name']
    if match:
        comment_url = match.group(1) + "comments"
        print(f"————————开始获取{info['name']}书籍评论————————")
        print(comment_url)
        response = session.get(comment_url, headers=req_header,proxies=proxies)
        if response.status_code == 200:
            html = etree.HTML(response.text, etree.HTMLParser())
            comments = html.xpath('//*[@id="comments"]/div[1]/ul/li')
            try:
                for comment in comments:
                    user_name = comment.xpath('./div[2]/h3/span[2]/a[1]/text()')[0]
                    true_comment = comment.xpath('./div[2]/p/span/text()')[0]
                    book.append({"book": book_name, "user": user_name, "comment": true_comment})
                return book
            except:
                print(f"{book_name}没有评论")
        else:
            print(f"{info['name']}访问出错")
    else:
        return ['找不到评论链接']
    response.close()


if __name__ == '__main__':
    loginurl = 'https://www.douban.com/accounts/login'
    infourl = 'https://book.douban.com/'
    # 实例化session
    session = requests.session()
    # 得到书名 and 链接
    infos = getlist(loginurl, infourl, session)
    # 往下进入每页，获取评论和评论人
    for info in infos:
        comment_data = get_comments(info, session)
        # 将评论保存在excel文件中,csv文件
        info_pd = pd.DataFrame(data=comment_data)
        # 将 DataFrame 数据 追加（append）到现有的 CSV 文件 中
        info_pd.to_csv("豆瓣评论.csv",mode="a",header=False,index=False)
        time.sleep(1)
    session.close()
