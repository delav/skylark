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
    report_url, result_data = build_report_data(record_id, project_id)
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
        notifier.send_email(settings.EMAIL_HOST_USER, notice.rcv_email)


def build_report_data(record_id, project_id):
    result_data = {}
    project = get_project_by_id(project_id)
    result_data['project_name'] = project.get('name', 'Nan')
    env_map = {item.get('id'): item.get('name') for item in get_env_list()}
    region_map = {item.get('id'): item.get('name') for item in get_region_list()}
    history_queryset = BuildHistory.objects.filter(
        record_id=record_id
    )
    for history in history_queryset.iterator():
        env_name = env_map.get(history.env_id)
        if env_name not in result_data:
            result_data[env_name] = {}
        children_data = {
            'history_id': history.id,
            'start_time': history.start_time,
            'end_time': history.end_time,
            'total_number': history.total_case,
            'success_number': history.passed_case,
            'failed_number': history.failed_case,
        }
        if not history.region_id:
            result_data[env_name] = children_data
            continue
        region_name = region_map.get(history.region_id, 'Nan')
        result_data[env_name][region_name] = children_data
    return 'report_url', result_data
