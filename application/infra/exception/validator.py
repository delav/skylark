from rest_framework.exceptions import APIException
from application.infra.exception import DetailError


class ValidationException(APIException):
    """
    Custom exception handler in serializers validate
    """

    default_detail = 'A server error occurred.'
    default_code = 'error'

    def __init__(self, detail=None, code=None):
        if detail is None:
            detail = self.default_detail
        if code is None:
            code = self.default_code

        self.detail = [DetailError(detail, code)]


