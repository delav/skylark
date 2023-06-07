from loguru import logger
from django.conf import settings
from rest_framework import mixins
from rest_framework import viewsets
from application.infra.django.response import JsonResponse
from application.userkeyword.models import UserKeyword
from application.userkeyword.serializers import UserKeywordSerializers
from application.common.keyword.formatkeyword import format_keyword_data

# Create your views here.


class UserKeywordViewSets(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = UserKeyword.objects.all()
    serializer_class = UserKeywordSerializers

    def list(self, request, *args, **kwargs):
        logger.info(f'get project user keyword: {request.query_params}')
        try:
            project_id = request.query_params.get('project')
            queryset = UserKeyword.objects.filter(project_id=project_id).select_related('test_case')
        except (Exception,) as e:
            logger.error(f'get user keyword failed: {e}')
            return JsonResponse(code=1000030, msg='request params error')
        user_keywords = []
        user_type = settings.KEYWORD_TYPE.get('UserKeyword')
        for item in queryset.iterator():
            serializer = self.get_serializer(item).data
            keyword_data = format_keyword_data(
                id=serializer['id'],
                name=item.test_case.name,
                ext_name=item.test_case.name,
                desc=item.test_case.document,
                group_id=serializer['group_id'],
                keyword_type=user_type,
                input_params=item.test_case.inputs,
                output_params=item.test_case.outputs,
                image=serializer['image']
            )
            user_keywords.append(format_keyword_data(**keyword_data))
        return JsonResponse(data=user_keywords)

