#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Frank Fu'

import logging
from aiohttp import ClientSession, web

from app.filters import marked_filter as markdown_highlight
from app.frame import get, post
from app.frame.helper import Page, set_valid_value,check_string
from app.frame.errors import APIValueError, APIResourceNotFoundError
from app.models import Blog, Tag

# 取（博客、标签）表的条目
@get('/api/manage/{table}')
async def api_get_items(table, *, page='1', size='10'):
    models = {'blogs': Blog, 'tags': Tag}
    num = await models[table].countRows()
    page = Page(num, set_valid_value(page), set_valid_value(size, 10))
    if num == 0:
        return dict(page=page, items=[])
    items = await models[table].findAll(orderBy='created_at desc', limit=(page.offset, page.limit + num % page.limit))
    return dict(page=page, items=items)


# 取某篇博客
@get('/api/manage/{table}/{id}')
async def api_get_blog(table,id):
    models = {'blogs': Blog, 'tags': Tag}
    return await models[table].find(id)


# 创建新博客
@post('/api/manage/blogs')
async def api_create_blog(request, *, name, tag, summary, content):
    check_string(name=name, tag=tag, summary=summary, content=content)
    blog = Blog(name=name.strip(), tag=tag.strip(), summary=summary.strip(), content=content.strip())
    await blog.save()
    blogs=await Blog.findAll("name='%s'" % blog.name);
    
    return blogs[0]


# 修改某篇博客
@post('/api/manage/blogs/{id}')
async def api_update_blog(id, request, *, name, summary, content):
    check_string(name=name, summary=summary, content=content)
    blog = await Blog.find(id)
    blog.name = name.strip()
    blog.summary = summary.strip()
    blog.content = content.strip()
    await blog.update()
    return blog


# 删除博客
@post('/api/manage/{table}/{id}/delete')
async def api_delete_item(table, id, request):
    models = {'blogs': Blog, 'tags': Tag}
    item = await models[table].find(id)
    if item:
        await item.remove()
    else:
        logging.warn('id: %s not exist in %s' % (id, table))
    if table == 'blogs':
        comments = await Comment.findAll('blog_id = ?', [id])
        for comment in comments:
            await comment.remove()
    return dict(id=id)

@get('/api/test')
async def api_test():
    return "a"