from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel, Field

from .enums import OrderStatus
from .http import HTTPRequestData

__all__ = [
    "AuthorizeInput",
    "OrderCreateInput",
    "OrderCaptureInput",
    "RefundCreateInput",
]


class AuthorizeInput(HTTPRequestData):
    """
    SEE: https://developers.payu.com/en/restapi.html#references_api_signature
    """

    grant_type: str
    client_id: int
    client_secret: str


class OrderCreateInputBuyer(BaseModel):
    """
    SEE: https://developers.payu.com/en/restapi.html#creating_new_order_api
    """

    email: str
    phone: str
    firstName: str
    lastName: str
    language: str


class OrderCreateInputPayMethods(BaseModel):
    """
    SEE: https://developers.payu.com/en/restapi.html#transparent
    """

    payMethod: Dict[str, Any]


class OrderCreateInputProduct(BaseModel):
    """
    SEE: https://developers.payu.com/en/restapi.html#creating_new_order_api
    """

    name: str
    unitPrice: str
    quantity: str


class OrderCreateInput(HTTPRequestData):
    """
    SEE: https://developers.payu.com/en/restapi.html#creating_new_order_api
    SEE: https://developers.payu.com/en/restapi.html#transparent
    """

    merchantPosId: str
    description: str
    currencyCode: Literal["PLN"]
    totalAmount: str
    customerIp: str = "127.0.0.1"
    notifyUrl: Optional[str]
    buyer: Optional[OrderCreateInputBuyer]
    products: List[OrderCreateInputProduct]
    payMethods: Optional[OrderCreateInputPayMethods]


class OrderCaptureInput(HTTPRequestData):
    """
    https://developers.payu.com/en/restapi.html#status_update
    """

    orderId: str
    orderStatus: Literal[OrderStatus.COMPLETED]


class RefundCreateInputRefund(BaseModel):
    """
    SEE: https://developers.payu.com/en/restapi.html#refunds_create
    """

    description: str
    amount: Optional[int] = Field(
        None, description="To issue a full refund do not pass this value"
    )


class RefundCreateInput(HTTPRequestData):
    """
    SEE: https://developers.payu.com/en/restapi.html#refunds_create
    """

    refund: RefundCreateInputRefund
