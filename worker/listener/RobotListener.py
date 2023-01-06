

class DebugRobotListener(object):
    ROBOT_LISTENER_API_VERSION = 3

    def __init__(self, msg):
        self.msg = msg

    def start_suite(self, data, result):
        pass

    def start_test(self, data, result):
        pass

    def end_test(self, data, result):
        pass

    def end_suite(self, data, result):
        pass

    def close(self):
        pass


