from infra.utils.timehanldler import get_partial_timestamp
from application.constant import *
from application.testsuite.models import TestSuite
from application.setupteardown.models import SetupTeardown
from application.variable.models import Variable
from application.tag.models import Tag
from application.common.operator.caseoperator import CaseOperator


class SuiteOperator(object):

    def __init__(self, project_id, new_dir_id, create_user, suite_name=None):
        self.project_id = project_id
        self.dir_id = new_dir_id
        self.create_by = create_user
        self.suite_name = suite_name

    def copy_suite_by_id(self, suite_id):
        suite_obj = TestSuite.objects.get(id=suite_id)
        if suite_obj.status == MODULE_STATUS_META.get('Deleted'):
            return None
        return self.copy_suite(suite_obj)

    def copy_suite_by_obj(self, suite_obj):
        return self.copy_suite(suite_obj)

    def copy_suite(self, suite_obj):
        self.generate_new_name(suite_obj.name)
        new_suite = TestSuite.objects.create(
            name=self.suite_name,
            document=suite_obj.document,
            category=suite_obj.category,
            create_by=self.create_by,
            suite_dir_id=self.dir_id,
            timeout=suite_obj.timeout,
            status=suite_obj.status
        )
        old_fixtures = SetupTeardown.objects.filter(
            module_id=suite_obj.id,
            module_type=MODULE_TYPE_META.get('TestSuite')
        )
        new_fixtures = []
        for fixture in old_fixtures.iterator():
            fixture.id = None
            fixture.module_id = new_suite.id
            new_fixtures.append(fixture)
        SetupTeardown.objects.bulk_create(new_fixtures)
        old_variables = Variable.objects.filter(
            module_id=suite_obj.id,
            module_type=MODULE_TYPE_META.get('TestSuite')
        )
        new_variables = []
        for variable in old_variables.iterator():
            variable.id = None
            variable.module_id = new_suite.id
            new_variables.append(variable)
        Variable.objects.bulk_create(new_fixtures)
        old_tags = Tag.objects.filter(
            module_id=suite_obj.id,
            module_type=MODULE_TYPE_META.get('TestSuite')
        )
        new_tags = []
        for tag in old_tags.iterator():
            tag.id = None
            tag.project_id = self.project_id
            tag.module_id = new_suite.id
            new_tags.append(tag)
        Tag.objects.bulk_create(new_tags)
        case_queryset = suite_obj.cases.all()
        for old_case in case_queryset.iterator():
            CaseOperator(
                self.project_id,
                new_suite.id,
                self.create_by
            ).copy_case_by_obj(old_case)
        return new_suite

    def generate_new_name(self, old_name):
        if self.suite_name is not None:
            return
        self.suite_name = old_name + f'-{get_partial_timestamp(4)}copy'
