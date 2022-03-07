import uvicorn

from conf.settings import settings

uvicorn.run(
    'univer_api.app:app',
    host=settings.server_host,
    port=settings.server_port,
    reload=settings.debug,
    debug=settings.debug,
)
