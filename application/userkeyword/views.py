from loguru import logger
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
        logger.info(f'get project user keyword: {request.query_params}')
        try:
            project_id = request.query_params.get('project')
            print(project_id)
            queryset = UserKeyword.objects.filter(project_id=project_id).select_related('test_case')
        except (Exception,) as e:
            logger.error(f'get user keyword failed: {e}')
            return JsonResponse(code=1000030, msg='request params error')
        user_keywords = []
        for item in queryset.iterator():
            ser = self.get_serializer(item).data
            keyword_data = {
                'id': ser['id'],
                'name': item.test_case.name,
                'ext_name': item.test_case.name,
                'desc': item.test_case.desc,
                'group': ser['group'],
                'input_arg': item.test_case.inputs,
                'output_arg': item.test_case.outputs,
                'input_desc': '',
                'output_desc': '',
                'image': ser['image']}
            user_keywords.append(keyword_data)
        return JsonResponse(data=user_keywords)

