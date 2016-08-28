#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Frank Fu'

import asyncio
from app import create_server

if __name__ == '__main__':
    # 创建一个异步事件回路实例
    loop = asyncio.get_event_loop()
    # 创建一个服务器实例放入到异步事件回路
    loop.run_until_complete(create_server(loop))
    # 异步事件回路永久运行
    loop.run_forever()