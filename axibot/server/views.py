import logging

from aiohttp import web
import aiohttp_themes

from . import handlers
from .state import State

log = logging.getLogger(__name__)


@aiohttp_themes.template('index.html')
async def index(request):
    return {'text': 'Hello World!'}


async def upload(request):
    app = request.app
    assert app['state'] == State.idle

    data = await request.post()
    upload = data['file']
    log.info("Received uploaded file: %s", upload.filename)

    try:
        handlers.set_document(app, upload.file)
    except Exception as e:
        return web.Response(text='failure: %s' % e, status=500)

    handlers.notify_of_new_document(app)
    return web.Response(text='ok')


async def document(request):
    app = request.app
    if app['document']:
        return web.Response(body=app['document'],
                            headers={'Cache-Control': 'no-store'},
                            content_type='image/svg+xml')
    else:
        return web.Response(status=404)
