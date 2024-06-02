# import requests
# from bs4 import BeautifulSoup
# from paddlenlp import Taskflow
# from pprint import pprint
# import networkx as nx
# import matplotlib.pyplot as plt

# url = "https://mp.weixin.qq.com/s?__biz=MzkyOTMzMTM3OA==&mid=2247484862&idx=1&sn=bc80de74dabf533fb03fa8105a251628&chksm=c20a6463f57ded75c23b4952b0c6ea9f8b6770cc190ebb80b802aa44e47aef6d00f02d9c7912#rd"
url = "https://mp.weixin.qq.com/s?__biz=MzIwMDE4OTYxOA==&mid=2649385377&idx=1&sn=19c73771d57585c8de2cd9653b478348&chksm=8e9e3a7cb9e9b36a0b4759e24fe1910a6a1064e084149c461b010517de99c284af04d5370f98#rd"
# response = requests.get(url)
# html_content = response.text
# soup = BeautifulSoup(html_content, 'html.parser')
# # text_content = soup.get_text()
# article_content = soup.find('div', id='js_content')
# text_content = article_content.getText()
# print(text_content)
# # 关系抽取
# schemagx = {'事件': ['时间','人名','组织'],'课题':['时间','人名','组织'],'奖项':['时间','人名','组织'],'会议':['时间','人名','组织']}
# iegx = Taskflow('information_extraction', schema=schemagx, model='uie-base')
# data=iegx(text_content)[0]
# G = nx.DiGraph()
# # 遍历数据并添加节点和边
# for category, items in data.items():
#     for item in items:
#         text = item['text']
#         start = item['start']
#         end = item['end']
#         probability = item['probability']
#         relations = item.get('relations', {})
#         # 添加节点
#         G.add_node(text, label=text, start=start, end=end, probability=probability)
#         # 添加关系边
#         for relation_type, relation_items in relations.items():
#             for relation_item in relation_items:
#                 relation_text = relation_item['text']
#                 # 添加关系边
#                 G.add_edge(text, relation_text, relation=relation_type)
#             # 使用matplotlib来绘制图
# pos = nx.spring_layout(G)  # 使用spring布局算法
# nx.draw_networkx_nodes(G, pos, node_size=1000, node_color='lightblue')
# nx.draw_networkx_edges(G, pos, alpha=0.5)
# nx.draw_networkx_labels(G, pos, font_size=16, font_family='sans-serif')
# # 显示图形
# plt.rcParams['font.sans-serif'] = ['SimHei']
# plt.rcParams['axes.unicode_minus'] = False
# plt.axis('off')
# plt.savefig('fig01.png')
# plt.show()

# def wx_article_analyse(url):
#     schema_entity = ['时间', '人名', '地名', '事件', '组织', '课题', '奖励', '会议']
#     response = requests.get(url)
#     html_content = response.text
#     soup = BeautifulSoup(html_content, 'html.parser')
#     article_content = soup.find('div', id='js_content')
#     text_content = article_content.getText()
#     # 实体抽取
#     ie_entity = Taskflow('information_extraction', schema=schema_entity, model='uie-base')
#     entity = ie_entity(text_content)[0]
#     # 关系抽取
#     schema_relation = {'事件': ['时间','人名','组织'],'课题':['时间','人名','组织'],'奖励':['时间','人名','组织'],'会议':['时间','人名','组织']}
#     ie_relation = Taskflow('information_extraction', schema=schema_relation, model='uie-base')
#     relation = ie_relation(text_content)[0]
#     return entity,relation

# def wx_article_plt(ID,data):
#     G = nx.DiGraph()
#     # 遍历数据并添加节点和边
#     for category, items in data.items():
#         for item in items:
#             text = item['text']
#             start = item['start']
#             end = item['end']
#             probability = item['probability']
#             relations = item.get('relations', {})
#             # 添加节点
#             G.add_node(text, label=text, start=start, end=end, probability=probability)
#             # 添加关系边
#             for relation_type, relation_items in relations.items():
#                 for relation_item in relation_items:
#                     relation_text = relation_item['text']
#                     # 添加关系边
#                     G.add_edge(text, relation_text, relation=relation_type)
#                 # 使用matplotlib来绘制图
#     pos = nx.spring_layout(G)  # 使用spring布局算法
#     nx.draw_networkx_nodes(G, pos, node_size=1000, node_color='lightblue')
#     nx.draw_networkx_edges(G, pos, alpha=0.5)
#     nx.draw_networkx_labels(G, pos, font_size=16, font_family='sans-serif')
#     # 显示图形
#     plt.rcParams['font.sans-serif'] = ['SimHei']
#     plt.rcParams['axes.unicode_minus'] = False
#     plt.axis('off')
#     plt.savefig('./pltfig/'+str(ID)+'.png')
#     plt.show()

# def wx_article_analyse(url):
#     schema_entity = ['人名', '组织', '课题', '奖励', '比赛']
#     response = requests.get(url)
#     html_content = response.text
#     soup = BeautifulSoup(html_content, 'html.parser')
#     article_content = soup.find('div', id='js_content')
#     text_content = article_content.getText()
#     # 实体抽取
#     ie_entity = Taskflow('information_extraction', schema=schema_entity, model='uie-base')
#     entity = ie_entity(text_content)[0]
#     # # 关系抽取
#     # schema_relation = {'事件': ['时间','人名','组织'],'课题': ['时间','人名','组织'],'奖励':['时间','人名','组织'],'会议': ['时间','人名','组织']}
#     # ie_relation = Taskflow('information_extraction', schema=schema_relation, model='uie-base')
#     # relation = ie_relation(text_content)[0]
#     # print(entity)
#     # print('实体关系')
#     # print(relation)
#     return entity
#
# data=wx_article_analyse(url=url)
# k = ['人名', '组织', '课题', '奖励', '比赛']
# for kk in k:
#     if kk in data:
#         print(f"{kk}实体信息如下：{data[kk]}")


string = "['舒继武', 'Kostas Gouliamos', '傅高升', '习近平', '刘文静', '李晓滨']"
string = string[1:-1]
print(string)
print(string.split(','))















# data=wx_article_analyse(url)
# wx_article_plt('2',data[1])
# print(data[0]['时间'])
# print(data[0]['人名'])
# print(data[0]['地名'])
# print(data[0]['事件'])
# print(data[0]['组织'])
# print(data[0]['课题'])
# print(data[0]['奖励'])
# print(data[0]['会议'])
# print(data[1])

