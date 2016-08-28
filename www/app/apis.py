#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Frank Fu'

import logging
from aiohttp import ClientSession, web

from app.filters import marked_filter as markdown_highlight
from app.frame import get, post
from app.frame.helper import Page 
from app.frame.errors import APIValueError, APIResourceNotFoundError
from app.models import Blog

@post('/api/blogs')
async def api_create_blog(request, *, name, summary, content,tag):
    check_admin(request)
    if not name or not name.strip():
        raise APIValueError('name', 'name cannot be empty.')
    if not summary or not summary.strip():
        raise APIValueError('summary', 'summary cannot be empty.')
    if not content or not content.strip():
        raise APIValueError('content', 'content cannot be empty.')
    blog = Blog(name=name.strip(), summary=summary.strip(), content=content.strip(),tag=tag.strip())
    await blog.save()
    return blog