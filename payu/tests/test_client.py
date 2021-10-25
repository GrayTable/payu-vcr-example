from vcr.config import VCR

from ..client import PayUClient
from ..spec import OrderCreateInput, RefundCreateInput


def test_authorize(payu_vcr: VCR, payu_client: PayUClient):
    with payu_vcr.use_cassette("client_authorize.json"):
        response = payu_client.authorize()

    assert response.success


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


def test_get_order(
    payu_vcr: VCR,
    payu_client: PayUClient,
    order_create_input: OrderCreateInput,
):
    with payu_vcr.use_cassette("client_get_order.json"):
        create_order_response = payu_client.create_order(order_create_input)
        assert create_order_response.orderId is not None

        create_refund_response = payu_client.get_order(create_order_response.orderId)

    assert create_refund_response.success is True
