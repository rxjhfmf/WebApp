#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Frank Fu'


import re, time, json, logging, hashlib, base64, asyncio
from app.frame import get, post
from .models import  Blog,Photo,PageModel

def tag2htmlstr(tag):
    b=tag.split(',')
    c=[]
    for x in b:
        x="\""+x+"\""
        c.append(x)
    return ",".join(c)

def ch2utf(name):
    a=name.encode('utf-8',"s")
    return "".join(str(a).split("\\x"))[2:-1]

@get('/blog/{id}')
async def get_blog(id):
    blog = await Blog.find(id)
    sid="blog"+str(blog.id)
    return {
        '__template__': 'blog.html',
        'blog': blog,
        'sid':sid
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
async def get_blogs(request):
    blogs = await Blog.findAll(orderBy="created_at desc",limit=5)
    for blog in blogs:
        blog.tag= tag2htmlstr(blog.tag)
    tags=["Python","C#"]

    return {
        '__template__': 'blogs.html',
        'blogs': blogs,
        'tags':tags
    }

@get('/about')
async def get_about(request):
    return {
        '__template__': 'aboutme.html',
    }

@get('/api/blogs/{id}')
def api_get_blog(*, id):
    blog = Blog.find(id)
    return blog
