#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Frank Fu'


import re, time, json, logging, hashlib, base64, asyncio
from app.frame import get, post
from .models import  *
from urllib import parse
from app.frame.helper import Page, set_valid_value
from markdown import markdown
import os

@get('/blog/{id}')
async def get_blog(id):
    blog = await Blog.find(id)
    blog.content=markdown(blog.content,['codehilite']);
    sid="blog"+str(blog.id)
    tags=await Tag.findAll(orderBy="name")
    return {
        '__template__': 'blog.html',
        'blog': blog,
        'sid':sid,
        'tags':tags
    }

@get('/')
def index():
    return{
    '__template__': 'index.html',
    }

@get('/photos')
async def get_photos(request):

    photos=[
        Photo(name="name1",alt="alt1",title='title1',src=parse.quote("me.jpg")),
        Photo(name="name2",alt="alt2",title='title2',src=parse.quote("A.jpg")),
    ]

    return{
    '__template__': 'photos.html',
    'photos':photos
    }

@get('/blogs')
async def get_blogs(request, *, tag='Python', page='1', size='5'):
    num = await Blog.countRows(where="position(? in `tag`)", args=[tag])
    page = Page(num, set_valid_value(page), set_valid_value(size, 10))
    tags=await Tag.findAll(orderBy="name")
    if num == 0:
        blogs = []
    else:
        blogs = await Blog.findAll("position(? in `tag`)", [tag], orderBy='created_at desc', limit=(page.offset, page.limit))
    
    for blog in blogs:
        blog.content=markdown(blog.content,['codehilite']);

    return {
        '__template__': 'blogs.html',
        'blogs': blogs,
        'page': page,
        'tag': tag,
        'tags': tags
    }

@get('/about')
async def get_about(request):
    path=os.path.abspath('.')
    fo = open('app/static/about.txt','rb')
    txt=fo.read()
    return {
        '__template__': 'aboutme.html',
        'txt':markdown(txt.decode("utf-8"),['codehilite'])
    }

# 管理页面
@get('/manage')
def manage():
    return 'redirect:/manage/blogs' 

# 管理标签、博客
@get('/manage/{table}')
def manage_table(table):
    return {
        '__template__': 'manage.html',
        'table': table,
    }

# 创建博客、标签
@get('/manage/{table}/create')
def manage_create(table):
    return {
        '__template__': '%s_edit.html' % (table)
    }

# 修改博客、标签
@get('/manage/{table}/edit')
def manage_edit(table):
    return {
        '__template__': '%s_edit.html' % (table)
    }

@get('/test')
def test():
    return{
    '__template__': 'test.html',
    }