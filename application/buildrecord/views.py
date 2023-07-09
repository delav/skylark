from loguru import logger
from rest_framework import mixins
from rest_framework import viewsets
from infra.django.response import JsonResponse
from infra.django.pagination.paginator import PagePagination
from application.usergroup.models import UserGroup
from application.user.models import User
from application.project.models import Project
from application.buildrecord.models import BuildRecord
from application.buildrecord.serializers import BuildRecordSerializers


# Create your views here.


class BuildRecordViewSets(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = BuildRecord.objects.all()
    serializer_class = BuildRecordSerializers
    pagination_class = PagePagination

    def list(self, request, *args, **kwargs):
        logger.info(f'get record by param: {request.query_params}')
        try:
            project_id = request.query_params.get('project')
            groups_queryset = UserGroup.objects.filter(user=request.user)
            users = User.objects.none()
            for group in groups_queryset:
                users |= group.user_set.all()
            group_emails = [user.email for user in users]
            projects = Project.objects.filter(create_by__in=group_emails, status=0)
            project_ids = [item.id for item in projects]
            if project_id:
                queryset = self.get_queryset().filter(
                    project_id=project_id).order_by('-create_at')
            else:
                queryset = self.get_queryset().filter(
                    project_id__in=project_ids).order_by('-create_at')
            pg_queryset = self.paginate_queryset(queryset)
            record_list = self.get_serializer(pg_queryset, many=True).data
        except (Exception,) as e:
            logger.error(f'get record failed: {e}')
            return JsonResponse(code=10400, msg='get record failed')
        result = {'data': record_list, 'total': queryset.count()}
        return JsonResponse(data=result)

    def retrieve(self, request, *args, **kwargs):
        logger.info(f'get detail')

