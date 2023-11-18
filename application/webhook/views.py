from loguru import logger
from rest_framework import viewsets
from rest_framework import mixins
from infra.django.response.jsonresponse import JsonResponse
from application.status import WebhookType, ModuleStatus
from application.usergroup.models import Group
from application.webhook.models import Webhook
from application.webhook.serializers import WebhookSerializers
from application.webhook.handler import generate_secret
from application.buildplan.models import BuildPlan
from application.common.access.projectaccess import has_project_permission


class WebhookViewSets(mixins.CreateModelMixin,
                      mixins.ListModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Webhook.objects.all()
    serializer_class = WebhookSerializers

    def create(self, request, *args, **kwargs):
        logger.info(f'create webhook: {request.data}')
        serializer = self.get_serializer(data=request.data)
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
        data = self.get_serializer(instance).data
        return JsonResponse(data=data)

    def list(self, request, *args, **kwargs):
        logger.info('get webhook list by user')
        groups_queryset = Group.objects.filter(
            user=request.user
        )
        if not groups_queryset.exists():
            return
        users = groups_queryset.first().user_set.all()
        user_email_list = [u.email for u in users]
        webhook_queryset = Webhook.objects.filter(
            status=ModuleStatus.NORMAL,
            create_by__in=user_email_list
        )
        webhook_list = self.get_serializer(webhook_queryset, many=True).data
        result = {
            'webhook_list': webhook_list,
            'type_list': [
                {'name': 'Build', 'value': WebhookType.BuildHook}
            ]
        }
        return JsonResponse(data=result)

    def destroy(self, request, *args, **kwargs):
        logger.info(f'delete webhook: {kwargs.get("pk")}')
        instance = self.get_object()
        groups_queryset = Group.objects.filter(
            user=request.user
        )
        if not groups_queryset.exists():
            return
        users = groups_queryset.first().user_set.all()
        user_email_list = [u.email for u in users]
        if request.user.email not in user_email_list:
            return JsonResponse(code=40300, msg='403_FORBIDDEN')
        instance.status = ModuleStatus.DELETED
        instance.save()
        return JsonResponse(data=instance.id)
