class TwitterApiException(Exception):
    """Base exception for the package"""


class QueryException(TwitterApiException):
    """Invalid request query"""


class RequestException(TwitterApiException):
    """Exception while processing the request"""


class HTTPError(TwitterApiException):
    """HTTP error"""
