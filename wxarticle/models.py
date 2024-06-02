"""
models.py 数据库模型文件
"""
# Create your models here.
from django.db import models
class wx_id(models.Model):
    # 微信公众号归属
    wx_attribution = models.CharField(max_length=20,default='null',null=True)
    # 微信公众号fakeid
    fakeid = models.CharField(max_length=30,default='null',null=True)
    # 微信公众号中文
    nickname = models.CharField(max_length=30,default='null',null=True)
    # 微信公众号英文
    alias = models.CharField(max_length=30,default='null',null=True)
    # 微信公众号中文简介
    signature = models.CharField(max_length=300,default='null',null=True)
    # 微信公众号图标
    head_img = models.BinaryField(null=True)
    # round_head_img = models.CharField(max_length=200,default='null')

class wx_attribution(models.Model):
    # 微信公众号归属
    wx_attribution = models.CharField(max_length=20,default='null',null=True)

class wx_article_url(models.Model):
    # 微信公众号中文
    nickname = models.CharField(max_length=30,default='null',null=True)
    # 微信公众号文章创建时间
    createtime = models.DateTimeField()
    # 微信公众号文章标题
    title = models.TextField(default='null')
    # 微信公众号文章链接
    url = models.CharField(max_length=300,default='null')
    # 是否完成数字资源实体解析
    entity_analyse = models.BooleanField(default=False)
    # 数字资源中五个维度的实体信息
    # 人名
    entity_name = models.TextField(default='null')
    # 组织
    entity_organization = models.TextField(default='null')
    # 课题
    entity_study = models.TextField(default='null')
    # 奖励
    entity_award = models.TextField(default='null')
    # 比赛
    entity_game = models.TextField(default='null')









