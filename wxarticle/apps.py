"""
apps.py 应用程序配置信息文件
"""
from django.apps import AppConfig
class IndexConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'wxarticle'
