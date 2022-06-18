from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.views import exception_handler
from rest_framework.status import HTTP_500_INTERNAL_SERVER_ERROR


class JsonResponse(Response):
    """
    An HttpResponse that allows its data to be rendered into
    arbitrary media types.
    """

    def __init__(self, data=None, status=None,
                 msg='success', code=20000,
                 template_name=None, headers=None,
                 exception=False, content_type=None):
        """
        Alters the init arguments slightly.
        For example, drop 'template_name', and instead use 'data'.

        Setting 'renderer' and 'media_type' will typically be deferred,
        For example being set automatically by the `APIView`.
        """
        super().__init__(None, status=status)

        if isinstance(data, Serializer):
            msg = (
                'You passed a Serializer instance as data, but '
                'probably meant to pass serialized `.data` or '
                '`.error`. representation.'
            )
            raise AssertionError(msg)

        self.data = {'data': data, 'msg': msg, 'code': code}
        self.template_name = template_name
        self.exception = exception
        self.content_type = content_type

        if headers:
            for name, value in headers.items():
                self[name] = value


def response_exception_handler(exc, context):
    """
    response interceptor,
    deal with the response exception
    """
    response = exception_handler(exc, context)
    field, message = '', ''
    code, msg = 10000, 'Unexpected error'
    # print('response:', response.data)
    result = response.data
    for index, value in enumerate(result):
        if index == 0:
            if isinstance(result, list):
                message = result[0]
            else:
                key = value
                value = result[key]

                if isinstance(value, str):
                    field = key
                    message = value
                else:
                    field = key
                    message = value[0]
    err_info = {'field': field, 'message': message}
    for key in err_info:
        if key == 'field':
            field = err_info[key]
        if key == 'message':
            msg = err_info[key]
            code = err_info[key].__dict__['code']
    if field != '':
        try:
            code = exception_desc[code][0]
            msg = exception_desc[code][1]
        except (KeyError,):
            code = 99999
    if response is None:
        return JsonResponse(
            code=50000, msg='Internal server error',
            status=HTTP_500_INTERNAL_SERVER_ERROR, exception=True)

    else:
        return JsonResponse(
            code=code, msg=msg,
            status=response.status_code, exception=True
        )


exception_desc = {
    'blank': (1000070, '该参数不能为空'),
    'required': (1000080, '缺少参数'),
    'invalid': (1000010, '非法参数'),
    'unique': (1000020, '该对象已存在，不能重复创建'),
    'not_authenticated': (1000030, '请先登录再进行操作'),
    'permission_denied': (1000040, '没有权限'),
    'token_not_valid': (1000050, '登录信息已过期')
}