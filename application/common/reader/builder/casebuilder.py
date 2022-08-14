from application.common.reader.builder.basebuilder import BaseBuilder
from application.caseentity.models import CaseEntity
from application.testcase.models import TestCase
from application.libkeyword.models import LibKeyword
from application.userkeyword.models import UserKeyword
from application.infra.utils import KeywordManager, MANAGE_NAMES


class CaseBuilder(BaseBuilder):

    def _splice_case_arg(self, key, *args):
        return self.small_sep + self.small_sep.join([key, *args])

    def _add_inout(self, key, value):
        if not value:
            return ''
        if '|' in value:
            cci_var = value.split('|')
        else:
            cci_var = [value]
        _line = self._splice_case_arg(key, *cci_var)
        return _line

    def _add_case_input(self, raw_content, inputs):
        arg_line = self._add_inout('[Arguments]', inputs)
        return raw_content + arg_line

    def _add_case_output(self, raw_content, outputs):
        ret_line = self._add_inout('[Return]', outputs)
        return raw_content + ret_line

    def _handle_case_content(self, case_item):
        case_id = case_item['id']
        case_name = case_item['case_name']
        # case name
        case_content = case_name + self.linefeed
        case_content = self._add_case_input(case_content, case_item["inputs"])
        case_entity = CaseEntity.objects.filter(test_case_id=case_id).values(
            'input_parm', 'output_parm', 'seq_number', 'keyword', 'user_keyword').order_by('seq_number')
        if not case_entity.exists():
            # case body is null, add blank line
            case_content += self.linefeed
            return case_content
        # compose case body
        for cc in case_entity.iterator():
            entity_line = EntityBuilder(cc).get_entity()
            case_content += entity_line
        case_content = self._add_case_output(case_content, case_item["outputs"])
        # test case end with newline
        case_content += self.linefeed
        return case_content

    def _handle_case_queryset(self, case_queryset):
        content = ''
        for case_item in case_queryset.iterator():
            case_content = self._handle_case_content(case_item)
            content += case_content + self.linefeed
        return content

    def get_case_by_ids(self, ids: list):
        if not ids:
            return ''
        cases = TestCase.objects.filter(id__in=ids).values(
                'id', 'case_name', 'inputs', 'outputs'
            )
        return self._handle_case_queryset(cases)

    def get_case_by_suite(self, suite):
        cases = suite.cases
        return self._handle_case_queryset(cases)


class EntityBuilder(BaseBuilder):
    def __init__(self, entity_dict):
        self.entity = entity_dict

    def get_entity(self):
        entity_line = ''
        # start with four space
        entity_line += self.small_sep
        # replicator with output parameter
        if self.entity['output_parm']:
            if self.special_sep in self.entity['output_parm']:
                cco_var = self.entity['output_parm'].split(self.special_sep)
                out_var = self.small_sep.join(cco_var) + self.small_sep
            else:
                out_var = self.entity['output_parm'] + self.small_sep
            entity_line += out_var
        # replicator with keyword name
        keyword_name = KeywordBuilder(self.entity).get_keyword_info()
        entity_line += keyword_name + self.small_sep
        # replicator with input parameter
        if self.entity['input_parm']:
            if self.special_sep in self.entity['input_parm']:
                cci_var = self.entity['input_parm'].split(self.special_sep)
                in_var = self.small_sep.join(cci_var)
            else:
                in_var = self.entity['input_parm']
            entity_line += in_var
        # one line per entity
        entity_line += self.linefeed
        return entity_line


class KeywordBuilder(BaseBuilder):
    def __init__(self, entity):
        self.entity = entity

    @property
    def is_lib(self):
        return self.entity['keyword'] is not None

    def get_keyword_info(self):
        return self.handle_lib_keyword() if self.is_lib else self.handle_user_keyword()

    def handle_lib_keyword(self):
        keyword_item = LibKeyword.objects.filter(id=self.entity['keyword_id']).values('name').first()
        km = KeywordManager(self.entity)
        kw_name = keyword_item['name']
        if hasattr(km, kw_name):
            cc = getattr(km, kw_name)()
            if kw_name in MANAGE_NAMES:
                keyword_item['name'] = cc.pop('name')
        keyword_name = keyword_item['name']
        return keyword_name

    def handle_user_keyword(self):
        uk = UserKeyword.objects.filter(id=self.entity['user_keyword_id']).first()
        keyword_name = uk.case.name
        return keyword_name
