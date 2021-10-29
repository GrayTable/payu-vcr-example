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

    access_token: Optional[str]
    token_type: Optional[str]
    expires_in: Optional[int]
    grant_type: Optional[str]

    @property
    def success(self):
        return all(
            [
                self.access_token is not None,
                self.token_type is not None,
                self.expires_in is not None,
                self.grant_type is not None,
            ]
        )


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
    redirectUri: Optional[str]
    orderId: Optional[str]
    extOrderId: Optional[str]

    @property
    def success(self) -> bool:
        return all(
            [
                self.status and self.status.statusCode == StatusCode.SUCCESS or False,
                self.redirectUri is not None,
                self.orderId is not None,
            ]
        )


class OrderCaptureOutput(BaseModel):
    """
    SEE: https://developers.payu.com/en/restapi.html#status_update
    """

    status: StatusOutput

    @property
    def success(self) -> bool:
        return self.status and self.status.statusCode == StatusCode.SUCCESS or False


class RefundCreateOutputRefund(BaseModel):
    """
    SEE: https://developers.payu.com/en/restapi.html#refunds_create
    """

    refundId: str
    extRefundId: str
    amount: str
    currencyCode: str
    description: str
    creationDateTime: str
    status: str
    statusDateTime: str


class RefundCreateOutput(BaseModel):
    """
    SEE: https://developers.payu.com/en/restapi.html#refunds_create
    """

    status: StatusOutput
    orderId: Optional[str]
    refund: Optional[RefundCreateOutputRefund]

    @property
    def success(self) -> bool:
        return all(
            [
                self.status and self.status.statusCode == StatusCode.SUCCESS or False,
                self.status is not None,
                self.refund is not None,
            ]
        )


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
    orders: Optional[List[OrderDetailOutputOrder]]

    @property
    def success(self) -> bool:
        return all(
            [
                self.status and self.status.statusCode == StatusCode.SUCCESS or False,
                self.orders is not None and len(self.orders) > 0,
            ]
        )


class OrderCancelOutput(BaseModel):
    """
    SEE: https://developers.payu.com/en/restapi.html#cancellation
    """

    status: StatusOutput
    orderId: str

    extOrderId: Optional[str]

    @property
    def success(self) -> bool:
        return self.status and self.status.statusCode == StatusCode.SUCCESS or False


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
