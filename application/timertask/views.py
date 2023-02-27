from loguru import logger
from rest_framework import mixins
from rest_framework import viewsets
from application.infra.response import JsonResponse
from application.timertask.models import TimerTask
from application.timertask.serializers import TimerTaskSerializers

# Create your views here.


class TimerTaskViewSets(mixins.RetrieveModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = TimerTask.objects.all()
    serializer_class = TimerTaskSerializers

    def create(self, request, *args, **kwargs):
        logger.info(f'create timer task: {request.data}')
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            self.perform_create(serializer)
        except Exception as e:
            logger.error(f'create timer task failed: {e}')
            return JsonResponse(code=10201, msg='create timer task failed')
        return JsonResponse(data=serializer.data)

    def retrieve(self, request, *args, **kwargs):
        pass

    def destroy(self, request, *args, **kwargs):
        pass
