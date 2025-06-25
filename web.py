import asyncio
from aiohttp import web, ClientSession, ClientTimeout

async def start_webserver():
    routes = web.RouteTableDef()

    @routes.get("/", allow_head=True)
    async def root_route_handler(request):
        res = {
            "status": "running",
        }
        return web.json_response(res)

    async def web_server():
        web_app = web.Application(client_max_size=30000000)
        web_app.add_routes(routes)
        return web_app

    app = web.AppRunner(await web_server())
    await app.setup()
    await web.TCPSite(app, "0.0.0.0", 8080).start()
    print("Web server started")

async def ping_server(url, sleep_time):
    while True:
        await asyncio.sleep(sleep_time)
        try:
            async with ClientSession(timeout=ClientTimeout(total=10)) as session:
                async with session.get(url) as resp:
                    print("Pinged server with response:", resp.status)
        except TimeoutError:
            print(f"Couldn't connect to the site {url}!")
        except Exception as e:
            print("Ping Error:", e)
