from unittest import mock
from unittest.mock import MagicMock

import pytest
from vcr.config import VCR

from payu.client.exceptions import PayUError
from payu.requestor.requestor import Requestor
from payu.spec.http import HTTPResponse

from ..client import PayUClient
from ..spec import OrderCreateInput, RefundCreateInput


def test_authorize(payu_vcr: VCR, payu_client: PayUClient):
    with payu_vcr.use_cassette("client_authorize.json"):
        response = payu_client.authorize()

    assert response.success


def test_get_order(
    payu_vcr: VCR,
    payu_client: PayUClient,
    order_create_input: OrderCreateInput,
):
    with payu_vcr.use_cassette("client_get_order.json"):
        create_order_response = payu_client.create_order(order_create_input)
        assert create_order_response.orderId is not None

        get_order_response = payu_client.get_order(create_order_response.orderId)

    assert get_order_response.success is True


def test_create_order(
    payu_vcr: VCR, payu_client: PayUClient, order_create_input: OrderCreateInput
):
    with payu_vcr.use_cassette("client_create_order.json"):
        response = payu_client.create_order(order_create_input)

    assert response.success is True


def test_capture_order(
    payu_vcr: VCR, payu_client: PayUClient, order_create_input: OrderCreateInput
):
    with payu_vcr.use_cassette("client_capture_order.json"):
        create_order_response = payu_client.create_order(order_create_input)
        assert create_order_response.orderId is not None

        capture_response = payu_client.capture_order(
            order_id=create_order_response.orderId
        )

    assert capture_response.success is True


def test_cancel_order(
    payu_vcr: VCR,
    payu_client: PayUClient,
    order_create_input: OrderCreateInput,
):
    with payu_vcr.use_cassette("client_cancel_order.json"):
        create_order_response = payu_client.create_order(order_create_input)
        assert create_order_response.orderId is not None

        capture_response = payu_client.cancel_order(
            order_id=create_order_response.orderId
        )

    assert capture_response.success is True


def test_get_refunds(
    payu_vcr: VCR,
    payu_client: PayUClient,
    order_create_input: OrderCreateInput,
    refund_create_input: RefundCreateInput,
):
    with payu_vcr.use_cassette("client_get_refunds.json"):
        create_order_response = payu_client.create_order(order_create_input)
        payu_client.create_refund(create_order_response.orderId, refund_create_input)
        get_refunds_response = payu_client.get_refunds(
            order_id=create_order_response.orderId
        )

    assert len(get_refunds_response.refunds) > 0


def test_create_refund(
    payu_vcr: VCR,
    payu_client: PayUClient,
    refund_create_input: RefundCreateInput,
    order_create_input: OrderCreateInput,
):
    with payu_vcr.use_cassette("client_create_refund.json"):
        create_order_response = payu_client.create_order(order_create_input)
        assert create_order_response.orderId is not None

        create_refund_response = payu_client.create_refund(
            create_order_response.orderId, refund_create_input
        )

    assert create_refund_response.success is True


def test_get_pay_methods(
    payu_vcr: VCR,
    payu_client: PayUClient,
):
    with payu_vcr.use_cassette("client_get_pay_methods.json"):
        paymethods = payu_client.get_pay_methods()

    assert len(paymethods.payByLinks) > 0


@mock.patch.object(Requestor, "send_request")
def test_payu_error(
    mock_requestor_send_request: MagicMock,
    payu_client: PayUClient,
    payu_error_response: HTTPResponse,
    order_create_input: OrderCreateInput,
):
    mock_requestor_send_request.return_value = payu_error_response

    with pytest.raises(PayUError) as exc_info:
        payu_client.create_order(order_create_input)

    assert exc_info.value.status_code == payu_error_response.status
    assert exc_info.value.data == payu_error_response.data
