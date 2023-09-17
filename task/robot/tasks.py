import json
from datetime import datetime
from django.conf import settings
from django.core.cache import cache
from infra.client.redisclient import RedisClient
from infra.utils.makedir import make_path
from application.constant import BuildStatus
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
def robot_notifier(task_id, project, env, region):
    conn = RedisClient(settings.ROBOT_REDIS_URL).connector
    task_redis_key = settings.TASK_RESULT_KEY_PREFIX + task_id
    current_result = conn.hgetall(task_redis_key)
    # current_result = cache.hgetall(task_redis_key)
    output_list = []
    # debug mode operate
    if not is_test_mode(task_id):
        batch = current_result.pop('batch')
        if len(current_result) != int(batch):
            return
        project_report_dir = settings.REPORT_PATH / project
        output_path = make_path(project_report_dir, task_id)
        for _, data in current_result.items():
            batch_result = json.loads(data)
            output_list.append(batch_result['output'].encode())
        title = f'{env}-{region}-{project}' if region else f'{env}-{project}'
        rebot(
            *output_list,
            logtitle=title + ' Log',
            reporttitle=title + ' Report',
            outputdir=output_path,
            prerebotmodifier=RobotModifier(LIB_NAME_MAP)
        )
        return
    # test mode operate
    history_id = convert_test_task_id(task_id)
    queryset = BuildHistory.objects.filter(id=history_id)
    instance = queryset.first()
    batch = instance.batch
    build_result = {
        'status': 0, 'start_time': 0, 'failed_case': 0,
        'passed_case': 0, 'skipped_case': 0, 'end_time': 0
    }
    output_list = []
    for _, data in current_result.items():
        batch_result = json.loads(data)
        build_result['failed_case'] += batch_result['failed']
        build_result['passed_case'] += batch_result['passed']
        build_result['skipped_case'] += batch_result['skipped']
        min_start_time = build_result['start_time'] or batch_result['start_time']
        max_end_time = build_result['end_time'] or batch_result['end_time']
        build_result['start_time'] = min(batch_result['start_time'], min_start_time)
        build_result['end_time'] = max(batch_result['end_time'], max_end_time)
        output_list.append(batch_result['output'].encode())
    build_result['start_time'] = datetime.fromtimestamp(build_result['start_time'])
    if len(current_result) != int(batch):
        del build_result['end_time']
        queryset.update(**build_result)
        return
    project_report_dir = settings.REPORT_PATH / project
    output_path = make_path(project_report_dir, task_id)
    title = f'{env}-{region}-{project}' if region else f'{env}-{project}'
    rebot(
        *output_list,
        logtitle=title + ' Log',
        reporttitle=title + ' Report',
        outputdir=output_path,
        prerebotmodifier=RobotModifier(LIB_NAME_MAP)
    )
    build_result['status'] = BuildStatus.FINNISH
    build_result['report_path'] = output_path
    build_result['end_time'] = datetime.fromtimestamp(build_result['end_time'])
    # build_result['report_content'] = str(output_list)
    queryset.update(**build_result)
    case_redis_key = settings.CASE_RESULT_KEY_PREFIX + task_id
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
    history_queryset = BuildHistory.objects.filter(
        record_id=instance.record_id
    )
    # status=-1, is running, wait all finish
    if any(item.status == -1 for item in history_queryset):
        return
    record = BuildRecord.objects.get(id=instance.record_id)
    record.status = 1
    record.finish_at = datetime.now()
    record.save()
    app.send_task(
        settings.REPORT_TASK,
        queue=settings.DEFAULT_QUEUE,
        routing_key=settings.DEFAULT_ROUTING_KEY,
        args=(history_id,)
    )



