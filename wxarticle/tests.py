from django.test import TestCase

# Create your tests here.

import requests
from bs4 import BeautifulSoup
from paddlenlp import Taskflow
from wxarticle.models import *


# def wx_article_entity(url):
#     schema_entity = ['人名', '组织', '课题', '奖励', '比赛']
#     dict_entity = {'人名':'entity_name', '组织':'entity_organization', '课题':'entity_study', '奖励':'entity_award', '比赛':'entity_game'}
#     response = requests.get(url)
#     html_content = response.text
#     soup = BeautifulSoup(html_content, 'html.parser')
#     article_content = soup.find('div', id='js_content')
#     text_content = article_content.getText()
#     # 实体抽取
#     ie_entity = Taskflow('information_extraction', schema=schema_entity, model='uie-base')
#     print(f"正在解析数字资源{url}")
#     entities = ie_entity(text_content)[0]
#     for schema_entity_name in schema_entity:
#         if schema_entity_name in entities:
#             # print(f"{entity_name}：{entities[entity_name]}")
#             entity_list = []
#             for text in entities[schema_entity_name]:
#                 entity_text = text['text']
#                 if entity_text not in entity_list:
#                     entity_list.append(entity_text)
#             print(f"实体信息{dict_entity[schema_entity_name]}：{entity_list}")
#     return
# url="https://mp.weixin.qq.com/s?__biz=MzIwMDE4OTYxOA==&mid=2649385771&idx=1&sn=f1a69197f8c94aaa243c0dfa5c209c46&chksm=8e9e38f6b9e9b1e0fffea03aecfd4c43a0bf9debcdd5f2e9eca61b14bce4ed2792e6e51100d7#rd"
# entities = wx_article_entity(url=url)


# def wx_article_analyse(request):
#     urls = wx_article_url.objects.values('url').filter(entity_analyse=False)['url']
#     print(urls)

    # schema_entity = ['人名', '组织', '课题', '奖励', '比赛']
    # dict_entity = {'人名':'entity_name', '组织':'entity_organization', '课题':'entity_study', '奖励':'entity_award', '比赛':'entity_game'}
    # response = requests.get(url)
    # html_content = response.text
    # soup = BeautifulSoup(html_content, 'html.parser')
    # article_content = soup.find('div', id='js_content')
    # text_content = article_content.getText()
    # # 实体抽取
    # ie_entity = Taskflow('information_extraction', schema=schema_entity, model='uie-base')
    # print(f"正在解析数字资源{url}")
    # entities = ie_entity(text_content)[0]
    # for schema_entity_name in schema_entity:
    #     if schema_entity_name in entities:
    #         # print(f"{entity_name}：{entities[entity_name]}")
    #         entity_list = []
    #         for text in entities[schema_entity_name]:
    #             entity_text = text['text']
    #             if entity_text not in entity_list:
    #                 entity_list.append(entity_text)
    #         print(f"实体信息{dict_entity[schema_entity_name]}：{entity_list}")
    # return


urls = wx_article_url.objects.values('url').filter(entity_analyse=False)['url']

print(urls)

