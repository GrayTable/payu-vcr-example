from abc import ABC, abstractmethod
from typing import Any, Dict, TypeVar, Union

from ..spec import inputs, outputs

T = TypeVar("T")
DictOrInput = Union[T, Dict[str, Any]]


class AbstractPayUClient(ABC):
    @abstractmethod
    def authorize(self) -> outputs.AuthorizeOutput:
        pass

    @abstractmethod
    def get_order(self, order_id: str) -> outputs.OrderDetailOutput:
        pass

    @abstractmethod
    def create_order(
        self, data: DictOrInput[inputs.OrderCreateInput]
    ) -> outputs.OrderCreateOutput:
        pass

    @abstractmethod
    def capture_order(self, order_id: str) -> outputs.OrderCaptureOutput:
        pass

    @abstractmethod
    def create_refund(
        self, order_id: str, data: DictOrInput[inputs.RefundCreateInput]
    ) -> outputs.RefundCreateOutput:
        pass
