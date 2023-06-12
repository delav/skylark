from django.conf import settings
from application.testsuite.models import TestSuite
from application.setupteardown.models import SetupTeardown
from application.variable.models import Variable
from application.tag.models import Tag
from application.common.operator.caseoperator import CaseOperator


class SuiteOperator(object):

    def __init__(self, project_id, new_dir_id, create_user):
        self.project_id = project_id
        self.dir_id = new_dir_id
        self.create_by = create_user

    def copy_suite_by_id(self, suite_id):
        suite_obj = TestSuite.objects.get(id=suite_id)
        return self.copy_suite(suite_obj)

    def copy_suite_by_obj(self, suite_obj):
        return self.copy_suite(suite_obj)

    def copy_suite(self, suite_obj):
        new_suite = TestSuite.objects.create(
            name=suite_obj.name,
            document=suite_obj.document,
            category=suite_obj.category,
            create_by=self.create_by,
            suite_dir_id=self.dir_id,
            timeout=suite_obj.timeout,
            status=suite_obj.status
        )
        old_fixtures = SetupTeardown.objects.filter(
            module_id=suite_obj.id,
            module_type=settings.MODULE_TYPE_META.get('TestSuite')
        )
        new_fixtures = []
        for fixture in old_fixtures.iterator():
            fixture.id = None
            fixture.module_id = new_suite.id
            new_fixtures.append(fixture)
        SetupTeardown.objects.bulk_create(new_fixtures)
        old_variables = Variable.objects.filter(
            module_id=suite_obj.id,
            module_type=settings.MODULE_TYPE_META.get('TestSuite')
        )
        new_variables = []
        for variable in old_variables.iterator():
            variable.id = None
            variable.module_id = new_suite.id
            new_variables.append(variable)
        Variable.objects.bulk_create(new_fixtures)
        old_tags = Tag.objects.filter(
            module_id=suite_obj.id,
            module_type=settings.MODULE_TYPE_META.get('TestSuite')
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

