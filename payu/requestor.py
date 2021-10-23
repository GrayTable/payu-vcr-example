from .abstract import AbstractRequestor
from .enums import RequestMethod
from .schema.requests import SignedRequest

import requests


class Requestor(AbstractRequestor):
    def __get_request_function(self, method):
        method_func_map = {
            RequestMethod.POST: requests.post,
            RequestMethod.PUT: requests.put,
            RequestMethod.GET: requests.get,
        }

        func = method_func_map.get(method)

        if not func:
            raise ValueError(f"Unknown request method {method}")

        return func

    def send_unsigned_request(self, method: RequestMethod, url: str, **options):
        request_func = self.__get_request_function(method)
        return request_func(url, **options)

    def send_signed_request(
        self,
        method: RequestMethod,
        url: str,
        signed_request: SignedRequest,
        **options,
    ):
        return self.send_unsigned_request(
            method=method,
            url=url,
            headers=signed_request.headers.dict(),
            json=signed_request.data and signed_request.data.dict() or None,
            **options,
        )
