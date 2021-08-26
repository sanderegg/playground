from typing import final
from fastapi import FastAPI, Response
from fastapi.exceptions import WebSocketRequestValidationError
from starlette.requests import ClientDisconnect, Request

app = FastAPI()

import asyncio
from asyncio import CancelledError, Task


async def cancel_request_if_client_disconnected(request: Request, task: Task) -> bool:
    try:
        while True:
            if await request.is_disconnected():
                print("client disconnected, cancel the request now!")
                task.cancel()
                break
            await asyncio.sleep(0.5)
    except CancelledError:
        print("auto cancel task cancelled...")

from fastapi import HTTPException


# @app.middleware("http")
# async def auto_cancel_task_middleware(request: Request, call_next):
#     print("middleware calling next")
#     try:
#         # import pdb; pdb.set_trace()
#         request_task = asyncio.ensure_future(call_next(request))
#         auto_cancel_task = asyncio.ensure_future(cancel_request_if_client_disconnected(request, request_task))
#         try:
#             response = await request_task
#         except CancelledError:
#             print("request was cancelled")
#             return Response("Oh No!", status_code=499)
#         print("middleware completed")
#     finally:
#         auto_cancel_task.cancel()
#     return response


from functools import wraps


def cancellable_request(func):
    @wraps(func)
    async def decorator(request: Request, *args, **kwargs) -> Response:
        request_task = asyncio.ensure_future(func(request, *args, **kwargs))
        auto_cancel_task = asyncio.ensure_future(cancel_request_if_client_disconnected(request, request_task))
        try:
            return await request_task
        except CancelledError:
            print("request was cancelled")
            return Response("Oh No!", status_code=499)
        finally:
            auto_cancel_task.cancel()
    return decorator


@app.get("/")
@cancellable_request
async def root(request: Request):
    try:
        # import pdb; pdb.set_trace()
        print("start handling request")
        await asyncio.sleep(5)
        print("slept a bit")
    except CancelledError:
        print("the request IS cancelled")
    finally:        
        print("completed request and request is diconnected:", await request.is_disconnected())
    return {"message": "Hello World"}
