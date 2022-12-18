from application.infra.robot.assembler.config import Config
from application.infra.robot.assembler.settings import SetupTeardownSetting


class DirInitFile(object):
    """
    dir init file only support setup teardown settings
    """

    def __init__(self, test_setup, test_teardown, suite_setup, suite_teardown):
        self.test_setup = test_setup
        self.test_teardown = test_teardown
        self.suite_setup = suite_setup
        self.suite_teardown = suite_teardown

    def get_text(self):
        settings_identification = Config().settings_line
        content = SetupTeardownSetting(
            self.test_setup,
            self.test_teardown,
            self.suite_setup,
            self.suite_teardown
        ).get_setup_teardown_setting()
        return settings_identification + content
