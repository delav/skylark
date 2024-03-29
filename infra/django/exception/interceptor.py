import traceback
import loguru
from rest_framework.views import exception_handler as rest_handler
from rest_framework.status import HTTP_500_INTERNAL_SERVER_ERROR
from infra.django.response import JsonResponse
from infra.django.exception import DetailError


def exception_handler(exc, context):
    """
    response interceptor,
    deal with the response exception
    """
    response = rest_handler(exc, context)
    if response is None:
        traceback.print_exc()
        return JsonResponse(
            code=99999,
            msg='500_SYSTEM_ERROR',
            status=HTTP_500_INTERNAL_SERVER_ERROR
        )
    if isinstance(response.data, list):
        if response.data and isinstance(response.data[0], DetailError):
            return JsonResponse(
                code=response.data[0].code,
                msg=response.data[0].text
            )
    if response.status_code == 400:
        response = JsonResponse(
            code=40000,
            msg='400_BAD_REQUEST'
        )
    elif response.status_code == 401:
        response = JsonResponse(
            code=40100,
            msg='401_UNAUTHORIZED'
        )
    elif response.status_code == 403:
        response = JsonResponse(
            code=40300,
            msg='403_FORBIDDEN'
        )
    elif response.status_code == 404:
        response = JsonResponse(
            code=40400,
            msg='404_NOT_FOUND'
        )
    elif response.status_code == 405:
        response = JsonResponse(
            code=response.status_code,
            msg='405_METHOD_NOT_ALLOWED'
        )
    elif 500 <= response.status_code <= 599:
        response = JsonResponse(
            code=55555,
            msg='INTERNAL_SERVER_ERROR'
        )
    return response
