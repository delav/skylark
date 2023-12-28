import json
from loguru import logger
from django.http import HttpResponse
from django.conf import settings
from rest_framework import viewsets
from rest_framework.decorators import action
from application.user.models import User
from application.status import WebhookType
from application.webhook.models import Webhook
from application.builder.handler import execute_plan_by_id
from application.workermanager.models import WorkerManager
from application.pythonlib.handler import update_library_repository
from skylark.celeryapp import app


class ExternalWebhookViewSets(viewsets.GenericViewSet):

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
        if webhook.hook_type == WebhookType.BuildHook:
            logger.info('触发测试计划构建')
            extra_data = json.loads(webhook.extra_data)
            return self._handle_build_hook(webhook.create_by, extra_data)
        elif webhook.hook_type == WebhookType.GitHook:
            logger.info('更新本地library文件')
            merge_info = request.data.get('object_attributes', {})
            return self._handle_git_hook(merge_info)
        return HttpResponse('unknown')

    @staticmethod
    def _handle_build_hook(create_by, extra_data):
        user_query = User.objects.filter(email=create_by)
        if not user_query.exists():
            return HttpResponse('failed')
        plan_list = extra_data.get('plan_list', '').split(',')
        for plan_id in plan_list:
            plan_id = int(plan_id.strip())
            execute_plan_by_id(plan_id, user_query.first())
        return HttpResponse('success')

    @staticmethod
    def _handle_git_hook(push_info):
        gitlab_push_to_master = all([
            push_info.get('payload', {}).get('event_name') == 'push',
            push_info.get('payload', {}).get('ref') == 'refs/heads/master',
        ])
        github_push_to_master = all([
            push_info.get('event') == 'push',
            push_info.get('payload', {}).get('ref') == 'refs/heads/main',
        ])
        if not gitlab_push_to_master and not github_push_to_master:
            return HttpResponse('OK', status=200)
        flag = update_library_repository()
        # notify slave git pull
        git_cmd = 'git'
        worker_queryset = WorkerManager.objects.filter(
            alive=True
        )
        for item in worker_queryset.iterator():
            app.send_task(
                settings.COMMAND_TASK,
                queue=item.queue,
                args=(git_cmd,)
            )

