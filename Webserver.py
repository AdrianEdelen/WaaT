from aiohttp import web
import logging

class Webserver:
    def __init__(self, host, port) -> None:
        self.logger = logging.getLogger(__name__)
        self.host = host
        self.port = port
        self.app = web.Application()
        self.app['websockets'] = []
        self.setup_routes()
        self.Started = False

    async def start(self):
        self.logger.debug(f"Starting Webserver")
        self.runner = web.AppRunner(self.app)
        await self.runner.setup()
        self.logger.debug(f"Setup Runner")
        self.site = web.TCPSite(self.runner, self.host, self.port)
        self.site.start()        
        self.logger.debug(f"Site Started")
        self.Started = True


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

    async def handle_story(request):
        words_with_details = get_all_words_detailed()
        return web.json_response(words_with_details)
        story = ' '.join(words)
        return web.FileResponse('index.html')
        return web.Response(text=story, content_type='text/html')
    
    async def websocket_handler(request):
        ws = web.WebSocketResponse()
        await ws.prepare(request)

        global websockets
        websockets.append(ws)
        try:
            async for msg in ws:
                # Handle incoming messages if necessary
                pass
        finally:
            websockets.remove(ws)

        return ws

    def setup_routes(self):
        self.app.router.add_get('/', self.root_handler)
        self.app.router.add_get('/audit', self.audit_handler)
        self.app.router.add_get('/audit/next', self.fetch_next_message)
        self.app.router.add_post('/audit/action', self.process_response)
        self.app.router.add_get('/story', self.handle_story)
        self.app.router.add_get('/ws', self.websocket_handler)
        self.app.router.add_static('/static/', path='static', name='static')
