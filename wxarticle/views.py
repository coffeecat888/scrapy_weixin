"""
views.py 视图文件
"""
# -*- coding: utf-8 -*-
from django.shortcuts import render
from wxarticle.models import *
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.db.models import Q,F,Count
from pycrawl01 import *
import requests
import base64
from .form import *
from PIL import Image
from io import BytesIO
from bs4 import BeautifulSoup
from paddlenlp import Taskflow
import networkx as nx
import matplotlib.pyplot as plt
# Create your views here.
globnickname = '闽江学院'

'''测试用函数'''
def dbtest(request):
    image_datas = wx_id.objects.values('head_img')
    image_data = image_datas[1]['head_img']
    image_bydata = base64.b64encode(image_data).decode('utf-8')
    return render(request,'dbtest.html',{'image_bydata':image_bydata})

####################################################
'''管理平台主页面'''
def wx_main(request):
    return render(request,'wxmain.html')

'''用于收割数据的微信公众号登录'''
def login(request):
    wechat_login("linlimju@outlook.com","ssuu291388")
    return HttpResponse('完成cookie信息收集')

'''公众号运营主体类别信息'''
def wx_attrib_list(request):
    data = wx_attribution.objects.all()
    return render(request,'wxattrib.html',locals())

'''设置公众号运营主体类别信息'''
def wx_attrib_add(request):
    if not request.POST:
        return HttpResponse("禁止访问")
    else:
        wx_attrib = request.POST['textfield']
        if wx_attrib == '':
            return render(request, 'message.html', context={'message': '不得为空字符串','action_':'wx_attrib_list'})
        elif wx_attribution.objects.filter(wx_attribution = wx_attrib):
            return render(request, 'message.html', context={'message': '数据库中有该主体类型了','action_':'wx_attrib_list'})
        else:
            wx_attribution.objects.create(wx_attribution=wx_attrib)
            return render(request, 'message.html', context={'message': '主体类型添加成功','action_':'wx_attrib_list'})

'''登记公众号信息'''
def wx_list_add(request):
    wxlistadd = wxidform()
    return render(request, 'wxlistadd.html', locals())

'''收割微信公众号信息'''
def wx_name_query(request):
    if not request.POST:
        return HttpResponse("禁止访问")
    else:
        nickname = request.POST['nickname']
        wx_attribution = request.POST['wx_attribution_choices']
        if nickname == '':
            return render(request, 'message.html', context={'message': '不得为空字符串','action_':'wx_list'})
        elif wx_id.objects.filter(nickname = nickname):
            return render(request, 'message.html', context={'message': '数据库中有该公众号fakeid了','action_':'wx_list'})
        else:
            wx_idinfo = wxh_get_fakeid(nickname)
            if wx_idinfo[2] == nickname:#确定检索结果为该公众号
                round_head_img = wx_idinfo[5]
                image_data = requests.get(round_head_img).content
                wx_id.objects.create(
                    wx_attribution =wx_attribution,
                    fakeid = wx_idinfo[1],
                    nickname = wx_idinfo[2],
                    alias = wx_idinfo[3],
                    signature = wx_idinfo[4],
                    head_img = image_data
                    )
                image_path = 'e:\\djangoproject\\wxarticle\\wxidimage\\'+wx_idinfo[2]+'.png'
                with open(image_path, "wb") as file:
                    file.write(image_data)
                    file.close()
                return render(request, 'message.html', context={'message': '已添加入数据库中','action_':'wx_list'})
            else:
                return render(request, 'message.html', context={'message': '无此微信公众号','action_':'wx_list'})

'''收割的微信公众号信息展示'''
def wx_name_list(request):
    data = wx_id.objects.values('id','wx_attribution','fakeid','nickname','signature','alias')
    for datadic in data:
        imagepath = '/static/'+datadic['nickname'] + '.png'
        datadic.setdefault('imagepath',imagepath)
        count = wx_article_url.objects.filter(nickname=datadic['nickname']).count()
        datadic.setdefault('count',count)
    return render(request, 'wxlist.html', context={'data':data})

'''收割的微信公众号下的文章'''
def wx_article_crawl(request):
    fakeid = request.POST['submitfakeid']
    nickname = request.POST['submitnickname1']
    wxh_get_content(nickname,fakeid)
    return render(request, 'message.html', {'message': '已爬取完成该公众号文章！','action_':'wx_list'})

'''显示微信公众号下的文章元数据'''
def wx_article_list(request):
    global globnickname
    print(globnickname)
    nickname = request.GET.get('submitnickname2',globnickname)
    globnickname = nickname
    print(globnickname)
    # 获取所有文章记录
    articles = wx_article_url.objects.filter(nickname=nickname)
    # 每页显示20条记录
    per_page = 20
    # 创建Paginator对象
    paginator = Paginator(articles, per_page)
    # 获取当前页码，默认为1
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    # 将分页对象和文章列表传递给模板
    return render(request, 'wxartilist.html', {'nickname':nickname,'page_obj': page_obj})

'''统计并图谱化展示微信公众号信息'''
def wx_list_statistics(request):
    data = wx_id.objects.values('wx_attribution').annotate(Count('wx_attribution'))
    wx_list_statistics = list(data)
    print(wx_list_statistics)
    return render(request, 'wxliststatistics.html', {'wx_list_statistics':wx_list_statistics})

'''抽取微信公众号文章的实体信息'''
def wx_article_analyse(request):
    urls = list(wx_article_url.objects.values('url').filter(entity_analyse=False))
    schema_entity = ['人名', '组织', '课题', '奖励', '比赛']
    dict_entity = {'人名':'entity_name', '组织':'entity_organization', '课题':'entity_study', '奖励':'entity_award', '比赛':'entity_game'}
    ie_entity = Taskflow('information_extraction', schema=schema_entity, model='uie-base')
    for dict_url in urls:
        url = dict_url['url']
        response = requests.get(url)
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')
        article_content = soup.find('div', id='js_content')
        text_content = article_content.getText()
        print(f"正在解析数字资源{url}")
        entities = ie_entity(text_content)[0]
        for schema_entity_name in schema_entity:
            if schema_entity_name in entities:
                # print(f"{entity_name}：{entities[entity_name]}")
                entity_list = []
                for text in entities[schema_entity_name]:
                    entity_text = text['text']
                    if entity_text not in entity_list:
                        entity_list.append(entity_text)
                print(f"实体信息{dict_entity[schema_entity_name]}：{entity_list}")
                wx_article_url.objects.filter(url=url).update(**{dict_entity[schema_entity_name]:entity_list,'entity_analyse':True})
    return HttpResponse("解析完成")

def wx_article_plt(data):
    G = nx.DiGraph()
    # 遍历数据并添加节点和边
    for category, items in data.items():
        for item in items:
            text = item['text']
            start = item['start']
            end = item['end']
            probability = item['probability']
            relations = item.get('relations', {})
            # 添加节点
            G.add_node(text, label=text, start=start, end=end, probability=probability)
            # 添加关系边
            for relation_type, relation_items in relations.items():
                for relation_item in relation_items:
                    relation_text = relation_item['text']
                    # 添加关系边
                    G.add_edge(text, relation_text, relation=relation_type)
                # 使用matplotlib来绘制图
    pos = nx.spring_layout(G)  # 使用spring布局算法
    nx.draw_networkx_nodes(G, pos, node_size=1000, node_color='lightblue')
    nx.draw_networkx_edges(G, pos, alpha=0.5)
    nx.draw_networkx_labels(G, pos, font_size=16, font_family='sans-serif')
    # 显示图形
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    plt.axis('off')
    plt.savefig('fig01.png')
    plt.show()





