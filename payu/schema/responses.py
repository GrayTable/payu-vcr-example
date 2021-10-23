from typing import List, Optional

from pydantic.main import BaseModel

from ..enums import OrderStatus, StatusCode


class AuthorizeResponse(BaseModel):
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


class StatusResponse(BaseModel):
    """
    SEE: https://developers.payu.com/en/restapi.html#references_statuses
    """

    statusCode: StatusCode
    statusDesc: Optional[str]
    codeLiteral: Optional[str]
    severity: Optional[str]
    code: Optional[str]


class OrderCreateResponse(BaseModel):
    """
    SEE: https://developers.payu.com/en/restapi.html#creating_new_order
    """

    status: StatusResponse
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


class OrderCaptureResponse(BaseModel):
    """
    SEE: https://developers.payu.com/en/restapi.html#status_update
    """

    status: StatusResponse

    @property
    def success(self) -> bool:
        return self.status and self.status.statusCode == StatusCode.SUCCESS or False


class RefundCreateResponseRefund(BaseModel):
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


class RefundCreateResponse(BaseModel):
    """
    SEE: https://developers.payu.com/en/restapi.html#refunds_create
    """

    status: StatusResponse
    orderId: Optional[str]
    refund: Optional[RefundCreateResponseRefund]

    @property
    def success(self) -> bool:
        return all(
            [
                self.status and self.status.statusCode == StatusCode.SUCCESS or False,
                self.status is not None,
                self.refund is not None,
            ]
        )


class OrderDetailResponseProduct(BaseModel):
    """
    SEE: https://developers.payu.com/en/restapi.html#order_data_retrieve
    """

    name: str
    unitPrice: str
    quantity: str


class OrderDetailResponseOrder(BaseModel):
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
    products: List[OrderDetailResponseProduct]


class OrderDetailResponse(BaseModel):
    """
    SEE: https://developers.payu.com/en/restapi.html#order_data_retrieve
    """

    status: StatusResponse
    orders: Optional[List[OrderDetailResponseOrder]]

    @property
    def success(self) -> bool:
        return all(
            [
                self.status and self.status.statusCode == StatusCode.SUCCESS or False,
                self.orders is not None and len(self.orders) > 0,
            ]
        )
