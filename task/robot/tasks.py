import json
from datetime import datetime
from django.conf import settings
from application.buildhistory.models import BuildHistory, HistoryDetail
from application.infra.client.redisclient import RedisClient
from application.infra.utils.makedir import make_path
from application.infra.utils.buildhandler import is_test_mode, convert_test_build_id
from worker.robot.rebot import rebot
from skylark.celeryapp import app


@app.task
def robot_runner(build_id, batch_no, run_suite, run_data):
    """robot execute task, no logic needed here, worker will do it"""
    pass


@app.task
def robot_notifier(build_id):
    conn = RedisClient(settings.ROBOT_REDIS_URL).connector
    task_redis_key = settings.TASK_RESULT_KEY_PREFIX + build_id
    current_result = conn.hgetall(task_redis_key)
    output_list = []
    # debug mode operate
    if not is_test_mode(build_id):
        batch = current_result.pop('batch')
        if len(current_result) != int(batch):
            return
        output_path = make_path(settings.REPORT_PATH, build_id)
        for _, data in current_result.items():
            batch_result = json.loads(data)
            output_list.append(batch_result['output'].encode())
        rebot(*output_list, outputdir=output_path, quiet=True)
        return
    # test mode operate
    history_id = convert_test_build_id(build_id)
    queryset = BuildHistory.objects.filter(id=history_id)
    instance = queryset.first()
    batch = instance.batch
    if len(current_result) != int(batch):
        return
    build_result = {
        'status': 0, 'start_time': 0, 'failed_case': 0,
        'passed_case': 0, 'skipped_case': 0, 'end_time': 0
    }
    output_list = []
    for _, data in current_result.items():
        batch_result = json.loads(data)
        min_start_time = build_result['start_time'] or batch_result['start_time']
        max_end_time = build_result['end_time'] or batch_result['end_time']
        build_result['start_time'] = min(batch_result['start_time'], min_start_time)
        build_result['end_time'] = max(batch_result['end_time'], max_end_time)
        output_list.append(batch_result['output'].encode())
    build_result['start_time'] = datetime.fromtimestamp(build_result['start_time'])
    build_result['end_time'] = datetime.fromtimestamp(build_result['end_time'])
    output_path = make_path(settings.REPORT_PATH, build_id)
    rebot(*output_list, outputdir=output_path, quiet=True)
    build_result['report_path'] = output_path
    # build_result['report_content'] = str(output_list)
    queryset.update(**build_result)
    case_redis_key = settings.CASE_RESULT_KEY_PREFIX + build_id
    case_detail_list = []
    cases_result = conn.hgetall(case_redis_key)
    for case_id, item in cases_result.items():
        item['test_case_id'] = int(case_id)
        item['start_time'] = datetime.fromtimestamp(item['start_time'])
        item['end_time'] = datetime.fromtimestamp(item['end_time'])
        item['build_history_id'] = history_id
        case_detail_list.append(item)
    HistoryDetail.objects.bulk_create(case_detail_list)



