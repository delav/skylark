from loguru import logger
from application.infra.builder.base import BaseBuilder
from application.caseentity.models import CaseEntity
from application.testcase.models import TestCase
from application.testsuite.models import TestSuite
from application.suitedir.models import SuiteDir
from application.variable.models import Variable
from application.libkeyword.models import LibKeyword
from application.userkeyword.models import UserKeyword
from .keywordhanlderr import KeywordManager
from .keywordalias import manage_names


class SuiteContentReader(BaseBuilder):

    def __init__(self):
        pass

    @staticmethod
    def _is_not_null(value):
        return value is not None and value != ''

    def get_suite_content(self):
        pass

    def _get_cases(self, *ids):
        content = ''
        cases = TestCase.objects.filter(id__in=ids, deleted=False).values(
                'id', 'case_name', 'inputs', 'outputs'
            )
        for case_item in cases.iterator():
            case_id = case_item['id']
            case_name = case_item['case_name']
            # case name
            content += (case_name + self.linefeed)
            case_entity = CaseEntity.objects.filter(test_case_id=case_id).values(
                'input_parm', 'output_parm', 'seq_number', 'keyword', 'user_keyword').order_by('seq_number')
            if not case_entity.exists():
                logger.info('测试用例内容为空: {}'.format(case_name))
                # case content is null, add blank line
                content += self.linefeed
                continue
            # compose case content
            for cc in case_entity.iterator():
                entity_line = ''
                # start with four space
                entity_line += self.small_sep
                # handler with output parameter
                if self._is_not_null(cc['output_parm']):
                    if self.special_sep in cc['output_parm']:
                        cco_var = cc['output_parm'].split(self.special_sep)
                        out_var = self.small_sep.join(cco_var) + self.small_sep
                    else:
                        out_var = cc['output_parm'] + self.small_sep
                    entity_line += out_var
                # handler with keyword name
                if cc['keyword'] is not None:
                    keyword_item = LibKeyword.objects.filter(id=cc['keyword_id']).values('name').first()
                    km = KeywordManager(cc)
                    kw_name = keyword_item['name']
                    if hasattr(km, kw_name):
                        cc = getattr(km, kw_name)()
                        if kw_name in manage_names:
                            keyword_item['name'] = cc.pop('name')
                    keyword_name = keyword_item['name']
                else:
                    uk = UserKeyword.objects.filter(id=cc['user_keyword_id']).first()
                    keyword_name = uk.case.name
                entity_line += keyword_name + self.small_sep
                # handler with input parameter
                if self._is_not_null(cc['input_parm']):
                    if self.special_sep in cc['input_parm']:
                        cci_var = cc['input_parm'].split(self.special_sep)
                        in_var = self.small_sep.join(cci_var)
                    else:
                        in_var = cc['input_parm']
                    entity_line += in_var
                # one line per entity
                entity_line += self.linefeed
            # test case end with newline
            content += self.linefeed
        logger.info('获取测试用例内容完成: {}'.format(ids))