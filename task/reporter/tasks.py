from django.conf import settings
from application.notification.models import Notification
from application.notification.handler import ReportNotifier
from application.buildrecord.models import BuildRecord
from application.buildhistory.models import BuildHistory
from application.status import NoticeMode
from application.manager import get_project_by_id, get_env_list, get_region_list
from skylark.celeryapp import app


@app.task
def send_report(record_id, project_id):
    notice_query = Notification.objects.filter(project_id=project_id)
    if not notice_query.exists():
        return
    notice = notice_query.first()
    group_switch = notice.notice_switch
    email_switch = notice.email_switch
    if not group_switch and email_switch:
        return
    record_query = BuildRecord.objects.filter(id=record_id)
    if not record_query.exists():
        return
    if record_query.first().periodic:
        create_by = 'Scheduler'
    else:
        create_by = record_query.first().create_by
    report_url, result_data = build_report_data(record_id, create_by, project_id)
    notifier = ReportNotifier(report_url, result_data)
    if group_switch:
        notice_mode = notice.notice_mode
        if notice_mode == NoticeMode.DING_TALK:
            notifier.send_ding(notice.ding_token, notice.ding_keyword)
        elif notice_mode == NoticeMode.WECOM:
            notifier.send_wecom(notice.wecom_token)
        elif notice_mode == NoticeMode.lARK:
            notifier.send_lark(notice.lark_token, notice.lark_keyword)
    if email_switch:
        email_list = notice.rcv_email.split(',')
        notifier.send_email(settings.EMAIL_HOST_USER, email_list)


def build_report_data(record_id, create_by, project_id):
    result_data = {}
    project = get_project_by_id(project_id)
    result_data['project_name'] = project.get('name', 'Nan')
    result_data['record_id'] = record_id
    result_data['tester'] = create_by
    env_map = {item.get('id'): item.get('name') for item in get_env_list()}
    region_map = {item.get('id'): item.get('name') for item in get_region_list()}
    history_queryset = BuildHistory.objects.filter(
        record_id=record_id
    )
    build_result_list = []
    for history in history_queryset.iterator():
        env_name = env_map.get(history.env_id)
        region_name = region_map.get(history.region_id, 'Nan')
        duration = 'unknown'
        if history.end_time:
            duration_second = (history.end_time - history.start_time).total_seconds()
            hours, remainder = divmod(duration_second, 3600)
            minutes, seconds = divmod(remainder, 60)
            duration = '{:02}:{:02}:{:02}'.format(int(hours), int(minutes), int(seconds))
        build_data = {
            'history_id': history.id,
            'env_name': env_name,
            'region_name': region_name,
            'start_time': history.start_time.strftime('%Y-%m-%d %H:%M:%S'),
            'end_time': history.end_time.strftime('%Y-%m-%d %H:%M:%S'),
            'duration': duration,
            'total_number': history.total_case,
            'passed_rate': str(round(history.passed_case / history.total_case, 3) * 100)+'%',
            'success_number': history.passed_case,
            'failed_number': history.failed_case,
            'skipped_number': history.skipped_case
        }
        build_result_list.append(build_data)
    result_data['data_list'] = build_result_list
    return 'report_url', result_data
