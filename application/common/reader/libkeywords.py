from application.libkeyword.models import LibKeyword
from application.libkeyword.serializers import LibKeywordSerializers
from application.infra.constant.constants import SPECIAL_SEP


class LibKeywordMap(object):

    def __init__(self):
        self.keyword_id_map = {}
        self.name_alias_map = {}
        self.alias_name_map = {}
        self._init_data()

    def _init_data(self):
        keywords = LibKeyword.objects.all()
        for item in keywords.iterator():
            ser_item = LibKeywordSerializers(item).data
            self.keyword_id_map[item.id] = ser_item
            name = ser_item['name']
            alias = ser_item['ext_name']
            self.name_alias_map[name] = alias
            self.alias_name_map[alias] = name

    def get_keyword_map(self):
        return self.keyword_id_map

    def get_alias_map(self):
        return self.alias_name_map

    def get_name_map(self):
        return self.name_alias_map


class LibKeywordManager(object):
    """
    handle special keyword, such as FOR, END IF..., function name is the keyword name.
    """

    def __init__(self, keyword, map_instance: LibKeywordMap):
        self.keyword = keyword
        self.map_ins = map_instance
        self.__callback__()

    def __callback__(self):
        func_name = self._get_func_name()
        if not hasattr(self, func_name):
            return
        getattr(self, func_name)()

    def _get_func_name(self):
        keyword_map = self.map_ins.get_keyword_map()
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
        alias_key_map = self.map_ins.get_alias_map()
        input_args = self.keyword['input_args']
        args_list = input_args.split(SPECIAL_SEP)
        for i in range(len(args_list)):
            alias = args_list[i]
            if alias not in alias_key_map:
                continue
            args_list[i] = alias_key_map[alias]
            new_input_args = SPECIAL_SEP.join(args_list)
            self.keyword['input_args'] = new_input_args

    def _run_keyword_and_continue_on_failure(self):
        #
        alias_key_map = self.map_ins.get_alias_map()
        input_args = self.keyword['input_args']
        args_list = input_args.split(SPECIAL_SEP)
        alias = args_list[0]
        args_list[0] = alias_key_map[alias]
        new_input_args = SPECIAL_SEP.join(args_list)
        self.keyword['input_args'] = new_input_args

