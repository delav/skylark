import json
from datetime import datetime
from skylark.celeryapp import app
from django.conf import settings
from application.builder.models import Builder
from application.infra.client.redisclient import RedisClient
from application.infra.utils.makedir import make_path
from worker.robot.rebot import rebot


@app.task
def robot_runner(build_id, batch_no, run_suite, run_data):
    """robot execute task, no logic needed here, worker will do it"""
    pass


@app.task
def robot_notifier(build_id):
    conn = RedisClient(settings.ROBOT_REDIS_URL).connector
    redis_key = settings.TASK_RESULT_KEY_PREFIX + build_id
    current_result = conn.hgetall(redis_key)
    batch = current_result.pop('batch')
    if len(current_result) != int(batch):
        return
    # all batch finish, merge xml output to html report/log file
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
    rebot(*output_list, outputdir=output_path)
    build_result['report_path'] = output_path
    queryset = Builder.objects.filter(id=int(build_id))
    queryset.update(**build_result)



