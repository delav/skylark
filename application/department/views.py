from loguru import logger
from rest_framework import mixins
from rest_framework import viewsets
from infra.django.response import JsonResponse
from application.department.models import Department
from application.department.serializers import DepartmentSerializers

# Create your views here.


class DepartmentViewSets(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializers

    def list(self, request, *args, **kwargs):
        logger.info(f'get department list')
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return JsonResponse(data=serializer.data)

