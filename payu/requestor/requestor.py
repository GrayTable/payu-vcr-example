from typing import Callable

import requests

from ..spec import http
from .abstract import AbstractRequestor

__all__ = ["Requestor"]


class Requestor(AbstractRequestor):
    def __get_request_function(self, method) -> Callable[..., requests.Response]:
        method_func_map = {
            http.HTTPMethod.POST: requests.post,
            http.HTTPMethod.PUT: requests.put,
            http.HTTPMethod.GET: requests.get,
            http.HTTPMethod.DELETE: requests.delete,
        }

        func = method_func_map.get(method)

        if not func:
            raise ValueError(f"Unknown request method {method}")

        return func

    def send_request(self, request: http.HTTPRequest) -> http.HTTPResponse:
        request_function = self.__get_request_function(request.method)
        request_kwargs = self.__prepare_request_kwargs(request)

        response = request_function(**request_kwargs)
        return http.HTTPResponse(status=response.status_code, data=response.json())

    def __prepare_request_kwargs(self, request: http.HTTPRequest):
        request_dict = request.dict()
        request_dict.pop("method")
        options = request_dict.pop("options") or {}

        if self.__is_json(request):
            request_dict["json"] = request_dict.pop("data")

        request_kwargs = {
            **request_dict,
            **options,
        }
        return request_kwargs

    def __is_json(self, request: http.HTTPRequest):
        return all(
            [
                request.headers.content_type == http.MIME_APPLICATION_JSON,
                isinstance(request.data, http.HTTPRequestData),
            ]
        )
