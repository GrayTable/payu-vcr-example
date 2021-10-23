from abc import ABC, abstractmethod
from typing import Any, Dict, TypeVar, Union

from .enums import RequestMethod
from .schema import (
    AuthorizeResponse,
    OrderCaptureResponse,
    OrderCreateRequest,
    OrderCreateResponse,
    RefundCreateRequest,
    RefundCreateResponse,
    SignedRequest,
)

T = TypeVar("T")
DictOrRequest = Union[T, Dict[str, Any]]
DictStrAny = Dict[str, Any]


class AbstractPayUClient:
    @abstractmethod
    def authorize(self) -> AuthorizeResponse:
        pass

    @abstractmethod
    def create_order(
        self, data: DictOrRequest[OrderCreateRequest]
    ) -> OrderCreateResponse:
        pass

    @abstractmethod
    def capture_order(self, order_id: str) -> OrderCaptureResponse:
        pass

    @abstractmethod
    def create_refund(
        self, order_id: str, data: DictOrRequest[RefundCreateRequest]
    ) -> RefundCreateResponse:
        pass


class AbstractRequestor(ABC):
    @abstractmethod
    def send_unsigned_request(
        self,
        method: RequestMethod,
        url: str,
        **options,
    ):
        pass

    @abstractmethod
    def send_signed_request(
        self,
        method: RequestMethod,
        url: str,
        signed_request: SignedRequest,
        **options,
    ):
        pass
