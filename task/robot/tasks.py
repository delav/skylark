import json
from datetime import datetime
from django.conf import settings
from django.core.cache import cache
from infra.client.redisclient import RedisClient
from infra.utils.makedir import make_path
from application.constant import REDIS_CASE_RESULT_KEY_PREFIX, REDIS_TASK_RESULT_KEY_PREFIX
from application.status import BuildStatus
from application.builder.handler import convert_test_task_id, is_test_mode
from application.buildrecord.models import BuildRecord
from application.buildhistory.models import BuildHistory, HistoryDetail
from application.storage import LIB_NAME_MAP
from worker.plugin.RebotModifier import RobotModifier
from worker.robot.rebot import rebot
from skylark.celeryapp import app


@app.task
def robot_runner(project, env, region, task_id,
                 batch_no, run_suite, run_data, variable_files, external_files):
    """robot execute task, no logic needed here, worker will do it"""
    pass


@app.task
def robot_notifier(task_id, project, env, region, notify_type):
    """
    received slaver notice task for execute test progressing
    notify_type: start/end
    """
    # debug mode operate, don't need to save anything
    if not is_test_mode(task_id):
        if notify_type == 'end':
            debug_notify(task_id, project, env, region)
        return
    # test mode operate, will save result info to db
    if notify_type == 'start':
        task_start_notify(task_id)
    if notify_type == 'end':
        task_end_notify(task_id, project, env, region)


def debug_notify(task_id, project, env, region):
    conn = RedisClient(settings.ROBOT_REDIS_URL).connector
    task_redis_key = REDIS_TASK_RESULT_KEY_PREFIX + task_id
    current_result = conn.hgetall(task_redis_key)
    batch = current_result.pop('batch')
    # test task not finish complete(maybe have multiple batches)
    if len(current_result) != int(batch):
        return
    project_report_dir = settings.REPORT_PATH / project
    output_path = make_path(project_report_dir, task_id)
    # fetch output content by batch no
    output_list = []
    for batch_no in range(1, int(batch) + 1):
        batch_output_redis_key = task_redis_key + f':output_{batch_no}'
        output_ctx = conn.get(batch_output_redis_key)
        output_list.append(output_ctx.encode())
    title = f'{env}-{region}-{project}' if region else f'{env}-{project}'
    rebot(
        *output_list,
        merge=True,
        logtitle=title + ' Log',
        reporttitle=title + ' Report',
        loglevel='DEBUG',
        outputdir=output_path,
        prerebotmodifier=RobotModifier(LIB_NAME_MAP)
    )


def task_start_notify(task_id):
    history_id = convert_test_task_id(task_id)
    queryset = BuildHistory.objects.filter(id=history_id)
    instance = queryset.first()
    if instance.status != BuildStatus.PENDING:
        return
    queryset.update(
        status=BuildStatus.RUNNING
    )


def task_end_notify(task_id, project, env, region):
    conn = RedisClient(settings.ROBOT_REDIS_URL).connector
    task_redis_key = REDIS_TASK_RESULT_KEY_PREFIX + task_id
    current_result = conn.hgetall(task_redis_key)
    history_id = convert_test_task_id(task_id)
    queryset = BuildHistory.objects.filter(id=history_id)
    if not queryset.exists():
        return
    instance = queryset.first()
    batch = instance.batch
    build_result = {
        'status': 0, 'start_time': 0, 'failed_case': 0,
        'passed_case': 0, 'skipped_case': 0, 'end_time': 0
    }
    output_list = []
    # get execute test result info of finish batches
    for _, data in current_result.items():
        batch_result = json.loads(data)
        build_result['failed_case'] += batch_result['failed']
        build_result['passed_case'] += batch_result['passed']
        build_result['skipped_case'] += batch_result['skipped']
        min_start_time = build_result['start_time'] or batch_result['start_time']
        max_end_time = build_result['end_time'] or batch_result['end_time']
        build_result['start_time'] = min(batch_result['start_time'], min_start_time)
        build_result['end_time'] = max(batch_result['end_time'], max_end_time)
    build_result['start_time'] = datetime.fromtimestamp(build_result['start_time'])
    if len(current_result) != int(batch):
        del build_result['end_time']
        queryset.update(**build_result)
        return
    # task finish
    for batch_no in range(1, int(batch) + 1):
        batch_output_redis_key = task_redis_key + f':output_{batch_no}'
        output_ctx = conn.get(batch_output_redis_key)
        output_list.append(output_ctx.encode())
    project_report_dir = settings.REPORT_PATH / project
    output_path = make_path(project_report_dir, task_id)
    title = f'{env}-{region}-{project}' if region else f'{env}-{project}'
    rebot(
        *output_list,
        merge=True,
        logtitle=title + ' Log',
        reporttitle=title + ' Report',
        outputdir=output_path,
        prerebotmodifier=RobotModifier(LIB_NAME_MAP)
    )
    build_result['status'] = BuildStatus.SUCCESS
    build_result['report_path'] = output_path
    build_result['end_time'] = datetime.fromtimestamp(build_result['end_time'])
    # build_result['report_content'] = str(output_list)
    queryset.update(**build_result)
    case_redis_key = REDIS_CASE_RESULT_KEY_PREFIX + task_id
    case_detail_list = []
    cases_result = conn.hgetall(case_redis_key)
    # cases_result = cache.hgetall(case_redis_key)
    for case_id, item in cases_result.items():
        item = json.loads(item)
        item['case_id'] = int(case_id)
        item['start_time'] = datetime.fromtimestamp(item['start_time'])
        item['end_time'] = datetime.fromtimestamp(item['end_time'])
        item['history_id'] = history_id
        case_detail_list.append(HistoryDetail(**item))
    HistoryDetail.objects.bulk_create(case_detail_list)
    # query all related task(history)
    task_status = BuildHistory.objects.filter(
        record_id=instance.record_id
    ).values('status')
    # wait all task finish
    if any(item['status'] not in (BuildStatus.FAILED, BuildStatus.SUCCESS) for item in task_status):
        return
    record = BuildRecord.objects.get(id=instance.record_id)
    record.status = BuildStatus.FINISH
    record.finish_at = datetime.now()
    record.save()
    app.send_task(
        settings.REPORT_TASK,
        args=(record.id, record.project_id)
    )
