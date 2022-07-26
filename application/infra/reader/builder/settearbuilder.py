from application.infra.reader.builder.basebuilder import BaseBuilder
from application.setupteardown.models import SetupTeardown


class SetTearBuilder(BaseBuilder):
    """
    gsuite or dir or project setup/teardown
    """
    def __init__(self, module_id, module_type):
        self.module_id = module_id
        self.module_type = module_type

    @staticmethod
    def _clear_spaces(value):
        """
        remove spaces in strings
        :param value: string
        :return: string
        """
        return value.replace(' ', '')

    @staticmethod
    def _is_not_null(value):
        """
        if the value is not null
        :param value: obj
        :return: bool
        """
        return value is not None and value != ''

    def _splice_settear(self, key, *args):
        """
        splice the setup/teardown for header
        :param key:
        :param args:
        :return:
        """
        return key + self.large_sep + self.small_sep.join(*args) + self.linefeed

    def _handler_step(self, step_str, prefix):
        """
        the setup/teardown if is has multiple keywords
        :param step_str: value
        :param prefix: setup/teardown key
        :return: string
        """
        module_setup_str = ''
        if self._is_not_null(step_str):
            if '|' in step_str:
                module_setup_list = step_str.split('|')
                if 'AND' in module_setup_list:
                    module_setup_list.insert(0, 'RUN KEYWORDS')
            else:
                module_setup_list = [step_str]
            module_setup_str = self._splice_settear(prefix, *module_setup_list)
        return module_setup_str

    def setting_info(self):
        """
        get setup/teardown info for header from obj
        :return: string
        """
        setup_teardown_str = ''
        try:
            st_obj = SetupTeardown.objects.get(
                module_id=self.module_id,
                module_type=self.module_type
            )
            module_setup = self._clear_spaces(st_obj.module_setup)
            module_teardown = self._clear_spaces(st_obj.module_teardown)
            test_setup = self._clear_spaces(st_obj.test_setup)
            test_teardown = self._clear_spaces(st_obj.test_teardown)
        except (Exception,):
            return setup_teardown_str

        module_setup_str = self._handler_step(module_setup, 'Suite Setup')
        setup_teardown_str += module_setup_str

        module_teardown_str = self._handler_step(module_teardown, 'Suite Teardown')
        setup_teardown_str += module_teardown_str

        test_setup_str = self._handler_step(test_setup, 'Test Setup')
        setup_teardown_str += test_setup_str

        test_teardown_str = self._handler_step(test_teardown, 'Test Teardown')
        setup_teardown_str += test_teardown_str

        return setup_teardown_str
