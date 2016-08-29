#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Frank Fu'


import re, time, json, logging, hashlib, base64, asyncio
from app.frame import get, post
from .models import  *
from app.frame.helper import Page, set_valid_value

def ch2utf(name):
    a=name.encode('utf-8',"s")
    return "".join(str(a).split("\\x"))[2:-1]

@get('/blog/{id}')
async def get_blog(id):
    blog = await Blog.find(id)
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

    str="a.jpg"
    photos=[
        Photo(name="name1",alt="alt1",title='title1',src=ch2utf("me.jpg")),
        Photo(name="name2",alt="alt2",title='title2',src=ch2utf("A_头像.jpg")),
    ]

    return{
    '__template__': 'photos.html',
    'photos':photos
    }

@get('/blogs')
async def get_blogs(request, *, tag='Python', page='1', size='5'):
    if not tag.endswith('"'):
        tag="\""+tag+"\""
    num = await Blog.countRows(where="position(? in `tag`)", args=[tag])
    page = Page(num, set_valid_value(page), set_valid_value(size, 10))
    tags=await Tag.findAll(orderBy="name")
    if num == 0:
        blogs = []
    else:
        blogs = await Blog.findAll("position(? in `tag`)", [tag], orderBy='created_at desc', limit=(page.offset, page.limit))

    return {
        '__template__': 'blogs.html',
        'blogs': blogs,
        'page': page,
        'tag': tag,
        'tags': tags
    }

@get('/about')
async def get_about(request):
    return {
        '__template__': 'aboutme.html',
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


# 创建博客
@get('/manage/blogs/create')
def manage_create_blog():
    return {
        '__template__': 'blog_edit.html'
    }


# 修改博客
@get('/manage/blogs/edit')
def manage_edit_blog():
    return {
        '__template__': 'blog_edit.html'
    }

# 创建标签
@get('/{template}/manage/tags/create')
def manage_create_blog():
    return {
        '__template__': 'tag_edit.html'
    }


# 修改标签
@get('/{template}/manage/tags/edit')
def manage_edit_blog():
    return {
        '__template__': 'tag_edit.html'
    }