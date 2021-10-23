from typing import Optional

from .abstract import AbstractPayUClient, AbstractRequestor, DictOrRequest
from .config import PayUConfig, PayUResourceUrls
from .enums import OrderStatus, RequestMethod
from .requestor import Requestor
from .schema import (
    AuthorizeRequest,
    AuthorizeResponse,
    OrderCaptureRequest,
    OrderCaptureResponse,
    OrderCreateRequest,
    OrderCreateResponse,
    RefundCreateRequest,
    RefundCreateResponse,
    SignedRequest,
    SignedRequestHeaders,
)
from .schema.requests import PayURequest
from .schema.responses import OrderDetailResponse


class PayUClient(AbstractPayUClient):
    def __init__(
        self,
        config: PayUConfig,
        requestor: AbstractRequestor = Requestor(),
    ):
        self.__config = config
        self.__urls = PayUResourceUrls.build_from_config(self.__config)
        self.__requestor = requestor

    def __sign_request(self, data: Optional[PayURequest] = None) -> SignedRequest:
        authorize_response = self.authorize()
        headers = SignedRequestHeaders(
            authorization=f"Bearer {authorize_response.access_token}"
        )
        signed_request = SignedRequest(
            headers=headers,
            data=data,
        )
        return signed_request

    def authorize(self) -> AuthorizeResponse:
        """
        SEE: https://developers.payu.com/en/restapi.html#references_api_signature
        """
        url = self.__urls.auth
        authorize_request = AuthorizeRequest(
            grant_type=self.__config.grant_type,
            client_id=self.__config.client_id,
            client_secret=self.__config.client_secret,
        )

        response = self.__requestor.send_unsigned_request(
            method=RequestMethod.POST,
            url=url,
            data=authorize_request.dict(),
        )

        authorize_response = AuthorizeResponse(**response.json())
        return authorize_response

    def get_order(
        self,
        order_id: str,
    ) -> OrderDetailResponse:
        """
        SEE: https://developers.payu.com/en/restapi.html#order_data_retrieve
        """
        url = self.__urls.order_detail.format(order_id=order_id)
        signed_request = self.__sign_request()

        response = self.__requestor.send_signed_request(
            method=RequestMethod.GET,
            url=url,
            signed_request=signed_request,
        )

        order_detail_response = OrderDetailResponse(**response.json())
        return order_detail_response

    def create_order(
        self, data: DictOrRequest[OrderCreateRequest]
    ) -> OrderCreateResponse:
        """
        SEE: https://developers.payu.com/en/restapi.html#creating_new_order
        """
        if not isinstance(data, OrderCreateRequest):
            data = OrderCreateRequest(**data)

        url = self.__urls.order_list
        signed_request = self.__sign_request(data)

        response = self.__requestor.send_signed_request(
            method=RequestMethod.POST,
            url=url,
            signed_request=signed_request,
            allow_redirects=False,
        )

        order_create_response = OrderCreateResponse(**response.json())
        return order_create_response

    def capture_order(self, order_id: str) -> OrderCaptureResponse:
        """
        SEE: https://developers.payu.com/en/restapi.html#status_update
        """
        data = OrderCaptureRequest(
            orderId=order_id,
            orderStatus=OrderStatus.COMPLETED,
        )

        url = self.__urls.order_status.format(order_id=order_id)
        signed_request = self.__sign_request(data)

        response = self.__requestor.send_signed_request(
            method=RequestMethod.PUT,
            url=url,
            signed_request=signed_request,
        )

        order_capture_response = OrderCaptureResponse(**response.json())
        return order_capture_response

    def create_refund(
        self, order_id: str, data: DictOrRequest[RefundCreateRequest]
    ) -> RefundCreateResponse:
        """
        SEE: https://developers.payu.com/en/restapi.html#refunds_create
        """
        if not isinstance(data, RefundCreateRequest):
            data = RefundCreateRequest(**data)

        url = self.__urls.order_refunds.format(order_id=order_id)
        signed_request = self.__sign_request(data)

        response = self.__requestor.send_signed_request(
            method=RequestMethod.POST,
            url=url,
            signed_request=signed_request,
        )

        refund_create_response = RefundCreateResponse(**response.json())
        return refund_create_response
