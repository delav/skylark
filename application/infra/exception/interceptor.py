from rest_framework.views import exception_handler
from rest_framework.status import HTTP_500_INTERNAL_SERVER_ERROR
from application import JsonResponse


def response_exc_handler(exc, context):
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