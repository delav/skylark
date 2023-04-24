from django.conf import settings


class InternalTypes:

    @property
    def case_category(self):
        return settings.CATEGORY_META.get('TestCase')

    @property
    def keyword_category(self):
        return settings.CATEGORY_META.get('Keyword')

    @property
    def resource_category(self):
        return settings.CATEGORY_META.get('Resource')

    @property
    def file_category(self):
        return settings.CATEGORY_META.get('ProjectFile')

    @property
    def project_module(self):
        return settings.MODULE_TYPE_META.get('Project')

    @property
    def dir_module(self):
        return settings.MODULE_TYPE_META.get('SuiteDir')

    @property
    def suite_module(self):
        return settings.MODULE_TYPE_META.get('TestSuite')

    @property
    def case_module(self):
        return settings.MODULE_TYPE_META.get('TestCase')
