from enum import Enum
from typing import Any, Dict, Optional, Union

from pydantic import BaseModel, Field

__all__ = [
    "HTTPHeaders",
    "HTTPMethod",
    "HTTPRequest",
    "HTTPRequestData",
    "HTTPResponse",
    "HTTPStatus",
    "MIME_APPLICATION_JSON",
    "SignedHTTPHeaders",
]


MIME_APPLICATION_JSON = "application/json"


class HTTPStatus(int, Enum):
    OK = 200
    CREATED = 201
    FOUND = 302
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    REQUEST_TIMEOUT = 408
    INTERNAL_SERVER_ERROR = 500
    SERVICE_UNAVAILABLE = 503


class HTTPMethod(str, Enum):
    POST = "POST"
    PUT = "PUT"
    GET = "GET"


class HTTPHeaders(BaseModel):
    content_type: str = Field("application/x-www-form-urlencoded")


class SignedHTTPHeaders(HTTPHeaders):
    content_type: str = Field(MIME_APPLICATION_JSON)
    authorization: str


class HTTPResponse(BaseModel):
    status: HTTPStatus
    data: Dict[str, Any]


class HTTPRequestData(BaseModel):
    pass


class HTTPRequest(BaseModel):
    method: HTTPMethod
    headers: HTTPHeaders = HTTPHeaders()
    url: str
    data: Union[HTTPRequestData, str, None] = Field(None, description="Request Data")
    params: Optional[Dict[str, Any]] = Field(None)
    allow_redirects: bool = Field(False)
    options: Optional[Dict[str, Any]] = Field(None)
