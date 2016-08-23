#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Frank Fu'

' url handlers '

import re, time, json, logging, hashlib, base64, asyncio
from coroweb import get, post
from models import  Blog

@get('/api/blogs/{id}')
def api_get_blog(*, id):
    blog = yield from Blog.find(id)
    return blog

@get('/')
async def index(request):
    
    blog=Blog(name="1",tag="1",content="1",summary="1",created_at=time.time(),count=1)

    await blog.save()

    summary = 'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.'
    blogs = [
        Blog(id='1', name='Test Blog',tag="test",content="I'm a teacher", summary=summary, created_at=time.time()-120,count=1),
        Blog(id='2', name='Something New',tag="test",content="I'm a coder", summary=summary, created_at=time.time()-3600,count=2),
        Blog(id='3', name='Learn Swift',tag="test",content="I'm a master", summary=summary, created_at=time.time()-7200,count=3)
    ]
    return {
        '__template__': 'blogs.html',
        'blogs': blogs
    }
