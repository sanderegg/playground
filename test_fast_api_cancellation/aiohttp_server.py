from aiohttp import web
import asyncio

from asyncio.exceptions import CancelledError

routes = web.RouteTableDef()

@routes.get('/')
async def hello(request):
    try:
        print("start handling request")
        await asyncio.sleep(14)
        print("slept a bit")
    except CancelledError:
        print("cancelled")
    finally:
        print("something happened")
    return web.Response(text="Hello, world")


app = web.Application()
app.add_routes(routes)
web.run_app(app)