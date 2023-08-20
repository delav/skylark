from loguru import logger
from rest_framework import mixins
from rest_framework import viewsets
from infra.django.response import JsonResponse
from application.constant import KeywordGroupType
from application.constant import KeywordType, ModuleStatus
from application.userkeyword.models import UserKeyword
from application.userkeyword.serializers import UserKeywordSerializers
from application.keywordgroup.models import KeywordGroup
from application.keywordgroup.serializers import KeywordGroupSerializers
from application.common.keyword.formatter import format_keyword_data

# Create your views here.


class UserKeywordViewSets(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = UserKeyword.objects.all()
    serializer_class = UserKeywordSerializers

    def list(self, request, *args, **kwargs):
        logger.info(f'get project user keyword: {request.query_params}')
        user_group = KeywordGroup.objects.filter(
            group_type=KeywordGroupType.USER
        )
        if not user_group.exists():
            return JsonResponse(data=[])
        group = KeywordGroupSerializers(user_group.first()).data
        project_id = request.query_params.get('project')
        queryset = UserKeyword.objects.filter(
            project_id=project_id,
            status=ModuleStatus.NORMAL
        ).select_related('test_case')
        if not queryset.exists():
            return JsonResponse(data=[])
        user_keywords = []
        for item in queryset.iterator():
            serializer_data = self.get_serializer(item).data
            keyword_data = format_keyword_data(
                id=serializer_data['id'],
                name=item.test_case.name,
                ext_name=item.test_case.name,
                desc=item.test_case.document,
                group_id=serializer_data['group_id'],
                keyword_type=KeywordType.USER,
                input_params=item.test_case.inputs,
                output_params=item.test_case.outputs,
                image=serializer_data['image']
            )
            if not keyword_data:
                continue
            user_keywords.append(format_keyword_data(**keyword_data))
        group['keywords'] = user_keywords
        return JsonResponse(data=[group])

