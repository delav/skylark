from worker.config import ROBOT_REDIS_URL
from worker.connector import RedisConnector


class RobotListener(object):
    ROBOT_LISTENER_API_VERSION = 3

    def __init__(self, task_id='id'):
        self.redis_key = 'task:' + task_id
        self.redis = RedisConnector(ROBOT_REDIS_URL)

    def start_suite(self, data, result):
        # print("suite data: %s" % data)
        # print("Start suite: %s" % data.suites)
        # print("suite cases: %s" % data.tests)
        # print("suite_test_count: %s" % data.test_count)
        pass

    def start_test(self, data, result):
        # print("start test data: {}".format(dir(data)))
        # print("start test result: {}".format(dir(result)))
        # print("start test name:{}".format(data.name))
        # print("CaseID:{}".format(data.doc))
        pass

    def end_test(self, data, result):
        # print("end test data: {}".format(dir(data)))
        # print("end test result: {}".format(dir(result)))
        # print("test result:{}".format(result.passed))
        # print("end test status:{}".format(result.status))
        self.redis.hash_set(self.redis_key, data.doc, result.status)

    def end_suite(self, data, result):
        # print("end suite data: {}".format(dir(data)))
        # print("end suite result: {}".format(dir(result)))
        pass

    def close(self):
        pass




