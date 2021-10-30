from typing import Any, List, Literal, Optional

from pydantic.main import BaseModel

from .enums import OrderStatus, StatusCode

__all__ = [
    "AuthorizeOutput",
    "StatusOutput",
    "OrderCreateOutput",
    "OrderCaptureOutput",
    "RefundCreateOutput",
    "OrderDetailOutput",
]


class AuthorizeOutput(BaseModel):
    """
    SEE: https://developers.payu.com/en/restapi.html#references_api_signature
    """

    access_token: str
    token_type: str
    expires_in: int
    grant_type: str


class StatusOutput(BaseModel):
    """
    SEE: https://developers.payu.com/en/restapi.html#references_statuses
    """

    statusCode: StatusCode
    statusDesc: Optional[str]
    codeLiteral: Optional[str]
    severity: Optional[str]
    code: Optional[str]


class OrderCreateOutput(BaseModel):
    """
    SEE: https://developers.payu.com/en/restapi.html#creating_new_order
    """

    status: StatusOutput
    redirectUri: str
    orderId: str
    extOrderId: Optional[str]


class OrderCaptureOutput(BaseModel):
    """
    SEE: https://developers.payu.com/en/restapi.html#status_update
    """

    status: StatusOutput


class RefundOutput(BaseModel):
    """
    SEE: https://developers.payu.com/en/restapi.html#refunds_create
    SEE: https://developers.payu.com/en/restapi.html#refunds_retrieve
    """

    refundId: str
    extRefundId: str
    amount: str
    currencyCode: str
    description: str
    creationDateTime: str
    status: str
    statusDateTime: Optional[str]


class RefundCreateOutput(BaseModel):
    """
    SEE: https://developers.payu.com/en/restapi.html#refunds_create
    """

    status: StatusOutput
    orderId: str
    refund: RefundOutput


class OrderDetailOutputProduct(BaseModel):
    """
    SEE: https://developers.payu.com/en/restapi.html#order_data_retrieve
    """

    name: str
    unitPrice: str
    quantity: str


class OrderDetailOutputOrder(BaseModel):
    """
    SEE: https://developers.payu.com/en/restapi.html#order_data_retrieve
    """

    orderId: str
    extOrderId: Optional[str]
    orderCreateDate: str
    notifyUrl: Optional[str]
    customerIp: str
    merchantPosId: str
    description: Optional[str]
    currencyCode: str
    totalAmount: str
    status: OrderStatus
    products: List[OrderDetailOutputProduct]


class OrderDetailOutput(BaseModel):
    """
    SEE: https://developers.payu.com/en/restapi.html#order_data_retrieve
    """

    status: StatusOutput
    orders: List[OrderDetailOutputOrder]


class OrderCancelOutput(BaseModel):
    """
    SEE: https://developers.payu.com/en/restapi.html#cancellation
    """

    status: StatusOutput
    orderId: str
    extOrderId: Optional[str]


class PayMethodsOutputPBL(BaseModel):
    """
    SEE: https://developers.payu.com/en/restapi.html#Transparent_retrieve
    """

    value: str
    name: str
    brandImageUrl: str
    status: Literal["ENABLED", "DISABLED"]
    minAmount: int
    maxAmount: int


class PayMethodsOutput(BaseModel):
    """
    SEE: https://developers.payu.com/en/restapi.html#Transparent_retrieve
    """

    payByLinks: List[PayMethodsOutputPBL]
    cardTokens: List[Any]
    pexTokens: List[Any]


class RefundsOutput(BaseModel):
    """
    SEE: https://developers.payu.com/en/restapi.html#refunds_retrieve
    """

    refunds: List[RefundOutput]
