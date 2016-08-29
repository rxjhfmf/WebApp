#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Frank Fu'

# 网页翻页信息类
class Page(object):

    def __init__(self, item_count, index=1, size=10):
        self.last = item_count // size + (1 if item_count % size > 0 else 0)  # 尾页
        self.index = min(index, self.last) if item_count > 0 else 1           # 当前页
        self.offset = size * (index - 1)    # 数据库查询用，偏移N个元素
        self.limit = size                   # 一页有多少个元素

# 设置合法的查询字符串参数
def set_valid_value(num_str, value=1):
    try:
        num = int(num_str)
    except ValueError:
        return value
    return num if num > 0 else value

# 检查字符串是否为空
def check_string(**kw):
    for field, string in kw.items():
        if not string or not string.strip():
            raise APIValueError(field, '%s cannot be empty.' % field)