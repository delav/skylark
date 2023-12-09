from application.manager import get_worker_by_ip
from application.workermanager.models import WorkerManager
from skylark.celeryapp import app


@app.task
def heartbeat(worker_ip):
    w = get_worker_by_ip(worker_ip)
    if w.get('alive'):
        return
    # update worker state


@app.task
def worker_collector(info_type, worker_info):
    if not isinstance(worker_info, dict):
        return
    worker_ip = worker_info.pop('ip')
    hostname = worker_info.pop('hostname', '')
    queue = worker_info.pop('queue')
    worker_query = WorkerManager.objects.filter(
        ip=worker_ip
    )
    if info_type == 'ready':
        if worker_query.exists():
            worker = worker_query.first()
            worker.alive = True
            worker.hostname = hostname
            worker.queue = queue
            worker.save()
            return
        WorkerManager.objects.create(
            ip=worker_ip,
            hostname=hostname,
            alive=True,
            queue=queue,
            extra_data=worker_info
        )
    elif info_type == 'shutdown':
        if worker_query.exists():
            worker = worker_query.first()
            worker.alive = False
            worker.hostname = hostname
            worker.queue = queue
            worker.save()


@app.task
def command_executor(cmd):
    pass
