from enum import Enum

__all__ = [
    "StatusCode",
    "OrderStatus",
    "RequestMethod",
]


class StatusCode(str, Enum):
    SUCCESS = "SUCCESS"
    WARNING_CONTINUE_REDIRECT = "WARNING_CONTINUE_REDIRECT"
    WARNING_CONTINUE_3DS = "WARNING_CONTINUE_3DS"
    WARNING_CONTINUE_CVV = "WARNING_CONTINUE_CVV"
    ERROR_SYNTAX = "ERROR_SYNTAX"
    ERROR_VALUE_INVALID = "ERROR_VALUE_INVALID"
    UNAUTHORIZED = "UNAUTHORIZED"
    DATA_NOT_FOUND = "DATA_NOT_FOUND"


class OrderStatus(str, Enum):
    NEW = "NEW"
    COMPLETED = "COMPLETED"
    WAITING_FOR_CONFIRMATION = "WAITING_FOR_CONFIRMATION"


class RequestMethod(str, Enum):
    POST = "POST"
    PUT = "PUT"
    GET = "GET"
