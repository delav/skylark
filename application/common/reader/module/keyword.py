from application.infra.constant.constants import SPECIAL_SEP
from application.common.reader.module import keyword_map, alias_map


class LibKeywordManager(object):
    """
    handle special keyword, such as FOR, END IF..., function name is the keyword name.
    """

    def __init__(self, keyword):
        self.keyword = keyword
        self.__callback__()

    def __callback__(self):
        func_name = self._get_func_name()
        if not hasattr(self, func_name):
            return
        getattr(self, func_name)()

    def _get_func_name(self):
        keyword_id = self.keyword['keyword_id']
        name = keyword_map[keyword_id]['name']
        self.keyword['keyword_name'] = name
        return '_' + name.lower()

    @property
    def keyword_name(self):
        return self.keyword['keyword_name']

    @property
    def entity_input(self):
        return self.keyword['input_args']

    @property
    def entity_output(self):
        return self.keyword['output_args']

    def _end(self):
        # special keyword 'end' of 'for' loop finish, must be upper
        self.keyword['keyword_name'] = 'END'

    def _for(self):
        # special keyword 'for' loop, must be upper
        self.keyword['keyword_name'] = 'FOR'

    def _run_keyword_if(self):
        # replace alias name to real keyword name in the args
        input_args = self.keyword['input_args']
        args_list = input_args.split(SPECIAL_SEP)
        for i in range(len(args_list)):
            alias = args_list[i]
            if alias not in alias_map:
                continue
            args_list[i] = alias_map[alias]
            new_input_args = SPECIAL_SEP.join(args_list)
            self.keyword['input_args'] = new_input_args

    def _run_keyword_and_continue_on_failure(self):
        # replace alias name to real keyword name in the args
        input_args = self.keyword['input_args']
        args_list = input_args.split(SPECIAL_SEP)
        alias = args_list[0]
        args_list[0] = alias_map[alias]
        new_input_args = SPECIAL_SEP.join(args_list)
        self.keyword['input_args'] = new_input_args
