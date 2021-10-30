from typing import Union

from ..config import PayUConfig, PayUUrls
from ..requestor import Requestor
from ..requestor.abstract import AbstractRequestor
from ..spec import enums, inputs, outputs
from ..spec.http import HTTPMethod, HTTPRequest, HTTPResponse, SignedHTTPHeaders
from .abstract import AbstractPayUClient, DictOrInput
from .exceptions import PayUError

__all__ = ["PayUClient"]


class PayUClient(AbstractPayUClient):
    def __init__(
        self,
        config: PayUConfig,
        requestor: AbstractRequestor = Requestor(),
    ):
        self.__config = config
        self.__urls = PayUUrls.build_from_config(self.__config)
        self.__requestor = requestor

    def __sign_request(self, request: HTTPRequest) -> HTTPRequest:
        authorize_response = self.authorize()
        request.headers = SignedHTTPHeaders(
            Authorization=f"Bearer {authorize_response.access_token}"
        )
        return request

    def __send_request(self, request: HTTPRequest) -> HTTPResponse:
        response = self.__requestor.send_request(request=request)

        if response.status > 399:
            raise PayUError(
                status_code=response.status,
                data=response.data,
            )

        return response

    def __send_signed_request(self, request: HTTPRequest) -> HTTPResponse:
        signed_request = self.__sign_request(request)
        response = self.__send_request(request=signed_request)
        return response

    def __create_api_url(
        self, endpoint: str, *params_args: Union[str, int], **params_kwargs
    ) -> str:
        url = "{}{}".format(self.__urls.api_url, endpoint)
        return url.format(*params_args, **params_kwargs)

    def authorize(self) -> outputs.AuthorizeOutput:
        """
        SEE: https://developers.payu.com/en/restapi.html#references_api_signature
        """
        url = "{}/pl/standard/user/oauth/authorize".format(self.__urls.base_url)

        authorize_input = inputs.AuthorizeInput(
            grant_type=self.__config.grant_type,
            client_id=self.__config.client_id,
            client_secret=self.__config.client_secret,
        )
        request = HTTPRequest(
            method=HTTPMethod.POST,
            url=url,
            data=authorize_input,
        )
        response = self.__send_request(request=request)

        authorize = outputs.AuthorizeOutput(**response.data)
        return authorize

    def get_order(
        self,
        order_id: str,
    ) -> outputs.OrderDetailOutput:
        """
        SEE: https://developers.payu.com/en/restapi.html#order_data_retrieve
        """
        url = self.__create_api_url("/orders/{}", order_id)

        request = HTTPRequest(
            method=HTTPMethod.GET,
            url=url,
        )
        response = self.__send_signed_request(request=request)

        order_detail = outputs.OrderDetailOutput(**response.data)
        return order_detail

    def create_order(
        self, data: DictOrInput[inputs.OrderCreateInput]
    ) -> outputs.OrderCreateOutput:
        """
        SEE: https://developers.payu.com/en/restapi.html#creating_new_order
        """
        url = self.__create_api_url("/orders")

        if not isinstance(data, inputs.OrderCreateInput):
            order_create_input = inputs.OrderCreateInput(**data)
        else:
            order_create_input = data

        request = HTTPRequest(
            url=url,
            method=HTTPMethod.POST,
            data=order_create_input.json(),
        )
        response = self.__send_signed_request(request=request)

        order_create = outputs.OrderCreateOutput(**response.data)
        return order_create

    def capture_order(self, order_id: str) -> outputs.OrderCaptureOutput:
        """
        SEE: https://developers.payu.com/en/restapi.html#status_update
        """
        url = self.__create_api_url("/orders/{}/status", order_id)

        order_capture_input = inputs.OrderCaptureInput(
            orderId=order_id,
            orderStatus=enums.OrderStatus.COMPLETED,
        )
        request = HTTPRequest(
            url=url,
            method=HTTPMethod.PUT,
            data=order_capture_input.json(),
        )
        response = self.__send_signed_request(request=request)

        order_capture = outputs.OrderCaptureOutput(**response.data)
        return order_capture

    def cancel_order(self, order_id: str) -> outputs.OrderCancelOutput:
        """
        SEE: https://developers.payu.com/en/restapi.html#cancellation
        """
        url = self.__create_api_url("/orders/{}", order_id)

        request = HTTPRequest(
            url=url,
            method=HTTPMethod.DELETE,
        )
        response = self.__send_signed_request(request=request)

        order_cancel = outputs.OrderCancelOutput(**response.data)
        return order_cancel

    def create_refund(
        self, order_id: str, data: DictOrInput[inputs.RefundCreateInput]
    ) -> outputs.RefundCreateOutput:
        """
        SEE: https://developers.payu.com/en/restapi.html#refunds_create
        """
        if not isinstance(data, inputs.RefundCreateInput):
            refund_create_input = inputs.RefundCreateInput(**data)
        else:
            refund_create_input = data

        url = self.__create_api_url("/orders/{}/refunds", order_id)

        request = HTTPRequest(
            method=HTTPMethod.POST,
            url=url,
            data=refund_create_input.json(),
        )
        response = self.__send_signed_request(request=request)

        refund_create = outputs.RefundCreateOutput(**response.data)
        return refund_create

    def get_pay_methods(self) -> outputs.PayMethodsOutput:
        """
        SEE: https://developers.payu.com/en/restapi.html#Transparent_retrieve
        """
        url = self.__create_api_url("/paymethods")

        request = HTTPRequest(
            method=HTTPMethod.GET,
            url=url,
        )
        response = self.__send_signed_request(request=request)

        pay_methods = outputs.PayMethodsOutput(**response.data)
        return pay_methods
