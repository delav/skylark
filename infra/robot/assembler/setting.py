from infra.robot.assembler.configure import Config


config = Config()


class Settings(object):

    def _combine_setting_str(self, key, value):
        """
        combine setting prefix and value to string
        :param key: prefix
        :param value: value
        :return: combine str
        """
        value = value.replace('\\', '/')
        return config.large_sep.join([key, value]) + config.linefeed

    def get_settings(self, prefix, setting):
        """
        get settings
        :return: settings str
        """
        setting_str = ''
        if isinstance(setting, str):
            return self._combine_setting_str(prefix, setting)
        return setting_str


class LibrarySetting(Settings):
    library_prefix = 'Library'

    def __init__(self, library_list: list):
        self.library_list = library_list

    def get_library_setting(self):
        libraries = ''
        for library in self.library_list:
            libraries += self.get_settings(self.library_prefix, library)
        return libraries


class ResourceSetting(Settings):
    resource_prefix = 'Resource'

    def __init__(self, resource_list: list):
        self.resource_list = resource_list

    def get_resource_setting(self):
        resources = ''
        for resource in self.resource_list:
            resources += self.get_settings(self.resource_prefix, resource)
        return resources


class TimeoutSetting(Settings):
    timeout_prefix = 'Test Timeout'

    def __init__(self, timeout_str: str):
        self.timeout_str = timeout_str

    def get_timeout_setting(self):
        if not self.timeout_str:
            return ''
        return self.get_settings(self.timeout_prefix, self.timeout_str)


class SetupTeardownSetting(Settings):
    test_setup_prefix = 'Test Setup'
    test_teardown_prefix = 'Test Teardown'
    suite_setup_prefix = 'Suite Setup'
    suite_teardown_prefix = 'Suite Teardown'
    multi_keyword_prefix = 'RUN KEYWORDS'

    def __init__(self, test_setup_str: str, test_teardown_str: str,
                 suite_setup_str: str, suite_teardown_str: str):
        self.test_setup_str = test_setup_str
        self.test_teardown_str = test_teardown_str
        self.suite_setup_str = suite_setup_str
        self.suite_teardown_str = suite_teardown_str

    def _contain(self, word_list, word):
        for item in word_list:
            if item.strip().upper() == word:
                return True
        return False

    def _handler_step(self, step_str):
        """
        the setup/teardown if it has multiple keywords
        :param step_str: value
        :return: string
        """
        new_step_str = ''
        if step_str:
            if '|' in step_str:
                step_list = step_str.split('|')
                if self._contain(step_list, 'AND'):
                    step_list.insert(0, self.multi_keyword_prefix)
            else:
                step_list = [step_str]
            new_step_str = config.small_sep.join(step_list)
        return new_step_str

    def get_setup_teardown_setting(self):
        setup_teardown_setting = ''
        if self.test_setup_str:
            format_test_setup = self._handler_step(self.test_setup_str)
            setup_teardown_setting += self.get_settings(self.test_setup_prefix, format_test_setup)
        if self.test_teardown_str:
            format_test_teardown = self._handler_step(self.test_teardown_str)
            setup_teardown_setting += self.get_settings(self.test_teardown_prefix, format_test_teardown)
        if self.suite_setup_str:
            format_suite_setup = self._handler_step(self.suite_setup_str)
            setup_teardown_setting += self.get_settings(self.suite_setup_prefix, format_suite_setup)
        if self.suite_teardown_str:
            format_suite_teardown = self._handler_step(self.suite_teardown_str)
            setup_teardown_setting += self.get_settings(self.suite_teardown_prefix, format_suite_teardown)
        return setup_teardown_setting


class VariableSetting(Settings):
    variable_prefix = 'Variables'

    def __init__(self, py_file_list):
        self.variable_files = py_file_list

    def get_variable_setting(self):
        variables = ''
        for file in self.variable_files:
            variables += self.get_settings(self.variable_prefix, file)
        return variables


class TagSetting(Settings):
    tag_prefix = 'Force Tags'

    def __init__(self, tag_list):
        self.tag_list = tag_list

    def get_tag_setting(self):
        if not self.tag_list:
            return ''
        tags = config.large_sep.join(self.tag_list)
        return self.get_settings(self.tag_prefix, tags)
