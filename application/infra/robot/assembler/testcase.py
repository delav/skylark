from application.infra.robot.assembler.config import Config

config = Config()


class EntityKey(object):
    def __init__(self, keyword_name_key, keyword_input_key, keyword_output_key):
        self.name_key = keyword_name_key
        self.input_key = keyword_input_key
        self.output_key = keyword_output_key


class KOCAssembler(object):

    def _combine_koc_str(self, key, *args):
        return config.small_sep + config.small_sep.join([key, *args])

    def _add_koc_setting(self, key, value):
        if not value:
            return ''
        if '|' in value:
            cci_var = value.split('|')
        else:
            cci_var = [value]
        _line = self._combine_koc_str(key, *cci_var)
        return _line

    def _get_koc_line(self, keyword_name, outputs, inputs):
        kw = EntityAssembler(
            keyword_name,
            outputs,
            inputs
        )
        case_line = ''
        # add output parameter
        case_line += config.small_sep + kw.get_output()
        # add keyword name
        case_line += config.small_sep + kw.get_name()
        # add input parameter
        case_line += config.small_sep + kw.get_input()
        # one line per entity
        case_line += config.linefeed
        return case_line


class TestcaseAssembler(KOCAssembler):
    # not use
    setup_prefix = '[Setup]'
    # not use
    teardown_prefix = '[Teardown]'
    timeout_prefix = '[Timeout]'

    def __init__(self, case_name: str, case_timeout: str, entity_list: list,
                 entity_key: EntityKey, case_setup='', case_teardown=''):
        self.name = case_name
        self.timeout = case_timeout
        self.setup = case_setup
        self.teardown = case_teardown
        self.entities = entity_list
        self.entity_key = entity_key

    def _get_koc_timeout(self):
        timeout_line = self._add_koc_setting(self.timeout_prefix, self.timeout)
        return timeout_line + config.linefeed

    def _get_case_setup(self, setup_str):
        pass

    def _get_case_teardown(self, teardown_str):
        pass

    def get_case_content(self):
        case_content = ''
        # add case name
        case_content += self.name + config.linefeed
        # add case timeout
        case_content += self._get_koc_timeout()
        # add case body
        for item in self.entities:
            case_content += self._get_koc_line(
                item.get(self.entity_key.name_key),
                item.get(self.entity_key.output_key),
                item.get(self.entity_key.input_key)
            )
        # end with newline
        case_content += config.linefeed
        return case_content


class KeywordAssembler(KOCAssembler):
    input_prefix = '[Arguments]'
    output_prefix = '[Return]'

    def __init__(self, keyword_name: str, keyword_inputs: str, keyword_outputs: str,
                 entity_list: list, entity_key: EntityKey):
        self.name = keyword_name
        self.inputs = keyword_inputs
        self.outputs = keyword_outputs
        self.entities = entity_list
        self.entity_key = entity_key

    def _get_keyword_input(self):
        arg_line = self._add_koc_setting(self.input_prefix, self.inputs)
        return arg_line + config.linefeed

    def _get_keyword_output(self):
        ret_line = self._add_koc_setting(self.output_prefix, self.outputs)
        return ret_line + config.linefeed

    def get_keyword_content(self):
        keyword_content = ''
        # add keyword name
        keyword_content += self.name + config.linefeed
        # add keyword input
        keyword_content += self._get_keyword_input()
        # add keyword body
        for item in self.entities:
            keyword_content += self._get_koc_line(
                item.get(self.entity_key.name_key),
                item.get(self.entity_key.output_key),
                item.get(self.entity_key.input_key)
            )
        # add keyword output
        keyword_content += self._get_keyword_output()
        # end with newline
        keyword_content += config.linefeed
        return keyword_content


class EntityAssembler(object):

    def __init__(self, name, outputs, inputs):
        self.keyword_name = name
        self.inputs = inputs
        self.outputs = outputs

    def _get_inout(self, outputs_or_inputs):
        inout_str = ''
        if outputs_or_inputs:
            if config.special_sep in outputs_or_inputs:
                cco_var = outputs_or_inputs.split(config.special_sep.special_sep)
                inout_str = config.small_sep.join(cco_var)
            else:
                inout_str = outputs_or_inputs
        return inout_str

    def get_name(self):
        return self.keyword_name

    def get_input(self):
        return self._get_inout(self.inputs)

    def get_output(self):
        return self._get_inout(self.outputs)
