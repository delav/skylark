from worker.robot.run import run
from worker.robot.utils import DataReader


class Runner(object):
    def __init__(self, run_data, run_suite):
        self.run_data = run_data
        self.run_suite = run_suite

    def start(self):
        run_suite_files = self.get_suite_list()
        run(*run_suite_files)

    def build_options(self):
        return []

    def get_suite_list(self):
        return self.run_data.get('suite').keys()
