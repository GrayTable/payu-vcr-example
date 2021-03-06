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


class ErrorStatusCode(str, Enum):
    ERROR_SYNTAX = "ERROR_SYNTAX"
    ERROR_VALUE_INVALID = "ERROR_VALUE_INVALID"
    ERROR_VALUE_MISSING = "ERROR_VALUE_MISSING"
    ERROR_ORDER_NOT_UNIQUE = "ERROR_ORDER_NOT_UNIQUE"
    ERROR_INTERNAL = "ERROR_INTERNAL"
    BUSINESS_ERROR = "BUSINESS_ERROR"
    UNAUTHORIZED = "UNAUTHORIZED"
    UNAUTHORIZED_REQUEST = "UNAUTHORIZED_REQUEST"
    DATA_NOT_FOUND = "DATA_NOT_FOUND"
    TIMEOUT = "TIMEOUT"
    GENERAL_ERROR = "GENERAL_ERROR"
    WARNING = "WARNING"
    SERVICE_NOT_AVAILABLE = "SERVICE_NOT_AVAILABLE"


class OrderStatus(str, Enum):
    NEW = "NEW"
    COMPLETED = "COMPLETED"
    WAITING_FOR_CONFIRMATION = "WAITING_FOR_CONFIRMATION"


class RequestMethod(str, Enum):
    POST = "POST"
    PUT = "PUT"
    GET = "GET"
