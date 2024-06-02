"""
form.py 表单配置信息文件
"""
from django import forms
from .models import *
class wxidform(forms.Form):
    # 微信公众号中文名
    nickname = forms.CharField(max_length=30,label='请完整填写公众号中文名称')
    # 设置下拉框的值将表 wx_attribution 中的 wx_attribution 字段作为下拉框的值
    wx_attribution_choices = forms.ModelChoiceField(
        queryset=wx_attribution.objects.all().values_list('wx_attribution', flat=True),
        label='请选择微信公众号类型',  # 下拉框的标签
        empty_label="请选择" , # 可选：为下拉框添加一个空选项
    )