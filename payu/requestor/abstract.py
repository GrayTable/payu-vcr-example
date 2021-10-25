from abc import ABC, abstractmethod

from ..spec import http

__all__ = ["AbstractRequestor"]


class AbstractRequestor(ABC):
    @abstractmethod
    def send_request(self, request: http.HTTPRequest) -> http.HTTPResponse:
        pass
