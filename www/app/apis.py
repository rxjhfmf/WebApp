#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Frank Fu'

import logging
from aiohttp import ClientSession, web

from app.filters import marked_filter as markdown_highlight
from app.frame import get, post
from app.frame.helper import Page, set_valid_value
from app.frame.errors import APIValueError, APIResourceNotFoundError
from app.models import Blog, Tag

# 取（博客、标签）表的条目
@get('/api/{table}')
async def api_get_items(table, *, page='1', size='10'):
    print("~~~~~~~~~~~~~~~")
    models = {'blogs': Blog, 'tags': Tag}
    num = await models[table].countRows()
    page = Page(num, set_valid_value(page), set_valid_value(size, 10))
    if num == 0:
        return dict(page=page, items=[])
    items = await models[table].findAll(orderBy='created_at desc', limit=(page.offset, page.limit + num % page.limit))
    return dict(page=page, items=items)


# 取某篇博客
@get('/api/{table}/{id}')
async def api_get_blog(table,id):
    models = {'blogs': Blog, 'tags': Tag}
    return await models[table].find(id)


# 创建新博客
@post('/api/blogs')
async def api_create_blog(request, *, name, summary, content):
    check_string(name=name, summary=summary, content=content)
    blog = Blog(user_id=request.__user__.id, user_name=request.__user__.name, user_image=request.__user__.image,
                name=name.strip(), summary=summary.strip(), content=content.strip())
    await blog.save()
    return blog


# 修改某篇博客
@post('/api/blogs/{id}')
async def api_update_blog(id, request, *, name, summary, content):
    check_string(name=name, summary=summary, content=content)
    blog = await Blog.find(id)
    blog.name = name.strip()
    blog.summary = summary.strip()
    blog.content = content.strip()
    await blog.update()
    return blog


# 删除博客
@post('/api/{table}/{id}/delete')
async def api_delete_item(table, id, request):
    models = {'users': User, 'blogs': Blog, 'comments': Comment, 'oauth': Oauth}
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