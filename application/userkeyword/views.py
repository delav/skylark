from loguru import logger
from django.core.exceptions import ValidationError
from rest_framework import mixins
from rest_framework import viewsets
from application.infra.response import JsonResponse
from application.userkeyword.models import UserKeyword
from application.userkeyword.serializers import UserKeywordSerializers

# Create your views here.


class UserKeywordViewSets(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = UserKeyword.objects.all()
    serializer_class = UserKeywordSerializers

    def list(self, request, *args, **kwargs):
        params = request.query_params
        project_id = params.get('project')
        logger.info(f'get project user keyword: {project_id}')
        try:
            queryset = UserKeyword.objects.select_related('test_case').filter(project_id=project_id)
        except ValidationError:
            return JsonResponse(code=1000030, msg='request params error')
        user_keywords = []
        for item in queryset.iterator():
            keyword_data = {
                'id': item.id,
                'name': item.test_case.case_name,
                'ext_name': item.test_case.case_name,
                'desc': item.test_case.case_desc,
                'group': item.group,
                'input_arg': item.test_case.inputs,
                'output_arg': item.case.outputs,
                'input_desc': '',
                'output_desc': '',
                'image': item.image}
            user_keywords.append(keyword_data)
        return JsonResponse(data=user_keywords)

