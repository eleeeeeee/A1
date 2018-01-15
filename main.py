import re
from selenium import webdriver

browser = webdriver.Chrome()

rank_url = "http://www.bilibili.com/ranking#!/origin/119/0/30"

browser.get(rank_url)
content = browser.page_source
browser.quit()

pattern = re.compile('div class="rank-item"><div class="num">(.*?)'
                     '</div>.*?href="(.*?)" target="_blank"><div class="preview">.*?div class="title">(.*?)</div>',re.S)
item = re.findall(pattern,content)

base_url = "https://www.bilibili.com"

import time
import requests
from browsermobproxy import Server

for i in  range(5):

    server = Server("C:\Users\dactang\Downloads\\browsermob-proxy-2.0-beta-5-bin\\browsermob-proxy-2.0-beta-5\\bin\\browsermob-proxy")
    server.start()
    proxy = server.create_proxy()

    # profile = webdriver.FirefoxProfile()
    # profile.set_proxy(proxy.selenium_proxy())
    # driver = webdriver.Firefox(firefox_profile=profile)

    chrome_options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(chrome_options=chrome_options)

    proxy.new_har("bilibili")
    driver.get(base_url+item[i][1])


    time.sleep(1)
    content = proxy.har
    server.stop()
    driver.quit()

    video_box = []
    data = content['log']['entries']
    for j in range(len(data)):
        url = data[j]['request']['url']
        if url.find("mp4") != -1:
            print(url)
            video_box.append(url)


    hd_video_url = video_box[1]

    try:
        video = requests.get(hd_video_url,timeout=10)
    except requests.exceptions.ConnectionError:
        print ("fail")

    string = "../data/" + item[i][0] +item[i][2] +'.mp4'
    fp = open(string,'wb')
    fp.write(video.content)





