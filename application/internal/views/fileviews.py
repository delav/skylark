from loguru import logger
from django.conf import settings
from django.http import FileResponse, HttpResponse
from django.utils.http import urlquote
from rest_framework import viewsets
from rest_framework.decorators import action
from infra.crypto.crypter import base64_encrypt
from application.virtualfile.handler import get_download_file_stream


class InternalFileViewSets(viewsets.GenericViewSet):

    @action(methods=['post'], detail=False)
    def download_file(self, request, *args, **kwargs):
        logger.info(f'接受slaver下载请求: {request.data}')
        auth = request.headers.get('auth')
        if auth != base64_encrypt(settings.INTERNAL_KEY):
            return HttpResponse('FORBIDDEN', status=403)
        path_str = request.data.get('path')
        file_name = request.data.get('name')
        if not path_str or path_str.strip() == '':
            return HttpResponse('404_NOT_FOUND', status=404)
        file = get_download_file_stream(path_str, file_name)
        if not file:
            return HttpResponse('404_NOT_FOUND', status=404)
        response = FileResponse(file)
        response['Content-Type'] = "application/octet-stream"
        response['Content-Disposition'] = f'attachment;filename={urlquote(file_name)}'
        response['Access-Control-Expose-Headers'] = "Content-Disposition"
        return response
