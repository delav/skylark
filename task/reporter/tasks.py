from application.buildhistory.models import BuildHistory
from skylark.celeryapp import app


@app.task
def send_report(history_id):
    pass
