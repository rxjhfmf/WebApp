import re, time, json, logging, hashlib, base64, asyncio
from coroweb import get, post
from models import  Blog,Photo,PageModel
import orm
from config import configs


async def init(loop):
    await orm.create_pool(loop=loop, host=configs.db.host, port=configs.db.port, user=configs.db.user, password=configs.db.password, db=configs.db.db)

    pages= await PageModel.findAll(where='name=?',args='about')


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(init(loop))

    
