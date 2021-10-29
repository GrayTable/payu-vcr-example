import json
import os
from json.decoder import JSONDecodeError

import pytest
import vcr
from vcr.config import VCR

from payu.spec import http

from ..client import PayUClient
from ..config import PayUConfig
from ..spec import OrderCreateInput, RefundCreateInput

CLIENT_CONFIG = PayUConfig(
    client_id=os.environ.get("TEST_PAYU_CLIENT_ID", 9999999),
    client_secret=os.environ.get("TEST_PAYU_CLIENT_SECRET", "TEST_CLIENT_SECRET"),
    enable_sandbox=True,
    autocapture_enabled=False,
)


def scrub_request(request):
    request.body = str(request.body).replace(str(CLIENT_CONFIG.client_id), "REDACTED")
    request.body = str(request.body).replace(CLIENT_CONFIG.client_secret, "REDACTED")
    return request


def scrub_response(response):
    response_bytes = response["body"]["string"]

    try:
        response_dict = json.loads(response_bytes)
        response_dict["access_token"] = "REDACTED"
        response_string = json.dumps(response_dict)
        response["body"]["string"] = bytes(response_string, "utf-8")
    except (JSONDecodeError, KeyError):
        pass

    return response


@pytest.fixture
def payu_vcr() -> VCR:
    return vcr.VCR(
        serializer="json",
        cassette_library_dir="payu/tests/cassettes",
        record_mode="once",
        match_on=["url", "method"],
        filter_headers=[("Authorization", "REDACTED")],
        before_record_request=[scrub_request],
        before_record_response=[scrub_response],
    )


@pytest.fixture
def payu_config() -> PayUConfig:
    return CLIENT_CONFIG


@pytest.fixture
def payu_client(payu_config) -> PayUClient:
    return PayUClient(payu_config)


@pytest.fixture
def payu_error_response() -> http.HTTPResponse:
    return http.HTTPResponse(
        status=403,
        data={
            "status": {
                "statusCode": "ERROR_VALUE_INVALID",
            }
        },
    )


@pytest.fixture
def order_create_input(payu_config: PayUConfig) -> OrderCreateInput:
    data = {
        "notifyUrl": None,
        "customerIp": "127.0.0.1",
        "merchantPosId": str(payu_config.client_id),
        "description": "TEST_DESCRIPTION",
        "currencyCode": "PLN",
        "totalAmount": "1000",
        "buyer": {
            "email": "johndoe@fakemail.com",
            "phone": "988988988",
            "firstName": "John",
            "lastName": "Doe",
            "language": "pl",
        },
        "products": [{"name": "TEST_PRODUCT", "unitPrice": "100", "quantity": "10"}],
    }
    return OrderCreateInput(**data)


@pytest.fixture
def refund_create_input() -> RefundCreateInput:
    data = {
        "refund": {
            "description": "TEST_REFUND_DESCRIPTION",
        }
    }
    return RefundCreateInput(**data)
