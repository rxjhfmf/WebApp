import asyncio
from models import Blog
import orm
import time

async def test(loop):
    await orm.create_pool(loop=loop, user='root', password='root',db='awesome')
    
    blog=Blog(name="1",tag="1",content="1",summary="1",created_at=time.time(),count=1)

    await blog.save()
    #await orm.close_pool()

loop = asyncio.get_event_loop()
loop.run_until_complete(test(loop))
#loop.close()