from skylark.celeryapp import app


@app.task
def clear_expired_file():
    pass
