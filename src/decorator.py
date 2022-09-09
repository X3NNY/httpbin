from utils import get_current_app
from tornado.web import RequestHandler
from settings import host_exp
import functools
from typing import Callable, Optional, Awaitable

class register_handler:
    def __init__(self, route: str, host: str = host_exp):
        self.route = route
        self.host = host

    def __call__(self, handler: RequestHandler) -> RequestHandler:
        return self.register(handler)

    def register(self, handler: RequestHandler) -> RequestHandler:
        def add_register(key: str, value: RequestHandler) -> RequestHandler:
            app = get_current_app()
            app.add_handlers(self.host, [(f'{key}', value)])
            return value
        return add_register(self.route, handler)


def authenticated(
    method: Callable[..., Optional[Awaitable[None]]]
) -> Callable[..., Optional[Awaitable[None]]]:
    @functools.wraps(method)
    def wrapper(  # type: ignore
        self: RequestHandler, *args, **kwargs
    ) -> Optional[Awaitable[None]]:
        if not self.current_user:
            if self.request.method in ("GET", "HEAD"):
                self.finish({'code': 403, 'data': None})
                return None
        return method(self, *args, **kwargs)
    return wrapper
