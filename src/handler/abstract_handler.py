from abc import abstractmethod
from handler.handler import *


class AbstractHandler(Handler):

    _next_handler: Handler = None

    def set_next(self, handler: Handler) -> Handler:
        self._next_handler = handler
        return handler
    
    @abstractmethod
    def handle(self, request: Any) -> Any:
        if self._next_handler:
            return self._next_handler.handle(request)
        
        return None
        