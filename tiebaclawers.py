import os
import time
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium. webdriver. common. by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import requests
from  pyquery import PyQuery as pq
from urllib.parse import quote
import threading


headers = {
    'User-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                 'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.69 Safari/537.36'
}

class Imgdown_thread(threading.Thread):
    def __init__(self, url):
        threading.Thread.__init__(self)
        self.url = url
    def run(self):
        img_link = self.url
        img_name = f'{img_link}'.split('/')[-1]
        img = requests.get(img_link, headers=headers)
        if img_name.split('.')[-1] == 'jpg':
            with open(dir_name+'/'+img_name, 'wb') as f:
                f.write(img.content)
                print(f'{img_link}下载完成')


def blog(link, page, browser, dir_name):
    print(f"正在下载第{page}页")
    url = link+f'{page}'
    browser.get(url)
    browser.execute_script('document.documentElement.scrollTop=100000')
    time.sleep(5)
    html = browser.page_source
    wait = WebDriverWait(browser, 10)
    source = pq(html)
    items = source('.d_post_content.j_d_post_content img').items()
    source = source('.d_post_content.j_d_post_content img')
    index = 0
    for item in items:
       index = index+1
    for i in range(0, index):
        souremlemte = source.eq(i)
        img_link = souremlemte.attr('src')
        down = Imgdown_thread(img_link)
        down.start()


if __name__ == '__main__':
    print('输入你要下载的帖子后面的数字编号：')
    url_num = input()
    print('输入保存的文件夹的名称：')
    dir_name =input()
    url = 'https://tieba.baidu.com/p/'+url_num
    link = 'https://tieba.baidu.com/p/'+url_num+'?pn='
    #option = webdriver.ChromeOptions()
    #option.add_argument('--headless')
    browser= webdriver.Chrome()
    browser.get(url)
    page_sour = browser.page_source
    page_sour = pq(page_sour)
    pages_index = page_sour('.l_reply_num').text().split('，')
    pages_index = pages_index[1].split('页')[0]
    pages_index = pages_index.split('共')[-1]
    pages_index = int(pages_index)
    browser.close()
    browser = webdriver.Chrome()
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)
    for i in range (1, pages_index+1):
        blog(link, i, browser, dir_name)
    browser.close()
