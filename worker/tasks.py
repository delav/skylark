from worker import app
from worker.robot.run import run
from worker.plugin.RobotListener import RobotListener
from worker.plugin.RebotModifier import RobotModifier


@app.task
def robot_runner(self, task_id, run_suite, meta_data, report_path):
    run(*run_suite,
        outputdir=report_path,
        metadata=meta_data,
        listener=RobotListener(task_id),)
        # prerebotmodifier=RobotModifier())  # UserWarning: 'keywords' attribute is read-only and deprecated since Robot Framework 4.0. Use 'body', 'setup' or 'teardown' instead.


@app.task
def merge_report(self):
    pass
