"""
admin.py 站点后台管理员配置信息文件
"""
from django.contrib import admin
from .models import *
# Register your models here.
admin.site.site_header = '闽江学院微信公众号资源管理系统后台数据管理'
admin.site.site_title = '闽江学院微信公众号资源管理系统后台数据管理'
# @admin.register(wx_article_url)
class wx_article_url_admin(admin.ModelAdmin):
    list_display = ['nickname','title','url']
admin.site.register(wx_article_url,wx_article_url_admin)
class wx_id_admin(admin.ModelAdmin):
    list_display = ['nickname','wx_attribution','fakeid']
admin.site.register(wx_id,wx_id_admin)