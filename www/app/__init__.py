#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Frank Fu'

import logging
import os
from aiohttp import web
from jinja2 import Environment, FileSystemLoader

from .frame import add_routes, add_static
from .frame.orm import create_pool
from .factorys import logger_factory, data_factory, response_factory
from .filters import datetime_filter, marked_filter
from config import db_config

logging.basicConfig(level=logging.INFO)

def init_jinja2(app, **kw):
    logging.info('init jinja2...')
    options = dict(
        autoescape = kw.get('autoescape', True),
        block_start_string = kw.get('block_start_string', '{%'),
        block_end_string = kw.get('block_end_string', '%}'),
        variable_start_string = kw.get('variable_start_string', '{{'),
        variable_end_string = kw.get('variable_end_string', '}}'),
        auto_reload = kw.get('auto_reload', True)
    )
    path = kw.get('path', None)
    if path is None:
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
    logging.info('set jinja2 template path: %s' % path)
    env = Environment(loader=FileSystemLoader(path), **options)
    filters = kw.get('filters', None)
    if filters is not None:
        for name, f in filters.items():
            env.filters[name] = f
    app['__templating__'] = env

async def create_server(loop):
    await create_pool(loop=loop, host=db_config.host, port=db_config.port, user=db_config.user, password=db_config.password, db=db_config.db)
    app = web.Application(loop=loop, middlewares=[
        logger_factory, response_factory
    ])
    init_jinja2(app, filters=dict(datetime=datetime_filter))
    add_routes(app, 'app.routes')
    add_routes(app, 'app.apis')
    add_static(app)
    srv = await loop.create_server(app.make_handler(), '0.0.0.0', 9000)
    logging.info('server started at http://127.0.0.1:9000...')
    return srv