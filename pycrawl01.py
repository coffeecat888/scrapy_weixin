"""
pycrawl01.py 爬虫文件
"""
# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
import time,json,random,requests,re
from wxarticle.models import *
from django.db.models import Min
from datetime import datetime
from django.utils import timezone
import re

'''登录微信公众号，获取登录之后的cookies信息，并保存到本地文本中'''
def wechat_login(account_name,password):
    '''用webdriver启动谷歌浏览器'''
    driver = webdriver.Chrome()
    driver.get("https://mp.weixin.qq.com/")
    time.sleep(2)
    driver.find_element(By.XPATH,'//*[@id="header"]/div[2]/div/div/div[2]/a').click()
    '''清空账号框中的内容'''
    driver.find_element(By.NAME,"account").clear()
    driver.find_element(By.NAME,"account").send_keys(account_name)
    time.sleep(1)
    driver.find_element(By.NAME,"password").clear()
    driver.find_element(By.NAME,"password").send_keys(password)
    time.sleep(1)
    driver.find_element(By.CLASS_NAME,"frm_checkbox_label").click()
    time.sleep(1)
    '''自动点击登录按钮进行登录'''
    driver.find_element(By.CLASS_NAME,"btn_login").click()
    '''拿手机扫二维码！'''
    time.sleep(20)
    cookie_items = driver.get_cookies()
    post = {}
    ''' 获取到的cookies是列表形式，将cookies转成json形式并存入本地名为cookie的文本中'''
    for cookie_item in cookie_items:
        post[cookie_item['name']] = cookie_item['value']
    cookie_str = json.dumps(post)
    with open('wxcookie.txt', 'w+', encoding='utf-8') as f:
        f.write(cookie_str)
    driver.quit()

'''获取微信公众号token,fakeid,nickname,alias,signature,round_head_img'''
def wxh_get_fakeid(query):
    '''query为要爬取的公众号名称'''
    url = 'https://mp.weixin.qq.com'#公众号主页
    '''设置headers'''
    header = {
        "HOST": "mp.weixin.qq.com",
        "User-Agent": \
            "Mozilla/\
            5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/\
            537.36 (KHTML, like Gecko) Chrome/\
            120.0.0.0 Safari/\
            537.36",
        "Accept": "* / *",
        "Accept - Encoding": "gzip, deflate, br ,utf-8",
        "Accept - Language": "zh - CN, zh;q = 0.9",
        "X - Requested - With": "XMLHttpRequest"
    }
    from requests.packages import urllib3
    urllib3.disable_warnings()  # 关闭警告
    '''读取获取到的cookies'''
    with open('wxcookie.txt', 'r', encoding='utf-8') as f:
        cookie = f.read()
        f.close()
    cookies = json.loads(cookie)
    session = requests.Session()
    session.keep_alive = False
    session.adapters.DEFAULT_RETRIES = 511# 增加重试连接次数
    time.sleep(1)
    '''
    登录之后的微信公众号首页url变化为：
    https://mp.weixin.qq.com/cgi-bin/home?t=home/index&lang=zh_CN&token=1588014800
    从这里获取token信息
    '''
    response = session.get(url=url, cookies=cookies, verify=False)
    # print(response.url)
    token = re.findall(r'token=(\d+)', str(response.url))[0]
    time.sleep(1)
    '''搜索微信公众号的接口地址'''
    search_url = 'https://mp.weixin.qq.com/cgi-bin/searchbiz'
    '''搜索微信公众号接口需要传入的参数，有三个变量：微信公众号token、随机数random、搜索的微信公众号名字query'''
    query_params = {
        'action': 'search_biz',
        'token': token,
        'lang': 'zh_CN',
        'f': 'json',
        'ajax': '1',
        'random': random.random(),
        'query': query,
        'begin': '0',
        'count': '5'
    }
    '''打开搜索微信公众号接口地址，需要传入相关参数信息如：cookies、params、headers'''
    search_response = session.get(
        search_url,
        cookies=cookies,
        headers=header,
        params=query_params)
    '''取搜索结果中的第一个公众号'''
    '''lists为json格式，包含了公众号的名称、英文缩写、图标、介绍等信息'''
    lists = search_response.json()['list'][0]
    ''' 获取这个公众号的fakeid，后面爬取公众号文章需要此字段'''
    fakeid = lists['fakeid']
    nickname = lists['nickname']#微信公众号中文
    alias = lists['alias']#微信公众号英文
    signature = lists['signature']#微信公众号中文简介
    round_head_img = lists['round_head_img']#微信公众号图标链接
    # print(token)
    # print(fakeid)
    return token,fakeid,nickname,alias,signature,round_head_img

'''爬取该微信公众号文章信息列表并写入数据表'''
def wxh_get_content(nickname,fakeid):
    appmsg_url = 'https://mp.weixin.qq.com/cgi-bin/appmsg'
    header = {
        "HOST": "mp.weixin.qq.com",
        "User-Agent": \
            "Mozilla/\
            5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/\
            537.36 (KHTML, like Gecko) Chrome/\
            120.0.0.0 Safari/\
            537.36",
        "Accept": "* / *",
        "Accept - Encoding": "gzip, deflate, br, utf-8",
        "Accept - Language": "zh - CN, zh;q = 0.9",
        "X - Requested - With": "XMLHttpRequest"
    }
    from requests.packages import urllib3
    urllib3.disable_warnings()  # 关闭警告
    # 读取获取到的cookies
    with open('wxcookie.txt', 'r', encoding='utf-8') as f:
        cookie = f.read()
        f.close()
    cookies = json.loads(cookie)
    session = requests.Session()
    session.keep_alive = False
    session.adapters.DEFAULT_RETRIES = 511
    time.sleep(1)
    response = session.get('https://mp.weixin.qq.com', cookies=cookies, verify=False)
    token = re.findall(r'token=(\d+)', str(response.url))[0]
    '''搜索文章需要传入几个参数：登录的公众号token、要爬取文章的公众号fakeid、随机数random'''
    query_id_data = {
        'token': token,
        'lang': 'zh_CN',
        'f': 'json',
        'ajax': '1',
        'random': random.random(),
        'action': 'list_ex',
        'begin': '0',  # 不同页，此参数变化，变化规则为每页加5
        'count': '5',
        'query': '',
        'fakeid': fakeid,
        'type': '9'
    }
    '''打开搜索的微信公众号文章列表页'''
    appmsg_response = session.get(
        appmsg_url,
        cookies=cookies,
        headers=header,
        params=query_id_data)
    '''获取文章总数'''
    print(appmsg_response.json())
    max_num = appmsg_response.json()['app_msg_cnt']
    '''每页至少有5条，获取文章总的页数，爬取时需要分页爬'''
    num = int(int(max_num) / 5)

    '''起始页begin参数，往后每页加5'''
    # #######
    begin = 0
    #
    '''开始循环发送请求，每次返回5条文章信息'''
    while num + 1 > 0:
        query_id_data = {
            'token': token,
            'lang': 'zh_CN',
            'f': 'json',
            'ajax': '1',
            'random': random.random(),
            'action': 'list_ex',
            'begin': '{}'.format(str(begin)),
            'count': '5',
            'query': '',
            'fakeid': fakeid,
            'type': '9'
        }
        print('正在翻页：--------------', begin)
        query_fakeid_response = session.get(
            appmsg_url,
            cookies=cookies,
            headers=header,
            params=query_id_data)
        time.sleep(5)
        fakeid_list = query_fakeid_response.json()['app_msg_list']
        # print(fakeid_list)
        min_createtime = wx_article_url.objects.filter(nickname = nickname).aggregate(Min('createtime'))
        # print(min_createtime)
        if min_createtime['createtime__min']:
            for item in fakeid_list:
                print(item)
                createtime = item['create_time']
                content_createtime = time.strftime('%Y-%m-%d %X', time.localtime(createtime))
                datetime_content_createtime = datetime.strptime(content_createtime, "%Y-%m-%d %H:%M:%S")
                datetime_content_createtime = timezone.make_aware(datetime_content_createtime, timezone.utc)
                if datetime_content_createtime < min_createtime['createtime__min']:
                    # updatetime = item['update_time']
                    # content_updatetime = time.strftime('%Y-%m-%d %X', time.localtime(updatetime))# 微信文章时间
                    # content_title = item['title']  # 微信文章标题
                    # content_link = item['link']  # 微信文章链接
                    # content_coverlink = item['cover']  # 微信文章图片链接
                    print(item)
                    try:
                        wx_article_url.objects.create(
                            nickname = nickname,
                            createtime = content_createtime,
                            url=item['link'],
                            title = item['title']
                        )
                    except :
                        text = item['title']
                        # 使用正则表达式提取中英文字符
                        # \w 匹配任何字母数字字符，相当于 [a-zA-Z0-9_]
                        # \u4e00-\u9fff 是中文字符的Unicode范围
                        pattern = r'[\w\u4e00-\u9fff]+'
                        # 找到所有匹配项
                        matches = re.findall(pattern, text)
                        # 将匹配项连接成一个字符串
                        result = ''.join(matches)
                        wx_article_url.objects.create(
                            nickname = nickname,
                            createtime = content_createtime,
                            url=item['link'],
                            title = result

                        )
        else:
            for item in fakeid_list:
                # print(item)
                createtime = item['create_time']
                # updatetime = item['update_time']
                content_createtime = time.strftime('%Y-%m-%d %X', time.localtime(createtime))
                # content_updatetime = time.strftime('%Y-%m-%d %X', time.localtime(updatetime))# 微信文章时间
                # content_title = item['title'] # 微信文章标题
                # content_link = item['link']# 微信文章链接
                # content_coverlink = item['cover']# 微信文章图片链接
                try:
                    wx_article_url.objects.create(
                        nickname=nickname,
                        createtime=content_createtime,
                        url=item['link'],
                        title=item['title']
                    )
                except :
                    text = item['title']
                    # 使用正则表达式提取中英文字符
                    # \w 匹配任何字母数字字符，相当于 [a-zA-Z0-9_]
                    # \u4e00-\u9fff 是中文字符的Unicode范围
                    pattern = r'[\w\u4e00-\u9fff]+'
                    # 找到所有匹配项
                    matches = re.findall(pattern, text)
                    # 将匹配项连接成一个字符串
                    result = ''.join(matches)
                    wx_article_url.objects.create(
                        nickname=nickname,
                        createtime=content_createtime,
                        url=item['link'],
                        title=result
                    )
        num -= 1
        begin = int(begin)
        begin += 5

        # if fakeid_list:
        #     # fileName = 爬取测试 + '.txt'
        #     # wxarticle=open(fileName, 'a', encoding='utf-8')
        #     for item in fakeid_list:
        #         # print(item)
        #         createtime = item['create_time']
        #         # updatetime = item['update_time']
        #         content_createtime = time.strftime('%Y-%m-%d %X', time.localtime(createtime))
        #         # content_updatetime = time.strftime('%Y-%m-%d %X', time.localtime(updatetime))# 微信文章时间
        #         content_title = item['title'].encode('utf-8')  # 微信文章标题
        #         content_link = item['link']# 微信文章链接
        #         content_coverlink = item['cover']# 微信文章图片链接
        #         wx_article_url.objects.create(
        #             nickname = nickname,
        #             createtime = content_createtime,
        #             title = content_title,
        #             url = content_link
        #         )
        #     num -= 1
        #     begin = int(begin)
        #     begin += 5

'''爬取该微信视频号信息列表并写入数据表'''
def wxh_get_video(query,token):
    video_url = 'https://mp.weixin.qq.com/cgi-bin/videosnap'
    header = {
        "HOST": "mp.weixin.qq.com",
        "User-Agent": \
            "Mozilla/\
            5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/\
            537.36 (KHTML, like Gecko) Chrome/\
            120.0.0.0 Safari/\
            537.36",
        "Accept": "* / *",
        "Accept - Encoding": "gzip, deflate, br, utf-8",
        "Accept - Language": "zh - CN, zh;q = 0.9",
        "X - Requested - With": "XMLHttpRequest"
    }
    from requests.packages import urllib3
    urllib3.disable_warnings()
    with open('wxcookie.txt', 'r', encoding='utf-8') as f:
        cookie = f.read()
        f.close()
    cookies = json.loads(cookie)
    session = requests.Session()
    session.keep_alive = False
    session.adapters.DEFAULT_RETRIES = 511
    time.sleep(1)
    query_videousername_data = {
        'action': 'search',
        'scene':'1',
        'buffer':'',
        'token': token,
        'lang': 'zh_CN',
        'f': 'json',
        'ajax': '1',
        'count': '1',
        'query': query,
    }
    query_videousername_response = session.get(
        video_url,
        cookies=cookies,
        headers=header,
        params=query_videousername_data)
    acct_list = query_videousername_response.json()['acct_list']
    username = acct_list[0]['username']
    # print(username)

    '''视频号下视频总数，该数据无法从接口直接获取，可指定数据量，
    该指定数据尽量取较大值，超出实际视频总数时不报错，低于时会造成数据爬取不完整'''
    video_num = 1000#指定数据
    query_video_data = {
        'action': 'get_feed_list',
        'username': username,
        'buffer':'',
        'count': video_num,
        'scene': '0',
        'token': token,
        'lang': 'zh_CN',
        'f': 'json',
        'ajax': '1',
    }
    query_video_response = session.get(
        video_url,
        cookies=cookies,
        headers=header,
        params=query_video_data)

    print(query_video_response.status_code)
    print(query_video_response.json()['list'])
    # video_list = query_video_response.json()['list']

if __name__ == '__main__':
    # 登录微信公众号，获取登录之后的cookies信息，并保存到本地文本中
    wechat_login()
    query = "闽院微图"
    print("开始爬取公众号：" + query)
    fake = wxh_get_fakeid(query)
    print(fake)











