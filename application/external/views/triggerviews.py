import json
from loguru import logger
from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.decorators import action
from application.user.models import User
from application.status import WebhookType
from application.webhook.models import Webhook
from application.builder.handler import execute_plan_by_id


class ExternalTriggerViewSets(viewsets.GenericViewSet):

    @action(methods=['post'], detail=False)
    def webhook_trigger(self, request, *args, **kwargs):
        logger.info(f'webhook trigger: {request.data}')
        params = request.query_params
        if not params.get('secret'):
            return HttpResponse('failed')
        webhook_query = Webhook.objects.filter(
            secret=params.get('secret')
        )
        if not webhook_query.exists():
            return HttpResponse('failed')
        webhook = webhook_query.first()
        user_query = User.object.filter(email=webhook.create_by)
        if not user_query.exists():
            return HttpResponse('failed')
        if webhook.hook_type == WebhookType.BuildHook:
            extra_data = json.loads(webhook.extra_data)
            plan_list = extra_data.get('plan_list', '').split(',')
            for plan_id in plan_list:
                plan_id = int(plan_id.strip())
                execute_plan_by_id(plan_id, user_query.first())
        return HttpResponse('success')


