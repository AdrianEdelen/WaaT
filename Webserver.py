from aiohttp import web
import logging

class Webserver:
    def __init__(self, host, port) -> None:
        self.host = host
        self.port = port
        self.app = web.Application()
        self.app['websockets'] = []
        self.setup_routes()
        self.runner = web.AppRunner(self.app)
        self.runner.setup()
        self.site = web.TCPSite(self.runner, self.host, self.port)
        self.site.start()        
        pass

    async def root_handler(self):
        raise web.HTTPFound('/static/index.html')
    
    async def audit_handler(request):
        return web.FileResponse('./static/audit.html')
    
    #TODO: this is for the message auditor
    async def fetch_next_message(request):
        pass

    #TODO: this is for audit as well, probably can go
    async def process_response(request):
        data = await request.json()
        action = data.get('action')
        return web.json_response({"status": "success"})

    def setup_routes(self):
        self.app.router.add_get('/', root_handler)
        self.app.router.add_get('/audit', audit_handler)
        self.app.router.add_get('/audit/next', fetch_next_message)
        self.app.router.add_post('/audit/action', process_response)
        self.app.router.add_static('/static/', path='static', name='static')
        self.app.router.add_get('/story', handle_story)
        self.app.router.add_get('/ws', websocket_handler)
