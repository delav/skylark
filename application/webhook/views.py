from loguru import logger
from rest_framework import viewsets
from rest_framework.decorators import action
from infra.django.response.jsonresponse import JsonResponse
from application.status import WebhookType, ModuleStatus
from application.webhook.models import Webhook
from application.webhook.serializers import WebhookSerializers
from application.webhook.handler import common_data, create_build_hook_data, generate_secret
from application.buildplan.models import BuildPlan
from application.common.access.projectaccess import has_project_permission


class WebhookViewSets(viewsets.GenericViewSet):

    @action(methods=['post'], detail=False)
    def create_webhook(self, request, *args, **kwargs):
        logger.info('create webhook')
        serializer = WebhookSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        if serializer.validated_data.get('hook_type') == WebhookType.BuildHook:
            plan_list = serializer.validated_data.get('extra_data').get('plan_list', '')
            plan_id_list = plan_list.split(',')
            for plan_id_str in plan_id_list:
                plan_query = BuildPlan.objects.filter(
                    id=plan_id_str,
                    status=ModuleStatus.NORMAL
                )
                if not plan_query.exists():
                    return JsonResponse(code=12901, msg=f'plan not exists: {plan_id_str}')
                if not has_project_permission(plan_query.first().project_id, request.user):
                    return JsonResponse(code=12902, msg=f'not permission for plan: {plan_id_str}')
        instance = Webhook.objects.create(
            **serializer.validated_data,
            secret=generate_secret()
        )
        data = WebhookSerializers(instance).data
        return JsonResponse(data=data)

    @action(methods=['get'], detail=False)
    def build_webhook(self, request, *args, **kwargs):
        logger.info(f'build webhook')
        hook_type = request.query_params.get('type')
        hook_data = common_data()
        if hook_type == WebhookType.BuildHook:
            buidl_extra_data = create_build_hook_data()
            hook_data.update(buidl_extra_data)
        return JsonResponse(data=hook_data)

    @action(methods=['get'], detail=False)
    def get_webhook_list(self, request, *args, **kwargs):
        logger.info('get webhook list by user')
        result = {
            'webhook_list': [],
            'type_list': [
                {'name': 'Build', 'value': WebhookType.BuildHook}
            ]
        }
        return JsonResponse(data=result)

