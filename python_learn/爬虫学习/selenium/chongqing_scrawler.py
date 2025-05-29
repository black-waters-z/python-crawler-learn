import time

from selenium import webdriver #用于操作浏览器
from selenium.webdriver.chrome.options import Options #用于设置谷歌浏览器
from selenium.webdriver.chrome.service import Service

def start_chrome():
    # 创建设置浏览器对象
    chrome_driver_path = r"D:\py\Python3\chromedriver.exe"
    q1=Options()
    # 禁用沙盒模式
    q1.add_argument('--no-sandbox')
    # 保持浏览器打开状态(默认代码执行完毕自动关闭）
    q1.add_experimental_option('detach',True)
    # 创建并启动浏览器
    a1=webdriver.Chrome(service=Service(executable_path=chrome_driver_path),options=q1)
    return a1
"""

def start():
    from selenium import webdriver

    # 初始化 WebDriver 并打开一个谷歌浏览器窗口
    driver = webdriver.Chrome()

    # 打开一个网页
    driver.get('https://www.baidu.com')

    # 打印页面标题
    print(driver.title)

    # 关闭浏览器
    driver.quit()

"""

"""
浏览器最大化：maximize_window()
浏览器最小化：minimize_window()
"""
a1=start_chrome()
# 打开指定网址
a1.get('http://baidu.com/')
time.sleep(2)
a1.maximize_window()
time.sleep(2)
# 关闭当前标签页,关闭整个窗口是因为只有这个标签页
a1.minimize_window()
time.sleep(2)
a1.close()
# 退出浏览器，释放驱动
a1.quit()

