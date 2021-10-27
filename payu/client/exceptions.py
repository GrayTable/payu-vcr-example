from typing import Any
from payu.spec import http


class PayUError(Exception):
    def __init__(self, status_code: http.HTTPStatus, data: Any):
        self.status_code = status_code
        self.data = data

        message = (
            "Payu Failed with error status code: "
            f"'{self.status_code}', data: {self.data}"
        )
        super().__init__(message)
