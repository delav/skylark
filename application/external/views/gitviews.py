from loguru import logger
from django.conf import settings
from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.decorators import action
from infra.client.gitclient import GitClient
from application.workermanager.models import WorkerManager
from skylark.celeryapp import app


class ExternalGitViewSets(viewsets.GenericViewSet):
    MERGE_STATUS = 'can_be_merged'
    STATE = 'merged'
    TARGET_BRANCH = 'master'

    @action(methods=['post'], detail=False)
    def invoke_merge(self, request, *args, **kwargs):
        logger.info('更新本地library')
        git_client = GitClient()
        merge_info = request.data.get('object_attributes', {})
        if not self.is_merged_master(merge_info):
            return HttpResponse('OK', status=200)
        library_path = settings.LIBRARY_BASE_DIR / settings.LIBRARY_PROJECT_NAME
        if not library_path.exists():
            try:
                git_client.clone(settings.LIBRARY_GIT, settings.LIBRARY_BASE_DIR)
            except (Exception,):
                logger.error('git clone failed')
        else:
            try:
                git_client.pull(library_path)
            except (Exception,):
                logger.error('git pull failed')
        # TODO
        # notify slave git pull
        git_cmd = 'git pull'
        worker_queryset = WorkerManager.objects.filter(
            alive=True
        )
        for item in worker_queryset.iterator():
            app.send_task(
                settings.COMMAND_TASK,
                queue=item.queue,
                args=(git_cmd,)
            )
        return HttpResponse('OK', status=200)

    @classmethod
    def is_merged_master(cls, merge_info):
        merge_status = merge_info.get('merge_status')
        state = merge_info.get('state')
        target_branch = merge_info.get('target_branch')
        return merge_status == cls.MERGE_STATUS and state == cls.STATE and target_branch == cls.TARGET_BRANCH


