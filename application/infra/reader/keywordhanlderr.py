import copy
from loguru import logger
from application.infra.builder.base import BaseBuilder
from .keywordalias import KeyAliasDict

alias_key_dict = KeyAliasDict().get_alias_key()


class KeywordManager(BaseBuilder):

    def __init__(self, keyword):
        self.keyword = keyword
        # print(self.keyword)

    def end(self):
        new_keyword = copy.deepcopy(self.keyword)
        try:
            new_keyword['name'] = 'END'
            self.keyword = new_keyword
        except Exception as e:
            logger.info('处理特殊关键字【end】异常: {}'.format(e))
        return self.keyword

    def for_list(self):
        new_keyword = copy.deepcopy(self.keyword)
        try:
            new_keyword['name'] = 'FOR'
            input_args = self.keyword['input_parm']
            args_list = input_args.split(self.special_sep)
            args_list.insert(1, 'IN')
            new_input_args = self.special_sep.join(args_list)
            new_keyword['input_parm'] = new_input_args
            self.keyword = new_keyword
        except Exception as e:
            logger.info('处理特殊关键字【for_list】异常: {}'.format(e))
        return self.keyword

    def for_dict(self):
        new_keyword = copy.deepcopy(self.keyword)
        try:
            new_keyword['name'] = 'FOR'
            input_args = self.keyword['input_parm']
            args_list = input_args.split(self.special_sep)
            args_list.insert(2, 'IN')
            new_input_args = self.special_sep.join(args_list)
            new_keyword['input_parm'] = new_input_args
            self.keyword = new_keyword
        except Exception as e:
            logger.info('处理特殊关键字【for_dict】异常: {}'.format(e))
        return self.keyword

    def run_keyword_and_continue_on_failure(self):
        new_keyword = copy.deepcopy(self.keyword)
        try:
            input_args = self.keyword['input_parm']
            args_list = input_args.split(self.special_sep)
            alias = args_list[0]
            keyword = alias_key_dict[alias]
            args_list[0] = keyword
            new_input_args = self.special_sep.join(args_list)
            new_keyword['input_parm'] = new_input_args
            self.keyword = new_keyword
        except Exception as e:
            logger.info('处理特殊关键字【run_keyword_and_continue_on_failure】异常: {}'.format(e))
        return self.keyword

    def run_keyword_if(self):
        new_keyword = copy.deepcopy(self.keyword)
        try:
            input_args = self.keyword['input_parm']
            args_list = input_args.split(self.special_sep)
            for i in range(len(args_list)):
                alias = args_list[i]
                if alias in alias_key_dict:
                    keyword = alias_key_dict[alias]
                    args_list[i] = keyword
                    new_input_args = self.special_sep.join(args_list)
                    new_keyword['input_parm'] = new_input_args
                    self.keyword = new_keyword
        except Exception as e:
            logger.info('处理特殊关键字【run_keyword_if】异常: {}'.format(e))
        return self.keyword
