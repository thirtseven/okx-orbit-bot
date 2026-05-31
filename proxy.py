#!/usr/bin/env python3
import asyncio
import aiohttp
from aiohttp import web

TARGET = "http://127.0.0.1:8081"

async def proxy_handler(request):
    try:
        async with aiohttp.ClientSession() as session:
            url = f"{TARGET}{request.path}"
            if request.query_string:
                url += f"?{request.query_string}"
            
            async with session.request(
                method=request.method,
                url=url,
                headers={k: v for k, v in request.headers.items() if k.lower() != 'host'},
                data=await request.read(),
                timeout=aiohttp.ClientTimeout(total=60)
            ) as resp:
                body = await resp.read()
                return web.Response(
                    body=body,
                    status=resp.status,
                    headers={k: v for k, v in resp.headers.items() if k.lower() not in ('transfer-encoding', 'content-encoding')}
                )
    except Exception as e:
        return web.Response(text=f"Proxy Error: {str(e)}", status=502)

app = web.Application()
app.router.add_route('*', '/{path_info:.*}', proxy_handler)

if __name__ == "__main__":
    web.run_app(app, host='0.0.0.0', port=8082)
