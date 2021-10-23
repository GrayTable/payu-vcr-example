from typing import List, Literal, Optional

from pydantic import BaseModel, Field

from ..enums import OrderStatus


class PayURequest(BaseModel):
    pass


class AuthorizeRequest(PayURequest):
    """
    SEE: https://developers.payu.com/en/restapi.html#references_api_signature
    """

    grant_type: str
    client_id: int
    client_secret: str


class SignedRequestHeaders(PayURequest):
    """
    SEE: https://developers.payu.com/en/restapi.html#references_api_signature
    """

    authorization: str
    content_type: str = Field("application/json")

    def dict(self, *args, **kwargs):
        data = super().dict(*args, **kwargs)
        data["Content-Type"] = data.pop("content_type")
        data["Authorization"] = data.pop("authorization")

        return data


class SignedRequest(BaseModel):
    """
    SEE: https://developers.payu.com/en/restapi.html#references_api_signature
    """

    headers: SignedRequestHeaders
    data: Optional[PayURequest]


class OrderCreateRequestBuyer(PayURequest):
    """
    SEE: https://developers.payu.com/en/restapi.html#creating_new_order_api
    """

    email: str
    phone: str
    firstName: str
    lastName: str
    language: str


class OrderCreateRequestProduct(PayURequest):
    """
    SEE: https://developers.payu.com/en/restapi.html#creating_new_order_api
    """

    name: str
    unitPrice: str
    quantity: str


class OrderCreateRequest(PayURequest):
    """
    SEE: https://developers.payu.com/en/restapi.html#creating_new_order_api
    """

    merchantPosId: str
    description: str
    currencyCode: Literal["PLN"]
    totalAmount: str
    customerIp: str = "127.0.0.1"
    notifyUrl: Optional[str]
    buyer: Optional[OrderCreateRequestBuyer]
    products: List[OrderCreateRequestProduct]


class OrderCaptureRequest(PayURequest):
    """
    https://developers.payu.com/en/restapi.html#status_update
    """

    orderId: str
    orderStatus: Literal[OrderStatus.COMPLETED]


class RefundCreateRequestRefund(PayURequest):
    """
    SEE: https://developers.payu.com/en/restapi.html#refunds_create
    """

    description: str
    amount: Optional[int] = Field(
        None, description="To issue a full refund do not pass this value"
    )


class RefundCreateRequest(PayURequest):
    """
    SEE: https://developers.payu.com/en/restapi.html#refunds_create
    """

    refund: RefundCreateRequestRefund
